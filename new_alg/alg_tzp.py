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

__all__ = ["TestTZP"]

import logging
from time import sleep, time

from .general_func.database import *
from .general_func.opc_full import ConnectOPC
from .general_func.procedure import *
from .general_func.reset import ResetProtection, ResetRelay
from .general_func.subtest import ProcedureFull
from .general_func.utils import CLILog
from .gui.msgbox_1 import *
from .gui.msgbox_2 import *


class TestTZP:

    def __init__(self):
        self.conn_opc = ConnectOPC()
        self.reset_relay = ResetRelay()
        self.reset_protect = ResetProtection()
        self.proc = Procedure()
        self.proc_full = ProcedureFull()
        self.mysql_conn = MySQLConnect()
        self.cli_log = CLILog("debug", __name__)

        self._list_ust_num: tuple[float, ...] = (0.5, 0.6, 0.7, 0.8, 0.9, 1.0)
        self._list_ust_volt: tuple[float, ...] = (25.7, 29.8, 34.3, 39.1, 43.7, 48.5)
        self._list_delta_t: list[str] = []
        self._list_delta_percent: list[str] = []
        self._list_tzp_result: list[[str]] = []

        self._coef_volt: float = 0.0
        self._health_flag: bool = False

        self._msg_1: str = "Переключите тумблер на корпусе блока в положение «Проверка» "
        self._msg_2: str = "Переключите тумблер на корпусе блока в положение «Работа» "
        self._msg_3: str = "Установите регулятор уставок на блоке в положение"

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
        self.cli_log.lev_info(f"старт теста {__doc__}", "skyblue")
        self.logger.debug("тест 1")
        self.cli_log.lev_info("тест 1", "gray")
        self.mysql_conn.mysql_ins_result('идет тест 1', '1')
        self.conn_opc.ctrl_relay('KL21', True)
        self.reset_protect.sbros_zashit_kl30(time_on=1.5, time_off=2.0)
        if self.conn_opc.subtest_read_di(test_num=1, subtest_num=1.0,
                                         err_code=[277, 278],
                                         position_inp=[False, True],
                                         di_xx=['inp_01', 'inp_05']):
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
        if self.conn_opc.subtest_read_di(test_num=2, subtest_num=2.0,
                                         err_code=[282, 283],
                                         position_inp=[True, False],
                                         di_xx=['inp_01', 'inp_05']):
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
        if self.conn_opc.subtest_read_di(test_num=2, subtest_num=2.1,
                                         err_code=[284, 285],
                                         position_inp=[False, True],
                                         di_xx=['inp_01', 'inp_05']):
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
            meas_volt = self.conn_opc.read_ai('AI0')
            self.logger.debug(f'измеренное напряжение: {meas_volt}')
            calc_delta_percent = 0.0044 * meas_volt ** 2 + 2.274 * meas_volt
            self.logger.debug(f'd%: {calc_delta_percent}')
            self._list_delta_percent.append(f'{calc_delta_percent:.2f}')
            if 0.9 * i / self._coef_volt <= meas_volt <= 1.1 * i / self._coef_volt:
                self.logger.debug(f'напряжение соответствует: {meas_volt:.2f}')
                self.mysql_conn.progress_level(0.0)
                self.conn_opc.ctrl_relay('KL63', True)
                inp_08, *_ = self.conn_opc.simplified_read_di(['inp_08'])
                self.logger.debug(f"inp_08 = {inp_08} (True)")
                while inp_08 is False:
                    self.logger.debug(f"inp_08 = {inp_08} (False)")
                    inp_08, *_ = self.conn_opc.simplified_read_di(['inp_08'])
                start_timer = time()
                self.logger.debug(f"начало отсчета: {start_timer}")
                sub_timer = 0
                inp_01, inp_05 = self.conn_opc.simplified_read_di(["inp_01", "inp_05"])
                self.logger.debug(f"{inp_01 =} {inp_05 =} (False)")
                while inp_05 is True and sub_timer <= 370:
                    sleep(0.2)
                    sub_timer = time() - start_timer
                    self.logger.debug(f"времени прошло {sub_timer:.1f}")
                    self.mysql_conn.progress_level(sub_timer)
                    inp_05, *_ = self.conn_opc.simplified_read_di(['inp_05'])
                    self.logger.debug(f"inp_01 = {inp_05} (False)")
                stop_timer = time()
                self.logger.debug(f"конец отсчета")
                self.mysql_conn.progress_level(0.0)
                self.conn_opc.ctrl_relay('KL63', False)
                calc_delta_t = stop_timer - start_timer
                self.logger.debug(f"dt: {calc_delta_t}")
                self.reset_relay.stop_procedure_3()
                self.logger.debug(f"останов процедуры 3")
                self._list_delta_t.append(f'{calc_delta_t:.1f}')
                self.mysql_conn.mysql_add_message(f'уставка {self._list_ust_num[k]} '
                                                  f'дельта t: {calc_delta_t:.1f}')
                self.mysql_conn.mysql_add_message(f'уставка {self._list_ust_num[k]} '
                                                  f'дельта %: {calc_delta_percent:.2f}')
                inp_01, inp_05 = self.conn_opc.simplified_read_di(['inp_01', 'inp_05'])
                self.logger.debug(f"inp_01 = {inp_01} (True), inp_05 = {inp_05} (False), время: {calc_delta_t}")
                if calc_delta_t <= 360 and inp_01 is True and inp_05 is False:
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
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=3, subtest_num=3.5,
                                         err_code=[284, 285],
                                         position_inp=[False, True],
                                         di_xx=['inp_01', 'inp_05']):
            return True
        return False

    def st_test_tzp(self) -> [bool, bool]:
        """
            Главная функция которая собирает все остальные
            :type: bool, bool
            :return:  результат теста, флаг исправности
        """
        if self.st_test_10():
            if self.st_test_11():
                if self.st_test_20():
                    if self.st_test_21():
                        if self.st_test_30():
                            return True, self._health_flag
        return False, self._health_flag

    def result_test_tzp(self) -> None:
        for t in range(len(self._list_delta_percent)):
            self._list_tzp_result.append((self._list_ust_num[t], self._list_delta_percent[t], self._list_delta_t[t]))
            self.logger.debug(f'{self._list_ust_num[t]}, {self._list_delta_percent[t]}, {self._list_delta_t[t]}')
        self.mysql_conn.mysql_tzp_result(self._list_tzp_result)
