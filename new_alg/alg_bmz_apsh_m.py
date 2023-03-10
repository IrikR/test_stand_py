# -*- coding: utf-8 -*-
"""
!!! НОВЫЙ НЕ ОБКАТАНЫЙ !!!

Алгоритм проверки

Тип блока: БМЗ АПШ.М
Производитель: Нет производителя, Электроаппарат-Развитие

"""

__all__ = ["TestBMZAPSHM"]

import logging
from time import sleep

from .general_func.database import *
from .general_func.opc_full import ConnectOPC
from .general_func.procedure import *
from .general_func.reset import ResetProtection, ResetRelay
from .general_func.subtest import ProcedureFull
from .general_func.utils import CLILog
from .gui.msgbox_1 import *


class TestBMZAPSHM:

    def __init__(self):
        self.conn_opc = ConnectOPC()
        self.proc = Procedure()
        self.proc_full = ProcedureFull()
        self.reset_relay = ResetRelay()
        self.reset_protect = ResetProtection()
        self.mysql_conn = MySQLConnect()
        self.cli_log = CLILog("debug", __name__)

        self.ust_1: float = 85.6

        self.coef_volt: float = 0.0
        self.health_flag: bool = False

        self.msg_1: str = "Убедитесь в отсутствии блоков во всех испытательных разъемах. " \
                          "Вставьте блок в соответствующий испытательный разъем»"

        logging.basicConfig(
            filename="C:\\Stend\\project_class\\log\\TestBMZAPShM.log",
            filemode="w",
            level=logging.DEBUG,
            encoding="utf-8",
            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('DEBUG')
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))

    def st_test_10(self) -> bool:
        """
        Тест 1. Проверка исходного состояния блока:
        """
        self.cli_log.lev_info(f"старт теста {__doc__}", "skyblue")

        if not my_msg(self.msg_1):
            return False

        self.logger.debug("тест 1.0")
        self.cli_log.lev_info("тест 1", "skyblue")
        self.conn_opc.ctrl_relay('KL21', True)
        self.reset_protect.sbros_zashit_kl30()
        if self.conn_opc.subtest_read_di(test_num=1, subtest_num=1.0,
                                         err_code=[347, 348, 349, 350],
                                         position_inp=[False, True, False, True],
                                         di_xx=['inp_01', 'inp_05', 'inp_02', 'inp_06']):
            return True
        return False

    def st_test_11(self) -> bool:
        """
        1.1.2. Проверка отсутствия короткого замыкания на входе измерительной части блока:
        1.2. Определение коэффициента Кс отклонения фактического напряжения от номинального
        """
        self.cli_log.lev_info("тест 1.1", "skyblue")
        if self.proc_full.procedure_1_full(test_num=1, subtest_num=1.1, coef_min_volt=0.9):
            self.coef_volt = self.proc_full.procedure_2_full(test_num=1, subtest_num=1.2)
            return True
        return False

    def st_test_20(self) -> bool:
        """
        Тест 2. Проверка работы 1 канала блока
        """
        self.logger.debug("старт теста 2.0")
        self.cli_log.lev_info("тест 2.0", "skyblue")
        if self.proc.procedure_x4_to_x5(coef_volt=self.coef_volt, setpoint_volt=self.ust_1):
            return True
        self.mysql_conn.mysql_ins_result('неисправен', '2')
        return False

    def st_test_21(self) -> bool:
        """
        2.1.  Проверка срабатывания блока от сигнала нагрузки:
        """
        self.cli_log.lev_info("тест 2.1", "skyblue")
        self.logger.debug("старт теста 2.1")
        self.conn_opc.ctrl_relay('KL63', True)
        sleep(3)
        self.logger.debug("таймаут 3 сек")
        self.cli_log.lev_debug("таймаут 3 сек", "gray")
        self.conn_opc.ctrl_relay('KL63', False)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=2, subtest_num=2.1,
                                         err_code=[352, 353, 354, 355],
                                         position_inp=[True, False, False, True],
                                         di_xx=['inp_01', 'inp_05', 'inp_02', 'inp_06']):
            self.reset_relay.stop_procedure_3()
            return True
        self.reset_relay.stop_procedure_3()
        return False

    def st_test_22(self) -> bool:
        """
        2.2. Сброс защит после проверки
        """
        self.logger.debug("старт теста 2.2")
        self.cli_log.lev_info("тест 2.2", "skyblue")
        self.reset_protect.sbros_zashit_kl30()
        if self.conn_opc.subtest_read_di(test_num=2, subtest_num=2.2,
                                         err_code=[356, 357, 358, 359],
                                         position_inp=[False, True, False, True],
                                         di_xx=['inp_01', 'inp_05', 'inp_02', 'inp_06']):
            return True
        return False

    def st_test_30(self) -> bool:
        """
        Тест 3. Проверка работы 2 канала блока
        """
        self.logger.debug("старт теста 3.0")
        self.cli_log.lev_info("тест 3.0", "skyblue")
        self.conn_opc.ctrl_relay('KL73', True)
        if self.proc.procedure_x4_to_x5(coef_volt=self.coef_volt, setpoint_volt=self.ust_1):
            return True
        self.mysql_conn.mysql_ins_result('неисправен', '3')
        return False

    def st_test_31(self) -> bool:
        self.cli_log.lev_info("тест 3.1", "skyblue")
        self.conn_opc.ctrl_relay('KL63', True)
        sleep(3)
        self.logger.debug("таймаут 3 сек")
        self.cli_log.lev_debug("таймаут 3 сек", "gray")
        self.conn_opc.ctrl_relay('KL63', False)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=3, subtest_num=3.1,
                                         err_code=[360, 361, 362, 363],
                                         position_inp=[False, True, True, False],
                                         di_xx=['inp_01', 'inp_05', 'inp_02', 'inp_06']):
            self.reset_relay.stop_procedure_3()
            return True
        self.reset_relay.stop_procedure_3()
        return False

    def st_test_32(self) -> bool:
        """
        3.2. Сброс защит после проверки
        """
        self.logger.debug("старт теста 3.2")
        self.cli_log.lev_info("тест 3.2", "skyblue")
        self.reset_protect.sbros_zashit_kl30()
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=3, subtest_num=3.2,
                                         err_code=[364, 365, 366, 367],
                                         position_inp=[False, True, False, True],
                                         di_xx=['inp_01', 'inp_05', 'inp_02', 'inp_06']):
            return True
        return False

    def st_test_bmz_apsh_m(self) -> [bool, bool]:
        """
            Главная функция которая собирает все остальные
            :type: bool, bool
            :return: результат теста, флаг исправности
        """
        if self.st_test_10():
            if self.st_test_11():
                if self.st_test_20():
                    if self.st_test_21():
                        if self.st_test_22():
                            if self.st_test_30():
                                if self.st_test_31():
                                    if self.st_test_32():
                                        return True, self.health_flag
        return False, self.health_flag
