#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки
Тип блока Производитель
БДУ-4-2	  Нет производителя
БДУ-4-2	  ДонЭнергоЗавод
БДУ-4-2	  ИТЭП

"""

import sys
import logging

from time import sleep

from gen_func_utils import *
from my_msgbox import *
from gen_mb_client import *
from gen_mysql_connect import *

__all__ = ["TestBDU42"]


class TestBDU42(object):

    def __init__(self):
        self.__resist = Resistor()
        self.__ctrl_kl = CtrlKL()
        self.__read_mb = ReadMB()
        self.__mysql_conn = MySQLConnect()
        self.__fault = Bug(True)

        logging.basicConfig(filename="C:\Stend\project_class\TestBDU42.log",
                            filemode="w",
                            level=logging.DEBUG,
                            encoding="utf-8",
                            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('WARNING')
        self.logger = logging.getLogger(__name__)

    def st_test_1_bdu_4_2(self) -> bool:
        """
            Тест 1. Проверка исходного состояния блока:
        """
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is False and in_a2 is False:
            pass
        else:
            self.__fault.debug_msg('тест 1 не пройден', 1)
            self.__mysql_conn.mysql_ins_result("неисправен", '1')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(5)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(6)
            return False
        self.__fault.debug_msg('тест 1 пройден', 4)
        self.__mysql_conn.mysql_ins_result("исправен", '1')
        return True

    def st_test_20_bdu_4_2(self) -> bool:
        """
            Тест 2. Проверка включения выключения блока от кнопки «Пуск Стоп».
            2.1. Проверка исходного состояния блока
        """
        self.__ctrl_kl.ctrl_relay('KL2', True)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is False and in_a2 is False:
            pass
        else:
            self.__fault.debug_msg('тест 2.1 не пройден', 1)
            self.__mysql_conn.mysql_ins_result("неисправен", '2')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(13)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(14)
            return False
        self.__fault.debug_msg('тест 2.1 пройден', 4)
        return True

    def st_test_21_bdu_4_2(self) -> bool:
        """
            2.2. Включение блока от кнопки «Пуск»
            2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        """

        if self.__subtest_22(2.2, 2):
            if self.__subtest_23(2.3, 2):
                return True
        return False

    def st_test_22_bdu_4_2(self) -> bool:
        """
            2.4. Выключение блока от кнопки «Стоп»
        """
        self.__ctrl_kl.ctrl_relay('KL12', False)
        sleep(2)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is False and in_a2 is False:
            pass
        else:
            self.__fault.debug_msg('тест 2.4 не пройден', 'red')
            self.__mysql_conn.mysql_ins_result("неисправен", '2')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(17)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(18)
            return False
        self.__fault.debug_msg('тест 2.4 пройден', 'green')
        self.__ctrl_kl.ctrl_relay('KL25', False)
        self.__ctrl_kl.ctrl_relay('KL1', False)
        self.__mysql_conn.mysql_ins_result("исправен", '2')
        return True

    def st_test_30_bdu_4_2(self) -> bool:
        """
            тест 3. повторяем тесты 2.2 и 2.3
        """
        self.__fault.debug_msg('тест 3.1 начат', 'blue')
        if self.__subtest_22(3.1, 3):
            if self.__subtest_23(3.2, 3):
                return True
        return False

    def st_test_31_bdu_4_2(self) -> bool:
        """
            3. Отключение исполнительного элемента при увеличении сопротивления цепи заземления
        """
        self.__fault.debug_msg('тест 3.2 начат', 'blue')
        self.__resist.resist_10_to_110_ohm()
        sleep(1)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is False and in_a2 is False:
            pass
        else:
            self.__fault.debug_msg('тест 3 не пройден', 1)
            self.__mysql_conn.mysql_ins_result("неисправен", '3')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(19)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(20)
            return False
        self.__fault.debug_msg('тест 3 пройден', 4)
        self.__ctrl_kl.ctrl_relay('KL12', False)
        self.__ctrl_kl.ctrl_relay('KL25', False)
        self.__ctrl_kl.ctrl_relay('KL1', False)
        self.__mysql_conn.mysql_ins_result("исправен", '3')
        return True

    def st_test_40_bdu_4_2(self) -> bool:
        """
            Тест 4. повторяем тесты 2.2 и 2.3
        """
        self.__fault.debug_msg('тест 4.1 начат', 'blue')
        if self.__subtest_22(4.1, 4):
            if self.__subtest_23(4.2, 4):
                return True
        return False

    def st_test_41_bdu_4_2(self) -> bool:
        """
            Тест 4. Защита от потери управляемости при замыкании проводов ДУ
        """
        self.__fault.debug_msg('тест 4.2 начат', 'blue')
        self.__ctrl_kl.ctrl_relay('KL11', True)
        sleep(1)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is False and in_a2 is False:
            pass
        else:
            self.__fault.debug_msg('тест 4 не пройден', 1)
            self.__mysql_conn.mysql_ins_result("неисправен", '4')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(9)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(10)
            return False
        self.__fault.debug_msg('тест 4 пройден', 4)
        self.__ctrl_kl.ctrl_relay('KL12', False)
        self.__ctrl_kl.ctrl_relay('KL25', False)
        self.__ctrl_kl.ctrl_relay('KL1', False)
        self.__ctrl_kl.ctrl_relay('KL11', False)
        self.__mysql_conn.mysql_ins_result("исправен", '4')
        return True

    def st_test_50_bdu_4_2(self) -> bool:
        """
            Тест 5. повторяем тесты 2.2 и 2.3
        """
        self.__fault.debug_msg('тест 5.1 начат', 'blue')
        if self.__subtest_22(5.1, 5):
            if self.__subtest_23(5.2, 5):
                return True
        return False

    def st_test_51_bdu_4_2(self) -> bool:
        """
            Тест 5. Защита от потери управляемости при обрыве проводов ДУ
        """
        self.__fault.debug_msg('тест 5.2 начат', 'blue')
        self.__ctrl_kl.ctrl_relay('KL12', False)
        sleep(1)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is False and in_a2 is False:
            pass
        else:
            self.__fault.debug_msg('тест 5 не пройден', 1)
            self.__mysql_conn.mysql_ins_result("неисправен", '5')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(11)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(12)
            return False
        self.__fault.debug_msg('тест 5 пройден', 4)
        self.__mysql_conn.mysql_ins_result("исправен", '5')
        return True

    def __subtest_22(self, subtest_2_num: float, test_2_num: int) -> bool:
        """
            2.2. Включение блока от кнопки «Пуск»
        """
        self.__fault.debug_msg(f'тест {subtest_2_num} начат', 'blue')
        self.__mysql_conn.mysql_ins_result(f'идёт тест {subtest_2_num}', f'{test_2_num}')
        self.__resist.resist_ohm(255)
        self.__resist.resist_ohm(10)
        sleep(1)
        self.__ctrl_kl.ctrl_relay('KL12', True)
        sleep(2)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is True and in_a2 is True:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", f'{test_2_num}')
            self.__fault.debug_msg(f'тест {subtest_2_num} положение выходов не соответствует', 'red')
            if in_a1 is False:
                self.__mysql_conn.mysql_error(15)
            elif in_a2 is False:
                self.__mysql_conn.mysql_error(16)
            return False
        self.__fault.debug_msg(f'тест {subtest_2_num} положение выходов соответствует', 'green')
        return True

    def __subtest_23(self, subtest_3_num: float, test_3_num: int) -> bool:
        """
            2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        """
        self.__fault.debug_msg(f'тест {subtest_3_num} начат', 'blue')
        self.__mysql_conn.mysql_ins_result(f'идёт тест {subtest_3_num}', f'{test_3_num}')
        self.__ctrl_kl.ctrl_relay('KL1', True)
        self.__ctrl_kl.ctrl_relay('KL25', True)
        sleep(2)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is True and in_a2 is True:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", f'{test_3_num}')
            self.__fault.debug_msg(f'тест {subtest_3_num} положение выходов не соответствует', 'red')
            if in_a1 is False:
                self.__mysql_conn.mysql_error(7)
            elif in_a2 is False:
                self.__mysql_conn.mysql_error(8)
            return False
        self.__fault.debug_msg(f'тест {subtest_3_num} положение выходов соответствует', 'green')
        return True

    def __inputs_a(self):
        in_a1 = self.__read_mb.read_discrete(1)
        in_a2 = self.__read_mb.read_discrete(2)
        if in_a1 is None or in_a2 is None:
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_a1, in_a2

    def st_test_bdu_4_2(self) -> bool:
        """
            главная функция которая собирает все остальные
        """
        if self.st_test_1_bdu_4_2():
            if self.st_test_20_bdu_4_2():
                if self.st_test_21_bdu_4_2():
                    if self.st_test_22_bdu_4_2():
                        if self.st_test_30_bdu_4_2():
                            if self.st_test_31_bdu_4_2():
                                if self.st_test_40_bdu_4_2():
                                    if self.st_test_41_bdu_4_2():
                                        if self.st_test_50_bdu_4_2():
                                            if self.st_test_51_bdu_4_2():
                                                return True
        return False


if __name__ == '__main__':
    test_bdu_4_2 = TestBDU42()
    reset_test_bdu_4_2 = ResetRelay()
    mysql_conn_test_bdu_4_2 = MySQLConnect()
    fault = Bug(True)
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
        fault.debug_msg(mce, 'red')
        my_msg(f'{mce}', 'red')
    finally:
        reset_test_bdu_4_2.reset_all()
        sys.exit()
