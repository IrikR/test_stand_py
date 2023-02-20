# -*- coding: utf-8 -*-
"""
ПРОВЕРЕН

Алгоритм проверки

Тип блока: БКЗ-ЗМК
Производитель: Без Производителя, ДонЭнергоЗавод, ИТЭП
Тип блока: БКЗ-Д
Производитель: Без Производителя, ДонЭнергоЗавод
Тип блока: БКЗ-З
Производитель: Без Производителя, ДонЭнергоЗавод, ИТЭП

"""

__all__ = ["TestBKZ3MK"]

import logging
import sys
from time import sleep, time

from .general_func.database import *
from .general_func.exception import *
from .general_func.opc_full import ConnectOPC
from .general_func.procedure import *
from .general_func.reset import ResetProtection, ResetRelay
from .general_func.resistance import Resistor
from .general_func.subtest import ProcedureFull
from .general_func.utils import CLILog
from .gui.msgbox_1 import *
from .gui.msgbox_2 import *


class TestBKZ3MK:

    def __init__(self):
        self.conn_opc = ConnectOPC()
        self.proc = Procedure()
        self.proc_full = ProcedureFull()
        self.reset_relay = ResetRelay()
        self.reset_protect = ResetProtection()
        self.resist = Resistor()
        self.mysql_conn = MySQLConnect()
        self.cli_log = CLILog("debug", __name__)

        # Тест 5. Проверка срабатывания защиты ТЗП блока по уставкам
        # медленные
        self.list_ust_tzp_num = (0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1)
        self.list_ust_tzp_volt = (4.7, 7.2, 8.7, 10.2, 11.6, 13.0, 14.4, 15.7, 17.6)
        self.list_delta_t_tzp = []
        self.list_delta_percent_tzp = []
        self.list_result_tzp = []
        # Тест 4. Проверка срабатывания защиты МТЗ блока по уставкам
        # быстрые
        self.list_ust_mtz_num = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
        self.list_ust_mtz_volt = (21.8, 27.2, 32.7, 38.1, 43.6, 49.0, 54.4, 59.9, 65.3, 70.8, 76.2)
        self.list_delta_t_mtz = []
        self.list_delta_percent_mtz = []
        self.list_result_mtz = []

        self.coef_volt: float = 0.0

        self.calc_delta_t_mtz: float = 0.0
        self.calc_delta_percent_mtz: float = 0.0
        self.delta_t_mtz: float = 0.0
        self.delta_percent_mtz: float = 0.0

        self.calc_delta_t_tzp: float = 0.0
        self.calc_delta_percent_tzp: float = 0.0
        self.delta_t_tzp: float = 0.0
        self.delta_percent_tzp: float = 0.0

        self.meas_volt: float = 0.0
        self.inp_01: bool = False
        self.inp_02: bool = False
        self.inp_05: bool = False
        self.inp_06: bool = False
        self.health_flag_mtz: bool = False
        self.health_flag_tzp: bool = False
        self.malfunction: bool = False

        self.msg_1 = "Убедитесь в отсутствии других блоков в панелях разъемов и вставьте " \
                     "блок в соответствующий разъем панели С»"
        self.msg_2 = "«Переключите регулятор МТЗ на корпусе блока в положение «1», регулятор ТЗП в положение " \
                     "«1.1» «Переключите тумблеры в положение «Работа» и «660В»"
        self.msg_3 = "Установите регулятор МТЗ (1-11), расположенный на корпусе блока, в положение"
        self.msg_4 = "Установите регулятор МТЗ (1-11), расположенный на блоке, в положение «11»"
        self.msg_5 = "Установите регулятор ТЗП (0.3-1.1), расположенный на блоке в положение"

        logging.basicConfig(filename="C:\\Stend\\project_class\\log\\TestBKZ3MK.log",
                            level=logging.DEBUG,
                            encoding="utf-8",
                            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s',
                            filemode="w")
        logging.getLogger('mysql').setLevel('WARNING')
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))

    def st_test_0(self) -> bool:
        self.cli_log.lev_info(f"старт теста {__doc__}", "skyblue")
        self.conn_opc.simplified_read_di(['inp_14', 'inp_15'])
        if my_msg(self.msg_1):
            if my_msg(self.msg_2):
                self.mysql_conn.mysql_ins_result('---', '1')
                self.mysql_conn.mysql_ins_result('---', '2')
                self.mysql_conn.mysql_ins_result('---', '3')
                return True
        return False

    def st_test_10(self) -> bool:
        """
        Тест 1. Проверка исходного состояния блока:
        """
        self.logger.debug("тест 1.0")
        self.mysql_conn.mysql_ins_result('идет тест 1', '1')
        self.conn_opc.ctrl_relay('KL21', True)
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        self.reset_protect.sbros_zashit_kl30(time_on=1.5, time_off=2.0)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=1, subtest_num=1.0,
                                         err_code=[317, 318],
                                         position_inp=[True, True],
                                         di_xx=['inp_05', 'inp_06']):
            return True
        return False

    def st_test_11(self) -> bool:
        """
        1.1.2. Проверка отсутствия короткого замыкания на входе измерительной части блока:
        1.2. Определение коэффициента Кс отклонения фактического напряжения от номинального
        """
        if self.proc_full.procedure_1_full(test_num=1, subtest_num=1.1):
            self.coef_volt = self.proc_full.procedure_2_full(test_num=1, subtest_num=1.2)
            return True
        return False

    def st_test_20(self) -> bool:
        """
        Тест 2. Проверка работы блока при нормальном сопротивлении изоляции контролируемого присоединения
        """
        self.logger.debug("тест 2.0")
        self.mysql_conn.mysql_ins_result('идет тест 2', '2')
        self.resist.resist_kohm(200)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=2, subtest_num=2.0,
                                         err_code=[319, 320],
                                         position_inp=[True, True],
                                         di_xx=['inp_05', 'inp_06']):
            return True
        return False

    def st_test_30(self) -> bool:
        """
        Тест 3. Проверка работы блока при снижении уровня сопротивлении изоляции ниже аварийной уставки
        """
        self.logger.debug("тест 3.0")
        self.mysql_conn.mysql_ins_result('идет тест 3.0', '3')
        self.conn_opc.ctrl_relay('KL22', True)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=3, subtest_num=3.0,
                                         err_code=[321, 322],
                                         position_inp=[True, False],
                                         di_xx=['inp_05', 'inp_06']):
            return True
        return False

    def st_test_31(self) -> bool:
        self.resist.resist_kohm(590)
        self.conn_opc.ctrl_relay('KL22', False)
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        self.reset_protect.sbros_zashit_kl30(time_on=1.5, time_off=2.0)
        if self.conn_opc.subtest_read_di(test_num=3, subtest_num=3.1,
                                         err_code=[321, 322],
                                         position_inp=[True, True],
                                         di_xx=['inp_05', 'inp_06']):
            return True
        return False

    def st_test_40(self) -> bool:
        """
        Тест 4. Проверка срабатывания защиты МТЗ блока по уставкам
        Δ% = 9,19125*U4
        """
        self.logger.debug("тест 4.0")
        self.mysql_conn.mysql_ins_result('идет тест 4.0', '4')
        k = 0
        for i in self.list_ust_mtz_volt:
            self.malfunction = False

            msg_result_mtz = my_msg_2(f'{self.msg_3} {self.list_ust_mtz_num[k]}')
            self.logger.debug(f"значение полученное от пользователя: {msg_result_mtz}")

            if msg_result_mtz == 0:
                pass
            elif msg_result_mtz == 1:
                return False
            elif msg_result_mtz == 2:
                self.mysql_conn.mysql_add_message(f'уставка МТЗ {self.list_ust_mtz_num[k]} пропущена')
                self.list_delta_percent_mtz.append('пропущена')
                self.list_delta_t_mtz.append('пропущена')
                k += 1
                continue

            # 4.1.  Проверка срабатывания блока от сигнала нагрузки:
            self.logger.debug("4.1.  Проверка срабатывания блока от сигнала нагрузки:")
            self.mysql_conn.mysql_add_message(f'уставка МТЗ: {self.list_ust_mtz_num[k]}, подтест 4.1')
            self.proc.procedure_1_24_34(coef_volt=self.coef_volt, setpoint_volt=i, factor=1.0)
            self.meas_volt = self.conn_opc.read_ai('AI0')
            self.func_delta_t_mtz(k=k)
            self.reset_relay.stop_procedure_3()
            # если не прошел предыдущий тест, то повышаем напряжение в 1.1 раза и повторяем проверку
            if self.calc_delta_t_mtz == 9999 or self.malfunction is True:
                self.proc.procedure_1_24_34(coef_volt=self.coef_volt, setpoint_volt=i, factor=1.1)
                self.meas_volt = self.conn_opc.read_ai('AI0')
                self.func_delta_t_mtz(k=k)
                self.reset_relay.stop_procedure_3()
            else:
                pass

            # обработка полученных результатов
            self.logger.debug("обработка полученных результатов")
            self.mysql_conn.mysql_add_message(f'уставка МТЗ: {self.list_ust_mtz_num[k]}, подтест 4.2')
            self.calc_delta_percent_mtz = self.meas_volt * 9.19125
            self.logger.info(f"коэффициент напряжения: {self.calc_delta_percent_mtz}")
            if self.calc_delta_t_mtz == 9999 or self.malfunction is True:
                self.delta_t_mtz = 'неисправен'
                self.delta_percent_mtz = 'неисправен'
                self.health_flag_mtz = True
            elif self.calc_delta_t_mtz <= 10 and self.malfunction is False:
                self.delta_t_mtz = '< 10'
                self.delta_percent_mtz = f"{self.calc_delta_percent_mtz:.2f}"
            elif self.calc_delta_t_mtz != 9999 and self.malfunction is False:
                self.delta_t_mtz = f"{self.calc_delta_t_mtz:.1f}"
                self.delta_percent_mtz = f"{self.calc_delta_percent_mtz:.2f}"
            self.logger.info(f"время срабатывания: {self.calc_delta_t_mtz}")

            # запись результатов в БД
            self.logger.debug("запись результатов в БД")
            result = f'уставка МТЗ: {self.list_ust_mtz_num[k]}, дельта %: {self.calc_delta_percent_mtz:.2f}, ' \
                     f'дельта t: {self.delta_t_mtz}'
            self.logger.info(result)
            #
            self.mysql_conn.mysql_add_message(result)
            self.list_delta_percent_mtz.append(f'{self.calc_delta_percent_mtz:.2f}')
            self.list_delta_t_mtz.append(f'{self.delta_t_mtz}')

            # сброс защиты блока после проверки
            self.logger.debug("сброс защиты блока после проверки")
            if self.reset_protection(test_num=4, subtest=4.3, err1=325, err2=326):
                k += 1
                continue
            else:
                self.mysql_conn.mysql_ins_result('неисправен', '4')
                self.health_flag_mtz = True
                return False
        if self.health_flag_mtz is True:
            self.mysql_conn.mysql_ins_result('неисправен', '4')
        else:
            pass
        self.logger.debug("тест 4 завершен")
        return True

    def st_test_50(self) -> bool:
        """
        Тест 5. Проверка срабатывания защиты ТЗП блока по уставкам
        """
        self.logger.debug("тест 5.0")
        self.malfunction = False
        if my_msg(self.msg_4):
            pass
        else:
            return False
        if self.reset_protection(test_num=5, subtest=5.0, err1=329, err2=330):
            pass
        else:
            return False
        m = 0
        for n in self.list_ust_tzp_volt:
            self.logger.debug(f"проверка уставки: {self.list_ust_tzp_volt[m]}")
            self.malfunction = False

            self.mysql_conn.mysql_add_message(f'уставка ТЗП: {self.list_ust_tzp_num[m]}, подтест 5.1')
            msg_result_tzp = my_msg_2(f'{self.msg_5} {self.list_ust_tzp_num[m]}')
            if msg_result_tzp == 0:
                pass
            elif msg_result_tzp == 1:
                return False
            elif msg_result_tzp == 2:
                self.mysql_conn.mysql_add_message(f'уставка ТЗП {self.list_ust_tzp_num[m]} пропущена')
                self.list_delta_percent_tzp.append('пропущена')
                self.list_delta_t_tzp.append('пропущена')
                m += 1
                continue

            # формирование напряжения для проверки по уставкам
            self.proc.procedure_x4_to_x5(coef_volt=self.coef_volt, setpoint_volt=n)
            self.meas_volt = self.conn_opc.read_ai('AI0')

            # 5.4.  Проверка срабатывания блока от сигнала нагрузки:
            self.func_delta_t_tzp()
            self.reset_relay.sbros_kl63_proc_all()

            # обработка результата
            # Δ%= 0.06075*(U4)2 + 8.887875*U4
            self.calc_delta_percent_tzp = 0.06075 * self.meas_volt ** 2 + 8.887875 * self.meas_volt

            if self.malfunction is True:
                self.delta_t_tzp = 'неисправен'
                self.delta_percent_tzp = 'неисправен'
                self.health_flag_tzp = True
            else:
                self.delta_t_tzp = f"{self.calc_delta_t_tzp:.1f}"
                self.delta_percent_tzp = f"{self.calc_delta_percent_tzp:.2f}"
            result = f'уставка ТЗП: {self.list_ust_tzp_num[m]} [дельта %: {self.delta_percent_tzp}, ' \
                     f'дельта t: {self.delta_t_mtz}]'

            # запись результатов в БД и логи
            self.list_delta_percent_tzp.append(self.delta_percent_tzp)
            self.list_delta_t_tzp.append(self.delta_t_tzp)
            self.mysql_conn.mysql_add_message(result)
            self.logger.info(result)
            self.mysql_conn.progress_level(0.0)

            if self.reset_protection(test_num=5, subtest=5.0, err1=329, err2=330):
                m += 1
                continue
            else:
                self.health_flag_tzp = True
                self.mysql_conn.mysql_ins_result('неисправен', '5')
                return False

        if self.health_flag_tzp is True:
            self.logger.debug("тест 5 завершен, блок неисправен")
            self.mysql_conn.mysql_ins_result('неисправен', '5')
        self.mysql_conn.mysql_ins_result('исправен', '5')
        return True

    def reset_protection(self, *, test_num: int, subtest: float, err1: int, err2: int) -> bool:
        """

        :param test_num:
        :param subtest:
        :param err1: для теста 4.5 = 325, для 5.5 = 329
        :param err2: для теста 4.5 = 326, для 5.5 = 330
        :return:
        """
        self.logger.debug(f"подтест {subtest}, сброс защиты блока")
        self.mysql_conn.mysql_ins_result(f'идет тест {subtest}', f'{test_num}')
        self.reset_protect.sbros_zashit_kl30(time_on=1.5, time_off=2.0)
        if self.conn_opc.subtest_read_di(test_num=test_num, subtest_num=subtest,
                                         err_code=[err1, err2],
                                         position_inp=[True, True],
                                         di_xx=['inp_05', 'inp_06']):
            return True
        self.mysql_conn.mysql_add_message("Блок не исправен. Не работает сброс защит.")
        return False

    def func_delta_t_tzp(self) -> None:
        self.conn_opc.ctrl_relay('KL63', True)
        inp_09, *_ = self.conn_opc.simplified_read_di(['inp_09'])
        i = 0
        while inp_09 is False and i <= 20:
            inp_09, *_ = self.conn_opc.simplified_read_di(['inp_09'])
            i += 1
        if inp_09 is True:
            start_timer = time()
            meas_time = 0
            self.inp_05, self.inp_06 = self.conn_opc.simplified_read_di(['inp_05', 'inp_06'])
            while self.inp_06 is True and meas_time <= 370:
                self.inp_05, self.inp_06 = self.conn_opc.simplified_read_di(['inp_05', 'inp_06'])
                meas_time = time() - start_timer
                self.mysql_conn.progress_level(meas_time)
            if self.inp_06 is False:
                stop_timer = time()
                self.calc_delta_t_tzp = stop_timer - start_timer
                self.malfunction = False
            else:
                self.malfunction = True
        else:
            self.malfunction = True

    def func_delta_t_mtz(self, *, k) -> None:
        for qw in range(3):
            if self.reset_protection(test_num=4, subtest=4.1, err1=325, err2=326):
                self.calc_delta_t_mtz, self.inp_01, self.inp_02, \
                    self.inp_05, self.inp_06 = self.conn_opc.ctrl_ai_code_v0(code=105)
                # sleep(2)
                # self.inp_05, self.inp_06 = self.conn_opc.simplified_read_di(['inp_05', 'inp_06'])
                result_delta_t = f"уставка МТЗ: {self.list_ust_mtz_num[k]}; попытка: {qw}; " \
                                 f"время: {self.calc_delta_t_mtz}"
                self.logger.info(result_delta_t)
                self.mysql_conn.mysql_add_message(result_delta_t)
                self.logger.debug(f"{self.inp_05 = } (False), {self.inp_06 = } (True)")
                if self.calc_delta_t_mtz == 9999:
                    sleep(3)
                    qw += 1
                    self.logger.debug("блок не сработал по времени, повтор проверки блока")
                    self.mysql_conn.mysql_add_message("блок не сработал по времени, повтор проверки блока")
                    self.malfunction = True
                    continue
                elif self.calc_delta_t_mtz != 9999 and self.inp_05 is False and self.inp_06 is True:
                    self.logger.debug(f"блок сработал, время срабатывания: {self.calc_delta_t_mtz:.1f}")
                    self.mysql_conn.mysql_add_message(f"блок сработал, время срабатывания: {self.calc_delta_t_mtz:.1f}")
                    self.malfunction = False
                    break
                else:
                    self.logger.debug("блок не сработал по положению контактов, повтор проверки блока")
                    self.mysql_conn.mysql_add_message("блок не сработал по положению контактов, повтор проверки блока")
                    self.malfunction = True
                    sleep(3)
                    qw += 1
                    continue
            else:
                self.health_flag_mtz = True
                self.malfunction = True
                break

    def st_test_bkz_3mk(self) -> [bool, bool, bool]:
        if self.st_test_0():
            if self.st_test_10():
                if self.st_test_11():
                    if self.st_test_20():
                        if self.st_test_30():
                            if self.st_test_31():
                                if self.st_test_40():
                                    if self.st_test_50():
                                        return True, self.health_flag_mtz, self.health_flag_tzp
        return False, self.health_flag_mtz, self.health_flag_tzp

    def result_test_bkz_3mk(self) -> None:
        for g1 in range(len(self.list_delta_percent_mtz)):
            self.list_result_mtz.append((self.list_ust_mtz_num[g1],
                                         self.list_delta_percent_mtz[g1],
                                         self.list_delta_t_mtz[g1]))
        self.mysql_conn.mysql_pmz_result(self.list_result_mtz)
        self.logger.info(f"результат проверки МТЗ: {self.list_result_mtz}")
        for g2 in range(len(self.list_delta_percent_tzp)):
            self.list_result_tzp.append((self.list_ust_tzp_num[g2],
                                         self.list_delta_percent_tzp[g2],
                                         self.list_delta_t_tzp[g2]))
        self.mysql_conn.mysql_tzp_result(self.list_result_tzp)
        self.logger.info(f"результат проверки ТЗП: {self.list_result_tzp}")

    def full_test_bkz_3mk(self) -> None:
        try:
            start_time = time()
            test, health_flag_mtz, health_flag_tzp = self.st_test_bkz_3mk()
            end_time = time()
            time_spent = end_time - start_time
            self.cli_log.lev_info(f"Время выполнения: {time_spent}", "gray")
            self.logger.debug(f"Время выполнения: {time_spent}")
            self.mysql_conn.mysql_add_message(f"Время выполнения: {time_spent}")
            if test and not health_flag_mtz and not health_flag_tzp:
                self.mysql_conn.mysql_block_good()
                self.result_test_bkz_3mk()
                self.logger.debug('Блок исправен')
                self.cli_log.lev_info('Блок исправен', 'green')
                my_msg('Блок исправен', 'green')
            else:
                self.mysql_conn.mysql_block_bad()
                self.result_test_bkz_3mk()
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
