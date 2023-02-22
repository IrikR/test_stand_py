# -*- coding: utf-8 -*-
"""
!!! ПРОВЕРЕН !!!

Алгоритм проверки

Тип блока: БДУ-Д4-2
Производитель: Нет производителя, ДонЭнергоЗавод
Тип блока: БДУ-Д.01
Производитель: Без Производителя

"""

__all__ = ["TestBDUD42"]

import logging
from time import sleep

from .general_func.database import *
from .general_func.opc_full import ConnectOPC
from .general_func.reset import ResetRelay
from .general_func.resistance import Resistor
from .general_func.subtest import Subtest2in
from .general_func.utils import CLILog


class TestBDUD42:

    def __init__(self):
        self.conn_opc = ConnectOPC()
        self.resist = Resistor()
        self.mysql_conn = MySQLConnect()
        self.subtest = Subtest2in()
        self.reset_relay = ResetRelay()
        self.cli_log = CLILog("debug", __name__)

        logging.basicConfig(filename="C:\Stend\project_class\log\TestBDUD42.log",
                            filemode="w",
                            level=logging.DEBUG,
                            encoding="utf-8",
                            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('DEBUG')
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))

    def st_test_1(self) -> bool:
        """
        Тест 1. Проверка исходного состояния блока:
        """
        self.cli_log.lev_info(f"старт теста {__doc__}", "skyblue")
        if self.conn_opc.subtest_read_di(test_num=1, subtest_num=1.0,
                                         err_code=[5, 6],
                                         position_inp=[False, False],
                                         di_xx=["inp_01", "inp_02"]):
            return True
        return False

    def st_test_20(self) -> bool:
        """
        Тест 2. Проверка включения выключения блока от кнопки «Пуск Стоп».
        2.1. Проверка исходного состояния блока
        """
        self.logger.debug("старт теста 2.0")
        self.conn_opc.ctrl_relay('KL2', True)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=2, subtest_num=2.0,
                                         err_code=[13, 14],
                                         position_inp=[False, False],
                                         di_xx=["inp_01", "inp_02"]):
            return True
        return False

    def st_test_21(self) -> bool:
        """
        2.2. Включение блока от кнопки «Пуск»
        2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        """
        if self.subtest.subtest_a_bdu(test_num=2, subtest_num=2.1, err_code_a=15, err_code_b=16,
                                      position_a=True, position_b=True):
            if self.subtest.subtest_b_bdu(test_num=2, subtest_num=2.2, err_code_a=7, err_code_b=8,
                                          position_a=True, position_b=True):
                return True
        return False

    def st_test_23(self) -> bool:
        """
        2.4. Выключение блока от кнопки «Стоп»
        """
        self.logger.debug("старт теста 2.3")
        self.conn_opc.ctrl_relay('KL12', False)
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=2, subtest_num=2.3,
                                         err_code=[17, 18],
                                         position_inp=[False, False],
                                         di_xx=["inp_01", "inp_02"]):
            self.conn_opc.ctrl_relay('KL1', False)
            self.conn_opc.ctrl_relay('KL25', False)
            return True
        return False

    def st_test_30(self) -> bool:
        """
        Повторяем тест 2.2. Включение блока от кнопки «Пуск»
        Повторяем тест 2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        """
        if self.subtest.subtest_a_bdu(test_num=3, subtest_num=3.0, err_code_a=15, err_code_b=16,
                                      position_a=True, position_b=True):
            if self.subtest.subtest_b_bdu(test_num=3, subtest_num=3.1, err_code_a=7, err_code_b=8,
                                          position_a=True, position_b=True):
                return True
        return False

    def st_test_32(self) -> bool:
        """
        3. Отключение исполнительного элемента при увеличении сопротивления цепи заземления
        """
        self.logger.debug("старт теста 3.2")
        self.resist.resist_10_to_110_ohm()
        sleep(3)
        self.logger.debug("таймаут 3 сек")
        self.cli_log.lev_debug("таймаут 3 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=3, subtest_num=3.2,
                                         err_code=[19, 20],
                                         position_inp=[False, False],
                                         di_xx=["inp_01", "inp_02"]):
            self.conn_opc.ctrl_relay('KL12', False)
            self.conn_opc.ctrl_relay('KL25', False)
            self.conn_opc.ctrl_relay('KL1', False)
            return True
        return False

    def st_test_40(self) -> bool:
        """
        Повторяем тест 2.2. Включение блока от кнопки «Пуск»
        Повторяем тест 2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        """
        if self.subtest.subtest_a_bdu(test_num=4, subtest_num=4.0, err_code_a=15, err_code_b=16,
                                      position_a=True, position_b=True):
            if self.subtest.subtest_b_bdu(test_num=4, subtest_num=4.1, err_code_a=7, err_code_b=8,
                                          position_a=True, position_b=True):
                return True
        return False

    def st_test_42(self) -> bool:
        """
        Тест 4. Защита от потери управляемости при замыкании проводов ДУ
        """
        self.logger.debug("старт теста 4.2")
        self.conn_opc.ctrl_relay('KL11', True)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=4, subtest_num=4.2,
                                         err_code=[9, 10],
                                         position_inp=[False, False],
                                         di_xx=["inp_01", "inp_02"]):
            self.conn_opc.ctrl_relay('KL12', False)
            self.conn_opc.ctrl_relay('KL25', False)
            self.conn_opc.ctrl_relay('KL1', False)
            self.conn_opc.ctrl_relay('KL11', False)
            return True
        return False

    def st_test_50(self) -> bool:
        """
        Повторяем тест 2.2. Включение блока от кнопки «Пуск»
        Повторяем тест 2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        """
        if self.subtest.subtest_a_bdu(test_num=5, subtest_num=5.0, err_code_a=15, err_code_b=16,
                                      position_a=True, position_b=True):
            if self.subtest.subtest_b_bdu(test_num=5, subtest_num=5.1, err_code_a=7, err_code_b=8,
                                          position_a=True, position_b=True):
                return True
        return False

    def st_test_52(self) -> bool:
        """
        Тест 5. Защита от потери управляемости при обрыве проводов ДУ
        """
        self.logger.debug("старт теста 5.2")
        self.conn_opc.ctrl_relay('KL12', False)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=5, subtest_num=5.2,
                                         err_code=[11, 12],
                                         position_inp=[False, False],
                                         di_xx=["inp_01", "inp_02"]):
            return True
        return False

    def st_test_bdu_d4_2(self) -> bool:
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
                                                return True
        return False
