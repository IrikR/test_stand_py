# -*- coding: utf-8 -*-
"""
!!! НОВЫЙ НЕ ОБКАТАНЫЙ !!!

Алгоритм проверки

Тип блока: БТЗ-3
Производитель: Нет производителя, ТЭТЗ-Инвест, Строй-энергомаш, Углеприбор.

"""

__all__ = ["TestBTZ3"]

import logging
import sys
from time import sleep, time

from .general_func.database import *
from .general_func.exception import *
from .general_func.opc_full import ConnectOPC
from .general_func.procedure import *
from .general_func.reset import ResetProtection, ResetRelay
from .general_func.subtest import ProcedureFull
from .general_func.utils import CLILog
from .gui.msgbox_1 import *
from .gui.msgbox_2 import *


class TestBTZ3:
    """
    Для сброса защиты блока нужно использовать следующие таймеры:
        Время включения 1.5 сек, время после отключения 3.0 сек
    """

    def __init__(self):
        self.conn_opc = ConnectOPC()
        self.reset = ResetRelay()
        self.reset_protect = ResetProtection()
        self.proc = Procedure()
        self.proc_full = ProcedureFull()
        self.mysql_conn = MySQLConnect()
        self.cli_log = CLILog("debug", __name__)

        self.list_ust_tzp_num = (0.5, 0.6, 0.7, 0.8, 0.9, 1.0)
        self.list_ust_tzp = (23.7, 28.6, 35.56, 37.4, 42.6, 47.3)
        self.list_ust_pmz_num = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
        self.list_ust_pmz = (67.9, 86.4, 100.1, 117.2, 140.7, 146.4, 156.6, 164.2, 175.7, 183.7, 192.1)
        self.ust_prov = 80.0
        self.list_delta_t_tzp = []
        self.list_delta_t_pmz = []
        self.list_delta_percent_tzp = []
        self.list_delta_percent_pmz = []
        self.list_result_tzp = []
        self.list_result_pmz = []

        self.coef_volt: float = 0.0
        self.calc_delta_t_pmz: float = 0.0

        self.health_flag: bool = False

        logging.basicConfig(
            filename="C:\\Stend\\project_class\\log\\TestBTZ3.log",
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
        """
        self.cli_log.lev_info(f"старт теста {__doc__}", "skyblue")
        self.conn_opc.simplified_read_di(['inp_14', 'inp_15'])
        msg_1 = "Переключите оба тумблера на корпусе блока в положение «Работа» и установите " \
                "регуляторы уставок в положение 1 (1-11) и положение 1 (0.5-1)"
        if my_msg(msg_1):
            pass
        else:
            return False
        self.mysql_conn.mysql_ins_result('идёт тест 1', '1')
        self.conn_opc.ctrl_relay('KL21', True)
        if self.reset_protection(test_num=1, subtest_num=1.0, err_code_a=368, err_code_b=369, err_code_c=370,
                                 err_code_d=371):
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
        Тест 2. Проверка работоспособности защиты ПМЗ блока в режиме «Проверка»
        """
        msg_2 = "Переключите тумблер ПМЗ (1-11) на корпусе блока в положение «Проверка»"
        if my_msg(msg_2):
            pass
        else:
            return False
        self.logger.debug("тест 2.0")
        self.mysql_conn.mysql_ins_result('идёт тест 2.0', '2')
        if self.proc.procedure_x4_to_x5(setpoint_volt=self.ust_prov, coef_volt=self.coef_volt):
            pass
        else:
            self.mysql_conn.mysql_ins_result("неисправен TV1", "2")
            return False
        return True

    def st_test_21(self) -> bool:
        """
        # 2.2.  Проверка срабатывания блока от сигнала нагрузки:
        """
        self.logger.debug("тест 2.1")
        self.mysql_conn.mysql_ins_result('идёт тест 2.1', '2')
        self.conn_opc.ctrl_relay('KL63', True)
        sleep(2)
        self.conn_opc.ctrl_relay('KL63', False)
        inp_01, inp_02, inp_05, inp_06 = self.conn_opc.simplified_read_di(['inp_01', 'inp_02', 'inp_05', 'inp_06'])
        if inp_01 is False and inp_05 is True and inp_02 is True and inp_06 is False:
            pass
        else:
            self.logger.debug("тест 2.2 положение выходов не соответствует")
            self.mysql_conn.mysql_ins_result('неисправен', '2')
            if inp_01 is True:
                self.mysql_conn.mysql_error(373)
            elif inp_05 is False:
                self.mysql_conn.mysql_error(374)
            elif inp_02 is False:
                self.mysql_conn.mysql_error(375)
            elif inp_06 is True:
                self.mysql_conn.mysql_error(376)
            return False
        self.logger.debug("тест 2.2 положение выходов соответствует")
        self.reset.stop_procedure_3()
        return True

    def st_test_22(self) -> bool:
        if self.reset_protection(test_num=2, subtest_num=2.2):
            return True
        return False

    def st_test_30(self) -> bool:
        """
        Тест 3. Проверка работоспособности защиты ТЗП блока в режиме «Проверка»
        """
        msg_3 = "Переключите тумблер ПМЗ (1-11) в положение «Работа» " \
                "«Переключите тумблер ТЗП (0.5-1) в положение «Проверка»"
        if my_msg(msg_3):
            pass
        else:
            return False
        self.logger.debug("тест 3.1")
        inp_01, inp_02, inp_05, inp_06 = self.conn_opc.simplified_read_di(['inp_01', 'inp_02', 'inp_05', 'inp_06'])
        if inp_01 is True and inp_05 is False and inp_02 is False and inp_06 is True:
            pass
        else:
            self.logger.debug("тест 3.1 положение выходов не соответствует")
            self.mysql_conn.mysql_ins_result('неисправен', '3')
            if inp_01 is False:
                self.mysql_conn.mysql_error(381)
            elif inp_05 is True:
                self.mysql_conn.mysql_error(382)
            elif inp_02 is True:
                self.mysql_conn.mysql_error(383)
            elif inp_06 is False:
                self.mysql_conn.mysql_error(384)
            return False
        self.logger.debug("тест 3.1 положение выходов соответствует")
        return True

    def st_test_31(self) -> bool:
        """
        3.2. Сброс защит после проверки
        """
        msg_4 = "Переключите тумблер ТЗП (0.5…1) на корпусе блока в положение \"Работа\""
        if my_msg(msg_4):
            pass
        else:
            return False
        self.logger.debug("тест 3.1")
        if self.reset_protection(test_num=3, subtest_num=3.1, err_code_a=385, err_code_b=386, err_code_c=387,
                                 err_code_d=388):
            return True
        return False

    def st_test_40(self) -> bool:
        """
        Тест 4. Проверка срабатывания защиты ПМЗ блока по уставкам
        """
        msg_4_1 = "Установите регулятор уставок ТЗП на блоке в положение 1.0"
        if my_msg(msg_4_1):
            pass
        else:
            return False
        k = 0
        for i in self.list_ust_pmz:
            self.logger.debug(f'тест 4 уставка {self.list_ust_pmz_num[k]}')
            msg_5 = 'Установите регулятор уставок ПМЗ на блоке в положение '
            msg_result_pmz = my_msg_2(f'{msg_5} {self.list_ust_pmz_num[k]}')
            if msg_result_pmz == 0:
                pass
            elif msg_result_pmz == 1:
                return False
            elif msg_result_pmz == 2:
                self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_pmz_num[k]} пропущена')
                self.list_delta_percent_pmz.append('пропущена')
                self.list_delta_t_pmz.append('пропущена')
                k += 1
                continue
            self.mysql_conn.mysql_ins_result(f'уставка {self.list_ust_pmz_num[k]}', "4")
            if self.proc.procedure_x4_to_x5(setpoint_volt=i, coef_volt=self.coef_volt):
                pass
            else:
                self.mysql_conn.mysql_ins_result("неисправен TV1", "4")
                return False
            # 4.1.  Проверка срабатывания блока от сигнала нагрузки:
            meas_volt = self.conn_opc.read_ai('AI0')
            # Δ%= 0.0062*U42+1.992* U4
            calc_delta_percent_pmz = 0.0062 * meas_volt ** 2 + 1.992 * meas_volt
            self.list_delta_percent_pmz.append(f'{calc_delta_percent_pmz:.2f}')
            for qw in range(4):
                self.calc_delta_t_pmz, inp_01, inp_02, \
                    inp_05, inp_06 = self.conn_opc.ctrl_ai_code_v0(103)
                self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_pmz_num[k]} '
                                                  f'дельта t: {self.calc_delta_t_pmz:.1f}')
                if 3000 < self.calc_delta_t_pmz <= 9999:
                    if self.reset_protection(test_num=4, subtest_num=4.1):
                        qw += 1
                        continue
                    else:
                        break
                else:
                    break
            self.logger.info(f'тест 4.1 дельта t: {self.calc_delta_t_pmz:.1f} '
                             f'уставка {self.list_ust_pmz_num[k]}')
            if self.calc_delta_t_pmz < 10:
                self.list_delta_t_pmz.append(f'< 10')
            elif self.calc_delta_t_pmz > 3000:
                self.list_delta_t_pmz.append(f'> 3000')
            else:
                self.list_delta_t_pmz.append(f'{self.calc_delta_t_pmz:.1f}')
            self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_pmz_num[k]} '
                                              f'дельта t: {self.calc_delta_t_pmz:.1f}')
            self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_pmz_num[k]} '
                                              f'дельта %: {calc_delta_percent_pmz:.2f}')
            inp_01, inp_02, inp_05, inp_06 = self.conn_opc.simplified_read_di(['inp_01', 'inp_02', 'inp_05', 'inp_06'])
            if inp_01 is False and inp_05 is True and inp_02 is True and inp_06 is False:
                self.logger.debug("тест 4.1 положение выходов соответствует")
                self.reset.stop_procedure_3()
                if self.reset_protection(test_num=1, subtest_num=1.0):
                    k += 1
                    continue
                else:
                    return False
            else:
                self.logger.debug("тест 4.1 положение выходов не соответствует", 1)
                self.mysql_conn.mysql_ins_result('неисправен', '4')
                self.mysql_conn.mysql_error(389)
                if self.subtest_42(i, k):
                    k += 1
                    continue
                else:
                    return False
        self.mysql_conn.mysql_ins_result('исправен', '4')
        return True

    def st_test_50(self) -> bool:
        """
        Тест 5. Проверка срабатывания защиты ТЗП блока по уставкам
        """
        m = 0
        for n in self.list_ust_tzp:
            msg_7 = 'Установите регулятор уставок на блоке в положение '
            msg_result_tzp = my_msg_2(f'{msg_7} {self.list_ust_tzp_num[m]}')
            if msg_result_tzp == 0:
                pass
            elif msg_result_tzp == 1:
                return False
            elif msg_result_tzp == 2:
                self.mysql_conn.mysql_add_message(f'уставка {self.list_ust_tzp_num[m]} пропущена')
                self.list_delta_percent_tzp.append('пропущена')
                self.list_delta_t_tzp.append('пропущена')
                m += 1
                continue
            self.mysql_conn.mysql_ins_result(f'уставка {self.list_ust_tzp_num[m]}', "5")
            if self.proc.procedure_x4_to_x5(setpoint_volt=n, coef_volt=self.coef_volt):
                pass
            else:
                self.mysql_conn.mysql_ins_result("неисправен TV1", "5")
                return False
            meas_volt = self.conn_opc.read_ai('AI0')
            # Δ%= 0.003*U42[i]+2.404* U4[i]
            calc_delta_percent_tzp = 0.003 * meas_volt ** 2 + 2.404 * meas_volt
            self.list_delta_percent_tzp.append(f'{calc_delta_percent_tzp:.2f}')
            # 5.4.  Проверка срабатывания блока от сигнала нагрузки:
            self.mysql_conn.progress_level(0.0)
            self.conn_opc.ctrl_relay('KL63', True)
            inp_09, *_ = self.conn_opc.simplified_read_di(['inp_09'])
            i1 = 0
            while inp_09 is False and i1 <= 4:
                inp_09, *_ = self.conn_opc.simplified_read_di(['inp_09'])
                i1 += 1
            start_timer_tzp = time()
            calc_delta_t_tzp = 0
            inp_05, *_ = self.conn_opc.simplified_read_di(['inp_05'])
            while inp_05 is True and calc_delta_t_tzp <= 370:
                inp_05, *_ = self.conn_opc.simplified_read_di(['inp_05'])
                stop_timer_tzp = time()
                calc_delta_t_tzp = stop_timer_tzp - start_timer_tzp
                self.mysql_conn.progress_level(calc_delta_t_tzp)
            self.conn_opc.ctrl_relay('KL63', False)
            self.reset.stop_procedure_3()
            self.mysql_conn.progress_level(0.0)
            self.logger.info(f'тест 5 delta t: {calc_delta_t_tzp:.1f} '
                             f'уставка {self.list_ust_tzp_num[m]}')
            self.list_delta_t_tzp.append(f'{calc_delta_t_tzp:.1f}')
            self.mysql_conn.mysql_add_message(f'уставка ТЗП {self.list_ust_tzp_num[m]} '
                                              f'дельта t: {calc_delta_t_tzp:.1f}')
            self.mysql_conn.mysql_add_message(f'уставка ТЗП {self.list_ust_tzp_num[m]} '
                                              f'дельта %: {calc_delta_percent_tzp:.2f}')
            inp_01, inp_02, inp_05, inp_06 = self.conn_opc.simplified_read_di(['inp_01', 'inp_02', 'inp_05', 'inp_06'])
            if inp_01 is False and inp_05 is True and inp_02 is True and inp_06 is False and calc_delta_t_tzp <= 360:
                if self.reset_protection(test_num=5, subtest_num=5.5):
                    m += 1
                    continue
                else:
                    return False
            else:
                if self.reset_protection(test_num=5, subtest_num=5.5):
                    m += 1
                    continue
                else:
                    return False
        self.mysql_conn.mysql_ins_result('исправен', '5')
        return True

    def subtest_42(self, i: float, k: int) -> bool:
        """
        4.2. Формирование нагрузочного сигнала 1,1*U3[i]:
        4.2.1. Сброс защит после проверки
        """
        if self.reset_protection(test_num=4, subtest_num=4.2):
            pass
        else:
            return False

        if self.proc.procedure_1_24_34(setpoint_volt=i, coef_volt=self.coef_volt, factor=1.1):
            pass
        else:
            self.mysql_conn.mysql_ins_result("неисправен TV1", "4")
            return False
        # 4.2.2.  Проверка срабатывания блока от сигнала нагрузки:
        meas_volt = self.conn_opc.read_ai('AI0')
        # Δ%= 0.0062*U42+1.992* U4
        calc_delta_percent_pmz = 0.0062 * meas_volt ** 2 + 1.992 * meas_volt
        self.list_delta_percent_pmz[-1] = f'{calc_delta_percent_pmz:.2f}'
        for wq in range(4):
            self.calc_delta_t_pmz = self.conn_opc.ctrl_ai_code_v0(103)
            if 3000 < self.calc_delta_t_pmz <= 9999:
                if self.reset_protection(test_num=4, subtest_num=4.3):
                    wq += 1
                    continue
            else:
                break
        if self.calc_delta_t_pmz < 10:
            self.list_delta_t_pmz[-1] = f'< 10'
        elif self.calc_delta_t_pmz > 3000:
            self.list_delta_t_pmz[-1] = f'> 3000'
        else:
            self.list_delta_t_pmz[-1] = f'{self.calc_delta_t_pmz:.1f}'
        self.mysql_conn.mysql_add_message(f'уставка ПМЗ {self.list_ust_pmz_num[k]} '
                                          f'дельта t: {self.calc_delta_t_pmz:.1f}')
        self.mysql_conn.mysql_add_message(f'уставка ПМЗ {self.list_ust_pmz_num[k]} '
                                          f'дельта %: {calc_delta_percent_pmz:.2f}')
        inp_01, inp_02, inp_05, inp_06 = self.conn_opc.simplified_read_di(['inp_01', 'inp_02', 'inp_05', 'inp_06'])
        if inp_01 is False and inp_05 is True and inp_02 is True and inp_06 is False:
            if self.reset_protection(test_num=4, subtest_num=4.4):
                pass
            else:
                self.mysql_conn.mysql_ins_result('неисправен', '4')
        else:
            self.mysql_conn.mysql_error(389)
            self.reset.stop_procedure_3()
            # 4.3. Сброс защит после проверки
            if self.reset_protection(test_num=4, subtest_num=4.4):
                pass
            else:
                return False
        return True

    def reset_protection(self, *, test_num: int, subtest_num: float, err_code_a: int = 377, err_code_b: int = 378,
                         err_code_c: int = 379, err_code_d: int = 380) -> bool:
        """
        Модуль сброса защиты блока
        :param test_num: номер теста
        :param subtest_num: номер подтеста
        :param err_code_a: код ошибки при неисправности 1-го выхода блока, по умолчанию 377
        :param err_code_b: код ошибки при неисправности 2-го выхода блока, по умолчанию 378
        :param err_code_c: код ошибки при неисправности 3-го выхода блока, по умолчанию 379
        :param err_code_d: код ошибки при неисправности 4-го выхода блока, по умолчанию 380
        :return: bool
        """
        self.logger.debug(f"сброс защит блока, тест {test_num}, подтест {subtest_num}")
        self.reset_protect.sbros_zashit_kl30(time_on=1.5, time_off=3.0)
        if self.conn_opc.subtest_read_di(test_num=test_num, subtest_num=subtest_num,
                                         err_code=[err_code_a, err_code_b, err_code_c, err_code_d],
                                         position_inp=[False, True, False, True],
                                         di_xx=['inp_01', 'inp_05', 'inp_02', 'inp_06']):
            return True
        return False

    def st_test_btz_3(self) -> [bool, bool]:
        if self.st_test_10():
            if self.st_test_11():
                if self.st_test_20():
                    if self.st_test_21():
                        if self.st_test_22():
                            if self.st_test_30():
                                if self.st_test_31():
                                    if self.st_test_40():
                                        if self.st_test_50():
                                            return True, self.health_flag
        return False, self.health_flag

    def result_test_btz_3(self) -> None:
        """
        Сведение всех результатов измерения, и запись в БД.
        """
        for g1 in range(len(self.list_delta_percent_pmz)):
            self.list_result_pmz.append((self.list_ust_pmz_num[g1],
                                         self.list_delta_percent_pmz[g1],
                                         self.list_delta_t_pmz[g1]))
        self.mysql_conn.mysql_pmz_result(self.list_result_pmz)
        for g2 in range(len(self.list_delta_percent_tzp)):
            self.list_result_tzp.append((self.list_ust_tzp_num[g2],
                                         self.list_delta_percent_tzp[g2],
                                         self.list_delta_t_tzp[g2]))
        self.mysql_conn.mysql_tzp_result(self.list_result_tzp)

    def full_test_btz_3(self) -> None:
        try:
            test, health_flag = self.st_test_btz_3()
            if test and not health_flag:
                self.result_test_btz_3()
                self.mysql_conn.mysql_block_good()
                self.logger.debug('Блок исправен')
                self.cli_log.lev_info('Блок исправен', 'green')
                my_msg('Блок исправен', 'green')
            else:
                self.result_test_btz_3()
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
        finally:
            self.conn_opc.full_relay_off()
            self.conn_opc.opc_close()
            sys.exit()


if __name__ == '__main__':
    test_btz_3 = TestBTZ3()
    test_btz_3.full_test_btz_3()
    # reset_test_btz_3 = ResetRelay()
    # mysql_conn_btz_3 = MySQLConnect()
    # try:
    #     test, health_flag = test_btz_3.st_test_btz_3()
    #     if test and not health_flag:
    #         test_btz_3.result_test_btz_3()
    #         mysql_conn_btz_3.mysql_block_good()
    #         my_msg('Блок исправен', 'green')
    #     else:
    #         test_btz_3.result_test_btz_3()
    #         mysql_conn_btz_3.mysql_block_bad()
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
    #     reset_test_btz_3.reset_all()
    #     sys.exit()
