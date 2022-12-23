#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки
Тип блока Производитель
БУ ПМВИР (пускатель)	Без Производителя

"""

import sys
import logging

from time import sleep

from gen_func_utils import *
from my_msgbox import *
from gen_mb_client import *
from gen_mysql_connect import *

__all__ = ["TestBUPMVIR"]


class TestBUPMVIR(object):

    def __init__(self):
        self.__resist = Resistor()
        self.__read_mb = ReadMB()
        self.__ctrl_kl = CtrlKL()
        self.__mysql_conn = MySQLConnect()
        self.__fault = Bug(True)

        logging.basicConfig(filename="C:\Stend\project_class\TestBUPMVIR.log",
                            filemode="w",
                            level=logging.DEBUG,
                            encoding="utf-8",
                            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('WARNING')
        self.logger = logging.getLogger(__name__)

    def st_test_10_bu_pmvir(self) -> bool:
        """
        Тест 1. Проверка исходного состояния блока:
        """
        in_a1 = self.__inputs_a()
        self.__fault.debug_msg(f'Тест 1.0 {in_a1 = } (False)', 'blue')
        if in_a1 is False:
            pass
        else:
            self.__mysql_conn.mysql_error(89)
            self.__mysql_conn.mysql_ins_result("неисправен", '1')
        # 1.1. Проверка состояния контактов блока при подаче напряжения питания
        self.__ctrl_kl.ctrl_relay('KL21', True)
        in_a1 = self.__inputs_a()
        self.__fault.debug_msg(f'Тест 1.1 {in_a1 = } (False)', 'blue')
        if in_a1 is False:
            pass
        else:
            self.__mysql_conn.mysql_error(90)
            self.__mysql_conn.mysql_ins_result("неисправен", '1')
            return False
        self.__mysql_conn.mysql_ins_result("исправен", '1')
        return True

    def st_test_20_bu_pmvir(self) -> bool:
        """
        2. Проверка включения/выключения блока от кнопки «Пуск/Стоп».
        2.1. Проверка исходного состояния блока
        """
        if self.__subtest_21():
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", '2')
            return False
        # 2.2. Выключение блока от кнопки «Стоп» при сопротивлении 10 Ом
        self.__ctrl_kl.ctrl_relay('KL12', False)
        sleep(2)
        in_a1 = self.__inputs_a()
        self.__fault.debug_msg(f'Тест 2.2 {in_a1 = } (False)', 'blue')
        if in_a1 is False:
            pass
        else:
            self.__mysql_conn.mysql_error(92)
            self.__mysql_conn.mysql_ins_result("неисправен", '2')
            return False
        self.__mysql_conn.mysql_ins_result("исправен", '2')
        return True

    def st_test_30_bu_pmvir(self) -> bool:
        """
        3. Проверка блокировки включения блока при снижении сопротивления изоляции контролируемого присоединения:
        """
        self.__ctrl_kl.ctrl_relay('KL22', True)
        self.__resist.resist_ohm(10)
        sleep(2)
        self.__ctrl_kl.ctrl_relay('KL12', True)
        sleep(2)
        in_a1 = self.__inputs_a()
        self.__fault.debug_msg(f'Тест 3.0 {in_a1 = } (False)', 'blue')
        if in_a1 is False:
            pass
        else:
            self.__mysql_conn.mysql_error(93)
            self.__mysql_conn.mysql_ins_result("неисправен", '3')
            return False
        self.__ctrl_kl.ctrl_relay('KL22', False)
        self.__ctrl_kl.ctrl_relay('KL12', False)
        self.__mysql_conn.mysql_ins_result("исправен", '3')
        return True

    def st_test_40_bu_pmvir(self) -> bool:
        """
        4.  Отключение блока при увеличении сопротивления цепи заземления на величину более 100 Ом
        """
        if self.__subtest_21():
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", '4')
            return False
        self.__resist.resist_10_to_137_ohm()
        sleep(2)
        in_a1 = self.__inputs_a()
        self.__fault.debug_msg(f'Тест 4.0 {in_a1 = } (False)', 'blue')
        if in_a1 is False:
            pass
        else:
            self.__mysql_conn.mysql_error(94)
            self.__mysql_conn.mysql_ins_result("неисправен", '4')
            return False
        self.__ctrl_kl.ctrl_relay('KL12', False)
        self.__mysql_conn.mysql_ins_result("исправен", '4')
        return True

    def st_test_50_bu_pmvir(self) -> bool:
        """
        Тест 5. Защита от потери управляемости блока при замыкании проводов ДУ
        """
        if self.__subtest_21():
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", '5')
            return False
        self.__ctrl_kl.ctrl_relay('KL11', True)
        sleep(1)
        in_a1 = self.__inputs_a()
        self.__fault.debug_msg(f'Тест 5.0 {in_a1 = } (False)', 'blue')
        if in_a1 is False:
            pass
        else:
            self.__mysql_conn.mysql_error(95)
            self.__mysql_conn.mysql_ins_result("неисправен", '5')
            return False
        self.__ctrl_kl.ctrl_relay('KL12', False)
        self.__ctrl_kl.ctrl_relay('KL11', False)
        self.__mysql_conn.mysql_ins_result("исправен", '5')
        return True

    def st_test_60_bu_pmvir(self) -> bool:
        """
        Тест 6. Защита от потери управляемости блока при обрыве проводов ДУ
        """
        if self.__subtest_21():
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", '6')
            return False
        self.__ctrl_kl.ctrl_relay('KL12', False)
        sleep(1)
        in_a1 = self.__inputs_a()
        self.__fault.debug_msg(f'Тест 6.0 {in_a1 = } (False)', 'blue')
        if in_a1 is False:
            pass
        else:
            self.__mysql_conn.mysql_error(96)
            self.__mysql_conn.mysql_ins_result("неисправен", '6')
            return False
        self.__mysql_conn.mysql_ins_result("исправен", '6')
        return True

    def st_test_70_bu_pmvir(self) -> bool:
        """
        7. Проверка отключения блока от срабатывания защиты УМЗ.
        """
        if self.__subtest_21():
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", '7')
            return False
        self.__ctrl_kl.ctrl_relay('KL27', False)
        self.__ctrl_kl.ctrl_relay('KL30', True)
        sleep(2)
        self.__ctrl_kl.ctrl_relay('KL27', True)
        sleep(6)
        in_a1 = self.__inputs_a()
        self.__fault.debug_msg(f'Тест 7.0 {in_a1 = } (False)', 'blue')
        if in_a1 is False:
            pass
        else:
            self.__mysql_conn.mysql_error(97)
            self.__mysql_conn.mysql_ins_result("неисправен", '7')
            return False
        self.__ctrl_kl.ctrl_relay('KL30', False)
        sleep(6)
        in_a1 = self.__inputs_a()
        self.__fault.debug_msg(f'Тест 7.1 {in_a1 = } (True)', 'blue')
        if in_a1 is True:
            pass
        else:
            self.__mysql_conn.mysql_error(98)
            self.__mysql_conn.mysql_ins_result("неисправен", '7')
            return False
        self.__mysql_conn.mysql_ins_result("исправен", '7')
        return True

    def __subtest_21(self) -> bool:
        """
        2.1. Включение блока от кнопки «Пуск» при сопротивлении 10 Ом
        """
        self.__resist.resist_ohm(10)
        sleep(1)
        self.__ctrl_kl.ctrl_relay('KL12', True)
        sleep(3)
        in_a1 = self.__inputs_a()
        self.__fault.debug_msg(f'Тест 2.1 {in_a1 = } (True)', 'blue')
        if in_a1 is True:
            return True
        else:
            self.__mysql_conn.mysql_error(91)
            return False

    def __inputs_a(self):
        in_a1 = self.__read_mb.read_discrete(1)
        if in_a1 is None:
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_a1

    def st_test_bu_pmvir(self) -> bool:
        if self.st_test_10_bu_pmvir():
            if self.st_test_20_bu_pmvir():
                if self.st_test_30_bu_pmvir():
                    if self.st_test_40_bu_pmvir():
                        if self.st_test_50_bu_pmvir():
                            if self.st_test_60_bu_pmvir():
                                if self.st_test_70_bu_pmvir():
                                    return True
        return False


if __name__ == '__main__':
    test_bu_pmvir = TestBUPMVIR()
    reset_test_bu_pmvir = ResetRelay()
    mysql_conn_bu_pmvir = MySQLConnect()
    fault = Bug(True)
    try:
        if test_bu_pmvir.st_test_bu_pmvir():
            mysql_conn_bu_pmvir.mysql_block_good()
            my_msg('Блок исправен', 'green')
        else:
            mysql_conn_bu_pmvir.mysql_block_bad()
            my_msg('Блок неисправен', 'red')
    except OSError:
        my_msg("ошибка системы", 'red')
    except SystemError:
        my_msg("внутренняя ошибка", 'red')
    except ModbusConnectException as mce:
        fault.debug_msg(mce, 'red')
        my_msg(f'{mce}', 'red')
    finally:
        reset_test_bu_pmvir.reset_all()
        sys.exit()
