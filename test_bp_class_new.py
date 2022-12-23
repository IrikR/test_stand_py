#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки

Тип блока: БП
Производитель: Строй-энергомаш, ТЭТЗ-Инвест, нет производителя
"""

import logging
import math
import sys
from time import sleep

from general_func.database import *
from general_func.exception import *
from general_func.modbus import *
from general_func.reset import ResetRelay, ResetProtection
from general_func.subtest import ReadOPCServer
from gui.msgbox_1 import *

__all__ = ["TestBP"]


class TestBP:
    """
    capacitor capacitance - емкость конденсатора
    charge - заряд
    """

    def __init__(self):
        self.mb_ctrl = CtrlKL()
        self.ai_read = AIRead()
        self.di_read = DIRead()
        self.reset_relay = ResetRelay()
        self.reset_protect = ResetProtection()
        self.mysql_conn = MySQLConnect()
        self.di_read_full = ReadOPCServer()

        self.capacitor_capacitance: float = 0.0
        self.capacitor_capacitance_d: float = 0.0

        self.msg_1 = "Убедитесь в отсутствии других блоков и вставьте блок БП в соответствующий разъем"

        logging.basicConfig(
            filename="C:\\Stend\\project_class\\log\\TestBP.log",
            filemode="w",
            level=logging.DEBUG,
            encoding="utf-8",
            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('WARNING')
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))

    def st_test_10(self) -> bool:
        """
        Тест 1. Проверка исходного состояния блока:
        Переключение АЦП на AI.1 канал
        """
        self.logger.debug("старт теста 1.0")
        in_a0, *_ = self.di_read.di_read('in_a0')
        if my_msg(self.msg_1):
            pass
        else:
            return False
        self.mysql_conn.mysql_ins_result("идёт тест 1", "1")
        self.mb_ctrl.ctrl_relay('KL78', True)
        if self.di_read_full.subtest_4di(test_num=1, subtest_num=1.0,
                                         err_code_a=344, err_code_b=344, err_code_c=344, err_code_d=344,
                                         position_a=True, position_b=False, position_c=True, position_d=False,
                                         di_a='in_a6', di_b='in_a1', di_c='in_a7', di_d='in_a2'):
            return True
        return False

    def st_test_20(self) -> bool:
        """
        Тест 2. Определение ёмкости пусковых конденсаторов
        2.1. Заряд конденсаторов
        """
        self.logger.debug("старт теста 2.0")
        self.mysql_conn.mysql_ins_result("идёт тест 2.1", "2")
        self.mb_ctrl.ctrl_relay('KL77', True)
        sleep(0.3)
        self.mb_ctrl.ctrl_relay('KL65', True)
        sleep(0.3)
        self.mb_ctrl.ctrl_relay('KL66', True)
        sleep(5)
        self.mb_ctrl.ctrl_relay('KL76', True)
        sleep(5)
        charge_1 = self.ai_read.ai_read('AI2')
        self.logger.info(f'заряд конденсатора по истечении 5с:\t{charge_1} В')
        if charge_1 != 999:
            pass
        else:
            self.mysql_conn.mysql_ins_result("неисправен", "2")
            return False
        sleep(15)
        charge_2 = self.ai_read.ai_read('AI2')
        self.logger.info(f'заряд конденсатора по истечении 15с:\t{charge_2} В')
        if charge_2 != 999:
            pass
        else:
            self.mysql_conn.mysql_ins_result("неисправен", "2")
            return False
        delta_charge = charge_1 - charge_2
        self.logger.info(f'дельта заряда конденсатора:\t{delta_charge} В')
        if delta_charge != 0:
            pass
        else:
            self.reset_protect.sbros_testa_bp_0()
            self.mysql_conn.mysql_ins_result("неисправен", "2")
            return False
        self.capacitor_capacitance = math.log(charge_1 / charge_2)
        self.logger.info(f'ёмкость:\t{self.capacitor_capacitance:.2f}')
        self.capacitor_capacitance = (15000 / self.capacitor_capacitance / 31300) * 1000
        self.logger.info(f'ёмкость:\t{self.capacitor_capacitance:.2f}')
        self.capacitor_capacitance_d = 100 - 100 * (self.capacitor_capacitance / 2000)
        self.logger.info(f'ёмкость:\t{self.capacitor_capacitance_d:.2f}')
        if self.capacitor_capacitance >= 1600:
            pass
        else:
            self.reset_protect.sbros_testa_bp_0()
            self.mysql_conn.mysql_ins_result(f'неисправен емкость снижена на {self.capacitor_capacitance_d:.1f} %', "2")
            return False
        # 2.3. Форсированный разряд
        self.mysql_conn.mysql_ins_result("идёт тест 2.3", "2")
        self.mb_ctrl.ctrl_relay('KL79', True)
        sleep(1)
        self.mb_ctrl.ctrl_relay('KL79', False)
        sleep(0.3)
        self.mysql_conn.mysql_ins_result("исправен", "2")
        self.mysql_conn.mysql_ins_result(f'{self.capacitor_capacitance:.1f}', "3")
        self.mysql_conn.mysql_ins_result(f'{self.capacitor_capacitance_d:.1f}', "4")
        return True

    def st_test_30(self) -> bool:
        """
        Тест 3. Проверка работоспособности реле удержания
        """
        self.logger.debug("старт теста 3.0")
        self.mysql_conn.mysql_ins_result("идёт тест 3", "5")
        self.mb_ctrl.ctrl_relay('KL75', True)
        sleep(0.3)
        if self.di_read_full.subtest_4di(test_num=5, subtest_num=5.0,
                                         err_code_a=344, err_code_b=344, err_code_c=344, err_code_d=344,
                                         position_a=False, position_b=True, position_c=False, position_d=True,
                                         di_a='in_a6', di_b='in_a1', di_c='in_a7', di_d='in_a2'):
            self.reset_protect.sbros_testa_bp_1()
            self.mysql_conn.mysql_ins_result("неисправен", "5")
            return True
        self.mysql_conn.mysql_ins_result("исправен", "5")
        return False

    def st_test_40(self) -> bool:
        """
        Тест 4. Проверка работоспособности реле удержания
        """
        self.logger.debug("старт теста 4.0")
        self.mysql_conn.mysql_ins_result("идёт тест 4", "6")
        meas_volt = self.ai_read.ai_read('AI2')
        calc_volt = meas_volt * (103 / 3)
        self.logger.debug(f'вычисленное напряжение, должно быть больше 6\t{calc_volt:.2f}')
        if calc_volt >= 6:
            pass
        else:
            self.reset_protect.sbros_testa_bp_1()
            self.mysql_conn.mysql_ins_result("неисправен", "6")
            return False
        self.reset_protect.sbros_testa_bp_1()
        self.mysql_conn.mysql_ins_result("исправен", "6")
        return True

    def st_test_bp(self) -> bool:
        if self.st_test_10():
            if self.st_test_20():
                if self.st_test_30():
                    if self.st_test_40():
                        return True
        return False


if __name__ == '__main__':
    test_bp = TestBP()
    reset_test_bp = ResetRelay()
    mysql_conn_bp = MySQLConnect()
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
        my_msg(f'{mce}', 'red')
    finally:
        reset_test_bp.reset_all()
        sys.exit()
