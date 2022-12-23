#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки

Тип блока:	УМЗ
Производитель: Нет производителя
"""

import sys
import logging

from time import sleep

from general_func.exception import *
from general_func.database import *
from general_func.modbus import *
from general_func.procedure import *
from general_func.subtest import ProcedureFull, ReadOPCServer
from general_func.reset import ResetRelay
from gui.msgbox_1 import *
from gui.msgbox_2 import *

__all__ = ["TestUMZ"]


class TestUMZ:

    def __init__(self):
        self.reset = ResetRelay()
        self.proc = Procedure()
        self.proc_full = ProcedureFull()
        self.ai_read = AIRead()
        self.di_read = DIRead()
        self.ctrl_kl = CtrlKL()
        self.mysql_conn = MySQLConnect()
        self.di_read_full = ReadOPCServer()

        self.list_ust_volt = (22.6, 27.1, 31.9, 36.5, 41.3, 46.4, 50.2, 54.7, 59.3, 63.8, 68.4)
        self.list_ust_num = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
        self.list_delta_t_ab = []
        self.list_delta_t_vg = []
        self.list_delta_percent_ab = []
        self.list_delta_percent_vg = []
        self.list_result = []
        self.meas_volt_ab = 0
        self.meas_volt_vg = 0
        self.test_setpoint_ab = False
        self.test_setpoint_vg = False
        self.coef_volt: float = 0.0
        self.calc_delta_t_ab = 0.0
        self.calc_delta_t_vg = 0.0

        self.sp_volt = 0.0
        self.num_ust = 1
        self.i = 0.0
        self.k = 0
        self.health_flag: bool = False

        self.msg_1 = "Убедитесь в отсутствии в панелях разъемов установленных блоков Подключите " \
                     "блок УМЗ в разъем Х8 на панели B с помощью соответствующей кабельной сборки"
        self.msg_2 = "Переключите тумблер режимов, расположенный на корпусе блока, в положение «Работа»"
        self.msg_3 = "Переведите оба регулятора уставок на корпусе блока в положение «1»"
        self.msg_4 = "Произведите взвод защит, нажав на корпусе блока на кнопку «Взвод»"
        self.msg_5 = 'Установите оба регулятора уставок на блоке в положение'

        logging.basicConfig(
            filename="C:\\Stend\\project_class\\log\\TestUMZ.log",
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
        if my_msg(self.msg_1):
            if my_msg(self.msg_2):
                if my_msg(self.msg_3):
                    if my_msg(self.msg_4):
                        return True
        return False

    def st_test_11(self) -> bool:
        if self.di_read_full.subtest_2di(test_num=1, subtest_num=1.1, err_code_a=476, err_code_b=477,
                                         position_a=False, position_b=True, di_a='in_a1', di_b='in_a2'):
            return True
        return False

    def st_test_12(self) -> bool:
        """
        1.1. Проверка вероятности наличия короткого замыкания на входе измерительной цепи блока.
        1.1.2. Проверка отсутствия короткого замыкания на входе измерительной части блока.
        1.2. Определение коэффициента Кс отклонения фактического напряжения от номинального.
        :return:
        """
        if self.proc_full.procedure_1_full(test_num=1, subtest_num=1.1, coef_min_volt=0.4):
            self.coef_volt = self.proc_full.procedure_2_full(test_num=1, subtest_num=1.2)
            return True
        return False

    def st_test_20(self) -> bool:
        """
        Тест 2. Проверка срабатывания защиты канала АБ по уставкам.
        :return:
        """
        if my_msg(self.msg_4):
            pass
        else:
            return False
        # k = 0
        for self.i in self.list_ust_volt:
            self.mysql_conn.mysql_ins_result("идет тест", "2")
            msg_result = my_msg_2(f'{self.msg_5} {self.list_ust_num[self.k]}')
            if msg_result == 0:
                pass
            elif msg_result == 1:
                return False
            elif msg_result == 2:
                self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[self.k]} пропущена')
                self.list_delta_percent_ab.append('пропущена')
                self.list_delta_t_ab.append('пропущена')
                self.list_delta_percent_vg.append('пропущена')
                self.list_delta_t_vg.append('пропущена')
                self.k += 1
                continue
            progress_msg = f'формируем U уставки'
            self.mysql_conn.mysql_ins_result(f'{progress_msg} {self.k}', '2')
            if self.proc.procedure_x4_to_x5(coef_volt=self.coef_volt, setpoint_volt=self.i):
                pass
            else:
                self.mysql_conn.mysql_ins_result('неисправен', '2')
                return False
            progress_msg = f'канал АБ дельта t'
            self.mysql_conn.mysql_ins_result(f'{progress_msg} {self.k}', '2')
            for i1 in range(5):
                self.calc_delta_t_ab = self.ctrl_kl.ctrl_ai_code_v0(109)
                if self.calc_delta_t_ab != 9999:
                    break
                else:
                    my_msg(self.msg_4, 'darkgrey')
                    continue
            self.list_delta_t_ab.append(f'{self.calc_delta_t_ab:.1f}')
            in_a1, in_a5 = self.di_read.di_read('in_a1', 'in_a5')
            if in_a1 is True and in_a5 is False:
                # Δ%= 0,00004762*(U4)2+9,5648* U4
                progress_msg = f'канал АБ дельта %'
                self.mysql_conn.mysql_ins_result(f'{progress_msg} {self.k}', '2')
                self.meas_volt_ab = self.ai_read.ai_read('AI0')
                calc_delta_percent_ab = 0.00004762 * self.meas_volt_ab ** 2 + 9.5648 * self.meas_volt_ab
                self.list_delta_percent_ab.append(f'{calc_delta_percent_ab:.2f}')
                self.test_setpoint_ab = True
                self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[self.k]} '
                                                  f'дельта t: {self.calc_delta_t_ab:.1f}')
                self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[self.k]} '
                                                  f'дельта %: {calc_delta_percent_ab:.2f}')
            else:
                self.test_setpoint_ab = False
            self.ctrl_kl.ctrl_relay('KL73', True)
            if my_msg(self.msg_4):
                pass
            else:
                return False
            progress_msg = f'канал ВГ дельта t'
            self.mysql_conn.mysql_ins_result(f'{progress_msg} {self.k}', '2')
            for i2 in range(5):
                self.calc_delta_t_vg = self.ctrl_kl.ctrl_ai_code_v0(109)
                if self.calc_delta_t_ab != 9999:
                    break
                else:
                    my_msg(self.msg_4, "darkgrey")
                    continue
            self.list_delta_t_vg.append(f'{self.calc_delta_t_vg:.1f}')
            in_a1, in_a5 = self.di_read.di_read('in_a1', 'in_a5')
            if in_a1 is True and in_a5 is False:
                # Δ%= 0,00004762*(U4)2+9,5648* U4
                progress_msg = f'канал ВГ дельта %'
                self.mysql_conn.mysql_ins_result(f'{progress_msg} {self.k}', '2')
                self.meas_volt_vg = self.ai_read.ai_read('AI0')
                calc_delta_percent_vg = 0.00004762 * self.meas_volt_vg ** 2 + 9.5648 * self.meas_volt_vg
                self.list_delta_percent_vg.append(f'{calc_delta_percent_vg:.2f}')
                self.test_setpoint_vg = True
                self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[self.k]} '
                                                  f'дельта t: {self.calc_delta_t_vg:.1f}')
                self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[self.k]} '
                                                  f'дельта %: {calc_delta_percent_vg:.2f}')
            else:
                self.test_setpoint_vg = False
            self.ctrl_kl.ctrl_relay('KL73', False)
            self.reset.stop_procedure_3()
            if my_msg(self.msg_4):
                pass
            else:
                return False
            if self.test_setpoint_ab is True and self.test_setpoint_vg is True:
                self.k += 1
                continue
            elif self.test_setpoint_ab is False and self.test_setpoint_vg is False:
                progress_msg = f'повышаем U уставки'
                self.mysql_conn.mysql_ins_result(f'{progress_msg} {self.k}', '2')
                self.st_subtest_20_0()
                if my_msg(self.msg_4):
                    pass
                else:
                    return False
                self.k += 1
                continue
            elif self.test_setpoint_ab is False and self.test_setpoint_vg is True:
                progress_msg = f'повышаем U уставки'
                self.mysql_conn.mysql_ins_result(f'{progress_msg} {self.k}', '2')
                self.st_subtest_20_1()
                if my_msg(self.msg_4):
                    pass
                else:
                    return False
                self.k += 1
                continue
            elif self.test_setpoint_ab is True and self.test_setpoint_vg is False:
                progress_msg = f'повышаем U уставки'
                self.mysql_conn.mysql_ins_result(f'{progress_msg} {self.k}', '2')
                self.st_subtest_20_2()
                if my_msg(self.msg_4):
                    pass
                else:
                    return False
                self.k += 1
                continue
        self.mysql_conn.mysql_ins_result('исправен', '2')
        if my_msg(self.msg_4):
            pass
        else:
            return False
        in_a1, in_a5 = self.di_read.di_read('in_a1', 'in_a5')
        if in_a1 is False and in_a5 is True:
            return True
        elif in_a1 is True:
            self.mysql_conn.mysql_error(480)
            return False
        elif in_a5 is False:
            self.mysql_conn.mysql_error(481)
            return False

    def st_subtest_20_0(self):
        # self.sp_volt = sp_volt
        if self.proc.procedure_1_24_34(coef_volt=self.coef_volt, setpoint_volt=self.i, factor=1.1):
            pass
        else:
            self.mysql_conn.mysql_ins_result('неисправен', '2')
            return False
        for i3 in range(5):
            self.calc_delta_t_ab = self.ctrl_kl.ctrl_ai_code_v0(109)
            sleep(0.5)
            in_a1, in_a5 = self.di_read.di_read('in_a1', 'in_a5')
            if self.calc_delta_t_ab != 9999 and in_a1 is True and in_a5 is False:
                self.test_setpoint_ab = True
                break
            else:
                my_msg(self.msg_4, "darkgrey")
                self.test_setpoint_ab = False
                continue
        self.meas_volt_ab = self.ai_read.ai_read('AI0')
        self.ctrl_kl.ctrl_relay('KL73', True)
        if my_msg(self.msg_4):
            pass
        else:
            return False
        for i4 in range(5):
            self.calc_delta_t_vg = self.ctrl_kl.ctrl_ai_code_v0(109)
            sleep(0.5)
            in_a1, in_a5 = self.di_read.di_read('in_a1', 'in_a5')
            if self.calc_delta_t_vg != 9999 and in_a1 is True and in_a5 is False:
                self.test_setpoint_vg = True
                break
            else:
                my_msg(self.msg_4, "darkgrey")
                self.test_setpoint_vg = False
                continue
        self.meas_volt_vg = self.ai_read.ai_read('AI0')
        self.ctrl_kl.ctrl_relay('KL73', False)
        self.reset.stop_procedure_3()
        # Δ%= 0,00004762*(U4)2+9,5648* U4
        calc_delta_percent_ab = 0.00004762 * self.meas_volt_ab ** 2 + 9.5648 * self.meas_volt_ab
        calc_delta_percent_vg = 0.00004762 * self.meas_volt_vg ** 2 + 9.5648 * self.meas_volt_vg
        self.list_delta_percent_ab[-1] = f'{calc_delta_percent_ab:.2f}'
        self.list_delta_percent_vg[-1] = f'{calc_delta_percent_vg:.2f}'
        self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[self.k]} '
                                          f'дельта t: {self.calc_delta_t_ab:.1f}')
        self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[self.k]} '
                                          f'дельта %: {calc_delta_percent_ab:.2f}')
        self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[self.k]} '
                                          f'дельта t: {self.calc_delta_t_vg:.1f}')
        self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[self.k]} '
                                          f'дельта %: {calc_delta_percent_vg:.2f}')
        if self.test_setpoint_ab is True and self.test_setpoint_vg is True:
            self.list_delta_t_ab[-1] = f'{self.calc_delta_t_ab:.1f}'
            self.list_delta_t_vg[-1] = f'{self.calc_delta_t_vg:.1f}'
        elif self.test_setpoint_ab is False and self.test_setpoint_vg is True:
            self.list_delta_t_ab[-1] = f'неисправен'
            self.list_delta_t_vg[-1] = f'{self.calc_delta_t_vg:.1f}'
        elif self.test_setpoint_ab is True and self.test_setpoint_vg is False:
            self.list_delta_t_ab[-1] = f'{self.calc_delta_t_ab:.1f}'
            self.list_delta_t_vg[-1] = f'неисправен'
        elif self.test_setpoint_ab is False and self.test_setpoint_vg is False:
            self.list_delta_t_ab[-1] = f'неисправен'
            self.list_delta_t_vg[-1] = f'неисправен'

    def st_subtest_20_1(self):
        if self.proc.procedure_1_24_34(coef_volt=self.coef_volt, setpoint_volt=self.i, factor=1.1):
            pass
        else:
            self.mysql_conn.mysql_ins_result('неисправен', '2')
            return False
        if my_msg(self.msg_4):
            pass
        else:
            return False
        for i3 in range(5):
            self.calc_delta_t_ab = self.ctrl_kl.ctrl_ai_code_v0(109)
            sleep(0.5)
            in_a1, in_a5 = self.di_read.di_read('in_a1', 'in_a5')
            if self.calc_delta_t_ab != 9999 and in_a1 is True and in_a5 is False:
                self.test_setpoint_ab = True
                break
            else:
                my_msg(self.msg_4, "darkgrey")
                self.test_setpoint_ab = False
                continue
        self.meas_volt_ab = self.ai_read.ai_read('AI0')
        self.reset.stop_procedure_3()
        # Δ%= 0,00004762*(U4)2+9,5648* U4
        calc_delta_percent_ab = 0.00004762 * self.meas_volt_ab ** 2 + 9.5648 * self.meas_volt_ab
        self.list_delta_percent_ab[-1] = f'{calc_delta_percent_ab:.2f}'
        self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[self.k]} '
                                          f'дельта t: {self.calc_delta_t_ab:.1f}')
        self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[self.k]} '
                                          f'дельта %: {calc_delta_percent_ab:.2f}')
        if self.test_setpoint_ab is True:
            self.list_delta_t_ab[-1] = f'{self.calc_delta_t_ab:.1f}'
        else:
            self.list_delta_t_ab[-1] = f'неисправен'

    def st_subtest_20_2(self):
        if self.proc.procedure_1_24_34(coef_volt=self.coef_volt, setpoint_volt=self.i, factor=1.1):
            pass
        else:
            self.mysql_conn.mysql_ins_result('неисправен', '2')
            return False
        self.ctrl_kl.ctrl_relay('KL73', True)
        if my_msg(self.msg_4):
            pass
        else:
            return False
        for i4 in range(5):
            self.calc_delta_t_vg = self.ctrl_kl.ctrl_ai_code_v0(109)
            sleep(0.5)
            in_a1, in_a5 = self.di_read.di_read('in_a1', 'in_a5')
            if self.calc_delta_t_vg != 9999 and in_a1 is True and in_a5 is False:
                self.test_setpoint_vg = True
                break
            else:
                my_msg(self.msg_4, "darkgrey")
                self.test_setpoint_vg = False
                continue
        self.meas_volt_vg = self.ai_read.ai_read('AI0')
        self.ctrl_kl.ctrl_relay('KL73', False)
        self.reset.stop_procedure_3()
        # Δ%= 0,00004762*(U4)2+9,5648* U4
        calc_delta_percent_vg = 0.00004762 * self.meas_volt_vg ** 2 + 9.5648 * self.meas_volt_vg
        self.list_delta_percent_vg[-1] = f'{calc_delta_percent_vg:.2f}'
        self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[self.k]} '
                                          f'дельта t: {self.calc_delta_t_vg:.1f}')
        self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[self.k]} '
                                          f'дельта %: {calc_delta_percent_vg:.2f}')
        if self.test_setpoint_vg is True:
            self.list_delta_t_vg[-1] = f'{self.calc_delta_t_vg:.1f}'
        else:
            self.list_delta_t_vg[-1] = f'неисправен'

    def result_umz(self):
        """

        :return:
        """
        for g1 in range(len(self.list_delta_percent_ab)):
            self.list_result.append((self.list_ust_num[g1], self.list_delta_percent_ab[g1], self.list_delta_t_ab[g1],
                                     self.list_ust_num[g1], self.list_delta_percent_vg[g1], self.list_delta_t_vg[g1]))
        self.mysql_conn.mysql_umz_result(self.list_result)

    def st_test_umz(self) -> [bool, bool]:
        """

        :return:
        """
        if self.st_test_10():
            if self.st_test_11():
                if self.st_test_12():
                    if self.st_test_20():
                        return True, self.health_flag
        return False, self.health_flag


if __name__ == '__main__':
    test_umz = TestUMZ()
    reset_test_umz = ResetRelay()
    mysql_conn_umz = MySQLConnect()
    try:
        test, health_flag = test_umz.st_test_umz()
        if test and not health_flag:
            test_umz.result_umz()
            mysql_conn_umz.mysql_block_good()
            my_msg('Блок исправен', 'green')
        else:
            test_umz.result_umz()
            mysql_conn_umz.mysql_block_bad()
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
        reset_test_umz.reset_all()
        sys.exit()
