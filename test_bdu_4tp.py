#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тип блока     Производитель
БДУ             Без Производителя
БДУ             Углеприбор
БДУ-1           Без Производителя
БДУ-1           Углеприбор
БДУ-4           Без Производителя
БДУ-4           Углеприбор
БДУ-Т           Без Производителя
БДУ-Т           Углеприбор
БДУ-Т           ТЭТЗ-Инвест
БДУ-Т           Строй-ЭнергоМаш
БДУ-П Х5-01     Пульсар
БДУ-П УХЛ 01    Пульсар
БДУ-П УХЛ5-03   Пульсар
"""

import sys

from time import sleep

from gen_func_utils import *
from my_msgbox import *
from gen_mb_client import *
from gen_mysql_connect import *

__all__ = ["TestBDU014TP"]


class TestBDU014TP(object):

    def __init__(self):
        self.__resist = Resistor()
        self.__ctrl_kl = CtrlKL()
        self.__read_mb = ReadMB()
        self.__mysql_conn = MySQLConnect()
        self.__fault = Bug(True)

    def test_1(self) -> bool:
        """
        Тест 1. Проверка исходного состояния блока:
        :return:
        """
        self.__fault.debug_msg(f'тест 1', 'blue')
        self.__mysql_conn.mysql_ins_result("идет тест 1", "1")
        in_a0, in_a1 = self.inputs_a()
        if in_a1 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", "1")
            self.__mysql_conn.mysql_error(476)
            self.__fault.debug_msg('тест 1.0 положение выходов не соответствует', 'red')
            return False
        self.__mysql_conn.mysql_ins_result("исправен", "1")
        self.__fault.debug_msg('тест 1.0 положение выходов соответствует', 'green')
        return True

    def test_20(self) -> bool:
        """
        Тест 2. Проверка включения / выключения блока от кнопки «Пуск / Стоп».
        2.1. Проверка исходного состояния блока
        """
        self.__fault.debug_msg(f'тест 2.0', 'blue')
        self.__mysql_conn.mysql_ins_result("идет тест 2.1", "2")
        self.__ctrl_kl.ctrl_relay('KL2', True)
        sleep(1)
        in_a0, in_a1 = self.inputs_a()
        if in_a1 is False:
            self.__fault.debug_msg('тест 2.0 положение выходов соответствует', 'green')
            return True
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", "2")
            self.__fault.debug_msg('тест 2.0 положение выходов не соответствует', 'red')
            return False

    def test_21(self) -> bool:
        """
        2.2. Включение канала блока от кнопки «Пуск» при сопротивлении 10 Ом
        """
        self.__fault.debug_msg(f'тест 2.1', 'blue')
        if self.subtest_22(2.2, 2):
            return True
        return False

    def test_22(self) -> bool:
        """
        2.3. Выключение канала блока от кнопки «Пуск» при сопротивлении 10 Ом
        """
        self.__fault.debug_msg(f'тест 2.2', 'blue')
        self.__mysql_conn.mysql_ins_result("идет тест 2.3", "2")
        self.__ctrl_kl.ctrl_relay('KL12', False)
        sleep(1)
        in_a0, in_a1 = self.inputs_a()
        if in_a1 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", "2")
            self.__mysql_conn.mysql_error(27)
            self.__fault.debug_msg('тест 2.2 положение выходов не соответствует', 'red')
            return False
        self.__fault.debug_msg('тест 2.2 положение выходов соответствует', 'green')
        self.__mysql_conn.mysql_ins_result("исправен", "2")
        return True

    def test_30(self) -> bool:
        """
        повтор теста 2.2
        """
        self.__fault.debug_msg(f'тест 3.0', 'blue')
        if self.subtest_22(3.1, 3):
            return True
        return False

    def test_31(self) -> bool:
        """
        3. Удержание исполнительного элемента при сопротивлении цепи заземления до 35 Ом
        """
        self.__fault.debug_msg(f'тест 3.1', 'blue')
        self.__resist.resist_10_to_35_ohm()
        sleep(1)
        in_a0, in_a1 = self.inputs_a()
        if in_a1 is True:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", "3")
            self.__mysql_conn.mysql_error(28)
            self.__fault.debug_msg('тест 3.1 положение выходов не соответствует', 'red')
            return False
        self.__mysql_conn.mysql_ins_result("исправен", "3")
        self.__fault.debug_msg('тест 3.1 положение выходов соответствует', 'green')
        return True

    def test_40(self) -> bool:
        """
        4. Отключение исполнительного элемента при сопротивлении цепи заземления свыше 50 Ом
        """
        self.__fault.debug_msg(f'тест 4.0', 'blue')
        self.__mysql_conn.mysql_ins_result("идет тест 4", "4")
        self.__resist.resist_35_to_110_ohm()
        sleep(1)
        in_a0, in_a1 = self.inputs_a()
        if in_a1 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", "4")
            self.__mysql_conn.mysql_error(29)
            self.__fault.debug_msg('тест 4.0 положение выходов не соответствует', 'red')
            return False
        self.__ctrl_kl.ctrl_relay('KL12', False)
        self.__ctrl_kl.ctrl_relay('KL1', False)
        self.__mysql_conn.mysql_ins_result("исправен", "4")
        self.__fault.debug_msg('тест 4.0 положение выходов соответствует', 'green')
        return True

    def test_50(self) -> bool:
        """
        повтор теста 2.2
        """
        self.__fault.debug_msg(f'тест 5.0', 'blue')
        if self.subtest_22(5.1, 5):
            return True
        return False

    def test_51(self) -> bool:
        """
        5. Защита от потери управляемости при замыкании проводов ДУ
        """
        self.__fault.debug_msg(f'тест 5.1', 'blue')
        self.__ctrl_kl.ctrl_relay('KL11', True)
        sleep(2)
        in_a0, in_a1 = self.inputs_a()
        if in_a1 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", "5")
            self.__mysql_conn.mysql_error(3)
            self.__fault.debug_msg('тест 5.1 положение выходов не соответствует', 'red')
            return False
        self.__ctrl_kl.ctrl_relay('KL12', False)
        self.__ctrl_kl.ctrl_relay('KL1', False)
        self.__ctrl_kl.ctrl_relay('KL11', False)
        self.__mysql_conn.mysql_ins_result("исправен", "5")
        self.__fault.debug_msg('тест 5.1 положение выходов соответствует', 'green')
        return True

    def test_60(self) -> bool:
        """
        повтор теста 2.2
        """
        self.__fault.debug_msg(f'тест 6.0', 'blue')
        if self.subtest_22(6.1, 6):
            return True
        return False

    def test_61(self) -> bool:
        """
        Тест 6. Защита от потери управляемости при обрыве проводов ДУ
        """
        self.__fault.debug_msg(f'тест 6.1', 'blue')
        self.__ctrl_kl.ctrl_relay('KL12', False)
        sleep(1)
        in_a0, in_a1 = self.inputs_a()
        if in_a1 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", "6")
            self.__mysql_conn.mysql_error(4)
            self.__fault.debug_msg('тест 6.1 положение выходов не соответствует', 'red')
            return False
        self.__mysql_conn.mysql_ins_result("исправен", "6")
        self.__fault.debug_msg('тест 6.1 положение выходов соответствует', 'green')
        return True

    def subtest_22(self, subtest_2_num: float, test_2_num: int) -> bool:
        self.__mysql_conn.mysql_ins_result(f'идёт тест {subtest_2_num}', f'{test_2_num}')
        self.__resist.resist_ohm(255)
        sleep(1)
        self.__resist.resist_ohm(10)
        sleep(2)
        self.__ctrl_kl.ctrl_relay('KL1', True)
        sleep(1)
        self.__ctrl_kl.ctrl_relay('KL12', True)
        sleep(1)
        in_a0, in_a1 = self.inputs_a()
        if in_a1 is True:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", f'{test_2_num}')
            self.__fault.debug_msg(f'тест {subtest_2_num} положение выходов не соответствует', 'red')
            self.__mysql_conn.mysql_error(26)
            return False
        self.__fault.debug_msg(f'тест {subtest_2_num} положение выходов соответствует', 'green')
        return True

    def inputs_a(self):
        in_a0, in_a1 = self.__read_mb.read_discrete_v1('in_a0', 'in_a1')
        self.__fault.debug_msg(f'{in_a0 = }  {in_a1 = }', 'blue')
        if in_a1 is None or in_a0 is None:
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_a0, in_a1

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
    fault = Bug(True)
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
        fault.debug_msg(mce, 'red')
        my_msg(f'{mce}', 'red')
    finally:
        reset_test_bdu_014tp.reset_all()
        sys.exit()
