#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки
Тип блока: БКИ
Производитель: нет производителя, Углеприбор
Тип блока: БКИ-П
Производитель: Пульсар

"""

import logging
import sys
from time import sleep

from general_func.database import *
from general_func.exception import *
from general_func.modbus import *
from general_func.reset import ResetRelay
from general_func.resistance import Resistor
from general_func.subtest import ReadOPCServer
from gui.msgbox_1 import *

__all__ = ["TestBKIP"]


class TestBKIP:

    def __init__(self):
        self.resist = Resistor()
        self.ctrl_kl = CtrlKL()
        self.mysql_conn = MySQLConnect()
        self.di_read_full = ReadOPCServer()

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

    def st_test_1(self):
        """
        Тест 1. Проверка исходного состояния блока
        """
        if self.di_read_full.subtest_2di(test_num=1, subtest_num=1.0, err_code_a=30, err_code_b=30,
                                         position_a=True, position_b=False, di_a='in_a0', di_b='in_a1'):
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
        self.ctrl_kl.ctrl_relay('KL21', True)
        self.logger.debug("включен KL21")
        sleep(2)
        self.resist.resist_kohm(220)
        sleep(2)
        if self.di_read_full.subtest_2di(test_num=2, subtest_num=2.0, err_code_a=31, err_code_b=31,
                                         position_a=True, position_b=False, di_a='in_a0', di_b='in_a1'):
            return True
        return False

    def st_test_30(self) -> bool:
        """
        Тест 3. Проверка работы блока в режиме «Предупредительный» при снижении
        уровня сопротивлении изоляции до 100 кОм
        """
        self.logger.debug("старт теста 3.0")
        self.resist.resist_220_to_100_kohm()
        b = self.ctrl_kl.ctrl_ai_code_100()
        i = 0
        while b == 2 or i <= 10:
            sleep(0.2)
            i += 1
            b = self.ctrl_kl.ctrl_ai_code_100()
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
        if self.di_read_full.subtest_2di(test_num=4, subtest_num=4.0, err_code_a=33, err_code_b=33,
                                         position_a=True, position_b=False, di_a='in_a0', di_b='in_a1'):
            return True
        self.ctrl_kl.ctrl_relay('KL21', False)
        self.logger.debug("отключен KL21")
        return False

    def st_test_50(self) -> bool:
        """
        Тест 5. Работа блока в режиме «Аварийный» при сопротивлении изоляции
        ниже 30 кОм (Подключение на внутреннее сопротивление)
        """
        self.ctrl_kl.ctrl_relay('KL22', True)
        self.logger.debug("включен KL22")
        sleep(1)
        if self.di_read_full.subtest_2di(test_num=5, subtest_num=5.0, err_code_a=34, err_code_b=34,
                                         position_a=False, position_b=True, di_a='in_a0', di_b='in_a1'):
            self.ctrl_kl.ctrl_relay('KL21', False)
            self.logger.debug("отключен KL21")
            return True
        return False

    def st_test_bki_p(self) -> bool:
        if self.st_test_1():
            if self.st_test_20():
                if self.st_test_30():
                    if self.st_test_40():
                        if self.st_test_50():
                            return True
        return False


if __name__ == '__main__':
    test_bki_p = TestBKIP()
    reset_test_bki_p = ResetRelay()
    mysql_conn_bki_p = MySQLConnect()
    try:
        if test_bki_p.st_test_bki_p():
            mysql_conn_bki_p.mysql_block_good()
            my_msg('Блок исправен', 'green')
        else:
            mysql_conn_bki_p.mysql_block_bad()
            my_msg('Блок неисправен', 'red')
    except OSError:
        my_msg("ошибка системы", 'red')
    except SystemError:
        my_msg("внутренняя ошибка", 'red')
    except ModbusConnectException as mce:
        my_msg(f'{mce}', 'red')
    finally:
        reset_test_bki_p.reset_all()
        sys.exit()
