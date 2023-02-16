# -*- coding: utf-8 -*-
"""
!!! НОВЫЙ НЕ ОБКАТАНЫЙ !!!

Алгоритм проверки

Тип блока: УБТЗ
Производитель: Нет производителя, Горэкс-Светотехника

"""

__all__ = ["TestUBTZ"]

import logging
import sys
from time import sleep, time

from .general_func.database import *
from .general_func.exception import *
from .general_func.opc_full import ConnectOPC
from .general_func.procedure import *
from .general_func.reset import ResetProtection, ResetRelay
from .general_func.subtest import ProcedureFull
from .general_func.utils import CLILog
from .general_func.rw_result import DIError
from .gui.msgbox_1 import *
from .gui.msgbox_2 import *


class TestUBTZ:

    def __init__(self):
        self.conn_opc = ConnectOPC()
        self.reset_relay = ResetRelay()
        self.reset_protect = ResetProtection()
        self.proc = Procedure()
        self.proc_full = ProcedureFull()
        self.mysql_conn = MySQLConnect()
        self.di_error = DIError()
        self.cli_log = CLILog("debug", __name__)

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
        self.cli_log.lev_info(f"старт теста {__doc__}", "skyblue")
        self.logger.debug("старт теста 1.0")
        if my_msg(self.msg_1):
            if my_msg(self.msg_2):
                pass
            else:
                return False
        else:
            return False
        self.mysql_conn.mysql_ins_result("идёт тест 1.0", '1')
        self.conn_opc.ctrl_relay('KL22', True)
        self.conn_opc.ctrl_relay('KL66', True)
        self.reset_protect.sbros_zashit_ubtz()
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=1, subtest_num=1.0,
                                         err_code=[451, 452, 453, 454],
                                         position_inp=[False, True, False, True],
                                         di_xx=['inp_01', 'inp_05', 'inp_02', 'inp_06']):
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
                self.calc_delta_t_bmz = self.conn_opc.ctrl_ai_code_v0(109)
                self.logger.debug(f'тест 2, дельта t\t{self.calc_delta_t_bmz:.1f}')
                if self.calc_delta_t_bmz == 9999:
                    self.reset_protect.sbros_zashit_ubtz()
                    continue
                else:
                    break

            in_a1, in_a2, in_a5, in_a6 = self.conn_opc.simplified_read_di(['inp_01', 'inp_02', 'inp_05', 'inp_06'])

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
                self.di_error.di_error(current_position=[in_a1, in_a5, in_a2, in_a6],
                                       expected_position=[True, False, False, True],
                                       err_code=[456, 457, 458, 459])
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
            self.conn_opc.ctrl_relay('KL63', True)
            self.mysql_conn.progress_level(0.0)
            in_b1, *_ = self.conn_opc.simplified_read_di(['inp_b1'])
            a = 0
            while in_b1 is False and a < 10:
                a += 1
                in_b1, *_ = self.conn_opc.simplified_read_di(['inp_09'])
            start_timer = time()
            sub_timer = 0
            in_a6, *_ = self.conn_opc.simplified_read_di(['inp_06'])
            while in_a6 is True and sub_timer <= 370:
                sub_timer = time() - start_timer
                self.logger.debug(f'времени прошло: {sub_timer}')
                self.mysql_conn.progress_level(sub_timer)
                sleep(0.2)
                in_a6, *_ = self.conn_opc.simplified_read_di(['inp_06'])
            stop_timer = time()
            in_a1, in_a2, in_a5, in_a6 = self.conn_opc.simplified_read_di(['in_01', 'in_02', 'in_05', 'in_06'])
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
                self.di_error.di_error(current_position=[in_a1, in_a5, in_a2, in_a6],
                                       expected_position=[False, True, False, True],
                                       err_code=[451, 452, 453, 454])
                self.mysql_conn.mysql_ins_result("тест 3 неисправен", '1')
                if self.subtest_33_or_45(test_num=3, subtest_num=3.0):
                    m += 1
                    continue
                else:
                    self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_tzp_num[m]}: '
                                                      f'не срабатывает сброс защит')
                    return False
        self.conn_opc.ctrl_relay('KL22', False)
        self.conn_opc.ctrl_relay('KL66', False)
        self.logger.debug(f"ТЗП дельта t: {self.list_delta_t_tzp}")
        self.mysql_conn.mysql_ins_result("исправен", '1')
        return True

    def subtest_32(self, i: float, k: int) -> bool:
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
            self.calc_delta_t_bmz = self.conn_opc.ctrl_ai_code_v0(109)
            self.logger.debug(f'тест 3 delta t:\t{self.calc_delta_t_bmz:.1f}')
            if self.calc_delta_t_bmz == 9999:
                self.reset_protect.sbros_zashit_ubtz()
                continue
            else:
                break

        self.reset_relay.stop_procedure_3()

        if self.calc_delta_t_bmz < 10:
            self.list_delta_t_bmz[-1] = f'< 10'
        elif self.calc_delta_t_bmz == 9999:
            self.list_delta_t_bmz[-1] = f'неисправен'
        else:
            self.list_delta_t_bmz[-1] = f'{self.calc_delta_t_bmz:.1f}'
        self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_bmz_num[k]}: '
                                          f'дельта t: {self.calc_delta_t_bmz:.1f}')

        if self.conn_opc.subtest_read_di(test_num=3, subtest_num=3.2,
                                         err_code=[464, 465, 466, 467],
                                         position_inp=[True, False, False, True],
                                         di_xx=['inp_01', 'inp_05', 'inp_02', 'inp_06']):
            return True
        return False

        # in_a1, in_a2, in_a5, in_a6 = self.conn_opc.simplified_read_di(['inp_01', 'inp_02', 'inp_05', 'inp_06'])
        # self.logger.debug(f'{in_a1 = }, {in_a2 = }, {in_a5 = }, {in_a6 = }')
        # if in_a1 is True and in_a5 is False and in_a2 is False and in_a6 is True:
        #     pass
        # else:
        #     self.logger.debug("тест 3.2 положение выходов не соответствует")
        #     if in_a1 is True:
        #         self.mysql_conn.mysql_error(464)
        #     elif in_a5 is True:
        #         self.mysql_conn.mysql_error(465)
        #     elif in_a2 is True:
        #         self.mysql_conn.mysql_error(466)
        #     elif in_a6 is True:
        #         self.mysql_conn.mysql_error(467)
        #     return False
        # self.logger.debug("тест 3.2 положение выходов соответствует")
        # return True

    def subtest_33_or_45(self, test_num: int, subtest_num: float) -> bool:
        """
        3.3. Сброс защит после проверки
        :return:
        """
        self.reset_protect.sbros_zashit_ubtz()
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=test_num, subtest_num=subtest_num,
                                         err_code=[460, 461, 462, 463],
                                         position_inp=[False, True, False, True],
                                         di_xx=['inp_01', 'inp_05', 'inp_02', 'inp_06']):
            return True
        self.mysql_conn.mysql_add_message(f'тест {test_num}: не срабатывает сброс защит')
        return False

    def st_test_ubtz(self) -> [bool]:
        if self.st_test_10():
            if self.st_test_11():
                if self.st_test_20():
                    if self.st_test_30():
                        return True, self.health_flag
        return False, self.health_flag

    def result_test_ubtz(self) -> None:
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

    def full_test_ubtz(self) -> None:
        try:
            start_time = time()
            test, health_flag = self.st_test_ubtz()
            end_time = time()
            time_spent = end_time - start_time
            self.cli_log.lev_info(f"Время выполнения: {time_spent}", "gray")
            self.logger.debug(f"Время выполнения: {time_spent}")
            self.mysql_conn.mysql_add_message(f"Время выполнения: {time_spent}")

            if test and not health_flag:
                self.result_test_ubtz()
                self.mysql_conn.mysql_block_good()
                self.logger.debug('Блок исправен')
                self.cli_log.lev_info('Блок исправен', 'green')
                my_msg('Блок исправен', 'green')
            else:
                self.result_test_ubtz()
                self.mysql_conn.mysql_block_bad()
                self.logger.debug('Блок неисправен')
                self.cli_log.lev_warning('Блок неисправен', 'red')
                my_msg('Блок неисправен', 'red')
        except OSError:
            self.logger.debug("ошибка системы")
            self.cli_log.lev_warning("ошибка системы", 'red')
            my_msg("ошибка системы", 'red')
        except SystemError:
            self.logger.debug("внутренняя ошибка")
            self.cli_log.lev_warning("внутренняя ошибка", 'red')
            my_msg("внутренняя ошибка", 'red')
        except ModbusConnectException as mce:
            self.logger.debug(f'{mce}')
            self.cli_log.lev_warning(f'{mce}', 'red')
            my_msg(f'{mce}', 'red')
        except HardwareException as hwe:
            self.logger.debug(f'{hwe}')
            self.cli_log.lev_warning(f'{hwe}', 'red')
            my_msg(f'{hwe}', 'red')
        except AttributeError as ae:
            self.logger.debug(f"Неверный атрибут. {ae}")
            self.cli_log.lev_warning(f"Неверный атрибут. {ae}", 'red')
            my_msg(f"Неверный атрибут. {ae}", 'red')
        except ValueError as ve:
            self.logger.debug(f"Некорректное значение для переменной. {ve}")
            self.cli_log.lev_warning(f"Некорректное значение для переменной. {ve}", 'red')
            my_msg(f"Некорректное значение для переменной. {ve}", 'red')
        finally:
            self.conn_opc.full_relay_off()
            self.conn_opc.opc_close()
            sys.exit()
