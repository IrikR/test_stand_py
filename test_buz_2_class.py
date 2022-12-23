#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки

Тип блока	Производитель
БУЗ-2	Строй-энергомаш
БУЗ-2	ТЭТЗ-Инвест
БУЗ-2	нет производителя

"""

__all__ = ["TestBUZ2"]

import sys
import logging

from time import sleep, time

from my_msgbox import *
from gen_func_procedure import *
from gen_func_utils import *
from gen_mb_client import *
from gen_mysql_connect import *


class TestBUZ2(object):

    def __init__(self):
        self.__proc = Procedure()
        self.__reset = ResetRelay()
        self.__read_mb = ReadMB()
        self.__mb_ctrl = CtrlKL()
        self.__mysql_conn = MySQLConnect()
        self.__fault = Bug(True)

        self.ust_1 = 75.8
        self.ust_2 = 20.3

        self.coef_volt: float = 0.0
        self.health_flag: bool = False

        self.msg_1 = "Убедитесь в отсутствии блоков в панелях разъемов. " \
                     "Вставьте испытуемый блок БУЗ-2 в разъем Х17 на панели B."
        self.msg_2 = "Вставьте заведомо исправные блок БИ в разъем Х26  и блок БДЗ в разъем Х16, " \
                     "расположенные на панели B."
        self.msg_3 = "Установите с помощью кнопок SB1, SB2 следующие уровни уставок: ПМЗ – 2000 А; ТЗП – 400 А"

        logging.basicConfig(filename="C:\Stend\project_class\TestBUZ2.log",
                            filemode="w",
                            level=logging.DEBUG,
                            encoding="utf-8",
                            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('WARNING')
        self.logger = logging.getLogger(__name__)

    def st_test_10_buz_2(self) -> bool:
        """
        Тест 1. Включение/выключение блока в нормальном режиме:
        """
        self.__inputs_a0()
        if my_msg(self.msg_1):
            if my_msg(self.msg_2):
                return True
        return False

    def st_test_11_buz_2(self) -> bool:
        """
        1.1.	Проверка вероятности наличия короткого замыкания на входе измерительной цепи блока
        """
        self.__fault.debug_msg("тестим шкаф", 3)
        meas_volt_ust = self.__proc.procedure_1_21_31()
        if meas_volt_ust != 0.0:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", "1")
            return False
        self.__mb_ctrl.ctrl_relay('KL73', True)
        sleep(5)
        self.__mb_ctrl.ctrl_relay('KL90', True)
        sleep(5)
        self.__mb_ctrl.ctrl_relay('KL63', True)
        min_volt = 0.6 * meas_volt_ust
        max_volt = 1.0 * meas_volt_ust
        meas_volt = self.__read_mb.read_analog()
        self.__fault.debug_msg(f'напряжение после включения KL63\t{meas_volt}\t'
                               f'должно быть от\t{min_volt}\tдо\t{max_volt}', 3)
        if min_volt <= meas_volt <= max_volt:
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '1')
            self.__mysql_conn.mysql_error(455)
            self.__reset.sbros_kl63_proc_1_21_31()
            return False
        self.__reset.sbros_kl63_proc_1_21_31()
        return True

    def st_test_12_buz_2(self) -> bool:
        """
        1.2. Определение коэффициента Кс отклонения фактического напряжения от номинального
        """
        self.__fault.debug_msg("вычисляем коэффициент сети", 3)
        self.coef_volt = self.__proc.procedure_1_22_32()
        if self.coef_volt != 0.0:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", "1")
            return False
        self.__reset.stop_procedure_32()
        self.__fault.debug_msg("включаем хуеву тучу релюшек", 3)
        self.__mb_ctrl.ctrl_relay('KL21', True)
        self.__mb_ctrl.ctrl_relay('KL2', True)
        self.__mb_ctrl.ctrl_relay('KL66', True)
        sleep(6)
        self.__mb_ctrl.ctrl_relay('KL84', True)
        sleep(2)
        self.__mb_ctrl.ctrl_relay('KL84', False)
        sleep(1)
        self.__mb_ctrl.ctrl_relay('KL80', True)
        sleep(0.1)
        self.__mb_ctrl.ctrl_relay('KL24', True)
        sleep(5)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is True and in_a2 is True:
            pass
        else:
            self.__fault.debug_msg("тест 1.3 положение выходов не соответствует", 1)
            self.__mysql_conn.mysql_ins_result("неисправен", "1")
            return False
        self.__fault.debug_msg("тест 1.3 положение выходов соответствует", 4)
        return True

    def st_test_13_buz_2(self) -> bool:
        """
        1.4.	Выключение блока
        """
        sleep(1)
        self.__mb_ctrl.ctrl_relay('KL80', False)
        sleep(0.1)
        self.__mb_ctrl.ctrl_relay('KL24', False)
        sleep(5)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is False and in_a2 is False:
            pass
        else:
            self.__fault.debug_msg("тест 1.4 положение выходов не соответствует", 1)
            self.__mysql_conn.mysql_ins_result("неисправен", "1")
            return False
        self.__fault.debug_msg("тест 1.4 положение выходов соответствует", 4)
        self.__mysql_conn.mysql_ins_result("исправен", "1")
        return True

    def st_test_20_buz_2(self) -> bool:
        """
        Тест 2. Проверка работоспособности защиты МТЗ:
        2.1. Пуск блока
        """
        self.__fault.debug_msg("тест 2 начало", 3)
        self.__mb_ctrl.ctrl_relay('KL66', False)
        sleep(0.3)
        self.__mb_ctrl.ctrl_relay('KL82', True)
        sleep(0.3)
        self.__mb_ctrl.ctrl_relay('KL66', True)
        if my_msg(self.msg_3):
            pass
        else:
            return False
        self.__fault.debug_msg("включаем хуеву тучу релюшек", 3)
        self.__mb_ctrl.ctrl_relay('KL66', False)
        sleep(1)
        self.__mb_ctrl.ctrl_relay('KL82', False)
        sleep(1)
        self.__mb_ctrl.ctrl_relay('KL66', True)
        sleep(1)
        self.__mb_ctrl.ctrl_relay('KL84', True)
        sleep(2)
        self.__mb_ctrl.ctrl_relay('KL84', False)
        sleep(1)
        self.__mb_ctrl.ctrl_relay('KL80', True)
        sleep(0.1)
        self.__mb_ctrl.ctrl_relay('KL24', True)
        sleep(2)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is True and in_a2 is True:
            pass
        else:
            self.__fault.debug_msg("тест 2.1 положение выходов не соответствует", 1)
            self.__mysql_conn.mysql_ins_result("неисправен", "2")
            return False
        self.__fault.debug_msg("тест 2.1 положение выходов соответствует", 4)
        return True

    def st_test_21_buz_2(self) -> bool:
        if self.__proc.procedure_x4_to_x5(coef_volt=self.coef_volt, setpoint_volt=self.ust_1):
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", "2")
            return False
        self.__mb_ctrl.ctrl_relay('KL63', True)
        sleep(0.5)
        self.__mb_ctrl.ctrl_relay('KL63', False)
        sleep(2)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is False and in_a2 is False:
            pass
        else:
            self.__fault.debug_msg("тест 2.1 положение выходов не соответствует", 1)
            self.__reset.stop_procedure_3()
            self.__mysql_conn.mysql_ins_result("неисправен", "2")
            return False
        self.__fault.debug_msg("тест 2.1 положение выходов соответствует", 4)
        self.__reset.stop_procedure_3()
        return True

    def st_test_22_buz_2(self) -> bool:
        """
        2.3.  Финишные операции при положительном завершении теста:
        """
        self.__fault.debug_msg("включаем хуеву тучу релюшек", 3)
        self.__mb_ctrl.ctrl_relay('KL80', False)
        self.__mb_ctrl.ctrl_relay('KL24', False)
        sleep(6)
        self.__mb_ctrl.ctrl_relay('KL84', True)
        sleep(2)
        self.__mb_ctrl.ctrl_relay('KL84', False)
        sleep(1)
        self.__mysql_conn.mysql_ins_result("исправен", "2")
        return True

    def st_test_30_buz_2(self) -> bool:
        """
        Тест 3. Проверка работоспособности защиты ТЗП
        3.1. Пуск блока
        """
        self.__mb_ctrl.ctrl_relay('KL80', True)
        sleep(0.1)
        self.__mb_ctrl.ctrl_relay('KL24', True)
        sleep(2)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is True and in_a2 is True:
            pass
        else:
            self.__fault.debug_msg("тест 3.1 положение выходов не соответствует", 1)
            self.__mysql_conn.mysql_ins_result("неисправен", "3")
            return False
        self.__fault.debug_msg("тест 3.1 положение выходов соответствует", 4)
        return True

    def st_test_31_buz_2(self) -> bool:
        if self.__proc.procedure_x4_to_x5(coef_volt=self.coef_volt, setpoint_volt=self.ust_2):
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", "3")
            return False
        self.__mb_ctrl.ctrl_relay('KL63', True)
        in_b1 = self.__inputs_b()
        k = 0
        while in_b1 is False and k <= 10:
            in_b1 = self.__inputs_b()
            k += 1
        start_timer = time()
        in_a1 = self.__inputs_a1()
        stop_timer = 0
        while in_a1 is True and stop_timer <= 360:
            in_a1 = self.__inputs_a1()
            stop_timer = time() - start_timer
            self.__fault.debug_msg(f'таймер тест 3.2 {stop_timer}', 2)
        timer_test_3 = stop_timer
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is False and in_a2 is False and timer_test_3 <= 360:
            pass
        else:
            self.__fault.debug_msg("тест 3.2 положение выходов не соответствует", 1)
            self.__mysql_conn.mysql_ins_result("неисправен", "3")
            self.__reset.sbros_kl63_proc_all()
            return False
        self.__fault.debug_msg("тест 3.2 положение выходов соответствует", 4)
        self.__reset.sbros_kl63_proc_all()
        self.__mysql_conn.mysql_ins_result(f'исправен, {timer_test_3:.1f} сек', "3")
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
        if in_a1 is None or in_a2 is None:
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_a1, in_a2

    def __inputs_a1(self):
        in_a1 = self.__read_mb.read_discrete(1)
        if in_a1 is None:
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_a1

    def __inputs_b(self):
        in_b1 = self.__read_mb.read_discrete(9)
        if in_b1 is None:
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_b1

    def st_test_buz_2(self) -> bool:
        if self.st_test_10_buz_2():
            if self.st_test_11_buz_2():
                if self.st_test_12_buz_2():
                    if self.st_test_13_buz_2():
                        if self.st_test_20_buz_2():
                            if self.st_test_21_buz_2():
                                if self.st_test_22_buz_2():
                                    if self.st_test_30_buz_2():
                                        if self.st_test_31_buz_2():
                                            return True
        return False


if __name__ == '__main__':
    test_buz_2 = TestBUZ2()
    reset_test_buz_2 = ResetRelay()
    mysql_conn_buz_2 = MySQLConnect()
    fault = Bug(True)
    try:
        if test_buz_2.st_test_buz_2():
            mysql_conn_buz_2.mysql_block_good()
            my_msg('Блок исправен', 'green')
        else:
            mysql_conn_buz_2.mysql_block_bad()
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
        reset_test_buz_2.reset_all()
        sys.exit()
