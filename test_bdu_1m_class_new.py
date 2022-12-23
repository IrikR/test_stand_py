#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки
Тип блока: БДУ-1М
Производитель: Пульсар, Нет производителя
"""

import sys
import logging

from time import sleep

from general_func.exception import *
from general_func.subtest import ReadOPCServer, SubtestBDU1M
from general_func.database import *
from general_func.modbus import *
from general_func.resistance import Resistor
from general_func.reset import ResetRelay
from gui.msgbox_1 import *

__all__ = ["TestBDU1M"]


class TestBDU1M:

    def __init__(self):
        self.resist = Resistor()
        self.ctrl_kl = CtrlKL()
        self.mysql_conn = MySQLConnect()
        self.subtest = SubtestBDU1M()
        self.di_read_full = ReadOPCServer()
        # C:\Stend\project_class
        logging.basicConfig(
            filename="C:\\Stend\\project_class\\log\\TestBDU1M.log",
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
        if self.di_read_full.subtest_1di(test_num=1, subtest_num=1.0, err_code=199, position=False, di_a='in_a2'):
            return True
        return False

    def st_test_20(self) -> bool:
        """
            Тест 2. Проверка включения / выключения блока от кнопки «Пуск / Стоп».
        """
        self.ctrl_kl.ctrl_relay('KL22', True)
        sleep(1)
        self.ctrl_kl.ctrl_relay('KL21', True)
        sleep(1)
        self.ctrl_kl.ctrl_relay('KL2', True)
        sleep(1)
        self.ctrl_kl.ctrl_relay('KL33', True)
        sleep(1)
        self.ctrl_kl.ctrl_relay('KL32', True)
        self.logger.debug("включены KL22, KL21, KL2, KL33, KL32")
        sleep(1)
        if self.di_read_full.subtest_1di(test_num=2, subtest_num=2.0, err_code=201, position=False, di_a='in_a2'):
            return True
        return False

    def st_test_21(self) -> bool:
        """
            2.2. Включение блока от кнопки «Пуск»
            2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        """
        if self.subtest.subtest_a(test_num=2, subtest_num=2.1):
            if self.subtest.subtest_b(test_num=2, subtest_num=2.2):
                return True
        return False

    def st_test_23(self) -> bool:
        """
            2.4. Выключение блока от кнопки «Стоп»
        """
        self.ctrl_kl.ctrl_relay('KL12', False)
        self.logger.debug("отключен KL12")
        sleep(2)
        if self.di_read_full.subtest_1di(test_num=2, subtest_num=2.3, err_code=207, position=False, di_a='in_a2'):
            self.ctrl_kl.ctrl_relay('KL25', False)
            self.ctrl_kl.ctrl_relay('KL1', False)
            self.ctrl_kl.ctrl_relay('KL22', True)
            self.logger.debug("отключен KL25, KL1 и включен KL22")
            return True
        return False

    def st_test_30(self) -> bool:
        """
            3. подготовительные операции (повторение тестов 2.2 и 2.3)
        """
        if self.subtest.subtest_a(test_num=3, subtest_num=3.0):
            if self.subtest.subtest_b(test_num=3, subtest_num=3.1):
                return True
        return False

    def st_test_32(self) -> bool:
        """
            3. Удержание исполнительного элемента при увеличении сопротивления цепи заземления до 50 Ом
        """
        self.resist.resist_10_to_20_ohm()
        sleep(3)
        if self.di_read_full.subtest_1di(test_num=3, subtest_num=3.2, err_code=209, position=True, di_a='in_a2'):
            return True
        return False

    def st_test_40(self) -> bool:
        """
            Тест 4. подготовительные операции (повторение тестов 2.2 и 2.3)
        """
        if self.subtest.subtest_a(test_num=4, subtest_num=4.0):
            if self.subtest.subtest_b(test_num=4, subtest_num=4.1):
                return True
        return False

    def st_test_42(self) -> bool:
        """
            Тест 4. Отключение исполнительного элемента при увеличении сопротивления
            цепи заземления на величину свыше 50 Ом
        """
        self.resist.resist_10_to_100_ohm()
        sleep(2)
        if self.di_read_full.subtest_1di(test_num=4, subtest_num=4.2, err_code=211, position=False, di_a='in_a2'):
            self.ctrl_kl.ctrl_relay('KL12', False)
            self.ctrl_kl.ctrl_relay('KL25', False)
            self.logger.debug("отключен KL12, KL25")
            return True
        return False

    def st_test_50(self) -> bool:
        """
            Тест 5. подготовительные операции (повторение тестов 2.2 и 2.3)
        """
        if self.subtest.subtest_a(test_num=5, subtest_num=5.0):
            if self.subtest.subtest_b(test_num=5, subtest_num=5.1):
                return True
        return False

    def st_test_52(self) -> bool:
        """
            Тест 5. Защита от потери управляемости при замыкании проводов ДУ
        """
        self.ctrl_kl.ctrl_relay('KL11', True)
        self.logger.debug("включен KL11")
        sleep(2)
        if self.di_read_full.subtest_1di(test_num=5, subtest_num=5.2, err_code=213, position=False, di_a='in_a2'):
            self.ctrl_kl.ctrl_relay('KL12', False)
            self.ctrl_kl.ctrl_relay('KL1', False)
            self.ctrl_kl.ctrl_relay('KL25', False)
            self.ctrl_kl.ctrl_relay('KL11', False)
            self.logger.debug("отключены KL12, KL1, KL25, KL11")
            return True
        return False

    def st_test_60(self) -> bool:
        """
            Тест 6. Защита от потери управляемости при обрыве проводов ДУ
        """
        if self.subtest.subtest_a(test_num=6, subtest_num=6.0):
            if self.subtest.subtest_b(test_num=6, subtest_num=6.1):
                return True
        return False

    def st_test_62(self) -> bool:
        self.ctrl_kl.ctrl_relay('KL12', False)
        self.logger.debug("отключен KL12")
        sleep(2)
        if self.di_read_full.subtest_1di(test_num=6, subtest_num=6.2, err_code=215, position=False, di_a='in_a2'):
            return True
        return False

    def st_test_bdu_1m(self):
        """
            Главная функция которая собирает все остальные.
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
                                                if self.st_test_60():
                                                    if self.st_test_62():
                                                        return True
        return False


if __name__ == '__main__':
    test_bdu_1m = TestBDU1M()
    mysql_conn_test_bdu_1m = MySQLConnect()
    reset_test_bdu_1m = ResetRelay()
    try:
        if test_bdu_1m.st_test_bdu_1m():
            mysql_conn_test_bdu_1m.mysql_block_good()
            my_msg('Блок исправен', 'green')
        else:
            mysql_conn_test_bdu_1m.mysql_block_bad()
            my_msg('Блок неисправен', 'red')
    except OSError:
        my_msg("ошибка системы", 'red')
    except SystemError:
        my_msg("внутренняя ошибка", 'red')
    except ModbusConnectException as mce:
        my_msg(f'{mce}', 'red')
    finally:
        reset_test_bdu_1m.reset_all()
        sys.exit()
