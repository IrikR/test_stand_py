# -*- coding: utf-8 -*-
"""
!!! НОВЫЙ НЕ ОБКАТАНЫЙ !!!

Алгоритм проверки

Тип блока: БЗМП-П
Производитель: Пульсар

"""

__all__ = ["TestBZMPP"]

import logging
import sys
from time import sleep, time

from .general_func.database import *
from .general_func.exception import *
from .general_func.opc_full import ConnectOPC
from .general_func.procedure import *
from .general_func.reset import ResetRelay, ResetProtection
from .general_func.resistance import Resistor
from .general_func.utils import CLILog
from .gui.msgbox_1 import *


class TestBZMPP:
    """
    overload - перегрузка
    """

    def __init__(self):
        self.conn_opc = ConnectOPC()
        self.proc = Procedure()
        self.reset = ResetRelay()
        self.reset_protect = ResetProtection()
        self.resist = Resistor()
        self.mysql_conn = MySQLConnect()
        self.cli_log = CLILog("debug", __name__)

        self.ust_pmz: float = 25.2
        self.ust_faz: float = 8.2
        self.ust_overload: float = 10.7

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

        logging.basicConfig(
            filename="C:\\Stend\\project_class\\log\\TestBZMPP.log",
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
        1.1.	Проверка вероятности наличия короткого замыкания на входе измерительной цепи блока
        """
        self.cli_log.lev_info(f"старт теста {__doc__}", "skyblue")
        self.conn_opc.simplified_read_di(['inp_14', 'inp_15'])
        if my_msg(self.msg_1):
            pass
        else:
            return False
        meas_volt_ust = self.proc.procedure_1_21_31()
        if meas_volt_ust != 0.0:
            pass
        else:
            self.mysql_conn.mysql_ins_result("неисправен TV1", "1")
            return False
        self.conn_opc.ctrl_relay('KL73', True)
        sleep(5)
        self.logger.debug("таймаут 5 сек")
        self.cli_log.lev_debug("таймаут 5 сек", "gray")
        self.conn_opc.ctrl_relay('KL90', True)
        sleep(5)
        self.logger.debug("таймаут 5 сек")
        self.cli_log.lev_debug("таймаут 5 сек", "gray")
        self.conn_opc.ctrl_relay('KL63', True)
        min_volt = 0.6 * meas_volt_ust
        max_volt = 1.0 * meas_volt_ust
        meas_volt = self.conn_opc.read_ai('AI0')
        self.logger.debug(f'напряжение после включения KL63 '
                          f'{min_volt:.2f} <= {meas_volt:.2f} <= {max_volt:.2f}')
        if min_volt <= meas_volt <= max_volt:
            pass
        else:
            self.mysql_conn.mysql_ins_result('неисправен', '1')
            self.mysql_conn.mysql_error(455)
            self.reset.sbros_kl63_proc_1_21_31()
            return False
        self.reset.sbros_kl63_proc_1_21_31()
        return True

    def st_test_11(self) -> bool:
        """
        1.2. Определение коэффициента Кс отклонения фактического напряжения от номинального
        """
        self.coef_volt = self.proc.procedure_1_22_32()
        if self.coef_volt != 0.0:
            pass
        else:
            self.mysql_conn.mysql_ins_result("неисправен", "1")
            self.reset.stop_procedure_32()
            return False
        self.reset.stop_procedure_32()
        return True

    def st_test_12(self) -> bool:
        self.conn_opc.ctrl_relay('KL67', True)
        self.mysql_conn.progress_level(0.0)
        timer_test_1 = 0
        start_timer_test_1 = time()
        while timer_test_1 <= 120:
            sleep(0.2)
            timer_test_1 = time() - start_timer_test_1
            self.mysql_conn.progress_level(timer_test_1)
            inp_01, inp_05, inp_06 = self.conn_opc.simplified_read_di(['inp_01', 'inp_05', 'inp_06'])
            self.logger.debug(f'времени прошло:\t{timer_test_1:.1f}')
            if inp_01 is True and inp_05 is True and inp_06 is False:
                break
            else:
                continue
        self.mysql_conn.progress_level(0.0)
        self.mysql_conn.mysql_ins_result("исправен", "1")
        return True

    def st_test_20(self) -> bool:
        """
        Тест 2. Проверка срабатывания блока при снижении изоляции цепей 36В
        """
        if my_msg(self.msg_2):
            if my_msg(self.msg_3):
                return True
        return False

    def st_test_21(self) -> bool:
        self.conn_opc.ctrl_relay('KL21', True)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        self.conn_opc.ctrl_relay('KL27', True)
        sleep(0.1)
        self.logger.debug("таймаут 0.1 сек")
        self.cli_log.lev_debug("таймаут 0.1 сек", "gray")
        self.conn_opc.ctrl_relay('KL27', False)
        sleep(0.2)
        self.logger.debug("таймаут 0.2 сек")
        self.cli_log.lev_debug("таймаут 0.2 сек", "gray")
        inp_01, inp_05, inp_06 = self.conn_opc.simplified_read_di(['inp_01', 'inp_05', 'inp_06'])
        self.logger.debug(f"{inp_01 = }, {inp_05 = }, {inp_06 = }")
        if inp_01 is False and inp_05 is False and inp_06 is True:
            pass
        else:
            self.logger.debug("тест 2.1.1 положение выходов не соответствует")
            self.mysql_conn.mysql_ins_result("неисправен", "2")
            return False
        sleep(5)
        self.logger.debug("таймаут 5 сек")
        self.cli_log.lev_debug("таймаут 5 сек", "gray")
        inp_01, inp_05, inp_06 = self.conn_opc.simplified_read_di(['inp_01', 'inp_05', 'inp_06'])
        self.logger.debug(f"{inp_01 = }, {inp_05 = }, {inp_06 = }")
        if inp_01 is True and inp_05 is True and inp_06 is False:
            pass
        else:
            self.logger.debug("тест 2.1.2 положение выходов не соответствует")
            self.mysql_conn.mysql_ins_result("неисправен", "2")
            return False
        self.mysql_conn.mysql_ins_result("исправен", "2")
        return True

    def st_test_30(self) -> bool:
        """
        Тест 3. Проверка срабатывания блока при снижении силовой изоляции
        """
        if my_msg(self.msg_4):
            pass
        else:
            return False
        self.resist.resist_kohm(61)
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        inp_01, inp_05, inp_06 = self.conn_opc.simplified_read_di(['inp_01', 'inp_05', 'inp_06'])
        self.logger.debug(f"{inp_01 = }, {inp_05 = }, {inp_06 = }")
        if inp_01 is False and inp_05 is False and inp_06 is True:
            pass
        else:
            self.logger.debug("тест 3.0 положение выходов не соответствует")
            self.mysql_conn.mysql_ins_result("неисправен", "3")
            return False
        return True

    def st_test_31(self) -> bool:
        self.resist.resist_kohm(590)
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        inp_01, inp_05, inp_06 = self.conn_opc.simplified_read_di(['inp_01', 'inp_05', 'inp_06'])
        self.logger.debug(f"{inp_01 = }, {inp_05 = }, {inp_06 = }")
        if inp_01 is True and inp_05 is True and inp_06 is False:
            pass
        else:
            self.logger.debug("тест 3.1 положение выходов не соответствует")
            self.mysql_conn.mysql_ins_result("неисправен", "3")
            return False
        self.mysql_conn.mysql_ins_result("исправен", "3")
        return True

    def st_test_40(self) -> bool:
        """
        Тест 4. Проверка защиты ПМЗ
        """
        if my_msg(self.msg_5):
            pass
        else:
            return False
        if self.proc.procedure_x4_to_x5(coef_volt=self.coef_volt, setpoint_volt=self.ust_pmz):
            return True
        self.mysql_conn.mysql_ins_result("неисправен", "4")
        return False

    def st_test_41(self) -> bool:
        """
        4.2.  Проверка срабатывания блока от сигнала нагрузки:
        """
        self.conn_opc.ctrl_relay('KL63', True)
        sleep(0.5)
        self.logger.debug("таймаут 0.5 сек")
        self.cli_log.lev_debug("таймаут 0.5 сек", "gray")
        self.conn_opc.ctrl_relay('KL63', False)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        inp_01, inp_05, inp_06 = self.conn_opc.simplified_read_di(['inp_01', 'inp_05', 'inp_06'])
        self.logger.debug(f"{inp_01 = }, {inp_05 = }, {inp_06 = }")
        if inp_01 is False and inp_05 is False and inp_06 is True:
            pass
        else:
            self.logger.debug("положение выходов не соответствует")
            self.mysql_conn.mysql_ins_result("неисправен", "4")
            self.reset.stop_procedure_3()
            return False
        self.reset.stop_procedure_3()
        return True

    def st_test_42(self) -> bool:
        """
        4.2.2. Сброс защит после проверки
        """
        self.reset_protect.sbros_zashit_kl24()
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        inp_01, inp_05, inp_06 = self.conn_opc.simplified_read_di(['inp_01', 'inp_05', 'inp_06'])
        if inp_01 is True and inp_05 is True and inp_06 is False:
            pass
        else:
            self.logger.debug("положение выходов не соответствует")
            self.mysql_conn.mysql_ins_result("неисправен", "4")
            return False
        self.mysql_conn.mysql_ins_result("исправен", "4")
        return True

    def st_test_50(self) -> bool:
        """
        Тест 5. Проверка защиты от несимметрии фаз
        """
        if my_msg(self.msg_6):
            pass
        else:
            return False
        if self.proc.procedure_x4_to_x5(coef_volt=self.coef_volt, setpoint_volt=self.ust_faz):
            return True
        self.mysql_conn.mysql_ins_result("неисправен TV1", "5")
        return False

    def st_test_51(self) -> bool:
        """
        5.2.  Проверка срабатывания блока от сигнала нагрузки:
        """
        self.conn_opc.ctrl_relay('KL81', True)
        sleep(0.1)
        self.logger.debug("таймаут 0.1 сек")
        self.cli_log.lev_debug("таймаут 0.1 сек", "gray")
        self.conn_opc.ctrl_relay('KL63', True)
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        inp_09, *_ = self.conn_opc.simplified_read_di(['inp_09'])
        i = 0
        while inp_09 is False and i <= 10:
            inp_09, *_ = self.conn_opc.simplified_read_di(['inp_09'])
            i += 1
        start_timer = time()
        inp_05, *_ = self.conn_opc.simplified_read_di(['inp_05'])
        stop_timer = 0
        while inp_05 is True and stop_timer <= 12:
            inp_05, *_ = self.conn_opc.simplified_read_di(['inp_05'])
            stop_timer = time() - start_timer
        timer_test_5_2 = stop_timer
        self.logger.debug(f'таймер тест 6.2: {timer_test_5_2:.1f}')
        inp_01, inp_05, inp_06 = self.conn_opc.simplified_read_di(['inp_01', 'inp_05', 'inp_06'])
        if inp_01 is False and inp_05 is False and inp_06 is True and timer_test_5_2 <= 12:
            pass
        else:
            self.logger.debug("положение выходов не соответствует")
            self.mysql_conn.mysql_ins_result("неисправен", "5")
            self.reset.sbros_kl63_proc_all()
            self.conn_opc.ctrl_relay('KL81', False)
            return False
        self.reset.sbros_kl63_proc_all()
        self.conn_opc.ctrl_relay('KL81', False)
        self.conn_opc.ctrl_relay('KL24', True)
        sleep(4)
        self.logger.debug("таймаут 4 сек")
        self.cli_log.lev_debug("таймаут 4 сек", "gray")
        self.conn_opc.ctrl_relay('KL24', False)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        inp_01, inp_05, inp_06 = self.conn_opc.simplified_read_di(['inp_01', 'inp_05', 'inp_06'])
        if inp_01 is True and inp_05 is True and inp_06 is False:
            pass
        else:
            self.logger.debug("положение выходов не соответствует")
            self.mysql_conn.mysql_ins_result("неисправен", "5")
            return False
        self.mysql_conn.mysql_ins_result(f'исправен, {timer_test_5_2:.1f} сек', "5")
        return True

    def st_test_60(self) -> bool:
        """
        Тест 6. Проверка защиты от перегрузки
        """
        if my_msg(self.msg_7):
            pass
        else:
            return False
        if self.proc.procedure_x4_to_x5(coef_volt=self.coef_volt, setpoint_volt=self.ust_overload):
            return True
        self.mysql_conn.mysql_ins_result("неисправен", "6")
        return False

    def st_test_61(self) -> bool:
        """
        # 6.2.  Проверка срабатывания блока от сигнала нагрузки:
        """
        self.conn_opc.ctrl_relay('KL63', True)
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        self.mysql_conn.progress_level(0.0)
        inp_09, *_ = self.conn_opc.simplified_read_di(['inp_09'])
        k = 0
        while inp_09 is False and k <= 10:
            inp_09, *_ = self.conn_opc.simplified_read_di(['inp_09'])
            k += 1
        start_timer = time()
        inp_05, *_ = self.conn_opc.simplified_read_di(['inp_05'])
        stop_timer = 0
        while inp_05 is True and stop_timer <= 360:
            inp_05, *_ = self.conn_opc.simplified_read_di(['inp_05'])
            stop_timer = time() - start_timer
            self.mysql_conn.progress_level(stop_timer)
        self.timer_test_6_2 = stop_timer
        self.logger.debug(f'таймер тест 6.2: {self.timer_test_6_2:.1f}')
        self.mysql_conn.progress_level(0.0)
        inp_01, inp_05, inp_06 = self.conn_opc.simplified_read_di(['inp_01', 'inp_05', 'inp_06'])
        if inp_01 is False and inp_05 is False and inp_06 is True and self.timer_test_6_2 <= 360:
            pass
        else:
            self.logger.debug("положение выходов не соответствует")
            self.mysql_conn.mysql_ins_result("неисправен", "6")
            self.reset.sbros_kl63_proc_all()
            return False
        self.reset.sbros_kl63_proc_all()
        return True

    def st_test_62(self) -> bool:
        """
        Выдаем сообщение: «Сработала защита от перегрузки»
        6.6. Сброс защит после проверки
        :return:
        """
        self.reset_protect.sbros_zashit_kl24()
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        inp_01, inp_05, inp_06 = self.conn_opc.simplified_read_di(['inp_01', 'inp_05', 'inp_06'])
        if inp_01 is True and inp_05 is True and inp_06 is False:
            pass
        else:
            self.logger.debug("положение выходов не соответствует")
            self.mysql_conn.mysql_ins_result("неисправен", "6")
            return False
        self.mysql_conn.mysql_ins_result(f'исправен, {self.timer_test_6_2:.1f} сек', "6")
        return True

    def st_test_bzmp_p(self) -> [bool]:
        if self.st_test_10():
            if self.st_test_11():
                if self.st_test_12():
                    if self.st_test_20():
                        if self.st_test_21():
                            if self.st_test_30():
                                if self.st_test_31():
                                    if self.st_test_40():
                                        if self.st_test_41():
                                            if self.st_test_42():
                                                if self.st_test_50():
                                                    if self.st_test_51():
                                                        if self.st_test_60():
                                                            if self.st_test_61():
                                                                if self.st_test_62():
                                                                    return True, self.health_flag
        return False, self.health_flag

    def full_test_bzmp_p(self) -> None:
        try:
            start_time = time()
            test, health_flag = self.st_test_bzmp_p()
            end_time = time()
            time_spent = end_time - start_time
            self.cli_log.lev_info(f"Время выполнения: {time_spent}", "gray")
            self.logger.debug(f"Время выполнения: {time_spent}")
            self.mysql_conn.mysql_add_message(f"Время выполнения: {time_spent}")

            if test and not health_flag:
                self.mysql_conn.mysql_block_good()
                self.logger.debug('Блок исправен')
                self.cli_log.lev_info('Блок исправен', 'green')
                my_msg('Блок исправен', 'green')
            else:
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
