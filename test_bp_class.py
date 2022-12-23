#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки

Тип блока	Производитель
БП	Строй-энергомаш
БП	ТЭТЗ-Инвест
БП	нет производителя
"""

import math
import sys
import logging

from time import sleep

from my_msgbox import *
from gen_func_utils import *
from gen_mb_client import *
from gen_mysql_connect import *

__all__ = ["TestBP"]


class TestBP(object):

    def __init__(self):
        self.__mb_ctrl = CtrlKL()
        self.__read_mb = ReadMB()
        self.__mysql_conn = MySQLConnect()
        self.__fault = Bug(True)

        self.emkost_kond: float = 0.0
        self.emkost_kond_d: float = 0.0

        self.msg_1 = "Убедитесь в отсутствии других блоков и вставьте блок БП в соответствующий разъем"

        logging.basicConfig(filename="C:\Stend\project_class\TestBP.log",
                            filemode="w",
                            level=logging.DEBUG,
                            encoding="utf-8",
                            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('WARNING')
        self.logger = logging.getLogger(__name__)

    def st_test_10_bp(self) -> bool:
        """
        Тест 1. Проверка исходного состояния блока:
        Переключение АЦП на AI.1 канал
        """
        self.__inputs_a0()
        if my_msg(self.msg_1):
            pass
        else:
            return False
        self.__mysql_conn.mysql_ins_result("идёт тест 1", "1")
        self.__fault.debug_msg("тест 1", 'blue')
        self.__mb_ctrl.ctrl_relay('KL78', True)
        in_a1, in_a2, in_a6, in_a7 = self.__inputs_a()
        self.__fault.debug_msg(f'{in_a1=}\t{in_a2=}\t{in_a6=}\t{in_a7=}', 'purple')
        if in_a6 is True and in_a1 is False and in_a7 is True and in_a2 is False:
            pass
        else:
            self.__fault.debug_msg("тест 1 положение выходов не соответствует", 'red')
            self.__mysql_conn.mysql_ins_result("неисправен", "1")
            return False
        self.__fault.debug_msg("тест 1 положение выходов соответствует", 'green')
        self.__mysql_conn.mysql_ins_result("исправен", "1")
        return True

    def st_test_20_bp(self) -> bool:
        """
        Тест 2. Определение ёмкости пусковых конденсаторов
        2.1. Заряд конденсаторов
        """
        self.__mysql_conn.mysql_ins_result("идёт тест 2.1", "2")
        self.__fault.debug_msg("тест 2", 'blue')
        self.__mb_ctrl.ctrl_relay('KL77', True)
        sleep(0.3)
        self.__mb_ctrl.ctrl_relay('KL65', True)
        sleep(0.3)
        self.__mb_ctrl.ctrl_relay('KL66', True)
        sleep(5)
        self.__mb_ctrl.ctrl_relay('KL76', True)
        sleep(5)
        zaryad_1 = self.__read_mb.read_analog_ai2()
        self.__fault.debug_msg(f'заряд конденсатора по истечении 5с:\t{zaryad_1} В', 'orange')
        if zaryad_1 != 999:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", "2")
            self.__fault.debug_msg("тест 2 не пройден", 'red')
            return False
        sleep(15)
        zaryad_2 = self.__read_mb.read_analog_ai2()
        self.__fault.debug_msg(f'заряд конденсатора по истечении 15с:\t{zaryad_2} В', 'orange')
        if zaryad_2 != 999:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", "2")
            self.__fault.debug_msg("тест 2 не пройден", 'red')
            return False
        delta_zaryad = zaryad_1 - zaryad_2
        self.__fault.debug_msg(f'дельта заряда конденсатора:\t{delta_zaryad} В', 'orange')
        if delta_zaryad != 0:
            pass
        else:
            self.__mb_ctrl.ctrl_relay('KL77', False)
            sleep(0.1)
            self.__mb_ctrl.ctrl_relay('KL65', False)
            sleep(0.1)
            self.__mb_ctrl.ctrl_relay('KL76', False)
            self.__mb_ctrl.ctrl_relay('KL66', False)
            self.__mb_ctrl.ctrl_relay('KL78', False)
            self.__mysql_conn.mysql_ins_result("неисправен", "2")
            self.__fault.debug_msg("тест 2 не пройден", 'red')
            return False
        self.emkost_kond = math.log(zaryad_1 / zaryad_2)
        self.__fault.debug_msg(f'ёмкость:\t{self.emkost_kond:.2f}', 'orange')
        self.emkost_kond = (15000 / self.emkost_kond / 31300) * 1000
        self.__fault.debug_msg(f'ёмкость:\t{self.emkost_kond:.2f}', 'orange')
        self.emkost_kond_d = 100 - 100 * (self.emkost_kond / 2000)
        self.__fault.debug_msg(f'ёмкость:\t{self.emkost_kond_d:.2f}', 'orange')
        if self.emkost_kond >= 1600:
            pass
        else:
            self.__mb_ctrl.ctrl_relay('KL77', False)
            sleep(0.1)
            self.__mb_ctrl.ctrl_relay('KL65', False)
            sleep(0.1)
            self.__mb_ctrl.ctrl_relay('KL76', False)
            self.__mb_ctrl.ctrl_relay('KL66', False)
            self.__mb_ctrl.ctrl_relay('KL78', False)
            self.__mysql_conn.mysql_ins_result(f'неиспр. емкость снижена на {self.emkost_kond_d:.1f} %', "2")
            self.__fault.debug_msg("тест 2 не пройден", 'red')
            return False
        # 2.3. Форсированный разряд
        self.__mysql_conn.mysql_ins_result("идёт тест 2.3", "2")
        self.__fault.debug_msg("тест 2.3", 'blue')
        self.__mb_ctrl.ctrl_relay('KL79', True)
        sleep(1)
        self.__mb_ctrl.ctrl_relay('KL79', False)
        sleep(0.3)
        self.__mysql_conn.mysql_ins_result("исправен", "2")
        self.__mysql_conn.mysql_ins_result(f'{self.emkost_kond:.1f}', "3")
        self.__mysql_conn.mysql_ins_result(f'{self.emkost_kond_d:.1f}', "4")
        return True

    def st_test_30_bp(self) -> bool:
        """
        Тест 3. Проверка работоспособности реле удержания
        """
        self.__mysql_conn.mysql_ins_result("идёт тест 3", "5")
        self.__fault.debug_msg("тест 3", 'blue')
        self.__mb_ctrl.ctrl_relay('KL75', True)
        sleep(0.3)
        in_a1, in_a2, in_a6, in_a7 = self.__inputs_a()
        self.__fault.debug_msg(f'{in_a1=}\t{in_a2=}\t{in_a6=}\t{in_a7=}', 'purple')
        if in_a6 is False and in_a1 is True and in_a7 is False and in_a2 is True:
            pass
        else:
            self.__fault.debug_msg("тест 3 положение выходов не соответствует", 'red')
            self.__mb_ctrl.ctrl_relay('KL77', False)
            sleep(0.1)
            self.__mb_ctrl.ctrl_relay('KL65', False)
            sleep(0.1)
            self.__mb_ctrl.ctrl_relay('KL76', False)
            self.__mb_ctrl.ctrl_relay('KL66', False)
            self.__mb_ctrl.ctrl_relay('KL78', False)
            self.__mb_ctrl.ctrl_relay('KL75', False)
            self.__mysql_conn.mysql_ins_result("неисправен", "5")
            self.__fault.debug_msg("тест 3 не пройден", 'red')
            return False
        self.__fault.debug_msg("тест 3 положение выходов соответствует", 'green')
        self.__mysql_conn.mysql_ins_result("исправен", "5")
        return True

    def st_test_40_bp(self) -> bool:
        """
        Тест 4. Проверка работоспособности реле удержания
        """
        self.__mysql_conn.mysql_ins_result("идёт тест 4", "6")
        self.__fault.debug_msg("тест 4", 'blue')
        meas_volt = self.__read_mb.read_analog_ai2()
        calc_volt = meas_volt * (103 / 3)
        self.__fault.debug_msg(f'вычисленное напряжение, должно быть больше 6\t{calc_volt:.2f}', 'orange')
        if calc_volt >= 6:
            pass
        else:
            self.__mb_ctrl.ctrl_relay('KL77', False)
            sleep(0.1)
            self.__mb_ctrl.ctrl_relay('KL65', False)
            sleep(0.1)
            self.__mb_ctrl.ctrl_relay('KL75', False)
            self.__mb_ctrl.ctrl_relay('KL76', False)
            self.__mb_ctrl.ctrl_relay('KL66', False)
            self.__mb_ctrl.ctrl_relay('KL78', False)
            self.__mysql_conn.mysql_ins_result("неисправен", "6")
            self.__fault.debug_msg("тест 4 не пройден", 'red')
            return False
        self.__mb_ctrl.ctrl_relay('KL77', False)
        sleep(0.1)
        self.__mb_ctrl.ctrl_relay('KL65', False)
        sleep(0.1)
        self.__mb_ctrl.ctrl_relay('KL75', False)
        self.__mb_ctrl.ctrl_relay('KL76', False)
        self.__mb_ctrl.ctrl_relay('KL66', False)
        self.__mb_ctrl.ctrl_relay('KL78', False)
        self.__mysql_conn.mysql_ins_result("исправен", "6")
        self.__fault.debug_msg("тест 4 пройден", 'green')
        return True

    def __inputs_a0(self):
        in_a0 = self.__read_mb.read_discrete(0)
        if in_a0 is None:
            # logging.error(f'нет связи с контроллером')
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_a0

    def __inputs_a(self):
        in_a1 = self.__read_mb.read_discrete(1)
        in_a2 = self.__read_mb.read_discrete(2)
        in_a6 = self.__read_mb.read_discrete(6)
        in_a7 = self.__read_mb.read_discrete(7)
        if in_a1 is None or in_a2 is None or in_a6 is None or in_a7 is None:
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_a1, in_a2, in_a6, in_a7

    def st_test_bp(self) -> bool:
        if self.st_test_10_bp():
            if self.st_test_20_bp():
                if self.st_test_30_bp():
                    if self.st_test_40_bp():
                        return True
        return False


if __name__ == '__main__':
    test_bp = TestBP()
    reset_test_bp = ResetRelay()
    mysql_conn_bp = MySQLConnect()
    fault = Bug(True)
    try:
        if test_bp.st_test_bp():
            mysql_conn_bp.mysql_block_good()
            my_msg('Блок исправен', 'green')
        else:
            mysql_conn_bp.mysql_block_bad()
            my_msg('Блок неисправен', 'red')
    except OSError:
        my_msg("ошибка системы", 'red')
    except SystemError:
        my_msg("внутренняя ошибка", 'red')
    except ModbusConnectException as mce:
        fault.debug_msg(mce, 'red')
        my_msg(f'{mce}', 'red')
    finally:
        reset_test_bp.reset_all()
        sys.exit()
