#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки
Тип блока: БДУ-4-2
Производитель: Нет производителя, ДонЭнергоЗавод, ИТЭП

"""

import sys
import logging

from time import sleep

from general_func.exception import *
from general_func.subtest import ReadOPCServer, Subtest2in
from general_func.database import *
from general_func.modbus import *
from general_func.resistance import Resistor
from general_func.reset import ResetRelay
from gui.msgbox_1 import *

__all__ = ["TestBDU42"]


class TestBDU42:

    def __init__(self):
        self.resist = Resistor()
        self.ctrl_kl = CtrlKL()
        self.mysql_conn = MySQLConnect()
        self.subtest = Subtest2in()
        self.di_read_full = ReadOPCServer()

        logging.basicConfig(
            filename="C:\\Stend\\project_class\\log\\TestBDU42.log",
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
        if self.di_read_full.subtest_2di(test_num=1, subtest_num=1.0, err_code_a=5, err_code_b=6, position_a=False,
                                         position_b=False, di_a='in_a1', di_b='in_a2'):
            return True
        return False

    def st_test_20(self) -> bool:
        """
            Тест 2. Проверка включения выключения блока от кнопки «Пуск Стоп».
            2.1. Проверка исходного состояния блока
        """
        self.logger.debug("старт теста 2.0")
        self.ctrl_kl.ctrl_relay('KL2', True)
        self.logger.debug("включен KL2")
        if self.di_read_full.subtest_2di(test_num=2, subtest_num=2.0, err_code_a=13, err_code_b=14, position_a=False,
                                         position_b=False, di_a='in_a1', di_b='in_a2'):
            return True
        return False

    def st_test_21(self) -> bool:
        """
            2.2. Включение блока от кнопки «Пуск»
            2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        """
        if self.subtest.subtest_a_bdu(test_num=2, subtest_num=2.1, err_code_a=15, err_code_b=16,
                                      position_a=True, position_b=True, resist=10, timeout=2):
            if self.subtest.subtest_b_bdu(test_num=2, subtest_num=2.2, err_code_a=7, err_code_b=8,
                                          position_a=True, position_b=True, kl1=True):
                return True
        return False

    def st_test_23(self) -> bool:
        """
            2.4. Выключение блока от кнопки «Стоп»
        """
        self.logger.debug("старт теста 2.3")
        self.ctrl_kl.ctrl_relay('KL12', False)
        self.logger.debug("отключен KL12")
        sleep(2)
        if self.di_read_full.subtest_2di(test_num=2, subtest_num=2.3, err_code_a=17, err_code_b=18, position_a=False,
                                         position_b=False, di_a='in_a1', di_b='in_a2'):
            self.ctrl_kl.ctrl_relay('KL25', False)
            self.ctrl_kl.ctrl_relay('KL1', False)
            self.logger.debug("отключены KL25, KL1")
            return True
        return False

    def st_test_30(self) -> bool:
        """
            Тест 3. повторяем тесты 2.2 и 2.3
        """
        if self.subtest.subtest_a_bdu(test_num=3, subtest_num=3.0, err_code_a=15, err_code_b=16,
                                      position_a=True, position_b=True, resist=10, timeout=2):
            if self.subtest.subtest_b_bdu(test_num=3, subtest_num=3.1, err_code_a=7, err_code_b=8,
                                          position_a=True, position_b=True):
                return True
        return False

    # noinspection DuplicatedCode
    def st_test_32(self) -> bool:
        """
            3. Отключение исполнительного элемента при увеличении сопротивления цепи заземления
        """
        self.logger.debug("старт теста 3.2")
        self.resist.resist_10_to_110_ohm()
        sleep(1)
        if self.di_read_full.subtest_2di(test_num=3, subtest_num=3.2, err_code_a=19, err_code_b=20, position_a=False,
                                         position_b=False, di_a='in_a1', di_b='in_a2'):
            self.ctrl_kl.ctrl_relay('KL12', False)
            self.ctrl_kl.ctrl_relay('KL25', False)
            self.ctrl_kl.ctrl_relay('KL1', False)
            self.logger.debug("отключены KL12, KL25, KL1")
            return True
        return False

    def st_test_40(self) -> bool:
        """
            Тест 4. повторяем тесты 2.2 и 2.3
        """
        if self.subtest.subtest_a_bdu(test_num=4, subtest_num=4.0, err_code_a=15, err_code_b=16,
                                      position_a=True, position_b=True):
            if self.subtest.subtest_b_bdu(test_num=4, subtest_num=4.1, err_code_a=7, err_code_b=8,
                                          position_a=True, position_b=True):
                return True
        return False

    def st_test_42(self) -> bool:
        """
        Тест 4. Защита от потери управляемости при замыкании проводов ДУ.
        :return:
        """
        self.logger.debug("старт теста 4.2")
        self.ctrl_kl.ctrl_relay('KL11', True)
        self.logger.debug("включен KL11")
        sleep(1)
        if self.di_read_full.subtest_2di(test_num=4, subtest_num=4.2, err_code_a=9, err_code_b=10, position_a=False,
                                         position_b=False, di_a='in_a1', di_b='in_a2'):
            self.ctrl_kl.ctrl_relay('KL12', False)
            self.ctrl_kl.ctrl_relay('KL25', False)
            self.ctrl_kl.ctrl_relay('KL1', False)
            self.ctrl_kl.ctrl_relay('KL11', False)
            self.logger.debug("отключены KL12, KL25, KL1, KL11")
            return True
        return False

    def st_test_50(self) -> bool:
        """
        Тест 5. повторяем тесты 2.2 и 2.3
        :return:
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
        :return: bool
        """
        self.logger.debug("старт теста 5.2")
        self.ctrl_kl.ctrl_relay('KL12', False)
        self.logger.debug("отключен KL12")
        sleep(1)
        if self.di_read_full.subtest_2di(test_num=5, subtest_num=5.2, err_code_a=11, err_code_b=12, position_a=False,
                                         position_b=False, di_a='in_a1', di_b='in_a2'):
            return True
        return False

    def st_test_bdu_4_2(self) -> bool:
        """
        Главная функция которая собирает все остальные.
        :return: bool
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
                                            if self.st_test_52:
                                                return True
        return False


if __name__ == '__main__':
    test_bdu_4_2 = TestBDU42()
    reset_test_bdu_4_2 = ResetRelay()
    mysql_conn_test_bdu_4_2 = MySQLConnect()
    try:
        if test_bdu_4_2.st_test_bdu_4_2():
            mysql_conn_test_bdu_4_2.mysql_block_good()
            my_msg('Блок исправен', 'green')
        else:
            mysql_conn_test_bdu_4_2.mysql_block_bad()
            my_msg('Блок неисправен', 'red')
    except OSError:
        my_msg("ошибка системы", 'red')
    except SystemError:
        my_msg("внутренняя ошибка", 'red')
    except ModbusConnectException as mce:
        my_msg(f'{mce}', 'red')
    finally:
        reset_test_bdu_4_2.reset_all()
        sys.exit()
