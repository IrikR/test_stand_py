#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки

Тип блока	        Производитель
МТЗ-5 вер.411256002	Завод Электромашина
"""

import sys
import logging

from time import sleep, time

from gen_func_utils import *
from my_msgbox import *
from my_msgbox_2 import *
from gen_func_procedure import *
from gen_mb_client import *
from gen_mysql_connect import *

__all__ = ["TestMTZ5V411"]


class TestMTZ5V411(object):

    def __init__(self):
        self.__reset = ResetRelay()
        self.__proc = Procedure()
        self.__read_mb = ReadMB()
        self.__ctrl_kl = CtrlKL()
        self.__mysql_conn = MySQLConnect()
        self.__fault = Bug(True)

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

        logging.basicConfig(filename="C:\Stend\project_class\TestMTZ5_411.log",
                            filemode="w",
                            level=logging.DEBUG,
                            encoding="utf-8",
                            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('WARNING')
        self.logger = logging.getLogger(__name__)

    def st_test_10(self) -> bool:
        """

        :return: bool
        """
        self.__inputs_a0()
        if my_msg(self.msg_1):
            if my_msg(self.msg_2):
                return True
        return False

    def st_test_11(self) -> bool:
        """
        Тест 1.1
        :return: bool
        """
        self.__mysql_conn.mysql_ins_result('идёт тест 1.1', '1')
        self.logger.debug("тест 1.1")
        self.__ctrl_kl.ctrl_relay('KL1', True)
        sleep(0.5)
        self.__ctrl_kl.ctrl_relay('KL2', True)
        sleep(1)
        self.__sbros_zashit()
        in_a1, in_a5 = self.__inputs_a()
        self.logger.debug(f"{in_a1 = } (True), {in_a5 = } (False)")
        if in_a1 is True and in_a5 is False:
            pass
        else:
            self.__fault.debug_msg("тест 1.1 положение выходов не соответствует", 'red')
            self.__mysql_conn.mysql_ins_result('неисправен', '1')
            return False
        self.__fault.debug_msg("тест 1.1 положение выходов соответствует", 'green')
        return True

    def st_test_12(self) -> bool:
        """
        1.1. Проверка вероятности наличия короткого замыкания на входе измерительной цепи блока
        :return: bool
        """
        self.logger.debug("тест 1.2")
        self.__mysql_conn.mysql_ins_result('идёт тест 1.2', '1')
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
        self.__fault.debug_msg(f'напряжение после включения KL63\t{meas_volt:.2f}\tдолжно быть '
                               f'от\t{min_volt:.2f}\tдо\t{max_volt:.2f}', 'orange')
        if min_volt <= meas_volt <= max_volt:
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '1')
            self.__mysql_conn.mysql_error(455)
            self.__reset.sbros_kl63_proc_1_21_31()
            return False
        self.__reset.sbros_kl63_proc_1_21_31()
        return True

    def st_test_13(self) -> bool:
        """
        1.1.3. Финишные операции отсутствия короткого замыкания на входе измерительной части блока::
        1.2. Определение коэффициента Кс отклонения фактического напряжения от номинального
        :return: bool
        """
        self.logger.debug("тест 1.3")
        self.__mysql_conn.mysql_ins_result('идёт тест 1.3', '1')
        self.__fault.debug_msg("1.2. Определение коэффициента Кс отклонения фактического "
                               "напряжения от номинального", 'blue')
        self.coef_volt = self.__proc.procedure_1_22_32()
        if self.coef_volt != 0.0:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен TV1", "1")
            self.__reset.stop_procedure_32()
            return False
        self.__reset.stop_procedure_32()
        self.__mysql_conn.mysql_ins_result('исправен', '1')
        return True

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
        in_a1, in_a5 = self.__inputs_a()
        self.logger.debug(f"{in_a1 = } (False), {in_a5 = } (True)")
        if in_a1 is False and in_a5 is True:
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '2')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(444)
            elif in_a5 is False:
                self.__mysql_conn.mysql_error(445)
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
        self.__mysql_conn.mysql_ins_result('идёт тест 2.1', '2')
        self.__fault.debug_msg("2.1 Сброс защит после проверки", 'blue')
        self.__sbros_zashit()
        in_a1, in_a5 = self.__inputs_a()
        self.logger.debug(f"{in_a1 = } (True), {in_a5 = } (False)")
        if in_a1 is True and in_a5 is False:
            pass
        else:
            self.__fault.debug_msg("положение выходов не соответствует", 'red')
            self.__mysql_conn.mysql_ins_result('неисправен', '2')
            if in_a1 is False:
                self.__mysql_conn.mysql_error(446)
            elif in_a5 is True:
                self.__mysql_conn.mysql_error(447)
            return False
        self.__fault.debug_msg("положение выходов соответствует", 'green')
        self.__mysql_conn.mysql_ins_result('исправен', '2')
        return True

    def st_test_30(self) -> bool:
        """
        Тест 3. Проверка срабатывания защиты ПМЗ блока по уставкам
        :return: bool
        """
        self.logger.debug("тест 3.0")
        self.__mysql_conn.mysql_ins_result('идёт тест 3', '3')
        k = 0
        for i in self.list_ust_mtz_volt:
            msg_result_mtz = my_msg_2(f'{self.msg_5} {self.list_ust_mtz_num[k]}')
            if msg_result_mtz == 0:
                pass
            elif msg_result_mtz == 1:
                return False
            elif msg_result_mtz == 2:
                self.__mysql_conn.mysql_add_message(f'уставка {self.list_ust_mtz_num[k]} пропущена')
                self.list_delta_percent_mtz.append('пропущена')
                self.list_delta_t_mtz.append('пропущена')
                k += 1
                continue
            if self.__proc.procedure_x4_to_x5(setpoint_volt=i, coef_volt=self.coef_volt):
                pass
            else:
                self.__mysql_conn.mysql_ins_result("неисправен TV1", "3")
                return False
            self.__fault.debug_msg("3.1.  Проверка срабатывания блока от сигнала нагрузки:", 'blue')
            # 3.1.  Проверка срабатывания блока от сигнала нагрузки:
            self.__mysql_conn.mysql_ins_result(f'уставка {self.list_ust_mtz_num[k]}', '3')
            # Δ%= 3.4364*(U4[i])/0.63
            meas_volt = self.__read_mb.read_analog()
            calc_delta_percent_mtz = 3.4364 * meas_volt / 0.63
            self.__fault.debug_msg(f'дельта %\t{calc_delta_percent_mtz:.2f}', 'orange')
            self.list_delta_percent_mtz.append(f'{calc_delta_percent_mtz:.2f}')

            calc_delta_t_mtz, in_a1, in_a5 = self.__subtest_time_calc()
            self.logger.debug(f"время срабатывания: {calc_delta_t_mtz}мс: {in_a1 = } (True), {in_a5 = } (False)")
            self.__reset.stop_procedure_3()
            if calc_delta_percent_mtz != 9999 and in_a1 is False and in_a5 is True:
                self.__fault.debug_msg(f'дельта t\t{calc_delta_t_mtz}', 'orange')
                self.list_delta_t_mtz.append(f'{calc_delta_t_mtz:.1f}')
                self.__mysql_conn.mysql_add_message(f'уставка {self.list_ust_mtz_num[k]}\t'
                                                    f'дельта t: {calc_delta_t_mtz:.1f}\t'
                                                    f'дельта %: {calc_delta_percent_mtz:.2f}')
                if self.__subtest_33():
                    k += 1
                    continue
                else:
                    self.__mysql_conn.mysql_ins_result('неисправен', '3')
                    return False
            else:
                if self.__subtest_32(i, k):
                    if self.__subtest_33():
                        k += 1
                        continue
                    else:
                        self.health_flag = True
                        self.__mysql_conn.mysql_error(448)
                        self.__mysql_conn.mysql_ins_result('неисправен', '3')
                        return False
                else:
                    self.health_flag = True
                    if self.__subtest_33():
                        k += 1
                        continue
                    else:
                        self.__mysql_conn.mysql_ins_result('неисправен', '3')
                        return False
        self.__mysql_conn.mysql_ins_result('исправен', '3')
        return True

    def st_test_40(self) -> bool:
        """
        Тест 4. Проверка срабатывания защиты от перегрузки блока по уставкам
        :return: bool
        """
        self.logger.debug("тест 4.0")
        if my_msg(self.msg_6):
            pass
        else:
            return False
        self.__mysql_conn.mysql_ins_result('идёт тест 4', '4')
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
                self.__mysql_conn.mysql_add_message(f'уставка {self.list_ust_tzp_num[m]} пропущена')
                self.list_delta_percent_tzp.append('пропущена')
                self.list_delta_t_tzp.append('пропущена')
                m += 1
                continue
            self.__mysql_conn.mysql_ins_result(f'уставка {self.list_ust_tzp_num[m]}', '4')
            if self.__proc.procedure_x4_to_x5(setpoint_volt=n, coef_volt=self.coef_volt):
                pass
            else:
                self.__mysql_conn.mysql_ins_result("неисправен TV1", "4")
                return False
            # Δ%= 3.4364*U4[i]/0.63
            meas_volt = self.__read_mb.read_analog()
            calc_delta_percent_tzp = 3.4364 * meas_volt / 0.63
            self.__fault.debug_msg(f'дельта %\t{calc_delta_percent_tzp:.2f}', 'orange')
            self.list_delta_percent_tzp.append(f'{calc_delta_percent_tzp:.2f}')
            # 4.4.  Проверка срабатывания блока от сигнала нагрузки:
            self.__ctrl_kl.ctrl_relay('KL63', True)
            r = 0
            in_b1 = self.__inputs_b()
            while in_b1 is False and r <= 5:
                in_b1 = self.__inputs_b()
                r += 1
            start_timer_tzp = time()
            delta_t_tzp = 0
            in_a5 = self.__inputs_a5()
            while in_a5 is False and delta_t_tzp <= 30:
                delta_t_tzp = time() - start_timer_tzp
                in_a5 = self.__inputs_a5()
            stop_timer_tzp = time()
            calc_delta_t_tzp = stop_timer_tzp - start_timer_tzp
            self.__fault.debug_msg(f'тест 3 delta t: {calc_delta_t_tzp:.1f}', 'orange')

            in_a1, in_a5 = self.__inputs_a()
            self.logger.debug(f"{in_a1 = } (False), {in_a5 = } (True)")
            self.__ctrl_kl.ctrl_relay('KL63', False)
            self.__reset.stop_procedure_3()
            if in_a1 is False and in_a5 is True and calc_delta_t_tzp <= 30:
                self.list_delta_t_tzp.append(f'{calc_delta_t_tzp:.1f}')
                self.__mysql_conn.mysql_add_message(f'уставка {self.list_ust_tzp_num[m]}\t'
                                                    f'дельта t: {calc_delta_t_tzp:.1f}\t'
                                                    f'дельта %: {calc_delta_percent_tzp:.2f}')
                self.__fault.debug_msg("положение выходов соответствует", 'green')
                if self.__subtest_45():
                    m += 1
                    continue
                else:
                    return False
            else:
                self.list_delta_t_tzp.append(f'неисправен')
                self.__mysql_conn.mysql_add_message(f'уставка {self.list_ust_tzp_num[m]}\t'
                                                    f'дельта t: {calc_delta_t_tzp:.1f}\t'
                                                    f'дельта %: {calc_delta_percent_tzp:.2f}')
                self.__fault.debug_msg("положение выходов не соответствует", 'red')
                self.__mysql_conn.mysql_error(448)
                self.health_flag = True
                if self.__subtest_45():
                    m += 1
                    continue
                else:
                    return False
        self.__mysql_conn.mysql_ins_result('исправен', '4')
        return True

    def __subtest_time_calc(self) -> [float, bool, bool]:
        self.logger.debug("подтест проверки времени срабатывания")
        for qw in range(3):
            self.logger.debug(f"попытка: {qw}")
            self.delta_t_mtz = self.__ctrl_kl.ctrl_ai_code_v0(110)
            self.in_1, self.in_5 = self.__inputs_a()
            self.logger.debug(f"время срабатывания: {self.delta_t_mtz}, "
                              f"{self.in_1 = } is False, "
                              f"{self.in_5 = } is True")
            if self.delta_t_mtz == 9999:
                qw += 1
                continue
            elif self.delta_t_mtz != 9999 and self.in_1 is False and self.in_5 is True:
                break
            else:
                qw += 1
                continue
        return self.delta_t_mtz, self.in_1, self.in_5

    def __subtest_32(self, i, k):
        """
        3.2. Формирование нагрузочного сигнала 1,15*U3[i]:
        :param i: напряжение уставки
        :param k: порядковый номер в цикле
        :return: bool
        """
        self.logger.debug("тест 3.2")
        self.__sbros_zashit()
        in_a1, in_a5 = self.__inputs_a()
        self.logger.debug(f"{in_a1 = } is True and {in_a5 = } is False")
        if in_a1 is True and in_a5 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '3')
            if in_a1 is False:
                self.__mysql_conn.mysql_error(446)
            elif in_a5 is True:
                self.__mysql_conn.mysql_error(447)
            return False
        if self.__proc.procedure_x4_to_x5(coef_volt=self.coef_volt, setpoint_volt=(i * 1.15)):
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '3')
            return False
        # 3.2.2.  Проверка срабатывания блока от сигнала нагрузки:
        meas_volt = self.__read_mb.read_analog()
        calc_delta_percent_mtz = 3.4364 * meas_volt / 0.63
        self.list_delta_percent_mtz[-1] = f'{calc_delta_percent_mtz:.2f}'

        calc_delta_t_mtz, in_a1, in_a5 = self.__subtest_time_calc()

        self.__reset.stop_procedure_3()

        if calc_delta_percent_mtz != 9999 and in_a1 is False and in_a5 is True:
            self.list_delta_t_mtz[-1] = f'{calc_delta_t_mtz:.1f}'
            self.__mysql_conn.mysql_add_message(f'уставка {self.list_ust_mtz_num[k]}\t'
                                                f'дельта t: {calc_delta_t_mtz:.1f}\t'
                                                f'дельта %: {calc_delta_percent_mtz:.2f}')
            return True
        else:
            self.list_delta_t_mtz[-1] = f'неисправен'
            self.__mysql_conn.mysql_add_message(f'уставка {self.list_ust_mtz_num[k]}\t'
                                                f'дельта t: {calc_delta_t_mtz:.1f}\t'
                                                f'дельта %: {calc_delta_percent_mtz:.2f}')
            self.health_flag = True
            self.__mysql_conn.mysql_error(448)
            return False

    def __subtest_33(self) -> bool:
        """
        3.3. Сброс защит после проверки
        3.5. Расчет относительной нагрузки сигнала
        Δ%= 3.4364*(U4[i])/0.63
        :return: bool
        """
        self.logger.debug("тест 3.3")
        self.__sbros_zashit()
        in_a1, in_a5 = self.__inputs_a()
        self.logger.debug(f"{in_a1 = } is True and {in_a5 = } is False")
        if in_a1 is True and in_a5 is False:
            return True
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '3')
            if in_a1 is False:
                self.__mysql_conn.mysql_error(446)
            elif in_a5 is True:
                self.__mysql_conn.mysql_error(447)
            return False
    
    def __subtest_45(self) -> bool:
        """
        4.6.1. Сброс защит после проверки
        Определение кратности сигнала нагрузки: Δ%= 3.4364*U4[i]/0.63
        :return: bool
        """
        self.logger.debug("тест 4.5")
        self.__sbros_zashit()
        in_a1, in_a5 = self.__inputs_a()
        self.logger.debug(f"{in_a1 = } is True and {in_a5 = } is False")
        if in_a1 is True and in_a5 is False:
            self.__fault.debug_msg("тест 4.5 положение выходов соответствует", 'green')
            return True
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '4')
            self.__fault.debug_msg("тест 4.5 положение выходов не соответствует", 'red')
            if in_a1 is False:
                self.__mysql_conn.mysql_error(446)
            elif in_a5 is True:
                self.__mysql_conn.mysql_error(447)
            return False
    
    def __sbros_zashit(self):
        self.__ctrl_kl.ctrl_relay('KL1', False)
        sleep(1.5)
        self.__ctrl_kl.ctrl_relay('KL1', True)
        sleep(2)
        self.logger.debug("выполнен сброс защит")

    def __inputs_a0(self):
        in_a0 = self.__read_mb.read_discrete(0)
        if in_a0 is None:
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_a0

    def __inputs_a(self):
        in_a1 = self.__read_mb.read_discrete(1)
        in_a5 = self.__read_mb.read_discrete(5)
        if in_a1 is None or in_a5 is None:
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_a1, in_a5
    
    def __inputs_a5(self):
        in_a5 = self.__read_mb.read_discrete(5)
        if in_a5 is None:
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_a5

    def __inputs_b(self):
        in_b1 = self.__read_mb.read_discrete(9)
        if in_b1 is None:
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_b1

    def st_test_mtz(self) -> [bool, bool]:
        """
        функция собирающая все алгоритмы в одну функцию
        :return: bool
        """
        if self.st_test_10():
            if self.st_test_11():
                if self.st_test_12():
                    if self.st_test_13():
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
        self.__mysql_conn.mysql_pmz_result(self.list_mtz_result)
        for g2 in range(len(self.list_delta_percent_tzp)):
            self.logger.debug(f"уставка: {self.list_ust_tzp_num[g2]}, "
                              f"%: {self.list_delta_percent_tzp[g2]}, "
                              f"t: {self.list_delta_t_tzp[g2]}")
            self.list_tzp_result.append(
                (self.list_ust_tzp_num[g2], self.list_delta_percent_tzp[g2], self.list_delta_t_tzp[g2]))
        self.__mysql_conn.mysql_tzp_result(self.list_tzp_result)
        self.logger.debug("результаты тестов записаны в БД")


if __name__ == '__main__':
    test_mtz = TestMTZ5V411()
    reset_test_mtz = ResetRelay()
    mysql_conn_mtz = MySQLConnect()
    fault = Bug(True)
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
        fault.debug_msg(mce, 'red')
        my_msg(f'{mce}', 'red')
    except HardwareException as hwe:
        my_msg(f'{hwe}', 'red')
    finally:
        reset_test_mtz.reset_all()
        sys.exit()
