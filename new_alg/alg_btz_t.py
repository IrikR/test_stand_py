# -*- coding: utf-8 -*-
"""
ПРОВЕРЕН

Алгоритм проверки

Тип блока: БТЗ-Т.
Производитель: Нет производителя, ТЭТЗ-Инвест, Строй-энергомаш, Углеприбор.

"""

__all__ = ["TestBTZT"]

import logging
from time import sleep, time

from .general_func.database import *
from .general_func.opc_full import ConnectOPC
from .general_func.procedure import *
from .general_func.reset import ResetProtection, ResetRelay
from .general_func.subtest import ProcedureFull
from .general_func.utils import CLILog
from .gui.msgbox_1 import *
from .gui.msgbox_2 import *


class TestBTZT:

    def __init__(self):
        self.conn_opc = ConnectOPC()
        self.reset_relay = ResetRelay()
        self.reset_protect = ResetProtection()
        self.proc = Procedure()
        self.proc_full = ProcedureFull()
        self.mysql_conn = MySQLConnect()
        self.cli_log = CLILog("debug", __name__)

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

        self.inp_01: bool = False
        self.inp_02: bool = False
        self.inp_05: bool = False
        self.inp_06: bool = False
        self.inp_09: bool = False

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
        self.cli_log.lev_info(f"старт теста {__doc__}", "skyblue")
        self.conn_opc.simplified_read_di(['inp_14', 'inp_15'])
        if my_msg(self.msg_1):
            pass
        else:
            return False
        self.logger.debug("тест 1")
        self.mysql_conn.mysql_ins_result('идет тест 1', '1')
        self.conn_opc.ctrl_relay('KL21', True)
        self.reset_protect.sbros_zashit_kl30()
        if self.conn_opc.subtest_read_di(test_num=1, subtest_num=1.0,
                                         err_code=[390, 391, 392, 393],
                                         position_inp=[False, True, False, True],
                                         di_xx=['inp_01', 'inp_05', 'inp_02', 'inp_06']):
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
        self.conn_opc.ctrl_relay('KL63', True)
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        self.conn_opc.ctrl_relay('KL63', False)
        if self.conn_opc.subtest_read_di(test_num=2, subtest_num=2.1,
                                         err_code=[395, 396, 397, 398],
                                         position_inp=[False, True, True, False],
                                         di_xx=['inp_01', 'inp_05', 'inp_02', 'inp_06']):
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
        if self.conn_opc.subtest_read_di(test_num=2, subtest_num=2.2,
                                         err_code=[399, 400, 401, 402],
                                         position_inp=[False, True, False, True],
                                         di_xx=['inp_01', 'inp_05', 'inp_02', 'inp_06']):
            if my_msg(self.msg_9):
                return True
        return False

    def st_test_30(self) -> bool:
        """
        Тест 3. Проверка работоспособности защиты ТЗП блока в режиме «Проверка»
        """
        if my_msg(self.msg_3):
            if self.conn_opc.subtest_read_di(test_num=3, subtest_num=3.0,
                                             err_code=[403, 404, 405, 406],
                                             position_inp=[True, False, False, True],
                                             di_xx=['inp_01', 'inp_05', 'inp_02', 'inp_06']):
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
        if self.conn_opc.subtest_read_di(test_num=3, subtest_num=3.1,
                                         err_code=[407, 408, 409, 410],
                                         position_inp=[False, True, False, True],
                                         di_xx=['inp_01', 'inp_05', 'inp_02', 'inp_06']):
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
            self.meas_volt = self.conn_opc.read_ai('AI0')
            self.func_delta_t_pmz(k=k)
            self.reset_relay.stop_procedure_3()
            if self.calc_delta_t_pmz == 9999 or self.malfunction is True:
                self.proc.procedure_1_24_34(coef_volt=self.coef_volt, setpoint_volt=i, factor=1.2)
                self.meas_volt = self.conn_opc.read_ai('AI0')
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
            self.meas_volt = self.conn_opc.read_ai('AI0')
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

    def reset_protection(self, *, test_num: int, subtest_num: float) -> bool:
        self.logger.debug("сброс защит")
        self.reset_protect.sbros_zashit_kl30()
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=test_num, subtest_num=subtest_num,
                                         err_code=[399, 400, 401, 402],
                                         position_inp=[False, True, False, True],
                                         di_xx=['inp_01', 'inp_05', 'inp_02', 'inp_06']):
            return True
        return False

    def func_delta_t_pmz(self, k: int) -> None:
        for qw in range(2):
            if self.reset_protection(test_num=4, subtest_num=4.2):
                # self.inp_01, self.inp_02, self.inp_05, self.inp_06 = self.conn_opc.simplified_read_di('inp_01', 'inp_02',
                #                                                                       'inp_05', 'inp_06')
                self.calc_delta_t_pmz, self.inp_01, self.inp_02, \
                    self.inp_05, self.inp_06 = self.conn_opc.ctrl_ai_code_v0(code=103)
                # sleep(3)
                # self.inp_01, self.inp_02, self.inp_05, self.inp_06 = self.conn_opc.simplified_read_di('inp_01', 'inp_02',
                #                                                                       'inp_05', 'inp_06')
                result_delta_t = f"уставка ПМЗ: {self.list_ust_pmz_num[k]}; попытка: {qw}; " \
                                 f"время: {self.calc_delta_t_pmz}"
                self.logger.info(result_delta_t)
                self.mysql_conn.mysql_add_message(result_delta_t)
                if self.calc_delta_t_pmz == 9999.9:
                    qw += 1
                    self.logger.debug("блок не сработал по времени, повтор проверки блока")
                    self.mysql_conn.mysql_add_message("блок не сработал по времени, повтор проверки блока")
                    self.malfunction = True
                    continue
                elif self.calc_delta_t_pmz != 9999.9 and self.inp_01 is False and self.inp_05 is True and \
                        self.inp_02 is True and self.inp_06 is False:
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

    def func_delta_t_tzp(self) -> None:
        self.conn_opc.ctrl_relay('KL63', True)
        self.inp_09, *_ = self.conn_opc.simplified_read_di(['inp_09'])
        i = 0
        while self.inp_09 is False and i <= 20:
            i += 1
            self.inp_09, *_ = self.conn_opc.simplified_read_di(['inp_09'])
        if self.inp_09 is True:
            start_timer = time()
            meas_time = 0
            self.inp_05, *_ = self.conn_opc.simplified_read_di(['inp_05'])
            while self.inp_05 is True and meas_time <= 370:
                self.inp_05, *_ = self.conn_opc.simplified_read_di(['inp_05'])
                meas_time = time() - start_timer
                self.mysql_conn.progress_level(meas_time)
            stop_timer = time()
            self.calc_delta_t_tzp = stop_timer - start_timer
            self.conn_opc.ctrl_relay('KL63', False)
            self.inp_01, self.inp_02, self.inp_05, self.inp_06 = self.conn_opc.simplified_read_di(
                ['inp_01', 'inp_02', 'inp_05', 'inp_06'])

            if self.inp_01 is True and self.inp_05 is False and self.inp_02 is False and self.inp_06 is True \
                    and self.calc_delta_t_tzp <= 360:
                self.malfunction = False
            else:
                self.malfunction = True
        else:
            self.malfunction = True

    def st_test_btz_t(self) -> [bool, bool, bool]:
        """
            Главная функция которая собирает все остальные
            :type: bool, bool, bool
            :return:  результат теста, флаг исправности ПМЗ, флаг исправности ТЗП
        """
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

    def result_test_btz_t(self) -> None:
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
