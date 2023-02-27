# -*- coding: utf-8 -*-
"""
!!! НОВЫЙ НЕ ОБКАТАНЫЙ !!!

Алгоритм проверки

Тип блока: ММТЗ-Д
Производитель: Нет производителя, ДонЭнергоЗавод

"""

__all__ = ["TestMMTZD"]

import logging
from time import sleep

from .general_func.database import *
from .general_func.opc_full import ConnectOPC
from .general_func.procedure import *
from .general_func.reset import ResetProtection, ResetRelay
from .general_func.subtest import ProcedureFull
from .general_func.utils import CLILog
from .gui.msgbox_1 import *
from .gui.msgbox_2 import *


class TestMMTZD:

    def __init__(self):
        self.conn_opc = ConnectOPC()
        self.reset_relay = ResetRelay()
        self.reset_protect = ResetProtection()
        self.proc = Procedure()
        self.proc_full = ProcedureFull()
        self.mysql_conn = MySQLConnect()
        self.cli_log = CLILog("debug", __name__)

        self.list_ust_num: tuple[int, ...] = (10, 20, 30, 40, 50)
        # self.ust = (7.7, 16.5, 25.4, 31.9, 39.4)
        self.list_ust_volt: tuple[float, ...] = (8.0, 16.5, 25.4, 31.9, 39.4)
        self.list_num_yach_test_2: tuple[int, ...] = (3, 4, 5, 6, 7)
        self.list_num_yach_test_3: tuple[int, ...] = (9, 10, 11, 12, 13)

        self.meas_volt_ust: float = 0.0
        self.coef_volt: float = 0.0
        self.health_flag: bool = False

        self.inp_01: bool = False
        self.inp_05: bool = False

        self.msg_1: str = "Убедитесь в отсутствии в панелях разъемов установленных блоков. " \
                          "Подключите блок в разъем Х21 на панели С"
        self.msg_2: str = "Переключите тумблер режимов, расположенный на корпусе блока, в положение «Работа»"
        self.msg_3: str = "Установите регулятор уставок III канала, расположенного на блоке в положение «50»"
        self.msg_4: str = "Установите регулятор уставок II канала, расположенного на блоке в положение\t"
        self.msg_5: str = "Установите регулятор уставок II канала, расположенного на блоке в положение «50»"
        self.msg_6: str = "Установите регулятор уставок III канала, расположенного на блоке в положение\t"

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
        self.cli_log.lev_info(f"старт теста {__doc__}", "skyblue")
        if my_msg(self.msg_1):
            if my_msg(self.msg_2):
                return True
        return False

    def st_test_11(self) -> bool:
        """
        Тест 1.1.
        Коды ошибок 412 и 413
        :return: bool
        """
        err_code = [412, 413]
        self.conn_opc.ctrl_relay('KL33', True)
        if self.reset_protection(test_num=1, subtest_num=1.1, err_code=err_code):
            return True
        return False

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
        err_code = [417, 418]

        if not my_msg(self.msg_3):
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
            self.conn_opc.ctrl_ai_code_v1(106)
            sleep(3)
            self.inp_01, self.inp_05 = self.conn_opc.simplified_read_di(['inp_01', 'inp_05'])
            self.reset_relay.stop_procedure_3()
            if self.inp_01 is False and self.inp_05 is False:
                self.logger.debug("положение выходов блока соответствует")
                if self.reset_protection(test_num=2, subtest_num=2.0, err_code=err_code):
                    self.mysql_conn.mysql_ins_result('исправен', f'{self.list_num_yach_test_2[k]}')
                else:
                    self.mysql_conn.mysql_ins_result('неисправен', f'{self.list_num_yach_test_2[k]}')
                    return False
            elif self.inp_01 is True:
                if self.subtest_22(i):
                    self.mysql_conn.mysql_ins_result('исправен', f'{self.list_num_yach_test_2[k]}')
                else:
                    self.mysql_conn.mysql_ins_result('неисправен', '2')
                    self.mysql_conn.mysql_error(415)
                    self.mysql_conn.mysql_ins_result('неисправен', f'{self.list_num_yach_test_2[k]}')
                    return False
            elif self.inp_05 is True:
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
        err_code = [417, 418]

        self.conn_opc.ctrl_relay('KL73', True)
        sleep(5)
        self.logger.debug("таймаут 5 сек")
        self.cli_log.lev_debug("таймаут 5 сек", "gray")

        if not my_msg(self.msg_5):
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

            self.conn_opc.ctrl_ai_code_v1(106)
            sleep(3)
            self.inp_01, self.inp_05 = self.conn_opc.simplified_read_di(['inp_01', 'inp_05'])
            self.reset_relay.stop_procedure_3()
            if self.inp_01 is False and self.inp_05 is False:
                if self.reset_protection(test_num=3, subtest_num=3.0, err_code=err_code):
                    self.mysql_conn.mysql_ins_result('исправен', f'{self.list_num_yach_test_3[x]}')
                else:
                    self.mysql_conn.mysql_ins_result('неисправен', f'{self.list_num_yach_test_3[x]}')
                    return False
            elif self.inp_01 is True:
                if self.subtest_32(y):
                    self.mysql_conn.mysql_ins_result('исправен', f'{self.list_num_yach_test_3[x]}')
                else:
                    self.mysql_conn.mysql_ins_result('неисправен', '3')
                    self.mysql_conn.mysql_error(419)
                    self.mysql_conn.mysql_ins_result('неисправен', f'{self.list_num_yach_test_3[x]}')
                    return False
            elif self.inp_05 is True:
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
        if not self.reset_protection(test_num=2, subtest_num=2.2, err_code=[417, 418]):
            return False

        if self.proc.procedure_1_24_34(coef_volt=self.coef_volt, setpoint_volt=i, factor=1.1):
            pass
        else:
            self.mysql_conn.mysql_ins_result('неисправен', '2')

        # 2.2.2.  Проверка срабатывания блока от сигнала нагрузки:
        self.conn_opc.ctrl_ai_code_v1(107)
        sleep(3)
        self.logger.debug("таймаут 3 сек")
        self.cli_log.lev_debug("таймаут 3 сек", "gray")

        self.inp_01, self.inp_05 = self.conn_opc.simplified_read_di(['inp_01', 'inp_05'])
        self.reset_relay.stop_procedure_3()
        if self.inp_01 is False and self.inp_05 is False:
            if self.reset_protection(test_num=2, subtest_num=2.3, err_code=[417, 418]):
                return True
            return False
        elif self.inp_01 is True:
            self.mysql_conn.mysql_ins_result('неисправен', '2')
            self.mysql_conn.mysql_error(415)
            if self.reset_protection(test_num=2, subtest_num=2.3, err_code=[417, 418]):
                return True
            return False
        elif self.inp_05 is True:
            self.mysql_conn.mysql_ins_result('неисправен', '2')
            self.mysql_conn.mysql_error(416)
            if self.reset_protection(test_num=2, subtest_num=2.3, err_code=[417, 418]):
                return True
            return False

    def subtest_32(self, y) -> bool:
        """
        3.2. Формирование нагрузочного сигнала 1,1*calc_volt[i]:
        :param y:
        :return:
        """
        if not self.reset_protection(test_num=3, subtest_num=3.2, err_code=[417, 418]):
            return False

        if self.proc.procedure_1_24_34(coef_volt=self.coef_volt, setpoint_volt=y, factor=1.1):
            pass
        else:
            self.mysql_conn.mysql_ins_result('неисправен', '3')
            return False

        # 2.2.2.  Проверка срабатывания блока от сигнала нагрузки:
        self.conn_opc.ctrl_ai_code_v1(107)
        sleep(3)
        self.logger.debug("таймаут 3 сек")
        self.cli_log.lev_debug("таймаут 3 сек", "gray")

        self.inp_01, self.inp_05 = self.conn_opc.simplified_read_di(['inp_01', 'inp_05'])
        self.reset_relay.stop_procedure_3()
        if self.inp_01 is False and self.inp_05 is False:
            if self.reset_protection(test_num=3, subtest_num=3.3, err_code=[417, 418]):
                return True
            return False

        elif self.inp_01 is True:
            self.mysql_conn.mysql_ins_result('неисправен', '3')
            self.mysql_conn.mysql_error(419)
            if self.reset_protection(test_num=3, subtest_num=3.3, err_code=[417, 418]):
                return True
            return False

        elif self.inp_05 is True:
            self.mysql_conn.mysql_ins_result('неисправен', '3')
            self.mysql_conn.mysql_error(420)
            if self.reset_protection(test_num=3, subtest_num=3.3, err_code=[417, 418]):
                return True
            return False

    def reset_protection(self, test_num: int, subtest_num: float, err_code: list[int]) -> bool:
        """
        Сброс защит с последующей проверкой состояния выходов блока.
        :param test_num: Номер теста
        :param subtest_num: Номер подтеста
        :param err_code: для тестов 3.х будет 417 и 418
        :return: bool
        """
        self.reset_protect.sbros_zashit_kl1()
        if self.conn_opc.subtest_read_di(test_num=test_num, subtest_num=subtest_num,
                                         err_code=err_code,
                                         position_inp=[True, True],
                                         di_xx=['inp_01', 'inp_05']):
            return True
        return False

    def st_test_mmtz_d(self) -> [bool, bool]:
        """
            Главная функция которая собирает все остальные
            :type: bool, bool
            :return:  результат теста, флаг исправности
        """
        if self.st_test_10():
            if self.st_test_11():
                if self.st_test_12():
                    if self.st_test_20():
                        if self.st_test_30():
                            return True, self.health_flag
        return False, self.health_flag
