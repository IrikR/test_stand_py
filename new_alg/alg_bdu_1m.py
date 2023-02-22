# -*- coding: utf-8 -*-
"""
!!! НОВЫЙ НЕ ОБКАТАНЫЙ !!!

Алгоритм проверки

Тип блока: БДУ-1М
Производитель: Пульсар, Нет производителя

"""

__all__ = ["TestBDU1M"]

import logging
from time import sleep

from .general_func.database import *
from .general_func.opc_full import ConnectOPC
from .general_func.reset import ResetRelay
from .general_func.resistance import Resistor
from .general_func.subtest import SubtestBDU1M
from .general_func.utils import CLILog


class TestBDU1M:

    def __init__(self):
        self.conn_opc = ConnectOPC()
        self.resist = Resistor()
        self.mysql_conn = MySQLConnect()
        self.subtest = SubtestBDU1M()
        self.reset_relay = ResetRelay()
        self.cli_log = CLILog("debug", __name__)
        # C:\Stend\project_class
        logging.basicConfig(
            filename="C:\\Stend\\project_class\\log\\TestBDU1M.log",
            filemode="w",
            level=logging.DEBUG,
            encoding="utf-8",
            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('DEBUG')
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))

    def st_test_1(self) -> bool:
        """
            Тест 1. Проверка исходного состояния блока
        """
        self.cli_log.lev_info(f"старт теста {__doc__}", "skyblue")
        if self.conn_opc.subtest_read_di(test_num=1, subtest_num=1.0, err_code=[199],
                                         position_inp=[False], di_xx=['inp_02']):
            return True
        return False

    def st_test_20(self) -> bool:
        """
            Тест 2. Проверка включения / выключения блока от кнопки «Пуск / Стоп».
        """
        self.conn_opc.ctrl_relay('KL22', True)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        self.conn_opc.ctrl_relay('KL21', True)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        self.conn_opc.ctrl_relay('KL2', True)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        self.conn_opc.ctrl_relay('KL33', True)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        self.conn_opc.ctrl_relay('KL32', True)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=2, subtest_num=2.0, err_code=[201],
                                         position_inp=[False], di_xx=['inp_02']):
            return True
        return False

    def st_test_21(self) -> bool:
        """
            2.2. Включение блока от кнопки «Пуск»
            2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        """
        if self.subtest.subtest_a(test_num=2, subtest_num=2.1):
            if self.subtest.subtest_b(test_num=2, subtest_num=2.2):
                return True
        return False

    def st_test_23(self) -> bool:
        """
            2.4. Выключение блока от кнопки «Стоп»
        """
        self.conn_opc.ctrl_relay('KL12', False)
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=2, subtest_num=2.3, err_code=[207],
                                         position_inp=[False], di_xx=['inp_02']):
            self.conn_opc.ctrl_relay('KL25', False)
            self.conn_opc.ctrl_relay('KL1', False)
            self.conn_opc.ctrl_relay('KL22', True)
            return True
        return False

    def st_test_30(self) -> bool:
        """
            3. подготовительные операции (повторение тестов 2.2 и 2.3)
        """
        if self.subtest.subtest_a(test_num=3, subtest_num=3.0):
            if self.subtest.subtest_b(test_num=3, subtest_num=3.1):
                return True
        return False

    def st_test_32(self) -> bool:
        """
            3. Удержание исполнительного элемента при увеличении сопротивления цепи заземления до 50 Ом
        """
        self.resist.resist_10_to_20_ohm()
        sleep(3)
        self.logger.debug("таймаут 3 сек")
        self.cli_log.lev_debug("таймаут 3 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=3, subtest_num=3.2, err_code=[209],
                                         position_inp=[True], di_xx=['inp_02']):
            return True
        return False

    def st_test_40(self) -> bool:
        """
            Тест 4. подготовительные операции (повторение тестов 2.2 и 2.3)
        """
        if self.subtest.subtest_a(test_num=4, subtest_num=4.0):
            if self.subtest.subtest_b(test_num=4, subtest_num=4.1):
                return True
        return False

    def st_test_42(self) -> bool:
        """
            Тест 4. Отключение исполнительного элемента при увеличении сопротивления
            цепи заземления на величину свыше 50 Ом
        """
        self.resist.resist_10_to_100_ohm()
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=4, subtest_num=4.2, err_code=[211],
                                         position_inp=[False], di_xx=['inp_02']):
            self.conn_opc.ctrl_relay('KL12', False)
            self.conn_opc.ctrl_relay('KL25', False)
            return True
        return False

    def st_test_50(self) -> bool:
        """
            Тест 5. подготовительные операции (повторение тестов 2.2 и 2.3)
        """
        if self.subtest.subtest_a(test_num=5, subtest_num=5.0):
            if self.subtest.subtest_b(test_num=5, subtest_num=5.1):
                return True
        return False

    def st_test_52(self) -> bool:
        """
            Тест 5. Защита от потери управляемости при замыкании проводов ДУ
        """
        self.conn_opc.ctrl_relay('KL11', True)
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=5, subtest_num=5.2, err_code=[213],
                                         position_inp=[False], di_xx=['inp_02']):
            self.conn_opc.ctrl_relay('KL12', False)
            self.conn_opc.ctrl_relay('KL1', False)
            self.conn_opc.ctrl_relay('KL25', False)
            self.conn_opc.ctrl_relay('KL11', False)
            return True
        return False

    def st_test_60(self) -> bool:
        """
            Тест 6. Защита от потери управляемости при обрыве проводов ДУ
        """
        if self.subtest.subtest_a(test_num=6, subtest_num=6.0):
            if self.subtest.subtest_b(test_num=6, subtest_num=6.1):
                return True
        return False

    def st_test_62(self) -> bool:
        self.conn_opc.ctrl_relay('KL12', False)
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=6, subtest_num=6.2, err_code=[215],
                                         position_inp=[False], di_xx=['inp_02']):
            return True
        return False

    def st_test_bdu_1m(self) -> bool:
        """
            Главная функция которая собирает все остальные
            :type: bool
            :return: результат теста
        """
        if self.st_test_1():
            if self.st_test_20():
                if self.st_test_21():
                    if self.st_test_23():
                        if self.st_test_30():
                            if self.st_test_32():
                                if self.st_test_40():
                                    if self.st_test_42():
                                        if self.st_test_50():
                                            if self.st_test_52():
                                                if self.st_test_60():
                                                    if self.st_test_62():
                                                        return True
        return False
