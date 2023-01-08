#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки

Тип блока	Производитель
БМЗ АПШ.М	Нет производителя
БМЗ АПШ.М	Электроаппарат-Развитие

"""

import sys
import logging

from time import sleep

from .gen_func_procedure import *
from .gen_func_utils import *
from .my_msgbox import *
from .gen_mb_client import *
from .gen_mysql_connect import *

__all__ = ["TestBMZAPSHM"]


class TestBMZAPSHM(object):

    def __init__(self):
        self.__proc = Procedure()
        self.__reset = ResetRelay()
        self.__ctrl_kl = CtrlKL()
        self.__read_mb = ReadMB()
        self.__mysql_conn = MySQLConnect()
        self.__fault = Bug(True)

        self.ust_1: float = 85.6

        self.coef_volt: float = 0.0
        self.health_flag: bool = False
        
        self.msg_1 = "Убедитесь в отсутствии блоков во всех испытательных разъемах. " \
                     "Вставьте блок в соответствующий испытательный разъем»"

        logging.basicConfig(filename="C:\Stend\project_class\TestBMZAPShM.log",
                            filemode="w",
                            level=logging.DEBUG,
                            encoding="utf-8",
                            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('WARNING')
        self.logger = logging.getLogger(__name__)

    def st_test_10_bmz_apsh_m(self) -> bool:
        """
        Тест 1. Проверка исходного состояния блока:
        """
        self.__inputs_a0()
        if my_msg(self.msg_1):
            pass
        else:
            return False
        self.__fault.debug_msg("тест 1", 4)
        self.__ctrl_kl.ctrl_relay('KL21', True)
        self.__reset.sbros_zashit_kl30()
        in_a1, in_a2, in_a5, in_a6 = self.__inputs_a()
        if in_a1 is False and in_a5 is True and in_a2 is False and in_a6 is True:
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '1')
            if in_a1 is True:
                self.__fault.debug_msg("вход 1 не соответствует", 1)
                self.__mysql_conn.mysql_error(347)
            elif in_a5 is False:
                self.__fault.debug_msg("вход 5 не соответствует", 1)
                self.__mysql_conn.mysql_error(348)
            elif in_a2 is True:
                self.__fault.debug_msg("вход 2 не соответствует", 1)
                self.__mysql_conn.mysql_error(349)
            elif in_a6 is False:
                self.__fault.debug_msg("вход 6 не соответствует", 1)
                self.__mysql_conn.mysql_error(350)
            return False
        self.__fault.debug_msg("состояние выходов соответствует", 3)
        return True

    def st_test_11_bmz_apsh_m(self) -> bool:
        """
        1.1. Проверка вероятности наличия короткого замыкания на входе измерительной цепи блока
        """
        self.__fault.debug_msg("тест 1.1", 4)
        meas_volt_ust = self.__proc.procedure_1_21_31()
        if meas_volt_ust != 0.0:
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '1')
            return False
        self.__fault.debug_msg("тест 1.1.2", 4)
        self.__ctrl_kl.ctrl_relay('KL63', True)
        meas_volt = self.__read_mb.read_analog()
        self.__fault.debug_msg(f'измеряем напряжение:\t {meas_volt}', 4)
        if 0.9 * meas_volt_ust <= meas_volt <= 1.1 * meas_volt_ust:
            pass
        else:
            self.__fault.debug_msg("напряжение не соответствует", 1)
            self.__mysql_conn.mysql_ins_result('неисправен', '1')
            self.__reset.sbros_kl63_proc_1_21_31()
            return False
        self.__fault.debug_msg("напряжение соответствует", 3)
        self.__fault.debug_msg("тест 1.1.3", 4)
        self.__reset.sbros_kl63_proc_1_21_31()
        return True

    def st_test_12_bmz_apsh_m(self) -> bool:
        """
        1.2. Определение коэффициента Кс отклонения фактического напряжения от номинального
        """
        self.__fault.debug_msg("тест 1.2", 4)
        self.coef_volt = self.__proc.procedure_1_22_32()
        if self.coef_volt != 0.0:
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '1')
            return False
        self.__fault.debug_msg(f'вычисляем коэффициент сети:\t {self.coef_volt}', 4)
        self.__reset.stop_procedure_32()
        self.__mysql_conn.mysql_ins_result('исправен', '1')
        self.__fault.debug_msg("тест 1 завершен", 3)
        return True

    def st_test_20_bmz_apsh_m(self) -> bool:
        """
        Тест 2. Проверка работы 1 канала блока
        """
        self.__fault.debug_msg("тест 2.0", 4)
        if self.__proc.procedure_x4_to_x5(coef_volt=self.coef_volt, setpoint_volt=self.ust_1):
            return True
        self.__mysql_conn.mysql_ins_result('неисправен', '2')
        return False

    def st_test_21_bmz_apsh_m(self) -> bool:
        """
        2.1.  Проверка срабатывания блока от сигнала нагрузки:
        """
        self.__fault.debug_msg("тест 2.1", 4)
        self.__ctrl_kl.ctrl_relay('KL63', True)
        sleep(3)
        self.__ctrl_kl.ctrl_relay('KL63', False)
        sleep(1)
        in_a1, in_a2, in_a5, in_a6 = self.__inputs_a()
        if in_a1 is True and in_a5 is False and in_a2 is False and in_a6 is True:
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '2')
            if in_a1 is False:
                self.__fault.debug_msg("вход 1 не соответствует", 1)
                self.__mysql_conn.mysql_error(352)
            elif in_a5 is True:
                self.__fault.debug_msg("вход 5 не соответствует", 1)
                self.__mysql_conn.mysql_error(353)
            elif in_a2 is True:
                self.__fault.debug_msg("вход 2 не соответствует", 1)
                self.__mysql_conn.mysql_error(354)
            elif in_a6 is False:
                self.__fault.debug_msg("вход 6 не соответствует", 1)
                self.__mysql_conn.mysql_error(355)
            return False
        self.__fault.debug_msg("выходы блока соответствуют", 3)
        self.__reset.stop_procedure_3()
        return True

    def st_test_22_bmz_apsh_m(self) -> bool:
        """
        2.2. Сброс защит после проверки
        """
        self.__fault.debug_msg("тест 2.2", 4)
        self.__reset.sbros_zashit_kl30()
        in_a1, in_a2, in_a5, in_a6 = self.__inputs_a()
        if in_a1 is False and in_a5 is True and in_a2 is False and in_a6 is True:
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '2')
            if in_a1 is True:
                self.__fault.debug_msg("вход 1 не соответствует", 1)
                self.__mysql_conn.mysql_error(356)
            elif in_a5 is False:
                self.__fault.debug_msg("вход 5 не соответствует", 1)
                self.__mysql_conn.mysql_error(357)
            elif in_a2 is True:
                self.__fault.debug_msg("вход 2 не соответствует", 1)
                self.__mysql_conn.mysql_error(358)
            elif in_a6 is False:
                self.__fault.debug_msg("вход 6 не соответствует", 1)
                self.__mysql_conn.mysql_error(359)
            return False
        self.__fault.debug_msg("выхода блока соответствуют", 3)
        self.__mysql_conn.mysql_ins_result('исправен', '2')
        self.__fault.debug_msg("тест 2 пройден", 3)
        return True

    def st_test_30_bmz_apsh_m(self) -> bool:
        """
        Тест 3. Проверка работы 2 канала блока
        """
        self.__fault.debug_msg("тест 3", 4)
        self.__ctrl_kl.ctrl_relay('KL73', True)
        if self.__proc.procedure_x4_to_x5(coef_volt=self.coef_volt, setpoint_volt=self.ust_1):
            return True
        self.__mysql_conn.mysql_ins_result('неисправен', '3')
        return False

    def st_test_31_bmz_apsh_m(self) -> bool:
        self.__ctrl_kl.ctrl_relay('KL63', True)
        sleep(3)
        self.__ctrl_kl.ctrl_relay('KL63', False)
        sleep(1)
        in_a1, in_a2, in_a5, in_a6 = self.__inputs_a()
        if in_a1 is False and in_a5 is True and in_a2 is True and in_a6 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '3')
            if in_a1 is True:
                self.__fault.debug_msg("вход 1 не соответствует", 1)
                self.__mysql_conn.mysql_error(360)
            elif in_a5 is False:
                self.__fault.debug_msg("вход 5 не соответствует", 1)
                self.__mysql_conn.mysql_error(361)
            elif in_a2 is False:
                self.__fault.debug_msg("вход 2 не соответствует", 1)
                self.__mysql_conn.mysql_error(362)
            elif in_a6 is True:
                self.__fault.debug_msg("вход 6 не соответствует", 1)
                self.__mysql_conn.mysql_error(363)
            return False
        self.__fault.debug_msg("состояние выходов соответствует", 3)
        self.__reset.stop_procedure_3()
        return True

    def st_test_32_bmz_apsh_m(self) -> bool:
        """
        3.2. Сброс защит после проверки
        """
        self.__fault.debug_msg("тест 3.2", 4)
        self.__reset.sbros_zashit_kl30()
        sleep(1)
        in_a1, in_a2, in_a5, in_a6 = self.__inputs_a()
        if in_a1 is False and in_a5 is True and in_a2 is False and in_a6 is True:
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '3')
            if in_a1 is True:
                self.__fault.debug_msg("вход 1 не соответствует", 1)
                self.__mysql_conn.mysql_error(364)
            elif in_a5 is False:
                self.__fault.debug_msg("вход 5 не соответствует", 1)
                self.__mysql_conn.mysql_error(365)
            elif in_a2 is False:
                self.__fault.debug_msg("вход 2 не соответствует", 1)
                self.__mysql_conn.mysql_error(366)
            elif in_a6 is True:
                self.__fault.debug_msg("вход 6 не соответствует", 1)
                self.__mysql_conn.mysql_error(367)
            return False
        self.__fault.debug_msg("состояние выходов блока соответсвует", 3)
        self.__mysql_conn.mysql_ins_result('исправен', '3')
        return True

    def __inputs_a0(self):
        in_a0 = self.__read_mb.read_discrete(0)
        if in_a0 is None:
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_a0

    def __inputs_a(self):
        in_a1 = self.__read_mb.read_discrete(1)
        in_a2 = self.__read_mb.read_discrete(2)
        in_a5 = self.__read_mb.read_discrete(5)
        in_a6 = self.__read_mb.read_discrete(6)
        if in_a1 is None or in_a2 is None or in_a5 is None or in_a6 is None:
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_a1, in_a2, in_a5, in_a6

    def st_test_bmz_apsh_m(self) -> bool:
        if self.st_test_10_bmz_apsh_m():
            if self.st_test_11_bmz_apsh_m():
                if self.st_test_12_bmz_apsh_m():
                    if self.st_test_20_bmz_apsh_m():
                        if self.st_test_21_bmz_apsh_m():
                            if self.st_test_22_bmz_apsh_m():
                                if self.st_test_30_bmz_apsh_m():
                                    if self.st_test_31_bmz_apsh_m():
                                        if self.st_test_32_bmz_apsh_m():
                                            return True
        return False

    def full_test_bmz_apsh_m(self):
        try:
            if self.st_test_bmz_apsh_m():
                self.__mysql_conn.mysql_block_good()
                my_msg('Блок исправен', 'green')
            else:
                self.__mysql_conn.mysql_block_bad()
                my_msg('Блок неисправен', 'red')
        except OSError:
            my_msg("ошибка системы", 'red')
        except SystemError:
            my_msg("внутренняя ошибка", 'red')
        except ModbusConnectException as mce:
            self.__fault.debug_msg(mce, 'red')
            my_msg(f'{mce}', 'red')
        finally:
            self.__reset.reset_all()
            sys.exit()


if __name__ == '__main__':
    test_bmz_apsh_m = TestBMZAPSHM()
    test_bmz_apsh_m.full_test_bmz_apsh_m()
    # reset_test_bmz_apsh_m = ResetRelay()
    # mysql_conn_bmz_apsh_m = MySQLConnect()
    # fault = Bug(True)
    # try:
    #     test_bmz_apsh_m = TestBMZAPSHM()
    #     if test_bmz_apsh_m.st_test_bmz_apsh_m():
    #         mysql_conn_bmz_apsh_m.mysql_block_good()
    #         my_msg('Блок исправен', 'green')
    #     else:
    #         mysql_conn_bmz_apsh_m.mysql_block_bad()
    #         my_msg('Блок неисправен', 'red')
    # except OSError:
    #     my_msg("ошибка системы", 'red')
    # except SystemError:
    #     my_msg("внутренняя ошибка", 'red')
    # except ModbusConnectException as mce:
    #     fault.debug_msg(mce, 'red')
    #     my_msg(f'{mce}', 'red')
    # finally:
    #     reset_test_bmz_apsh_m.reset_all()
    #     sys.exit()
