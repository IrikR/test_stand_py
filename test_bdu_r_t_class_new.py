#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тип блока: БДУ-Р-Т
Производитель: Нет производителя, ТЭТЗ-Инвест, Стройэнергомаш

"""

import sys
import logging

from time import sleep

from general_func.exception import *
from general_func.subtest import Subtest2in, ReadOPCServer
from general_func.database import *
from general_func.modbus import *
from general_func.resistance import Resistor
from general_func.reset import ResetRelay
from gui.msgbox_1 import *

__all__ = ["TestBDURT"]


class TestBDURT:

    def __init__(self):
        self.resist = Resistor()
        self.ctrl_kl = CtrlKL()
        self.mysql_conn = MySQLConnect()
        self.subtest = Subtest2in()
        self.di_read_full = ReadOPCServer()

        logging.basicConfig(
            filename="C:\\Stend\\project_class\\log\\TestBDURT.log",
            filemode="w",
            level=logging.DEBUG,
            encoding="utf-8",
            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('DEBUG')
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))

    def st_test_1(self) -> bool:
        if self.di_read_full.subtest_2di(test_num=1, subtest_num=1.0, err_code_a=288, err_code_b=288, position_a=False,
                                         position_b=False):
            return True
        return False

    def st_test_20(self) -> bool:
        """
        Тест 2. Проверка включения/выключения блока от кнопки «Пуск/Стоп» в режиме «Вперед».
        """
        self.logger.debug("старт теста 2.0")
        self.ctrl_kl.ctrl_relay('KL2', True)
        self.logger.debug("включен KL2")
        sleep(1)
        if self.di_read_full.subtest_2di(test_num=2, subtest_num=2.0, err_code_a=290, err_code_b=291, position_a=False,
                                         position_b=False):
            return True
        return False

    def st_test_21(self) -> bool:
        """
        2.2. Включение блока от кнопки «Пуск» в режиме «Вперёд»
        2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        """
        if self.subtest.subtest_a_bdu(test_num=2, subtest_num=2.1, err_code_a=292, err_code_b=293,
                                      position_a=True, position_b=False):
            if self.subtest.subtest_b_bdu(test_num=2, subtest_num=2.2, err_code_a=294, err_code_b=295,
                                          position_a=True, position_b=False):
                return True
        return False

    def st_test_23(self) -> bool:
        """
        2.4. Выключение блока в режиме «Вперед» от кнопки «Стоп»
        """
        self.logger.debug("старт теста 2.3")
        self.ctrl_kl.ctrl_relay('KL12', False)
        self.logger.debug(' включен KL12')
        sleep(1)
        if self.di_read_full.subtest_2di(test_num=2, subtest_num=2.3, err_code_a=296, err_code_b=297, position_a=False,
                                         position_b=False):
            self.ctrl_kl.ctrl_relay('KL25', False)
            self.ctrl_kl.ctrl_relay('KL1', False)
            self.logger.debug(' отключены KL25, KL1')
            return True
        return False

    def st_test_30(self) -> bool:
        """
        Тест 3. Проверка включения/выключения блока от кнопки «Пуск/Стоп» в режиме «Назад»
        3.1. Включение блока от кнопки «Пуск» в режиме «Назад»
        """
        self.logger.debug("старт теста 3.0")
        self.ctrl_kl.ctrl_relay('KL26', True)
        self.logger.debug(' включен KL26')
        self.resist.resist_ohm(10)
        self.ctrl_kl.ctrl_relay('KL12', True)
        self.logger.debug(' включен KL12')
        sleep(1)
        if self.di_read_full.subtest_2di(test_num=3, subtest_num=3.0, err_code_a=298, err_code_b=299, position_a=False,
                                         position_b=True):
            return True
        return False

    def st_test_31(self) -> bool:
        """
        3.2. Проверка удержания контактов К5.2 режима «Назад» блока во включенном состоянии
        при подключении Rш пульта управления:
        """
        self.logger.debug("старт теста 3.1")
        self.ctrl_kl.ctrl_relay('KL27', True)
        self.ctrl_kl.ctrl_relay('KL1', True)
        self.ctrl_kl.ctrl_relay('KL25', True)
        self.logger.debug(' включены KL27, KL25, KL1')
        sleep(1)
        if self.di_read_full.subtest_2di(test_num=3, subtest_num=3.1, err_code_a=300, err_code_b=301, position_a=True,
                                         position_b=False):
            return True
        return False

    def st_test_32(self) -> bool:
        """
        3.3. Выключение блока в режиме «Вперед» от кнопки «Стоп»
        """
        self.logger.debug("старт теста 3.2")
        self.ctrl_kl.ctrl_relay('KL12', False)
        self.logger.debug(' отключен KL12')
        sleep(1)
        if self.di_read_full.subtest_2di(test_num=3, subtest_num=3.2, err_code_a=302, err_code_b=303, position_a=False,
                                         position_b=False):
            self.ctrl_kl.ctrl_relay('KL26', False)
            self.ctrl_kl.ctrl_relay('KL27', False)
            self.ctrl_kl.ctrl_relay('KL1', False)
            self.ctrl_kl.ctrl_relay('KL25', False)
            self.logger.debug(' отключены KL26, KL27, KL1, KL25')
            return True
        return False

    def st_test_40(self) -> bool:
        """
        Повторяем тест 2.2. Включение блока от кнопки «Пуск» в режиме «Вперёд»
        Повторяем тест 2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        """
        if self.subtest.subtest_a_bdu(test_num=4, subtest_num=4.0, err_code_a=292, err_code_b=293,
                                      position_a=True, position_b=False):
            if self.subtest.subtest_b_bdu(test_num=4, subtest_num=4.1, err_code_a=294, err_code_b=295,
                                          position_a=True, position_b=False):
                return True
        return False

    def st_test_42(self) -> bool:
        """
        # 4. Отключение исполнительного элемента при увеличении сопротивления цепи заземления на величину свыше 50 Ом
        """
        self.logger.debug("старт теста 4.2")
        self.resist.resist_10_to_50_ohm()
        sleep(1)
        if self.di_read_full.subtest_2di(test_num=4, subtest_num=4.2, err_code_a=304, err_code_b=305, position_a=False,
                                         position_b=False):
            self.ctrl_kl.ctrl_relay('KL12', False)
            self.ctrl_kl.ctrl_relay('KL25', False)
            self.ctrl_kl.ctrl_relay('KL1', False)
            self.logger.debug(' отключены KL12, KL25, KL1')
            return True
        return False

    def st_test_50(self) -> bool:
        """
        Повторяем тест 2.2. Включение блока от кнопки «Пуск» в режиме «Вперёд»
        Повторяем тест 2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        """
        if self.subtest.subtest_a_bdu(test_num=5, subtest_num=5.0, err_code_a=292, err_code_b=293,
                                      position_a=True, position_b=False):
            if self.subtest.subtest_b_bdu(test_num=5, subtest_num=5.1, err_code_a=294, err_code_b=295,
                                          position_a=True, position_b=False):
                return True
        return False

    def st_test_52(self) -> bool:
        """
        # 5. Защита от потери управляемости при замыкании проводов ДУ
        """
        self.logger.debug("старт теста 5.2")
        self.ctrl_kl.ctrl_relay('KL11', True)
        self.logger.debug(' включен KL11')
        sleep(1)
        if self.di_read_full.subtest_2di(test_num=5, subtest_num=5.2, err_code_a=306, err_code_b=307, position_a=False,
                                         position_b=False):
            self.ctrl_kl.ctrl_relay('KL12', False)
            self.ctrl_kl.ctrl_relay('KL1', False)
            self.ctrl_kl.ctrl_relay('KL25', False)
            self.ctrl_kl.ctrl_relay('KL11', False)
            self.logger.debug(' отключены KL12, KL1, KL25, KL11')
            return True
        return False

    def st_test_60(self) -> bool:
        """
        Повторяем тест 2.2. Включение блока от кнопки «Пуск» в режиме «Вперёд»
        Повторяем тест 2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        """
        if self.subtest.subtest_a_bdu(test_num=6, subtest_num=6.0, err_code_a=292, err_code_b=293,
                                      position_a=True, position_b=False):
            if self.subtest.subtest_b_bdu(test_num=6, subtest_num=6.1, err_code_a=294, err_code_b=295,
                                          position_a=True, position_b=False):
                return True
        return False

    def st_test_62(self) -> bool:
        """
        # Тест 6. Защита от потери управляемости при обрыве проводов ДУ
        """
        self.logger.debug("старт теста 6.2")
        self.ctrl_kl.ctrl_relay('KL12', False)
        self.logger.debug(' отключен KL12')
        sleep(1)
        if self.di_read_full.subtest_2di(test_num=6, subtest_num=6.2, err_code_a=308, err_code_b=309, position_a=False,
                                         position_b=False):
            return True
        return False

    def st_test_70(self) -> bool:
        """
        # Тест 7. Проверка работоспособности функции "Проверка" блока
        """
        self.logger.debug("старт теста 7.0")
        self.ctrl_kl.ctrl_relay('KL24', True)
        self.logger.debug(' включен KL24')
        sleep(1)
        if self.di_read_full.subtest_2di(test_num=7, subtest_num=7.0, err_code_a=310, err_code_b=311, position_a=False,
                                         position_b=True):
            return True
        return False

    def st_test_bdu_r_t(self) -> bool:
        """
        Главная функция которая собирает все остальные
        """
        if self.st_test_1():
            if self.st_test_20():
                if self.st_test_21():
                    if self.st_test_23():
                        if self.st_test_30():
                            if self.st_test_31():
                                if self.st_test_32():
                                    if self.st_test_40():
                                        if self.st_test_42():
                                            if self.st_test_50():
                                                if self.st_test_52():
                                                    if self.st_test_60():
                                                        if self.st_test_62():
                                                            if self.st_test_70():
                                                                return True
        return False


if __name__ == '__main__':
    test_bdu_r_t = TestBDURT()
    reset_test_bdu_r_t = ResetRelay()
    mysql_conn_bdu_r_t = MySQLConnect()
    try:
        if test_bdu_r_t.st_test_bdu_r_t():
            mysql_conn_bdu_r_t.mysql_block_good()
            my_msg('Блок исправен', 'green')
        else:
            mysql_conn_bdu_r_t.mysql_block_bad()
            my_msg('Блок неисправен', 'red')
    except OSError:
        my_msg("ошибка системы", 'red')
    except SystemError:
        my_msg("внутренняя ошибка", 'red')
    except ModbusConnectException as mce:
        my_msg(f'{mce}', 'red')
    finally:
        reset_test_bdu_r_t.reset_all()
        sys.exit()
