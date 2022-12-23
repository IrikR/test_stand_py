#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки
Тип блока: БКИ-2Т
Производитель: нет производителя, ТЭТЗ-Инвест, Строй-энерго
Модификации: 52, 53, 54

"""

import sys
import logging

from time import sleep

from general_func.exception import *
from general_func.subtest import ReadOPCServer
from general_func.database import *
from general_func.modbus import *
from general_func.resistance import Resistor
from general_func.reset import ResetRelay
from gui.msgbox_1 import *

__all__ = ["TestBKI2T"]


class TestBKI2T:

    def __init__(self):
        self.resist = Resistor()
        self.ctrl_kl = CtrlKL()
        self.mysql_conn = MySQLConnect()
        self.di_read_full = ReadOPCServer()

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
        if self.di_read_full.subtest_4di(test_num=1, subtest_num=1.0,
                                         err_code_a=35, err_code_b=35, err_code_c=36, err_code_d=36,
                                         position_a=True, position_b=False, position_c=True, position_d=False,
                                         di_a='in_a5', di_b='in_a1', di_c='in_a6', di_d='in_a2'):
            return True
        return False

    def st_test_20(self) -> bool:
        """
        Тест 2. Проверка работы блока при подаче питания и при
        нормальном сопротивлении изоляции контролируемого присоединения
        """
        self.logger.debug("старт теста 2.0")
        self.ctrl_kl.ctrl_relay('KL21', True)
        self.logger.debug("включен KL21")
        sleep(5)
        if self.di_read_full.subtest_4di(test_num=2, subtest_num=2.0,
                                         err_code_a=37, err_code_b=37, err_code_c=38, err_code_d=38,
                                         position_a=True, position_b=False, position_c=True, position_d=False,
                                         di_a='in_a5', di_b='in_a1', di_c='in_a6', di_d='in_a2'):
            return True
        return False

    def st_test_30(self) -> bool:
        """
        Тест 3. Проверка работы 1 канала (К1) блока при снижении
        уровня сопротивлении изоляции ниже 30 кОм в цепи 1 канала
        """
        self.logger.debug("старт теста 3.0")
        self.ctrl_kl.ctrl_relay('KL31', True)
        self.logger.debug("включен KL31")
        self.resist.resist_kohm(12)
        sleep(1)
        if self.di_read_full.subtest_4di(test_num=3, subtest_num=3.0,
                                         err_code_a=39, err_code_b=39, err_code_c=40, err_code_d=40,
                                         position_a=False, position_b=True, position_c=True, position_d=False,
                                         di_a='in_a5', di_b='in_a1', di_c='in_a6', di_d='in_a2'):
            self.resist.resist_kohm(590)
            return True
        return False

    def st_test_40(self) -> bool:
        """
        Тест 4. Проверка работы 1 канала (К1) блока от кнопки «Проверка БКИ» в цепи 1 канала
        """
        if self.di_read_full.subtest_4di(test_num=4, subtest_num=4.0,
                                         err_code_a=37, err_code_b=37, err_code_c=38, err_code_d=38,
                                         position_a=True, position_b=False, position_c=True, position_d=False,
                                         di_a='in_a5', di_b='in_a1', di_c='in_a6', di_d='in_a2'):
            return True
        return False

    def st_test_41(self) -> bool:
        """

        :return:
        """
        self.logger.debug("старт теста 4.1")
        self.ctrl_kl.ctrl_relay('KL23', True)
        self.ctrl_kl.ctrl_relay('KL22', True)
        self.logger.debug("включены KL23, KL22")
        sleep(1)
        if self.di_read_full.subtest_4di(test_num=4, subtest_num=4.1,
                                         err_code_a=41, err_code_b=41, err_code_c=42, err_code_d=42,
                                         position_a=False, position_b=True, position_c=True, position_d=False,
                                         di_a='in_a5', di_b='in_a1', di_c='in_a6', di_d='in_a2'):
            self.resist.resist_kohm(590)
            self.ctrl_kl.ctrl_relay('KL22', False)
            self.logger.debug("отключен KL22")
            return True
        return False

    def st_test_50(self) -> bool:
        """
        Тест 5. Проверка работы 2 канала (К2) блока при снижении уровня
        сопротивлении изоляции ниже 30 кОм в цепи 2 канала
        """
        self.logger.debug("старт теста 5.0")
        self.ctrl_kl.ctrl_relay('KL31', False)
        self.logger.debug("отключен KL31")
        sleep(1)
        self.resist.resist_kohm(12)
        sleep(1)
        if self.di_read_full.subtest_4di(test_num=5, subtest_num=5.0,
                                         err_code_a=43, err_code_b=43, err_code_c=44, err_code_d=44,
                                         position_a=True, position_b=False, position_c=False, position_d=True,
                                         di_a='in_a5', di_b='in_a1', di_c='in_a6', di_d='in_a2'):
            self.resist.resist_kohm(590)
            return True
        return False

    def st_test_60(self) -> bool:
        """
        Тест 6. Проверка работы 2 канала (К2) блока от кнопки «Проверка БКИ» в цепи 2 канала
        """
        if self.di_read_full.subtest_4di(test_num=6, subtest_num=6.0,
                                         err_code_a=37, err_code_b=37, err_code_c=38, err_code_d=38,
                                         position_a=True, position_b=False, position_c=True, position_d=False,
                                         di_a='in_a5', di_b='in_a1', di_c='in_a6', di_d='in_a2'):
            return True
        return False

    def st_test_61(self) -> bool:
        self.logger.debug("старт теста 6.1")
        self.ctrl_kl.ctrl_relay('KL22', True)
        self.logger.debug("включен KL22")
        sleep(1)
        if self.di_read_full.subtest_4di(test_num=6, subtest_num=6.1,
                                         err_code_a=45, err_code_b=45, err_code_c=46, err_code_d=46,
                                         position_a=True, position_b=False, position_c=False, position_d=True,
                                         di_a='in_a5', di_b='in_a1', di_c='in_a6', di_d='in_a2'):
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


if __name__ == '__main__':
    test_bki_2t = TestBKI2T()
    reset_test_bki_2t = ResetRelay()
    mysql_conn_bki_2t = MySQLConnect()
    try:
        if test_bki_2t.st_test_bki_2t():
            mysql_conn_bki_2t.mysql_block_good()
            my_msg('Блок исправен', 'green')
        else:
            mysql_conn_bki_2t.mysql_block_bad()
            my_msg('Блок неисправен', 'red')
    except OSError:
        my_msg("ошибка системы", 'red')
    except SystemError:
        my_msg("внутренняя ошибка", 'red')
    except ModbusConnectException as mce:
        my_msg(f'{mce}', 'red')
    finally:
        reset_test_bki_2t.reset_all()
        sys.exit()
