#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки

Тип блока	Производитель
МТЗП-2	Frecon
"""

import sys
import logging

from time import sleep, time

from gen_func_procedure import *
from gen_func_utils import *
from my_msgbox import *
from gen_mb_client import *
from gen_mysql_connect import *

__all__ = ["TestMTZP2"]


class TestMTZP2(object):

    def __init__(self):
        self.__reset = ResetRelay()
        self.__proc = Procedure()
        self.__resist = Resistor()
        self.__read_mb = ReadMB()
        self.__ctrl_kl = CtrlKL()
        self.__mysql_conn = MySQLConnect()
        self.__fault = Bug(True)

        self.ust_1 = 10.9 * 8.2
        self.ust_2 = 8.2 * 8.2
        self.ust_3 = 5.5 * 8.2

        self.meas_volt_ust = 0.0
        self.coef_volt = 0.0
        self.health_flag: bool = False

        self.msg_1 = "Убедитесь в отсутствии других блоков и подключите блок МТЗП-2 в соответствующие разъемы"
        self.msg_2 = "С помощью кнопок на лицевой панели установите следующие значения режима МТЗ-1:\n " \
                     "- Защита введена: ДА; - Уставка по току: 400А;\n" \
                     " - Уставка по времени: 20 мс; - Отключение КА – ДА."
        self.msg_3 = "С помощью кнопок на лицевой панели установите следующие значения режима МТЗ-2:\n" \
                     " - Защита введена: ДА; - Уставка по току: 300А; \n" \
                     "- Уставка по времени: 31000 мс; - Отключение КА – ДА."
        self.msg_4 = "С помощью кнопок на лицевой панели установите следующие значения режима УМТЗ: \n" \
                     "- Защита введена: ДА; - Уставка по току: 300А; \n" \
                     "- Уставка по времени: 20 мс; - Отключение КА – ДА."
        self.msg_5 = "С помощью кнопок на лицевой панели установите следующие значения режима МТЗ-3: \n" \
                     "- Защита введена: ДА; - Уставка по току: 200А; \n" \
                     "- Уставка по времени: 60000 мс; - Отключение КА – ДА."

        logging.basicConfig(filename="C:\Stend\project_class\TestMTZP2.log",
                            filemode="w",
                            level=logging.DEBUG,
                            encoding="utf-8",
                            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('WARNING')
        self.logger = logging.getLogger(__name__)

    def st_test_10(self) -> bool:
        """
        Подтест 1.0
        :return: bool
        """
        self.__inputs_a0()
        if my_msg(self.msg_1):
            pass
        else:
            return False
        self.__fault.debug_msg('тест 1.1', 'blue')
        self.__mysql_conn.mysql_ins_result("идёт тест 1.2", '1')
        return True

    def st_test_11(self) -> bool:
        """
        Подтест 1.1
        :return: bool
        """
        self.meas_volt_ust = self.__proc.procedure_1_21_31()
        if self.meas_volt_ust != 0.0:
            return True
        else:
            self.__reset.stop_procedure_31()
            return False

    def st_test_12(self) -> bool:
        """
        Подтест 1.1 продолжение
        :return: bool
        """
        self.__ctrl_kl.ctrl_relay('KL73', True)
        sleep(5)
        self.__ctrl_kl.ctrl_relay('KL91', True)
        sleep(5)
        self.__ctrl_kl.ctrl_relay('KL63', True)
        meas_volt = self.__read_mb.read_analog()
        min_volt = 0.8 * self.meas_volt_ust
        max_volt = 1.0 * self.meas_volt_ust
        self.__fault.debug_msg(f'измеренное напряжение\t{min_volt:.2f} <= {meas_volt:.2f} <= {max_volt:.2f}', 'orange')
        if min_volt <= meas_volt <= max_volt:
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '1')
            self.__reset.sbros_kl63_proc_1_21_31()
            return False
        self.__reset.sbros_kl63_proc_1_21_31()
        return True

    def st_test_13(self) -> bool:
        """
        1.2. Определение коэффициента Кс отклонения фактического напряжения от номинального.
        :return: bool
        """
        self.__fault.debug_msg('тест 1.3', 'blue')
        self.__mysql_conn.mysql_ins_result("идёт тест 1.4", '1')
        self.coef_volt = self.__proc.procedure_1_22_32()
        if self.coef_volt != 0.0:
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '1')
            self.__reset.stop_procedure_32()
            return False
        self.__reset.stop_procedure_32()
        self.__fault.debug_msg('тест 1.3 завершён', 'green')
        return True

    def st_test_14(self) -> bool:
        """
        Подтест 1.3
        :return: bool
        """
        self.__ctrl_kl.ctrl_relay('KL88', True)
        sleep(10)
        self.__ctrl_kl.ctrl_relay('KL24', True)
        self.__ctrl_kl.ctrl_relay('KL24', False)
        sleep(10)
        self.__ctrl_kl.ctrl_relay('KL84', True)
        sleep(0.5)
        self.__ctrl_kl.ctrl_relay('KL84', False)
        sleep(1)
        in_a1, in_b2 = self.__inputs_a1_b2()
        if in_b2 is True and in_a1 is False:
            pass
        else:
            self.__fault.debug_msg('тест 1.3 положение выходов не соответствует', 'red')
            self.__mysql_conn.mysql_ins_result('неисправен', '1')
            return False
        self.__mysql_conn.mysql_ins_result('исправен', '1')
        self.__fault.debug_msg('тест 1.3 положение выходов соответствует', 'green')
        return True

    def st_test_20(self) -> bool:
        """
        Тест 2. Пуск и стоп от выносного пульта:
        :return: bool
        """
        self.__mysql_conn.mysql_ins_result('идёт тест 2.1', '2')
        self.__ctrl_kl.ctrl_relay('KL92', True)
        sleep(1)
        self.__ctrl_kl.ctrl_relay('KL93', True)
        sleep(0.5)
        self.__ctrl_kl.ctrl_relay('KL93', False)
        sleep(2)
        in_a1, in_b2 = self.__inputs_a1_b2()
        if in_b2 is False and in_a1 is True:
            pass
        else:
            self.__fault.debug_msg('тест 2.1 положение выходов не соответствует', 'red')
            self.__mysql_conn.mysql_ins_result('неисправен', '2')
            return False
        return True

    def st_test_21(self) -> bool:
        """
        Подтест 2.2
        :return: bool
        """
        self.__mysql_conn.mysql_ins_result('идёт тест 2.2', '2')
        self.__fault.debug_msg('тест 2.1 положение выходов соответствует', 'green')
        sleep(0.5)
        self.__ctrl_kl.ctrl_relay('KL94', True)
        sleep(1)
        self.__ctrl_kl.ctrl_relay('KL94', False)
        sleep(2)
        in_a1, in_b2 = self.__inputs_a1_b2()
        if in_b2 is True and in_a1 is False:
            pass
        else:
            self.__fault.debug_msg('тест 2.2 положение выходов не соответствует', 'red')
            self.__mysql_conn.mysql_ins_result('неисправен', '2')
            return False
        self.__fault.debug_msg('тест 2.2 положение выходов соответствует', 'green')
        self.__mysql_conn.mysql_ins_result('исправен', '2')
        return True

    def st_test_30(self) -> bool:
        """
        Тест 3. Пуск и стоп от пульта дистанционного управления:
        :return: bool
        """
        self.__mysql_conn.mysql_ins_result('идёт тест 3.1', '3')
        self.__resist.resist_ohm(0)
        sleep(1)
        self.__ctrl_kl.ctrl_relay('KL12', True)
        sleep(0.5)
        in_a1, in_b2 = self.__inputs_a1_b2()
        if in_b2 is False and in_a1 is True:
            pass
        else:
            self.__fault.debug_msg('тест 3.1 положение выходов не соответствует', 'red')
            self.__mysql_conn.mysql_ins_result('неисправен', '3')
            return False
        self.__mysql_conn.mysql_ins_result('идёт тест 3.2', '3')
        self.__fault.debug_msg('тест 3.1 положение выходов соответствует', 'green')
        return True

    def st_test_31(self) -> bool:
        """
        Подтест 3.2
        :return: bool
        """
        self.__ctrl_kl.ctrl_relay('KL25', True)
        self.__resist.resist_ohm(255)
        sleep(0.5)
        in_a1, in_b2 = self.__inputs_a1_b2()
        if in_b2 is False and in_a1 is True:
            pass
        else:
            self.__fault.debug_msg('тест 3.2 положение выходов не соответствует', 'red')
            self.__mysql_conn.mysql_ins_result('неисправен', '3')
            return False
        self.__fault.debug_msg('тест 3.2 положение выходов соответствует', 'green')
        return True

    def st_test_32(self) -> bool:
        """
        Подтест 3.3
        :return: bool
        """
        self.__mysql_conn.mysql_ins_result('идёт тест 3.3', '3')
        self.__ctrl_kl.ctrl_relay('KL12', False)
        sleep(0.2)
        self.__ctrl_kl.ctrl_relay('KL12', True)
        in_a1, in_b2 = self.__inputs_a1_b2()
        if in_b2 is True and in_a1 is False:
            pass
        else:
            self.__fault.debug_msg('тест 3.3 положение выходов не соответствует', 'red')
            self.__mysql_conn.mysql_ins_result('неисправен', '3')
            return False
        self.__fault.debug_msg('тест 3.3 положение выходов соответствует', 'green')
        self.__ctrl_kl.ctrl_relay('KL12', False)
        self.__ctrl_kl.ctrl_relay('KL25', False)
        self.__resist.resist_ohm(255)
        self.__mysql_conn.mysql_ins_result('исправен', '3')
        return True

    def st_test_40(self) -> bool:
        """
        Тест 4. Проверка защиты МТЗ-1
        :return: bool
        """
        if my_msg(self.msg_2):
            pass
        else:
            return False
        self.__mysql_conn.mysql_ins_result('идёт тест 4.1', '4')
        self.__resist.resist_ohm(0)
        self.__ctrl_kl.ctrl_relay('KL12', True)
        sleep(0.5)
        in_a1, in_b2 = self.__inputs_a1_b2()
        if in_b2 is False and in_a1 is True:
            pass
        else:
            self.__fault.debug_msg('тест 4.1 положение выходов не соответствует', 'red')
            self.__mysql_conn.mysql_ins_result('неисправен', '4')
            return False
        self.__fault.debug_msg('тест 4.1 положение выходов соответствует', 'green')
        return True

    def st_test_41(self) -> bool:
        """
        4.2.  Проверка срабатывания блока от сигнала нагрузки:
        :return: bool
        """
        if self.__proc.procedure_x4_to_x5(setpoint_volt=self.ust_1, coef_volt=self.coef_volt):
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен TV1', '4')
            return False
        self.__mysql_conn.mysql_ins_result('идёт тест 4.2', '4')
        self.__ctrl_kl.ctrl_relay('KL63', True)
        sleep(0.5)
        self.__ctrl_kl.ctrl_relay('KL63', False)
        in_a1, in_b2 = self.__inputs_a1_b2()
        if in_b2 is True and in_a1 is False:
            pass
        else:
            self.__reset.stop_procedure_3()
            self.__fault.debug_msg('тест 4.2 положение выходов не соответствует', 'red')
            self.__mysql_conn.mysql_ins_result('неисправен', '4')
            return False
        self.__fault.debug_msg('тест 4.2 положение выходов соответствует', 'green')
        self.__reset.stop_procedure_3()
        self.__ctrl_kl.ctrl_relay('KL12', False)
        self.__ctrl_kl.ctrl_relay('KL24', True)
        sleep(0.5)
        self.__ctrl_kl.ctrl_relay('KL24', False)
        sleep(0.5)
        self.__ctrl_kl.ctrl_relay('KL84', True)
        sleep(0.5)
        self.__ctrl_kl.ctrl_relay('KL84', False)
        self.__mysql_conn.mysql_ins_result('исправен', '4')
        return True

    def st_test_50(self) -> bool:
        """
        Тест 5. Проверка защиты МТЗ-2
        :return: bool
        """
        if my_msg(self.msg_3):
            pass
        else:
            return False
        self.__mysql_conn.mysql_ins_result('идёт тест 5.1', '5')
        self.__resist.resist_ohm(0)
        sleep(1)
        self.__ctrl_kl.ctrl_relay('KL12', True)
        sleep(1)
        self.__ctrl_kl.ctrl_relay('KL25', True)
        sleep(1)
        self.__resist.resist_ohm(255)
        sleep(0.5)
        in_a1, in_b2 = self.__inputs_a1_b2()
        if in_b2 is False and in_a1 is True:
            pass
        else:
            self.__fault.debug_msg('тест 5.1 положение выходов не соответствует', 'red')
            self.__mysql_conn.mysql_ins_result('неисправен', '5')
            return False
        self.__fault.debug_msg('тест 5.1 положение выходов соответствует', 'green')
        return True

    def st_test_51(self) -> bool:
        """
        Продолжение теста 5
        :return: boolean
        """
        self.__mysql_conn.mysql_ins_result('идёт тест 5.2', '5')
        if self.__proc.procedure_x4_to_x5(setpoint_volt=self.ust_2, coef_volt=self.coef_volt):
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен TV1', '5')
            return False
        self.__mysql_conn.mysql_ins_result('идёт тест 5.3', '5')
        self.__ctrl_kl.ctrl_relay('KL63', True)
        start_timer = time()
        __timer = 0
        in_a1, in_b2 = self.__inputs_a1_b2()
        while (in_a1 is True or in_b2 is False) and __timer <= 41:
            sleep(0.2)
            in_a1, in_b2 = self.__inputs_a1_b2()
            __timer = time() - start_timer
            self.__fault.debug_msg(f'времени прошло\t{__timer}', 'orange')
        in_a1, in_b2 = self.__inputs_a1_b2()
        if in_b2 is True and in_a1 is False and __timer <= 35:
            pass
        else:
            self.__fault.debug_msg('тест 5.3 положение выходов не соответствует', 'red')
            self.__mysql_conn.mysql_ins_result('неисправен', '5')
            return False
        self.__fault.debug_msg('тест 5.3 положение выходов соответствует', 'green')
        self.__ctrl_kl.ctrl_relay('KL63', False)
        self.__reset.stop_procedure_3()
        self.sbros_mtzp()
        self.__mysql_conn.mysql_ins_result('исправен', '5')
        return True

    def st_test_60(self) -> bool:
        """
        Тест 6. Проверка защиты УМТЗ
        :return: boolean
        """
        if my_msg(self.msg_4):
            pass
        else:
            return False
        self.__mysql_conn.mysql_ins_result('идёт тест 6.1', '6')
        self.__resist.resist_ohm(0)
        if self.__proc.procedure_x4_to_x5(setpoint_volt=self.ust_2, coef_volt=self.coef_volt):
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен TV1', '6')
            return False
        self.__ctrl_kl.ctrl_relay('KL63', True)
        self.__ctrl_kl.ctrl_relay('KL12', True)
        sleep(0.2)
        self.__ctrl_kl.ctrl_relay('KL25', True)
        self.__resist.resist_ohm(255)
        sleep(0.5)
        self.__ctrl_kl.ctrl_relay('KL63', False)
        sleep(0.2)
        in_a1, in_b2 = self.__inputs_a1_b2()
        if in_b2 is True and in_a1 is False:
            pass
        else:
            self.__reset.stop_procedure_3()
            self.__fault.debug_msg('тест 6.1 положение выходов не соответствует', 'red')
            self.__mysql_conn.mysql_ins_result('неисправен', '6')
            return False
        self.__fault.debug_msg('тест 6.1 положение выходов соответствует', 'green')
        self.__reset.stop_procedure_3()
        self.sbros_mtzp()
        self.__mysql_conn.mysql_ins_result('исправен', '6')
        return True

    def st_test_70(self) -> bool:
        """
        Тест 7. Проверка защиты МТЗ-3
        :return: bool
        """
        if my_msg(self.msg_5):
            pass
        else:
            return False
        self.__mysql_conn.mysql_ins_result('идёт тест 7.1', '7')
        self.__resist.resist_ohm(0)
        sleep(1)
        self.__ctrl_kl.ctrl_relay('KL12', True)
        sleep(1)
        self.__ctrl_kl.ctrl_relay('KL25', True)
        sleep(1)
        self.__resist.resist_ohm(255)
        sleep(1)
        in_a1, in_b2 = self.__inputs_a1_b2()
        if in_b2 is False and in_a1 is True:
            pass
        else:
            self.__fault.debug_msg('тест 7.1 положение выходов не соответствует', 'red')
            self.__mysql_conn.mysql_ins_result('неисправен', '7')
            return False
        self.__fault.debug_msg('тест 7.1 положение выходов соответствует', 'green')
        if self.__proc.procedure_x4_to_x5(setpoint_volt=self.ust_3, coef_volt=self.coef_volt):
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен TV1', '7')
            return False
        self.__mysql_conn.mysql_ins_result('идёт тест 7.2', '7')
        self.__ctrl_kl.ctrl_relay('KL63', True)
        start_timer_2 = time()
        __timer_2 = 0
        in_a1, in_b2 = self.__inputs_a1_b2()
        while (in_b2 is False or in_a1 is True) and __timer_2 <= 75:
            sleep(0.2)
            in_a1, in_b2 = self.__inputs_a1_b2()
            __timer_2 = time() - start_timer_2
            self.__fault.debug_msg(f'времени прошло\t{__timer_2}', 'orange')
        in_a1, in_b2 = self.__inputs_a1_b2()
        if in_b2 is True and in_a1 is False and __timer_2 <= 65:
            pass
        else:
            self.__reset.sbros_kl63_proc_all()
            self.__fault.debug_msg('тест 7.2 положение выходов не соответствует', 'red')
            self.__mysql_conn.mysql_ins_result('неисправен', '7')
            return False
        self.__fault.debug_msg('тест 7.2 положение выходов соответствует', 'green')
        self.__reset.sbros_kl63_proc_all()
        self.sbros_mtzp()
        self.__mysql_conn.mysql_ins_result('исправен', '7')
        return True

    def sbros_mtzp(self):
        """
        Общая функция для некоторых функций.
        :return
        """
        self.__ctrl_kl.ctrl_relay('KL12', False)
        self.__ctrl_kl.ctrl_relay('KL25', False)
        self.__resist.resist_ohm(255)
        self.__ctrl_kl.ctrl_relay('KL24', True)
        sleep(0.5)
        self.__ctrl_kl.ctrl_relay('KL24', False)
        sleep(0.5)
        self.__ctrl_kl.ctrl_relay('KL84', True)
        sleep(0.5)
        self.__ctrl_kl.ctrl_relay('KL84', False)

    def __inputs_a0(self):
        in_a0 = self.__read_mb.read_discrete(0)
        if in_a0 is None:
            # logging.error(f'нет связи с контроллером')
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_a0

    def __inputs_a1_b2(self):
        """
        Считывает из OPC сервера положение входов ПЛК
        :return: вход а1 и вход b2
        """
        in_a1 = self.__read_mb.read_discrete(1)
        in_b2 = self.__read_mb.read_discrete(10)
        if in_a1 is None or in_b2 is None:
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_a1, in_b2

    def st_test_mtzp_2(self) -> bool:
        if self.st_test_10():
            if self.st_test_11():
                if self.st_test_12():
                    if self.st_test_13():
                        if self.st_test_14():
                            if self.st_test_20():
                                if self.st_test_21():
                                    if self.st_test_30():
                                        if self.st_test_31():
                                            if self.st_test_32():
                                                if self.st_test_40():
                                                    if self.st_test_41():
                                                        if self.st_test_50():
                                                            if self.st_test_51():
                                                                if self.st_test_60():
                                                                    if self.st_test_70():
                                                                        return True
        return False


if __name__ == '__main__':
    test_mtzp = TestMTZP2()
    reset_test_mtzp = ResetRelay()
    mysql_conn_mtzp = MySQLConnect()
    fault = Bug(True)
    try:
        if test_mtzp.st_test_mtzp_2():
            mysql_conn_mtzp.mysql_block_good()
            my_msg('Блок исправен', 'green')
        else:
            mysql_conn_mtzp.mysql_block_bad()
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
        reset_test_mtzp.reset_all()
        sys.exit()
