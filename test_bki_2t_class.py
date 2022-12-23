#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки
Тип блока Производитель
БКИ-2Т	нет производителя	52
БКИ-2Т	ТЭТЗ-Инвест	53
БКИ-2Т	Строй-энерго	54

"""

import sys
import logging

from time import sleep

from gen_func_utils import *
from my_msgbox import *
from gen_mb_client import *
from gen_mysql_connect import *

__all__ = ["TestBKI2T"]


class TestBKI2T(object):

    def __init__(self):
        self.__resist = Resistor()
        self.__ctrl_kl = CtrlKL()
        self.__read_mb = ReadMB()
        self.__mysql_conn = MySQLConnect()
        self.__fault = Bug(True)

        logging.basicConfig(filename="C:\Stend\project_class\TestBKI2T.log",
                            filemode="w",
                            level=logging.DEBUG,
                            encoding="utf-8",
                            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('WARNING')
        self.logger = logging.getLogger(__name__)

    def st_test_1_bki_2t(self) -> bool:
        """
        Тест 1. Проверка исходного состояния блока:
        """
        self.__mysql_conn.mysql_ins_result("идет тест 1", "1")
        in_a1, in_a2, in_a5, in_a6 = self.__inputs_a()
        if in_a5 is True and in_a1 is False and in_a6 is True and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", "1")
            self.__fault.debug_msg('тест 1 не пройден', 1)
            if in_a5 is False or in_a1 is True:
                self.__mysql_conn.mysql_error(35)
            elif in_a6 is False or in_a2 is True:
                self.__mysql_conn.mysql_error(36)
            return False
        self.__fault.debug_msg('тест 1 пройден', 3)
        self.__mysql_conn.mysql_ins_result("исправен", '1')
        return True

    def st_test_20_bki_2t(self) -> bool:
        """
        Тест 2. Проверка работы блока при подаче питания и при
        нормальном сопротивлении изоляции контролируемого присоединения
        """
        self.__mysql_conn.mysql_ins_result("идет тест 2.1", "2")
        self.__ctrl_kl.ctrl_relay('KL21', True)
        sleep(5)
        if self.__subtest_21(2.2, 2):
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", '2')
            return False
        self.__mysql_conn.mysql_ins_result("исправен", '2')
        return True

    def st_test_30_bki_2t(self) -> bool:
        """
        Тест 3. Проверка работы 1 канала (К1) блока при снижении
        уровня сопротивлении изоляции ниже 30 кОм в цепи 1 канала
        """
        self.__mysql_conn.mysql_ins_result("идет тест 3", "3")
        self.__ctrl_kl.ctrl_relay('KL31', True)
        self.__resist.resist_kohm(12)
        sleep(1)
        in_a1, in_a2, in_a5, in_a6 = self.__inputs_a()
        if in_a5 is False and in_a1 is True and in_a6 is True and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", '3')
            if in_a5 is True or in_a1 is False:
                self.__mysql_conn.mysql_error(39)
            elif in_a6 is False or in_a2 is True:
                self.__mysql_conn.mysql_error(40)
            return False
        self.__resist.resist_kohm(590)
        self.__mysql_conn.mysql_ins_result("исправен", '3')
        return True

    def st_test_40_bki_2t(self) -> bool:
        """
        Тест 4. Проверка работы 1 канала (К1) блока от кнопки «Проверка БКИ» в цепи 1 канала
        """
        if self.__subtest_21(4.1, 4):
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", '4')
            return False
        self.__ctrl_kl.ctrl_relay('KL23', True)
        self.__ctrl_kl.ctrl_relay('KL22', True)
        sleep(1)
        in_a1, in_a2, in_a5, in_a6 = self.__inputs_a()
        if in_a5 is False and in_a1 is True and in_a6 is True and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", '4')
            if in_a5 is True or in_a1 is False:
                self.__mysql_conn.mysql_error(41)
            elif in_a6 is False or in_a2 is True:
                self.__mysql_conn.mysql_error(42)
            return False
        self.__resist.resist_kohm(590)
        self.__ctrl_kl.ctrl_relay('KL22', False)
        self.__mysql_conn.mysql_ins_result("исправен", '4')
        return True

    def st_test_50_bki_2t(self) -> bool:
        """
        Тест 5. Проверка работы 2 канала (К2) блока при снижении уровня
        сопротивлении изоляции ниже 30 кОм в цепи 2 канала
        """
        self.__mysql_conn.mysql_ins_result("идет тест 5", "5")
        self.__ctrl_kl.ctrl_relay('KL31', False)
        sleep(1)
        self.__resist.resist_kohm(12)
        sleep(1)
        in_a1, in_a2, in_a5, in_a6 = self.__inputs_a()
        if in_a5 is True and in_a1 is False and in_a6 is False and in_a2 is True:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", '5')
            if in_a5 is False or in_a1 is True:
                self.__mysql_conn.mysql_error(43)
            elif in_a6 is True or in_a2 is False:
                self.__mysql_conn.mysql_error(44)
            return False
        self.__resist.resist_kohm(590)
        self.__mysql_conn.mysql_ins_result("исправен", '5')
        return True

    def st_test_60_bki_2t(self) -> bool:
        """
        Тест 6. Проверка работы 2 канала (К2) блока от кнопки «Проверка БКИ» в цепи 2 канала
        """
        if self.__subtest_21(6.1, 6):
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", '6')
        self.__ctrl_kl.ctrl_relay('KL22', True)
        sleep(1)
        in_a1, in_a2, in_a5, in_a6 = self.__inputs_a()
        if in_a5 is True and in_a1 is False and in_a6 is False and in_a2 is True:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", '6')
            if in_a5 is False or in_a1 is True:
                self.__mysql_conn.mysql_error(45)
            elif in_a6 is True or in_a2 is False:
                self.__mysql_conn.mysql_error(46)
            return False
        self.__mysql_conn.mysql_ins_result("исправен", '6')
        return True

    def __subtest_21(self, subtest_2_num: float, test_2_num: int) -> bool:
        self.__mysql_conn.mysql_ins_result(f'идёт тест {subtest_2_num}', f'{test_2_num}')
        in_a1, in_a2, in_a5, in_a6 = self.__inputs_a()
        if in_a5 is True and in_a1 is False and in_a6 is True and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", f'{test_2_num}')
            self.__fault.debug_msg(f'тест {subtest_2_num} положение выходов не соответствует', 1)
            if in_a5 is False or in_a1 is True:
                self.__mysql_conn.mysql_error(37)
            elif in_a6 is False or in_a2 is True:
                self.__mysql_conn.mysql_error(38)
            return False
        self.__fault.debug_msg(f'тест {subtest_2_num} положение выходов соответствует', 4)
        return True

    def __inputs_a(self):
        in_a1 = self.__read_mb.read_discrete(1)
        in_a2 = self.__read_mb.read_discrete(2)
        in_a5 = self.__read_mb.read_discrete(5)
        in_a6 = self.__read_mb.read_discrete(6)
        if in_a1 is None or in_a2 is None or in_a5 is None or in_a6 is None:
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_a1, in_a2, in_a5, in_a6

    def st_test_bki_2t(self) -> bool:
        if self.st_test_1_bki_2t():
            if self.st_test_20_bki_2t():
                if self.st_test_30_bki_2t():
                    if self.st_test_40_bki_2t():
                        if self.st_test_50_bki_2t():
                            if self.st_test_60_bki_2t():
                                return True
        return False


if __name__ == '__main__':
    test_bki_2t = TestBKI2T()
    reset_test_bki_2t = ResetRelay()
    mysql_conn_bki_2t = MySQLConnect()
    fault = Bug(True)
    try:
        if test_bki_2t.st_test_bki_2t():
            mysql_conn_bki_2t.mysql_block_good()
            my_msg('Блок исправен', 'green')
        else:
            mysql_conn_bki_2t.mysql_block_bad()
            my_msg('Блок неисправен', 'red')
    except OSError:
        my_msg("ошибка системы", 'red')
    except SystemError:
        my_msg("внутренняя ошибка", 'red')
    except ModbusConnectException as mce:
        fault.debug_msg(mce, 'red')
        my_msg(f'{mce}', 'red')
    finally:
        reset_test_bki_2t.reset_all()
        sys.exit()
