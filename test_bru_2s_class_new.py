#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки

Тип блока: БРУ-2С
Производитель: Нет производителя

"""

import sys
import logging

from general_func.exception import *
from general_func.database import *
from general_func.modbus import *
from general_func.subtest import SubtestBDU, ReadOPCServer
from general_func.resistance import Resistor
from general_func.reset import ResetRelay
from gui.msgbox_1 import *

__all__ = ["TestBRU2S"]


class TestBRU2S:

    def __init__(self):
        self.resist = Resistor()
        self.ctrl_kl = CtrlKL()
        self.mysql_conn = MySQLConnect()
        self.sub_test = SubtestBDU()
        self.di_read_full = ReadOPCServer()

        self.msg_1 = "Переведите тумблер «П/А» на блоке в положение «П» и нажмите кнопку «ОК» " \
                     "Если на блоке нет тумблера «П/А» нажмите кнопку «Отмена»"

        logging.basicConfig(
            filename="C:\\Stend\\project_class\\log\\TestBRU2S.log",
            filemode="w",
            level=logging.DEBUG,
            encoding="utf-8",
            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('DEBUG')
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))

    def st_test_10(self) -> bool:
        """
        Тест 1. Проверка исходного состояния блока:
        :return: bool:
        """
        if self.di_read_full.subtest_1di(test_num=1, subtest_num=1.0, err_code=47):
            return True
        return False

    def st_test_20(self) -> bool:
        """
        Тест 2. Проверка включения/выключения блока от кнопки «Пуск/Стоп»
        :return: bool:
        """
        self.logger.debug(f"старт теста: 2, подтест: 0")
        self.ctrl_kl.ctrl_relay('KL21', True)
        self.logger.debug(f'включение KL21')
        if self.di_read_full.subtest_1di(test_num=2, subtest_num=2.0, err_code=48, position=False):
            return True
        return False

    def st_test_21(self) -> bool:
        """
        2.2. Включение блока от кнопки «Пуск»
        2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        :return: bool:
        """
        if self.sub_test.subtest_a_bdu43_bru2s(test_num=2, subtest_num=2.1):
            if self.sub_test.subtest_b_bru2s(test_num=2, subtest_num=2.2):
                return True
        return False

    def st_test_23(self) -> bool:
        """
        2.4. Выключение блока от кнопки «Стоп»
        :return: bool:
        """
        self.mysql_conn.mysql_add_message(f"старт теста: 2, подтест: 3")
        self.logger.debug(f"старт теста: 1, подтест: 0")
        self.ctrl_kl.ctrl_relay('KL12', False)
        self.logger.debug(f'отключение KL12')
        if self.di_read_full.subtest_1di(test_num=2, subtest_num=2.3, err_code=51, position=False):
            self.ctrl_kl.ctrl_relay('KL25', False)
            self.logger.debug(f'отключение KL25')
            return True
        return False

    def st_test_30(self) -> bool:
        """
        Повторяем подтесты 2.2. Включение блока от кнопки «Пуск»
        Повторяем подтесты 2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        :return: bool:
        """
        if self.sub_test.subtest_a_bdu43_bru2s(test_num=3, subtest_num=3.0):
            if self.sub_test.subtest_b_bru2s(test_num=3, subtest_num=3.1):
                return True
        return False

    def st_test_32(self) -> bool:
        """
        3. Отключение выходного контакта блока при увеличении сопротивления цепи заземления
        :return: bool:
        """
        self.logger.debug(f"старт теста: 3, подтест: 2")
        self.resist.resist_ohm(150)
        if self.di_read_full.subtest_1di(test_num=3, subtest_num=3.2, err_code=52, position=False):
            self.ctrl_kl.ctrl_relay('KL12', False)
            self.ctrl_kl.ctrl_relay('KL25', False)
            self.logger.debug(f'отключение KL12, KL25')
            return True
        return False

    def st_test_40(self) -> bool:
        """
        Повторяем подтесты 2.2. Включение блока от кнопки «Пуск»
        Повторяем подтесты 2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        :return: bool:
        """
        if self.sub_test.subtest_a_bdu43_bru2s(test_num=4, subtest_num=4.0):
            if self.sub_test.subtest_b_bru2s(test_num=4, subtest_num=4.1):
                return True
        return False

    def st_test_42(self) -> bool:
        """
        4. Защита от потери управляемости при замыкании проводов ДУ
        :return: bool:
        """
        self.logger.debug(f"старт теста: 4, подтест: 2")
        self.ctrl_kl.ctrl_relay('KL11', True)
        self.logger.debug(f'отключение KL11')
        if self.di_read_full.subtest_1di(test_num=4, subtest_num=4.2, err_code=53, position=False):
            self.ctrl_kl.ctrl_relay('KL12', False)
            self.ctrl_kl.ctrl_relay('KL25', False)
            self.ctrl_kl.ctrl_relay('KL11', False)
            self.logger.debug(f'отключение KL12, KL25, KL11')
            return True
        return False

    def st_test_50(self) -> bool:
        """
        Повторяем подтесты 2.2. Включение блока от кнопки «Пуск»
        Повторяем подтесты 2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        :return: bool:
        """
        if self.sub_test.subtest_a_bdu43_bru2s(test_num=5, subtest_num=5.0):
            if self.sub_test.subtest_b_bru2s(test_num=5, subtest_num=5.1):
                return True
        return False

    def st_test_52(self) -> bool:
        """
        Тест 5. Защита от потери управляемости блока при обрыве проводов ДУ
        :return: bool:
        """
        self.logger.debug(f"старт теста: 5, подтест: 2")
        self.ctrl_kl.ctrl_relay('KL12', False)
        self.logger.debug(f'отключение KL12')
        if self.di_read_full.subtest_1di(test_num=5, subtest_num=5.2, err_code=54, position=False):
            self.ctrl_kl.ctrl_relay('KL25', False)
            self.logger.debug(f'отключение KL25'
                              f'')
            return True
        return False

    def st_test_60(self) -> bool:
        """
        Тест 6.0
        :return: bool:
        """
        self.logger.debug(f"старт теста: 6, подтест: 0")
        if my_msg(self.msg_1):
            if self.subtest_6():
                self.mysql_conn.mysql_ins_result('исправен', '6')
                if self.subtest_7():
                    self.mysql_conn.mysql_ins_result('исправен', '7')
                else:
                    self.mysql_conn.mysql_ins_result('неисправен', '7')
                    return False
            else:
                self.mysql_conn.mysql_ins_result('неисправен', '6')
                return False
        else:
            if self.subtest_7():
                self.mysql_conn.mysql_ins_result('пропущен', '6')
                self.mysql_conn.mysql_ins_result('исправен', '7')
            else:
                self.mysql_conn.mysql_ins_result('пропущен', '6')
                self.mysql_conn.mysql_ins_result('неисправен', '7')
                return False
        return True

    def subtest_6(self) -> bool:
        """
        Тест 6. Блокировка включения блока при снижении сопротивления изоляции
        контролируемого присоединения до уровня предупредительной уставки.
        :return: bool
        """
        self.logger.debug(f"старт теста: 6, подтест: 1")
        self.resist.resist_kohm(200)
        self.ctrl_kl.ctrl_relay('KL12', True)
        self.logger.debug(f'включение KL12')
        if self.di_read_full.subtest_1di(test_num=6, subtest_num=6.0, err_code=55, position=False):
            self.ctrl_kl.ctrl_relay('KL12', False)
            self.logger.debug(f'отключение KL12')
            return True
        return False

    def subtest_7(self) -> bool:
        """
        Тест 7. Блокировка включения блока при снижении сопротивления изоляции
        контролируемого присоединения до уровня аварийной уставки.
        :return: bool
        """
        self.logger.debug(f"старт теста: 7, подтест: 0")
        self.resist.resist_kohm(30)
        self.ctrl_kl.ctrl_relay('KL12', True)
        self.logger.debug(f'включение KL12')
        if self.di_read_full.subtest_1di(test_num=7, subtest_num=7.0, err_code=56, position=False):
            self.ctrl_kl.ctrl_relay('KL12', False)
            self.logger.debug(f'отключение KL12')
            return True
        return False

    def st_test_bru_2s(self) -> bool:
        if self.st_test_10():
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
                                                    return True
        return False


if __name__ == '__main__':
    test_bru_2s = TestBRU2S()
    reset_test_bru_2s = ResetRelay()
    mysql_conn_bru_2s = MySQLConnect()
    try:
        if test_bru_2s.st_test_bru_2s():
            mysql_conn_bru_2s.mysql_block_good()
            my_msg('Блок исправен', 'green')
        else:
            mysql_conn_bru_2s.mysql_block_bad()
            my_msg('Блок неисправен', 'red')
    except OSError:
        my_msg("ошибка системы", 'red')
    except SystemError:
        my_msg("внутренняя ошибка", 'red')
    except ModbusConnectException as mce:
        my_msg(f'{mce}', 'red')
    finally:
        reset_test_bru_2s.reset_all()
        sys.exit()
