#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
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

import sys
import logging

from time import sleep

from general_func.exception import *
from general_func.subtest import SubtestBDU, ReadOPCServer
from general_func.database import *
from general_func.modbus import *
from general_func.resistance import Resistor
from general_func.reset import ResetRelay
from gui.msgbox_1 import *

__all__ = ["TestBDU014TP"]


class TestBDU014TP:

    def __init__(self):
        self.resist = Resistor()
        self.ctrl_kl = CtrlKL()
        self.mysql_conn = MySQLConnect()
        self.sub_test = SubtestBDU()
        self.di_read_full = ReadOPCServer()

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
        if self.di_read_full.subtest_1di(test_num=1, subtest_num=1.0, err_code=47, di_a='in_a1'):
            return True
        return False

    def test_20(self) -> bool:
        """
        Тест 2. Проверка включения / выключения блока от кнопки «Пуск / Стоп».
        2.1. Проверка исходного состояния блока
        """
        self.logger.debug(f"старт теста: 2, подтест: 0")
        self.ctrl_kl.ctrl_relay('KL2', True)
        self.logger.debug(f'включение KL2')
        sleep(1)
        if self.di_read_full.subtest_1di(test_num=2, subtest_num=2.0, err_code=21, di_a='in_a1'):
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
        self.ctrl_kl.ctrl_relay('KL12', False)
        self.logger.debug(f'отключение KL12')
        sleep(1)
        if self.di_read_full.subtest_1di(test_num=2, subtest_num=2.2, err_code=27, di_a='in_a1'):
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
        if self.di_read_full.subtest_1di(test_num=3, subtest_num=3.1, err_code=28, position=True, di_a='in_a1'):
            return True
        return False

    def test_40(self) -> bool:
        """
        4. Отключение исполнительного элемента при сопротивлении цепи заземления свыше 50 Ом
        """
        self.logger.debug(f"старт теста: 4, подтест: 0")
        self.resist.resist_35_to_110_ohm()
        sleep(1)
        if self.di_read_full.subtest_1di(test_num=4, subtest_num=4.0, err_code=29, di_a='in_a1'):
            self.ctrl_kl.ctrl_relay('KL12', False)
            self.ctrl_kl.ctrl_relay('KL1', False)
            self.logger.debug(f'отключение KL12, KL1')
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
        self.ctrl_kl.ctrl_relay('KL11', True)
        sleep(2)
        if self.di_read_full.subtest_1di(test_num=5, subtest_num=5.1, err_code=3, di_a='in_a1'):
            self.ctrl_kl.ctrl_relay('KL12', False)
            self.ctrl_kl.ctrl_relay('KL1', False)
            self.ctrl_kl.ctrl_relay('KL11', False)
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
        self.ctrl_kl.ctrl_relay('KL12', False)
        self.logger.debug(f'отключение KL12')
        sleep(1)
        if self.di_read_full.subtest_1di(test_num=6, subtest_num=6.1, err_code=4, position=False, di_a='in_a1'):
            return True
        return False

    def st_test_bdu_014tp(self) -> bool:
        """
            Главная функция которая собирает все остальные
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


if __name__ == '__main__':
    test_bdu_014tp = TestBDU014TP()
    reset_test_bdu_014tp = ResetRelay()
    mysql_conn_test_bdu_014tp = MySQLConnect()
    try:
        if test_bdu_014tp.st_test_bdu_014tp():
            mysql_conn_test_bdu_014tp.mysql_block_good()
            my_msg('Блок исправен', 'green')
        else:
            mysql_conn_test_bdu_014tp.mysql_block_bad()
            my_msg('Блок неисправен', 'red')
    except OSError:
        my_msg("ошибка системы", 'red')
    except SystemError:
        my_msg("внутренняя ошибка", 'red')
    except ModbusConnectException as mce:
        my_msg(f'{mce}', 'red')
    finally:
        reset_test_bdu_014tp.reset_all()
        sys.exit()
