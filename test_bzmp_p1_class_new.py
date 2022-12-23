#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тип блока: БЗМП-П1
Производитель: Пульсар.
"""

import sys
import logging

from time import sleep, time

from general_func.exception import *
from general_func.database import *
from general_func.modbus import *
from general_func.procedure import *
from general_func.reset import ResetRelay, ResetProtection
from general_func.subtest import ReadOPCServer
from gui.msgbox_1 import *

__all__ = ["TestBZMPP1"]


class TestBZMPP1:

    def __init__(self):
        self.proc = Procedure()
        self.reset = ResetRelay()
        self.ai_read = AIRead()
        self.mb_ctrl = CtrlKL()
        self.di_read = DIRead()
        self.mysql_conn = MySQLConnect()
        self.reset_protect = ResetProtection()
        self.di_read_full = ReadOPCServer()

        self.ust: float = 14.64
        self.ust_pmz: float = 25.2
        self.ust_faz: float = 8.2

        self.coef_volt: float = 0.0
        self.timer_test_5_2: float = 0.0
        self.timer_test_6_2: float = 0.0
        self.health_flag: bool = False

        self.msg_1 = "Убедитесь в отсутствии других блоков и вставьте блок БЗМП-П1 в соответствующий разъем"
        self.msg_2 = "С помощью кнопок SB1…SB3, расположенных на панели разъемов, " \
                     "установите следующие параметры блока: - Iном=200А; Iпер=1.2; Iпуск=7.5»"
        self.msg_3 = "С помощью кнопок SB1…SB3 перейдите к окну на дисплее блока с надписью «Токи фаз»"
        self.msg_4 = "С помощью кнопок SB1…SB3 перейдите к окну на дисплее блока с надписью «Токи фаз»"
        self.msg_5 = "С помощью кнопок SB1…SB3 перейдите к окну на дисплее блока с надписью «Токи фаз»"

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
        self.di_read.di_read('in_a0')
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
        self.mb_ctrl.ctrl_relay('KL73', True)
        sleep(5)
        self.mb_ctrl.ctrl_relay('KL90', True)
        sleep(5)
        self.mb_ctrl.ctrl_relay('KL63', True)
        min_volt = 0.6 * meas_volt_ust
        max_volt = 1.0 * meas_volt_ust
        meas_volt = self.ai_read.ai_read('AI0')
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
            pass
        else:
            self.mysql_conn.mysql_ins_result("неисправен TV1", "1")
            return False
        self.reset.stop_procedure_32()
        return True

    def st_test_13(self) -> bool:
        self.logger.debug("идёт тест 1.3")
        self.mb_ctrl.ctrl_relay('KL67', True)
        timer_test_1 = 0
        start_timer_test_1 = time()
        while timer_test_1 <= 120:
            sleep(0.2)
            timer_test_1 = time() - start_timer_test_1
            in_a1, in_a6 = self.di_read.di_read('in_a1', 'in_a6')
            self.logger.debug(f'времени прошло\t{timer_test_1:.1f}')
            if in_a1 is True and in_a6 is False:
                break
            else:
                continue
        in_a1, in_a6 = self.di_read.di_read('in_a1', 'in_a6')
        if in_a1 is True and in_a6 is False:
            pass
        else:
            self.mysql_conn.mysql_ins_result("неисправен", "1")
            return False
        self.mysql_conn.mysql_ins_result("исправен", "1")
        return True

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
        self.mb_ctrl.ctrl_relay('KL63', True)
        sleep(0.5)
        self.mb_ctrl.ctrl_relay('KL63', False)
        sleep(1)
        in_a1, in_a6 = self.di_read.di_read('in_a1', 'in_a6')
        if in_a1 is False and in_a6 is True:
            pass
        else:
            self.logger.debug("положение выходов не соответствует")
            self.mysql_conn.mysql_ins_result("неисправен", "2")
            self.reset.stop_procedure_3()
            return False
        self.reset.stop_procedure_3()
        return True

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
        if my_msg(self.msg_4):
            pass
        else:
            return False
        if self.proc.procedure_x4_to_x5(coef_volt=self.coef_volt, setpoint_volt=self.ust_faz):
            return True
        self.mysql_conn.mysql_ins_result("неисправен TV1", "3")
        return False

    def st_test_31(self) -> bool:
        self.logger.debug("идёт тест 3.1")
        self.mb_ctrl.ctrl_relay('KL81', True)
        sleep(0.1)
        self.mb_ctrl.ctrl_relay('KL63', True)
        in_b1, *_ = self.di_read.di_read('in_b1')
        i = 0
        while in_b1 is False and i <= 10:
            in_b1, *_ = self.di_read.di_read('in_b1')
            i += 1
        start_timer = time()
        in_a6, *_ = self.di_read.di_read('in_a6')
        stop_timer = 0
        while in_a6 is False and stop_timer <= 12:
            in_a6, *_ = self.di_read.di_read('in_a6')
            stop_timer = time() - start_timer
        self.timer_test_5_2 = stop_timer
        self.logger.debug(f'таймер тест 3: {self.timer_test_5_2:.1f}')
        in_a1, in_a6 = self.di_read.di_read('in_a1', 'in_a6')
        if in_a1 is False and in_a6 is True and self.timer_test_5_2 <= 12:
            pass
        else:
            self.logger.debug("положение выходов не соответствует")
            self.mysql_conn.mysql_ins_result("неисправен", "3")
            self.reset.sbros_kl63_proc_all()
            self.mb_ctrl.ctrl_relay('KL81', False)
            return False
        self.logger.debug("положение выходов соответствует")
        self.reset.sbros_kl63_proc_all()
        self.mb_ctrl.ctrl_relay('KL81', False)
        return True

    def st_test_32(self) -> bool:
        """
        3.5. Сброс защит после проверки
        """
        self.logger.debug("идёт тест 3.2")
        self.mb_ctrl.ctrl_relay('KL24', True)
        sleep(4)
        self.mb_ctrl.ctrl_relay('KL24', False)
        sleep(0.7)
        in_a1, in_a6 = self.di_read.di_read('in_a1', 'in_a6')
        if in_a1 is True and in_a6 is False:
            pass
        else:
            self.logger.debug("положение выходов не соответствует")
            self.mysql_conn.mysql_ins_result("неисправен", "5")
            return False
        self.logger.debug("положение выходов соответствует")
        self.mysql_conn.mysql_ins_result(f'исправен, {self.timer_test_5_2:.1f} сек', "3")
        return True

    def st_test_40(self) -> bool:
        """
        Тест 4. Проверка защиты от перегрузки
        """
        self.logger.debug("идёт тест 4.0")
        if my_msg(self.msg_5):
            pass
        else:
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
        self.mb_ctrl.ctrl_relay('KL63', True)
        in_b1, *_ = self.di_read.di_read('in_b1')
        k = 0
        while in_b1 is False and k <= 10:
            in_b1, *_ = self.di_read.di_read('in_b1')
            k += 1
        start_timer = time()
        in_a6, *_ = self.di_read.di_read('in_a6')
        stop_timer = 0
        while in_a6 is False and stop_timer <= 360:
            in_a6, *_ = self.di_read.di_read('in_a6')
            stop_timer = time() - start_timer
            self.logger.debug(f'таймер тест 4: {stop_timer:.1f}')
        self.timer_test_6_2 = stop_timer
        self.logger.debug(f'таймер тест 4: {self.timer_test_6_2:.1f}')
        in_a1, in_a6 = self.di_read.di_read('in_a1', 'in_a6')
        if in_a1 is False and in_a6 is True and self.timer_test_6_2 <= 360:
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
        if self.di_read_full.subtest_2di(test_num=test_num, subtest_num=subtest_num, err_code_a=345, err_code_b=345,
                                         position_a=True, position_b=False, di_a='in_a1', di_b='in_a6'):
            return True
        return False

    def st_test_bzmp_p1(self) -> [bool, bool]:
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


if __name__ == '__main__':
    test_bzmp_p1 = TestBZMPP1()
    reset_test_bzmp_p1 = ResetRelay()
    mysql_conn_bzmp_p1 = MySQLConnect()
    try:
        test, health_flag = test_bzmp_p1.st_test_bzmp_p1()
        if test and not health_flag:
            mysql_conn_bzmp_p1.mysql_block_good()
            my_msg('Блок исправен', 'green')
        else:
            mysql_conn_bzmp_p1.mysql_block_bad()
            my_msg('Блок неисправен', 'red')
    except OSError:
        my_msg("ошибка системы", 'red')
    except SystemError:
        my_msg("внутренняя ошибка", 'red')
    except ModbusConnectException as mce:
        my_msg(f'{mce}', 'red')
    except HardwareException as hwe:
        my_msg(f'{hwe}', 'red')
    finally:
        reset_test_bzmp_p1.reset_all()
        sys.exit()
