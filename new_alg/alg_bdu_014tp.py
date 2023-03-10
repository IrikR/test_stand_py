# -*- coding: utf-8 -*-
"""
!!! НОВЫЙ НЕ ОБКАТАНЫЙ !!!

Тип блока: БДУ
Производитель Углеприбор, Без Производителя
Тип блока: БДУ-1
Производитель Углеприбор, Без Производителя
Тип блока: БДУ-4
Производитель Углеприбор, Без Производителя
Тип блока: БДУ-Т
Производитель Строй-ЭнергоМаш, Углеприбор, ТЭТЗ-Инвест, Без Производителя
Тип блока: БДУ-П Х5-01
Производитель Пульсар
Тип блока: БДУ-П УХЛ 01
Производитель Пульсар
Тип блока: БДУ-П УХЛ5-03
Производитель Пульсар

"""

__all__ = ["TestBDU014TP"]

import logging
from time import sleep

from .general_func.database import *
from .general_func.opc_full import ConnectOPC
from .general_func.reset import ResetRelay
from .general_func.resistance import Resistor
from .general_func.subtest import SubtestBDU
from .general_func.utils import CLILog


class TestBDU014TP:

    def __init__(self):
        self.conn_opc = ConnectOPC()
        self.resist = Resistor()
        self.mysql_conn = MySQLConnect()
        self.sub_test = SubtestBDU()
        self.reset_relay = ResetRelay()
        self.cli_log = CLILog("debug", __name__)

        logging.basicConfig(
            filename="C:\\Stend\\project_class\\log\\TestBDU014TP.log",
            filemode="w",
            level=logging.DEBUG,
            encoding="utf-8",
            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('DEBUG')
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))

    def test_1(self) -> bool:
        """
        Тест 1. Проверка исходного состояния блока:
        :return:
        """
        self.cli_log.lev_info(f"старт теста {__doc__}", "skyblue")
        if self.conn_opc.subtest_read_di(test_num=1, subtest_num=1.0,
                                         err_code=[47],
                                         position_inp=[False],
                                         di_xx=['inp_01']):
            return True
        return False

    def test_20(self) -> bool:
        """
        Тест 2. Проверка включения / выключения блока от кнопки «Пуск / Стоп».
        2.1. Проверка исходного состояния блока
        """
        self.logger.debug(f"старт теста: 2, подтест: 0")
        self.conn_opc.ctrl_relay('KL2', True)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=2, subtest_num=2.0,
                                         err_code=[21],
                                         position_inp=[False],
                                         di_xx=['inp_01']):
            return True
        return False

    def test_21(self) -> bool:
        """
        2.2. Включение канала блока от кнопки «Пуск» при сопротивлении 10 Ом
        """
        if self.sub_test.subtest_a_bdu014tp(test_num=2, subtest_num=2.1):
            return True
        return False

    def test_22(self) -> bool:
        """
        2.3. Выключение канала блока от кнопки «Пуск» при сопротивлении 10 Ом
        """
        self.logger.debug(f"старт теста: 2, подтест: 2")
        self.conn_opc.ctrl_relay('KL12', False)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=2, subtest_num=2.2,
                                         err_code=[27],
                                         position_inp=[False],
                                         di_xx=['inp_01']):
            return True
        return False

    def test_30(self) -> bool:
        """
        Повтор теста 2.2
        """
        if self.sub_test.subtest_a_bdu014tp(test_num=3, subtest_num=3.0):
            return True
        return False

    def test_31(self) -> bool:
        """
        3. Удержание исполнительного элемента при сопротивлении цепи заземления до 35 Ом
        """
        self.logger.debug(f"старт теста: 3, подтест: 1")
        self.resist.resist_10_to_35_ohm()
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=3, subtest_num=3.1,
                                         err_code=[28],
                                         position_inp=[True],
                                         di_xx=['inp_01']):
            return True
        return False

    def test_40(self) -> bool:
        """
        4. Отключение исполнительного элемента при сопротивлении цепи заземления свыше 50 Ом
        """
        self.logger.debug(f"старт теста: 4, подтест: 0")
        self.resist.resist_35_to_110_ohm()
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=4, subtest_num=4.0,
                                         err_code=[29],
                                         position_inp=[False],
                                         di_xx=['inp_01']):
            self.conn_opc.ctrl_relay('KL12', False)
            self.conn_opc.ctrl_relay('KL1', False)
            return True
        return False

    def test_50(self) -> bool:
        """
        Повтор теста 2.2
        """
        if self.sub_test.subtest_a_bdu014tp(test_num=5, subtest_num=5.0):
            return True
        return False

    def test_51(self) -> bool:
        """
        5. Защита от потери управляемости при замыкании проводов ДУ
        """
        self.logger.debug(f"старт теста: 5, подтест: 1")
        self.conn_opc.ctrl_relay('KL11', True)
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=5, subtest_num=5.1,
                                         err_code=[3],
                                         position_inp=[False],
                                         di_xx=['inp_01']):
            self.conn_opc.ctrl_relay('KL12', False)
            self.conn_opc.ctrl_relay('KL1', False)
            self.conn_opc.ctrl_relay('KL11', False)
            return True
        return False

    def test_60(self) -> bool:
        """
        Повтор теста 2.2
        """
        if self.sub_test.subtest_a_bdu014tp(test_num=6, subtest_num=6.0):
            return True
        return False

    def test_61(self) -> bool:
        """
        Тест 6. Защита от потери управляемости при обрыве проводов ДУ
        """
        self.logger.debug(f"старт теста: 6, подтест: 1")
        self.conn_opc.ctrl_relay('KL12', False)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=6, subtest_num=6.1,
                                         err_code=[4],
                                         position_inp=[False],
                                         di_xx=['inp_01']):
            return True
        return False

    def st_test_bdu_014tp(self) -> bool:
        """
            Главная функция которая собирает все остальные
            :type: bool
            :return: результат теста
        """
        if self.test_1():
            if self.test_20():
                if self.test_21():
                    if self.test_22():
                        if self.test_30():
                            if self.test_31():
                                if self.test_40():
                                    if self.test_50():
                                        if self.test_51():
                                            if self.test_60():
                                                if self.test_61():
                                                    return True
        return False
