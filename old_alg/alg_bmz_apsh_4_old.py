#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки

Тип блока	Производитель
БМЗ АПШ 4.0	Нет производителя
БМЗ АПШ 4.0	Горэкс-Светотехника

"""

import sys
import logging

from time import sleep

from .gen_func_procedure import *
from .gen_func_utils import *
from .my_msgbox import *
from .my_msgbox_2 import *
from .gen_mb_client import *
from .gen_mysql_connect import *

__all__ = ["TestBMZAPSH4"]


class TestBMZAPSH4(object):

    def __init__(self):
        self.__proc = Procedure()
        self.__reset = ResetRelay()
        self.__ctrl_kl = CtrlKL()
        self.__read_mb = ReadMB()
        self.__mysql_conn = MySQLConnect()
        self.__fault = Bug(True)

        self.list_ust_num = (1, 2, 3, 4, 5)
        self.list_ust = (9.84, 16.08, 23.28, 34.44, 50.04)

        self.list_delta_t = []
        self.list_result = []

        self.coef_volt: float = 0.0
        self.health_flag: bool = False

        logging.basicConfig(filename="C:\Stend\project_class\TestBMZAPSh4.log",
                            filemode="w",
                            level=logging.DEBUG,
                            encoding="utf-8",
                            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('WARNING')
        self.logger = logging.getLogger(__name__)

    def st_test_10_bmz_apsh_4(self) -> bool:
        """
        # Тест 1. Проверка исходного состояния блока:
        """
        self.__inputs_a0()
        msg_1 = "Установите переключатель уставок на блоке в положение 1"
        if my_msg(msg_1):
            pass
        else:
            return False
        self.__mysql_conn.mysql_ins_result('идёт тест 1.1', '1')
        self.__ctrl_kl.ctrl_relay('KL66', True)
        self.__reset.sbros_zashit_kl1()
        in_a1 = self.__inputs_a()
        if in_a1 is False:
            pass
        else:
            self.__fault.debug_msg("вход 1 не соответствует", 1)
            self.__mysql_conn.mysql_ins_result('неисправен', '1')
            self.__mysql_conn.mysql_error(342)
            return False
        self.__fault.debug_msg("вход 1 соответствует", 4)
        return True

    def st_test_11_bmz_apsh_4(self) -> bool:
        """
        Проверка на КЗ входа блока, и межвиткового замыкания трансформатора
        """
        self.__mysql_conn.mysql_ins_result('идёт тест 1.2', '1')
        meas_volt_ust = self.__proc.procedure_1_21_31()
        if meas_volt_ust != 0.0:
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен TV1', '1')
        self.__ctrl_kl.ctrl_relay('KL63', True)
        meas_volt = self.__read_mb.read_analog()
        if 0.9 * meas_volt_ust <= meas_volt <= 1.1 * meas_volt_ust:
            pass
        else:
            self.__fault.debug_msg("напряжение не соответствует", 1)
            self.__mysql_conn.mysql_ins_result('неисправен', '1')
            self.__mysql_conn.mysql_error(343)
            self.__reset.sbros_kl63_proc_1_21_31()
            return False
        self.__fault.debug_msg(f'напряжение соответствует заданному \t {meas_volt:.2f}', 'orange')
        self.__reset.sbros_kl63_proc_1_21_31()
        return True

    def st_test_12_bmz_apsh_4(self) -> bool:
        """
        Коэффициент сети
        """
        self.__mysql_conn.mysql_ins_result('идёт тест 1.3', '1')
        coef_volt = self.__proc.procedure_1_22_32()
        if coef_volt != 0.0:
            pass
        else:
            self.__reset.stop_procedure_32()
            self.__mysql_conn.mysql_ins_result('неисправен', '1')
            return False
        self.__mysql_conn.mysql_ins_result('тест 1 исправен', '1')
        self.__reset.stop_procedure_32()
        return True

    def st_test_20_bmz_apsh_4(self) -> bool:
        """
        Тест 2. Проверка срабатывания защиты блока по уставкам
        """
        self.__fault.debug_msg("запуск теста 2", 3)
        self.__mysql_conn.mysql_ins_result('идёт тест 2', '1')
        k = 0
        for i in self.list_ust:
            msg_4 = 'Установите регулятор уставок на блоке в положение:'
            msg_result = my_msg_2(f'{msg_4} {self.list_ust_num[k]}')
            if msg_result == 0:
                pass
            elif msg_result == 1:
                return False
            elif msg_result == 2:
                self.__mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[k]} пропущена')
                self.list_delta_t.append('пропущена')
                k += 1
                continue
            self.__mysql_conn.mysql_ins_result(f'уставка {self.list_ust_num[k]}', '4')
            if self.__proc.procedure_x4_to_x5(coef_volt=self.coef_volt, setpoint_volt=i):
                pass
            else:
                self.__mysql_conn.mysql_ins_result('неисправен TV1', '1')
            # 2.1.  Проверка срабатывания блока от сигнала нагрузки:
            calc_delta_t = self.__ctrl_kl.ctrl_ai_code_v0(111)
            self.__fault.debug_msg(f'delta t:\t {calc_delta_t:.1f}', 2)
            self.list_delta_t.append(f'{calc_delta_t:.1f}')
            self.__mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[k]} дельта t: {calc_delta_t:.1f}')
            in_a1 = self.__inputs_a()
            if in_a1 is True:
                self.__fault.debug_msg("вход 1 соответствует", 4)
                self.__reset.stop_procedure_3()
                if self.__sbros_zashit():
                    k += 1
                    continue
                else:
                    return False
            else:
                self.__fault.debug_msg("вход 1 не соответствует", 1)
                self.__mysql_conn.mysql_ins_result('неисправен', '1')
                self.__mysql_conn.mysql_error(344)
                self.__reset.stop_procedure_3()
                if self.__subtest_2_2(i=i, k=k):
                    if self.__sbros_zashit():
                        k += 1
                        continue
                    else:
                        return False
                else:
                    return False
        self.__mysql_conn.mysql_ins_result('исправен', '1')
        self.__fault.debug_msg("тест 2 пройден", 3)
        self.__fault.debug_msg("сбрасываем все и завершаем проверку", 3)
        for t1 in range(len(self.list_delta_t)):
            self.list_result.append((self.list_ust_num[t1], self.list_delta_t[t1]))
        self.__mysql_conn.mysql_ubtz_btz_result(self.list_result)
        return True

    def __subtest_2_2(self, i, k):
        if self.__sbros_zashit():
            pass
        else:
            return False
        if self.__proc.procedure_1_25_35(coef_volt=self.coef_volt, setpoint_volt=i):
            pass
        else:
            return False
        calc_delta_t = self.__ctrl_kl.ctrl_ai_code_v0(111)
        self.__fault.debug_msg(f'delta t: {calc_delta_t:.1f}', 'orange')
        self.list_delta_t[-1] = f'{calc_delta_t:.1f}'
        self.__mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[k]} дельта t: {calc_delta_t:.1f}')
        in_a1 = self.__inputs_a()
        if in_a1 is True:
            pass
        else:
            self.__fault.debug_msg("вход 1 не соответствует", 1)
            self.__mysql_conn.mysql_ins_result('неисправен', '1')
            self.__mysql_conn.mysql_error(346)
            return False
        self.__reset.stop_procedure_3()
        return True

    def __sbros_zashit(self):
        self.__ctrl_kl.ctrl_relay('KL1', True)
        sleep(1.5)
        self.__ctrl_kl.ctrl_relay('KL1', False)
        sleep(2)
        in_a1 = self.__inputs_a()
        if in_a1 is False:
            pass
        else:
            self.__fault.debug_msg("вход 1 не соответствует", 1)
            self.__mysql_conn.mysql_ins_result('неисправен', '1')
            self.__mysql_conn.mysql_error(344)
            return False
        self.__fault.debug_msg("вход 1 соответствует", 4)
        return True

    def __inputs_a0(self):
        in_a0 = self.__read_mb.read_discrete(0)
        if in_a0 is None:
            # logging.error(f'нет связи с контроллером')
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_a0

    def __inputs_a(self):
        in_a1 = self.__read_mb.read_discrete(1)
        if in_a1 is None:
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_a1

    def __inputs_b(self):
        in_b0 = self.__read_mb.read_discrete(8)
        in_b1 = self.__read_mb.read_discrete(9)
        if in_b0 is None or in_b1 is None:
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_b0, in_b1

    def st_test_bmz_apsh_4(self) -> bool:
        if self.st_test_10_bmz_apsh_4():
            if self.st_test_11_bmz_apsh_4():
                if self.st_test_12_bmz_apsh_4():
                    if self.st_test_20_bmz_apsh_4():
                        return True
        return False

    def full_test_bmz_apsh_4(self):
        try:
            if self.st_test_bmz_apsh_4():
                self.__mysql_conn.mysql_block_good()
                my_msg('Блок исправен', 'green')
            else:
                self.__mysql_conn.mysql_block_bad()
                my_msg('Блок неисправен', 'red')
        except OSError:
            my_msg("ошибка системы", 'red')
        except SystemError:
            my_msg("внутренняя ошибка", 'red')
        except ModbusConnectException as mce:
            self.__fault.debug_msg(mce, 'red')
            my_msg(f'{mce}', 'red')
        except HardwareException as hwe:
            my_msg(f'{hwe}', 'red')
        finally:
            self.__reset.reset_all()
            sys.exit()


if __name__ == '__main__':
    test_bmz_apsh_4 = TestBMZAPSH4()
    test_bmz_apsh_4.full_test_bmz_apsh_4()
    # reset_test_bmz_apsh_4 = ResetRelay()
    # mysql_conn_bmz_apsh_4 = MySQLConnect()
    # fault = Bug(True)
    # try:
    #     if test_bmz_apsh_4.st_test_bmz_apsh_4():
    #         mysql_conn_bmz_apsh_4.mysql_block_good()
    #         my_msg('Блок исправен', 'green')
    #     else:
    #         mysql_conn_bmz_apsh_4.mysql_block_bad()
    #         my_msg('Блок неисправен', 'red')
    # except OSError:
    #     my_msg("ошибка системы", 'red')
    # except SystemError:
    #     my_msg("внутренняя ошибка", 'red')
    # except ModbusConnectException as mce:
    #     fault.debug_msg(mce, 'red')
    #     my_msg(f'{mce}', 'red')
    # except HardwareException as hwe:
    #     my_msg(f'{hwe}', 'red')
    # finally:
    #     reset_test_bmz_apsh_4.reset_all()
    #     sys.exit()
