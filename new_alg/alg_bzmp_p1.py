# -*- coding: utf-8 -*-
"""
!!! НОВЫЙ НЕ ОБКАТАНЫЙ !!!

Тип блока: БЗМП-П1
Производитель: Пульсар.

"""

__all__ = ["TestBZMPP1"]

import logging
from time import sleep, time

from .general_func.database import *
from .general_func.opc_full import ConnectOPC
from .general_func.procedure import *
from .general_func.reset import ResetProtection, ResetRelay
from .general_func.utils import CLILog
from .gui.msgbox_1 import *


class TestBZMPP1:

    def __init__(self):
        self.conn_opc = ConnectOPC()
        self.proc = Procedure()
        self.reset = ResetRelay()
        self.mysql_conn = MySQLConnect()
        self.reset_protect = ResetProtection()
        self.cli_log = CLILog("debug", __name__)

        self.ust: float = 14.64
        self.ust_pmz: float = 25.2
        self.ust_faz: float = 8.2

        self.coef_volt: float = 0.0
        self.timer_test_5_2: float = 0.0
        self.timer_test_6_2: float = 0.0
        self.health_flag: bool = False

        self.msg_1: str = "Убедитесь в отсутствии других блоков и вставьте блок БЗМП-П1 в соответствующий разъем"
        self.msg_2: str = "С помощью кнопок SB1…SB3, расположенных на панели разъемов, " \
                          "установите следующие параметры блока: - Iном=200А; Iпер=1.2; Iпуск=7.5»"
        self.msg_3: str = "С помощью кнопок SB1…SB3 перейдите к окну на дисплее блока с надписью «Токи фаз»"
        self.msg_4: str = "С помощью кнопок SB1…SB3 перейдите к окну на дисплее блока с надписью «Токи фаз»"
        self.msg_5: str = "С помощью кнопок SB1…SB3 перейдите к окну на дисплее блока с надписью «Токи фаз»"

        logging.basicConfig(
            filename="C:\\Stend\\project_class\\log\\TestBZMPP1.log",
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
        """
        self.cli_log.lev_info(f"старт теста {__doc__}", "skyblue")
        if my_msg(self.msg_1):
            return True
        return False

    def st_test_11(self) -> bool:
        """
        1.1.	Проверка вероятности наличия короткого замыкания на входе измерительной цепи блока
        """
        self.logger.debug("идёт тест 1.1")
        meas_volt_ust = self.proc.procedure_1_21_31()
        if meas_volt_ust != 0.0:
            pass
        else:
            self.mysql_conn.mysql_ins_result("неисправен TV1", "1")
            return False
        self.conn_opc.ctrl_relay('KL73', True)
        sleep(5)
        self.logger.debug("таймаут 5 сек")
        self.cli_log.lev_debug("таймаут 5 сек", "gray")
        self.conn_opc.ctrl_relay('KL90', True)
        sleep(5)
        self.logger.debug("таймаут 5 сек")
        self.cli_log.lev_debug("таймаут 5 сек", "gray")
        self.conn_opc.ctrl_relay('KL63', True)
        min_volt = 0.6 * meas_volt_ust
        max_volt = 1.0 * meas_volt_ust
        meas_volt = self.conn_opc.read_ai('AI0')
        self.logger.debug(f'напряжение после включения KL63 '
                          f'{min_volt} <= {meas_volt} <= {max_volt}')
        if min_volt <= meas_volt <= max_volt:
            pass
        else:
            self.mysql_conn.mysql_ins_result('неисправен', '1')
            self.mysql_conn.mysql_error(455)
            self.reset.sbros_kl63_proc_1_21_31()
            return False
        self.reset.sbros_kl63_proc_1_21_31()
        return True

    def st_test_12(self) -> bool:
        """
        1.2. Определение коэффициента Кс отклонения фактического напряжения от номинального
        """
        self.logger.debug("идёт тест 1.2")
        self.coef_volt = self.proc.procedure_1_22_32()
        if self.coef_volt != 0.0:
            self.reset.stop_procedure_32()
            return True
        self.mysql_conn.mysql_ins_result("неисправен TV1", "1")
        return False

    def st_test_13(self) -> bool:
        self.logger.debug("идёт тест 1.3")
        self.conn_opc.ctrl_relay('KL67', True)
        timer_test_1 = 0
        start_timer_test_1 = time()
        while timer_test_1 <= 120:
            sleep(0.2)
            timer_test_1 = time() - start_timer_test_1
            inp_01, inp_06 = self.conn_opc.simplified_read_di(['inp_01', 'inp_06'])
            self.logger.debug(f'времени прошло\t{timer_test_1:.1f}')
            if inp_01 is True and inp_06 is False:
                break
            else:
                continue
        inp_01, inp_06 = self.conn_opc.simplified_read_di(['inp_01', 'inp_06'])
        if inp_01 is True and inp_06 is False:
            self.mysql_conn.mysql_ins_result("исправен", "1")
            return True
        self.mysql_conn.mysql_ins_result("неисправен", "1")
        return False

    def st_test_20(self) -> bool:
        """
        Тест 2. Проверка защиты ПМЗ
        """
        if my_msg(self.msg_2):
            if my_msg(self.msg_3):
                return True
        return False

    def st_test_21(self) -> bool:
        self.logger.debug("идёт тест 2.1")
        if self.proc.procedure_x4_to_x5(coef_volt=self.coef_volt, setpoint_volt=self.ust_pmz):
            return True
        self.mysql_conn.mysql_ins_result("неисправен TV1", "2")
        return False

    def st_test_22(self) -> bool:
        self.logger.debug("идёт тест 2.2")
        self.conn_opc.ctrl_relay('KL63', True)
        sleep(0.5)
        self.logger.debug("таймаут 0.5 сек")
        self.cli_log.lev_debug("таймаут 0.5 сек", "gray")
        self.conn_opc.ctrl_relay('KL63', False)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        inp_01, inp_06 = self.conn_opc.simplified_read_di(['inp_01', 'inp_06'])
        if inp_01 is False and inp_06 is True:
            self.reset.stop_procedure_3()
            return True
        self.logger.debug("положение выходов не соответствует")
        self.mysql_conn.mysql_ins_result("неисправен", "2")
        self.reset.stop_procedure_3()
        return False

    def st_test_23(self) -> bool:
        """
        2.4.2. Сброс защит после проверки
        """
        if self.reset_protection(test_num=2, subtest_num=2.3):
            return True
        return False

    def st_test_30(self) -> bool:
        """
        Тест 3. Проверка защиты от несимметрии фаз
        """
        self.logger.debug("идёт тест 3.0")
        if not my_msg(self.msg_4):
            return False

        if self.proc.procedure_x4_to_x5(coef_volt=self.coef_volt, setpoint_volt=self.ust_faz):
            return True
        self.mysql_conn.mysql_ins_result("неисправен TV1", "3")
        return False

    def st_test_31(self) -> bool:
        self.logger.debug("идёт тест 3.1")
        self.conn_opc.ctrl_relay('KL81', True)
        sleep(0.1)
        self.logger.debug("таймаут 0.1 сек")
        self.cli_log.lev_debug("таймаут 0.1 сек", "gray")
        self.conn_opc.ctrl_relay('KL63', True)
        inp_09, *_ = self.conn_opc.simplified_read_di(['inp_09'])
        i = 0
        while inp_09 is False and i <= 10:
            inp_09, *_ = self.conn_opc.simplified_read_di(['inp_09'])
            i += 1
        start_timer = time()
        inp_06, *_ = self.conn_opc.simplified_read_di(['inp_06'])
        stop_timer = 0
        while inp_06 is False and stop_timer <= 12:
            inp_06, *_ = self.conn_opc.simplified_read_di(['inp_06'])
            stop_timer = time() - start_timer
        self.timer_test_5_2 = stop_timer
        self.logger.debug(f'таймер тест 3: {self.timer_test_5_2:.1f}')
        inp_01, inp_06 = self.conn_opc.simplified_read_di(['inp_01', 'inp_06'])
        if inp_01 is False and inp_06 is True and self.timer_test_5_2 <= 12:
            self.logger.debug("положение выходов соответствует")
            self.reset.sbros_kl63_proc_all()
            self.conn_opc.ctrl_relay('KL81', False)
            return True
        self.logger.debug("положение выходов не соответствует")
        self.mysql_conn.mysql_ins_result("неисправен", "3")
        self.reset.sbros_kl63_proc_all()
        self.conn_opc.ctrl_relay('KL81', False)
        return False

    def st_test_32(self) -> bool:
        """
        3.5. Сброс защит после проверки
        """
        self.logger.debug("идёт тест 3.2")
        self.conn_opc.ctrl_relay('KL24', True)
        sleep(4)
        self.logger.debug("таймаут 4 сек")
        self.cli_log.lev_debug("таймаут 4 сек", "gray")
        self.conn_opc.ctrl_relay('KL24', False)
        sleep(0.7)
        self.logger.debug("таймаут 0.7 сек")
        self.cli_log.lev_debug("таймаут 0.7 сек", "gray")
        inp_01, inp_06 = self.conn_opc.simplified_read_di(['inp_01', 'inp_06'])
        if inp_01 is True and inp_06 is False:
            self.logger.debug("положение выходов соответствует")
            self.mysql_conn.mysql_ins_result(f'исправен, {self.timer_test_5_2:.1f} сек', "3")
            return True
        self.logger.debug("положение выходов не соответствует")
        self.mysql_conn.mysql_ins_result("неисправен", "5")
        return False

    def st_test_40(self) -> bool:
        """
        Тест 4. Проверка защиты от перегрузки
        """
        self.logger.debug("идёт тест 4.0")

        if not my_msg(self.msg_5):
            return False

        if self.proc.procedure_x4_to_x5(coef_volt=self.coef_volt, setpoint_volt=self.ust):
            return True
        self.mysql_conn.mysql_ins_result("неисправен TV1", "4")
        return False

    def st_test_41(self) -> bool:
        """
        4.2.  Проверка срабатывания блока от сигнала нагрузки:
        """
        self.logger.debug("идёт тест 4.1")
        self.conn_opc.ctrl_relay('KL63', True)
        inp_09, *_ = self.conn_opc.simplified_read_di(['inp_09'])
        k = 0
        while inp_09 is False and k <= 10:
            inp_09, *_ = self.conn_opc.simplified_read_di(['inp_09'])
            k += 1
        start_timer = time()
        inp_06, *_ = self.conn_opc.simplified_read_di(['inp_06'])
        stop_timer = 0
        while inp_06 is False and stop_timer <= 360:
            inp_06, *_ = self.conn_opc.simplified_read_di(['inp_06'])
            stop_timer = time() - start_timer
            self.logger.debug(f'таймер тест 4: {stop_timer:.1f}')
        self.timer_test_6_2 = stop_timer
        self.logger.debug(f'таймер тест 4: {self.timer_test_6_2:.1f}')
        inp_01, inp_06 = self.conn_opc.simplified_read_di(['inp_01', 'inp_06'])
        if inp_01 is False and inp_06 is True and self.timer_test_6_2 <= 360:
            pass
        else:
            self.logger.debug("положение выходов не соответствует")
            self.mysql_conn.mysql_ins_result("неисправен", "4")
            self.reset.sbros_kl63_proc_all()
            return False
        self.logger.debug("положение выходов соответствует")
        self.reset.sbros_kl63_proc_all()
        return True

    def st_test_42(self) -> bool:
        """
        4.6. Сброс защит после проверки
        """
        if self.reset_protection(test_num=4, subtest_num=4.2):
            self.mysql_conn.mysql_ins_result(f'исправен, {self.timer_test_6_2:.1f} сек', "4")
            return True
        return False

    def reset_protection(self, *, test_num: int, subtest_num: float) -> bool:
        """
        Код ошибки	345	–	Сообщение	«Блок не исправен. Не работает сброс защиты блока после срабатывания».
        :param test_num:
        :param subtest_num:
        :return:
        """
        self.reset_protect.sbros_zashit_kl24()
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=test_num, subtest_num=subtest_num,
                                         err_code=[345, 345],
                                         position_inp=[True, False],
                                         di_xx=['inp_01', 'inp_06']):
            return True
        return False

    def st_test_bzmp_p1(self) -> [bool, bool]:
        """
            Главная функция которая собирает все остальные
            :type: bool, bool
            :return:  результат теста, флаг исправности
        """
        if self.st_test_10():
            if self.st_test_11():
                if self.st_test_12():
                    if self.st_test_13():
                        if self.st_test_20():
                            if self.st_test_21():
                                if self.st_test_22():
                                    if self.st_test_23():
                                        if self.st_test_30():
                                            if self.st_test_31():
                                                if self.st_test_32():
                                                    if self.st_test_40():
                                                        if self.st_test_41():
                                                            if self.st_test_42():
                                                                return True, self.health_flag
        return False, self.health_flag
