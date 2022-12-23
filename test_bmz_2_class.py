#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки

Тип блока	Производитель	    Уникальный номер
БМЗ-2	    Нет производителя	        77
БМЗ-2	    ТЭТЗ-Инвест	                78
БМЗ-2	    Строй-энергомаш	            79

"""

import sys
import logging

from time import sleep

from my_msgbox import *
from my_msgbox_2 import *
from gen_func_procedure import *
from gen_func_utils import *
from gen_mb_client import *
from gen_mysql_connect import *

__all__ = ['TestBMZ2']


class TestBMZ2(object):

    def __init__(self):
        self.__reset = ResetRelay()
        self.__proc = Procedure()
        self.__ctrl_kl = CtrlKL()
        self.__read_mb = ReadMB()
        self.__mysql_conn = MySQLConnect()
        self.__fault = Bug(True)

        self.ust_test = 80.0
        self.list_ust_num = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
        # расчетный лист уставок (при тестировании данных напряжений не хватает)
        # ust = (32.2, 40.2, 48.2, 56.3, 64.3, 72.3, 80.4, 88.4, 96.5, 104.5, 112.5)
        self.list_ust_volt = (34.2, 42.2, 50.2, 58.3, 66.3, 74.3, 82.4, 90.4, 98.5, 106.5, 114.5)
        self.list_delta_t = []
        self.list_delta_percent = []
        self.list_result = []

        self.coef_volt: float = 0.0
        self.calc_delta_t: float = 0.0
        self.health_flag: bool = False

        self.msg_1 = "Переключите тумблер на корпусе блока в положение " \
                     "«Работа» и установите регулятор уставок в положение 1"
        self.msg_2 = "Переключите тумблер на корпусе блока в положение «Проверка»."
        self.msg_3 = "Переключите тумблер на корпусе блока в положение «Работа»"
        self.msg_4 = 'Установите регулятор уставок на блоке в положение '

        logging.basicConfig(filename="C:\Stend\project_class\TestBMZ2.log",
                            filemode="w",
                            level=logging.DEBUG,
                            encoding="utf-8",
                            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('WARNING')
        self.logger = logging.getLogger(__name__)

    def st_test_10_bmz_2(self) -> bool:
        """
        Тест 1. Проверка исходного состояния блока:
        """
        self.__inputs_a0()
        if my_msg(self.msg_1):
            pass
        else:
            return False
        self.__mysql_conn.mysql_ins_result('идет тест 1', '1')
        self.__ctrl_kl.ctrl_relay('KL21', True)
        self.__fault.debug_msg("KL21 включен", 4)
        self.__reset.sbros_zashit_kl30()
        self.__fault.debug_msg("тест 1 сброс защит", 4)
        in_a1, in_a2, in_a5 = self.__inputs_a()
        if in_a1 is False and in_a5 is True and in_a2 is False:
            self.__fault.debug_msg("верное состояние выходов блока", 3)
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '1')
            if in_a1 is True:
                self.__fault.debug_msg("неверное состояние", 1)
                self.__mysql_conn.mysql_error(331)
            elif in_a5 is False:
                self.__fault.debug_msg("неверное состояние", 1)
                self.__mysql_conn.mysql_error(332)
            elif in_a2 is True:
                self.__fault.debug_msg("неверное состояние", 1)
                self.__mysql_conn.mysql_error(333)
            return False
        return True

    def st_test_11_bmz_2(self) -> bool:
        """
        1.1. Проверка вероятности наличия короткого замыкания на входе измерительной цепи блока
        """
        self.__mysql_conn.mysql_ins_result('идет тест 1.1', '1')
        meas_volt_ust = self.__proc.procedure_1_21_31()
        self.__fault.debug_msg(f'напряжение в процедуре 1 {meas_volt_ust}', 2)
        if meas_volt_ust != 0.0:
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '1')
        self.__ctrl_kl.ctrl_relay('KL63', True)
        meas_volt = self.__read_mb.read_analog()
        self.__fault.debug_msg(f'напряжение после подключения KL63 {meas_volt:.2f}', 2)
        if 0.6 * meas_volt_ust <= meas_volt <= 1.1 * meas_volt_ust:
            pass
        else:
            self.__fault.debug_msg("напряжение не соответствует", 1)
            self.__mysql_conn.mysql_ins_result('неисправен', '1')
            self.__mysql_conn.mysql_error(394)
            self.__reset.sbros_kl63_proc_1_21_31()
            return False
        self.__fault.debug_msg("напряжение соответствует", 4)
        self.__reset.sbros_kl63_proc_1_21_31()
        return True

    def st_test_12_bmz_2(self) -> bool:
        """
        1.2. Определение коэффициента Кс отклонения фактического напряжения от номинального
        """
        self.__mysql_conn.mysql_ins_result('идет тест 1.2', '1')
        self.coef_volt = self.__proc.procedure_1_22_32()
        if self.coef_volt != 0.0:
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '1')
            return False
        self.__mysql_conn.mysql_ins_result('исправен', '1')
        self.__reset.stop_procedure_3()
        self.__fault.debug_msg("тест 1 пройден", 2)
        return True

    def st_test_20_bmz_2(self) -> bool:
        """
        Тест 2. Проверка работоспособности защиты блока в режиме «Проверка»
        """
        if my_msg(self.msg_2):
            pass
        else:
            return False
        self.__mysql_conn.mysql_ins_result('идет тест 2', '2')
        self.__fault.debug_msg("начало теста 2, сброс всех реле", 4)
        if self.__proc.procedure_x4_to_x5(coef_volt=self.coef_volt, setpoint_volt=self.ust_test):
            return True
        self.__mysql_conn.mysql_ins_result('неисправен', '2')
        return False

    def st_test_21_bmz_2(self) -> bool:
        self.__ctrl_kl.ctrl_relay('KL63', True)
        sleep(2)
        self.__ctrl_kl.ctrl_relay('KL63', False)
        sleep(1)
        in_a1, in_a2, in_a5 = self.__inputs_a()
        if in_a1 is True and in_a5 is False and in_a2 is True:
            self.__fault.debug_msg("состояние выходов блока соответствуют", 3)
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '2')
            if in_a1 is False:
                self.__fault.debug_msg("состояние входа 1 не соответствует", 1)
                self.__mysql_conn.mysql_error(335)
            elif in_a5 is True:
                self.__fault.debug_msg("состояние входа 5 не соответствует", 1)
                self.__mysql_conn.mysql_error(336)
            elif in_a2 is False:
                self.__fault.debug_msg("состояние входа 2 не соответствует", 1)
                self.__mysql_conn.mysql_error(337)
            return False
        self.__reset.stop_procedure_3()
        return True

    def st_test_22_bmz_2(self) -> bool:
        """
        2.4.2. Сброс защит после проверки
        """
        self.__mysql_conn.mysql_ins_result('идет тест 2.4', '2')
        self.__reset.sbros_zashit_kl30()
        in_a1, in_a2, in_a5 = self.__inputs_a()
        if in_a1 is False and in_a5 is True and in_a2 is False:
            self.__fault.debug_msg("состояние выходов соответствует", 3)
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '2')
            if in_a1 is True:
                self.__fault.debug_msg("вход 1 не соответствует", 1)
                self.__mysql_conn.mysql_error(338)
            elif in_a5 is False:
                self.__fault.debug_msg("вход 5 не соответствует", 1)
                self.__mysql_conn.mysql_error(339)
            elif in_a2 is True:
                self.__fault.debug_msg("вход 2 не соответствует", 1)
                self.__mysql_conn.mysql_error(340)
            return False
        self.__mysql_conn.mysql_ins_result('исправен', '2')
        self.__fault.debug_msg("тест 2 пройден", 2)
        return True

    def st_test_30_bmz_2(self) -> bool:
        """
        Тест 3. Проверка срабатывания защиты блока по уставкам
        """
        if my_msg(self.msg_3):
            pass
        else:
            return False
        self.__mysql_conn.mysql_ins_result('идет тест 3', '3')
        # Цикл i=1…11 (Таблица уставок 1)
        k = 0
        for i in self.list_ust_volt:
            msg_result = my_msg_2(f'{self.msg_4} {self.list_ust_num[k]}')
            if msg_result == 0:
                pass
            elif msg_result == 1:
                return False
            elif msg_result == 2:
                self.__mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[k]} пропущена')
                self.list_delta_percent.append('пропущена')
                self.list_delta_t.append('пропущена')
                k += 1
                continue
            self.__mysql_conn.mysql_ins_result('идет тест 3.1', '3')
            if self.__proc.procedure_x4_to_x5(coef_volt=self.coef_volt, setpoint_volt=i):
                pass
            else:
                self.__mysql_conn.mysql_ins_result('неисправен', '3')
                return False
            # qw = 0
            for qw in range(4):
                self.calc_delta_t = self.__ctrl_kl.ctrl_ai_code_v0(code=104)
                self.__fault.debug_msg(f'дельта t \t {self.calc_delta_t:.1f}', 'orange')
                if self.calc_delta_t == 9999:
                    self.__reset.sbros_zashit_kl30()
                    sleep(3)
                    qw += 1
                    continue
                else:
                    break
            self.__fault.debug_msg(f'дельта t \t {self.calc_delta_t:.1f}', 2)
            if self.calc_delta_t < 10:
                self.list_delta_t.append(f'< 10')
            elif self.calc_delta_t == 9999:
                self.list_delta_t.append(f'неисправен')
            else:
                self.list_delta_t.append(f'{self.calc_delta_t:.1f}')
            # Δ%= 6,1085*U4
            meas_volt = self.__read_mb.read_analog()
            calc_delta_percent = meas_volt * 6.1085
            self.__fault.debug_msg(f'дельта % \t {calc_delta_percent:.2f}', 2)
            self.list_delta_percent.append(f'{calc_delta_percent:.2f}')
            self.__reset.stop_procedure_3()
            self.__mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[k]} дельта t: {self.calc_delta_t:.1f}')
            self.__mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[k]} дельта %: {calc_delta_percent:.2f}')
            in_a1, in_a2, in_a5 = self.__inputs_a()
            if in_a1 is True and in_a5 is False and in_a2 is True:
                self.__fault.debug_msg("соответствие выходов блока, сбрасываем и переходим к тесту 3.5", 3)
                if self.__subtest_35():
                    k += 1
                    continue
                else:
                    self.__mysql_conn.mysql_ins_result('неисправен', '3')
                    k += 1
                    continue
            else:
                self.__fault.debug_msg("не соответствие выходов блока, переходим к тесту 3.2", 2)
                self.__mysql_conn.mysql_ins_result('неисправен', '3')
                self.__mysql_conn.mysql_error(341)
                if self.__subtest_32(i, k):
                    if self.__subtest_35():
                        k += 1
                        continue
                    else:
                        self.__mysql_conn.mysql_ins_result('неисправен', '3')
                        k += 1
                        continue
                else:
                    if self.__subtest_35():
                        k += 1
                        continue
                    else:
                        self.__mysql_conn.mysql_ins_result('неисправен', '3')
                        k += 1
                        continue
        self.__mysql_conn.mysql_ins_result('исправен', '3')
        return True

    def __subtest_32(self, i, k) -> bool:
        """
        3.2. Формирование нагрузочного сигнала 1,1*calc_volt[i]:
        3.2.1. Сброс защит после проверки
        """
        self.__mysql_conn.mysql_ins_result('идет тест 3.2', '3')
        self.__fault.debug_msg("старт теста 3.2", 3)
        self.__reset.sbros_zashit_kl30()
        in_a1, in_a2, in_a5 = self.__inputs_a()
        if in_a1 is False and in_a5 is True and in_a2 is False:
            self.__fault.debug_msg("состояние выходов блока соответствуют", 3)
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '3')
            if in_a1 is True:
                self.__fault.debug_msg("состояние входа 1 не соответствуют", 1)
                self.__mysql_conn.mysql_error(338)
            elif in_a5 is False:
                self.__fault.debug_msg("состояние входа 5 не соответствует", 1)
                self.__mysql_conn.mysql_error(339)
            elif in_a2 is True:
                self.__fault.debug_msg("состояние входа 2 не соответствует", 1)
                self.__mysql_conn.mysql_error(340)
            return False
        self.__mysql_conn.mysql_ins_result('идет тест 3.3', '3')
        if self.__proc.procedure_1_25_35(coef_volt=self.coef_volt, setpoint_volt=i):
            pass
        else:
            return False
        # Δ%= 6,1085*U4
        meas_volt = self.__read_mb.read_analog()
        calc_delta_percent = meas_volt * 6.1085
        self.__fault.debug_msg(f'дельта % \t {calc_delta_percent:.2f}', 2)
        self.list_delta_percent[-1] = f'{calc_delta_percent:.2f}'
        self.__mysql_conn.mysql_ins_result('идет тест 3.4', '3')
        # wq = 0
        for wq in range(4):
            self.calc_delta_t = self.__ctrl_kl.ctrl_ai_code_v0(code=104)
            self.__fault.debug_msg(f'дельта t \t {self.calc_delta_t:.1f}', 'orange')
            if self.calc_delta_t == 9999:
                self.__reset.sbros_zashit_kl30()
                sleep(3)
                wq += 1
                continue
            else:
                break
        self.__fault.debug_msg(f'дельта t \t {self.calc_delta_t:.1f}', 2)
        if self.calc_delta_t < 10:
            self.list_delta_t[-1] = f'< 10'
        elif self.calc_delta_t == 9999:
            self.list_delta_t[-1] = f'неисправен'
        else:
            self.list_delta_t[-1] = f'{self.calc_delta_t:.1f}'
        self.__mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[k]} дельта t: {self.calc_delta_t:.1f}')
        self.__mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[k]} дельта %: {calc_delta_percent:.2f}')
        in_a1, in_a2, in_a5 = self.__inputs_a()
        if in_a1 is True and in_a5 is False and in_a2 is True:
            pass
        else:
            self.__fault.debug_msg("выходы блока не соответствуют", 1)
            self.__mysql_conn.mysql_ins_result('неисправен', '3')
            self.__mysql_conn.mysql_error(341)
            return False
        self.__fault.debug_msg("выходы блока соответствуют", 3)
        self.__reset.stop_procedure_3()
        self.__fault.debug_msg("сброс реле и старт теста 3.5", 2)
        return True

    def __subtest_35(self):
        """
        3.5. Расчет относительной нагрузки сигнала
        """
        self.__mysql_conn.mysql_ins_result('идет тест 3.5', '3')
        self.__fault.debug_msg("старт теста 3.5", 2)
        self.__reset.sbros_zashit_kl30()
        in_a1, in_a2, in_a5 = self.__inputs_a()
        if in_a1 is False and in_a5 and in_a2 is False:
            self.__fault.debug_msg("состояние выходов блока соответствует", 3)
            self.__fault.debug_msg("тест 3.5 завершен", 2)
            return True
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '3')
            if in_a1 is True:
                self.__fault.debug_msg("вход 1 не соответствует", 1)
                self.__mysql_conn.mysql_error(338)
            elif in_a5 is False:
                self.__fault.debug_msg("вход 5 не соответствует", 1)
                self.__mysql_conn.mysql_error(339)
            elif in_a2 is True:
                self.__fault.debug_msg("вход 2 не соответствует", 1)
                self.__mysql_conn.mysql_error(340)
            return False

    def __inputs_a0(self):
        in_a0 = self.__read_mb.read_discrete(0)
        if in_a0 is None:
            # logging.error(f'нет связи с контроллером')
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_a0

    def __inputs_a(self):
        in_a1 = self.__read_mb.read_discrete(1)
        in_a2 = self.__read_mb.read_discrete(2)
        in_a5 = self.__read_mb.read_discrete(5)
        if in_a1 is None or in_a2 is None or in_a5 is None:
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_a1, in_a2, in_a5

    def __inputs_b(self):
        in_b0 = self.__read_mb.read_discrete(8)
        in_b1 = self.__read_mb.read_discrete(9)
        if in_b0 is None or in_b1 is None:
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_b0, in_b1

    def st_test_bmz_2(self) -> bool:
        if self.st_test_10_bmz_2():
            if self.st_test_11_bmz_2():
                if self.st_test_12_bmz_2():
                    if self.st_test_20_bmz_2():
                        if self.st_test_21_bmz_2():
                            if self.st_test_22_bmz_2():
                                if self.st_test_30_bmz_2():
                                    return True
        return False

    def result_test_bmz_2(self):
        for g1 in range(len(self.list_delta_percent)):
            self.list_result.append((self.list_ust_num[g1], self.list_delta_percent[g1], self.list_delta_t[g1]))
        self.__mysql_conn.mysql_tzp_result(self.list_result)


if __name__ == '__main__':
    test_bmz_2 = TestBMZ2()
    reset_test_bmz_2 = ResetRelay()
    mysql_conn_bmz2 = MySQLConnect()
    fault = Bug(True)
    try:
        test_bmz_2 = TestBMZ2()
        if test_bmz_2.st_test_bmz_2():
            test_bmz_2.result_test_bmz_2()
            mysql_conn_bmz2.mysql_block_good()
            my_msg('Блок исправен', 'green')
        else:
            test_bmz_2.result_test_bmz_2()
            mysql_conn_bmz2.mysql_block_bad()
            my_msg('Блок неисправен', 'red')
    except OSError:
        my_msg("ошибка системы", 'red')
    except SystemError:
        my_msg("внутренняя ошибка", 'red')
    except ModbusConnectException as mce:
        fault.debug_msg(mce, 'red')
        my_msg(f'{mce}', 'red')
    except HardwareException as hwe:
        my_msg(f'{hwe}', 'red')
    finally:
        reset_test_bmz_2.reset_all()
        sys.exit()
