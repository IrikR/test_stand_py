#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ПРОВЕРЕН
Алгоритм проверки

Тип блока: БТЗ-Т.
Производитель: Нет производителя, ТЭТЗ-Инвест, Строй-энергомаш, Углеприбор.
"""

import sys
import logging

from time import time, sleep

from .general_func.exception import *
from .general_func.database import *
from .general_func.modbus import *
from .general_func.procedure import *
from .general_func.reset import ResetRelay, ResetProtection
from .general_func.subtest import ProcedureFull, ReadOPCServer
from .gui.msgbox_1 import *
from .gui.msgbox_2 import *
from .general_func.utils import CLILog


__all__ = ["TestBTZT"]


class TestBTZT:

    def __init__(self):
        self.reset_relay = ResetRelay()
        self.reset_protect = ResetProtection()
        self.proc = Procedure()
        self.proc_full = ProcedureFull()
        self.ai_read = AIRead()
        self.ctrl_kl = CtrlKL()
        self.di_read = DIRead()
        self.mysql_conn = MySQLConnect()
        self.di_read_full = ReadOPCServer()
        self.cli_log = CLILog(True, __name__)

        self.ust_test: float = 80.0
        # self.ust_1 = (23.7, 28.6, 35.56, 37.4, 42.6, 47.3)
        self.list_ust_tzp_volt = (25.7, 30.6, 37.56, 39.4, 44.6, 49.3)
        # self.list_ust_pmz_volt = (67.9, 86.4, 99.1, 117.2, 140.7, 146.4, 156.6, 164.2, 175.7, 183.7, 192.1)
        self.list_ust_pmz_volt = (70.9, 89.4, 103.1, 121.2, 144.7, 150.4, 160.6, 168.2, 179.7, 187.7, 196.1)
        self.list_delta_t_pmz = []
        self.list_delta_t_tzp = []
        self.list_delta_percent_pmz = []
        self.list_delta_percent_tzp = []
        self.list_ust_tzp_num = (0.5, 0.6, 0.7, 0.8, 0.9, 1.0)
        self.list_ust_pmz_num = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
        self.list_result_pmz = []
        self.list_result_tzp = []

        self.coef_volt: float = 0.0
        self.meas_volt: float = 0.0

        self.calc_delta_t_pmz: float = 0.0
        self.calc_delta_percent_pmz: float = 0.0
        self.delta_t_pmz: float = 0.0
        self.delta_percent_pmz: float = 0.0

        self.calc_delta_t_tzp: float = 0.0
        self.calc_delta_percent_tzp: float = 0.0
        self.delta_t_tzp: float = 0.0
        self.delta_percent_tzp: float = 0.0

        self.health_flag_pmz: bool = False
        self.health_flag_tzp: bool = False
        self.malfunction: bool = False

        self.in_a1: bool = False
        self.in_a2: bool = False
        self.in_a5: bool = False
        self.in_a6: bool = False
        self.in_b1: bool = False

        self.msg_1 = "Переключите оба тумблера на корпусе блока в положение «Работа» и установите " \
                     "регуляторы уставок в положение 1 (1-11) и положение 1.0 (0.5-1.0)"
        self.msg_2 = "Переключите тумблер ПМЗ (1-11) в положение «Проверка»"
        self.msg_9 = "Переключите тумблер ПМЗ (1-11) в положение «Работа»"
        self.msg_3 = "Переключите тумблер ТЗП (0.5-1.0) в положение «Проверка»"
        self.msg_8 = "Переключите тумблер ТЗП (0.5…1.0) в положение «Работа»"
        self.msg_5 = "Установите регулятор уставок ПМЗ (1-11) на блоке в положение"
        self.msg_7 = "Установите регулятор уставок ТЗП (0.5…1.0) на блоке в положение"

        logging.basicConfig(filename="C:\Stend\project_class\log\TestBTZT.log",
                            filemode="w",
                            level=logging.DEBUG,
                            encoding="utf-8",
                            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('WARNING')
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))

    def st_test_10(self) -> bool:
        """
        Тест 1. Проверка исходного состояния блока:
        """
        self.di_read.di_read('in_b6', 'in_b7')
        if my_msg(self.msg_1):
            pass
        else:
            return False
        self.logger.debug("тест 1")
        self.mysql_conn.mysql_ins_result('идет тест 1', '1')
        self.ctrl_kl.ctrl_relay('KL21', True)
        self.reset_protect.sbros_zashit_kl30()
        if self.di_read_full.subtest_4di(test_num=1, subtest_num=1.0,
                                         err_code_a=390, err_code_b=391, err_code_c=392, err_code_d=393,
                                         position_a=False, position_b=True, position_c=False, position_d=True,
                                         di_a='in_a1', di_b='in_a5', di_c='in_a2', di_d='in_a6'):
            return True
        return False

    def st_test_11(self) -> bool:
        """
        1.1.2. Проверка отсутствия короткого замыкания на входе измерительной части блока:
        1.2. Определение коэффициента Кс отклонения фактического напряжения от номинального
        """
        if self.proc_full.procedure_1_full(test_num=1, subtest_num=1.1, coef_min_volt=0.4):
            self.coef_volt = self.proc_full.procedure_2_full(test_num=1, subtest_num=1.2)
            return True
        return False

    def st_test_20(self) -> bool:
        """
        Тест 2. Проверка работоспособности защиты ПМЗ блока в режиме «Проверка»
        """
        if my_msg(self.msg_2):
            pass
        else:
            return False
        self.logger.debug("тест 2")
        self.mysql_conn.mysql_ins_result('идет тест 2.1', '2')
        if self.proc.procedure_x4_to_x5(coef_volt=self.coef_volt, setpoint_volt=self.ust_test):
            return True
        self.mysql_conn.mysql_ins_result('неисправен', '2')
        return False

    def st_test_21(self) -> bool:
        """
        2.2.  Проверка срабатывания блока от сигнала нагрузки:
        """
        self.logger.debug("тест 2.2")
        self.mysql_conn.mysql_ins_result('идет тест 2.2', '2')
        self.ctrl_kl.ctrl_relay('KL63', True)
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.log_msg("таймаут 2 сек", "gray")
        self.ctrl_kl.ctrl_relay('KL63', False)
        if self.di_read_full.subtest_4di(test_num=2, subtest_num=2.1,
                                         err_code_a=395, err_code_b=396, err_code_c=397, err_code_d=398,
                                         position_a=False, position_b=True, position_c=True, position_d=False,
                                         di_a='in_a1', di_b='in_a5', di_c='in_a2', di_d='in_a6'):
            self.reset_relay.stop_procedure_3()
            return True
        self.reset_relay.stop_procedure_3()
        return False

    def st_test_22(self) -> bool:
        """
        2.4.2. Сброс защит после проверки
        """
        self.logger.debug("тест 2.2")
        self.mysql_conn.mysql_ins_result('идет тест 2.2', '2')
        self.reset_protect.sbros_zashit_kl30()
        if self.di_read_full.subtest_4di(test_num=2, subtest_num=2.2,
                                         err_code_a=399, err_code_b=400, err_code_c=401, err_code_d=402,
                                         position_a=False, position_b=True, position_c=False, position_d=True,
                                         di_a='in_a1', di_b='in_a5', di_c='in_a2', di_d='in_a6'):
            if my_msg(self.msg_9):
                return True
        return False

    def st_test_30(self) -> bool:
        """
        Тест 3. Проверка работоспособности защиты ТЗП блока в режиме «Проверка»
        """
        if my_msg(self.msg_3):
            if self.di_read_full.subtest_4di(test_num=3, subtest_num=3.0,
                                             err_code_a=403, err_code_b=404, err_code_c=405, err_code_d=406,
                                             position_a=True, position_b=False, position_c=False, position_d=True,
                                             di_a='in_a1', di_b='in_a5', di_c='in_a2', di_d='in_a6'):
                return True
        return False

    def st_test_31(self) -> bool:
        """
        3.2. Сброс защит после проверки
        """
        self.logger.debug("тест 3.2")
        self.mysql_conn.mysql_ins_result('идет тест 3.2', '3')
        if my_msg(self.msg_8):
            pass
        else:
            return False
        self.reset_protect.sbros_zashit_kl30()
        sleep(1)
        if self.di_read_full.subtest_4di(test_num=3, subtest_num=3.1,
                                         err_code_a=407, err_code_b=408, err_code_c=409, err_code_d=410,
                                         position_a=False, position_b=True, position_c=False, position_d=True,
                                         di_a='in_a1', di_b='in_a5', di_c='in_a2', di_d='in_a6'):
            return True
        return False

    def st_test_40(self) -> bool:
        """
        Тест 4. Проверка срабатывания защиты ПМЗ блока по уставкам
        """
        self.logger.debug("тест 4")
        self.mysql_conn.mysql_ins_result('идет тест 4.0', '4')
        k = 0
        for i in self.list_ust_pmz_volt:
            self.malfunction = False
            msg_result = my_msg_2(f'{self.msg_5} {self.list_ust_pmz_num[k]}')

            if msg_result == 0:
                pass
            elif msg_result == 1:
                return False
            elif msg_result == 2:
                self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_pmz_num[k]} пропущена')
                self.list_delta_percent_pmz.append('пропущена')
                self.list_delta_t_pmz.append('пропущена')
                k += 1
                continue
            self.mysql_conn.mysql_ins_result('идет тест 4.1', '4')

            # 4.1.  Проверка срабатывания блока от сигнала нагрузки:
            self.logger.debug("4.1.  Проверка срабатывания блока от сигнала нагрузки:")
            self.mysql_conn.mysql_add_message(f'уставка МТЗ: {self.list_ust_pmz_num[k]}, подтест 4.1')
            self.proc.procedure_1_24_34(coef_volt=self.coef_volt, setpoint_volt=i, factor=1.1)
            self.meas_volt = self.ai_read.ai_read('AI0')
            self.func_delta_t_pmz(k=k)
            self.reset_relay.stop_procedure_3()
            if self.calc_delta_t_pmz == 9999 or self.malfunction is True:
                self.proc.procedure_1_24_34(coef_volt=self.coef_volt, setpoint_volt=i, factor=1.2)
                self.meas_volt = self.ai_read.ai_read('AI0')
                self.func_delta_t_pmz(k=k)
                self.reset_relay.stop_procedure_3()
            else:
                pass

            # обработка полученных результатов
            # Δ%= 2.7938*U4
            self.logger.debug("обработка полученных результатов")
            calc_delta_percent_pmz = 2.7938 * self.meas_volt
            self.mysql_conn.mysql_add_message(f'уставка МТЗ: {self.list_ust_pmz_num[k]}, подтест 4.2')
            if self.calc_delta_t_pmz == 9999 or self.malfunction is True:
                self.delta_t_pmz = 'неисправен'
                self.delta_percent_pmz = 'неисправен'
                self.health_flag_pmz = True
            elif self.calc_delta_t_pmz <= 10 and self.malfunction is False:
                self.delta_t_pmz = '< 10'
                self.delta_percent_pmz = f"{calc_delta_percent_pmz:.2f}"
            elif self.calc_delta_t_pmz != 9999 and self.malfunction is False:
                self.delta_t_pmz = f"{self.calc_delta_t_pmz:.1f}"
                self.delta_percent_pmz = f"{calc_delta_percent_pmz:.2f}"

            # запись результатов в БД
            self.logger.debug("запись результатов в БД")
            result_pmz = f'уставка {self.list_ust_pmz_num[k]}: дельта t: {self.delta_t_pmz}, ' \
                         f'дельта %: {self.delta_percent_pmz}'
            self.mysql_conn.mysql_add_message(result_pmz)
            self.logger.info(result_pmz)
            self.list_delta_percent_pmz.append(self.delta_percent_pmz)
            self.list_delta_t_pmz.append(self.delta_t_pmz)

            # сброс защиты после проверки
            self.logger.debug("сброс защиты после проверки")
            if self.reset_protection(test_num=4, subtest_num=4.2):
                k += 1
                continue
            else:
                self.health_flag_pmz = True
                self.mysql_conn.mysql_ins_result('неисправен', '4')
                return False
        self.mysql_conn.mysql_ins_result('исправен', '4')
        self.logger.debug("тест 4 завершен")
        return True

    def st_test_50(self) -> bool:
        """
        Тест 5. Проверка срабатывания защиты ТЗП блока по уставкам
        """
        self.logger.debug("тест 5")
        self.mysql_conn.mysql_ins_result('идет тест 5', '5')
        m = 0
        for n in self.list_ust_tzp_volt:
            self.malfunction = False
            msg_result = my_msg_2(f'{self.msg_7} {self.list_ust_tzp_num[m]}')
            self.logger.debug(f"от пользователя пришло {msg_result}")
            if msg_result == 0:
                pass
            elif msg_result == 1:
                return False
            elif msg_result == 2:
                self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_tzp_num[m]} пропущена')
                self.list_delta_percent_tzp.append('пропущена')
                self.list_delta_t_tzp.append('пропущена')
                m += 1
                continue

            # формирование испытательного напряжения
            self.logger.debug("5.1 формирование испытательного напряжения")
            self.mysql_conn.mysql_ins_result('идет тест 5.1', '5')
            if self.proc.procedure_x4_to_x5(coef_volt=self.coef_volt, setpoint_volt=n):
                pass
            else:
                self.mysql_conn.mysql_ins_result('неисправен', '5')
                return False

            # измерение испытательного напряжения и вычисление процентного соотношения
            self.logger.debug("5.2 измерение испытательного напряжения и вычисление процентного соотношения")
            self.mysql_conn.mysql_ins_result('идет тест 5.2', '5')
            self.meas_volt = self.ai_read.ai_read('AI0')
            # Δ%= 0.0044*U42[i]+2.274* U4[i]
            calc_delta_percent_tzp = 0.0044 * self.meas_volt ** 2 + 2.274 * self.meas_volt

            # Проверка срабатывания блока от сигнала нагрузки:
            self.logger.debug("5.3 Проверка срабатывания блока от сигнала нагрузки:")
            self.mysql_conn.progress_level(0.0)
            self.logger.debug("тест 5.3")
            self.mysql_conn.mysql_ins_result('идет тест 5.3', '5')

            self.func_delta_t_tzp()

            # обработка результатов
            self.logger.debug("5.4 обработка результатов")
            if self.malfunction is True:
                self.delta_t_tzp = "неисправен"
                self.delta_percent_tzp = "неисправен"
                self.health_flag_tzp = True
                self.mysql_conn.mysql_error(411)
            elif self.malfunction is False:
                self.delta_t_tzp = f'{self.calc_delta_t_tzp:.1f}'
                self.delta_percent_tzp = f'{calc_delta_percent_tzp:.2f}'

            # запись результатов в БД
            self.logger.debug("5.5 запись результатов в БД")
            result = f'уставка {self.list_ust_tzp_num[m]}: дельта t: {self.delta_t_tzp}, ' \
                     f'дельта %: {self.delta_percent_tzp}'
            self.logger.info(result)
            self.mysql_conn.mysql_add_message(result)
            self.list_delta_t_tzp.append(self.delta_t_tzp)
            self.list_delta_percent_tzp.append(self.delta_percent_tzp)

            if self.reset_protection(test_num=5, subtest_num=5.4):
                m += 1
                continue
            else:
                self.mysql_conn.mysql_ins_result('неисправен', '5')
                return False
        self.mysql_conn.mysql_ins_result('исправен', '5')
        return True

    def reset_protection(self, *, test_num: int, subtest_num: float):
        self.logger.debug("сброс защит")
        self.reset_protect.sbros_zashit_kl30()
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.log_msg("таймаут 1 сек", "gray")
        if self.di_read_full.subtest_4di(test_num=test_num, subtest_num=subtest_num,
                                         err_code_a=399, err_code_b=400, err_code_c=401, err_code_d=402,
                                         position_a=False, position_b=True, position_c=False, position_d=True,
                                         di_a='in_a1', di_b='in_a5', di_c='in_a2', di_d='in_a6'):
            return True
        return False

    def func_delta_t_pmz(self, k):
        for qw in range(2):
            if self.reset_protection(test_num=4, subtest_num=4.2):
                # self.in_a1, self.in_a2, self.in_a5, self.in_a6 = self.di_read.di_read('in_a1', 'in_a2',
                #                                                                       'in_a5', 'in_a6')
                self.calc_delta_t_pmz, self.in_a1, self.in_a2, \
                    self.in_a5, self.in_a6 = self.ctrl_kl.ctrl_ai_code_v0(code=103)
                # sleep(3)
                # self.in_a1, self.in_a2, self.in_a5, self.in_a6 = self.di_read.di_read('in_a1', 'in_a2',
                #                                                                       'in_a5', 'in_a6')
                result_delta_t = f"уставка ПМЗ: {self.list_ust_pmz_num[k]}; попытка: {qw}; " \
                                 f"время: {self.calc_delta_t_pmz}"
                self.logger.info(result_delta_t)
                self.mysql_conn.mysql_add_message(result_delta_t)
                if self.calc_delta_t_pmz == 9999:
                    qw += 1
                    self.logger.debug("блок не сработал по времени, повтор проверки блока")
                    self.mysql_conn.mysql_add_message("блок не сработал по времени, повтор проверки блока")
                    self.malfunction = True
                    continue
                elif self.calc_delta_t_pmz != 9999 and self.in_a1 is False and self.in_a5 is True and \
                        self.in_a2 is True and self.in_a6 is False:
                    self.logger.debug(f"блок сработал, время срабатывания: {self.calc_delta_t_pmz:.1f}")
                    self.mysql_conn.mysql_add_message(f"блок сработал, время срабатывания: {self.calc_delta_t_pmz:.1f}")
                    self.malfunction = False
                    break
                else:
                    self.logger.debug("блок не сработал по положению контактов, повтор проверки блока")
                    self.mysql_conn.mysql_add_message("блок не сработал по положению контактов, повтор проверки блока")
                    self.malfunction = True
                    qw += 1
                    continue
            else:
                self.health_flag_pmz = True
                self.malfunction = True
                break

    def func_delta_t_tzp(self):
        self.ctrl_kl.ctrl_relay('KL63', True)
        self.in_b1, *_ = self.di_read.di_read('in_b1')
        i = 0
        while self.in_b1 is False and i <= 20:
            i += 1
            self.in_b1, *_ = self.di_read.di_read('in_b1')
        if self.in_b1 is True:
            start_timer = time()
            meas_time = 0
            self.in_a5, *_ = self.di_read.di_read('in_a5')
            while self.in_a5 is True and meas_time <= 370:
                self.in_a5, *_ = self.di_read.di_read('in_a5')
                meas_time = time() - start_timer
                self.mysql_conn.progress_level(meas_time)
            stop_timer = time()
            self.calc_delta_t_tzp = stop_timer - start_timer
            self.ctrl_kl.ctrl_relay('KL63', False)
            self.in_a1, self.in_a2, self.in_a5, self.in_a6 = self.di_read.di_read('in_a1', 'in_a2', 'in_a5', 'in_a6')

            if self.in_a1 is True and self.in_a5 is False and self.in_a2 is False and self.in_a6 is True \
                    and self.calc_delta_t_tzp <= 360:
                self.malfunction = False
            else:
                self.malfunction = True
        else:
            self.malfunction = True

    def st_test_btz_t(self) -> [bool, bool]:
        if self.st_test_10():
            if self.st_test_11():
                if self.st_test_20():
                    if self.st_test_21():
                        if self.st_test_22():
                            if self.st_test_30():
                                if self.st_test_31():
                                    if self.st_test_40():
                                        if self.st_test_50():
                                            return True, self.health_flag_pmz, self.health_flag_tzp
        return False, self.health_flag_pmz, self.health_flag_tzp

    def result_test_btz_t(self):
        """
        Сведение всех результатов измерения, и запись в БД.
        """
        for g1 in range(len(self.list_delta_percent_pmz)):
            self.list_result_pmz.append((self.list_ust_pmz_num[g1],
                                         self.list_delta_percent_pmz[g1],
                                         self.list_delta_t_pmz[g1]))
        self.mysql_conn.mysql_pmz_result(self.list_result_pmz)
        for g2 in range(len(self.list_delta_percent_tzp)):
            self.list_result_tzp.append((self.list_ust_tzp_num[g2],
                                         self.list_delta_percent_tzp[g2],
                                         self.list_delta_t_tzp[g2]))
        self.mysql_conn.mysql_tzp_result(self.list_result_tzp)

    def full_test_btz_t(self):
        try:
            test, health_flag_pmz, health_flag_tzp = self.st_test_btz_t()
            if test and not health_flag_pmz and not health_flag_tzp:
                self.result_test_btz_t()
                self.mysql_conn.mysql_block_good()
                self.logger.debug('Блок исправен')
                self.cli_log.log_msg('Блок исправен', 'green')
                my_msg('Блок исправен', 'green')
            else:
                self.result_test_btz_t()
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
    test_btz_t = TestBTZT()
    test_btz_t.full_test_btz_t()
    # reset_test_btz_t = ResetRelay()
    # mysql_conn_btz_t = MySQLConnect()
    # try:
    #     test, health_flag_pmz, health_flag_tzp = test_btz_t.st_test_btz_t()
    #     if test and not health_flag_pmz and not health_flag_tzp:
    #         test_btz_t.result_test_btz_t()
    #         mysql_conn_btz_t.mysql_block_good()
    #         my_msg('Блок исправен', 'green')
    #     else:
    #         test_btz_t.result_test_btz_t()
    #         mysql_conn_btz_t.mysql_block_bad()
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
    #     reset_test_btz_t.reset_all()
    #     sys.exit()
