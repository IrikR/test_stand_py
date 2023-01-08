#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки

Тип блока	Производитель
БЗМП-Д	ДИГ, ООО

"""

__all__ = ["TestBZMPD"]

import sys
import logging

from time import sleep, time

from .my_msgbox import *
from .gen_func_procedure import *
from .gen_func_utils import *
from .gen_mb_client import *
from .gen_mysql_connect import *


class TestBZMPD(object):

    def __init__(self):
        self.__proc = Procedure()
        self.__reset = ResetRelay()
        self.__resist = Resistor()
        self.__read_mb = ReadMB()
        self.__mb_ctrl = CtrlKL()
        self.__mysql_conn = MySQLConnect()
        self.__fault = Bug(True)

        self.ust_1 = 22.6
        self.ust_2 = 15.0

        self.coef_volt = 0.0
        self.timer_test_5 = 0.0

        self.health_flag: bool = False

        self.msg_1 = "Убедитесь в отсутствии других блоков и подключите блок БЗМП-Д к испытательной панели"
        self.msg_2 = "С помощью кнопок SB1…SB3, расположенных на панели разъемов, " \
                     "установите следующие параметры блока, " \
                     "при их наличии в зависимости от исполнения блока:\n" \
                     "- Номинальный ток: 160А (все исполнения);- Кратность пускового тока: 7.5 (все исполнения);\n" \
                     "- Номинальное рабочее напряжение: 1140В (все исполнения);\n" \
                     "- Перекос фаз по току: 0% (все исполнения); - Датчик тока: ДТК-1 (некоторые исполнения);\n" \
                     "- Режим работы: пускатель (некоторые исполнения) или БРУ ВКЛ, БКИ ВКЛ (некоторые исполнения)"
        self.msg_3 = "С помощью кнопки SB3 перейдите в главное окно меню блока"
        self.msg_4 = "С помощью кнопки SB3 перейдите в главное окно меню блока"
        self.msg_5 = "С помощью кнопки SB3 перейдите в главное окно меню блока"

        logging.basicConfig(filename="C:\Stend\project_class\TestBZMPD.log",
                            filemode="w",
                            level=logging.DEBUG,
                            encoding="utf-8",
                            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('WARNING')
        self.logger = logging.getLogger(__name__)

    def st_test_10_bzmp_d(self) -> bool:
        """
        Тест 1. Проверка исходного состояния блока:
        """
        self.__inputs_a0()
        self.__mysql_conn.mysql_ins_result('идёт тест 1.1', '1')
        self.__mysql_conn.mysql_ins_result('---', '2')
        self.__mysql_conn.mysql_ins_result('---', '3')
        self.__mysql_conn.mysql_ins_result('---', '4')
        self.__mysql_conn.mysql_ins_result('---', '5')
        if my_msg(self.msg_1):
            return True
        else:
            return False

    def st_test_11_bzmp_d(self) -> bool:
        """
        1.1.	Проверка вероятности наличия короткого замыкания на входе измерительной цепи блока
        """
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

    def st_test_12_bzmp_d(self) -> bool:
        """
        1.2. Определение коэффициента Кс отклонения фактического напряжения от номинального
        """
        self.__mysql_conn.mysql_ins_result('идёт тест 1.2', '1')
        self.coef_volt = self.__proc.procedure_1_22_32()
        if self.coef_volt != 0.0:
            pass
        else:
            self.__reset.stop_procedure_32()
            self.__mysql_conn.mysql_ins_result("неисправен TV1", "1")
            return False
        self.__reset.stop_procedure_32()
        return True

    def st_test_13_bzmp_d(self) -> bool:
        """
        Подача напряжения питания ~50В
        """
        self.__mysql_conn.mysql_ins_result('идёт тест 1.3', '1')
        self.__mb_ctrl.ctrl_relay('KL67', True)
        timer_test_1 = 0
        start_timer_test_1 = time()
        while timer_test_1 <= 120:
            self.__mb_ctrl.ctrl_relay('KL24', True)
            sleep(0.2)
            self.__mb_ctrl.ctrl_relay('KL24', False)
            sleep(0.8)
            timer_test_1 = time() - start_timer_test_1
            in_a1, in_a5, in_a6 = self.__inputs_a()
            self.__fault.debug_msg(f'времени прошло\t{timer_test_1:.2f}', 'orange')
            if in_a1 is True and in_a5 is True and in_a6 is False:
                break
            else:
                continue
        sleep(1)
        in_a1, in_a5, in_a6 = self.__inputs_a()
        self.__fault.debug_msg(f'{in_a1 = } (True), {in_a5 = } (True), {in_a6 = } (False)', 'purple')
        if in_a1 is True and in_a5 is True and in_a6 is False:
            pass
        else:
            self.__fault.debug_msg("тест 1.3 положение выходов не соответствует", 'red')
            self.__mysql_conn.mysql_ins_result("неисправен", "1")
            return False
        self.__fault.debug_msg("тест 1.3 положение выходов соответствует", 'green')
        self.__mysql_conn.mysql_ins_result("исправен", "1")
        return True

    def st_test_20_bzmp_d(self) -> bool:
        """
        Тест 2. Проверка срабатывания блока при снижении изоляции цепей 36В
        """
        if my_msg(self.msg_2):
            if my_msg(self.msg_3):
                return True
        return False

    def st_test_21_bzmp_d(self) -> bool:
        self.__fault.debug_msg("идёт тест 2.1", 'blue')
        self.__mysql_conn.mysql_ins_result('идёт тест 2.1', '2')
        self.__mb_ctrl.ctrl_relay('KL21', True)
        sleep(1)
        self.__mb_ctrl.ctrl_relay('KL84', True)
        sleep(5)
        self.__mb_ctrl.ctrl_relay('KL84', False)
        sleep(0.2)
        in_a6 = self.__inputs_a6()
        if in_a6 is True:
            pass
        else:
            self.__fault.debug_msg("тест 2.1 положение выходов не соответствует", 'red')
            self.__mysql_conn.mysql_ins_result("неисправен", "2")
            return False
        self.__fault.debug_msg("тест 2.1 положение выходов соответствует", 'green')
        return True

    def st_test_22_bzmp_d(self) -> bool:
        """
        2.2. Сброс защит после проверки
        """
        self.__fault.debug_msg("идёт тест 2.2", 'blue')
        self.__mysql_conn.mysql_ins_result('идёт тест 2.2', '2')
        self.__mb_ctrl.ctrl_relay('KL24', True)
        sleep(0.3)
        self.__mb_ctrl.ctrl_relay('KL24', False)
        sleep(0.7)
        in_a1, in_a5, in_a6 = self.__inputs_a()
        if in_a1 is True and in_a5 is True and in_a6 is False:
            pass
        else:
            self.__fault.debug_msg("тест 2.2 положение выходов не соответствует", 'red')
            self.__mysql_conn.mysql_ins_result("неисправен", "2")
            return False
        self.__mysql_conn.mysql_ins_result("исправен", "2")
        self.__fault.debug_msg("тест 2.2 положение выходов соответствует", 'green')
        return True

    def st_test_30_bzmp_d(self) -> bool:
        """
        Тест 3. Проверка срабатывания блока при снижении силовой изоляции
        """
        self.__fault.debug_msg("идёт тест 3.0", 'blue')
        if my_msg(self.msg_4):
            pass
        else:
            return False
        self.__mysql_conn.mysql_ins_result('идёт тест 3.1', '3')
        self.__resist.resist_kohm(61)
        sleep(5)
        in_a1, in_a5, in_a6 = self.__inputs_a()
        self.__fault.debug_msg(f'{in_a1 = } (False), {in_a5 = } (False), {in_a6 = } (True)', 'orange')
        if in_a1 is False and in_a5 is False and in_a6 is True:
            pass
        else:
            self.__fault.debug_msg("тест 3.0 положение выходов не соответствует", 'red')
            self.__mysql_conn.mysql_ins_result("неисправен", "3")
            return False
        self.__fault.debug_msg("тест 3.0 положение выходов соответствует", 'green')
        return True

    def st_test_31_bzmp_d(self) -> bool:
        self.__fault.debug_msg("идёт тест 3.1", 'blue')
        self.__resist.resist_kohm(590)
        sleep(2)
        self.__mysql_conn.mysql_ins_result('идёт тест 3.2', '3')
        self.__mb_ctrl.ctrl_relay('KL24', True)
        sleep(0.3)
        self.__mb_ctrl.ctrl_relay('KL24', False)
        sleep(1)
        in_a1, in_a5, in_a6 = self.__inputs_a()
        self.__fault.debug_msg(f'{in_a1 = } (True), {in_a5 = } (True), {in_a6 = } (False)', 'purple')
        if in_a1 is True and in_a5 is True and in_a6 is False:
            pass
        else:
            self.__fault.debug_msg("тест 3.1 положение выходов не соответствует", 'red')
            self.__mysql_conn.mysql_ins_result("неисправен", "3")
            return False
        self.__fault.debug_msg("тест 3.1 положение выходов соответствует", 'green')
        self.__mysql_conn.mysql_ins_result("исправен", "3")
        return True

    def st_test_40_bzmp_d(self) -> bool:
        """
        Тест 4. Проверка защиты ПМЗ
        """
        self.__fault.debug_msg("идёт тест 4.0", 'blue')
        if my_msg(self.msg_5):
            pass
        else:
            return False
        self.__mysql_conn.mysql_ins_result('идёт тест 4.1', '4')
        if self.__proc.procedure_x4_to_x5(coef_volt=self.coef_volt, setpoint_volt=self.ust_1):
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", "4")
            return False
        return True

    def st_test_41_bzmp_d(self) -> bool:
        """
        4.2.  Проверка срабатывания блока от сигнала нагрузки:
        """
        self.__fault.debug_msg("идёт тест 4.1", 'blue')
        self.__mysql_conn.mysql_ins_result('идёт тест 4.2', '4')
        self.__mb_ctrl.ctrl_relay('KL63', True)
        sleep(0.5)
        self.__mb_ctrl.ctrl_relay('KL63', False)
        in_a1, in_a5, in_a6 = self.__inputs_a()
        if in_a1 is False and in_a5 is False and in_a6 is True:
            pass
        else:
            self.__fault.debug_msg("положение выходов не соответствует", 'red')
            self.__mysql_conn.mysql_ins_result("неисправен", "4")
            self.__reset.stop_procedure_3()
            return False
        self.__fault.debug_msg("положение выходов соответствует", 'green')
        self.__reset.stop_procedure_3()
        return True

    def st_test_42_bzmp_d(self) -> bool:
        self.__fault.debug_msg("идёт тест 4.2", 'blue')
        self.__mysql_conn.mysql_ins_result('идёт тест 4.3', '4')
        self.__mb_ctrl.ctrl_relay('KL24', True)
        sleep(0.3)
        self.__mb_ctrl.ctrl_relay('KL24', False)
        sleep(0.7)
        in_a1, in_a5, in_a6 = self.__inputs_a()
        if in_a1 is True and in_a5 is True and in_a6 is False:
            pass
        else:
            self.__fault.debug_msg("положение выходов не соответствует", 'red')
            self.__mysql_conn.mysql_ins_result("неисправен", "4")
            return False
        self.__fault.debug_msg("положение выходов соответствует", 'green')
        self.__mysql_conn.mysql_ins_result("исправен", "4")
        return True

    def st_test_50_bzmp_d(self) -> bool:
        """
        Тест 5. Проверка защиты от перегрузки
        """
        self.__fault.debug_msg("идёт тест 5.0", 'blue')
        self.__mysql_conn.mysql_ins_result('идёт тест 5.1', '5')
        if self.__proc.procedure_x4_to_x5(coef_volt=self.coef_volt, setpoint_volt=self.ust_2):
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен TV1", "4")
            return False
        return True

    def st_test_51_bzmp_d(self) -> bool:
        """
        5.2.  Проверка срабатывания блока от сигнала нагрузки:
        """
        self.__fault.debug_msg("идёт тест 5.1", 'blue')
        self.__mysql_conn.mysql_ins_result('идёт тест 5.2', '5')
        self.__mb_ctrl.ctrl_relay('KL63', True)
        self.__mysql_conn.progress_level(0.0)
        in_b1 = self.__inputs_b()
        k = 0
        while in_b1 is False and k <= 10:
            in_b1 = self.__inputs_b()
            k += 1
        start_timer_test_5 = time()
        in_a5 = self.__inputs_a5()
        stop_timer = 0
        while in_a5 is True and stop_timer <= 360:
            in_a5 = self.__inputs_a5()
            sleep(0.2)
            stop_timer_test_5 = time() - start_timer_test_5
            self.__fault.debug_msg(f'таймер тест 5: {stop_timer_test_5:.1f}', 'orange')
            self.__mysql_conn.progress_level(stop_timer_test_5)
        stop_timer_test_5 = time()
        self.timer_test_5 = stop_timer_test_5 - start_timer_test_5
        self.__mysql_conn.progress_level(0.0)
        self.__fault.debug_msg(f'таймер тест 5: {self.timer_test_5:.1f}', 'orange')
        sleep(2)
        self.__mysql_conn.mysql_ins_result('идёт тест 5.2', '5')
        in_a1, in_a5, in_a6 = self.__inputs_a()
        if in_a1 is False and in_a5 is False and in_a6 is True and self.timer_test_5 <= 360:
            pass
        else:
            self.__fault.debug_msg("положение выходов не соответствует", 'red')
            self.__mysql_conn.mysql_ins_result("неисправен", "5")
            self.__reset.sbros_kl63_proc_all()
            return False
        self.__fault.debug_msg("положение выходов соответствует", 'green')
        self.__reset.sbros_kl63_proc_all()
        return True

    def st_test_52_bzmp_d(self) -> bool:
        self.__fault.debug_msg("идёт тест 5.2", 'blue')
        self.__mysql_conn.mysql_ins_result('идёт тест 5.3', '5')
        self.__sbros_zashit()
        in_a1, in_a5, in_a6 = self.__inputs_a()
        if in_a1 is True and in_a5 is True and in_a6 is False:
            pass
        else:
            self.__fault.debug_msg("положение выходов не соответствует", 'red')
            self.__mysql_conn.mysql_ins_result("неисправен", "5")
            return False
        self.__fault.debug_msg("положение выходов соответствует", 'green')
        self.__mysql_conn.mysql_ins_result(f'исправен, {self.timer_test_5:.1f} сек', "5")
        return True

    def __sbros_zashit(self):
        self.__mb_ctrl.ctrl_relay('KL24', True)
        sleep(3)
        self.__mb_ctrl.ctrl_relay('KL24', False)
        sleep(0.7)

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

    def st_test_bzmp_d(self) -> bool:
        if self.st_test_10_bzmp_d():
            if self.st_test_11_bzmp_d():
                if self.st_test_12_bzmp_d():
                    if self.st_test_13_bzmp_d():
                        if self.st_test_20_bzmp_d():
                            if self.st_test_21_bzmp_d():
                                if self.st_test_22_bzmp_d():
                                    if self.st_test_30_bzmp_d():
                                        if self.st_test_31_bzmp_d():
                                            if self.st_test_40_bzmp_d():
                                                if self.st_test_41_bzmp_d():
                                                    if self.st_test_42_bzmp_d():
                                                        if self.st_test_50_bzmp_d():
                                                            if self.st_test_51_bzmp_d():
                                                                if self.st_test_52_bzmp_d():
                                                                    return True
        return False

    def full_test_bzmp_d(self):
        try:
            if self.st_test_bzmp_d():
                self.__mysql_conn.mysql_block_good()
                my_msg('Блок исправен', 'green')
            else:
                self.__mysql_conn.mysql_block_bad()
                my_msg('Блок неисправен', 'red')
        except OSError:
            my_msg("ошибка системы", 'red')
        except SystemError:
            my_msg("внутренняя ошибка", 'red')
        except ModbusConnectException as mce:
            self.__fault.debug_msg(mce, 'red')
            my_msg(f'{mce}', 'red')
        except HardwareException as hwe:
            my_msg(f'{hwe}', 'red')
        finally:
            self.__reset.reset_all()
            sys.exit()


if __name__ == '__main__':
    test_bzmp_d = TestBZMPD()
    test_bzmp_d.full_test_bzmp_d()
    # reset_test_bzmp_d = ResetRelay()
    # mysql_conn_bzmp_d = MySQLConnect()
    # fault = Bug(True)
    # try:
    #     if test_bzmp_d.st_test_bzmp_d():
    #         mysql_conn_bzmp_d.mysql_block_good()
    #         my_msg('Блок исправен', 'green')
    #     else:
    #         mysql_conn_bzmp_d.mysql_block_bad()
    #         my_msg('Блок неисправен', 'red')
    # except OSError:
    #     my_msg("ошибка системы", 'red')
    # except SystemError:
    #     my_msg("внутренняя ошибка", 'red')
    # except ModbusConnectException as mce:
    #     fault.debug_msg(mce, 'red')
    #     my_msg(f'{mce}', 'red')
    # except HardwareException as hwe:
    #     my_msg(f'{hwe}', 'red')
    # finally:
    #     reset_test_bzmp_d.reset_all()
    #     sys.exit()
