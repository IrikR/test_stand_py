# -*- coding: utf-8 -*-
"""
!!! НОВЫЙ НЕ ОБКАТАНЫЙ !!!

Алгоритм проверки

Тип блока:	УМЗ
Производитель: Нет производителя

"""

__all__ = ["TestUMZ"]

import logging
import sys
from time import sleep, time

from .general_func.database import *
from .general_func.exception import *
from .general_func.opc_full import ConnectOPC
from .general_func.procedure import *
from .general_func.reset import ResetRelay
from .general_func.subtest import ProcedureFull
from .general_func.utils import CLILog
from .gui.msgbox_1 import *
from .gui.msgbox_2 import *


class TestUMZ:

    def __init__(self):
        self.conn_opc = ConnectOPC()
        self.reset = ResetRelay()
        self.proc = Procedure()
        self.proc_full = ProcedureFull()
        self.mysql_conn = MySQLConnect()
        self.cli_log = CLILog("debug", __name__)

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
        self.cli_log.lev_info(f"старт теста {__doc__}", "skyblue")
        if my_msg(self.msg_1):
            if my_msg(self.msg_2):
                if my_msg(self.msg_3):
                    if my_msg(self.msg_4):
                        return True
        return False

    def st_test_11(self) -> bool:
        if self.conn_opc.subtest_read_di(test_num=1, subtest_num=1.1, err_code=[476, 477],
                                         position_inp=[False, True],
                                         di_xx=['inp_01', 'inp_02']):
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
                self.calc_delta_t_ab = self.conn_opc.ctrl_ai_code_v0(109)
                if self.calc_delta_t_ab != 9999:
                    break
                else:
                    my_msg(self.msg_4, 'darkgrey')
                    continue
            self.list_delta_t_ab.append(f'{self.calc_delta_t_ab:.1f}')
            in_a1, in_a5 = self.conn_opc.simplified_read_di(['inp_01', 'inp_05'])
            if in_a1 is True and in_a5 is False:
                # Δ%= 0,00004762*(U4)2+9,5648* U4
                progress_msg = f'канал АБ дельта %'
                self.mysql_conn.mysql_ins_result(f'{progress_msg} {self.k}', '2')
                self.meas_volt_ab = self.conn_opc.read_ai('AI0')
                calc_delta_percent_ab = 0.00004762 * self.meas_volt_ab ** 2 + 9.5648 * self.meas_volt_ab
                self.list_delta_percent_ab.append(f'{calc_delta_percent_ab:.2f}')
                self.test_setpoint_ab = True
                self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[self.k]} '
                                                  f'дельта t: {self.calc_delta_t_ab:.1f}')
                self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[self.k]} '
                                                  f'дельта %: {calc_delta_percent_ab:.2f}')
            else:
                self.test_setpoint_ab = False
            self.conn_opc.ctrl_relay('KL73', True)
            if my_msg(self.msg_4):
                pass
            else:
                return False
            progress_msg = f'канал ВГ дельта t'
            self.mysql_conn.mysql_ins_result(f'{progress_msg} {self.k}', '2')
            for i2 in range(5):
                self.calc_delta_t_vg = self.conn_opc.ctrl_ai_code_v0(109)
                if self.calc_delta_t_ab != 9999:
                    break
                else:
                    my_msg(self.msg_4, "darkgrey")
                    continue
            self.list_delta_t_vg.append(f'{self.calc_delta_t_vg:.1f}')
            in_a1, in_a5 = self.conn_opc.simplified_read_di(['inp_01', 'inp_05'])
            if in_a1 is True and in_a5 is False:
                # Δ%= 0,00004762*(U4)2+9,5648* U4
                progress_msg = f'канал ВГ дельта %'
                self.mysql_conn.mysql_ins_result(f'{progress_msg} {self.k}', '2')
                self.meas_volt_vg = self.conn_opc.read_ai('AI0')
                calc_delta_percent_vg = 0.00004762 * self.meas_volt_vg ** 2 + 9.5648 * self.meas_volt_vg
                self.list_delta_percent_vg.append(f'{calc_delta_percent_vg:.2f}')
                self.test_setpoint_vg = True
                self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[self.k]} '
                                                  f'дельта t: {self.calc_delta_t_vg:.1f}')
                self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[self.k]} '
                                                  f'дельта %: {calc_delta_percent_vg:.2f}')
            else:
                self.test_setpoint_vg = False
            self.conn_opc.ctrl_relay('KL73', False)
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
        in_a1, in_a5 = self.conn_opc.simplified_read_di(['inp_01', 'inp_05'])
        if in_a1 is False and in_a5 is True:
            return True
        elif in_a1 is True:
            self.mysql_conn.mysql_error(480)
            return False
        elif in_a5 is False:
            self.mysql_conn.mysql_error(481)
            return False

    def st_subtest_20_0(self) -> bool:
        # self.sp_volt = sp_volt
        if self.proc.procedure_1_24_34(coef_volt=self.coef_volt, setpoint_volt=self.i, factor=1.1):
            pass
        else:
            self.mysql_conn.mysql_ins_result('неисправен', '2')
            return False
        for i3 in range(5):
            self.calc_delta_t_ab = self.conn_opc.ctrl_ai_code_v0(109)
            sleep(0.5)
            in_a1, in_a5 = self.conn_opc.simplified_read_di(['inp_01', 'inp_05'])
            if self.calc_delta_t_ab != 9999 and in_a1 is True and in_a5 is False:
                self.test_setpoint_ab = True
                break
            else:
                my_msg(self.msg_4, "darkgrey")
                self.test_setpoint_ab = False
                continue
        self.meas_volt_ab = self.conn_opc.read_ai('AI0')
        self.conn_opc.ctrl_relay('KL73', True)
        if my_msg(self.msg_4):
            pass
        else:
            return False
        for i4 in range(5):
            self.calc_delta_t_vg = self.conn_opc.ctrl_ai_code_v0(109)
            sleep(0.5)
            in_a1, in_a5 = self.conn_opc.simplified_read_di(['inp_01', 'inp_05'])
            if self.calc_delta_t_vg != 9999 and in_a1 is True and in_a5 is False:
                self.test_setpoint_vg = True
                break
            else:
                my_msg(self.msg_4, "darkgrey")
                self.test_setpoint_vg = False
                continue
        self.meas_volt_vg = self.conn_opc.read_ai('AI0')
        self.conn_opc.ctrl_relay('KL73', False)
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

    def st_subtest_20_1(self) -> bool:
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
            self.calc_delta_t_ab = self.conn_opc.ctrl_ai_code_v0(109)
            sleep(0.5)
            in_a1, in_a5 = self.conn_opc.simplified_read_di(['inp_01', 'inp_05'])
            if self.calc_delta_t_ab != 9999 and in_a1 is True and in_a5 is False:
                self.test_setpoint_ab = True
                break
            else:
                my_msg(self.msg_4, "darkgrey")
                self.test_setpoint_ab = False
                continue
        self.meas_volt_ab = self.conn_opc.read_ai('AI0')
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

    def st_subtest_20_2(self) -> bool:
        if self.proc.procedure_1_24_34(coef_volt=self.coef_volt, setpoint_volt=self.i, factor=1.1):
            pass
        else:
            self.mysql_conn.mysql_ins_result('неисправен', '2')
            return False
        self.conn_opc.ctrl_relay('KL73', True)
        if my_msg(self.msg_4):
            pass
        else:
            return False
        for i4 in range(5):
            self.calc_delta_t_vg = self.conn_opc.ctrl_ai_code_v0(109)
            sleep(0.5)
            in_a1, in_a5 = self.conn_opc.simplified_read_di(['inp_01', 'inp_05'])
            if self.calc_delta_t_vg != 9999 and in_a1 is True and in_a5 is False:
                self.test_setpoint_vg = True
                break
            else:
                my_msg(self.msg_4, "darkgrey")
                self.test_setpoint_vg = False
                continue
        self.meas_volt_vg = self.conn_opc.read_ai('AI0')
        self.conn_opc.ctrl_relay('KL73', False)
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

    def result_umz(self) -> None:
        """

        :return:
        """
        for g1 in range(len(self.list_delta_percent_ab)):
            self.list_result.append((self.list_ust_num[g1], self.list_delta_percent_ab[g1], self.list_delta_t_ab[g1],
                                     self.list_ust_num[g1], self.list_delta_percent_vg[g1], self.list_delta_t_vg[g1]))
        self.mysql_conn.mysql_umz_result(self.list_result)

    def st_test_umz(self) -> [bool]:
        """

        :return:
        """
        if self.st_test_10():
            if self.st_test_11():
                if self.st_test_12():
                    if self.st_test_20():
                        return True, self.health_flag
        return False, self.health_flag

    def full_test_umz(self) -> None:
        try:
            start_time = time()
            test, health_flag = self.st_test_umz()
            end_time = time()
            time_spent = end_time - start_time
            self.cli_log.lev_info(f"Время выполнения: {time_spent}", "gray")
            self.logger.debug(f"Время выполнения: {time_spent}")
            self.mysql_conn.mysql_add_message(f"Время выполнения: {time_spent}")

            if test and not health_flag:
                self.result_umz()
                self.mysql_conn.mysql_block_good()
                self.logger.debug('Блок исправен')
                self.cli_log.lev_info('Блок исправен', 'green')
                my_msg('Блок исправен', 'green')
            else:
                self.result_umz()
                self.mysql_conn.mysql_block_bad()
                self.logger.debug('Блок неисправен')
                self.cli_log.lev_warning('Блок неисправен', 'red')
                my_msg('Блок неисправен', 'red')
        except OSError:
            self.logger.debug("ошибка системы")
            self.cli_log.lev_warning("ошибка системы", 'red')
            my_msg("ошибка системы", 'red')
        except SystemError:
            self.logger.debug("внутренняя ошибка")
            self.cli_log.lev_warning("внутренняя ошибка", 'red')
            my_msg("внутренняя ошибка", 'red')
        except ModbusConnectException as mce:
            self.logger.debug(f'{mce}')
            self.cli_log.lev_warning(f'{mce}', 'red')
            my_msg(f'{mce}', 'red')
        except HardwareException as hwe:
            self.logger.debug(f'{hwe}')
            self.cli_log.lev_warning(f'{hwe}', 'red')
            my_msg(f'{hwe}', 'red')
        except AttributeError as ae:
            self.logger.debug(f"Неверный атрибут. {ae}")
            self.cli_log.lev_warning(f"Неверный атрибут. {ae}", 'red')
            my_msg(f"Неверный атрибут. {ae}", 'red')
        except ValueError as ve:
            self.logger.debug(f"Некорректное значение для переменной. {ve}")
            self.cli_log.lev_warning(f"Некорректное значение для переменной. {ve}", 'red')
            my_msg(f"Некорректное значение для переменной. {ve}", 'red')
        finally:
            self.conn_opc.full_relay_off()
            self.conn_opc.opc_close()
            sys.exit()
