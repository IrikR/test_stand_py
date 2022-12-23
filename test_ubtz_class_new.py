#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки

Тип блока: УБТЗ
Производитель: Нет производителя, Горэкс-Светотехника

"""

import logging
import sys
from time import sleep, time

from general_func.database import *
from general_func.exception import *
from general_func.modbus import *
from general_func.procedure import *
from general_func.reset import ResetRelay, ResetProtection
from general_func.subtest import ReadOPCServer, ProcedureFull
from gui.msgbox_1 import *
from gui.msgbox_2 import *

__all__ = ["TestUBTZ"]


class TestUBTZ:

    def __init__(self):
        self.reset_relay = ResetRelay()
        self.reset_protect = ResetProtection()
        self.proc = Procedure()
        self.proc_full = ProcedureFull()
        self.di_read = DIRead()
        self.ctrl_kl = CtrlKL()
        self.mysql_conn = MySQLConnect()
        self.di_read_full = ReadOPCServer()

        self.list_ust_bmz_num = (1, 2, 3, 4, 5, 6, 7)
        self.list_ust_tzp_num = (1, 2, 3, 4, 5, 6, 7)
        self.list_ust_bmz_volt = (6.9, 13.8, 27.4, 41.1, 54.8, 68.5, 82.2)
        self.list_ust_tzp_volt = (11.2, 15.0, 18.7, 22.4, 26.2, 29.9, 33.6)

        self.coef_volt: float = 0.0
        self.calc_delta_t_bmz = 0.0
        self.health_flag: bool = False

        self.list_delta_t_tzp = []
        self.list_delta_t_bmz = []
        self.list_bmz_result = []
        self.list_tzp_result = []

        self.msg_1 = "Убедитесь в отсутствии других блоков в панелях разъемов и вставьте " \
                     "блок в соответствующий разъем панели С"
        self.msg_2 = "Переключите регулятор МТЗ на корпусе блока в положение «1», регулятор ТЗП в положение «0»"
        self.msg_3 = "Установите регулятор МТЗ, расположенный на корпусе блока, в положение"
        # self.msg_4 = "Установите регулятор МТЗ, расположенный на блоке, в положение «0»"
        self.msg_5 = "Установите регулятор ТЗП, расположенный на блоке в положение"

        #
        logging.basicConfig(
            filename="C:\\Stend\\project_class\\log\\TestUBTZ.log",
            filemode="w",
            level=logging.DEBUG,
            encoding="utf-8",
            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('WARNING')
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))

    def st_test_10(self) -> bool:
        self.logger.debug("старт теста 1.0")
        if my_msg(self.msg_1):
            if my_msg(self.msg_2):
                pass
            else:
                return False
        else:
            return False
        self.mysql_conn.mysql_ins_result("идёт тест 1.0", '1')
        self.ctrl_kl.ctrl_relay('KL22', True)
        self.ctrl_kl.ctrl_relay('KL66', True)
        self.reset_protect.sbros_zashit_ubtz()
        sleep(2)
        if self.di_read_full.subtest_4di(test_num=1, subtest_num=1.0,
                                         err_code_a=451, err_code_b=452, err_code_c=453, err_code_d=454,
                                         position_a=False, position_b=True, position_c=False, position_d=True,
                                         di_a='in_a1', di_b='in_a5', di_c='in_a2', di_d='in_a6'):
            return True
        return False

    def st_test_11(self) -> bool:
        """
        1.1.2. Проверка отсутствия короткого замыкания на входе измерительной части блока:
        1.2. Определение коэффициента Кс отклонения фактического напряжения от номинального.
        :return:
        """
        if self.proc_full.procedure_1_full(test_num=1, subtest_num=1.1, coef_min_volt=0.6):
            self.coef_volt = self.proc_full.procedure_2_full(test_num=1, subtest_num=1.2)
            return True
        return False

    def st_test_20(self) -> bool:
        """
        Тест 2. Проверка срабатывания защиты БМЗ блока по уставкам.
        :return:
        """
        k = 0
        for i in self.list_ust_bmz_volt:
            msg_result_bmz = my_msg_2(f'{self.msg_3} {self.list_ust_bmz_num[k]}')
            if msg_result_bmz == 0:
                pass
            elif msg_result_bmz == 1:
                return False
            elif msg_result_bmz == 2:
                self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_bmz_num[k]} пропущена')
                self.list_delta_t_bmz.append('пропущена')
                k += 1
                continue
            self.mysql_conn.mysql_ins_result(f'уставка БМЗ {self.list_ust_bmz_num[k]}', '1')
            if self.proc.procedure_x4_to_x5(coef_volt=self.coef_volt, setpoint_volt=i):
                pass
            else:
                self.mysql_conn.mysql_ins_result('неисправен TV1', '1')
                return False
            # 3.1.  Проверка срабатывания блока от сигнала нагрузки:
            for qw in range(4):
                self.calc_delta_t_bmz = self.ctrl_kl.ctrl_ai_code_v0(109)
                self.logger.debug(f'тест 2, дельта t\t{self.calc_delta_t_bmz:.1f}')
                if self.calc_delta_t_bmz == 9999:
                    self.reset_protect.sbros_zashit_ubtz()
                    continue
                else:
                    break
            in_a1, in_a2, in_a5, in_a6 = self.di_read.di_read('in_a1', 'in_a2', 'in_a5', 'in_a6')
            self.reset_relay.stop_procedure_3()
            if self.calc_delta_t_bmz < 10:
                self.list_delta_t_bmz.append(f'< 10')
            elif self.calc_delta_t_bmz == 9999:
                self.list_delta_t_bmz.append(f'неисправен')
            else:
                self.list_delta_t_bmz.append(f'{self.calc_delta_t_bmz:.1f}')
            self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_bmz_num[k]} '
                                              f'дельта t: {self.calc_delta_t_bmz:.1f}')
            self.logger.debug(f'{in_a1 = } (T), {in_a2 = } (F), {in_a5 = } (F), {in_a6 = } (T)')
            if in_a1 is True and in_a5 is False and in_a2 is False and in_a6 is True:
                self.logger.debug('тест 2 положение выходов соответствует')
                if self.subtest_33_or_45(test_num=2, subtest_num=2.0):
                    k += 1
                    continue
                else:
                    self.mysql_conn.mysql_ins_result("тест 2 неисправен", '1')
                    self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_bmz_num[k]}: '
                                                      f'не срабатывает сброс защит')
                    k += 1
                    continue
            else:
                self.logger.debug('тест 2 положение выходов не соответствует')
                if in_a1 is False:
                    self.mysql_conn.mysql_error(456)
                elif in_a5 is True:
                    self.mysql_conn.mysql_error(457)
                elif in_a2 is True:
                    self.mysql_conn.mysql_error(458)
                elif in_a6 is False:
                    self.mysql_conn.mysql_error(459)
                if self.subtest_32(i=i, k=k):
                    if self.subtest_33_or_45(test_num=2, subtest_num=2.0):
                        k += 1
                        continue
                    else:
                        self.mysql_conn.mysql_ins_result("тест 2 неисправен", '1')
                        self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_bmz_num[k]}: '
                                                          f'не срабатывает сброс защит')
                        return False
                else:
                    if self.subtest_33_or_45(test_num=2, subtest_num=2.0):
                        k += 1
                        continue
                    else:
                        self.mysql_conn.mysql_ins_result("тест 2 неисправен", '1')
                        self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_bmz_num[k]}: '
                                                          f'не срабатывает сброс защит')
                        return False
        self.mysql_conn.mysql_ins_result("тест 2 исправен", '1')
        return True

    def st_test_30(self) -> bool:
        """
        Тест 3. Проверка срабатывания защиты ТЗП блока по уставкам.
        :return:
        """
        m = 0
        for n in self.list_ust_tzp_volt:
            msg_result_tzp = my_msg_2(f'{self.msg_5} {self.list_ust_tzp_num[m]}')
            if msg_result_tzp == 0:
                pass
            elif msg_result_tzp == 1:
                return False
            elif msg_result_tzp == 2:
                self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_tzp_num[m]} пропущена')
                self.list_delta_t_tzp.append('пропущена')
                m += 1
                continue
            self.mysql_conn.mysql_ins_result(f'уставка ТЗП {self.list_ust_tzp_num[m]}', '1')
            if self.proc.procedure_x4_to_x5(coef_volt=self.coef_volt, setpoint_volt=n):
                pass
            else:
                self.mysql_conn.mysql_ins_result("тест 3 неисправен TV1", '1')
                return False
            # 4.4.  Проверка срабатывания блока от сигнала нагрузки:
            self.ctrl_kl.ctrl_relay('KL63', True)
            self.mysql_conn.progress_level(0.0)
            in_b1, *_ = self.di_read.di_read('in_b1')
            a = 0
            while in_b1 is False and a < 10:
                a += 1
                in_b1, *_ = self.di_read.di_read('in_b1')
            start_timer = time()
            sub_timer = 0
            in_a6, *_ = self.di_read.di_read('in_a6')
            while in_a6 is True and sub_timer <= 370:
                sub_timer = time() - start_timer
                self.logger.debug(f'времени прошло: {sub_timer}')
                self.mysql_conn.progress_level(sub_timer)
                sleep(0.2)
                in_a6, *_ = self.di_read.di_read('in_a6')
            stop_timer = time()
            in_a1, in_a2, in_a5, in_a6 = self.di_read.di_read('in_a1', 'in_a2', 'in_a5', 'in_a6')
            self.logger.debug(f'{in_a1 = } (F), {in_a2 = } (F), {in_a5 = } (T), {in_a6 = } (T)')
            self.reset_relay.stop_procedure_3()
            self.mysql_conn.progress_level(0.0)
            calc_delta_t_tzp = stop_timer - start_timer
            self.logger.debug(f'тест 3 delta t:\t{calc_delta_t_tzp:.1f}')
            self.list_delta_t_tzp.append(f'{calc_delta_t_tzp:.1f}')
            self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_tzp_num[m]} '
                                              f'дельта t: {calc_delta_t_tzp:.1f}')
            if in_a1 is False and in_a5 is True and in_a2 is False and in_a6 is True and calc_delta_t_tzp <= 360:
                if self.subtest_33_or_45(test_num=3, subtest_num=3.0):
                    m += 1
                    continue
                else:
                    self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_tzp_num[m]}: '
                                                      f'не срабатывает сброс защит')
                    return False
            else:
                if in_a1 is True:
                    self.mysql_conn.mysql_error(451)
                elif in_a5 is True:
                    self.mysql_conn.mysql_error(452)
                elif in_a2 is True:
                    self.mysql_conn.mysql_error(453)
                elif in_a6 is True:
                    self.mysql_conn.mysql_error(454)
                self.mysql_conn.mysql_ins_result("тест 3 неисправен", '1')
                if self.subtest_33_or_45(test_num=3, subtest_num=3.0):
                    m += 1
                    continue
                else:
                    self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_tzp_num[m]}: '
                                                      f'не срабатывает сброс защит')
                    return False
        self.ctrl_kl.ctrl_relay('KL22', False)
        self.ctrl_kl.ctrl_relay('KL66', False)
        self.logger.debug(f"ТЗП дельта t: {self.list_delta_t_tzp}")
        self.mysql_conn.mysql_ins_result("исправен", '1')
        return True

    def subtest_32(self, i, k):
        """
        3.2. Формирование нагрузочного сигнала 1,1*U3[i]:
        3.2.1. Сброс защит после проверки
        :return:
        """
        self.subtest_33_or_45(test_num=3, subtest_num=3.2)
        self.logger.debug("тест 3.1 положение выходов соответствует")
        if self.proc.procedure_1_24_34(coef_volt=self.coef_volt, setpoint_volt=i, factor=1.1):
            pass
        else:
            self.mysql_conn.mysql_ins_result("неисправен TV1", '1')
            return False
        # 3.2.2.  Проверка срабатывания блока от сигнала нагрузки:
        for wq in range(4):
            self.calc_delta_t_bmz = self.ctrl_kl.ctrl_ai_code_v0(109)
            self.logger.debug(f'тест 3 delta t:\t{self.calc_delta_t_bmz:.1f}')
            if self.calc_delta_t_bmz == 9999:
                self.reset_protect.sbros_zashit_ubtz()
                continue
            else:
                break
        self.reset_relay.stop_procedure_3()
        in_a1, in_a2, in_a5, in_a6 = self.di_read.di_read('in_a1', 'in_a2', 'in_a5', 'in_a6')
        if self.calc_delta_t_bmz < 10:
            self.list_delta_t_bmz[-1] = f'< 10'
        elif self.calc_delta_t_bmz == 9999:
            self.list_delta_t_bmz[-1] = f'неисправен'
        else:
            self.list_delta_t_bmz[-1] = f'{self.calc_delta_t_bmz:.1f}'
        self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_bmz_num[k]}: '
                                          f'дельта t: {self.calc_delta_t_bmz:.1f}')
        self.logger.debug(f'{in_a1 = }, {in_a2 = }, {in_a5 = }, {in_a6 = }')
        if in_a1 is True and in_a5 is False and in_a2 is False and in_a6 is True:
            pass
        else:
            self.logger.debug("тест 3.2 положение выходов не соответствует")
            if in_a1 is True:
                self.mysql_conn.mysql_error(464)
            elif in_a5 is True:
                self.mysql_conn.mysql_error(465)
            elif in_a2 is True:
                self.mysql_conn.mysql_error(466)
            elif in_a6 is True:
                self.mysql_conn.mysql_error(467)
            return False
        self.logger.debug("тест 3.2 положение выходов соответствует")
        return True

    def subtest_33_or_45(self, test_num: int, subtest_num: float) -> bool:
        """
        3.3. Сброс защит после проверки
        :return:
        """
        self.reset_protect.sbros_zashit_ubtz()
        sleep(2)
        if self.di_read_full.subtest_4di(test_num=test_num, subtest_num=subtest_num,
                                         err_code_a=460, err_code_b=461, err_code_c=462, err_code_d=463,
                                         position_a=False, position_b=True, position_c=False, position_d=True,
                                         di_a='in_a1', di_b='in_a5', di_c='in_a2', di_d='in_a6'):
            return True
        self.mysql_conn.mysql_add_message(f'тест {test_num}: не срабатывает сброс защит')
        return False

    def st_test_ubtz(self) -> [bool, bool]:
        if self.st_test_10():
            if self.st_test_11():
                if self.st_test_20():
                    if self.st_test_30():
                        return True, self.health_flag
        return False, self.health_flag

    def result_test_ubtz(self):
        for g1 in range(len(self.list_delta_t_bmz)):
            self.list_bmz_result.append((self.list_ust_bmz_num[g1], self.list_delta_t_bmz[g1]))
            self.logger.debug(f"запись уставок МТЗ в БД: {self.list_ust_bmz_num[g1]} "
                              f"{self.list_delta_t_bmz[g1]}")
        self.mysql_conn.mysql_ubtz_btz_result(self.list_bmz_result)
        for g2 in range(len(self.list_delta_t_tzp)):
            self.list_tzp_result.append((self.list_ust_tzp_num[g2], self.list_delta_t_tzp[g2]))
            self.logger.debug(f"запись уставок ТЗП в БД: {self.list_ust_tzp_num[g2]} "
                              f"{self.list_delta_t_tzp[g2]}")
        self.mysql_conn.mysql_ubtz_tzp_result(self.list_tzp_result)


if __name__ == '__main__':
    test_ubtz = TestUBTZ()
    reset_test_ubtz = ResetRelay()
    mysql_conn_ubtz = MySQLConnect()
    try:
        test, health_flag = test_ubtz.st_test_ubtz()
        if test and not health_flag:
            test_ubtz.result_test_ubtz()
            mysql_conn_ubtz.mysql_block_good()
            my_msg('Блок исправен', 'green')
        else:
            test_ubtz.result_test_ubtz()
            mysql_conn_ubtz.mysql_block_bad()
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
        reset_test_ubtz.reset_all()
        sys.exit()
