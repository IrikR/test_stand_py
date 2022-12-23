#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки

Тип блока	Производитель
БЗМП-П	Пульсар

"""

__all__ = ["TestBZMPP"]

import sys
import logging

from time import sleep, time

from my_msgbox import *
from gen_func_procedure import *
from gen_func_utils import *
from gen_mb_client import *
from gen_mysql_connect import *


class TestBZMPP(object):

    def __init__(self):
        self.__proc = Procedure()
        self.__reset = ResetRelay()
        self.__resist = Resistor()
        self.__read_mb = ReadMB()
        self.__mb_ctrl = CtrlKL()
        self.__mysql_conn = MySQLConnect()
        self.__fault = Bug(True)

        self.ust_pmz: float = 25.2
        self.ust_faz: float = 8.2
        self.ust_peregruz: float = 10.7

        self.coef_volt: float = 0.0
        self.timer_test_6_2: float = 0.0
        self.health_flag: bool = False

        self.msg_1 = "Убедитесь в отсутствии других блоков и вставьте блок БЗМП-П в соответствующий разъем"
        self.msg_2 = "С помощью кнопок SB1…SB3, расположенных на панели разъемов, " \
                     "установите следующие параметры блока:" \
                     "Iном = 200А; Iпер = 1.2; Iпуск= 7.5; Uном = 660В»"
        self.msg_3 = "С помощью кнопки SB3 перейдите к окну на дисплее блока с надписью «Uном=660В»"
        self.msg_4 = "С помощью кнопки SB3 перейдите к окну на дисплее блока с надписью «Uном=660В»"
        self.msg_5 = "С помощью кнопки SB3 перейдите к окну на дисплее блока с надписью «Токи фаз»"
        self.msg_6 = "С помощью кнопок SB1…SB3 перейдите к окну на дисплее блока с надписью «Токи фаз»"
        self.msg_7 = "С помощью кнопок SB1…SB3 перейдите к окну на дисплее блока с надписью «Токи фаз»"

        logging.basicConfig(filename="C:\Stend\project_class\TestBZMPP.log",
                            filemode="w",
                            level=logging.DEBUG,
                            encoding="utf-8",
                            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('WARNING')
        self.logger = logging.getLogger(__name__)

    def st_test_10_bzmp_p(self) -> bool:
        """
        Тест 1. Проверка исходного состояния блока:
        1.1.	Проверка вероятности наличия короткого замыкания на входе измерительной цепи блока
        """
        self.__inputs_a0()
        if my_msg(self.msg_1):
            pass
        else:
            return False
        meas_volt_ust = self.__proc.procedure_1_21_31()
        if meas_volt_ust != 0.0:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен TV1", "1")
            return False
        self.__mb_ctrl.ctrl_relay('KL73', True)
        sleep(5)
        self.__mb_ctrl.ctrl_relay('KL90', True)
        sleep(5)
        self.__mb_ctrl.ctrl_relay('KL63', True)
        min_volt = 0.6 * meas_volt_ust
        max_volt = 1.0 * meas_volt_ust
        meas_volt = self.__read_mb.read_analog()
        self.__fault.debug_msg(f'напряжение после включения KL63 '
                               f'{min_volt:.2f} <= {meas_volt:.2f} <= {max_volt:.2f}', 'orange')
        if min_volt <= meas_volt <= max_volt:
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '1')
            self.__mysql_conn.mysql_error(455)
            self.__reset.sbros_kl63_proc_1_21_31()
            return False
        self.__reset.sbros_kl63_proc_1_21_31()
        return True

    def st_test_11_bzmp_p(self) -> bool:
        """
        1.2. Определение коэффициента Кс отклонения фактического напряжения от номинального
        """
        self.coef_volt = self.__proc.procedure_1_22_32()
        if self.coef_volt != 0.0:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", "1")
            self.__reset.stop_procedure_32()
            return False
        self.__reset.stop_procedure_32()
        return True

    def st_test_12_bzmp_p(self) -> bool:
        self.__mb_ctrl.ctrl_relay('KL67', True)
        self.__mysql_conn.progress_level(0.0)
        timer_test_1 = 0
        start_timer_test_1 = time()
        while timer_test_1 <= 120:
            sleep(0.2)
            timer_test_1 = time() - start_timer_test_1
            self.__mysql_conn.progress_level(timer_test_1)
            in_a1, in_a5, in_a6 = self.__inputs_a()
            self.__fault.debug_msg(f'времени прошло:\t{timer_test_1:.1f}', 'orange')
            if in_a1 is True and in_a5 is True and in_a6 is False:
                break
            else:
                continue
        self.__mysql_conn.progress_level(0.0)
        self.__mysql_conn.mysql_ins_result("исправен", "1")
        return True

    def st_test_20_bzmp_p(self) -> bool:
        """
        Тест 2. Проверка срабатывания блока при снижении изоляции цепей 36В
        """
        if my_msg(self.msg_2):
            if my_msg(self.msg_3):
                return True
        return False

    def st_test_21_bzmp_p(self) -> bool:
        self.__mb_ctrl.ctrl_relay('KL21', True)
        sleep(1)
        self.__mb_ctrl.ctrl_relay('KL27', True)
        sleep(0.1)
        self.__mb_ctrl.ctrl_relay('KL27', False)
        sleep(0.2)
        in_a1, in_a5, in_a6 = self.__inputs_a()
        self.__fault.debug_msg(f"{in_a1 = }, {in_a5 = }, {in_a6 = }", 'purple')
        if in_a1 is False and in_a5 is False and in_a6 is True:
            pass
        else:
            self.__fault.debug_msg("тест 2.1.1 положение выходов не соответствует", 'red')
            self.__mysql_conn.mysql_ins_result("неисправен", "2")
            return False
        sleep(5)
        in_a1, in_a5, in_a6 = self.__inputs_a()
        self.__fault.debug_msg(f"{in_a1 = }, {in_a5 = }, {in_a6 = }", 'purple')
        if in_a1 is True and in_a5 is True and in_a6 is False:
            pass
        else:
            self.__fault.debug_msg("тест 2.1.2 положение выходов не соответствует", 'red')
            self.__mysql_conn.mysql_ins_result("неисправен", "2")
            return False
        self.__mysql_conn.mysql_ins_result("исправен", "2")
        return True

    def st_test_30_bzmp_p(self) -> bool:
        """
        Тест 3. Проверка срабатывания блока при снижении силовой изоляции
        """
        if my_msg(self.msg_4):
            pass
        else:
            return False
        self.__resist.resist_kohm(61)
        sleep(2)
        in_a1, in_a5, in_a6 = self.__inputs_a()
        self.__fault.debug_msg(f"{in_a1 = }, {in_a5 = }, {in_a6 = }", 'purple')
        if in_a1 is False and in_a5 is False and in_a6 is True:
            pass
        else:
            self.__fault.debug_msg("тест 3.0 положение выходов не соответствует", 'red')
            self.__mysql_conn.mysql_ins_result("неисправен", "3")
            return False
        return True

    def st_test_31_bzmp_p(self) -> bool:
        self.__resist.resist_kohm(590)
        sleep(2)
        in_a1, in_a5, in_a6 = self.__inputs_a()
        self.__fault.debug_msg(f"{in_a1 = }, {in_a5 = }, {in_a6 = }", 'purple')
        if in_a1 is True and in_a5 is True and in_a6 is False:
            pass
        else:
            self.__fault.debug_msg("тест 3.1 положение выходов не соответствует", 'red')
            self.__mysql_conn.mysql_ins_result("неисправен", "3")
            return False
        self.__mysql_conn.mysql_ins_result("исправен", "3")
        return True

    def st_test_40_bzmp_p(self) -> bool:
        """
        Тест 4. Проверка защиты ПМЗ
        """
        if my_msg(self.msg_5):
            pass
        else:
            return False
        if self.__proc.procedure_x4_to_x5(coef_volt=self.coef_volt, setpoint_volt=self.ust_pmz):
            return True
        self.__mysql_conn.mysql_ins_result("неисправен", "4")
        return False

    def st_test_41_bzmp_p(self) -> bool:
        """
        4.2.  Проверка срабатывания блока от сигнала нагрузки:
        """
        self.__mb_ctrl.ctrl_relay('KL63', True)
        sleep(0.5)
        self.__mb_ctrl.ctrl_relay('KL63', False)
        sleep(1)
        in_a1, in_a5, in_a6 = self.__inputs_a()
        self.__fault.debug_msg(f"{in_a1 = }, {in_a5 = }, {in_a6 = }", 'purple')
        if in_a1 is False and in_a5 is False and in_a6 is True:
            pass
        else:
            self.__fault.debug_msg("положение выходов не соответствует", 'red')
            self.__mysql_conn.mysql_ins_result("неисправен", "4")
            self.__reset.stop_procedure_3()
            return False
        self.__reset.stop_procedure_3()
        return True

    def st_test_42_bzmp_p(self) -> bool:
        """
        4.2.2. Сброс защит после проверки
        """
        self.__sbros_zashit()
        sleep(2)
        in_a1, in_a5, in_a6 = self.__inputs_a()
        if in_a1 is True and in_a5 is True and in_a6 is False:
            pass
        else:
            self.__fault.debug_msg("положение выходов не соответствует", 'red')
            self.__mysql_conn.mysql_ins_result("неисправен", "4")
            return False
        self.__mysql_conn.mysql_ins_result("исправен", "4")
        return True

    def st_test_50_bzmp_p(self) -> bool:
        """
        Тест 5. Проверка защиты от несимметрии фаз
        """
        if my_msg(self.msg_6):
            pass
        else:
            return False
        if self.__proc.procedure_x4_to_x5(coef_volt=self.coef_volt, setpoint_volt=self.ust_faz):
            return True
        self.__mysql_conn.mysql_ins_result("неисправен TV1", "5")
        return False

    def st_test_51_bzmp_p(self) -> bool:
        """
        5.2.  Проверка срабатывания блока от сигнала нагрузки:
        """
        self.__mb_ctrl.ctrl_relay('KL81', True)
        sleep(0.1)
        self.__mb_ctrl.ctrl_relay('KL63', True)
        sleep(2)
        in_b1 = self.__inputs_b()
        i = 0
        while in_b1 is False and i <= 10:
            in_b1 = self.__inputs_b()
            i += 1
        start_timer = time()
        in_a5 = self.__inputs_a5()
        stop_timer = 0
        while in_a5 is True and stop_timer <= 12:
            in_a5 = self.__inputs_a5()
            stop_timer = time() - start_timer
        timer_test_5_2 = stop_timer
        self.__fault.debug_msg(f'таймер тест 6.2: {timer_test_5_2:.1f}', 'orange')
        in_a1, in_a5, in_a6 = self.__inputs_a()
        if in_a1 is False and in_a5 is False and in_a6 is True and timer_test_5_2 <= 12:
            pass
        else:
            self.__fault.debug_msg("положение выходов не соответствует", 'red')
            self.__mysql_conn.mysql_ins_result("неисправен", "5")
            self.__reset.sbros_kl63_proc_all()
            self.__mb_ctrl.ctrl_relay('KL81', False)
            return False
        self.__reset.sbros_kl63_proc_all()
        self.__mb_ctrl.ctrl_relay('KL81', False)
        self.__mb_ctrl.ctrl_relay('KL24', True)
        sleep(4)
        self.__mb_ctrl.ctrl_relay('KL24', False)
        sleep(1)
        in_a1, in_a5, in_a6 = self.__inputs_a()
        if in_a1 is True and in_a5 is True and in_a6 is False:
            pass
        else:
            self.__fault.debug_msg("положение выходов не соответствует", 'red')
            self.__mysql_conn.mysql_ins_result("неисправен", "5")
            return False
        self.__mysql_conn.mysql_ins_result(f'исправен, {timer_test_5_2:.1f} сек', "5")
        return True

    def st_test_60_bzmp_p(self) -> bool:
        """
        Тест 6. Проверка защиты от перегрузки
        """
        if my_msg(self.msg_7):
            pass
        else:
            return False
        if self.__proc.procedure_x4_to_x5(coef_volt=self.coef_volt, setpoint_volt=self.ust_peregruz):
            return True
        self.__mysql_conn.mysql_ins_result("неисправен", "6")
        return False

    def st_test_61_bzmp_p(self) -> bool:
        """
        # 6.2.  Проверка срабатывания блока от сигнала нагрузки:
        """
        self.__mb_ctrl.ctrl_relay('KL63', True)
        sleep(2)
        self.__mysql_conn.progress_level(0.0)
        in_b1 = self.__inputs_b()
        k = 0
        while in_b1 is False and k <= 10:
            in_b1 = self.__inputs_b()
            k += 1
        start_timer = time()
        in_a5 = self.__inputs_a5()
        stop_timer = 0
        while in_a5 is True and stop_timer <= 360:
            in_a5 = self.__inputs_a5()
            stop_timer = time() - start_timer
            self.__mysql_conn.progress_level(stop_timer)
        self.timer_test_6_2 = stop_timer
        self.__fault.debug_msg(f'таймер тест 6.2: {self.timer_test_6_2:.1f}', 'orange')
        self.__mysql_conn.progress_level(0.0)
        in_a1, in_a5, in_a6 = self.__inputs_a()
        if in_a1 is False and in_a5 is False and in_a6 is True and self.timer_test_6_2 <= 360:
            pass
        else:
            self.__fault.debug_msg("положение выходов не соответствует", 'red')
            self.__mysql_conn.mysql_ins_result("неисправен", "6")
            self.__reset.sbros_kl63_proc_all()
            return False
        self.__reset.sbros_kl63_proc_all()
        return True

    def st_test_62_bzmp_p(self) -> bool:
        """
        Выдаем сообщение: «Сработала защита от перегрузки»
        6.6. Сброс защит после проверки
        :return:
        """
        self.__sbros_zashit()
        sleep(2)
        in_a1, in_a5, in_a6 = self.__inputs_a()
        if in_a1 is True and in_a5 is True and in_a6 is False:
            pass
        else:
            self.__fault.debug_msg("положение выходов не соответствует", 'red')
            self.__mysql_conn.mysql_ins_result("неисправен", "6")
            return False
        self.__mysql_conn.mysql_ins_result(f'исправен, {self.timer_test_6_2:.1f} сек', "6")
        return True

    def __sbros_zashit(self):
        self.__mb_ctrl.ctrl_relay('KL24', True)
        sleep(3)
        self.__mb_ctrl.ctrl_relay('KL24', False)

    def __inputs_a0(self):
        in_a0 = self.__read_mb.read_discrete(0)
        if in_a0 is None:
            # logging.error(f'нет связи с контроллером')
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_a0

    def __inputs_a(self):
        in_a1 = self.__read_mb.read_discrete(1)
        in_a5 = self.__read_mb.read_discrete(5)
        in_a6 = self.__read_mb.read_discrete(6)
        if in_a1 is None or in_a5 is None or in_a6 is None:
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_a1, in_a5, in_a6

    def __inputs_a5(self):
        in_a5 = self.__read_mb.read_discrete(5)
        if in_a5 is None:
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_a5

    def __inputs_a6(self):
        in_a6 = self.__read_mb.read_discrete(6)
        if in_a6 is None:
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_a6

    def __inputs_b(self):
        in_b1 = self.__read_mb.read_discrete(9)
        if in_b1 is None:
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_b1

    def st_test_bzmp_p(self) -> bool:
        if self.st_test_10_bzmp_p():
            if self.st_test_11_bzmp_p():
                if self.st_test_12_bzmp_p():
                    if self.st_test_20_bzmp_p():
                        if self.st_test_21_bzmp_p():
                            if self.st_test_30_bzmp_p():
                                if self.st_test_31_bzmp_p():
                                    if self.st_test_40_bzmp_p():
                                        if self.st_test_41_bzmp_p():
                                            if self.st_test_42_bzmp_p():
                                                if self.st_test_50_bzmp_p():
                                                    if self.st_test_51_bzmp_p():
                                                        if self.st_test_60_bzmp_p():
                                                            if self.st_test_61_bzmp_p():
                                                                if self.st_test_62_bzmp_p():
                                                                    return True
        return False


if __name__ == '__main__':
    test_bzmp_p = TestBZMPP()
    reset_test_bzmp_p = ResetRelay()
    mysql_conn_bzmp_p = MySQLConnect()
    fault = Bug(True)
    try:
        if test_bzmp_p.st_test_bzmp_p():
            mysql_conn_bzmp_p.mysql_block_good()
            my_msg('Блок исправен', 'green')
        else:
            mysql_conn_bzmp_p.mysql_block_bad()
            my_msg('Блок неисправен', 'red')
    except OSError:
        my_msg("ошибка системы", 'red')
    except SystemError:
        my_msg("внутренняя ошибка", 'red')
    except ModbusConnectException as mce:
        fault.debug_msg(mce, 'red')
        my_msg(f'{mce}', 'red')
    except HardwareException as hwe:
        my_msg(f'{hwe}', 'red')
    finally:
        reset_test_bzmp_p.reset_all()
        sys.exit()
