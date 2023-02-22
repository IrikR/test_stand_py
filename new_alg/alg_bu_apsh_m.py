# -*- coding: utf-8 -*-
"""
!!! НОВЫЙ НЕ ОБКАТАНЫЙ !!!

Алгоритм проверки

Тип блока: БУ АПШ.М
Производитель: Без Производителя, Горэкс-Светотехника.

"""

__all__ = ["TestBUAPSHM"]

import logging
from time import sleep

from .general_func.database import *
from .general_func.opc_full import ConnectOPC
from .general_func.reset import ResetRelay
from .general_func.resistance import Resistor
from .general_func.subtest import Subtest2in
from .general_func.utils import CLILog


class TestBUAPSHM:

    def __init__(self):
        self.conn_opc = ConnectOPC()
        self.resist = Resistor()
        self.mysql_conn = MySQLConnect()
        self.subtest = Subtest2in()
        self.reset_relay = ResetRelay()
        self.cli_log = CLILog("debug", __name__)

        logging.basicConfig(
            filename="C:\\Stend\\project_class\\log\\TestBUAPShM.log",
            filemode="w",
            level=logging.DEBUG,
            encoding="utf-8",
            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('DEBUG')
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))

    def st_test_10(self) -> bool:
        """
        Тест 1. Проверка исходного состояния контактов блока:
        1.1. Проверка состояния контактов блока при подаче напряжения питания
        """
        self.cli_log.lev_info(f"старт теста {__doc__}", "skyblue")
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=1, subtest_num=1.0,
                                         err_code=[99, 100],
                                         position_inp=[False, False],
                                         di_xx=['inp_01', 'inp_02']):
            self.conn_opc.ctrl_relay('KL21', True)
            sleep(1)
            self.logger.debug("таймаут 1 сек")
            self.cli_log.lev_debug("таймаут 1 сек", "gray")
            if self.conn_opc.subtest_read_di(test_num=1, subtest_num=1.1,
                                             err_code=[101, 102],
                                             position_inp=[False, False],
                                             di_xx=['inp_01', 'inp_02']):
                return True
        return False

    def st_test_20(self) -> bool:
        """
        2. Проверка включения / выключения 1 канала блока от кнопки «Пуск / Стоп».
        2.1. Выключение 1 канала блока от кнопки «Пуск» при сопротивлении 10 Ом
        """
        self.logger.debug("старт теста 2.0")
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        if self.subtest.subtest_a_bdu(test_num=2, subtest_num=2.0, err_code_a=103, err_code_b=104,
                                      position_a=True, position_b=False, resist=10, timeout=3):
            self.conn_opc.ctrl_relay('KL12', False)
            sleep(1)
            self.logger.debug("таймаут 1 сек")
            self.cli_log.lev_debug("таймаут 1 сек", "gray")
            if self.conn_opc.subtest_read_di(test_num=2, subtest_num=2.1,
                                             err_code=[105, 106],
                                             position_inp=[False, False],
                                             di_xx=['inp_01', 'inp_02']):
                return True
        return False

    def st_test_30(self) -> bool:
        """
        3. Отключение 1 канала блока при увеличении сопротивления
        цепи заземления на величину более 100 Ом
        """
        self.logger.debug("старт теста 3.0")
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        if self.subtest.subtest_a_bdu(test_num=3, subtest_num=3.0, err_code_a=103, err_code_b=104,
                                      position_a=True, position_b=False, resist=10, timeout=3):
            self.resist.resist_10_to_110_ohm()
            sleep(2)
            self.logger.debug("таймаут 2 сек")
            self.cli_log.lev_debug("таймаут 2 сек", "gray")
            if self.conn_opc.subtest_read_di(test_num=3, subtest_num=3.1,
                                             err_code=[107, 108],
                                             position_inp=[False, False],
                                             di_xx=['inp_01', 'inp_02']):
                self.conn_opc.ctrl_relay('KL12', False)
                return True
        return False

    def st_test_40(self) -> bool:
        """
        4. Защита от потери управляемости 1 канала блока при замыкании проводов ДУ
        """
        self.logger.debug("старт теста 4.0")
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        if self.subtest.subtest_a_bdu(test_num=4, subtest_num=4.0, err_code_a=103, err_code_b=104,
                                      position_a=True, position_b=False, resist=10, timeout=3):
            self.conn_opc.ctrl_relay('KL11', True)
            sleep(2)
            self.logger.debug("таймаут 2 сек")
            self.cli_log.lev_debug("таймаут 2 сек", "gray")
            if self.conn_opc.subtest_read_di(test_num=4, subtest_num=4.1,
                                             err_code=[109, 110],
                                             position_inp=[False, False],
                                             di_xx=['inp_01', 'inp_02']):
                self.conn_opc.ctrl_relay('KL12', False)
                self.conn_opc.ctrl_relay('KL11', False)
                return True
        return False

    def st_test_50(self) -> bool:
        """
        Тест 5. Защита от потери управляемости 1 канала блока при обрыве проводов ДУ
        """
        self.logger.debug("старт теста 5.0")
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        if self.subtest.subtest_a_bdu(test_num=5, subtest_num=5.0, err_code_a=103, err_code_b=104,
                                      position_a=True, position_b=False, resist=10, timeout=3):
            self.conn_opc.ctrl_relay('KL12', False)
            sleep(2)
            self.logger.debug("таймаут 2 сек")
            self.cli_log.lev_debug("таймаут 2 сек", "gray")
            if self.conn_opc.subtest_read_di(test_num=5, subtest_num=5.1,
                                             err_code=[111, 112],
                                             position_inp=[False, False],
                                             di_xx=['inp_01', 'inp_02']):
                return True
        return False

    def st_test_60(self) -> bool:
        """
        6. Проверка включения / выключения 2 канала блока от кнопки «Пуск / Стоп».
        6.1. Включение 1 канала блока от кнопки «Пуск» при сопротивлении 10 Ом.
        6.2. Выключение 2 канала блока от кнопки «Пуск» при сопротивлении 10 Ом
        """
        self.logger.debug("старт теста 6.0")
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        self.conn_opc.ctrl_relay('KL26', True)
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        if self.subtest.subtest_a_bdu(test_num=6, subtest_num=6.0, err_code_a=113, err_code_b=114,
                                      position_a=False, position_b=True, resist=10, timeout=3):
            self.conn_opc.ctrl_relay('KL12', False)
            sleep(1)
            self.logger.debug("таймаут 1 сек")
            self.cli_log.lev_debug("таймаут 1 сек", "gray")
            if self.conn_opc.subtest_read_di(test_num=6, subtest_num=6.1,
                                             err_code=[115, 116],
                                             position_inp=[False, False],
                                             di_xx=['inp_01', 'inp_02']):
                return True
        return False

    def st_test_70(self) -> bool:
        """
        7. Отключение 2 канала блока при увеличении сопротивления цепи заземления
        на величину более 100 Ом
        """
        self.logger.debug("старт теста 1.0")
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        if self.subtest.subtest_a_bdu(test_num=7, subtest_num=7.0, err_code_a=113, err_code_b=114,
                                      position_a=False, position_b=True, resist=10, timeout=3):
            self.resist.resist_10_to_110_ohm()
            sleep(2)
            self.logger.debug("таймаут 2 сек")
            self.cli_log.lev_debug("таймаут 2 сек", "gray")
            if self.conn_opc.subtest_read_di(test_num=7, subtest_num=7.1,
                                             err_code=[117, 118],
                                             position_inp=[False, False],
                                             di_xx=['inp_01', 'inp_02']):
                self.conn_opc.ctrl_relay('KL12', False)
                return True
        return False

    def st_test_80(self) -> bool:
        """
        8. Защита от потери управляемости 2 канала блока при замыкании проводов ДУ
        """
        self.logger.debug("старт теста 1.0")
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        if self.subtest.subtest_a_bdu(test_num=8, subtest_num=8.0, err_code_a=113, err_code_b=114,
                                      position_a=False, position_b=True, resist=10, timeout=3):
            self.conn_opc.ctrl_relay('KL11', True)
            sleep(2)
            self.logger.debug("таймаут 2 сек")
            self.cli_log.lev_debug("таймаут 2 сек", "gray")
            if self.conn_opc.subtest_read_di(test_num=8, subtest_num=8.1,
                                             err_code=[119, 120],
                                             position_inp=[False, False],
                                             di_xx=['inp_01', 'inp_02']):
                self.conn_opc.ctrl_relay('KL12', False)
                self.conn_opc.ctrl_relay('KL11', False)
                return True
        return False

    def st_test_90(self) -> bool:
        """
        Тест 9. Защита от потери управляемости 2 канала блока при обрыве проводов ДУ
        """
        self.logger.debug("старт теста 1.0")
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        if self.subtest.subtest_a_bdu(test_num=9, subtest_num=9.0, err_code_a=113, err_code_b=114,
                                      position_a=False, position_b=True, resist=10, timeout=3):
            self.conn_opc.ctrl_relay('KL12', False)
            sleep(2)
            self.logger.debug("таймаут 2 сек")
            self.cli_log.lev_debug("таймаут 2 сек", "gray")
            if self.conn_opc.subtest_read_di(test_num=9, subtest_num=9.1,
                                             err_code=[121, 122],
                                             position_inp=[False, False],
                                             di_xx=['inp_01', 'inp_02']):
                return True
        return False

    def st_test_bu_apsh_m(self) -> bool:
        """
            Главная функция которая собирает все остальные
            :type: bool,
            :return: результат теста
        """
        if self.st_test_10():
            if self.st_test_20():
                if self.st_test_30():
                    if self.st_test_40():
                        if self.st_test_50():
                            if self.st_test_60():
                                if self.st_test_70():
                                    if self.st_test_80():
                                        if self.st_test_90():
                                            return True
        return False
