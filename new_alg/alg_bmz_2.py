# -*- coding: utf-8 -*-
"""
!!! НОВЫЙ НЕ ОБКАТАНЫЙ !!!

Алгоритм проверки

Тип блока: БМЗ-2
Производитель: Нет производителя, ТЭТЗ-Инвест, Строй-энергомаш

"""

__all__ = ['TestBMZ2']

import logging
import sys
from time import sleep

from .general_func.database import *
from .general_func.exception import *
from .general_func.opc_full import ConnectOPC
from .general_func.procedure import *
from .general_func.reset import ResetProtection, ResetRelay
from .general_func.subtest import ProcedureFull
from .general_func.utils import CLILog
from .gui.msgbox_1 import *
from .gui.msgbox_2 import *


class TestBMZ2:

    def __init__(self):
        self.conn_opc = ConnectOPC()
        self.reset_relay = ResetRelay()
        self.reset_protect = ResetProtection()
        self.proc = Procedure()
        self.proc_full = ProcedureFull()
        self.mysql_conn = MySQLConnect()
        self.cli_log = CLILog("debug", __name__)

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

        logging.basicConfig(
            filename="C:\\Stend\\project_class\\log\\TestBMZ2.log",
            filemode="w",
            level=logging.DEBUG,
            encoding="utf-8",
            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('WARNING')
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))

    def st_test_10_bmz_2(self) -> bool:
        """
        Тест 1. Проверка исходного состояния блока:
        """
        self.cli_log.lev_info(f"старт теста {__doc__}", "skyblue")
        self.conn_opc.simplified_read_di(['inp_14', 'inp_15'])
        if my_msg(self.msg_1):
            pass
        else:
            return False
        self.mysql_conn.mysql_ins_result('идет тест 1', '1')
        self.conn_opc.ctrl_relay('KL21', True)
        self.logger.debug("KL21 включен")
        if self.reset_protection(test_num=1, subtest_num=1.0):
            return True
        return False

    def st_test_11_bmz_2(self) -> bool:
        """
        1.1.2. Проверка отсутствия короткого замыкания на входе измерительной части блока:
        1.2. Определение коэффициента Кс отклонения фактического напряжения от номинального
        """
        if self.proc_full.procedure_1_full(test_num=1, subtest_num=1.1):
            self.coef_volt = self.proc_full.procedure_2_full(test_num=1, subtest_num=1.2)
            return True
        return False

    def st_test_20_bmz_2(self) -> bool:
        """
        Тест 2. Проверка работоспособности защиты блока в режиме «Проверка»
        """
        if my_msg(self.msg_2):
            pass
        else:
            return False
        self.mysql_conn.mysql_ins_result('идет тест 2', '2')
        self.logger.debug("начало теста 2, сброс всех реле")
        if self.proc.procedure_x4_to_x5(coef_volt=self.coef_volt, setpoint_volt=self.ust_test):
            return True
        self.mysql_conn.mysql_ins_result('неисправен', '2')
        return False

    def st_test_21_bmz_2(self) -> bool:
        self.conn_opc.ctrl_relay('KL63', True)
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        self.conn_opc.ctrl_relay('KL63', False)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=2, subtest_num=2.1,
                                         err_code=[335, 336, 337],
                                         position_inp=[True, False, True],
                                         di_xx=['inp_01', 'inp_05', 'inp_02']):
            self.reset_relay.stop_procedure_3()
            return True
        return False

    def st_test_22_bmz_2(self) -> bool:
        """
        2.4.2. Сброс защит после проверки
        """
        self.mysql_conn.mysql_ins_result('идет тест 2.4', '2')
        if self.reset_protection(test_num=2, subtest_num=2.2):
            return True
        return False

    def st_test_30_bmz_2(self) -> bool:
        """
        Тест 3. Проверка срабатывания защиты блока по уставкам
        """
        if my_msg(self.msg_3):
            pass
        else:
            return False
        self.mysql_conn.mysql_ins_result('идет тест 3', '3')
        # Цикл i=1…11 (Таблица уставок 1)
        k = 0
        for i in self.list_ust_volt:
            msg_result = my_msg_2(f'{self.msg_4} {self.list_ust_num[k]}')
            if msg_result == 0:
                pass
            elif msg_result == 1:
                return False
            elif msg_result == 2:
                self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[k]} пропущена')
                self.list_delta_percent.append('пропущена')
                self.list_delta_t.append('пропущена')
                k += 1
                continue
            self.mysql_conn.mysql_ins_result('идет тест 3.1', '3')
            if self.proc.procedure_x4_to_x5(coef_volt=self.coef_volt, setpoint_volt=i):
                pass
            else:
                self.mysql_conn.mysql_ins_result('неисправен', '3')
                return False
            # qw = 0
            for qw in range(4):
                self.calc_delta_t = self.conn_opc.ctrl_ai_code_v0(code=104)
                self.logger.info(f'дельта t \t {self.calc_delta_t:.1f}')
                if self.calc_delta_t == 9999:
                    self.reset_protect.sbros_zashit_kl30()
                    sleep(3)
                    qw += 1
                    continue
                else:
                    break
            self.logger.debug(f'дельта t \t {self.calc_delta_t:.1f}')
            if self.calc_delta_t < 10:
                self.list_delta_t.append(f'< 10')
            elif self.calc_delta_t == 9999:
                self.list_delta_t.append(f'неисправен')
            else:
                self.list_delta_t.append(f'{self.calc_delta_t:.1f}')
            # Δ%= 6,1085*U4
            meas_volt = self.conn_opc.read_ai('AI0')
            calc_delta_percent = meas_volt * 6.1085
            self.logger.debug(f'дельта % \t {calc_delta_percent:.2f}')
            self.list_delta_percent.append(f'{calc_delta_percent:.2f}')
            self.reset_relay.stop_procedure_3()
            self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[k]} дельта t: {self.calc_delta_t:.1f}')
            self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[k]} дельта %: {calc_delta_percent:.2f}')
            inp_01, inp_02, inp_05 = self.conn_opc.simplified_read_di(['inp_01', 'inp_02', 'inp_05'])
            if inp_01 is True and inp_05 is False and inp_02 is True:
                self.logger.debug("соответствие выходов блока, сбрасываем и переходим к тесту 3.5")
                if self.reset_protection(test_num=3, subtest_num=3.5):
                    k += 1
                    continue
                else:
                    self.mysql_conn.mysql_ins_result('неисправен', '3')
                    k += 1
                    continue
            else:
                self.logger.debug("не соответствие выходов блока, переходим к тесту 3.2")
                self.mysql_conn.mysql_ins_result('неисправен', '3')
                self.mysql_conn.mysql_error(341)
                if self.subtest_32(i, k):
                    if self.reset_protection(test_num=3, subtest_num=3.5):
                        k += 1
                        continue
                    else:
                        self.mysql_conn.mysql_ins_result('неисправен', '3')
                        k += 1
                        continue
                else:
                    if self.reset_protection(test_num=3, subtest_num=3.5):
                        k += 1
                        continue
                    else:
                        self.mysql_conn.mysql_ins_result('неисправен', '3')
                        k += 1
                        continue
        self.mysql_conn.mysql_ins_result('исправен', '3')
        return True

    def subtest_32(self, i: float, k: int) -> bool:
        """
        3.2. Формирование нагрузочного сигнала 1,1*calc_volt[i]:
        3.2.1. Сброс защит после проверки
        """
        self.mysql_conn.mysql_ins_result('идет тест 3.2', '3')
        self.logger.debug("старт теста 3.2")
        if self.reset_protection(test_num=3, subtest_num=3.2):
            pass
        else:
            return False
        self.mysql_conn.mysql_ins_result('идет тест 3.3', '3')
        if self.proc.procedure_1_24_34(coef_volt=self.coef_volt, setpoint_volt=i, factor=1.1):
            pass
        else:
            return False
        # Δ%= 6,1085*U4
        meas_volt = self.conn_opc.read_ai('AI0')
        calc_delta_percent = meas_volt * 6.1085
        self.logger.debug(f'дельта % \t {calc_delta_percent:.2f}')
        self.list_delta_percent[-1] = f'{calc_delta_percent:.2f}'
        self.mysql_conn.mysql_ins_result('идет тест 3.4', '3')
        # wq = 0
        for wq in range(4):
            self.calc_delta_t = self.conn_opc.ctrl_ai_code_v0(code=104)
            self.logger.info(f'дельта t \t {self.calc_delta_t:.1f}')
            if self.calc_delta_t == 9999:
                self.reset_protect.sbros_zashit_kl30()
                sleep(3)
                wq += 1
                continue
            else:
                break
        self.logger.debug(f'дельта t \t {self.calc_delta_t:.1f}')
        if self.calc_delta_t < 10:
            self.list_delta_t[-1] = f'< 10'
        elif self.calc_delta_t == 9999:
            self.list_delta_t[-1] = f'неисправен'
        else:
            self.list_delta_t[-1] = f'{self.calc_delta_t:.1f}'
        self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[k]} дельта t: {self.calc_delta_t:.1f}')
        self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[k]} дельта %: {calc_delta_percent:.2f}')
        inp_01, inp_02, inp_05 = self.conn_opc.simplified_read_di(['inp_01', 'inp_02', 'inp_05'])
        if inp_01 is True and inp_05 is False and inp_02 is True:
            pass
        else:
            self.logger.debug("выходы блока не соответствуют")
            self.mysql_conn.mysql_ins_result('неисправен', '3')
            self.mysql_conn.mysql_error(341)
            return False
        self.logger.debug("выходы блока соответствуют")
        self.reset_relay.stop_procedure_3()
        self.logger.debug("сброс реле и старт теста 3.5")
        return True

    def reset_protection(self, *, test_num: int = 3, subtest_num: float = 3.5):
        """
        Сброс защиты блока.
        :param test_num: Номер теста.
        :param subtest_num: номер подтеста.
        :return:
        """
        self.mysql_conn.mysql_ins_result(f'идёт тест {subtest_num}', f'{test_num}')
        self.logger.debug(f"старт теста {subtest_num}")
        self.reset_protect.sbros_zashit_kl30()
        if self.conn_opc.subtest_read_di(test_num=test_num, subtest_num=subtest_num,
                                         err_code=[338, 339, 340],
                                         position_inp=[False, True, False],
                                         di_xx=['inp_01', 'inp_05', 'inp_02']):
            return True
        return False

    def st_test_bmz_2(self) -> [bool, bool]:
        if self.st_test_10_bmz_2():
            if self.st_test_11_bmz_2():
                if self.st_test_20_bmz_2():
                    if self.st_test_21_bmz_2():
                        if self.st_test_22_bmz_2():
                            if self.st_test_30_bmz_2():
                                return True, self.health_flag
        return False, self.health_flag

    def result_test_bmz_2(self) -> None:
        for g1 in range(len(self.list_delta_percent)):
            self.list_result.append((self.list_ust_num[g1], self.list_delta_percent[g1], self.list_delta_t[g1]))
        self.mysql_conn.mysql_tzp_result(self.list_result)

    def full_test_bmz_2(self) -> None:
        try:
            test, health_flag = self.st_test_bmz_2()
            if test and not health_flag:
                self.result_test_bmz_2()
                self.mysql_conn.mysql_block_good()
                self.logger.debug('Блок исправен')
                self.cli_log.lev_info('Блок исправен', 'green')
                my_msg('Блок исправен', 'green')
            else:
                self.result_test_bmz_2()
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
        finally:
            self.conn_opc.full_relay_off()
            self.conn_opc.opc_close()
            sys.exit()
