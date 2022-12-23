#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки

Тип блока: БМЗ АПШ 4.0
Производитель: Нет производителя, Горэкс-Светотехника

"""

import sys
import logging

from general_func.exception import *
from general_func.database import *
from general_func.modbus import *
from general_func.procedure import *
from general_func.reset import ResetRelay, ResetProtection
from general_func.subtest import ProcedureFull
from gui.msgbox_1 import *
from gui.msgbox_2 import *

__all__ = ["TestBMZAPSH4"]


class TestBMZAPSH4:

    def __init__(self):
        self.proc = Procedure()
        self.proc_full = ProcedureFull()
        self.reset_relay = ResetRelay()
        self.reset_protect = ResetProtection()
        self.ctrl_kl = CtrlKL()
        self.di_read = DIRead()
        self.mysql_conn = MySQLConnect()

        self.list_ust_num = (1, 2, 3, 4, 5)
        self.list_ust = (9.84, 16.08, 23.28, 34.44, 50.04)

        self.list_delta_t = []
        self.list_result = []

        self.coef_volt: float = 0.0
        self.health_flag: bool = False

        logging.basicConfig(
            filename="C:\\Stend\\project_class\\log\\TestBMZAPSh4.log",
            filemode="w",
            level=logging.DEBUG,
            encoding="utf-8",
            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('WARNING')
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))

    def st_test_10(self) -> bool:
        """
        # Тест 1. Проверка исходного состояния блока:
        """
        self.di_read.di_read('in_a0')
        msg_1 = "Установите переключатель уставок на блоке в положение 1"
        if my_msg(msg_1):
            pass
        else:
            return False
        self.mysql_conn.mysql_ins_result('идёт тест 1.1', '1')
        self.ctrl_kl.ctrl_relay('KL66', True)
        if self.reset_protection(test_num=1, subtest_num=1.0, err_code=342):
            return True
        return False

    def st_test_11(self) -> bool:
        """
        1.1.2. Проверка отсутствия короткого замыкания на входе измерительной части блока:
        1.2. Определение коэффициента Кс отклонения фактического напряжения от номинального.
        :return:
        """
        if self.proc_full.procedure_1_full(test_num=1, subtest_num=1.1, coef_min_volt=0.9):
            self.coef_volt = self.proc_full.procedure_2_full(test_num=1, subtest_num=1.2)
            return True
        return False

    def st_test_20(self) -> bool:
        """
        Тест 2. Проверка срабатывания защиты блока по уставкам
        """
        self.logger.debug("запуск теста 2")
        self.mysql_conn.mysql_ins_result('идёт тест 2.0', '1')
        k = 0
        for i in self.list_ust:
            msg_4 = 'Установите регулятор уставок на блоке в положение:'
            msg_result = my_msg_2(f'{msg_4} {self.list_ust_num[k]}')
            if msg_result == 0:
                pass
            elif msg_result == 1:
                return False
            elif msg_result == 2:
                self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[k]} пропущена')
                self.list_delta_t.append('пропущена')
                k += 1
                continue
            self.mysql_conn.mysql_ins_result(f'уставка {self.list_ust_num[k]}', '4')
            if self.proc.procedure_x4_to_x5(coef_volt=self.coef_volt, setpoint_volt=i):
                pass
            else:
                self.mysql_conn.mysql_ins_result('неисправен TV1', '1')
            # 2.1.  Проверка срабатывания блока от сигнала нагрузки:
            calc_delta_t = self.ctrl_kl.ctrl_ai_code_v0(111)
            self.logger.debug(f'delta t:\t {calc_delta_t:.1f}')
            self.list_delta_t.append(f'{calc_delta_t:.1f}')
            self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[k]} дельта t: {calc_delta_t:.1f}')
            in_a1, *_ = self.di_read.di_read('in_a1')
            if in_a1 is True:
                self.logger.debug("вход 1 соответствует")
                self.reset_relay.stop_procedure_3()
                if self.reset_protection(test_num=2, subtest_num=2.2):
                    k += 1
                    continue
                else:
                    return False
            else:
                self.logger.debug("вход 1 не соответствует")
                self.mysql_conn.mysql_ins_result('неисправен', '1')
                self.mysql_conn.mysql_error(344)
                self.reset_relay.stop_procedure_3()
                if self.subtest_2_2(i=i, k=k):
                    if self.reset_protection(test_num=2, subtest_num=2.2):
                        k += 1
                        continue
                    else:
                        return False
                else:
                    return False
        self.mysql_conn.mysql_ins_result('исправен', '1')
        self.logger.debug("тест 2 пройден")
        self.logger.debug("сбрасываем все и завершаем проверку")
        for t1 in range(len(self.list_delta_t)):
            self.list_result.append((self.list_ust_num[t1], self.list_delta_t[t1]))
        self.mysql_conn.mysql_ubtz_btz_result(self.list_result)
        return True

    def subtest_2_2(self, i, k):
        if self.reset_protection(test_num=2, subtest_num=2.2):
            pass
        else:
            return False
        if self.proc.procedure_1_24_34(coef_volt=self.coef_volt, setpoint_volt=i, factor=1.1):
            pass
        else:
            return False
        calc_delta_t = self.ctrl_kl.ctrl_ai_code_v0(111)
        self.logger.info(f'delta t: {calc_delta_t:.1f}')
        self.list_delta_t[-1] = f'{calc_delta_t:.1f}'
        self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[k]} дельта t: {calc_delta_t:.1f}')
        in_a1, *_ = self.di_read.di_read('in_a1')
        if in_a1 is True:
            pass
        else:
            self.logger.debug("вход 1 не соответствует")
            self.mysql_conn.mysql_ins_result('неисправен', '1')
            self.mysql_conn.mysql_error(346)
            return False
        self.reset_relay.stop_procedure_3()
        return True

    def reset_protection(self, *, test_num: int, subtest_num: float, err_code: int = 344) -> bool:
        """
        Метод сброса защиты блока.
        :param test_num:
        :param subtest_num:
        :param err_code:
        :return:
        """
        self.logger.debug(f"сброс защит блока, тест {test_num}, подтест {subtest_num}")
        self.reset_protect.sbros_zashit_kl1()
        in_a1, *_ = self.di_read.di_read('in_a1')
        if in_a1 is False:
            self.logger.debug("вход 1 соответствует")
            return True
        self.logger.debug("вход 1 не соответствует")
        self.mysql_conn.mysql_ins_result('неисправен', f'{test_num}')
        self.mysql_conn.mysql_error(err_code)
        return False

    def st_test_bmz_apsh_4(self) -> [bool, bool]:
        if self.st_test_10():
            if self.st_test_11():
                if self.st_test_20():
                    return True, self.health_flag
        return False, self.health_flag


if __name__ == '__main__':
    test_bmz_apsh_4 = TestBMZAPSH4()
    reset_test_bmz_apsh_4 = ResetRelay()
    mysql_conn_bmz_apsh_4 = MySQLConnect()
    try:
        test, health_flag = test_bmz_apsh_4.st_test_bmz_apsh_4()
        if test and not health_flag:
            mysql_conn_bmz_apsh_4.mysql_block_good()
            my_msg('Блок исправен', 'green')
        else:
            mysql_conn_bmz_apsh_4.mysql_block_bad()
            my_msg('Блок неисправен', 'red')
    except OSError:
        my_msg("ошибка системы", 'red')
    except SystemError:
        my_msg("внутренняя ошибка", 'red')
    except ModbusConnectException as mce:
        my_msg(f'{mce}', 'red')
    except HardwareException as hwe:
        my_msg(f'{hwe}', 'red')
    finally:
        reset_test_bmz_apsh_4.reset_all()
        sys.exit()
