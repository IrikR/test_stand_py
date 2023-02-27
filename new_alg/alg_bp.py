# -*- coding: utf-8 -*-
"""
!!! НОВЫЙ НЕ ОБКАТАНЫЙ !!!

Алгоритм проверки

Тип блока: БП
Производитель: Строй-энергомаш, ТЭТЗ-Инвест, нет производителя

"""

__all__ = ["TestBP"]

import logging
import math
from time import sleep

from .general_func.database import *
from .general_func.opc_full import ConnectOPC
from .general_func.reset import ResetProtection, ResetRelay
from .general_func.utils import CLILog
from .gui.msgbox_1 import *


class TestBP:
    """
    capacitor capacitance - емкость конденсатора
    charge - заряд
    """

    def __init__(self):
        self.conn_opc = ConnectOPC()
        self.reset_relay = ResetRelay()
        self.reset_protect = ResetProtection()
        self.mysql_conn = MySQLConnect()
        self.cli_log = CLILog("debug", __name__)

        self.capacitor_capacitance: float = 0.0
        self.capacitor_capacitance_d: float = 0.0

        self.msg_1: str = "Убедитесь в отсутствии других блоков и вставьте блок БП в соответствующий разъем"

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

        self.cli_log.lev_info(f"старт теста {__doc__}", "skyblue")

        if not my_msg(self.msg_1):
            return False

        self.mysql_conn.mysql_ins_result("идёт тест 1", "1")
        self.conn_opc.ctrl_relay('KL78', True)
        if self.conn_opc.subtest_read_di(test_num=1, subtest_num=1.0,
                                         err_code=[344, 344, 344, 344],
                                         position_inp=[True, False, True, False],
                                         di_xx=['inp_06', 'inp_01', 'inp_07', 'inp_02']):
            return True
        return False

    def st_test_20(self) -> bool:
        """
        Тест 2. Определение ёмкости пусковых конденсаторов
        2.1. Заряд конденсаторов
        """
        self.logger.debug("старт теста 2.0")
        self.mysql_conn.mysql_ins_result("идёт тест 2.1", "2")
        self.conn_opc.ctrl_relay('KL77', True)
        sleep(0.3)
        self.logger.debug("таймаут 0.3 сек")
        self.cli_log.lev_debug("таймаут 0.3 сек", "gray")
        self.conn_opc.ctrl_relay('KL65', True)
        sleep(0.3)
        self.logger.debug("таймаут 0.3 сек")
        self.cli_log.lev_debug("таймаут 0.3 сек", "gray")
        self.conn_opc.ctrl_relay('KL66', True)
        sleep(5)
        self.logger.debug("таймаут 5 сек")
        self.cli_log.lev_debug("таймаут 5 сек", "gray")
        self.conn_opc.ctrl_relay('KL76', True)
        sleep(5)
        self.logger.debug("таймаут 5 сек")
        self.cli_log.lev_debug("таймаут 5 сек", "gray")
        charge_1 = self.conn_opc.read_ai('AI2')
        self.logger.info(f'заряд конденсатора по истечении 5с:\t{charge_1} В')
        if charge_1 != 999:
            pass
        else:
            self.mysql_conn.mysql_ins_result("неисправен", "2")
            return False
        sleep(15)
        self.logger.debug("таймаут 15 сек")
        self.cli_log.lev_debug("таймаут 15 сек", "gray")
        charge_2 = self.conn_opc.read_ai('AI2')
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
        self.conn_opc.ctrl_relay('KL79', True)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        self.conn_opc.ctrl_relay('KL79', False)
        sleep(0.3)
        self.logger.debug("таймаут 0.3 сек")
        self.cli_log.lev_debug("таймаут 0.3 сек", "gray")
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
        self.conn_opc.ctrl_relay('KL75', True)
        sleep(0.3)
        self.logger.debug("таймаут 0.3 сек")
        self.cli_log.lev_debug("таймаут 0.3 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=5, subtest_num=5.0,
                                         err_code=[344, 344, 344, 344],
                                         position_inp=[False, True, False, True],
                                         di_xx=['inp_06', 'inp_01', 'inp_07', 'inp_02']):
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
        meas_volt = self.conn_opc.read_ai('AI2')
        calc_volt = meas_volt * (103 / 3)
        self.logger.debug(f'вычисленное напряжение, должно быть больше 6\t{calc_volt:.2f}')
        if calc_volt >= 6:
            self.reset_protect.sbros_testa_bp_1()
            self.mysql_conn.mysql_ins_result("исправен", "6")
            return True
        self.reset_protect.sbros_testa_bp_1()
        self.mysql_conn.mysql_ins_result("неисправен", "6")
        return False


    def st_test_bp(self) -> bool:
        """
            Главная функция которая собирает все остальные
            :type: bool
            :return:  результат теста
        """
        if self.st_test_10():
            if self.st_test_20():
                if self.st_test_30():
                    if self.st_test_40():
                        return True
        return False
