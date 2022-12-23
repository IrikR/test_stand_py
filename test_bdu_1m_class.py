#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тип блока     Производитель
БДУ-1М  Нет производителя
БДУ-1М  Пульсар
"""

import sys
import logging

from time import sleep

from gen_func_utils import *
from my_msgbox import *
from gen_mb_client import *
from gen_mysql_connect import *

__all__ = ["TestBDU1M"]


class TestBDU1M(object):

    def __init__(self):
        self.__resist = Resistor()
        self.__ctrl_kl = CtrlKL()
        self.__read_mb = ReadMB()
        self.__mysql_conn = MySQLConnect()
        self.__fault = Bug(True)

        logging.basicConfig(filename="C:\Stend\project_class\TestBDU1M.log",
                            filemode="w",
                            level=logging.DEBUG,
                            encoding="utf-8",
                            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('WARNING')
        self.logger = logging.getLogger(__name__)

    def st_test_1_bdu_1m(self) -> bool:
        """
            Тест 1. Проверка исходного состояния блока
        """
        self.__mysql_conn.mysql_ins_result("идёт тест 1", '1')
        in_a1, in_a2 = self.__inputs_a()
        self.__fault.debug_msg(f'{in_a2 = }', 'blue')
        if in_a2 is False:
            pass
        else:
            self.__fault.debug_msg('тест 1 положение выходов не соответствует', 'red')
            self.__mysql_conn.mysql_ins_result("неисправен", '1')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(198)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(199)
            return False
        self.__fault.debug_msg('тест 1 положение выходов соответствует', 'green')
        self.__mysql_conn.mysql_ins_result("исправен", '1')
        return True

    def st_test_20_bdu_1m(self) -> bool:
        """
            Тест 2. Проверка включения / выключения блока от кнопки «Пуск / Стоп».
        """
        self.__mysql_conn.mysql_ins_result("идёт тест 2.1", '2')
        self.__ctrl_kl.ctrl_relay('KL22', True)
        sleep(1)
        self.__ctrl_kl.ctrl_relay('KL21', True)
        sleep(1)
        self.__ctrl_kl.ctrl_relay('KL2', True)
        sleep(1)
        self.__ctrl_kl.ctrl_relay('KL33', True)
        sleep(1)
        self.__ctrl_kl.ctrl_relay('KL32', True)
        sleep(1)
        in_a1, in_a2 = self.__inputs_a()
        if in_a2 is False:
            pass
        else:
            self.__fault.debug_msg('тест 2.1 положение выходов не соответствует', 'red')
            self.__mysql_conn.mysql_ins_result("неисправен", '2')
            if in_a1 is False:
                self.__mysql_conn.mysql_error(200)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(201)
            return False
        self.__fault.debug_msg('тест 2.1 положение выходов соответствует', 'green')
        return True

    def st_test_22_bdu_1m(self) -> bool:
        """
            2.2. Включение блока от кнопки «Пуск»
            2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        """
        if self.__subtest_22(2.1, 2):
            if self.__subtest_23(2.2, 2):
                return True
        return False

    def st_test_24_bdu_1m(self) -> bool:
        """
            2.4. Выключение блока от кнопки «Стоп»
        """
        self.__mysql_conn.mysql_ins_result("идёт тест 2.3", '2')
        self.__ctrl_kl.ctrl_relay('KL12', False)
        sleep(2)
        in_a1, in_a2 = self.__inputs_a()
        if in_a2 is False:
            pass
        else:
            self.__fault.debug_msg('тест 2.4 положение выходов не соответствует', 'red')
            self.__mysql_conn.mysql_ins_result("неисправен", '2')
            if in_a1 is False:
                self.__mysql_conn.mysql_error(206)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(207)
            return False
        self.__fault.debug_msg('тест 2.4 положение выходов соответствует', 'green')
        self.__ctrl_kl.ctrl_relay('KL25', False)
        self.__ctrl_kl.ctrl_relay('KL1', False)
        self.__ctrl_kl.ctrl_relay('KL22', True)
        self.__mysql_conn.mysql_ins_result("исправен", '2')
        return True

    def st_test_30_bdu_1m(self) -> bool:
        """
            3. подготовительные операции (повторение тестов 2.2 и 2.3)
        """
        if self.__subtest_22(3.1, 3):
            if self.__subtest_23(3.2, 3):
                return True
        return False

    def st_test_31_bdu_1m(self) -> bool:
        """
            3. Удержание исполнительного элемента при увеличении сопротивления цепи заземления до 50 Ом
        """
        self.__mysql_conn.mysql_ins_result("идёт тест 3.3", '3')
        self.__resist.resist_10_to_20_ohm()
        sleep(3)
        in_a1, in_a2 = self.__inputs_a()
        if in_a2 is True:
            pass
        else:
            self.__fault.debug_msg('тест 3.2 положение выходов не соответствует', 'red')
            self.__mysql_conn.mysql_ins_result("неисправен", '3')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(208)
            elif in_a2 is False:
                self.__mysql_conn.mysql_error(209)
            return False
        self.__fault.debug_msg('тест 3.2 положение выходов соответствует', 'green')
        self.__mysql_conn.mysql_ins_result("исправен", '3')
        return True

    def st_test_40_bdu_1m(self) -> bool:
        """
            Тест 4. подготовительные операции (повторение тестов 2.2 и 2.3)
        """
        if self.__subtest_22(4.1, 4):
            if self.__subtest_23(4.2, 4):
                return True
        return False

    def st_test_41_bdu_1m(self) -> bool:
        """
            Тест 4. Отключение исполнительного элемента при увеличении сопротивления
            цепи заземления на величину свыше 50 Ом
        """
        self.__mysql_conn.mysql_ins_result("идёт тест 4.3", '4')
        self.__resist.resist_10_to_100_ohm()
        sleep(2)
        in_a1, in_a2 = self.__inputs_a()
        if in_a2 is False:
            pass
        else:
            self.__fault.debug_msg('тест 4.3 положение выходов не соответствует', 'red')
            self.__mysql_conn.mysql_ins_result("неисправен", '4')
            if in_a1 is False:
                self.__mysql_conn.mysql_error(210)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(211)
            return False
        self.__fault.debug_msg('тест 4.3 положение выходов соответствует', 'green')
        self.__ctrl_kl.ctrl_relay('KL12', False)
        self.__ctrl_kl.ctrl_relay('KL25', False)
        self.__mysql_conn.mysql_ins_result("исправен", '4')
        return True

    def st_test_50_bdu_1m(self) -> bool:
        """
            Тест 5. подготовительные операции (повторение тестов 2.2 и 2.3)
        """
        if self.__subtest_22(5.1, 5):
            if self.__subtest_23(5.2, 5):
                return True
        return False

    def st_test_51_bdu_1m(self) -> bool:
        """
            5. Защита от потери управляемости при замыкании проводов ДУ
        """
        self.__mysql_conn.mysql_ins_result("идёт тест 5.3", '5')
        self.__ctrl_kl.ctrl_relay('KL11', True)
        sleep(2)
        in_a1, in_a2 = self.__inputs_a()
        if in_a2 is False:
            pass
        else:
            self.__fault.debug_msg('тест 5.3 положение выходов не соответствует', 'red')
            self.__mysql_conn.mysql_ins_result("неисправен", '5')
            if in_a1 is False:
                self.__mysql_conn.mysql_error(212)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(213)
            return False
        self.__fault.debug_msg('тест 5.2 положение выходов соответствует', 'green')
        self.__ctrl_kl.ctrl_relay('KL12', False)
        self.__ctrl_kl.ctrl_relay('KL1', False)
        self.__ctrl_kl.ctrl_relay('KL25', False)
        self.__ctrl_kl.ctrl_relay('KL11', False)
        self.__mysql_conn.mysql_ins_result("исправен", '5')
        return True

    def st_test_60_bdu_1m(self) -> bool:
        """
            Тест 6. Защита от потери управляемости при обрыве проводов ДУ
        """
        if self.__subtest_22(6.1, 6):
            if self.__subtest_23(6.2, 6):
                return True
        return False

    def st_test_61_bdu_1m(self) -> bool:
        self.__mysql_conn.mysql_ins_result("идёт тест 6.3", '6')
        self.__ctrl_kl.ctrl_relay('KL12', False)
        sleep(2)
        in_a1, in_a2 = self.__inputs_a()
        if in_a2 is False:
            pass
        else:
            self.__fault.debug_msg('тест 6.2 положение выходов не соответствует', 'red')
            self.__mysql_conn.mysql_ins_result("неисправен", '6')
            if in_a1 is False:
                self.__mysql_conn.mysql_error(214)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(215)
            return False
        self.__fault.debug_msg('тест 6.2 положение выходов соответствует', 'green')
        self.__mysql_conn.mysql_ins_result("исправен", '6')
        return True
    
    def __subtest_22(self, subtest_2_num: float, test_2_num: int) -> bool:
        """
            2.2. Включение блока от кнопки «Пуск»
        """
        self.__mysql_conn.mysql_ins_result(f'идёт тест {subtest_2_num}', f'{test_2_num}')
        self.__ctrl_kl.ctrl_relay('KL22', True)
        self.__ctrl_kl.ctrl_relay('KL1', False)
        self.__ctrl_kl.ctrl_relay('KL25', False)
        sleep(1)
        self.__resist.resist_ohm(10)
        sleep(1)
        self.__ctrl_kl.ctrl_relay('KL12', True)
        sleep(1)
        in_a1, in_a2 = self.__inputs_a()
        if in_a2 is True:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", f'{test_2_num}')
            self.__fault.debug_msg(f'тест {subtest_2_num} положение выходов не соответствует', 'red')
            if in_a1 is False:
                self.__mysql_conn.mysql_error(202)
            elif in_a2 is False:
                self.__mysql_conn.mysql_error(203)
            return False
        self.__fault.debug_msg(f'тест {subtest_2_num} положение выходов соответствует', 'green')
        return True

    def __subtest_23(self, subtest_3_num: float, test_3_num: int) -> bool:
        """
            2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        """
        self.__mysql_conn.mysql_ins_result(f'идёт тест {subtest_3_num}', f'{test_3_num}')
        self.__ctrl_kl.ctrl_relay('KL1', True)
        self.__ctrl_kl.ctrl_relay('KL22', False)
        sleep(1)
        self.__ctrl_kl.ctrl_relay('KL25', True)
        sleep(1)
        in_a1, in_a2 = self.__inputs_a()
        if in_a2 is True:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", f'{test_3_num}')
            self.__fault.debug_msg(f'тест {subtest_3_num} положение выходов не соответствует', 'red')
            if in_a1 is False:
                self.__mysql_conn.mysql_error(204)
            elif in_a2 is False:
                self.__mysql_conn.mysql_error(205)
            return False
        self.__fault.debug_msg(f'тест {subtest_3_num} положение выходов соответствует', 'green')
        return True
    
    def __inputs_a(self):
        in_a1 = self.__read_mb.read_discrete(1)
        in_a2 = self.__read_mb.read_discrete(2)
        if in_a1 is None or in_a2 is None:
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_a1, in_a2

    def st_test_bdu_1m(self):
        """
            главная функция которая собирает все остальные
        """
        if self.st_test_1_bdu_1m():
            if self.st_test_20_bdu_1m():
                if self.st_test_22_bdu_1m():
                    if self.st_test_24_bdu_1m():
                        if self.st_test_30_bdu_1m():
                            if self.st_test_31_bdu_1m():
                                if self.st_test_40_bdu_1m():
                                    if self.st_test_41_bdu_1m():
                                        if self.st_test_50_bdu_1m():
                                            if self.st_test_51_bdu_1m():
                                                if self.st_test_60_bdu_1m():
                                                    if self.st_test_61_bdu_1m():
                                                        return True
        return False


if __name__ == '__main__':
    test_bdu_1m = TestBDU1M()
    mysql_conn_test_bdu_1m = MySQLConnect()
    reset_test_bdu_1m = ResetRelay()
    fault = Bug(True)
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
        fault.debug_msg(mce, 'red')
        my_msg(f'{mce}', 'red')
    finally:
        reset_test_bdu_1m.reset_all()
        sys.exit()
