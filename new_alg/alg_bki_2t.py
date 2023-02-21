# -*- coding: utf-8 -*-
"""
!!! НОВЫЙ НЕ ОБКАТАНЫЙ !!!

Алгоритм проверки

Тип блока: БКИ-2Т
Производитель: нет производителя, ТЭТЗ-Инвест, Строй-энерго
Модификации: 52, 53, 54

"""

__all__ = ["TestBKI2T"]

import logging
from time import sleep

from .general_func.database import *
from .general_func.opc_full import ConnectOPC
from .general_func.reset import ResetRelay
from .general_func.resistance import Resistor
from .general_func.utils import CLILog


class TestBKI2T:

    def __init__(self):
        self.conn_opc = ConnectOPC()
        self.resist = Resistor()
        self.mysql_conn = MySQLConnect()
        self.reset_relay = ResetRelay()
        self.cli_log = CLILog("debug", __name__)

        logging.basicConfig(
            filename="C:\\Stend\\project_class\\log\\TestBKI2T.log",
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
        if self.conn_opc.subtest_read_di(test_num=1, subtest_num=1.0,
                                         err_code=[35, 35, 36, 36],
                                         position_inp=[True, False, True, False],
                                         di_xx=['inp_05', 'inp_01', 'inp_06', 'inp_02']):
            return True
        return False

    def st_test_20(self) -> bool:
        """
        Тест 2. Проверка работы блока при подаче питания и при
        нормальном сопротивлении изоляции контролируемого присоединения
        """
        self.logger.debug("старт теста 2.0")
        self.conn_opc.ctrl_relay('KL21', True)
        sleep(5)
        self.logger.debug("таймаут 5 сек")
        self.cli_log.lev_debug("таймаут 5 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=2, subtest_num=2.0,
                                         err_code=[37, 37, 38, 38],
                                         position_inp=[True, False, True, False],
                                         di_xx=['inp_05', 'inp_01', 'inp_06', 'inp_02']):
            return True
        return False

    def st_test_30(self) -> bool:
        """
        Тест 3. Проверка работы 1 канала (К1) блока при снижении
        уровня сопротивлении изоляции ниже 30 кОм в цепи 1 канала
        """
        self.logger.debug("старт теста 3.0")
        self.conn_opc.ctrl_relay('KL31', True)
        self.resist.resist_kohm(12)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=3, subtest_num=3.0,
                                         err_code=[39, 39, 40, 40],
                                         position_inp=[False, True, True, False],
                                         di_xx=['inp_05', 'inp_01', 'inp_06', 'inp_02']):
            self.resist.resist_kohm(590)
            return True
        return False

    def st_test_40(self) -> bool:
        """
        Тест 4. Проверка работы 1 канала (К1) блока от кнопки «Проверка БКИ» в цепи 1 канала
        """
        if self.conn_opc.subtest_read_di(test_num=4, subtest_num=4.0,
                                         err_code=[37, 37, 38, 38],
                                         position_inp=[True, False, True, False],
                                         di_xx=['inp_05', 'inp_01', 'inp_06', 'inp_02']):
            return True
        return False

    def st_test_41(self) -> bool:
        """

        :return:
        """
        self.logger.debug("старт теста 4.1")
        self.conn_opc.ctrl_relay('KL23', True)
        self.conn_opc.ctrl_relay('KL22', True)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=4, subtest_num=4.1,
                                         err_code=[41, 41, 42, 42],
                                         position_inp=[False, True, True, False],
                                         di_xx=['inp_05', 'inp_01', 'inp_06', 'inp_02']):
            self.resist.resist_kohm(590)
            self.conn_opc.ctrl_relay('KL22', False)
            return True
        return False

    def st_test_50(self) -> bool:
        """
        Тест 5. Проверка работы 2 канала (К2) блока при снижении уровня
        сопротивлении изоляции ниже 30 кОм в цепи 2 канала
        """
        self.logger.debug("старт теста 5.0")
        self.conn_opc.ctrl_relay('KL31', False)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        self.resist.resist_kohm(12)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=5, subtest_num=5.0,
                                         err_code=[43, 43, 44, 44],
                                         position_inp=[True, False, False, True],
                                         di_xx=['inp_05', 'inp_01', 'inp_06', 'inp_02']):
            self.resist.resist_kohm(590)
            return True
        return False

    def st_test_60(self) -> bool:
        """
        Тест 6. Проверка работы 2 канала (К2) блока от кнопки «Проверка БКИ» в цепи 2 канала
        """
        if self.conn_opc.subtest_read_di(test_num=6, subtest_num=6.0,
                                         err_code=[37, 37, 38, 38],
                                         position_inp=[True, False, True, False],
                                         di_xx=['inp_05', 'inp_01', 'inp_06', 'inp_02']):
            return True
        return False

    def st_test_61(self) -> bool:
        self.logger.debug("старт теста 6.1")
        self.conn_opc.ctrl_relay('KL22', True)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=6, subtest_num=6.1,
                                         err_code=[45, 45, 46, 46],
                                         position_inp=[True, False, False, True],
                                         di_xx=['inp_05', 'inp_01', 'inp_06', 'inp_02']):
            return True
        return False

    def st_test_bki_2t(self) -> bool:
        if self.st_test_10():
            if self.st_test_20():
                if self.st_test_30():
                    if self.st_test_40():
                        if self.st_test_41():
                            if self.st_test_50():
                                if self.st_test_60():
                                    if self.st_test_61():
                                        return True
        return False
