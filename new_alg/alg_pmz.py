# -*- coding: utf-8 -*-
"""
!!! НОВЫЙ НЕ ОБКАТАНЫЙ !!!

Алгоритм проверки

Тип блока: ПМЗ
Производитель: Нет производителя, Углеприбор
Тип блока: ПМЗ-П
Производитель: Нет производителя, Пульсар

"""

__all__ = ["TestPMZ"]

import logging
from time import sleep

from .general_func.database import *
from .general_func.opc_full import ConnectOPC
from .general_func.procedure import *
from .general_func.reset import ResetProtection, ResetRelay
from .general_func.subtest import ProcedureFull
from .general_func.utils import CLILog
from .gui.msgbox_1 import *
from .gui.msgbox_2 import *


class TestPMZ:

    def __init__(self):
        self.conn_opc = ConnectOPC()
        self.proc = Procedure()
        self.proc_full = ProcedureFull()
        self.reset_relay = ResetRelay()
        self.reset_protect = ResetProtection()
        self.mysql_conn = MySQLConnect()
        self.cli_log = CLILog("debug", __name__)

        self.ust_1: float = 80.0
        self.list_ust_num: tuple[int, ...] = (1, 2, 3, 4, 5, 6, 7, 8, 9)
        self.list_ust_volt: tuple[float, ...] = (75.4, 92, 114, 125, 141, 156.4, 172, 182.4, 196)
        self.list_delta_t: list[str] = []
        self.list_delta_percent: list[str] = []
        self.list_result: list[[str]] = []

        self.meas_volt_ust: float = 0.0
        self.coef_volt: float = 0.0
        self.calc_delta_t: float = 0.0
        self.health_flag: bool = False

        self.inp_01: bool = False
        self.inp_02: bool = False
        self.inp_05: bool = False
        self.inp_06: bool = False

        self.msg_1: str = "Убедитесь в отсутствии в панелях разъемов установленных блоков Подключите " \
                          "блок ПМЗ в разъем Х14 на панели B"
        self.msg_2: str = "Переключите тумблер режимов, расположенный на корпусе блока, в положение «Работа»"
        self.msg_3: str = 'Установите регулятор уставок на блоке в положение'
        self.msg_4: str = "Переключите тумблер на корпусе блока в положение «Проверка»"

        logging.basicConfig(
            filename="C:\\Stend\\project_class\\log\\TestPMZ.log",
            filemode="w",
            level=logging.DEBUG,
            encoding="utf-8",
            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('WARNING')
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))

    def st_test_10(self) -> bool:
        self.cli_log.lev_info(f"старт теста {__doc__}", "skyblue")
        if my_msg(self.msg_1):
            if my_msg(self.msg_2):
                return True
        return False

    def st_test_11(self) -> bool:
        """
        Тест 1. Проверка исходного состояния блока:
        :return:
        """
        self.conn_opc.ctrl_relay('KL21', True)
        self.reset_protect.sbros_zashit_kl30(time_on=1.5, time_off=2.0)
        self.logger.debug("сброс защит")
        inp_01, inp_02, inp_05 = self.conn_opc.simplified_read_di(['inp_01', 'inp_02', 'inp_05'])
        if inp_01 is False and inp_02 is False and inp_05 is True:
            pass
        else:
            self.mysql_conn.mysql_ins_result('неисправен', '1')
            self.logger.debug("положение выходов блока не соответствует")
            return False
        self.logger.debug("положение выходов блока соответствует")
        self.mysql_conn.mysql_ins_result('исправен', '1')
        return True

    def st_test_20(self) -> bool:
        """
        Тест 2. Проверка работоспособности блока в режиме «Проверка»
        Процедура 2.1. Проверка вероятности наличия короткого замыкания на входе измерительной цепи блока
        2.1.1. Проверка отсутствия вероятности возникновения межвиткового замыкания на стороне первичной обмотки TV1
        :return:
        """
        self.mysql_conn.mysql_ins_result('идет тест 2.1', '2')
        self.meas_volt_ust = self.proc.procedure_1_21_31()
        if self.meas_volt_ust != 0.0:
            return True
        self.mysql_conn.mysql_ins_result("неисправен", "1")
        return False

    def st_test_21(self) -> bool:
        """
        1.1.2. Проверка отсутствия короткого замыкания на входе измерительной части блока:
        1.2. Определение коэффициента Кс отклонения фактического напряжения от номинального.
        :return:
        """
        if self.proc_full.procedure_1_full(test_num=2, subtest_num=2.1, coef_min_volt=0.4):
            self.coef_volt = self.proc_full.procedure_2_full(test_num=2, subtest_num=2.2)
            return True
        return False

    def st_test_23(self) -> bool:
        """
        Процедура 2.3. Формирование нагрузочного сигнала U3:
        :return:
        """
        if my_msg(self.msg_4):
            pass
        else:
            return False
        self.logger.debug("тест 2.3")
        if self.proc.procedure_x4_to_x5(coef_volt=self.coef_volt, setpoint_volt=self.ust_1):
            return True
        self.mysql_conn.mysql_ins_result('неисправен', '2')
        return False

    def st_test_24(self) -> bool:
        """
        2.4.  Проверка срабатывания блока от сигнала нагрузки:
        :return:
        """
        self.conn_opc.ctrl_ai_code_v1(108)
        inp_01, inp_02, inp_05 = self.conn_opc.simplified_read_di(['inp_01', 'inp_02', 'inp_05'])
        if inp_01 is True and inp_02 is True and inp_05 is False:
            pass
        else:
            self.logger.debug("положение выходов блока не соответствует")
            self.reset_relay.stop_procedure_3()
            self.mysql_conn.mysql_ins_result('неисправен', '2')
            return False
        self.logger.debug("положение выходов блока соответствует")
        self.reset_relay.stop_procedure_3()
        return True

    def st_test_25(self) -> bool:
        """
        2.4.2. Сброс защит после проверки
        :return:
        """
        self.reset_protect.sbros_zashit_kl30(time_on=1.5, time_off=2.0)
        self.logger.debug("сброс защит")
        inp_01, inp_02, inp_05 = self.conn_opc.simplified_read_di(['inp_01', 'inp_02', 'inp_05'])
        if inp_01 is False and inp_02 is False and inp_05 is True:
            pass
        else:
            self.logger.debug("положение выходов блока не соответствует")
            self.mysql_conn.mysql_ins_result('неисправен', '2')
            return False
        self.logger.debug("положение выходов блока соответствует")
        self.mysql_conn.mysql_ins_result('исправен', '2')
        return True

    def st_test_30(self) -> bool:
        """
        Тест 3. Проверка срабатывания блока по уставкам.
        :return:
        """
        if my_msg(self.msg_2):
            pass
        else:
            return False
        k = 0
        for i in self.list_ust_volt:
            msg_result = my_msg_2(f'{self.msg_3} {self.list_ust_num[k]}')
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
            if self.proc.procedure_x4_to_x5(coef_volt=self.coef_volt, setpoint_volt=i):
                pass
            else:
                return False
            # Δ%= 0.0038*U42[i]+2.27* U4[i]
            meas_volt = self.conn_opc.read_ai('AI0')
            calc_delta_percent = 0.0038 * meas_volt ** 2 + 2.27 * meas_volt
            self.list_delta_percent.append(f'{calc_delta_percent:.2f}')
            # 3.4.  Проверка срабатывания блока от сигнала нагрузки:
            for qw in range(4):
                self.calc_delta_t, self.inp_01, self.inp_02, \
                    self.inp_05, self.inp_06 = self.conn_opc.ctrl_ai_code_v0(104)
                self.logger.debug(f'время срабатывания, {self.calc_delta_t:.1f} мс')
                self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[k]} '
                                                  f'дельта t: {self.calc_delta_t:.1f}')
                if self.calc_delta_t == 9999.9:
                    sleep(3)
                    # qw += 1
                    self.reset_protect.sbros_zashit_kl30(time_on=1.5, time_off=2.0)
                    continue
                # elif 100 < self.calc_delta_t < 9999:
                #     sleep(3)
                #     # qw += 1
                #     self.reset.sbros_zashit_kl30_1s5()
                #     continue
                else:
                    break
            self.logger.debug(f'время срабатывания: {self.calc_delta_t:.1f} мс')
            if self.calc_delta_t < 10.0:
                self.list_delta_t.append(f'< 10')
            elif self.calc_delta_t == 9999.9:
                self.list_delta_t.append(f'неисправен')
            else:
                self.list_delta_t.append(f'{self.calc_delta_t:.1f}')
            self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[k]} дельта t: {self.calc_delta_t:.1f}')
            self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[k]} дельта %: {calc_delta_percent:.2f}')
            self.reset_relay.stop_procedure_3()
            inp_01, inp_02, inp_05 = self.conn_opc.simplified_read_di(['inp_01', 'inp_02', 'inp_05'])
            if inp_01 is True and inp_02 is True and inp_05 is False:
                self.logger.debug("положение выходов блока соответствует")
                if self.subtest_36():
                    k += 1
                    continue
                return False
            else:
                self.logger.debug("положение выходов блока не соответствует")
                if self.subtest_35(i=i, k=k):
                    if self.subtest_36():
                        k += 1
                        continue
                self.mysql_conn.mysql_ins_result('неисправен', '3')
                return False
        self.mysql_conn.mysql_ins_result('исправен', '3')
        return True

    def subtest_35(self, i: float, k: int) -> bool:
        """
        3.5. Формирование нагрузочного сигнала 1,1*U3[i]:
        :param i:
        :param k:
        :return:
        """
        self.reset_protect.sbros_zashit_kl30(time_on=1.5, time_off=2.0)
        self.logger.debug("сброс защит")
        inp_01, inp_02, inp_05 = self.conn_opc.simplified_read_di(['inp_01', 'inp_02', 'inp_05'])
        if inp_01 is False and inp_02 is False and inp_05 is True:
            pass
        else:
            self.logger.debug("положение выходов блока не соответствует")
            self.mysql_conn.mysql_ins_result('неисправен', '3')
            return False
        self.logger.debug("положение выходов блока соответствует")
        if self.proc.procedure_1_24_34(coef_volt=self.coef_volt, setpoint_volt=i, factor=1.1):
            pass
        else:
            return False
        # Δ%= 0.0038*U42[i]+2.27* U4[i]
        meas_volt = self.conn_opc.read_ai('AI0')
        calc_delta_percent = 0.0038 * meas_volt ** 2 + 2.27 * meas_volt
        self.list_delta_percent[-1] = f'{calc_delta_percent:.2f}'
        for wq in range(4):
            self.calc_delta_t, self.inp_01, self.inp_02, \
                self.inp_05, self.inp_06 = self.conn_opc.ctrl_ai_code_v0(104)
            self.logger.debug(f'время срабатывания, {self.calc_delta_t:.1f} мс')
            self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[k]} '
                                              f'дельта t: {self.calc_delta_t:.1f}')
            if self.calc_delta_t == 9999.9:
                sleep(3)
                wq += 1
                self.reset_protect.sbros_zashit_kl30(time_on=1.5, time_off=2.0)
                continue
            elif 100 < self.calc_delta_t < 9999.9:
                sleep(3)
                wq += 1
                self.reset_protect.sbros_zashit_kl30(time_on=1.5, time_off=2.0)
                continue
            else:
                break
        self.logger.debug(f'время срабатывания, {self.calc_delta_t:.1f} мс')
        if self.calc_delta_t < 10.0:
            self.list_delta_t[-1] = f'< 10'
        elif self.calc_delta_t > 100.0:
            self.list_delta_t.append(f'> 100')
        else:
            self.list_delta_t[-1] = f'{self.calc_delta_t:.1f}'
        self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[k]} дельта t: {self.calc_delta_t:.1f}')
        self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[k]} дельта %: {calc_delta_percent:.2f}')
        inp_01, inp_02, inp_05 = self.conn_opc.simplified_read_di(['inp_01', 'inp_02', 'inp_05'])
        if inp_01 is True and inp_02 is True and inp_05 is False:
            pass
        else:
            self.logger.debug("положение выходов блока не соответствует")
            self.reset_relay.stop_procedure_3()
            self.mysql_conn.mysql_ins_result('неисправен', '3')
            return False
        self.logger.debug("положение выходов блока соответствует")
        self.reset_relay.stop_procedure_3()
        return True

    def subtest_36(self) -> bool:
        """
        3.6. Сброс защит после проверки
        :return:
        """
        self.reset_protect.sbros_zashit_kl30(time_on=1.5, time_off=2.0)
        self.logger.debug("сброс защит")
        inp_01, inp_02, inp_05 = self.conn_opc.simplified_read_di(['inp_01', 'inp_02', 'inp_05'])
        if inp_01 is False and inp_02 is False and inp_05 is True:
            pass
        else:
            self.logger.debug("положение выходов блока не соответствует")
            self.mysql_conn.mysql_ins_result('неисправен', '3')
            return False
        self.logger.debug("положение выходов блока соответствует")
        return True

    def st_test_pmz(self) -> [bool, bool]:
        """
            Главная функция которая собирает все остальные
            :type: bool, bool
            :return:  результат теста, флаг исправности
        """
        if self.st_test_10():
            if self.st_test_11():
                if self.st_test_20():
                    if self.st_test_21():
                        if self.st_test_23():
                            if self.st_test_24():
                                if self.st_test_25():
                                    if self.st_test_30():
                                        return True, self.health_flag
        return False, self.health_flag

    def result_test_pmz(self) -> None:
        for g1 in range(len(self.list_delta_percent)):
            self.list_result.append((self.list_ust_num[g1], self.list_delta_percent[g1], self.list_delta_t[g1]))
        self.mysql_conn.mysql_pmz_result(self.list_result)
