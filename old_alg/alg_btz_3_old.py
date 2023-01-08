#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки

Тип блока	Производитель
БТЗ-3	    Нет производителя
БТЗ-3	    ТЭТЗ-Инвест
БТЗ-3	    Строй-энергомаш
БТЗ-3	    Углеприбор

"""

import sys
import logging

from time import sleep, time

from .gen_func_utils import *
from .my_msgbox import *
from .my_msgbox_2 import *
from .gen_func_procedure import *
from .gen_mb_client import *
from .gen_mysql_connect import *

__all__ = ["TestBTZ3"]


class TestBTZ3(object):

    def __init__(self):
        self.__reset = ResetRelay()
        self.__proc = Procedure()
        self.__ctrl_kl = CtrlKL()
        self.__read_mb = ReadMB()
        self.__mysql_conn = MySQLConnect()
        self.reset_relay = ResetRelay()
        self.__fault = Bug(True)

        self.list_ust_tzp_num = (0.5, 0.6, 0.7, 0.8, 0.9, 1.0)
        self.list_ust_tzp = (23.7, 28.6, 35.56, 37.4, 42.6, 47.3)
        self.list_ust_pmz_num = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
        self.list_ust_pmz = (67.9, 86.4, 100.1, 117.2, 140.7, 146.4, 156.6, 164.2, 175.7, 183.7, 192.1)
        self.ust_prov = 80.0
        self.list_delta_t_tzp = []
        self.list_delta_t_pmz = []
        self.list_delta_percent_tzp = []
        self.list_delta_percent_pmz = []
        self.list_result_tzp = []
        self.list_result_pmz = []

        self.coef_volt: float = 0.0
        self.calc_delta_t_pmz: float = 0.0

        self.health_flag: bool = False

        logging.basicConfig(filename="C:\Stend\project_class\TestBTZ3.log",
                            filemode="w",
                            level=logging.DEBUG,
                            encoding="utf-8",
                            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('WARNING')
        self.logger = logging.getLogger(__name__)

    def st_test_10_btz_3(self) -> bool:
        """
        Тест 1. Проверка исходного состояния блока:
        """
        self.__inputs_a0()
        msg_1 = "Переключите оба тумблера на корпусе блока в положение «Работа» и установите " \
                "регуляторы уставок в положение 1 (1-11) и положение 1 (0.5-1)"
        if my_msg(msg_1):
            pass
        else:
            return False
        self.__mysql_conn.mysql_ins_result('идёт тест 1', '1')
        self.__ctrl_kl.ctrl_relay('KL21', True)
        self.__sbros_zashit_kl30()
        in_a1, in_a2, in_a5, in_a6 = self.__inputs_a()
        if in_a1 is False and in_a5 is True and in_a2 is False and in_a6 is True:
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '1')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(368)
            elif in_a5 is False:
                self.__mysql_conn.mysql_error(369)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(370)
            elif in_a6 is False:
                self.__mysql_conn.mysql_error(371)
            return False
        return True

    def st_test_11_btz_3(self) -> bool:
        """
        1.1. Проверка вероятности наличия короткого замыкания на входе измерительной цепи блока
        """
        self.__mysql_conn.mysql_ins_result('идёт тест 1.1', '1')
        meas_volt_ust = self.__proc.procedure_1_21_31()
        if meas_volt_ust != 0.0:
            pass
        else:
            self.__mysql_conn.mysql_error(433)
            self.__mysql_conn.mysql_ins_result('неисправен', '1')
            return False
        self.__ctrl_kl.ctrl_relay('KL63', True)
        min_volt = 0.6 * meas_volt_ust
        max_volt = 1.0 * meas_volt_ust
        meas_volt = self.__read_mb.read_analog()
        self.__fault.debug_msg(f'напряжение после включения KL63: '
                               f'{min_volt:.2f} < = {meas_volt:.2f} <= {max_volt:.2f}', 'orange')
        if min_volt <= meas_volt <= max_volt:
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '1')
            self.__mysql_conn.mysql_error(455)
            self.__reset.sbros_kl63_proc_1_21_31()
            return False
        self.__reset.sbros_kl63_proc_1_21_31()
        return True

    def st_test_12_btz_3(self) -> bool:
        """
        1.2. Определение коэффициента Кс отклонения фактического напряжения от номинального
        """
        self.__mysql_conn.mysql_ins_result('идёт тест 1.2', '1')
        self.__fault.debug_msg("1.2. Определение коэффициента Кс отклонения фактического напряжения от номинального", 3)
        self.coef_volt = self.__proc.procedure_1_22_32()
        if self.coef_volt != 0.0:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен TV1", "1")
            return False
        self.__reset.stop_procedure_32()
        self.__mysql_conn.mysql_ins_result('исправен', '1')
        return True

    def st_test_20_btz_3(self) -> bool:
        """
        Тест 2. Проверка работоспособности защиты ПМЗ блока в режиме «Проверка»
        """
        msg_2 = "Переключите тумблер ПМЗ (1-11) на корпусе блока в положение «Проверка»"
        if my_msg(msg_2):
            pass
        else:
            return False
        self.__fault.debug_msg("тест 2.1", 'blue')
        self.__mysql_conn.mysql_ins_result('идёт тест 2', '2')
        if self.__proc.procedure_x4_to_x5(setpoint_volt=self.ust_prov, coef_volt=self.coef_volt):
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен TV1", "2")
            return False
        return True

    def st_test_21_btz_3(self) -> bool:
        """
        # 2.2.  Проверка срабатывания блока от сигнала нагрузки:
        """
        self.__fault.debug_msg("тест 2.2", 'blue')
        self.__mysql_conn.mysql_ins_result('идёт тест 2.2', '2')
        self.__ctrl_kl.ctrl_relay('KL63', True)
        sleep(2)
        self.__ctrl_kl.ctrl_relay('KL63', False)
        in_a1, in_a2, in_a5, in_a6 = self.__inputs_a()
        if in_a1 is False and in_a5 is True and in_a2 is True and in_a6 is False:
            pass
        else:
            self.__fault.debug_msg("тест 2.2 положение выходов не соответствует", 'red')
            self.__mysql_conn.mysql_ins_result('неисправен', '2')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(373)
            elif in_a5 is False:
                self.__mysql_conn.mysql_error(374)
            elif in_a2 is False:
                self.__mysql_conn.mysql_error(375)
            elif in_a6 is True:
                self.__mysql_conn.mysql_error(376)
            return False
        self.__fault.debug_msg("тест 2.2 положение выходов соответствует", 'green')
        self.__reset.stop_procedure_3()
        return True

    def st_test_22_btz_3(self) -> bool:
        self.__fault.debug_msg("тест 2.3", 'blue')
        self.__sbros_zashit_kl30()
        in_a1, in_a2, in_a5, in_a6 = self.__inputs_a()
        if in_a1 is False and in_a5 is True and in_a2 is False and in_a6 is True:
            pass
        else:
            self.__fault.debug_msg("тест 2.3 положение выходов не соответствует", 'red')
            self.__mysql_conn.mysql_ins_result('неисправен', '2')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(377)
            elif in_a5 is False:
                self.__mysql_conn.mysql_error(378)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(379)
            elif in_a6 is False:
                self.__mysql_conn.mysql_error(380)
            return False
        self.__fault.debug_msg("тест 2.3 положение выходов соответствует", 'green')
        self.__mysql_conn.mysql_ins_result('исправен', '2')
        return True

    def st_test_30_btz_3(self) -> bool:
        """
        Тест 3. Проверка работоспособности защиты ТЗП блока в режиме «Проверка»
        """
        msg_3 = "Переключите тумблер ПМЗ (1-11) в положение «Работа» " \
                "«Переключите тумблер ТЗП (0.5-1) в положение «Проверка»"
        if my_msg(msg_3):
            pass
        else:
            return False
        self.__fault.debug_msg("тест 3.1", 'blue')
        in_a1, in_a2, in_a5, in_a6 = self.__inputs_a()
        if in_a1 is True and in_a5 is False and in_a2 is False and in_a6 is True:
            pass
        else:
            self.__fault.debug_msg("тест 3.1 положение выходов не соответствует", 'red')
            self.__mysql_conn.mysql_ins_result('неисправен', '3')
            if in_a1 is False:
                self.__mysql_conn.mysql_error(381)
            elif in_a5 is True:
                self.__mysql_conn.mysql_error(382)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(383)
            elif in_a6 is False:
                self.__mysql_conn.mysql_error(384)
            return False
        self.__fault.debug_msg("тест 3.1 положение выходов соответствует", 'green')
        return True

    def st_test_31_btz_3(self) -> bool:
        """
        3.2. Сброс защит после проверки
        """
        msg_4 = "Переключите тумблер ТЗП (0.5…1) на корпусе блока в положение \"Работа\""
        if my_msg(msg_4):
            pass
        else:
            return False
        self.__fault.debug_msg("тест 3.2", 'blue')
        self.__sbros_zashit_kl30()
        in_a1, in_a2, in_a5, in_a6 = self.__inputs_a()
        if in_a1 is False and in_a5 is True and in_a2 is False and in_a6 is True:
            pass
        else:
            self.__fault.debug_msg("тест 3.2 положение выходов не соответствует", 'red')
            self.__mysql_conn.mysql_ins_result('неисправен', '3')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(385)
            elif in_a5 is False:
                self.__mysql_conn.mysql_error(386)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(387)
            elif in_a6 is False:
                self.__mysql_conn.mysql_error(388)
            return False
        self.__fault.debug_msg("тест 3.2 положение выходов соответствует", 'green')
        self.__mysql_conn.mysql_ins_result('исправен', '3')
        return True

    def st_test_40_btz_3(self) -> bool:
        """
        Тест 4. Проверка срабатывания защиты ПМЗ блока по уставкам
        """
        msg_4_1 = "Установите регулятор уставок ТЗП на блоке в положение 1.0"
        if my_msg(msg_4_1):
            pass
        else:
            return False
        k = 0
        for i in self.list_ust_pmz:
            self.__fault.debug_msg(f'тест 4 уставка {self.list_ust_pmz_num[k]}', 'blue')
            msg_5 = 'Установите регулятор уставок ПМЗ на блоке в положение '
            msg_result_pmz = my_msg_2(f'{msg_5} {self.list_ust_pmz_num[k]}')
            if msg_result_pmz == 0:
                pass
            elif msg_result_pmz == 1:
                return False
            elif msg_result_pmz == 2:
                self.__mysql_conn.mysql_add_message(f'уставка {self.list_ust_pmz_num[k]} пропущена')
                self.list_delta_percent_pmz.append('пропущена')
                self.list_delta_t_pmz.append('пропущена')
                k += 1
                continue
            self.__mysql_conn.mysql_ins_result(f'уставка {self.list_ust_pmz_num[k]}', "4")
            if self.__proc.procedure_x4_to_x5(setpoint_volt=i, coef_volt=self.coef_volt):
                pass
            else:
                self.__mysql_conn.mysql_ins_result("неисправен TV1", "4")
                return False
            # 4.1.  Проверка срабатывания блока от сигнала нагрузки:
            meas_volt = self.__read_mb.read_analog()
            # Δ%= 0.0062*U42+1.992* U4
            calc_delta_percent_pmz = 0.0062 * meas_volt ** 2 + 1.992 * meas_volt
            self.list_delta_percent_pmz.append(f'{calc_delta_percent_pmz:.2f}')
            for qw in range(4):
                self.calc_delta_t_pmz = self.__ctrl_kl.ctrl_ai_code_v0(103)
                self.__mysql_conn.mysql_add_message(f'уставка {self.list_ust_pmz_num[k]} '
                                                    f'дельта t: {self.calc_delta_t_pmz:.1f}')
                if 3000 < self.calc_delta_t_pmz <= 9999:
                    self.__sbros_zashit_kl30()
                    sleep(3)
                    qw += 1
                    continue
                else:
                    qw = 0
                    break
            self.__fault.debug_msg(f'тест 4.1 дельта t: {self.calc_delta_t_pmz:.1f} '
                                   f'уставка {self.list_ust_pmz_num[k]}', 'orange')
            if self.calc_delta_t_pmz < 10:
                self.list_delta_t_pmz.append(f'< 10')
            elif self.calc_delta_t_pmz > 3000:
                self.list_delta_t_pmz.append(f'> 3000')
            else:
                self.list_delta_t_pmz.append(f'{self.calc_delta_t_pmz:.1f}')
            self.__mysql_conn.mysql_add_message(f'уставка {self.list_ust_pmz_num[k]} '
                                                f'дельта t: {self.calc_delta_t_pmz:.1f}')
            self.__mysql_conn.mysql_add_message(f'уставка {self.list_ust_pmz_num[k]} '
                                                f'дельта %: {calc_delta_percent_pmz:.2f}')
            in_a1, in_a2, in_a5, in_a6 = self.__inputs_a()
            if in_a1 is False and in_a5 is True and in_a2 is True and in_a6 is False:
                self.__fault.debug_msg("тест 4.1 положение выходов соответствует", 'green')
                self.__reset.stop_procedure_3()
                if self.__subtest_45():
                    k += 1
                    continue
                else:
                    return False
            else:
                self.__fault.debug_msg("тест 4.1 положение выходов не соответствует", 1)
                self.__mysql_conn.mysql_ins_result('неисправен', '4')
                self.__mysql_conn.mysql_error(389)
                if self.__subtest_42(i, k):
                    k += 1
                    continue
                else:
                    return False
        self.__mysql_conn.mysql_ins_result('исправен', '4')
        return True

    def st_test_50_btz_3(self) -> bool:
        """
        Тест 5. Проверка срабатывания защиты ТЗП блока по уставкам
        """
        m = 0
        for n in self.list_ust_tzp:
            msg_7 = 'Установите регулятор уставок на блоке в положение '
            msg_result_tzp = my_msg_2(f'{msg_7} {self.list_ust_tzp_num[m]}')
            if msg_result_tzp == 0:
                pass
            elif msg_result_tzp == 1:
                return False
            elif msg_result_tzp == 2:
                self.__mysql_conn.mysql_add_message(f'уставка {self.list_ust_tzp_num[m]} пропущена')
                self.list_delta_percent_tzp.append('пропущена')
                self.list_delta_t_tzp.append('пропущена')
                m += 1
                continue
            self.__mysql_conn.mysql_ins_result(f'уставка {self.list_ust_tzp_num[m]}', "5")
            if self.__proc.procedure_x4_to_x5(setpoint_volt=n, coef_volt=self.coef_volt):
                pass
            else:
                self.__mysql_conn.mysql_ins_result("неисправен TV1", "5")
                return False
            meas_volt = self.__read_mb.read_analog()
            # Δ%= 0.003*U42[i]+2.404* U4[i]
            calc_delta_percent_tzp = 0.003 * meas_volt ** 2 + 2.404 * meas_volt
            self.list_delta_percent_tzp.append(f'{calc_delta_percent_tzp:.2f}')
            # 5.4.  Проверка срабатывания блока от сигнала нагрузки:
            self.__mysql_conn.progress_level(0.0)
            self.__ctrl_kl.ctrl_relay('KL63', True)
            in_b1 = self.__inputs_b1()
            i1 = 0
            while in_b1 is False and i1 <= 4:
                in_b0, in_b1 = self.__inputs_b()
                i1 += 1
            start_timer_tzp = time()
            calc_delta_t_tzp = 0
            in_a5 = self.__inputs_a5()
            while in_a5 is True and calc_delta_t_tzp <= 370:
                in_a5 = self.__inputs_a5()
                stop_timer_tzp = time()
                calc_delta_t_tzp = stop_timer_tzp - start_timer_tzp
                self.__mysql_conn.progress_level(calc_delta_t_tzp)
            self.__ctrl_kl.ctrl_relay('KL63', False)
            self.__reset.stop_procedure_3()
            self.__mysql_conn.progress_level(0.0)
            self.__fault.debug_msg(f'тест 5 delta t: {calc_delta_t_tzp:.1f} '
                                   f'уставка {self.list_ust_tzp_num[m]}', 'orange')
            self.list_delta_t_tzp.append(f'{calc_delta_t_tzp:.1f}')
            self.__mysql_conn.mysql_add_message(f'уставка ТЗП {self.list_ust_tzp_num[m]} '
                                                f'дельта t: {calc_delta_t_tzp:.1f}')
            self.__mysql_conn.mysql_add_message(f'уставка ТЗП {self.list_ust_tzp_num[m]} '
                                                f'дельта %: {calc_delta_percent_tzp:.2f}')
            in_a1, in_a2, in_a5, in_a6 = self.__inputs_a()
            if in_a1 is False and in_a5 is True and in_a2 is True and in_a6 is False and calc_delta_t_tzp <= 360:
                if self.__subtest_56():
                    m += 1
                    continue
                else:
                    return False
            else:
                if self.__subtest_55():
                    m += 1
                    continue
                else:
                    return False
        self.__mysql_conn.mysql_ins_result('исправен', '5')
        return True

    def __subtest_55(self):
        self.__sbros_zashit_kl30()
        in_a1, in_a2, in_a5, in_a6 = self.__inputs_a()
        if in_a1 is False and in_a5 is True and in_a2 is False and in_a6 is True:
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '5')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(377)
            elif in_a5 is False:
                self.__mysql_conn.mysql_error(378)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(379)
            elif in_a6 is False:
                self.__mysql_conn.mysql_error(380)
            return False
        return True

    def __subtest_56(self):
        self.__sbros_zashit_kl30()
        in_a1, in_a2, in_a5, in_a6 = self.__inputs_a()
        if in_a1 is False and in_a5 is True and in_a2 is False and in_a6 is True:
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '5')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(377)
            elif in_a5 is False:
                self.__mysql_conn.mysql_error(378)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(379)
            elif in_a6 is False:
                self.__mysql_conn.mysql_error(380)
            return False
        return True

    def __subtest_42(self, i, k) -> bool:
        """
        4.2. Формирование нагрузочного сигнала 1,1*U3[i]:
        4.2.1. Сброс защит после проверки
        """
        self.__sbros_zashit_kl30()
        in_a1, in_a2, in_a5, in_a6 = self.__inputs_a()
        if in_a1 is False and in_a5 is True and in_a2 is False and in_a6 is True:
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '4')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(377)
            elif in_a5 is False:
                self.__mysql_conn.mysql_error(378)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(379)
            elif in_a6 is False:
                self.__mysql_conn.mysql_error(380)
            return False
        if self.__proc.procedure_1_25_35(setpoint_volt=i, coef_volt=self.coef_volt):
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен TV1", "4")
            return False
        # 4.2.2.  Проверка срабатывания блока от сигнала нагрузки:
        meas_volt = self.__read_mb.read_analog()
        # Δ%= 0.0062*U42+1.992* U4
        calc_delta_percent_pmz = 0.0062 * meas_volt ** 2 + 1.992 * meas_volt
        self.list_delta_percent_pmz[-1] = f'{calc_delta_percent_pmz:.2f}'
        for wq in range(4):
            self.calc_delta_t_pmz = self.__ctrl_kl.ctrl_ai_code_v0(103)
            if 3000 < self.calc_delta_t_pmz <= 9999:
                self.__sbros_zashit_kl30()
                sleep(3)
                wq += 1
                continue
            else:
                wq = 0
                break
        if self.calc_delta_t_pmz < 10:
            self.list_delta_t_pmz[-1] = f'< 10'
        elif self.calc_delta_t_pmz > 3000:
            self.list_delta_t_pmz[-1] = f'> 3000'
        else:
            self.list_delta_t_pmz[-1] = f'{self.calc_delta_t_pmz:.1f}'
        self.__mysql_conn.mysql_add_message(f'уставка ПМЗ {self.list_ust_pmz_num[k]} '
                                            f'дельта t: {self.calc_delta_t_pmz:.1f}')
        self.__mysql_conn.mysql_add_message(f'уставка ПМЗ {self.list_ust_pmz_num[k]} '
                                            f'дельта %: {calc_delta_percent_pmz:.2f}')
        in_a1, in_a2, in_a5, in_a6 = self.__inputs_a()
        if in_a1 is False and in_a5 is True and in_a2 is True and in_a6 is False:
            if self.__subtest_45():
                pass
            else:
                self.__mysql_conn.mysql_ins_result('неисправен', '4')
        else:
            self.__mysql_conn.mysql_error(389)
            self.__reset.stop_procedure_3()
            # 4.3. Сброс защит после проверки
            self.__sbros_zashit_kl30()
            in_a1, in_a2, in_a5, in_a6 = self.__inputs_a()
            if in_a1 is False and in_a5 is True and in_a2 is False and in_a6 is True:
                pass
            else:
                self.__mysql_conn.mysql_ins_result('неисправен', '4')
                if in_a1 is True:
                    self.__mysql_conn.mysql_error(377)
                elif in_a5 is False:
                    self.__mysql_conn.mysql_error(378)
                elif in_a2 is True:
                    self.__mysql_conn.mysql_error(379)
                elif in_a6 is False:
                    self.__mysql_conn.mysql_error(380)
                return False
        return True

    def __subtest_45(self) -> bool:
        """
        4.5. Расчет относительной нагрузки сигнала
        4.6. Сброс защит после проверки
        """
        self.__sbros_zashit_kl30()
        in_a1, in_a2, in_a5, in_a6 = self.__inputs_a()
        if in_a1 is False and in_a5 is True and in_a2 is False and in_a6 is True:
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '4')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(377)
            elif in_a5 is False:
                self.__mysql_conn.mysql_error(378)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(379)
            elif in_a6 is False:
                self.__mysql_conn.mysql_error(380)
            return False
        return True

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
        in_a6 = self.__read_mb.read_discrete(6)
        if in_a1 is None or in_a2 is None or in_a5 is None or in_a6 is None:
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_a1, in_a2, in_a5, in_a6

    def __inputs_a5(self):
        in_a5 = self.__read_mb.read_discrete(5)
        if in_a5 is None:
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_a5

    def __inputs_b(self):
        in_b0 = self.__read_mb.read_discrete(8)
        in_b1 = self.__read_mb.read_discrete(9)
        if in_b0 is None or in_b1 is None:
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_b0, in_b1

    def __inputs_b1(self):
        in_b1 = self.__read_mb.read_discrete(9)
        if in_b1 is None:
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_b1

    def __sbros_zashit_kl30(self):
        self.__ctrl_kl.ctrl_relay('KL30', True)
        sleep(1.5)
        self.__ctrl_kl.ctrl_relay('KL30', False)
        sleep(3)

    def st_test_btz_3(self) -> bool:
        if self.st_test_10_btz_3():
            if self.st_test_11_btz_3():
                if self.st_test_12_btz_3():
                    if self.st_test_20_btz_3():
                        if self.st_test_21_btz_3():
                            if self.st_test_22_btz_3():
                                if self.st_test_30_btz_3():
                                    if self.st_test_31_btz_3():
                                        if self.st_test_40_btz_3():
                                            if self.st_test_50_btz_3():
                                                return True
        return False

    def result_test_btz_3(self):
        """
        сведение всех результатов измерения, и запись в БД
        """
        for g1 in range(len(self.list_delta_percent_pmz)):
            self.list_result_pmz.append((self.list_ust_pmz_num[g1],
                                         self.list_delta_percent_pmz[g1],
                                         self.list_delta_t_pmz[g1]))
        self.__mysql_conn.mysql_pmz_result(self.list_result_pmz)
        for g2 in range(len(self.list_delta_percent_tzp)):
            self.list_result_tzp.append((self.list_ust_tzp_num[g2],
                                         self.list_delta_percent_tzp[g2],
                                         self.list_delta_t_tzp[g2]))
        self.__mysql_conn.mysql_tzp_result(self.list_result_tzp)

    def full_test_btz_3(self):
        try:
            if self.st_test_btz_3():
                self.result_test_btz_3()
                self.__mysql_conn.mysql_block_good()
                my_msg('Блок исправен', 'green')
            else:
                self.result_test_btz_3()
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
            self.reset_relay.reset_all()
            sys.exit()


if __name__ == '__main__':
    test_btz_3 = TestBTZ3()
    test_btz_3.full_test_btz_3()
    # reset_test_btz_3 = ResetRelay()
    # mysql_conn_btz_3 = MySQLConnect()
    # fault = Bug(True)
    # try:
    #     if test_btz_3.st_test_btz_3():
    #         test_btz_3.result_test_btz_3()
    #         mysql_conn_btz_3.mysql_block_good()
    #         my_msg('Блок исправен', 'green')
    #     else:
    #         test_btz_3.result_test_btz_3()
    #         mysql_conn_btz_3.mysql_block_bad()
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
    #     reset_test_btz_3.reset_all()
    #     sys.exit()
