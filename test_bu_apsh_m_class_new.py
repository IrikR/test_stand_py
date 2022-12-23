#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки

Тип блока: БУ АПШ.М
Производитель: Без Производителя, Горэкс-Светотехника.
"""

import logging
import sys
from time import sleep

from general_func.database import *
from general_func.exception import *
from general_func.modbus import *
from general_func.reset import ResetRelay
from general_func.resistance import Resistor
from general_func.subtest import Subtest2in, ReadOPCServer
from gui.msgbox_1 import *

__all__ = ["TestBUAPSHM"]


class TestBUAPSHM:

    def __init__(self):
        self.resist = Resistor()
        self.ctrl_kl = CtrlKL()
        self.mysql_conn = MySQLConnect()
        self.subtest = Subtest2in()
        self.di_read_full = ReadOPCServer()

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
        self.logger.debug("старт теста 1.0")
        sleep(2)
        if self.di_read_full.subtest_2di(test_num=1, subtest_num=1.0, err_code_a=99, err_code_b=100, position_a=False,
                                         position_b=False):
            self.ctrl_kl.ctrl_relay('KL21', True)
            self.logger.debug("включен KL21")
            sleep(1)
            if self.di_read_full.subtest_2di(test_num=1, subtest_num=1.1, err_code_a=101, err_code_b=102,
                                             position_a=False, position_b=False):
                return True
        return False

    def st_test_20(self) -> bool:
        """
        2. Проверка включения / выключения 1 канала блока от кнопки «Пуск / Стоп».
        2.1. Выключение 1 канала блока от кнопки «Пуск» при сопротивлении 10 Ом
        """
        self.logger.debug("старт теста 2.0")
        sleep(2)
        if self.subtest.subtest_a_bdu(test_num=2, subtest_num=2.0, err_code_a=103, err_code_b=104,
                                      position_a=True, position_b=False, resist=10, timeout=3):
            self.ctrl_kl.ctrl_relay('KL12', False)
            self.logger.debug("отключен KL12")
            sleep(1)
            if self.di_read_full.subtest_2di(test_num=2, subtest_num=2.1, err_code_a=105, err_code_b=106,
                                             position_a=False, position_b=False):
                return True
        return False

    def st_test_30(self) -> bool:
        """
        3. Отключение 1 канала блока при увеличении сопротивления
        цепи заземления на величину более 100 Ом
        """
        self.logger.debug("старт теста 3.0")
        sleep(2)
        if self.subtest.subtest_a_bdu(test_num=3, subtest_num=3.0, err_code_a=103, err_code_b=104,
                                      position_a=True, position_b=False, resist=10, timeout=3):
            self.resist.resist_10_to_110_ohm()
            sleep(2)
            if self.di_read_full.subtest_2di(test_num=3, subtest_num=3.1, err_code_a=107, err_code_b=108,
                                             position_a=False, position_b=False):
                self.ctrl_kl.ctrl_relay('KL12', False)
                self.logger.debug("отключен KL12")
                return True
        return False

    def st_test_40(self) -> bool:
        """
        4. Защита от потери управляемости 1 канала блока при замыкании проводов ДУ
        """
        self.logger.debug("старт теста 4.0")
        sleep(2)
        if self.subtest.subtest_a_bdu(test_num=4, subtest_num=4.0, err_code_a=103, err_code_b=104,
                                      position_a=True, position_b=False, resist=10, timeout=3):
            self.ctrl_kl.ctrl_relay('KL11', True)
            self.logger.debug("включен KL11")
            sleep(2)
            if self.di_read_full.subtest_2di(test_num=4, subtest_num=4.1, err_code_a=109, err_code_b=110,
                                             position_a=False, position_b=False):
                self.ctrl_kl.ctrl_relay('KL12', False)
                self.ctrl_kl.ctrl_relay('KL11', False)
                self.logger.debug("отключены KL12, KL11")
                return True
        return False

    def st_test_50(self) -> bool:
        """
        Тест 5. Защита от потери управляемости 1 канала блока при обрыве проводов ДУ
        """
        self.logger.debug("старт теста 5.0")
        sleep(2)
        if self.subtest.subtest_a_bdu(test_num=5, subtest_num=5.0, err_code_a=103, err_code_b=104,
                                      position_a=True, position_b=False, resist=10, timeout=3):
            self.ctrl_kl.ctrl_relay('KL12', False)
            self.logger.debug("отключен KL12")
            sleep(2)
            if self.di_read_full.subtest_2di(test_num=5, subtest_num=5.1, err_code_a=111, err_code_b=112,
                                             position_a=False, position_b=False):
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
        self.ctrl_kl.ctrl_relay('KL26', True)
        self.logger.debug("включен KL26")
        sleep(2)
        if self.subtest.subtest_a_bdu(test_num=6, subtest_num=6.0, err_code_a=113, err_code_b=114,
                                      position_a=False, position_b=True, resist=10, timeout=3):
            self.ctrl_kl.ctrl_relay('KL12', False)
            self.logger.debug("отключен KL12")
            sleep(1)
            if self.di_read_full.subtest_2di(test_num=6, subtest_num=6.1, err_code_a=115, err_code_b=116,
                                             position_a=False, position_b=False):
                return True
        return False

    def st_test_70(self) -> bool:
        """
        7. Отключение 2 канала блока при увеличении сопротивления цепи заземления
        на величину более 100 Ом
        """
        self.logger.debug("старт теста 1.0")
        sleep(2)
        if self.subtest.subtest_a_bdu(test_num=7, subtest_num=7.0, err_code_a=113, err_code_b=114,
                                      position_a=False, position_b=True, resist=10, timeout=3):
            self.resist.resist_10_to_110_ohm()
            sleep(2)
            if self.di_read_full.subtest_2di(test_num=7, subtest_num=7.1, err_code_a=117, err_code_b=118,
                                             position_a=False, position_b=False):
                self.ctrl_kl.ctrl_relay('KL12', False)
                self.logger.debug("отключен KL12")
                return True
        return False

    def st_test_80(self) -> bool:
        """
        8. Защита от потери управляемости 2 канала блока при замыкании проводов ДУ
        """
        self.logger.debug("старт теста 1.0")
        sleep(2)
        if self.subtest.subtest_a_bdu(test_num=8, subtest_num=8.0, err_code_a=113, err_code_b=114,
                                      position_a=False, position_b=True, resist=10, timeout=3):
            self.ctrl_kl.ctrl_relay('KL11', True)
            self.logger.debug("включен KL11")
            sleep(2)
            if self.di_read_full.subtest_2di(test_num=8, subtest_num=8.1, err_code_a=119, err_code_b=120,
                                             position_a=False, position_b=False):
                self.ctrl_kl.ctrl_relay('KL12', False)
                self.ctrl_kl.ctrl_relay('KL11', False)
                self.logger.debug("отключены KL12, KL11")
                return True
        return False

    def st_test_90(self) -> bool:
        """
        Тест 9. Защита от потери управляемости 2 канала блока при обрыве проводов ДУ
        """
        self.logger.debug("старт теста 1.0")
        sleep(2)
        if self.subtest.subtest_a_bdu(test_num=9, subtest_num=9.0, err_code_a=113, err_code_b=114,
                                      position_a=False, position_b=True, resist=10, timeout=3):
            self.ctrl_kl.ctrl_relay('KL12', False)
            self.logger.debug("отключен KL12")
            sleep(2)
            if self.di_read_full.subtest_2di(test_num=9, subtest_num=9.1, err_code_a=121, err_code_b=122,
                                             position_a=False, position_b=False):
                return True
        return False

    def st_test_bu_apsh_m(self) -> bool:
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


if __name__ == '__main__':
    test_bu_apsh_m = TestBUAPSHM()
    reset_test_bu_apsh_m = ResetRelay()
    mysql_conn_bu_apsh_m = MySQLConnect()
    try:
        if test_bu_apsh_m.st_test_bu_apsh_m():
            mysql_conn_bu_apsh_m.mysql_block_good()
            my_msg('Блок исправен', 'green')
        else:
            mysql_conn_bu_apsh_m.mysql_block_bad()
            my_msg('Блок неисправен', 'red')
    except OSError:
        my_msg("ошибка системы", 'red')
    except SystemError:
        my_msg("внутренняя ошибка", 'red')
    except ModbusConnectException as mce:
        my_msg(f's{mce}', 'red')
    finally:
        reset_test_bu_apsh_m.reset_all()
        sys.exit()
