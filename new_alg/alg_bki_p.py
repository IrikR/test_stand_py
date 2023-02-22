# -*- coding: utf-8 -*-
"""
!!! НОВЫЙ НЕ ОБКАТАНЫЙ !!!

Алгоритм проверки

Тип блока: БКИ
Производитель: нет производителя, Углеприбор
Тип блока: БКИ-П
Производитель: Пульсар

"""

__all__ = ["TestBKIP"]

import logging
from time import sleep

from .general_func.database import *
from .general_func.opc_full import ConnectOPC
from .general_func.reset import ResetRelay
from .general_func.resistance import Resistor
from .general_func.utils import CLILog
from .gui.msgbox_1 import *


class TestBKIP:

    def __init__(self):
        self.conn_opc = ConnectOPC()
        self.resist = Resistor()
        self.mysql_conn = MySQLConnect()
        self.reset_relay = ResetRelay()
        self.cli_log = CLILog("debug", __name__)

        self.msg_1 = 'Переведите тумблер на блоке в режим «Предупредительный»'
        self.msg_2 = 'Переведите тумблер на блоке в режим «Аварийный»'

        logging.basicConfig(
            filename="C:\\Stend\\project_class\\log\\TestBKIP.log",
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
        if self.conn_opc.subtest_read_di(test_num=1, subtest_num=1.0,
                                         err_code=[30, 30],
                                         position_inp=[True, False],
                                         di_xx=['inp_00', 'inp_01']):
            return True
        return False

    def st_test_20(self) -> bool:
        """
        Тест 2. Проверка работы блока при нормальном сопротивлении изоляции
        """
        self.logger.debug("старт теста 2.0")
        if my_msg(self.msg_1):
            self.logger.debug("от пользователя пришло подтверждение")
        else:
            self.logger.debug("от пользователя пришла отмена")
            return False
        self.conn_opc.ctrl_relay('KL21', True)
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        self.resist.resist_kohm(220)
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=2, subtest_num=2.0,
                                         err_code=[31, 31],
                                         position_inp=[True, False],
                                         di_xx=['inp_00', 'inp_01']):
            return True
        return False

    def st_test_30(self) -> bool:
        """
        Тест 3. Проверка работы блока в режиме «Предупредительный» при снижении
        уровня сопротивлении изоляции до 100 кОм
        """
        self.logger.debug("старт теста 3.0")
        self.resist.resist_220_to_100_kohm()
        b = self.conn_opc.ctrl_ai_code_100()
        i = 0
        while b == 2 or i <= 10:
            sleep(0.2)
            i += 1
            b = self.conn_opc.ctrl_ai_code_100()
            if b == 0:
                break
            elif b == 1:
                self.mysql_conn.mysql_error(32)
                return False
        self.mysql_conn.mysql_ins_result("исправен", "3")
        return True

    def st_test_40(self) -> bool:
        """
        Тест 4. Проверка работы блока в режиме «Аварийный» при сопротивлении изоляции 100 кОм
        """
        self.logger.debug("старт теста 4.0")
        if my_msg(self.msg_2):
            self.logger.debug("от пользователя пришло подтверждение")
        else:
            self.logger.debug("от пользователя пришла отмена")
            return False
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=4, subtest_num=4.0,
                                         err_code=[33, 33],
                                         position_inp=[True, False],
                                         di_xx=['inp_00', 'inp_01']):
            return True
        self.conn_opc.ctrl_relay('KL21', False)
        return False

    def st_test_50(self) -> bool:
        """
        Тест 5. Работа блока в режиме «Аварийный» при сопротивлении изоляции
        ниже 30 кОм (Подключение на внутреннее сопротивление)
        """
        self.conn_opc.ctrl_relay('KL22', True)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=5, subtest_num=5.0,
                                         err_code=[34, 34],
                                         position_inp=[False, True],
                                         di_xx=['inp_00', 'inp_01']):
            self.conn_opc.ctrl_relay('KL21', False)
            return True
        return False

    def st_test_bki_p(self) -> bool:
        """
            Главная функция которая собирает все остальные
            :type: bool
            :return: результат теста
        """
        if self.st_test_1():
            if self.st_test_20():
                if self.st_test_30():
                    if self.st_test_40():
                        if self.st_test_50():
                            return True
        return False
