#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ПРОВЕРЕН
Алгоритм проверки

Тип блока: ТЗП
Производитель: Нет производителя, Углеприбор
Уникальный номер: 61, 62
Тип блока: ТЗП-П
Производитель: Нет производителя, Пульсар
Уникальный номер: 63, 64


"""

import logging
import sys
from time import time, sleep

from .general_func.database import *
from .general_func.exception import *
from .general_func.modbus import *
from .general_func.procedure import *
from .general_func.reset import ResetRelay, ResetProtection
from .general_func.subtest import ReadOPCServer, ProcedureFull
from .gui.msgbox_1 import *
from .gui.msgbox_2 import *
from .general_func.utils import CLILog

__all__ = ["TestTZP"]


class TestTZP:

    def __init__(self):
        self.reset_relay = ResetRelay()
        self.reset_protect = ResetProtection()
        self.proc = Procedure()
        self.proc_full = ProcedureFull()
        self.ai_read = AIRead()
        self.di_read = DIRead()
        self.ctrl_kl = CtrlKL()
        self.mysql_conn = MySQLConnect()
        self.di_read_full = ReadOPCServer()
        self.cli_log = CLILog(True, __name__)

        self._list_ust_num = (0.5, 0.6, 0.7, 0.8, 0.9, 1.0)
        self._list_ust_volt = (25.7, 29.8, 34.3, 39.1, 43.7, 48.5)
        self._list_delta_t = []
        self._list_delta_percent = []
        self._list_tzp_result = []

        self._coef_volt = 0.0
        self._health_flag: bool = False

        self._msg_1 = "Переключите тумблер на корпусе блока в положение «Проверка» "
        self._msg_2 = "Переключите тумблер на корпусе блока в положение «Работа» "
        self._msg_3 = "Установите регулятор уставок на блоке в положение"

        logging.basicConfig(
            filename="C:\Stend\project_class\log\TestTZP.log",
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
        self.logger.debug("тест 1")
        self.cli_log.log_msg("тест 1", "gray")
        self.di_read.di_read('in_b6', 'in_b7')
        self.mysql_conn.mysql_ins_result('идет тест 1', '1')
        self.ctrl_kl.ctrl_relay('KL21', True)
        self.logger.debug("включен KL21")
        self.reset_protect.sbros_zashit_kl30(time_on=1.5, time_off=2.0)
        if self.di_read_full.subtest_2di(test_num=1, subtest_num=1.0, err_code_a=277, err_code_b=278, position_a=False,
                                         position_b=True, di_b='in_a5'):
            return True
        return False

    def st_test_11(self) -> bool:
        """
        1.1.2. Проверка отсутствия короткого замыкания на входе измерительной части блока:
        1.2. Определение коэффициента Кс отклонения фактического напряжения от номинального.
        :return:
        """
        if self.proc_full.procedure_1_full(test_num=1, subtest_num=1.2):
            self._coef_volt = self.proc_full.procedure_2_full(test_num=1, subtest_num=1.3)
            return True
        return False

    def st_test_20(self) -> bool:
        """
        Тест 2. Проверка работоспособности блока в режиме «Проверка»
        :return:
        """
        self.logger.debug("тест 2.0")
        if my_msg(f'{self._msg_1}'):
            pass
        else:
            return False
        self.mysql_conn.mysql_ins_result('идет тест 2.0', '2')
        if self.di_read_full.subtest_2di(test_num=2, subtest_num=2.0, err_code_a=282, err_code_b=283,
                                         position_a=True, position_b=False, di_b='in_a5'):
            return True
        return False

    def st_test_21(self) -> bool:
        """
        2.2. Сброс защит после проверки
        :return:
        """
        self.logger.debug("тест 2.1")
        if my_msg(f'{self._msg_2}'):
            pass
        else:
            return False
        self.mysql_conn.mysql_ins_result('идет тест 2.1', '2')
        self.reset_protect.sbros_zashit_kl30(time_on=1.5, time_off=2.0)
        if self.di_read_full.subtest_2di(test_num=2, subtest_num=2.1, err_code_a=284, err_code_b=285,
                                         position_a=False, position_b=True, di_b='in_a5'):
            return True
        return False

    def st_test_30(self) -> bool:
        """
        Тест 3. Проверка срабатывания блока по уставкам.
        :return:
        """
        self.logger.debug(f'тест 3.0')
        self.mysql_conn.mysql_ins_result('идет тест 3', '3')
        k = 0
        for i in self._list_ust_volt:
            self.logger.debug(f'цикл: {k}, уставка: {i}')
            self.mysql_conn.mysql_ins_result(f'проверка уставки {self._list_ust_num[k]}', '3')
            msg_result = my_msg_2(f'{self._msg_3} {self._list_ust_num[k]}')
            self.logger.debug(f'от пользователя пришло: {msg_result}')
            if msg_result == 0:
                pass
            elif msg_result == 1:
                self.logger.debug(f'отмена')
                return False
            elif msg_result == 2:
                self.mysql_conn.mysql_add_message(f'уставка {self._list_ust_num[k]} пропущена')
                self._list_delta_percent.append('пропущена')
                self._list_delta_t.append('пропущена')
                self.logger.debug(f'уставка: {k} пропущена')
                k += 1
                continue
            if self.proc.procedure_x4_to_x5(coef_volt=self._coef_volt, setpoint_volt=i):
                self.logger.debug(f'процедура 1, 2.4, 3.4: пройдена')
                pass
            else:
                self.mysql_conn.mysql_ins_result('неисправен', '4')
                self.logger.debug(f'процедура 1, 2.4, 3.4: не пройдена')
                return False
            meas_volt = self.ai_read.ai_read('AI0')
            self.logger.debug(f'измеренное напряжение: {meas_volt}')
            calc_delta_percent = 0.0044 * meas_volt ** 2 + 2.274 * meas_volt
            self.logger.debug(f'd%: {calc_delta_percent}')
            self._list_delta_percent.append(f'{calc_delta_percent:.2f}')
            if 0.9 * i / self._coef_volt <= meas_volt <= 1.1 * i / self._coef_volt:
                self.logger.debug(f'напряжение соответствует: {meas_volt:.2f}')
                self.mysql_conn.progress_level(0.0)
                self.ctrl_kl.ctrl_relay('KL63', True)
                self.logger.debug("включение KL63")
                in_b0, *_ = self.di_read.di_read('in_b0')
                self.logger.debug(f"in_b0 = {in_b0} (True)")
                while in_b0 is False:
                    self.logger.debug(f"in_b0 = {in_b0} (False)")
                    in_b0, *_ = self.di_read.di_read('in_b0')
                start_timer = time()
                self.logger.debug(f"начало отсчета: {start_timer}")
                sub_timer = 0
                in_a1, in_a5 = self.di_read.di_read("in_a1", "in_a5")
                self.logger.debug(f"in_a1 = {in_a5} (False)")
                while in_a5 is True and sub_timer <= 370:
                    sleep(0.2)
                    sub_timer = time() - start_timer
                    self.logger.debug(f"времени прошло {sub_timer:.1f}")
                    self.mysql_conn.progress_level(sub_timer)
                    in_a5, *_ = self.di_read.di_read('in_a5')
                    self.logger.debug(f"in_a1 = {in_a5} (False)")
                stop_timer = time()
                self.logger.debug(f"конец отсчета")
                self.mysql_conn.progress_level(0.0)
                self.ctrl_kl.ctrl_relay('KL63', False)
                self.logger.debug(f"отключение KL63")
                calc_delta_t = stop_timer - start_timer
                self.logger.debug(f"dt: {calc_delta_t}")
                self.reset_relay.stop_procedure_3()
                self.logger.debug(f"останов процедуры 3")
                self._list_delta_t.append(f'{calc_delta_t:.1f}')
                self.mysql_conn.mysql_add_message(f'уставка {self._list_ust_num[k]} '
                                                  f'дельта t: {calc_delta_t:.1f}')
                self.mysql_conn.mysql_add_message(f'уставка {self._list_ust_num[k]} '
                                                  f'дельта %: {calc_delta_percent:.2f}')
                in_a1, in_a5 = self.di_read.di_read('in_a1', 'in_a5')
                self.logger.debug(f"in_a1 = {in_a1} (True), in_a5 = {in_a5} (False), время: {calc_delta_t}")
                if calc_delta_t <= 360 and in_a1 is True and in_a5 is False:
                    # Если в период времени до 6 минут входа DI.A1, DI.A5 занимают
                    # состояние, указанное в таблице выше, то переходим к п.3.6.
                    if self.subtest_35():
                        self.logger.debug(f"переход на новую итерацию цикла")
                        k += 1
                        continue
                    else:
                        self.mysql_conn.mysql_add_message(f'уставка {self._list_ust_num[k]}: '
                                                          f'не срабатывает сброс защит')
                        self.logger.debug(f'уставка {self._list_ust_num[k]}: не срабатывает сброс защит')
                        return False
                else:
                    # Если в период времени до 6 минут входа DI.A1, DI.A5 не занимают
                    # состояние, указанное в таблице выше, то переходим к п.3.5.
                    self.logger.debug("время переключения не соответствует")
                    self.mysql_conn.mysql_error(287)
                    if self.subtest_35():
                        k += 1
                        self.logger.debug(f"переход на новую итерацию цикла")
                        continue
                    else:
                        self.mysql_conn.mysql_add_message(f'уставка {self._list_ust_num[k]}: '
                                                          f'не срабатывает сброс защит')
                        self.logger.debug(f'уставка {self._list_ust_num[k]}: не срабатывает сброс защит')
                        return False
            else:
                self.logger.debug("напряжение U4 не соответствует")
                self.mysql_conn.mysql_error(286)
                self.reset_relay.stop_procedure_3()
                self.logger.debug("останов процедуры 3")
        self.mysql_conn.mysql_ins_result('исправен', '3')
        self.logger.debug("тест 3 завершен")
        return True

    def subtest_35(self) -> bool:
        self.mysql_conn.mysql_ins_result('идет тест 3.5', '3')
        self.logger.debug("идет тест 3.5")
        self.reset_protect.sbros_zashit_kl30(time_on=1.5, time_off=2.0)
        self.logger.debug("сброс защит")
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.log_msg("таймаут 1 сек", "gray")
        if self.di_read_full.subtest_2di(test_num=3, subtest_num=3.5, err_code_a=284, err_code_b=285,
                                         position_a=False, position_b=True, di_b='in_a5'):
            return True
        return False

    def st_test_tzp(self) -> [bool, bool]:
        if self.st_test_10():
            if self.st_test_11():
                if self.st_test_20():
                    if self.st_test_21():
                        if self.st_test_30():
                            return True, self._health_flag
        return False, self._health_flag

    def result_test_tzp(self):
        for t in range(len(self._list_delta_percent)):
            self._list_tzp_result.append((self._list_ust_num[t], self._list_delta_percent[t], self._list_delta_t[t]))
            self.logger.debug(f'{self._list_ust_num[t]}, {self._list_delta_percent[t]}, {self._list_delta_t[t]}')
        self.mysql_conn.mysql_tzp_result(self._list_tzp_result)

    def full_test_tzp(self):
        try:
            test, health_flag = self.st_test_tzp()
            if test and not health_flag:
                self.result_test_tzp()
                self.mysql_conn.mysql_block_good()
                my_msg('Блок исправен', 'green')
            else:
                self.result_test_tzp()
                self.mysql_conn.mysql_block_bad()
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
            self.reset_relay.reset_all()
            sys.exit()

if __name__ == '__main__':
    test_tzp = TestTZP()
    test_tzp.full_test_tzp()
    # reset_test_tzp = ResetRelay()
    # mysql_conn_tzp = MySQLConnect()
    # try:
    #     test, health_flag = test_tzp.st_test_tzp()
    #     if test and not health_flag:
    #         test_tzp.result_test_tzp()
    #         mysql_conn_tzp.mysql_block_good()
    #         my_msg('Блок исправен', 'green')
    #     else:
    #         test_tzp.result_test_tzp()
    #         mysql_conn_tzp.mysql_block_bad()
    #         my_msg('Блок неисправен', 'red')
    # except OSError:
    #     my_msg("ошибка системы", 'red')
    # except SystemError:
    #     my_msg("внутренняя ошибка", 'red')
    # except ModbusConnectException as mce:
    #     my_msg(f'{mce}', 'red')
    # except HardwareException as hwe:
    #     my_msg(f'{hwe}', 'red')
    # finally:
    #     reset_test_tzp.reset_all()
    #     sys.exit()
