# -*- coding: utf-8 -*-
"""
!!! НОВЫЙ НЕ ОБКАТАНЫЙ !!!

Алгоритм проверки

Тип блока: БУЗ-2
Производитель: Строй-энергомаш, ТЭТЗ-Инвест, нет производителя

"""

__all__ = ["TestBUZ2"]

import logging
from time import sleep, time

from .general_func.database import *
from .general_func.opc_full import ConnectOPC
from .general_func.procedure import *
from .general_func.reset import ResetRelay
from .general_func.subtest import *
from .general_func.utils import CLILog
from .gui.msgbox_1 import *


class TestBUZ2:

    def __init__(self):
        self.conn_opc = ConnectOPC()
        self.proc = Procedure()
        self.reset = ResetRelay()
        self.mysql_conn = MySQLConnect()
        self.subtest = Subtest2in()
        self.cli_log = CLILog("debug", __name__)

        self.ust_1 = 75.8
        self.ust_2 = 20.3

        self.coef_volt: float = 0.0
        self.health_flag: bool = False

        self.msg_1 = "Убедитесь в отсутствии блоков в панелях разъемов. " \
                     "Вставьте испытуемый блок БУЗ-2 в разъем Х17 на панели B."
        self.msg_2 = "Вставьте заведомо исправные блок БИ в разъем Х26  и блок БДЗ в разъем Х16, " \
                     "расположенные на панели B."
        self.msg_3 = "Установите с помощью кнопок SB1, SB2 следующие уровни уставок: ПМЗ – 2000 А; ТЗП – 400 А"

        logging.basicConfig(
            filename="C:\\Stend\\project_class\\log\\TestBUZ2.log",
            filemode="w",
            level=logging.DEBUG,
            encoding="utf-8",
            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('DEBUG')
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))

    def st_test_10(self) -> bool:
        """
        Тест 1. Включение/выключение блока в нормальном режиме:
        """
        self.cli_log.lev_info(f"старт теста {__doc__}", "skyblue")
        self.conn_opc.simplified_read_di(['inp_14', 'inp_15'])
        if my_msg(self.msg_1):
            if my_msg(self.msg_2):
                return True
        return False

    def st_test_11(self) -> bool:
        """
        1.1.	Проверка вероятности наличия короткого замыкания на входе измерительной цепи блока
        """
        min_volt, max_volt = self.proc.procedure_1_21_31_v1()
        self.conn_opc.ctrl_relay('KL73', True)
        sleep(5)
        self.logger.debug("таймаут 5 сек")
        self.cli_log.lev_debug("таймаут 5 сек", "gray")
        self.conn_opc.ctrl_relay('KL90', True)
        sleep(5)
        self.logger.debug("таймаут 5 сек")
        self.cli_log.lev_debug("таймаут 5 сек", "gray")
        self.conn_opc.ctrl_relay('KL63', True)
        meas_volt = self.conn_opc.read_ai('AI0')
        self.reset.sbros_kl63_proc_1_21_31()
        if min_volt <= meas_volt <= max_volt:
            return True
        self.mysql_conn.mysql_ins_result('неисправен', '1')
        self.mysql_conn.mysql_error(455)
        return False

    def st_test_12(self) -> bool:
        """
        1.2. Определение коэффициента Кс отклонения фактического напряжения от номинального
        """
        self.coef_volt = self.proc.procedure_1_22_32()
        if self.coef_volt != 0.0:
            pass
        else:
            self.mysql_conn.mysql_ins_result("неисправен", "1")
            return False
        self.reset.stop_procedure_32()
        self.conn_opc.ctrl_relay('KL21', True)
        self.conn_opc.ctrl_relay('KL2', True)
        self.conn_opc.ctrl_relay('KL66', True)
        sleep(6)
        self.logger.debug("таймаут 6 сек")
        self.cli_log.lev_debug("таймаут 6 сек", "gray")
        self.conn_opc.ctrl_relay('KL84', True)
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        self.conn_opc.ctrl_relay('KL84', False)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        self.conn_opc.ctrl_relay('KL80', True)
        sleep(0.1)
        self.logger.debug("таймаут 0.1 сек")
        self.cli_log.lev_debug("таймаут 0.1 сек", "gray")
        self.conn_opc.ctrl_relay('KL24', True)
        sleep(5)
        self.logger.debug("таймаут 5 сек")
        self.cli_log.lev_debug("таймаут 5 сек", "gray")
        inp_01, inp_02 = self.conn_opc.simplified_read_di(['inp_01', 'inp_02'])
        if inp_01 is True and inp_02 is True:
            pass
        else:
            self.mysql_conn.mysql_ins_result("неисправен", "1")
            return False
        return True

    def st_test_13(self) -> bool:
        """
        1.4.	Выключение блока
        """
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        self.conn_opc.ctrl_relay('KL80', False)
        sleep(0.1)
        self.logger.debug("таймаут 0.1 сек")
        self.cli_log.lev_debug("таймаут 0.1 сек", "gray")
        self.conn_opc.ctrl_relay('KL24', False)
        sleep(5)
        self.logger.debug("таймаут 5 сек")
        self.cli_log.lev_debug("таймаут 5 сек", "gray")
        inp_01, inp_02 = self.conn_opc.simplified_read_di(['inp_01', 'inp_02'])
        if inp_01 is False and inp_02 is False:
            pass
        else:
            self.mysql_conn.mysql_ins_result("неисправен", "1")
            return False
        self.mysql_conn.mysql_ins_result("исправен", "1")
        return True

    def st_test_20(self) -> bool:
        """
        Тест 2. Проверка работоспособности защиты МТЗ:
        2.1. Пуск блока
        """
        self.conn_opc.ctrl_relay('KL66', False)
        sleep(0.3)
        self.logger.debug("таймаут 0.3 сек")
        self.cli_log.lev_debug("таймаут 0.3 сек", "gray")
        self.conn_opc.ctrl_relay('KL82', True)
        sleep(0.3)
        self.logger.debug("таймаут 0.3 сек")
        self.cli_log.lev_debug("таймаут 0.3 сек", "gray")
        self.conn_opc.ctrl_relay('KL66', True)
        if my_msg(self.msg_3):
            pass
        else:
            return False
        self.conn_opc.ctrl_relay('KL66', False)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        self.conn_opc.ctrl_relay('KL82', False)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        self.conn_opc.ctrl_relay('KL66', True)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        self.conn_opc.ctrl_relay('KL84', True)
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        self.conn_opc.ctrl_relay('KL84', False)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        self.conn_opc.ctrl_relay('KL80', True)
        sleep(0.1)
        self.logger.debug("таймаут 0.1 сек")
        self.cli_log.lev_debug("таймаут 0.1 сек", "gray")
        self.conn_opc.ctrl_relay('KL24', True)
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        inp_01, inp_02 = self.conn_opc.simplified_read_di(['inp_01', 'inp_02'])
        if inp_01 is True and inp_02 is True:
            pass
        else:
            self.mysql_conn.mysql_ins_result("неисправен", "2")
            return False
        return True

    def st_test_21(self) -> bool:
        if self.proc.procedure_x4_to_x5(coef_volt=self.coef_volt, setpoint_volt=self.ust_1):
            pass
        else:
            self.mysql_conn.mysql_ins_result("неисправен", "2")
            return False
        self.conn_opc.ctrl_relay('KL63', True)
        sleep(0.5)
        self.logger.debug("таймаут 0.5 сек")
        self.cli_log.lev_debug("таймаут 0.5 сек", "gray")
        self.conn_opc.ctrl_relay('KL63', False)
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        inp_01, inp_02 = self.conn_opc.simplified_read_di(['inp_01', 'inp_02'])
        if inp_01 is False and inp_02 is False:
            pass
        else:
            self.reset.stop_procedure_3()
            self.mysql_conn.mysql_ins_result("неисправен", "2")
            return False
        self.reset.stop_procedure_3()
        return True

    def st_test_22(self) -> bool:
        """
        2.3.  Финишные операции при положительном завершении теста:
        """
        self.conn_opc.ctrl_relay('KL80', False)
        self.conn_opc.ctrl_relay('KL24', False)
        sleep(6)
        self.logger.debug("таймаут 6 сек")
        self.cli_log.lev_debug("таймаут 6 сек", "gray")
        self.conn_opc.ctrl_relay('KL84', True)
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        self.conn_opc.ctrl_relay('KL84', False)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        self.mysql_conn.mysql_ins_result("исправен", "2")
        return True

    def st_test_30(self) -> bool:
        """
        Тест 3. Проверка работоспособности защиты ТЗП
        3.1. Пуск блока
        """
        self.conn_opc.ctrl_relay('KL80', True)
        sleep(0.1)
        self.logger.debug("таймаут 0.1 сек")
        self.cli_log.lev_debug("таймаут 0.1 сек", "gray")
        self.conn_opc.ctrl_relay('KL24', True)
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        inp_01, inp_02 = self.conn_opc.simplified_read_di(['inp_01', 'inp_02'])
        if inp_01 is True and inp_02 is True:
            pass
        else:
            self.mysql_conn.mysql_ins_result("неисправен", "3")
            return False
        return True

    def st_test_31(self) -> bool:
        if self.proc.procedure_x4_to_x5(coef_volt=self.coef_volt, setpoint_volt=self.ust_2):
            pass
        else:
            self.mysql_conn.mysql_ins_result("неисправен", "3")
            return False
        self.conn_opc.ctrl_relay('KL63', True)
        inp_09, *_ = self.conn_opc.simplified_read_di(['inp_09'])
        k = 0
        while inp_09 is False and k <= 10:
            inp_09, *_ = self.conn_opc.simplified_read_di(['inp_09'])
            k += 1
        start_timer = time()
        inp_01, *_ = self.conn_opc.simplified_read_di(['inp_01'])
        stop_timer = 0
        while inp_01 is True and stop_timer <= 360:
            inp_01, *_ = self.conn_opc.simplified_read_di(['inp_01'])
            stop_timer = time() - start_timer
        timer_test_3 = stop_timer
        inp_01, inp_02 = self.conn_opc.simplified_read_di(['inp_01', 'inp_02'])
        if inp_01 is False and inp_02 is False and timer_test_3 <= 360:
            pass
        else:
            self.mysql_conn.mysql_ins_result("неисправен", "3")
            self.reset.sbros_kl63_proc_all()
            return False
        self.reset.sbros_kl63_proc_all()
        self.mysql_conn.mysql_ins_result(f'исправен, {timer_test_3:.1f} сек', "3")
        return True

    def st_test_buz_2(self) -> [bool, bool]:
        """
            Главная функция которая собирает все остальные
            :type: bool, bool,
            :return: результат теста, флаг исправности
        """
        if self.st_test_10():
            if self.st_test_11():
                if self.st_test_12():
                    if self.st_test_13():
                        if self.st_test_20():
                            if self.st_test_21():
                                if self.st_test_22():
                                    if self.st_test_30():
                                        if self.st_test_31():
                                            return True, self.health_flag
        return False, self.health_flag
