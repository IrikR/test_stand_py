#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки
Тип блока Производитель
БДУ	Без Производителя
БДУ	Углеприбор

"""

import sys
import logging

from time import sleep

from gen_func_utils import *
from my_msgbox import *
from gen_mb_client import *
from gen_mysql_connect import *

__all__ = ["TestBDU"]


class TestBDU(object):

    def __init__(self):
        self.__resist = Resistor()
        self.__ctrl_kl = CtrlKL()
        self.__read_mb = ReadMB()
        self.__mysql_conn = MySQLConnect()
        self.__fault = Bug(True)

        logging.basicConfig(filename="C:\Stend\project_class\TestBDU.log",
                            filemode="w",
                            level=logging.DEBUG,
                            encoding="utf-8",
                            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('WARNING')
        self.logger = logging.getLogger(__name__)

    def st_test_1_bdu(self) -> bool:
        """
        Тест 1. проверка исходного состояния блока
        """
        in_a1 = self.__inputs_a()
        if in_a1 is False:
            pass
        else:
            self.__fault.debug_msg(f'{in_a1=} \tблок неисправен', 1)
            self.__mysql_conn.mysql_ins_result('неисправен', '1')
            return False
        self.__mysql_conn.mysql_ins_result('исправен', '1')
        self.__fault.debug_msg(f'{in_a1=} \tтест 1 пройден', 3)
        return True

    def st_test_20_bdu(self) -> bool:
        """
        Тест-2 Проверка включения/отключения блока от кнопки пуск
        """
        self.__ctrl_kl.ctrl_relay('KL2', True)
        sleep(3)
        in_a1 = self.__inputs_a()
        if in_a1 is False:
            pass
        else:
            self.__fault.debug_msg(f'{in_a1=} \tблок неисправен', 1)
            self.__mysql_conn.mysql_ins_result('неисправен', '2')
            return False
        self.__fault.debug_msg(f'{in_a1=} \tтест 2.1 пройден', 3)
        return True

    def st_test_21_bdu(self) -> bool:
        """
        Тест-2.2 Проверка канала блока от кнопки "Пуск"
        """
        self.__resist.resist_ohm(10)
        sleep(3)
        self.__ctrl_kl.ctrl_relay('KL12', True)
        sleep(3)
        in_a1 = self.__inputs_a()
        if in_a1 is True:
            pass
        else:
            self.__fault.debug_msg(f'{in_a1=} \tТест 2.2 блок неисправен', 1)
            self.__mysql_conn.mysql_ins_result('неисправен', '2')
            return False
        self.__fault.debug_msg(f'{in_a1=} \tтест 2.2 пройден', 3)
        return True

    def st_test_22_bdu(self) -> bool:
        """
        Тест 2.3 Выключение канала блока от кнопки «Пуск» при сопротивлении 10 Ом
        """
        sleep(3)
        self.__ctrl_kl.ctrl_relay('KL12', False)
        sleep(3)
        in_a1 = self.__inputs_a()
        if in_a1 is False:
            pass
        else:
            self.__fault.debug_msg(f'{in_a1=} \tТест 2.3 блок неисправен', 1)
            self.__mysql_conn.mysql_ins_result('неисправен', '2')
            return False
        self.__fault.debug_msg(f'{in_a1=} \tтест 2.3 пройден', 3)
        self.__mysql_conn.mysql_ins_result('исправен', '2')
        return True

    def st_test_30_bdu(self) -> bool:
        """
        Тест-3. Удержание исполнительного элемента при сопротивлении цепи заземления до 35 Ом
        """
        sleep(3)
        self.__ctrl_kl.ctrl_relay('KL12', True)
        sleep(0.5)
        # Отключаем KL5, KL8 для формирования 35 Ом
        self.__ctrl_kl.ctrl_relay('KL5', False)
        self.__ctrl_kl.ctrl_relay('KL8', False)
        sleep(1)
        in_a1 = self.__inputs_a()
        if in_a1 is False:
            pass
        else:
            self.__fault.debug_msg(f'{in_a1=} \tТест 3 блок неисправен', 1)
            self.__mysql_conn.mysql_ins_result('неисправен', '3')
            return False
        self.__fault.debug_msg(f'{in_a1=} \tтест 3 пройден', 3)
        self.__mysql_conn.mysql_ins_result('исправен', '3')
        return True

    def st_test_40_bdu(self) -> bool:
        """
        Тест 4. Отключение исполнительного элемента при сопротивлении цепи заземления свыше 50 Ом
        """
        self.__ctrl_kl.ctrl_relay('KL7', False)
        self.__ctrl_kl.ctrl_relay('KL9', False)
        self.__ctrl_kl.ctrl_relay('KL4', True)
        self.__ctrl_kl.ctrl_relay('KL6', True)
        self.__ctrl_kl.ctrl_relay('KL10', True)
        in_a1 = self.__inputs_a()
        if in_a1 is False:
            pass
        else:
            self.__fault.debug_msg(f'{in_a1=} \tТест 4 блок неисправен', 1)
            self.__mysql_conn.mysql_ins_result('неисправен', '4')
            return False
        self.__ctrl_kl.ctrl_relay('KL12', False)
        sleep(0.5)
        self.__fault.debug_msg(f'{in_a1=} \tтест 4 пройден', 3)
        self.__mysql_conn.mysql_ins_result('исправен', '4')
        return True

    def st_test_50_bdu(self) -> bool:
        """
        Тест 5. Защита от потери управляемости при замыкании проводов ДУ
        """
        self.__resist.resist_ohm(10)
        sleep(1)
        self.__ctrl_kl.ctrl_relay('KL12', True)
        sleep(0.5)
        self.__ctrl_kl.ctrl_relay('KL11', True)
        sleep(1)
        in_a1 = self.__inputs_a()
        if in_a1 is False:
            pass
        else:
            self.__fault.debug_msg(f'{in_a1=} \tТест 5 блок неисправен', 1)
            self.__mysql_conn.mysql_ins_result('неисправен', '5')
            return False
        self.__fault.debug_msg(f'{in_a1=} \tтест 5 пройден', 3)
        self.__mysql_conn.mysql_ins_result('исправен', '5')
        self.__ctrl_kl.ctrl_relay('KL12', False)
        self.__ctrl_kl.ctrl_relay('KL11', False)
        self.__ctrl_kl.ctrl_relay('KL1', False)
        return True

    def st_test_60_bdu(self) -> bool:
        """
        Тест 6. Защита от потери управляемости при обрыве проводов ДУ
        """
        self.__resist.resist_ohm(10)
        sleep(1)
        self.__ctrl_kl.ctrl_relay('KL12', True)
        sleep(1)
        self.__ctrl_kl.ctrl_relay('KL12', False)
        sleep(1)
        in_a1 = self.__inputs_a()
        if in_a1 is False:
            pass
        else:
            self.__fault.debug_msg(f'{in_a1=} \tТест 6 блок неисправен', 1)
            self.__mysql_conn.mysql_ins_result('неисправен', '6')
            return False
        self.__fault.debug_msg(f'{in_a1=} \tтест 6 пройден', 3)
        self.__mysql_conn.mysql_ins_result('исправен', '6')
        self.__fault.debug_msg(f'{in_a1=} \tтест завершен', 3)
        return True

    def __inputs_a(self):
        in_a1 = self.__read_mb.read_discrete(1)
        if in_a1 is None:
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_a1

    def st_test_bdu(self) -> bool:
        """
            Главная функция которая собирает все остальные
        """
        if self.st_test_1_bdu():
            if self.st_test_20_bdu():
                if self.st_test_21_bdu():
                    if self.st_test_22_bdu():
                        if self.st_test_30_bdu():
                            if self.st_test_40_bdu():
                                if self.st_test_50_bdu():
                                    if self.st_test_60_bdu():
                                        return True
        return False


if __name__ == '__main__':
    test_bdu = TestBDU()
    reset_test_bdu = ResetRelay()
    mysql_conn_test_bdu = MySQLConnect()
    fault = Bug(True)
    try:
        if test_bdu.st_test_bdu():
            mysql_conn_test_bdu.mysql_block_good()
            my_msg('Блок исправен', 'green')
        else:
            mysql_conn_test_bdu.mysql_block_bad()
            my_msg('Блок неисправен', 'red')
    except OSError:
        my_msg("ошибка системы", 'red')
    except SystemError:
        my_msg("внутренняя ошибка", 'red')
    except ModbusConnectException as mce:
        fault.debug_msg(mce, 'red')
        my_msg(f'{mce}', 'red')
    finally:
        reset_test_bdu.reset_all()
        sys.exit()
