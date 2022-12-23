#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки
Тип блока: БКИ-1
Производитель: нет производителя, Углеприбор
Тип блока: БКИ-Т
Производитель: нет производителя, Углеприбор, ТЭТЗ-Инвест, СтройЭнергоМаш

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

__all__ = ["TestBKI1T"]


class TestBKI1T:

    def __init__(self):
        self.resist = Resistor()
        self.ctrl_kl = CtrlKL()
        self.mysql_conn = MySQLConnect()
        self.di_read_full = ReadOPCServer()

        logging.basicConfig(
            filename="C:\\Stend\\project_class\\log\\TestBKI1T.log",
            filemode="w",
            level=logging.DEBUG,
            encoding="utf-8",
            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('DEBUG')
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))

    def st_test_1_bki_1t(self) -> bool:
        """
        Тест 1. Проверка исходного состояния блока
        """
        if self.di_read_full.subtest_2di(test_num=1, subtest_num=1.0, err_code_a=30, err_code_b=30,
                                         position_a=True, position_b=False, di_a='in_a0', di_b='in_a1'):
            return True
        return False

    def st_test_20_bki_1t(self) -> bool:
        """
        Тест 2. Проверка работы блока при нормальном сопротивлении изоляции
        """
        self.ctrl_kl.ctrl_relay('KL21', True)
        sleep(2)
        self.resist.resist_kohm(220)
        sleep(2)
        if self.di_read_full.subtest_2di(test_num=2, subtest_num=2.0, err_code_a=31, err_code_b=31,
                                         position_a=True, position_b=False, di_a='in_a0', di_b='in_a1'):
            return True
        return False

    def st_test_30_bki_1t(self) -> bool:
        """
        Тест 3. Проверка работы блока в режиме «Предупредительный» при снижении
        уровня сопротивлении изоляции до 100 кОм
        """
        self.resist.resist_220_to_100_kohm()
        b = self.ctrl_kl.ctrl_ai_code_100()
        i = 0
        while b == 2 or i <= 30:
            sleep(0.2)
            i += 1
            b = self.ctrl_kl.ctrl_ai_code_100()
            if b == 0:
                break
            elif b == 1 or b == 9999:
                self.mysql_conn.mysql_error(32)
                self.mysql_conn.mysql_ins_result("неисправен", "3")
                return False
        self.mysql_conn.mysql_ins_result("исправен", "3")
        return True

    def st_test_40_bki_1t(self) -> bool:
        """
        Тест 4. Проверка работы блока в режиме «Аварийный» при сопротивлении изоляции 100 кОм
        """
        self.ctrl_kl.ctrl_relay('KL24', True)
        sleep(1)
        if self.di_read_full.subtest_2di(test_num=4, subtest_num=4.0, err_code_a=33, err_code_b=33,
                                         position_a=True, position_b=False, di_a='in_a0', di_b='in_a1'):
            self.ctrl_kl.ctrl_relay('KL21', False)
            return True
        return False

    def st_test_50_bki_1t(self) -> bool:
        """
        Тест 5. Работа блока в режиме «Аварийный» при сопротивлении изоляции
        ниже 30 кОм (Подключение на внутреннее сопротивление)
        """
        # self.resist.resist_kohm(220)
        sleep(1)
        self.ctrl_kl.ctrl_relay('KL22', True)
        sleep(1)
        if self.di_read_full.subtest_2di(test_num=5, subtest_num=5.0, err_code_a=34, err_code_b=34,
                                         position_a=False, position_b=True, di_a='in_a0', di_b='in_a1'):
            self.ctrl_kl.ctrl_relay('KL21', False)
            return True
        return False

    def st_test_bki_1t(self) -> bool:
        if self.st_test_1_bki_1t():
            if self.st_test_20_bki_1t():
                if self.st_test_30_bki_1t():
                    if self.st_test_40_bki_1t():
                        if self.st_test_50_bki_1t():
                            return True
        return False


if __name__ == '__main__':
    test_bki_1t = TestBKI1T()
    reset_test_bki_1t = ResetRelay()
    mysql_conn_bki_1t = MySQLConnect()
    try:
        if test_bki_1t.st_test_bki_1t():
            mysql_conn_bki_1t.mysql_block_good()
            my_msg('Блок исправен', 'green')
        else:
            mysql_conn_bki_1t.mysql_block_bad()
            my_msg('Блок неисправен', 'red')
    except OSError:
        my_msg("ошибка системы", 'red')
    except SystemError:
        my_msg("внутренняя ошибка", 'red')
    except ModbusConnectException as mce:
        my_msg(f'{mce}', 'red')
    finally:
        reset_test_bki_1t.reset_all()
        sys.exit()
