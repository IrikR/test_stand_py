#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки

Тип блока: ММТЗ-Д
Производитель: Нет производителя, ДонЭнергоЗавод

"""

import sys
import logging

from time import sleep

from general_func.exception import *
from general_func.database import *
from general_func.modbus import *
from general_func.procedure import *
from general_func.reset import ResetRelay, ResetProtection
from general_func.subtest import ProcedureFull
from gui.msgbox_1 import *
from gui.msgbox_2 import *

__all__ = ["TestMMTZD"]


class TestMMTZD:

    def __init__(self):
        self.reset_relay = ResetRelay()
        self.reset_protect = ResetProtection()
        self.proc = Procedure()
        self.proc_full = ProcedureFull()
        self.ctrl_kl = CtrlKL()
        self.di_read = DIRead()
        self.mysql_conn = MySQLConnect()

        self.list_ust_num = (10, 20, 30, 40, 50)
        # self.ust = (7.7, 16.5, 25.4, 31.9, 39.4)
        self.list_ust_volt = (8.0, 16.5, 25.4, 31.9, 39.4)
        self.list_num_yach_test_2 = (3, 4, 5, 6, 7)
        self.list_num_yach_test_3 = (9, 10, 11, 12, 13)

        self.meas_volt_ust = 0.0
        self.coef_volt = 0.0
        self.health_flag: bool = False

        self.msg_1 = "Убедитесь в отсутствии в панелях разъемов установленных блоков. " \
                     "Подключите блок в разъем Х21 на панели С"
        self.msg_2 = "Переключите тумблер режимов, расположенный на корпусе блока, в положение «Работа»"
        self.msg_3 = "Установите регулятор уставок III канала, расположенного на блоке в положение «50»"
        self.msg_4 = "Установите регулятор уставок II канала, расположенного на блоке в положение\t"
        self.msg_5 = "Установите регулятор уставок II канала, расположенного на блоке в положение «50»"
        self.msg_6 = "Установите регулятор уставок III канала, расположенного на блоке в положение\t"

        logging.basicConfig(
            filename="C:\\Stend\\project_class\\log\\TestMMTZD.log",
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
        :return:
        """
        self.di_read.di_read('in_a0')
        if my_msg(self.msg_1):
            if my_msg(self.msg_2):
                return True
        return False

    def st_test_11(self) -> bool:
        self.ctrl_kl.ctrl_relay('KL33', True)
        self.reset_protect.sbros_zashit_kl1()
        in_a1, in_a5 = self.di_read.di_read('in_a1', 'in_a5')
        if in_a1 is True and in_a5 is True:
            pass
        else:
            self.mysql_conn.mysql_ins_result("неисправен", "1")
            if in_a1 is False:
                self.logger.debug("положение входа 1 не соответствует")
                self.mysql_conn.mysql_error(412)
            elif in_a5 is False:
                self.logger.debug("положение входа 5 не соответствует")
                self.mysql_conn.mysql_error(413)
            return False
        self.logger.debug("положение выходов блока соответствует")
        return True

    def st_test_12(self) -> bool:
        """
        1.1.2. Проверка отсутствия короткого замыкания на входе измерительной части блока:
        1.2. Определение коэффициента Кс отклонения фактического напряжения от номинального
        """
        if self.proc_full.procedure_1_full(test_num=1, subtest_num=1.2, coef_min_volt=0.4):
            self.coef_volt = self.proc_full.procedure_2_full(test_num=1, subtest_num=1.3)
            return True
        return False

    def st_test_20(self) -> bool:
        """
        Тест 2. Проверка срабатывания защиты II канала по уставкам.
        :return:
        """
        if my_msg(self.msg_3):
            pass
        else:
            return False
        k = 0
        for i in self.list_ust_volt:
            msg_result = my_msg_2(f'{self.msg_4} {self.list_ust_num[k]}')
            if msg_result == 0:
                pass
            elif msg_result == 1:
                return False
            elif msg_result == 2:
                self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[k]} пропущена')
                k += 1
                continue
            if self.proc.procedure_x4_to_x5(coef_volt=self.coef_volt, setpoint_volt=i):
                pass
            else:
                self.mysql_conn.mysql_ins_result('неисправен', '2')
                return False
            # 2.1.  Проверка срабатывания блока от сигнала нагрузки:
            self.ctrl_kl.ctrl_ai_code_v1(106)
            sleep(3)
            in_a1, in_a5 = self.di_read.di_read('in_a1', 'in_a5')
            self.reset_relay.stop_procedure_3()
            if in_a1 is False and in_a5 is False:
                self.logger.debug("положение выходов блока соответствует")
                if self.subtest_23():
                    self.mysql_conn.mysql_ins_result('исправен', f'{self.list_num_yach_test_2[k]}')
                else:
                    self.mysql_conn.mysql_ins_result('неисправен', f'{self.list_num_yach_test_2[k]}')
                    return False
            elif in_a1 is True:
                if self.subtest_22(i):
                    self.mysql_conn.mysql_ins_result('исправен', f'{self.list_num_yach_test_2[k]}')
                else:
                    self.mysql_conn.mysql_ins_result('неисправен', '2')
                    self.mysql_conn.mysql_error(415)
                    self.mysql_conn.mysql_ins_result('неисправен', f'{self.list_num_yach_test_2[k]}')
                    return False
            elif in_a5 is True:
                if self.subtest_22(i):
                    self.mysql_conn.mysql_ins_result('исправен', f'{self.list_num_yach_test_2[k]}')
                else:
                    self.mysql_conn.mysql_ins_result('неисправен', '2')
                    self.mysql_conn.mysql_error(416)
                    self.mysql_conn.mysql_ins_result('неисправен', f'{self.list_num_yach_test_2[k]}')
                    return False
            k += 1
        self.mysql_conn.mysql_ins_result('исправен', '2')
        return True

    def st_test_30(self) -> bool:
        """
        Тест 3. Проверка срабатывания защиты III канала по уставкам.
        :return:
        """
        self.ctrl_kl.ctrl_relay('KL73', True)
        sleep(5)
        if my_msg(self.msg_5):
            pass
        else:
            return False
        x = 0
        for y in self.list_ust_volt:
            msg_result = my_msg_2(f'{self.msg_6} {self.list_ust_num[x]}')
            if msg_result == 0:
                pass
            elif msg_result == 1:
                return False
            elif msg_result == 2:
                self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[x]} пропущена')
                x += 1
                continue
            if self.proc.procedure_x4_to_x5(coef_volt=self.coef_volt, setpoint_volt=y):
                pass
            else:
                self.mysql_conn.mysql_ins_result('неисправен', '3')
            self.ctrl_kl.ctrl_ai_code_v1(106)
            sleep(3)
            in_a1, in_a5 = self.di_read.di_read('in_a1', 'in_a5')
            self.reset_relay.stop_procedure_3()
            if in_a1 is False and in_a5 is False:
                if self.subtest_33():
                    self.mysql_conn.mysql_ins_result('исправен', f'{self.list_num_yach_test_3[x]}')
                else:
                    self.mysql_conn.mysql_ins_result('неисправен', f'{self.list_num_yach_test_3[x]}')
                    return False
            elif in_a1 is True:
                if self.subtest_32(y):
                    self.mysql_conn.mysql_ins_result('исправен', f'{self.list_num_yach_test_3[x]}')
                else:
                    self.mysql_conn.mysql_ins_result('неисправен', '3')
                    self.mysql_conn.mysql_error(419)
                    self.mysql_conn.mysql_ins_result('неисправен', f'{self.list_num_yach_test_3[x]}')
                    return False
            elif in_a5 is True:
                if self.subtest_32(y):
                    self.mysql_conn.mysql_ins_result('исправен', f'{self.list_num_yach_test_3[x]}')
                else:
                    self.mysql_conn.mysql_ins_result('неисправен', '3')
                    self.mysql_conn.mysql_error(420)
                    self.mysql_conn.mysql_ins_result('неисправен', f'{self.list_num_yach_test_3[x]}')
                    return False
            x += 1
        self.mysql_conn.mysql_ins_result('исправен', '8')
        return True

    def subtest_22(self, i) -> bool:
        """
        2.2. Формирование нагрузочного сигнала 1,1*calc_volt[i]:
        :param i:
        :return:
        """
        self.reset_protect.sbros_zashit_kl1()
        in_a1, in_a5 = self.di_read.di_read('in_a1', 'in_a5')
        if in_a1 is True and in_a5 is True:
            pass
        elif in_a1 is False:
            self.mysql_conn.mysql_ins_result('неисправен', '2')
            self.mysql_conn.mysql_error(417)
            return False
        elif in_a5 is False:
            self.mysql_conn.mysql_ins_result('неисправен', '2')
            self.mysql_conn.mysql_error(418)
            return False
        if self.proc.procedure_1_24_34(coef_volt=self.coef_volt, setpoint_volt=i, factor=1.1):
            pass
        else:
            self.mysql_conn.mysql_ins_result('неисправен', '2')
        # 2.2.2.  Проверка срабатывания блока от сигнала нагрузки:
        self.ctrl_kl.ctrl_ai_code_v1(107)
        sleep(3)
        in_a1, in_a5 = self.di_read.di_read('in_a1', 'in_a5')
        self.reset_relay.stop_procedure_3()
        if in_a1 is False and in_a5 is False:
            if self.subtest_23():
                return True
            else:
                return False
        elif in_a1 is True:
            self.mysql_conn.mysql_ins_result('неисправен', '2')
            self.mysql_conn.mysql_error(415)
            if self.subtest_23():
                return True
            else:
                return False
        elif in_a5 is True:
            self.mysql_conn.mysql_ins_result('неисправен', '2')
            self.mysql_conn.mysql_error(416)
            if self.subtest_23():
                return True
            else:
                return False

    def subtest_23(self) -> bool:
        """
        2.3. Сброс защит после проверки
        :return:
        """
        self.reset_protect.sbros_zashit_kl1()
        in_a1, in_a5 = self.di_read.di_read('in_a1', 'in_a5')
        if in_a1 is True and in_a5 is True:
            return True
        else:
            self.mysql_conn.mysql_ins_result('неисправен', '2')
            if in_a1 is False:
                self.mysql_conn.mysql_error(417)
            elif in_a5 is False:
                self.mysql_conn.mysql_error(418)
            return False

    def subtest_32(self, y) -> bool:
        """
        3.2. Формирование нагрузочного сигнала 1,1*calc_volt[i]:
        :param y:
        :return:
        """
        self.reset_protect.sbros_zashit_kl1()
        in_a1, in_a5 = self.di_read.di_read('in_a1', 'in_a5')
        if in_a1 is True and in_a5 is True:
            pass
        elif in_a1 is False:
            self.mysql_conn.mysql_ins_result('неисправен', '3')
            self.mysql_conn.mysql_error(417)
            return False
        elif in_a5 is False:
            self.mysql_conn.mysql_ins_result('неисправен', '3')
            self.mysql_conn.mysql_error(418)
            return False
        if self.proc.procedure_1_24_34(coef_volt=self.coef_volt, setpoint_volt=y, factor=1.1):
            pass
        else:
            self.mysql_conn.mysql_ins_result('неисправен', '3')
            return False
        # 2.2.2.  Проверка срабатывания блока от сигнала нагрузки:
        self.ctrl_kl.ctrl_ai_code_v1(107)
        sleep(3)
        in_a1, in_a5 = self.di_read.di_read('in_a1', 'in_a5')
        self.reset_relay.stop_procedure_3()
        if in_a1 is False and in_a5 is False:
            if self.subtest_33():
                return True
            else:
                return False
        elif in_a1 is True:
            self.mysql_conn.mysql_ins_result('неисправен', '3')
            self.mysql_conn.mysql_error(419)
            if self.subtest_33():
                return True
            else:
                return False
        elif in_a5 is True:
            self.mysql_conn.mysql_ins_result('неисправен', '3')
            self.mysql_conn.mysql_error(420)
            if self.subtest_33():
                return True
            else:
                return False

    def subtest_33(self) -> bool:
        """
        2.3. Сброс защит после проверки
        :return:
        """
        self.reset_protect.sbros_zashit_kl1()
        in_a1, in_a5 = self.di_read.di_read('in_a1', 'in_a5')
        if in_a1 is True and in_a5 is True:
            return True
        else:
            self.mysql_conn.mysql_ins_result('неисправен', '3')
            if in_a1 is False:
                self.mysql_conn.mysql_error(417)
            elif in_a5 is False:
                self.mysql_conn.mysql_error(418)
            return False

    def st_test_mmtz_d(self) -> [bool, bool]:
        if self.st_test_10():
            if self.st_test_11():
                if self.st_test_12():
                    if self.st_test_20():
                        if self.st_test_30():
                            return True, self.health_flag
        return False, self.health_flag


if __name__ == '__main__':
    test_mmtz_d = TestMMTZD()
    reset_test_mmtz_d = ResetRelay()
    mysql_conn_mmtz_d = MySQLConnect()
    try:
        test, health_flag = test_mmtz_d.st_test_mmtz_d()
        if test and not health_flag:
            mysql_conn_mmtz_d.mysql_block_good()
            my_msg('Блок исправен', 'green')
        else:
            mysql_conn_mmtz_d.mysql_block_bad()
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
        reset_test_mmtz_d.reset_all()
        sys.exit()
