#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
!!! НОВЫЙ НЕ ОБКАТАНЫЙ !!!

Алгоритм проверки

Тип блока: МТЗ-5 вер.2-7/0.4-2
Производитель: Завод Электромашина.

"""

import sys
import logging

from time import sleep, time

from .general_func.exception import *
from .general_func.database import *
from .general_func.modbus import *
from .general_func.procedure import *
from .general_func.reset import ResetRelay, ResetProtection
from .general_func.subtest import ProcedureFull
from .gui.msgbox_1 import *
from .gui.msgbox_2 import *
from .general_func.utils import CLILog

__all__ = ["TestMTZ5V27"]


class TestMTZ5V27:

    def __init__(self):
        self.reset_relay = ResetRelay()
        self.reset_protect = ResetProtection()
        self.proc = Procedure()
        self.proc_full = ProcedureFull()
        self.ai_read = AIRead()
        self.ctrl_kl = CtrlKL()
        self.di_read = DIRead()
        self.mysql_conn = MySQLConnect()
        self.cli_log = CLILog(True, __name__)

        self.list_ust_tzp_num = (0.4, 0.7, 1.0, 1.3, 1.6, 1.8, 2.0)
        self.list_ust_tzp_volt = (10.8, 18.8, 26.55, 34.05, 41.4, 46.2, 50.85)
        self.list_ust_mtz_num = (2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7)
        self.list_ust_mtz_volt = (37.6, 46.8, 55.8, 64.8, 73.6, 82.4, 91.0, 99.6, 108, 116.4, 124.6)
        self.list_delta_t_mtz = []
        self.list_delta_t_tzp = []
        self.list_delta_percent_mtz = []
        self.list_delta_percent_tzp = []
        self.list_mtz_result = []
        self.list_tzp_result = []
        self.ust_mtz = 30.0

        self.coef_volt: float = 0.0
        self.calc_delta_t_mtz = 0.0
        self.delta_t_mtz: float
        self.in_1: bool
        self.in_5: bool
        self.health_flag: bool = False

        self.msg_1 = "Убедитесь в отсутствии других блоков в панелях разъемов " \
                     "и вставьте блок в соответствующий разъем панели B"
        self.msg_2 = "«Переключите тумблер на корпусе блока в положение «Работа» и установите регуляторы уставок " \
                     "в положение 7 (2-7) и в положение 2 (0.4-2)»"
        self.msg_3 = "Переключите регулятор МТЗ, расположенный на корпусе блока в положение «Проверка»"
        self.msg_4 = "установите регуляторы уставок в положение 2 (2-7) и в положение 0.4 (0.4-2)»"
        self.msg_5 = "Переключите тумблер, расположенный на корпусе блока в положение «Работа»"
        self.msg_6 = "Установите регулятор уставок на блоке в положение \t"
        self.msg_7 = "Установите регулятор времени перегруза на блоке в положение «21 сек»"
        self.msg_8 = "Установите регулятор уставок на блоке в положение\t"

        logging.basicConfig(
            filename="C:\\Stend\\project_class\\log\\TestMTZ5_v27.log",
            filemode="w",
            level=logging.DEBUG,
            encoding="utf-8",
            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('WARNING')
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))

    def st_test_10(self) -> bool:
        """
        Тест 1.0
        :return: bool
        """
        self.di_read.di_read('in_b6', 'in_b7')
        if my_msg(self.msg_1):
            if my_msg(self.msg_2):
                pass
            else:
                return False
        else:
            return False
        self.mysql_conn.mysql_ins_result('идёт тест 1', '1')
        self.ctrl_kl.ctrl_relay('KL1', True)
        sleep(0.5)
        self.logger.debug("таймаут 0.5 сек")
        self.cli_log.log_msg("таймаут 0.5 сек", "gray")
        self.ctrl_kl.ctrl_relay('KL2', True)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.log_msg("таймаут 1 сек", "gray")
        self.reset_protect.sbros_zashit_mtz5()
        in_a1, in_a5 = self.di_read.di_read('in_a1', 'in_a5')
        if in_a1 is True and in_a5 is False:
            pass
        else:
            self.logger.debug("тест 1.1 положение выходов не соответствует")
            self.mysql_conn.mysql_ins_result('неисправен', '1')
            return False
        self.logger.debug("тест 1.1 положение выходов соответствует")
        return True

    def st_test_11(self) -> bool:
        """
        1.1.2. Проверка отсутствия короткого замыкания на входе измерительной части блока:
        1.2. Определение коэффициента Кс отклонения фактического напряжения от номинального
        """
        if self.proc_full.procedure_1_full(test_num=1, subtest_num=1.1, coef_min_volt=0.6):
            self.coef_volt = self.proc_full.procedure_2_full(test_num=1, subtest_num=1.2)
            return True
        return False

    def st_test_20(self) -> bool:
        """
        Тест 2. Проверка работоспособности защиты МТЗ блока в режиме «Проверка»
        :return: bool
        """
        self.mysql_conn.mysql_ins_result('идёт тест 2', '2')
        if my_msg(self.msg_3):
            if my_msg(self.msg_4):
                pass
            else:
                return False
        else:
            return False
        if self.proc.procedure_x4_to_x5(setpoint_volt=self.ust_mtz, coef_volt=self.coef_volt):
            pass
        else:
            self.mysql_conn.mysql_ins_result("неисправен TV1", "2")
            return False
        return True

    def st_test_21(self) -> bool:
        """
        2.2.  Проверка срабатывания блока от сигнала нагрузки:
        :return: bool
        """
        self.logger.debug("2.2.  Проверка срабатывания блока от сигнала нагрузки:")
        self.mysql_conn.mysql_ins_result('идёт тест 2.2', '2')
        self.ctrl_kl.ctrl_relay('KL63', True)
        sleep(0.5)
        self.logger.debug("таймаут 0.5 сек")
        self.cli_log.log_msg("таймаут 0.5 сек", "gray")
        self.ctrl_kl.ctrl_relay('KL63', False)
        sleep(0.2)
        self.logger.debug("таймаут 0.2 сек")
        self.cli_log.log_msg("таймаут 0.2 сек", "gray")
        in_a1, in_a5 = self.di_read.di_read('in_a1', 'in_a5')
        if in_a1 is False and in_a5 is True:
            pass
        else:
            self.mysql_conn.mysql_ins_result('неисправен', '2')
            if in_a1 is True:
                self.mysql_conn.mysql_error(444)
            elif in_a5 is False:
                self.mysql_conn.mysql_error(445)
            self.reset_relay.stop_procedure_3()
            return False
        self.reset_relay.stop_procedure_3()
        return True

    def st_test_22(self) -> bool:
        """
        2.4.2. Сброс защит после проверки
        :return: bool
        """
        self.mysql_conn.mysql_ins_result('идёт тест 2.4', '2')
        self.logger.debug("2.4.2. Сброс защит после проверки")
        self.reset_protect.sbros_zashit_mtz5()
        in_a1, in_a5 = self.di_read.di_read('in_a1', 'in_a5')
        if in_a1 is True and in_a5 is False:
            pass
        else:
            self.logger.debug("положение выходов не соответствует")
            self.mysql_conn.mysql_ins_result('неисправен', '2')
            if in_a1 is False:
                self.mysql_conn.mysql_error(446)
            elif in_a5 is True:
                self.mysql_conn.mysql_error(447)
            return False
        self.logger.debug("положение выходов соответствует")
        self.mysql_conn.mysql_ins_result('исправен', '2')
        return True

    def st_test_30(self) -> bool:
        """
        Тест 3. Проверка срабатывания защиты ПМЗ блока по уставкам
        :return: bool
        """
        if my_msg(self.msg_5):
            pass
        else:
            return False
        self.mysql_conn.mysql_ins_result('идёт тест 3', '3')
        k = 0
        for i in self.list_ust_mtz_volt:
            msg_result_mtz = my_msg_2(f'{self.msg_6} {self.list_ust_mtz_num[k]}')
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

            # if self.proc.procedure_x4_to_x5(setpoint_volt=i, coef_volt=self.coef_volt):
            #     pass
            # else:
            #     self.mysql_conn.mysql_ins_result("неисправен TV1", "3")
            #     return False
            self.proc.procedure_1_24_34(coef_volt=self.coef_volt, setpoint_volt=i, factor=1.1)
            calc_delta_t_mtz, in_a1, in_a5 = self.subtest_time_calc()

            # 3.1.  Проверка срабатывания блока от сигнала нагрузки:
            self.logger.debug("3.1.  Проверка срабатывания блока от сигнала нагрузки:")
            self.mysql_conn.mysql_ins_result(f'уставка {self.list_ust_mtz_num[k]}', '3')

            # Δ%= 0.0029*(U4)2+5.192*U4
            meas_volt = self.ai_read.ai_read('AI0')
            calc_delta_percent_mtz = 0.0029 * meas_volt ** 2 + 5.192 * meas_volt
            self.logger.debug(f'дельта %:\t{calc_delta_percent_mtz:.2f}')
            self.list_delta_percent_mtz.append(f'{calc_delta_percent_mtz:.2f}')

            self.logger.debug(f"время срабатывания: {calc_delta_t_mtz}мс: {in_a1 = } (False), {in_a5 = } (True)")
            self.reset_relay.stop_procedure_3()
            if calc_delta_percent_mtz != 9999 and in_a1 is False and in_a5 is True:
                self.logger.debug(f'дельта t\t{calc_delta_t_mtz}')
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
        if my_msg(self.msg_7):
            pass
        else:
            return False
        self.mysql_conn.mysql_ins_result('идёт тест 4', '4')
        m = 0
        for n in self.list_ust_tzp_volt:
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
            # Δ%= 0.0132*U42[i]+5.4183* U4[i]
            meas_volt = self.ai_read.ai_read('AI0')
            calc_delta_percent_tzp = 0.0132 * meas_volt ** 2 + 5.4183 * meas_volt
            self.logger.debug(f'дельта %:\t{calc_delta_percent_tzp:.2f}')
            self.list_delta_percent_tzp.append(f'{calc_delta_percent_tzp:.2f}')
            # 4.4.  Проверка срабатывания блока от сигнала нагрузки:
            self.ctrl_kl.ctrl_relay('KL63', True)
            self.mysql_conn.progress_level(0.0)
            r = 0
            in_b1, *_ = self.di_read.di_read('in_b1')
            while in_b1 is False and r <= 5:
                in_b1, *_ = self.di_read.di_read('in_b1')
                r += 1
            start_timer_tzp = time()
            delta_t_tzp = 0
            in_a5, *_ = self.di_read.di_read('in_a5')
            while in_a5 is False and delta_t_tzp <= 21:
                delta_t_tzp = time() - start_timer_tzp
                self.mysql_conn.progress_level(delta_t_tzp)
                in_a5, *_ = self.di_read.di_read('in_a5')
            stop_timer_tzp = time()
            self.ctrl_kl.ctrl_relay('KL63', False)
            calc_delta_t_tzp = stop_timer_tzp - start_timer_tzp
            self.mysql_conn.progress_level(0.0)
            self.logger.debug(f'тест 3 delta t: {calc_delta_t_tzp:.1f}')
            self.list_delta_t_tzp.append(f'{calc_delta_t_tzp:.1f}')
            self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_tzp_num[m]} '
                                              f'дельта t: {calc_delta_t_tzp:.1f}')
            self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_tzp_num[m]} '
                                              f'дельта %: {calc_delta_percent_tzp:.2f}')
            self.reset_relay.stop_procedure_3()
            in_a1, in_a5 = self.di_read.di_read('in_a1', 'in_a5')
            if in_a1 is False and in_a5 is True and calc_delta_t_tzp <= 21:
                self.logger.debug("положение выходов соответствует")
                if self.subtest_46():
                    m += 1
                    continue
                else:
                    return False
            else:
                self.logger.debug("положение выходов не соответствует")
                self.mysql_conn.mysql_error(448)
                if self.subtest_46():
                    m += 1
                    continue
                else:
                    return False
        self.mysql_conn.mysql_ins_result('исправен', '4')
        return True

    def subtest_32(self, i: float, k: int) -> bool:
        """
        3.2. Формирование нагрузочного сигнала 1,15*U3[i]:
        :param i: уставка
        :param k: счетчик цикла
        :return: bool
        """
        self.reset_protect.sbros_zashit_mtz5()
        in_a1, in_a5 = self.di_read.di_read('in_a1', 'in_a5')
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
        calc_delta_percent_mtz = 0.0029 * meas_volt ** 2 + 5.192 * meas_volt
        self.list_delta_percent_mtz[-1] = f'{calc_delta_percent_mtz:.2f}'

        calc_delta_t_mtz, in_a1, in_a5 = self.subtest_time_calc()
        self.logger.debug(f"время срабатывания: {calc_delta_t_mtz}мс: {in_a1 = } (False), {in_a5 = } (True)")
        self.reset_relay.stop_procedure_3()

        for wq in range(2):
            self.calc_delta_t_mtz, in_a1, in_a2, in_a5, in_a6 = self.ctrl_kl.ctrl_ai_code_v0(110)
            if 500 < self.calc_delta_t_mtz <= 9999:
                self.reset_protect.sbros_zashit_mtz5()
                sleep(3)
                wq += 1
                continue
            else:
                break
        # in_a1, in_a5 = self.di_read.di_read('in_a1', 'in_a5')
        if self.calc_delta_t_mtz < 10:
            self.list_delta_t_mtz[-1] = f'< 10'
        elif self.calc_delta_t_mtz > 500:
            self.list_delta_t_mtz[-1] = f'> 500'
        else:
            self.list_delta_t_mtz[-1] = f'{self.calc_delta_t_mtz:.1f}'
        self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_mtz_num[k]} '
                                          f'дельта t: {self.calc_delta_t_mtz}')
        self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_mtz_num[k]} '
                                          f'дельта %: {calc_delta_percent_mtz:.2f}')
        if in_a1 is False and in_a5 is True:
            self.reset_relay.stop_procedure_3()
            return True
        else:
            self.reset_relay.stop_procedure_3()
            self.mysql_conn.mysql_error(448)
            return False

    def subtest_33(self) -> bool:
        """
        3.3. Сброс защит после проверки
        3.5. Расчет относительной нагрузки сигнала
        Δ%= 3.4364*(U4[i])/0.63
        :return: bool
        """
        self.reset_protect.sbros_zashit_mtz5()
        in_a1, in_a5 = self.di_read.di_read('in_a1', 'in_a5')
        if in_a1 is True and in_a5 is False:
            self.logger.debug("подтест 3.3 пройден")
            return True
        else:
            self.mysql_conn.mysql_ins_result('неисправен', '3')
            self.logger.debug("подтест 3.3 не пройден")
            if in_a1 is False:
                self.mysql_conn.mysql_error(446)
            elif in_a5 is True:
                self.mysql_conn.mysql_error(447)
            return False

    def subtest_46(self) -> bool:
        """
        4.6.1. Сброс защит после проверки
        Определение кратности сигнала нагрузки: Δ%= 3.4364*U4[i]/0.63
        :return: bool
        """
        self.reset_protect.sbros_zashit_mtz5()
        in_a1, in_a5 = self.di_read.di_read('in_a1', 'in_a5')
        if in_a1 is True and in_a5 is False:
            self.logger.debug("тест 4.6 положение выходов соответствует")
            return True
        else:
            self.mysql_conn.mysql_ins_result('неисправен', '4')
            self.logger.debug("тест 4.6 положение выходов не соответствует")
            if in_a1 is False:
                self.mysql_conn.mysql_error(449)
            elif in_a5 is True:
                self.mysql_conn.mysql_error(450)
            return False

    def subtest_time_calc(self) -> [float, bool, bool]:
        self.logger.debug("подтест проверки времени срабатывания")
        for stc in range(2):
            self.logger.debug(f"попытка: {stc}")
            self.reset_protect.sbros_zashit_mtz5()
            delta_t_mtz, in_1, in_2, in_5, in_6 = self.ctrl_kl.ctrl_ai_code_v0(110)
            # self.in_1, self.in_5 = self.di_read.di_read('in_a1', 'in_a5')
            self.logger.debug(f"время срабатывания: {delta_t_mtz}, "
                              f"{in_1 = } is False, "
                              f"{in_5 = } is True")
            if delta_t_mtz == 9999:
                stc += 1
                continue
            elif delta_t_mtz != 9999 and in_1 is False and in_5 is True:
                break
            else:
                stc += 1
                continue
        return delta_t_mtz, in_1, in_5

    # def sbros_zashit(self):
    #     """
    #     Сброс защит.
    #     :return:
    #     """
    #     self.ctrl_kl.ctrl_relay('KL1', False)
    #     sleep(1.5)
    #     self.ctrl_kl.ctrl_relay('KL1', True)
    #     sleep(2)

    def result_test(self) -> None:
        """
        Записывает результаты проверки в БД.
        :return:
        """
        for g1 in range(len(self.list_delta_percent_mtz)):
            self.list_mtz_result.append((self.list_ust_mtz_num[g1],
                                         self.list_delta_percent_mtz[g1],
                                         self.list_delta_t_mtz[g1]))
        self.mysql_conn.mysql_pmz_result(self.list_mtz_result)
        for g2 in range(len(self.list_delta_percent_tzp)):
            self.list_tzp_result.append((self.list_ust_tzp_num[g2],
                                         self.list_delta_percent_tzp[g2],
                                         self.list_delta_t_tzp[g2]))
        self.mysql_conn.mysql_tzp_result(self.list_tzp_result)

    def st_test_mtz_5_v2_7(self) -> [bool]:
        """
        Функция собирающая все тесты в один тест.
        :return: Bool
        """
        if self.st_test_10():
            if self.st_test_11():
                if self.st_test_20():
                    if self.st_test_21():
                        if self.st_test_22():
                            if self.st_test_30():
                                if self.st_test_40():
                                    return True, self.health_flag
        return False, self.health_flag

    def full_test_mtz_5_v27(self) -> None:
        try:
            test, health_flag = self.st_test_mtz_5_v2_7()
            if test and not health_flag:
                self.result_test()
                self.mysql_conn.mysql_block_good()
                self.logger.debug('Блок исправен')
                self.cli_log.log_msg('Блок исправен', 'green')
                my_msg('Блок исправен', 'green')
            else:
                self.result_test()
                self.mysql_conn.mysql_block_bad()
                self.logger.debug('Блок неисправен')
                self.cli_log.log_msg('Блок неисправен', 'red')
                my_msg('Блок неисправен', 'red')
        except OSError:
            self.logger.debug("ошибка системы")
            self.cli_log.log_msg("ошибка системы", 'red')
            my_msg("ошибка системы", 'red')
        except SystemError:
            self.logger.debug("внутренняя ошибка")
            self.cli_log.log_msg("внутренняя ошибка", 'red')
            my_msg("внутренняя ошибка", 'red')
        except ModbusConnectException as mce:
            self.logger.debug(f'{mce}')
            self.cli_log.log_msg(f'{mce}', 'red')
            my_msg(f'{mce}', 'red')
        except HardwareException as hwe:
            self.logger.debug(f'{hwe}')
            self.cli_log.log_msg(f'{hwe}', 'red')
            my_msg(f'{hwe}', 'red')
        finally:
            self.reset_relay.reset_all()
            sys.exit()


if __name__ == '__main__':
    test_mtz = TestMTZ5V27()
    test_mtz.full_test_mtz_5_v27()
    # reset_test_mtz = ResetRelay()
    # mysql_conn_mtz = MySQLConnect()
    # try:
    #     test, health_flag = test_mtz.st_test_mtz_5_v2_7()
    #     if test and not health_flag:
    #         test_mtz.result_test()
    #         mysql_conn_mtz.mysql_block_good()
    #         my_msg('Блок исправен', 'green')
    #     else:
    #         test_mtz.result_test()
    #         mysql_conn_mtz.mysql_block_bad()
    #         my_msg('Блок неисправен', 'red')
    # except OSError:
    #     my_msg("ошибка системы", 'red')
    # except SystemError:
    #     my_msg("внутренняя ошибка", 'red')
    # except ModbusConnectException as mce:
    #     my_msg(f'{mce}', 'red')
    # except HardwareException as hwe:
    #     my_msg(f'{hwe}', 'red')
    # finally:
    #     reset_test_mtz.reset_all()
    #     sys.exit()
