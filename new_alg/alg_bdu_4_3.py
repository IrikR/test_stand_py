# -*- coding: utf-8 -*-
"""
!!! НОВЫЙ НЕ ОБКАТАНЫЙ !!!

Алгоритм проверки

Тип блока: БДУ-4-3
Производитель: Без Производителя, Углеприбор

"""

__all__ = ["TestBDU43"]

import logging

from .general_func.database import *
from .general_func.opc_full import ConnectOPC
from .general_func.reset import ResetRelay
from .general_func.resistance import Resistor
from .general_func.subtest import SubtestBDU
from .general_func.utils import CLILog


class TestBDU43:

    def __init__(self):
        self.conn_opc = ConnectOPC()
        self.resist = Resistor()
        self.mysql_conn = MySQLConnect()
        self.sub_test = SubtestBDU()
        self.reset_relay = ResetRelay()
        self.cli_log = CLILog("debug", __name__)

        logging.basicConfig(
            filename="C:\\Stend\\project_class\\log\\TestBDU43.log",
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
        if self.conn_opc.subtest_read_di(test_num=1, subtest_num=1.0, err_code=[47], di_xx=['inp_01'],
                                         position_inp=[False]):
            return True
        return False

    def st_test_20(self) -> bool:
        """
            Тест 2. Проверка включения выключения блока от кнопки «Пуск Стоп».
            2.1. Проверка исходного состояния блока
        """
        self.logger.debug("старт теста 2.0")
        self.conn_opc.ctrl_relay('KL2', True)
        if self.conn_opc.subtest_read_di(test_num=2, subtest_num=2.0,
                                         err_code=[13],
                                         position_inp=[False],
                                         di_xx=['inp_01']):
            return True
        return False

    def st_test_21(self) -> bool:
        """
            2.2. Включение блока от кнопки «Пуск»
            2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        """
        if self.sub_test.subtest_a_bdu43_bru2s(test_num=2, subtest_num=2.1):
            if self.sub_test.subtest_b_bdu43_d(test_num=2, subtest_num=2.2):
                return True
        return False

    def st_test_23(self) -> bool:
        """
            2.4. Выключение блока от кнопки «Стоп»
        """
        self.logger.debug("старт теста 2.3")
        self.conn_opc.ctrl_relay('KL12', False)
        if self.conn_opc.subtest_read_di(test_num=2, subtest_num=2.3,
                                         err_code=[23],
                                         position_inp=[False],
                                         di_xx=['inp_01']):
            self.conn_opc.ctrl_relay('KL25', False)
            self.conn_opc.ctrl_relay('KL1', False)
            return True
        return False

    def st_test_30(self) -> bool:
        """
            3. повторяем тесты 2.2 и 2.3
        """
        if self.sub_test.subtest_a_bdu43_bru2s(test_num=3, subtest_num=3.0):
            if self.sub_test.subtest_b_bdu43_d(test_num=3, subtest_num=3.1):
                return True
        return False

    def st_test_32(self) -> bool:
        """
            3.2 Отключение исполнительного элемента при увеличении сопротивления цепи заземления
        """
        self.logger.debug("старт теста 3.2")
        self.resist.resist_0_to_63_ohm()
        if self.conn_opc.subtest_read_di(test_num=3, subtest_num=3.2,
                                         err_code=[24],
                                         position_inp=[False],
                                         di_xx=['inp_01']):
            self.conn_opc.ctrl_relay('KL12', False)
            self.conn_opc.ctrl_relay('KL25', False)
            self.conn_opc.ctrl_relay('KL1', False)
            return True
        return False

    def st_test_40(self) -> bool:
        """
            4. повторяем тесты 2.2 и 2.3
        """
        if self.sub_test.subtest_a_bdu43_bru2s(test_num=4, subtest_num=4.0):
            if self.sub_test.subtest_b_bdu43_d(test_num=4, subtest_num=4.1):
                return True
        return False

    def st_test_42(self) -> bool:
        """
            Тест 4.2 Защита от потери управляемости при замыкании проводов ДУ
        """
        self.logger.debug("старт теста 4.2")
        self.conn_opc.ctrl_relay('KL11', True)
        if self.conn_opc.subtest_read_di(test_num=4, subtest_num=4.2,
                                         err_code=[3], position_inp=[False],
                                         di_xx=['inp_01']):
            self.conn_opc.ctrl_relay('KL12', False)
            self.conn_opc.ctrl_relay('KL25', False)
            self.conn_opc.ctrl_relay('KL1', False)
            self.conn_opc.ctrl_relay('KL11', False)
            return True
        return False

    def st_test_50(self) -> bool:
        """
            5. повторяем тесты 2.2 и 2.3
        """
        if self.sub_test.subtest_a_bdu43_bru2s(test_num=5, subtest_num=5.0):
            if self.sub_test.subtest_b_bdu43_d(test_num=5, subtest_num=5.1):
                return True
        return False

    def st_test_52(self) -> bool:
        """
            Тест 5. Защита от потери управляемости при обрыве проводов ДУ
        """
        self.logger.debug("старт теста 5.2")
        self.conn_opc.ctrl_relay('KL12', False)
        if self.conn_opc.subtest_read_di(test_num=5, subtest_num=5.2,
                                         err_code=[4], position_inp=[False],
                                         di_xx=['inp_01']):
            return True
        return False

    def st_test_bdu_4_3(self) -> bool:
        """
            Главная функция которая собирает все остальные
            :type: bool
            :return: результат теста
        """
        if self.st_test_10():
            if self.st_test_20():
                if self.st_test_21():
                    if self.st_test_23():
                        if self.st_test_30():
                            if self.st_test_32():
                                if self.st_test_40():
                                    if self.st_test_42():
                                        if self.st_test_50():
                                            if self.st_test_52():
                                                return True
        return False
