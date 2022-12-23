#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки
Тип блока	Производитель
БКИ	нет производителя
БКИ	Углеприбор
БКИ-П	Пульсар

"""

import sys
import logging

from time import sleep

from gen_func_utils import *
from my_msgbox import *
from gen_mb_client import *
from gen_mysql_connect import *

__all__ = ["TestBKIP"]


class TestBKIP(object):

    def __init__(self):
        self.__resist = Resistor()
        self.__ctrl_kl = CtrlKL()
        self.__read_mb = ReadMB()
        self.__mysql_conn = MySQLConnect()
        self.__fault = Bug(True)

        self.msg_1 = 'Переведите тумблер на блоке в режим «Предупредительный»'
        self.msg_2 = 'Переведите тумблер на блоке в режим «Аварийный»'

        logging.basicConfig(filename="C:\Stend\project_class\TestBKIP.log",
                            filemode="w",
                            level=logging.DEBUG,
                            encoding="utf-8",
                            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('WARNING')
        self.logger = logging.getLogger(__name__)

    def st_test_1_bki_p(self):
        """
        Тест 1. Проверка исходного состояния блока
        """
        self.__fault.debug_msg('тест 1.0', 'blue')
        in_a0, in_a1 = self.__inputs_a()
        if in_a0 is True and in_a1 is False:
            pass
        elif in_a0 is False or in_a1 is True:
            self.__mysql_conn.mysql_ins_result("неисправен", "1")
            self.__mysql_conn.mysql_error(30)
            return False
        self.__mysql_conn.mysql_ins_result("исправен", "1")
        return True

    def st_test_20_bki_p(self) -> bool:
        """
        Тест 2. Проверка работы блока при нормальном сопротивлении изоляции
        """
        self.__fault.debug_msg('тест 2.0', 'blue')
        if my_msg(self.msg_1):
            pass
        else:
            return False
        self.__ctrl_kl.ctrl_relay('KL21', True)
        sleep(2)
        self.__resist.resist_kohm(220)
        sleep(2)
        in_a0, in_a1 = self.__inputs_a()
        if in_a0 is True and in_a1 is False:
            pass
        elif in_a0 is False or in_a1 is True:
            self.__mysql_conn.mysql_ins_result("неисправен", "2")
            self.__mysql_conn.mysql_error(31)
            return False
        self.__mysql_conn.mysql_ins_result("исправен", "2")
        return True

    def st_test_30_bki_p(self) -> bool:
        """
        Тест 3. Проверка работы блока в режиме «Предупредительный» при снижении
        уровня сопротивлении изоляции до 100 кОм
        """
        self.__fault.debug_msg('тест 3.0', 'blue')
        self.__resist.resist_220_to_100_kohm()
        b = self.__ctrl_kl.ctrl_ai_code_100()
        i = 0
        while b == 2 or i <= 10:
            sleep(0.2)
            i += 1
            b = self.__ctrl_kl.ctrl_ai_code_100()
            if b == 0:
                break
            elif b == 1:
                self.__mysql_conn.mysql_error(32)
                return False
        self.__mysql_conn.mysql_ins_result("исправен", "3")
        return True

    def st_test_40_bki_p(self) -> bool:
        """
        Тест 4. Проверка работы блока в режиме «Аварийный» при сопротивлении изоляции 100 кОм
        """
        self.__fault.debug_msg('тест 4.0', 'blue')
        if my_msg(self.msg_2):
            pass
        else:
            return False
        sleep(2)
        in_a0, in_a1 = self.__inputs_a()
        if in_a0 is True and in_a1 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", "4")
            self.__mysql_conn.mysql_error(33)
            self.__ctrl_kl.ctrl_relay('KL21', False)
            return False
        self.__mysql_conn.mysql_ins_result("исправен", "4")
        return True

    def st_test_50_bki_p(self) -> bool:
        """
        Тест 5. Работа блока в режиме «Аварийный» при сопротивлении изоляции
        ниже 30 кОм (Подключение на внутреннее сопротивление)
        """
        self.__fault.debug_msg('тест 5.0', 'blue')
        self.__ctrl_kl.ctrl_relay('KL22', True)
        sleep(1)
        in_a0, in_a1 = self.__inputs_a()
        if in_a0 is False and in_a1 is True:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", "5")
            self.__mysql_conn.mysql_error(34)
            return False
        self.__ctrl_kl.ctrl_relay('KL21', False)
        self.__mysql_conn.mysql_ins_result("исправен", "5")
        return True

    def __inputs_a(self):
        in_a0 = self.__read_mb.read_discrete(0)
        in_a1 = self.__read_mb.read_discrete(1)
        if in_a0 is None or in_a1 is None:
            raise ModbusConnectException('нет связи с контроллером')
        return in_a0, in_a1

    def st_test_bki_p(self) -> bool:
        if self.st_test_1_bki_p():
            if self.st_test_20_bki_p():
                if self.st_test_30_bki_p():
                    if self.st_test_40_bki_p():
                        if self.st_test_50_bki_p():
                            return True
        return False


if __name__ == '__main__':
    test_bki_p = TestBKIP()
    reset_test_bki_p = ResetRelay()
    mysql_conn_bki_p = MySQLConnect()
    fault = Bug(True)
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
        fault.debug_msg(mce, 'red')
        my_msg(f'{mce}', 'red')
    finally:
        reset_test_bki_p.reset_all()
        sys.exit()
