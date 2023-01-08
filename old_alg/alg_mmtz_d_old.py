#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки

Тип блока	Производитель
ММТЗ-Д	Нет производителя
ММТЗ-Д	ДонЭнергоЗавод

"""

import sys
import logging

from time import sleep

from .gen_func_procedure import *
from .gen_func_utils import *
from .my_msgbox import *
from .my_msgbox_2 import *
from .gen_mb_client import *
from .gen_mysql_connect import *

__all__ = ["TestMMTZD"]


class TestMMTZD(object):

    def __init__(self):
        self.__reset = ResetRelay()
        self.__proc = Procedure()
        self.__read_mb = ReadMB()
        self.__ctrl_kl = CtrlKL()
        self.__mysql_conn = MySQLConnect()
        self.__fault = Bug(True)

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

        logging.basicConfig(filename="C:\Stend\project_class\TestMMTZD.log",
                            filemode="w",
                            level=logging.DEBUG,
                            encoding="utf-8",
                            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('WARNING')
        self.logger = logging.getLogger(__name__)

    def st_test_10(self) -> bool:
        """
        Тест 1. Проверка исходного состояния блока:
        :return:
        """
        self.__inputs_a0()
        if my_msg(self.msg_1):
            if my_msg(self.msg_2):
                return True
        return False

    def st_test_11(self) -> bool:
        self.__ctrl_kl.ctrl_relay('KL33', True)
        self.__reset.sbros_zashit_kl1()
        in_a1, in_a5 = self.__inputs_a()
        if in_a1 is True and in_a5 is True:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", "1")
            if in_a1 is False:
                self.__fault.debug_msg("положение входа 1 не соответствует", 1)
                self.__mysql_conn.mysql_error(412)
            elif in_a5 is False:
                self.__fault.debug_msg("положение входа 5 не соответствует", 1)
                self.__mysql_conn.mysql_error(413)
            return False
        self.__fault.debug_msg("положение выходов блока соответствует", 3)
        return True

    def st_test_12(self) -> bool:
        """
        1.1. Проверка вероятности наличия короткого замыкания на входе измерительной цепи блока
        :return:
        """
        self.meas_volt_ust = self.__proc.procedure_1_21_31()
        if self.meas_volt_ust != 0.0:
            return True
        self.__mysql_conn.mysql_ins_result("неисправен", "1")
        return False

    def st_test_13(self) -> bool:
        """
        1.1.2. Проверка отсутствия короткого замыкания на входе измерительной части блока:
        :return:
        """
        self.__fault.debug_msg("тест 1.1.2 начало\t", 3)
        self.__ctrl_kl.ctrl_relay('KL63', True)
        min_volt = 0.4 * self.meas_volt_ust
        max_volt = 1.1 * self.meas_volt_ust
        meas_volt = self.__read_mb.read_analog()
        self.__fault.debug_msg(f'напряжение после включения KL63\t{meas_volt:.2f}\tдолжно быть '
                               f'от\t{min_volt:.2f}\tдо\t{max_volt:.2f}', 3)
        if min_volt <= meas_volt <= max_volt:
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '1')
            self.__mysql_conn.mysql_error(455)
            self.__reset.sbros_kl63_proc_1_21_31()
            return False
        self.__reset.sbros_kl63_proc_1_21_31()
        return True

    def st_test_14(self) -> bool:
        """
        1.2. Определение коэффициента Кс отклонения фактического напряжения от номинального
        :return:
        """
        self.coef_volt = self.__proc.procedure_1_22_32()
        self.__fault.debug_msg(f'коэф. сети равен: {self.coef_volt:.2f}', 2)
        if self.coef_volt != 0.0:
            pass
        else:
            self.__reset.stop_procedure_32()
            self.__mysql_conn.mysql_ins_result('неисправен', '1')
            return False
        self.__mysql_conn.mysql_ins_result('исправен', '1')
        self.__reset.stop_procedure_32()
        return True

    def st_test_20(self) -> bool:
        """
        Тест 2. Проверка срабатывания защиты II канала по уставкам
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
                self.__mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[k]} пропущена')
                k += 1
                continue
            if self.__proc.procedure_x4_to_x5(coef_volt=self.coef_volt, setpoint_volt=i):
                pass
            else:
                self.__mysql_conn.mysql_ins_result('неисправен', '2')
                return False
            # 2.1.  Проверка срабатывания блока от сигнала нагрузки:
            self.__ctrl_kl.ctrl_ai_code_v1(106)
            sleep(3)
            in_a1, in_a5 = self.__inputs_a()
            self.__reset.stop_procedure_3()
            if in_a1 is False and in_a5 is False:
                self.__fault.debug_msg("положение выходов блока соответствует", 3)
                if self.__subtest_23():
                    self.__mysql_conn.mysql_ins_result('исправен', f'{self.list_num_yach_test_2[k]}')
                else:
                    self.__mysql_conn.mysql_ins_result('неисправен', f'{self.list_num_yach_test_2[k]}')
                    return False
            elif in_a1 is True:
                if self.__subtest_22(i):
                    self.__mysql_conn.mysql_ins_result('исправен', f'{self.list_num_yach_test_2[k]}')
                else:
                    self.__mysql_conn.mysql_ins_result('неисправен', '2')
                    self.__mysql_conn.mysql_error(415)
                    self.__mysql_conn.mysql_ins_result('неисправен', f'{self.list_num_yach_test_2[k]}')
                    return False
            elif in_a5 is True:
                if self.__subtest_22(i):
                    self.__mysql_conn.mysql_ins_result('исправен', f'{self.list_num_yach_test_2[k]}')
                else:
                    self.__mysql_conn.mysql_ins_result('неисправен', '2')
                    self.__mysql_conn.mysql_error(416)
                    self.__mysql_conn.mysql_ins_result('неисправен', f'{self.list_num_yach_test_2[k]}')
                    return False
            k += 1
        self.__mysql_conn.mysql_ins_result('исправен', '2')
        return True

    def st_test_30(self) -> bool:
        """
        Тест 3. Проверка срабатывания защиты III канала по уставкам
        :return:
        """
        self.__ctrl_kl.ctrl_relay('KL73', True)
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
                self.__mysql_conn.mysql_add_message(f'уставка {self.list_ust_num[x]} пропущена')
                x += 1
                continue
            if self.__proc.procedure_x4_to_x5(coef_volt=self.coef_volt, setpoint_volt=y):
                pass
            else:
                self.__mysql_conn.mysql_ins_result('неисправен', '3')
            self.__ctrl_kl.ctrl_ai_code_v1(106)
            sleep(3)
            in_a1, in_a5 = self.__inputs_a()
            self.__reset.stop_procedure_3()
            if in_a1 is False and in_a5 is False:
                if self.__subtest_33():
                    self.__mysql_conn.mysql_ins_result('исправен', f'{self.list_num_yach_test_3[x]}')
                else:
                    self.__mysql_conn.mysql_ins_result('неисправен', f'{self.list_num_yach_test_3[x]}')
                    return False
            elif in_a1 is True:
                if self.__subtest_32(y):
                    self.__mysql_conn.mysql_ins_result('исправен', f'{self.list_num_yach_test_3[x]}')
                else:
                    self.__mysql_conn.mysql_ins_result('неисправен', '3')
                    self.__mysql_conn.mysql_error(419)
                    self.__mysql_conn.mysql_ins_result('неисправен', f'{self.list_num_yach_test_3[x]}')
                    return False
            elif in_a5 is True:
                if self.__subtest_32(y):
                    self.__mysql_conn.mysql_ins_result('исправен', f'{self.list_num_yach_test_3[x]}')
                else:
                    self.__mysql_conn.mysql_ins_result('неисправен', '3')
                    self.__mysql_conn.mysql_error(420)
                    self.__mysql_conn.mysql_ins_result('неисправен', f'{self.list_num_yach_test_3[x]}')
                    return False
            x += 1
        self.__mysql_conn.mysql_ins_result('исправен', '8')
        return True

    def __subtest_22(self, i) -> bool:
        """
        2.2. Формирование нагрузочного сигнала 1,1*calc_volt[i]:
        :param i:
        :return:
        """
        self.__reset.sbros_zashit_kl1()
        in_a1, in_a5 = self.__inputs_a()
        if in_a1 is True and in_a5 is True:
            pass
        elif in_a1 is False:
            self.__mysql_conn.mysql_ins_result('неисправен', '2')
            self.__mysql_conn.mysql_error(417)
            return False
        elif in_a5 is False:
            self.__mysql_conn.mysql_ins_result('неисправен', '2')
            self.__mysql_conn.mysql_error(418)
            return False
        if self.__proc.procedure_1_25_35(coef_volt=self.coef_volt, setpoint_volt=i):
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '2')
        # 2.2.2.  Проверка срабатывания блока от сигнала нагрузки:
        self.__ctrl_kl.ctrl_ai_code_v1(107)
        sleep(3)
        in_a1, in_a5 = self.__inputs_a()
        self.__reset.stop_procedure_3()
        if in_a1 is False and in_a5 is False:
            if self.__subtest_23():
                return True
            else:
                return False
        elif in_a1 is True:
            self.__mysql_conn.mysql_ins_result('неисправен', '2')
            self.__mysql_conn.mysql_error(415)
            if self.__subtest_23():
                return True
            else:
                return False
        elif in_a5 is True:
            self.__mysql_conn.mysql_ins_result('неисправен', '2')
            self.__mysql_conn.mysql_error(416)
            if self.__subtest_23():
                return True
            else:
                return False

    def __subtest_23(self) -> bool:
        """
        2.3. Сброс защит после проверки
        :return:
        """
        self.__reset.sbros_zashit_kl1()
        in_a1, in_a5 = self.__inputs_a()
        if in_a1 is True and in_a5 is True:
            return True
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '2')
            if in_a1 is False:
                self.__mysql_conn.mysql_error(417)
            elif in_a5 is False:
                self.__mysql_conn.mysql_error(418)
            return False

    def __subtest_32(self, y) -> bool:
        """
        3.2. Формирование нагрузочного сигнала 1,1*calc_volt[i]:
        :param y:
        :return:
        """
        self.__reset.sbros_zashit_kl1()
        in_a1, in_a5 = self.__inputs_a()
        if in_a1 is True and in_a5 is True:
            pass
        elif in_a1 is False:
            self.__mysql_conn.mysql_ins_result('неисправен', '3')
            self.__mysql_conn.mysql_error(417)
            return False
        elif in_a5 is False:
            self.__mysql_conn.mysql_ins_result('неисправен', '3')
            self.__mysql_conn.mysql_error(418)
            return False
        if self.__proc.procedure_1_25_35(coef_volt=self.coef_volt, setpoint_volt=y):
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '3')
            return False
        # 2.2.2.  Проверка срабатывания блока от сигнала нагрузки:
        self.__ctrl_kl.ctrl_ai_code_v1(107)
        sleep(3)
        in_a1, in_a5 = self.__inputs_a()
        self.__reset.stop_procedure_3()
        if in_a1 is False and in_a5 is False:
            if self.__subtest_33():
                return True
            else:
                return False
        elif in_a1 is True:
            self.__mysql_conn.mysql_ins_result('неисправен', '3')
            self.__mysql_conn.mysql_error(419)
            if self.__subtest_33():
                return True
            else:
                return False
        elif in_a5 is True:
            self.__mysql_conn.mysql_ins_result('неисправен', '3')
            self.__mysql_conn.mysql_error(420)
            if self.__subtest_33():
                return True
            else:
                return False

    def __subtest_33(self) -> bool:
        """
        2.3. Сброс защит после проверки
        :return:
        """
        self.__reset.sbros_zashit_kl1()
        in_a1, in_a5 = self.__inputs_a()
        if in_a1 is True and in_a5 is True:
            return True
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '3')
            if in_a1 is False:
                self.__mysql_conn.mysql_error(417)
            elif in_a5 is False:
                self.__mysql_conn.mysql_error(418)
            return False

    def __inputs_a0(self):
        in_a0 = self.__read_mb.read_discrete(0)
        if in_a0 is None:
            # logging.error(f'нет связи с контроллером')
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_a0

    def __inputs_a(self):
        in_a1 = self.__read_mb.read_discrete(1)
        in_a5 = self.__read_mb.read_discrete(5)
        if in_a1 is None or in_a5 is None:
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_a1, in_a5

    def st_test_mmtz_d(self) -> bool:
        if self.st_test_10():
            if self.st_test_11():
                if self.st_test_12():
                    if self.st_test_13():
                        if self.st_test_14():
                            if self.st_test_20():
                                if self.st_test_30():
                                    return True
        return False

    def full_test_mmtz_d(self):
        try:
            if self.st_test_mmtz_d():
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
        except HardwareException as hwe:
            my_msg(f'{hwe}', 'red')
        finally:
            self.__reset.reset_all()
            sys.exit()


if __name__ == '__main__':
    test_mmtz_d = TestMMTZD()
    test_mmtz_d.full_test_mmtz_d()
    # reset_test_mmtz_d = ResetRelay()
    # mysql_conn_mmtz_d = MySQLConnect()
    # fault = Bug(True)
    # try:
    #     if test_mmtz_d.st_test_mmtz_d():
    #         mysql_conn_mmtz_d.mysql_block_good()
    #         my_msg('Блок исправен', 'green')
    #     else:
    #         mysql_conn_mmtz_d.mysql_block_bad()
    #         my_msg('Блок неисправен', 'red')
    # except OSError:
    #     my_msg("ошибка системы", 'red')
    # except SystemError:
    #     my_msg("внутренняя ошибка", 'red')
    # except ModbusConnectException as mce:
    #     fault.debug_msg(mce, 'red')
    #     my_msg(f'{mce}', 'red')
    # except HardwareException as hwe:
    #     my_msg(f'{hwe}', 'red')
    # finally:
    #     reset_test_mmtz_d.reset_all()
    #     sys.exit()
