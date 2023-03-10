# -*- coding: utf-8 -*-
"""
!!! НА ИСПЫТАНИИ !!!

Алгоритм проверки

Тип блока: БДУ-1
Производитель: Без Производителя, Углеприбор

"""

__all__ = ["TestBDU1"]

import logging
from time import sleep

from .general_func.database import MySQLConnect
from .general_func.opc_full import ConnectOPC
from .general_func.reset import ResetRelay
from .general_func.resistance import Resistor
from .general_func.subtest import SubtestBDU
from .general_func.utils import CLILog


class TestBDU1:
    """
    st_test_1: Тест 1. Проверка исходного состояния блока;
    st_test_20: Тест 2 Проверка включения/отключения блока от кнопки пуск
    st_test_21: Тест-2.2 Проверка канала блока от кнопки "Пуск"
    st_test_22: Тест 2.3 Выключение канала блока от кнопки «Пуск» при сопротивлении 10 Ом
    st_test_30: Тест-3. Удержание исполнительного элемента при сопротивлении цепи заземления до 35 Ом
    st_test_40: Тест 4. Отключение исполнительного элемента при сопротивлении цепи заземления свыше 50 Ом
    st_test_50: Тест 5. Защита от потери управляемости при замыкании проводов ДУ
    st_test_60: Тест 6. Защита от потери управляемости при обрыве проводов ДУ
    st_test_bdu_1: Главная функция которая собирает все остальные.
    """

    def __init__(self):
        self.conn_opc = ConnectOPC()
        self.resist = Resistor()
        self.mysql_conn = MySQLConnect()
        self.subtest = SubtestBDU()
        self.reset_test_bdu_1 = ResetRelay()
        self.cli_log = CLILog("info", __name__)

        logging.basicConfig(
            filename="C:\\Stend\\project_class\\log\\TestBDU1.log",
            filemode="w",
            level=logging.DEBUG,
            encoding="utf-8",
            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('WARNING')
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))

    def st_test_1(self) -> bool:
        """
        Тест 1. Проверка исходного состояния блока.
        :return: Bool
        """
        self.cli_log.lev_info(f"старт теста {__doc__}", "skyblue")
        self.logger.debug(f"старт теста {__doc__}")
        if self.conn_opc.subtest_read_di(test_num=1, subtest_num=1.0, err_code=[30], di_xx=['inp_01'],
                                         position_inp=[False]):
            return True
        return False

    def st_test_20(self) -> bool:
        """
        Тест-2 Проверка включения/отключения блока от кнопки пуск.
        :return: Bool
        """
        self.logger.debug(f"теста 2.0")
        self.cli_log.lev_info("теста 2.0", "gray")
        self.conn_opc.ctrl_relay('KL2', True)
        sleep(3)
        self.logger.debug("таймаут 3 сек")
        self.cli_log.lev_debug("таймаут 3 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=2, subtest_num=2.0, err_code=[30], di_xx=['inp_01'],
                                         position_inp=[False]):
            return True
        return False

    def st_test_21(self) -> bool:
        """
        Тест-2.2 Проверка канала блока от кнопки "Пуск"
            Код ошибки 21 – Сообщение: Блок не исправен. Нет срабатывания блока от кнопки Пуск.
        :return: Bool
        """
        self.logger.debug(f"теста 2.1")
        self.cli_log.lev_info("Тест 2.1", "gray")
        self.resist.resist_ohm(10)
        sleep(3)
        self.logger.debug("таймаут 3 сек")
        self.cli_log.lev_debug("таймаут 3 сек", "gray")
        self.conn_opc.ctrl_relay('KL12', True)
        sleep(3)
        self.logger.debug("таймаут 3 сек")
        self.cli_log.lev_debug("таймаут 3 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=2, subtest_num=2.1, err_code=[21], di_xx=['inp_01'],
                                         position_inp=[True]):
            return True
        return False

    def st_test_22(self) -> bool:
        """
        Тест 2.3 Выключение канала блока от кнопки «Пуск» при сопротивлении 10 Ом.
            Код ошибки	23	–	Сообщение	«Блок не исправен. Блок не выключается от кнопки «Стоп».
        :return: Bool
        """
        self.logger.debug(f"теста 2.2")
        self.cli_log.lev_info("Тест 2.2", "gray")
        sleep(3)
        self.logger.debug("таймаут 3 сек")
        self.cli_log.lev_debug("таймаут 3 сек", "gray")
        self.conn_opc.ctrl_relay('KL12', False)
        sleep(3)
        self.logger.debug("таймаут 3 сек")
        self.cli_log.lev_debug("таймаут 3 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=2, subtest_num=2.2, err_code=[23], di_xx=['inp_01'],
                                         position_inp=[False]):
            return True
        return False

    def st_test_30(self) -> bool:
        """
        Тест-3. Удержание исполнительного элемента при сопротивлении цепи заземления до 35 Ом
            Код ошибки 28 – Сообщение: «Блок не исправен. Отсутствие удержания исполнительного
        элемента при сопротивлении до 35 Ом».

        :return: Bool
        """
        self.logger.debug(f"теста 3.0")
        self.cli_log.lev_info("Тест 3", "gray")
        sleep(3)
        self.logger.debug("таймаут 3 сек")
        self.cli_log.lev_debug("таймаут 3 сек", "gray")
        self.conn_opc.ctrl_relay('KL12', True)
        sleep(0.5)
        self.logger.debug("таймаут 0.5 сек")
        self.cli_log.lev_debug("таймаут 0.5 сек", "gray")
        # Отключаем KL5, KL8 для формирования 35 Ом
        self.conn_opc.ctrl_relay('KL5', False)
        self.conn_opc.ctrl_relay('KL8', False)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=3, subtest_num=3.0, err_code=[28], di_xx=['inp_01'],
                                         position_inp=[False]):
            return True
        return False

    def st_test_40(self) -> bool:
        """
        Тест 4. Отключение исполнительного элемента при сопротивлении цепи заземления свыше 50 Ом
            Код ошибки 29 – Сообщение: «Блок не исправен. Отключение исполнительного элемента при
            сопротивлении цепи заземления более 50 Ом».
        :return: Bool
        """
        self.logger.debug(f"теста 4.0")
        self.cli_log.lev_info("Тест 4", "gray")
        self.conn_opc.ctrl_relay('KL7', False)
        self.conn_opc.ctrl_relay('KL9', False)
        self.conn_opc.ctrl_relay('KL4', True)
        self.conn_opc.ctrl_relay('KL6', True)
        self.conn_opc.ctrl_relay('KL10', True)
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=4, subtest_num=4.0, err_code=[29], di_xx=['inp_01'],
                                         position_inp=[False]):
            self.conn_opc.ctrl_relay('KL12', True)
            return True
        return False

    def st_test_50(self) -> bool:
        """
        Тест 5. Защита от потери управляемости при замыкании проводов ДУ
                Код ошибки	03	–	Сообщение	«Блок не исправен. Выходные контакты блока не отключаются
                при замыкании проводов цепей ДУ».
        :return: Bool
        """
        self.logger.debug(f"теста 5.0")
        self.cli_log.lev_info("Тест 5", "gray")
        self.resist.resist_ohm(10)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        self.conn_opc.ctrl_relay('KL12', True)
        sleep(0.5)
        self.logger.debug("таймаут 0.5 сек")
        self.cli_log.lev_debug("таймаут 0.5 сек", "gray")
        self.conn_opc.ctrl_relay('KL11', True)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=5, subtest_num=5.0, err_code=[3], di_xx=['inp_01'],
                                         position_inp=[False]):
            self.conn_opc.ctrl_relay('KL12', False)
            self.conn_opc.ctrl_relay('KL11', False)
            self.conn_opc.ctrl_relay('KL1', False)
            return True
        return False

    def st_test_60(self) -> bool:
        """
        Тест 6. Защита от потери управляемости при обрыве проводов ДУ
        :return: Bool
        """
        self.logger.debug(f"теста 6.0")
        self.cli_log.lev_info("Тест 6", "gray")
        self.resist.resist_ohm(10)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        self.conn_opc.ctrl_relay('KL12', True)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        self.conn_opc.ctrl_relay('KL12', False)
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=4, subtest_num=4.0, err_code=[29], di_xx=['inp_01'],
                                         position_inp=[False]):
            return True
        return False

    def st_test_bdu_1(self) -> bool:
        """
            Главная функция которая собирает все остальные
            :type: bool
            :return: результат теста
        """
        if self.st_test_1():
            if self.st_test_20():
                if self.st_test_21():
                    if self.st_test_22():
                        if self.st_test_30():
                            if self.st_test_40():
                                if self.st_test_50():
                                    if self.st_test_60():
                                        return True
        return False
