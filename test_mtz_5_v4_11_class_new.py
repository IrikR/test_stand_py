#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки

Тип блока: МТЗ-5 вер.411256002
Производитель: Завод Электромашина.
"""

import sys
import logging

from time import sleep, time

from general_func.exception import *
from general_func.database import *
from general_func.modbus import *
from general_func.procedure import *
from general_func.subtest import *
from general_func.reset import ResetRelay, ResetProtection
from gui.msgbox_1 import *
from gui.msgbox_2 import *

__all__ = ["TestMTZ5V411"]


class TestMTZ5V411:

    def __init__(self):
        self.reset_relay = ResetRelay()
        self.reset_protect = ResetProtection()
        self.proc = Procedure()
        self.proc_full = ProcedureFull()
        self.ai_read = AIRead()
        self.ctrl_kl = CtrlKL()
        self.di_read = DIRead()
        self.mysql_conn = MySQLConnect()
        self.sub_test = SubtestMTZ5()

        self.list_ust_tzp_num = (0.8, 1, 1.5, 2, 2.25, 2.5, 3)
        self.list_ust_tzp_volt = (15.4, 19.3, 29.0, 38.5, 43.4, 48.2, 57.9)
        self.list_ust_mtz_num = (2, 3, 4, 5, 6, 7, 8)
        self.list_ust_mtz_volt = (38.5, 57.8, 77.1, 96.3, 115.5, 134.8, 154.0)
        self.list_delta_t_mtz = []
        self.list_delta_t_tzp = []
        self.list_delta_percent_mtz = []
        self.list_delta_percent_tzp = []
        self.list_mtz_result = []
        self.list_tzp_result = []
        # self.ust_mtz_volt = 30.0

        self.coef_volt: float = 0.0
        self.delta_t_mtz: float
        self.in_1: bool
        self.in_5: bool
        self.health_flag: bool = False

        self.msg_1 = "Убедитесь в отсутствии других блоков в панелях разъемов " \
                     "и вставьте блок в соответствующий разъем панели B"
        self.msg_2 = "Переключите регулятор МТЗ на корпусе блока в положение «8», регулятор «Перегруз» в положение 3"
        self.msg_3 = "Переключите регулятор МТЗ, расположенный на корпусе блока в положение «Проверка»"
        self.msg_4 = "Переключите регулятор МТЗ, расположенный на корпусе блока в положение «2»"
        self.msg_5 = "Установите регулятор уставок на блоке в положение "
        self.msg_6 = "Установите регулятор времени перегруза на блоке в положение «20 сек»"
        # self.msg_7 = "Установите регулятор МТЗ, расположенный на блоке, в положение «8»"
        self.msg_8 = "Установите регулятор уставок на блоке в положение "
        # C:\Stend\project_class
        logging.basicConfig(
            filename="C:\\Stend\\project_class\\log\\TestMTZ5_411.log",
            filemode="w",
            level=logging.DEBUG,
            encoding="utf-8",
            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('WARNING')
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))

    def st_test_10(self) -> bool:
        """

        :return: bool
        """
        self.di_read.di_read("in_a0")
        if my_msg(self.msg_1):
            if my_msg(self.msg_2):
                return True
        return False

    def st_test_11(self) -> bool:
        """
        Тест 1.1
        :return: bool
        """
        self.mysql_conn.mysql_ins_result('идёт тест 1.1', '1')
        self.logger.debug("тест 1.1")
        self.ctrl_kl.ctrl_relay('KL1', True)
        sleep(0.5)
        self.ctrl_kl.ctrl_relay('KL2', True)
        sleep(1)
        self.reset_protect.sbros_zashit_mtz5()
        in_a1, in_a5 = self.di_read.di_read("in_a1", "in_a5")
        self.logger.debug(f"{in_a1 = } (True), {in_a5 = } (False)")
        if in_a1 is True and in_a5 is False:
            return True
        self.mysql_conn.mysql_ins_result('неисправен', '1')
        return False

    def st_test_12(self) -> bool:
        """
        1.1.2. Проверка отсутствия короткого замыкания на входе измерительной части блока:
        1.2. Определение коэффициента Кс отклонения фактического напряжения от номинального.
        :return:
        """
        if self.proc_full.procedure_1_full(test_num=1, subtest_num=1.2, coef_min_volt=0.6):
            self.coef_volt = self.proc_full.procedure_2_full(test_num=1, subtest_num=1.3)
            return True
        return False

    def st_test_20(self) -> bool:
        """
        Тест 2. Проверка работоспособности защиты МТЗ блока в режиме «Проверка»
        :return: bool
        """
        self.logger.debug("тест 2.0")
        if my_msg(self.msg_3):
            pass
        else:
            return False
        in_a1, in_a5 = self.di_read.di_read("in_a1", "in_a5")
        self.logger.debug(f"{in_a1 = } (False), {in_a5 = } (True)")
        if in_a1 is False and in_a5 is True:
            pass
        else:
            self.mysql_conn.mysql_ins_result('неисправен', '2')
            if in_a1 is True:
                self.mysql_conn.mysql_error(444)
            elif in_a5 is False:
                self.mysql_conn.mysql_error(445)
            return False
        return True

    def st_test_21(self) -> bool:
        """
        2.4.2. Сброс защит после проверки
        :return: bool
        """
        if my_msg(self.msg_4):
            pass
        else:
            return False
        self.logger.debug("тест 2.1")
        self.mysql_conn.mysql_ins_result('идёт тест 2.1', '2')
        self.reset_protect.sbros_zashit_mtz5()
        in_a1, in_a5 = self.di_read.di_read("in_a1", "in_a5")
        self.logger.debug(f"{in_a1 = } (True), {in_a5 = } (False)")
        if in_a1 is True and in_a5 is False:
            pass
        else:
            self.mysql_conn.mysql_ins_result('неисправен', '2')
            if in_a1 is False:
                self.mysql_conn.mysql_error(446)
            elif in_a5 is True:
                self.mysql_conn.mysql_error(447)
            return False
        self.mysql_conn.mysql_ins_result('исправен', '2')
        return True

    def st_test_30(self) -> bool:
        """
        Тест 3. Проверка срабатывания защиты ПМЗ блока по уставкам.
        :return: bool
        """
        self.logger.debug("тест 3.0")
        self.mysql_conn.mysql_ins_result('идёт тест 3', '3')
        k = 0
        for i in self.list_ust_mtz_volt:
            msg_result_mtz = my_msg_2(f'{self.msg_5} {self.list_ust_mtz_num[k]}')
            if msg_result_mtz == 0:
                pass
            elif msg_result_mtz == 1:
                return False
            elif msg_result_mtz == 2:
                self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_mtz_num[k]} пропущена')
                self.list_delta_percent_mtz.append('пропущена')
                self.list_delta_t_mtz.append('пропущена')
                k += 1
                continue
            if self.proc.procedure_x4_to_x5(setpoint_volt=i, coef_volt=self.coef_volt):
                pass
            else:
                self.mysql_conn.mysql_ins_result("неисправен TV1", "3")
                return False
            # 3.1.  Проверка срабатывания блока от сигнала нагрузки:
            self.mysql_conn.mysql_ins_result(f'уставка {self.list_ust_mtz_num[k]}', '3')
            # Δ%= 3.4364*(U4[i])/0.63
            meas_volt = self.ai_read.ai_read('AI0')
            calc_delta_percent_mtz = 3.4364 * meas_volt / 0.63
            self.list_delta_percent_mtz.append(f'{calc_delta_percent_mtz:.2f}')

            calc_delta_t_mtz, in_a1, in_a5 = self.sub_test.subtest_time_calc_mtz()
            self.logger.debug(f"время срабатывания: {calc_delta_t_mtz}мс: {in_a1 = } (True), {in_a5 = } (False)")
            self.reset_relay.stop_procedure_3()
            if calc_delta_percent_mtz != 9999 and in_a1 is False and in_a5 is True:
                self.list_delta_t_mtz.append(f'{calc_delta_t_mtz:.1f}')
                self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_mtz_num[k]}\t'
                                                  f'дельта t: {calc_delta_t_mtz:.1f}\t'
                                                  f'дельта %: {calc_delta_percent_mtz:.2f}')
                if self.subtest_33():
                    k += 1
                    continue
                else:
                    self.mysql_conn.mysql_ins_result('неисправен', '3')
                    return False
            else:
                if self.subtest_32(i, k):
                    if self.subtest_33():
                        k += 1
                        continue
                    else:
                        self.health_flag = True
                        self.mysql_conn.mysql_error(448)
                        self.mysql_conn.mysql_ins_result('неисправен', '3')
                        return False
                else:
                    self.health_flag = True
                    if self.subtest_33():
                        k += 1
                        continue
                    else:
                        self.mysql_conn.mysql_ins_result('неисправен', '3')
                        return False
        self.mysql_conn.mysql_ins_result('исправен', '3')
        return True

    def st_test_40(self) -> bool:
        """
        Тест 4. Проверка срабатывания защиты от перегрузки блока по уставкам.
        :return: bool
        """
        self.logger.debug("тест 4.0")
        if my_msg(self.msg_6):
            pass
        else:
            return False
        self.mysql_conn.mysql_ins_result('идёт тест 4', '4')
        m = 0
        for n in self.list_ust_tzp_volt:
            if my_msg(f'{self.msg_8} {self.list_ust_tzp_num[m]}'):
                pass
            else:
                return False
            msg_result_tzp = my_msg_2(f'{self.msg_8} {self.list_ust_tzp_num[m]}')
            if msg_result_tzp == 0:
                pass
            elif msg_result_tzp == 1:
                return False
            elif msg_result_tzp == 2:
                self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_tzp_num[m]} пропущена')
                self.list_delta_percent_tzp.append('пропущена')
                self.list_delta_t_tzp.append('пропущена')
                m += 1
                continue
            self.mysql_conn.mysql_ins_result(f'уставка {self.list_ust_tzp_num[m]}', '4')
            if self.proc.procedure_x4_to_x5(setpoint_volt=n, coef_volt=self.coef_volt):
                pass
            else:
                self.mysql_conn.mysql_ins_result("неисправен TV1", "4")
                return False
            # Δ%= 3.4364*U4[i]/0.63
            meas_volt = self.ai_read.ai_read('AI0')
            calc_delta_percent_tzp = 3.4364 * meas_volt / 0.63
            self.list_delta_percent_tzp.append(f'{calc_delta_percent_tzp:.2f}')
            # 4.4.  Проверка срабатывания блока от сигнала нагрузки:
            self.ctrl_kl.ctrl_relay('KL63', True)
            r = 0
            in_b1, *_ = self.di_read.di_read('in_b1')
            while in_b1 is False and r <= 5:
                in_b1, *_ = self.di_read.di_read("in_b1")
                r += 1
            start_timer_tzp = time()
            delta_t_tzp = 0
            in_a5, *_ = self.di_read.di_read("in_a5")
            while in_a5 is False and delta_t_tzp <= 30:
                delta_t_tzp = time() - start_timer_tzp
                in_a5, *_ = self.di_read.di_read("in_a5")
            stop_timer_tzp = time()
            calc_delta_t_tzp = stop_timer_tzp - start_timer_tzp

            in_a1, in_a5 = self.di_read.di_read("in_a1", "in_a5")
            self.logger.debug(f"{in_a1 = } (False), {in_a5 = } (True)")
            self.ctrl_kl.ctrl_relay('KL63', False)
            self.reset_relay.stop_procedure_3()
            if in_a1 is False and in_a5 is True and calc_delta_t_tzp <= 30:
                self.list_delta_t_tzp.append(f'{calc_delta_t_tzp:.1f}')
                self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_tzp_num[m]}\t'
                                                  f'дельта t: {calc_delta_t_tzp:.1f}\t'
                                                  f'дельта %: {calc_delta_percent_tzp:.2f}')
                if self.subtest_45():
                    m += 1
                    continue
                else:
                    return False
            else:
                self.list_delta_t_tzp.append(f'неисправен')
                self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_tzp_num[m]}\t'
                                                  f'дельта t: {calc_delta_t_tzp:.1f}\t'
                                                  f'дельта %: {calc_delta_percent_tzp:.2f}')
                self.mysql_conn.mysql_error(448)
                self.health_flag = True
                if self.subtest_45():
                    m += 1
                    continue
                else:
                    return False
        self.mysql_conn.mysql_ins_result('исправен', '4')
        return True

    def subtest_32(self, i, k):
        """
        3.2. Формирование нагрузочного сигнала 1,15*U3[i]:
        :param i: напряжение уставки
        :param k: порядковый номер в цикле
        :return: bool
        """
        self.logger.debug("тест 3.2")
        self.reset_protect.sbros_zashit_mtz5()
        in_a1, in_a5 = self.di_read.di_read('in_a1', 'in_a5')
        self.logger.debug(f"{in_a1 = } is True and {in_a5 = } is False")
        if in_a1 is True and in_a5 is False:
            pass
        else:
            self.mysql_conn.mysql_ins_result('неисправен', '3')
            if in_a1 is False:
                self.mysql_conn.mysql_error(446)
            elif in_a5 is True:
                self.mysql_conn.mysql_error(447)
            return False
        if self.proc.procedure_1_24_34(coef_volt=self.coef_volt, setpoint_volt=i, factor=1.15):
            pass
        else:
            self.mysql_conn.mysql_ins_result('неисправен', '3')
            return False
        # 3.2.2.  Проверка срабатывания блока от сигнала нагрузки:
        meas_volt = self.ai_read.ai_read('AI0')
        calc_delta_percent_mtz = 3.4364 * meas_volt / 0.63
        self.list_delta_percent_mtz[-1] = f'{calc_delta_percent_mtz:.2f}'

        calc_delta_t_mtz, in_a1, in_a5 = self.sub_test.subtest_time_calc_mtz()

        self.reset_relay.stop_procedure_3()

        if calc_delta_percent_mtz != 9999 and in_a1 is False and in_a5 is True:
            self.list_delta_t_mtz[-1] = f'{calc_delta_t_mtz:.1f}'
            self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_mtz_num[k]}\t'
                                              f'дельта t: {calc_delta_t_mtz:.1f}\t'
                                              f'дельта %: {calc_delta_percent_mtz:.2f}')
            return True
        else:
            self.list_delta_t_mtz[-1] = f'неисправен'
            self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_mtz_num[k]}\t'
                                              f'дельта t: {calc_delta_t_mtz:.1f}\t'
                                              f'дельта %: {calc_delta_percent_mtz:.2f}')
            self.health_flag = True
            self.mysql_conn.mysql_error(448)
            return False

    def subtest_33(self) -> bool:
        """
        3.3. Сброс защит после проверки
        3.5. Расчет относительной нагрузки сигнала
        Δ%= 3.4364*(U4[i])/0.63
        :return: bool
        """
        self.logger.debug("тест 3.3")
        self.reset_protect.sbros_zashit_mtz5()
        in_a1, in_a5 = self.di_read.di_read('in_a1', 'in_a5')
        self.logger.debug(f"{in_a1 = } is True and {in_a5 = } is False")
        if in_a1 is True and in_a5 is False:
            return True
        else:
            self.mysql_conn.mysql_ins_result('неисправен', '3')
            if in_a1 is False:
                self.mysql_conn.mysql_error(446)
            elif in_a5 is True:
                self.mysql_conn.mysql_error(447)
            return False
    
    def subtest_45(self) -> bool:
        """
        4.6.1. Сброс защит после проверки
        Определение кратности сигнала нагрузки: Δ%= 3.4364*U4[i]/0.63
        :return: bool
        """
        self.logger.debug("тест 4.5")
        self.reset_protect.sbros_zashit_mtz5()
        in_a1, in_a5 = self.di_read.di_read('in_a1', 'in_a5')
        self.logger.debug(f"{in_a1 = } is True and {in_a5 = } is False")
        if in_a1 is True and in_a5 is False:
            return True
        else:
            self.mysql_conn.mysql_ins_result('неисправен', '4')
            if in_a1 is False:
                self.mysql_conn.mysql_error(446)
            elif in_a5 is True:
                self.mysql_conn.mysql_error(447)
            return False

    def st_test_mtz(self) -> [bool, bool]:
        """
        Функция собирающая все алгоритмы в одну функцию.
        :return: bool
        """
        if self.st_test_10():
            if self.st_test_11():
                if self.st_test_12():
                    if self.st_test_20():
                        if self.st_test_21():
                            if self.st_test_30():
                                if self.st_test_40():
                                    return True, self.health_flag
        return False, self.health_flag

    def result_test_mtz(self):
        for g1 in range(len(self.list_delta_percent_mtz)):
            self.logger.debug(f"уставка: {self.list_ust_mtz_num[g1]}, "
                              f"%: {self.list_delta_percent_mtz[g1]}, "
                              f"t: {self.list_delta_t_mtz[g1]}")
            self.list_mtz_result.append(
                (self.list_ust_mtz_num[g1], self.list_delta_percent_mtz[g1], self.list_delta_t_mtz[g1]))
        self.mysql_conn.mysql_pmz_result(self.list_mtz_result)
        for g2 in range(len(self.list_delta_percent_tzp)):
            self.logger.debug(f"уставка: {self.list_ust_tzp_num[g2]}, "
                              f"%: {self.list_delta_percent_tzp[g2]}, "
                              f"t: {self.list_delta_t_tzp[g2]}")
            self.list_tzp_result.append(
                (self.list_ust_tzp_num[g2], self.list_delta_percent_tzp[g2], self.list_delta_t_tzp[g2]))
        self.mysql_conn.mysql_tzp_result(self.list_tzp_result)
        self.logger.debug("результаты тестов записаны в БД")


if __name__ == '__main__':
    test_mtz = TestMTZ5V411()
    reset_test_mtz = ResetRelay()
    mysql_conn_mtz = MySQLConnect()
    try:
        test, health_flag = test_mtz.st_test_mtz()
        if test and not health_flag:
            test_mtz.result_test_mtz()
            mysql_conn_mtz.mysql_block_good()
            my_msg('Блок исправен', 'green')
        else:
            test_mtz.result_test_mtz()
            mysql_conn_mtz.mysql_block_bad()
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
        reset_test_mtz.reset_all()
        sys.exit()
