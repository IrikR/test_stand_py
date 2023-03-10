# -*- coding: utf-8 -*-
"""
!!! НОВЫЙ НЕ ОБКАТАНЫЙ !!!

Алгоритм проверки

Тип блока: МТЗ-5 вер.2-7/0.4-2
Производитель: Завод Электромашина.

"""

__all__ = ["TestMTZ5V27"]

import logging
from time import sleep, time

from .general_func.database import *
from .general_func.exception import HardwareException
from .general_func.opc_full import ConnectOPC
from .general_func.procedure import *
from .general_func.reset import ResetProtection, ResetRelay
from .general_func.subtest import ProcedureFull, SubtestMTZ5
from .general_func.utils import CLILog
from .gui.msgbox_1 import *
from .gui.msgbox_2 import *


class TestMTZ5V27:

    def __init__(self):
        self.conn_opc = ConnectOPC()
        self.reset_relay = ResetRelay()
        self.reset_protect = ResetProtection()
        self.proc = Procedure()
        self.proc_full = ProcedureFull()
        self.mysql_conn = MySQLConnect()
        self.subtest = SubtestMTZ5()
        self.cli_log = CLILog("debug", __name__)

        self.tuple_ust_tzp_num: tuple[float, ...] = (0.4, 0.7, 1.0, 1.3, 1.6, 1.8, 2.0)
        self.tuple_ust_tzp_volt: tuple[float, ...] = (10.8, 18.8, 26.55, 34.05, 41.4, 46.2, 50.85)
        self.tuple_ust_mtz_num: tuple[float, ...] = (2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7)
        self.tuple_ust_mtz_volt: tuple[float, ...] = (37.6, 46.8, 55.8, 64.8, 73.6, 82.4, 91.0, 99.6, 108, 116.4, 124.6)
        self.ust_mtz: float = 30.0

        self.list_delta_t_mtz: list[str] = []
        self.list_delta_t_tzp: list[str] = []
        self.list_delta_percent_mtz: list[str] = []
        self.list_delta_percent_tzp: list[str] = []
        self.list_mtz_result: list[[str]] = []
        self.list_tzp_result: list[[str]] = []

        self.coef_volt: float = 0.0
        self.calc_delta_t_mtz: float = 0.0
        self.delta_t_mtz: float
        self.in_1: bool
        self.in_5: bool
        self.health_flag: bool = False

        self.msg_1: str = "Убедитесь в отсутствии других блоков в панелях разъемов " \
                          "и вставьте блок в соответствующий разъем панели B"
        self.msg_2: str = "«Переключите тумблер на корпусе блока в положение «Работа» и установите регуляторы уставок " \
                          "в положение 7 (2-7) и в положение 2 (0.4-2)»"
        self.msg_3: str = "Переключите регулятор МТЗ, расположенный на корпусе блока в положение «Проверка»"
        self.msg_4: str = "установите регуляторы уставок в положение 2 (2-7) и в положение 0.4 (0.4-2)»"
        self.msg_5: str = "Переключите тумблер, расположенный на корпусе блока в положение «Работа»"
        self.msg_6: str = "Установите регулятор уставок на блоке в положение \t"
        self.msg_7: str = "Установите регулятор времени перегруза на блоке в положение «21 сек»"
        self.msg_8: str = "Установите регулятор уставок на блоке в положение\t"

        logging.basicConfig(
            filename="C:\\Stend\\project_class\\log\\TestMTZ5_v27.log",
            filemode="w",
            level=logging.DEBUG,
            encoding="utf-8",
            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('WARNING')
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))

    def st_test_00(self) -> bool:
        """
        Тест 0.0
        :return: bool
        """
        self.cli_log.lev_info(f"старт теста {__doc__}", "skyblue")
        if my_msg(self.msg_1):
            if my_msg(self.msg_2):
                return True
        return False

    def st_test_10(self) -> bool:
        self.mysql_conn.mysql_ins_result('идёт тест 1', '1')
        self.conn_opc.ctrl_relay('KL1', True)
        sleep(0.5)
        self.logger.debug("таймаут 0.5 сек")
        self.cli_log.lev_debug("таймаут 0.5 сек", "gray")
        self.conn_opc.ctrl_relay('KL2', True)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.subtest.subtest_xx(test_num=1, subtest_num=1.0, err_code_a=421, err_code_b=422):
            return True
        return False

    def st_test_11(self) -> bool:
        """
        1.1.2. Проверка отсутствия короткого замыкания на входе измерительной части блока:
        1.2. Определение коэффициента Кс отклонения фактического напряжения от номинального
        """
        if self.proc_full.procedure_1_full(test_num=1, subtest_num=1.1, coef_min_volt=0.6):
            self.coef_volt = self.proc_full.procedure_2_full(test_num=1, subtest_num=1.2)
            return True
        return False

    def st_test_20(self) -> bool:
        """
        Тест 2. Проверка работоспособности защиты МТЗ блока в режиме «Проверка»
        :return: bool
        """
        self.mysql_conn.mysql_ins_result('идёт тест 2', '2')
        if my_msg(self.msg_3):
            if my_msg(self.msg_4):
                if self.proc.procedure_x4_to_x5(setpoint_volt=self.ust_mtz, coef_volt=self.coef_volt):
                    return True
        self.mysql_conn.mysql_ins_result("неисправен TV1", "2")
        return False

    def st_test_21(self) -> bool:
        """
        2.2.  Проверка срабатывания блока от сигнала нагрузки:
        :return: bool
        """
        self.logger.debug("2.2.  Проверка срабатывания блока от сигнала нагрузки:")
        self.mysql_conn.mysql_ins_result('идёт тест 2.2', '2')
        self.conn_opc.ctrl_relay('KL63', True)
        sleep(0.5)
        self.logger.debug("таймаут 0.5 сек")
        self.cli_log.lev_debug("таймаут 0.5 сек", "gray")
        self.conn_opc.ctrl_relay('KL63', False)
        sleep(0.2)
        self.logger.debug("таймаут 0.2 сек")
        self.cli_log.lev_debug("таймаут 0.2 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=2, subtest_num=2.1,
                                         err_code=[444, 445],
                                         position_inp=[False, True],
                                         di_xx=['inp_01', 'inp_05']):
            self.reset_relay.stop_procedure_3()
            return True
        self.reset_relay.stop_procedure_3()
        return False

    def st_test_22(self) -> bool:
        """
        2.4.2. Сброс защит после проверки
        :return: bool
        """
        if self.subtest.subtest_xx(test_num=2, subtest_num=2.2, err_code_a=446, err_code_b=447):
            return True
        return False
        # self.mysql_conn.mysql_ins_result('идёт тест 2.4', '2')
        # self.logger.debug("2.4.2. Сброс защит после проверки")
        # self.reset_protect.sbros_zashit_mtz5()
        # if self.conn_opc.subtest_read_di(test_num=2, subtest_num=2.2,
        #                                  err_code=[446, 447],
        #                                  position_inp=[True, False],
        #                                  di_xx=['inp_01', 'inp_05']):
        #     self.logger.debug("положение выходов соответствует")
        #     self.mysql_conn.mysql_ins_result('исправен', '2')
        #     return True
        # self.logger.debug("положение выходов не соответствует")
        # self.mysql_conn.mysql_ins_result('неисправен', '2')
        # return False

    def st_test_30(self) -> bool:
        """
        Тест 3. Проверка срабатывания защиты ПМЗ блока по уставкам
        :return: bool
        """
        if my_msg(self.msg_5):
            pass
        else:
            return False
        self.mysql_conn.mysql_ins_result('идёт тест 3', '3')
        k = 0
        for i in self.tuple_ust_mtz_volt:
            msg_result_mtz = my_msg_2(f'{self.msg_6} {self.tuple_ust_mtz_num[k]}')
            if msg_result_mtz == 0:
                pass
            elif msg_result_mtz == 1:
                return False
            elif msg_result_mtz == 2:
                self.mysql_conn.mysql_add_message(f'уставка {self.tuple_ust_mtz_num[k]} пропущена')
                self.list_delta_percent_mtz.append('пропущена')
                self.list_delta_t_mtz.append('пропущена')
                k += 1
                continue

            # if self.proc.procedure_x4_to_x5(setpoint_volt=i, coef_volt=self.coef_volt):
            #     pass
            # else:
            #     self.mysql_conn.mysql_ins_result("неисправен TV1", "3")
            #     return False
            self.proc.procedure_1_24_34(coef_volt=self.coef_volt, setpoint_volt=i, factor=1.1)
            calc_delta_t_mtz, inp_01, inp_02, inp_05, inp_06 = self.subtest.subtest_time_calc_mtz()

            # 3.1.  Проверка срабатывания блока от сигнала нагрузки:
            self.logger.debug("3.1.  Проверка срабатывания блока от сигнала нагрузки:")
            self.mysql_conn.mysql_ins_result(f'уставка {self.tuple_ust_mtz_num[k]}', '3')

            # Δ%= 0.0029*(U4)2+5.192*U4
            meas_volt = self.conn_opc.read_ai('AI0')
            calc_delta_percent_mtz = 0.0029 * meas_volt ** 2 + 5.192 * meas_volt
            self.logger.debug(f'дельта %:\t{calc_delta_percent_mtz:.2f}')
            self.list_delta_percent_mtz.append(f'{calc_delta_percent_mtz:.2f}')

            self.logger.debug(f"время срабатывания: {calc_delta_t_mtz}мс: {inp_01 = } (False), {inp_05 = } (True)")
            self.reset_relay.stop_procedure_3()
            if calc_delta_percent_mtz != 9999 and inp_01 is False and inp_05 is True:
                self.logger.debug(f'дельта t\t{calc_delta_t_mtz}')
                self.list_delta_t_mtz.append(f'{calc_delta_t_mtz:.1f}')
                self.mysql_conn.mysql_add_message(f'уставка {self.tuple_ust_mtz_num[k]}\t'
                                                  f'дельта t: {calc_delta_t_mtz:.1f}\t'
                                                  f'дельта %: {calc_delta_percent_mtz:.2f}')
                if self.subtest.subtest_xx(test_num=3, subtest_num=3.3, err_code_a=446, err_code_b=447):
                    k += 1
                    continue
                else:
                    self.mysql_conn.mysql_ins_result('неисправен', '3')
                    return False
            else:
                if self.subtest_32(i, k):
                    if self.subtest.subtest_xx(test_num=3, subtest_num=3.3, err_code_a=446, err_code_b=447):
                        k += 1
                        continue
                    else:
                        self.health_flag = True
                        self.mysql_conn.mysql_error(448)
                        self.mysql_conn.mysql_ins_result('неисправен', '3')
                        return False
                else:
                    self.health_flag = True
                    if self.subtest.subtest_xx(test_num=3, subtest_num=3.3, err_code_a=446, err_code_b=447):
                        k += 1
                        continue
                    else:
                        self.mysql_conn.mysql_ins_result('неисправен', '3')
                        return False
        self.mysql_conn.mysql_ins_result('исправен', '3')
        return True

    def st_test_40(self) -> bool:
        """
        Тест 4. Проверка срабатывания защиты от перегрузки блока по уставкам
        :return: bool
        """
        if my_msg(self.msg_7):
            pass
        else:
            return False
        self.mysql_conn.mysql_ins_result('идёт тест 4', '4')
        m = 0
        for n in self.tuple_ust_tzp_volt:
            msg_result_tzp = my_msg_2(f'{self.msg_8} {self.tuple_ust_tzp_num[m]}')
            if msg_result_tzp == 0:
                pass
            elif msg_result_tzp == 1:
                return False
            elif msg_result_tzp == 2:
                self.mysql_conn.mysql_add_message(f'уставка {self.tuple_ust_tzp_num[m]} пропущена')
                self.list_delta_percent_tzp.append('пропущена')
                self.list_delta_t_tzp.append('пропущена')
                m += 1
                continue
            self.mysql_conn.mysql_ins_result(f'уставка {self.tuple_ust_tzp_num[m]}', '4')
            if self.proc.procedure_x4_to_x5(setpoint_volt=n, coef_volt=self.coef_volt):
                pass
            else:
                self.mysql_conn.mysql_ins_result("неисправен TV1", "4")
                return False
            # Δ%= 0.0132*U42[i]+5.4183* U4[i]
            meas_volt = self.conn_opc.read_ai('AI0')
            calc_delta_percent_tzp = 0.0132 * meas_volt ** 2 + 5.4183 * meas_volt
            self.logger.debug(f'дельта %:\t{calc_delta_percent_tzp:.2f}')
            self.list_delta_percent_tzp.append(f'{calc_delta_percent_tzp:.2f}')
            # 4.4.  Проверка срабатывания блока от сигнала нагрузки:
            self.conn_opc.ctrl_relay('KL63', True)
            self.mysql_conn.progress_level(0.0)

            r = 0
            inp_09, *_ = self.conn_opc.simplified_read_di(["inp_09"])
            while inp_09 is False and r <= 5:
                inp_09, *_ = self.conn_opc.simplified_read_di(["inp_09"])
                r += 1
            if inp_09 is False:
                raise HardwareException("Неисправность в стенде, контроль состояния вторичного главного контакта KL63")

            start_timer_tzp = time()
            delta_t_tzp = 0
            inp_05, *_ = self.conn_opc.simplified_read_di(["inp_05"])
            while inp_05 is False and delta_t_tzp <= 21:
                delta_t_tzp = time() - start_timer_tzp
                self.mysql_conn.progress_level(delta_t_tzp)
                inp_05, *_ = self.conn_opc.simplified_read_di(["inp_05"])
            stop_timer_tzp = time()
            self.conn_opc.ctrl_relay('KL63', False)
            calc_delta_t_tzp = stop_timer_tzp - start_timer_tzp
            self.mysql_conn.progress_level(0.0)
            self.logger.debug(f'тест 3 delta t: {calc_delta_t_tzp:.1f}')
            self.list_delta_t_tzp.append(f'{calc_delta_t_tzp:.1f}')
            self.mysql_conn.mysql_add_message(f'уставка {self.tuple_ust_tzp_num[m]} '
                                              f'дельта t: {calc_delta_t_tzp:.1f}')
            self.mysql_conn.mysql_add_message(f'уставка {self.tuple_ust_tzp_num[m]} '
                                              f'дельта %: {calc_delta_percent_tzp:.2f}')
            self.reset_relay.stop_procedure_3()
            inp_01, inp_05 = self.conn_opc.simplified_read_di(["inp_01", "inp_05"])
            if inp_01 is False and inp_05 is True and calc_delta_t_tzp <= 21:
                self.logger.debug("положение выходов соответствует")
                if self.subtest.subtest_xx(test_num=4, subtest_num=4.6, err_code_a=449, err_code_b=450):
                    m += 1
                    continue
                else:
                    return False
            else:
                self.logger.debug("положение выходов не соответствует")
                self.mysql_conn.mysql_error(448)
                if self.subtest.subtest_xx(test_num=4, subtest_num=4.6, err_code_a=449, err_code_b=450):
                    m += 1
                    continue
                else:
                    return False
        self.mysql_conn.mysql_ins_result('исправен', '4')
        return True

    def subtest_32(self, i: float, k: int) -> bool:
        """
        3.2. Формирование нагрузочного сигнала 1,15*U3[i]:
        :param i: уставка
        :param k: счетчик цикла
        :return: bool
        """
        if self.subtest.subtest_xx(test_num=3, subtest_num=3.2, err_code_a=446, err_code_b=447):
            pass
        else:
            return False
        if self.proc.procedure_1_24_34(coef_volt=self.coef_volt, setpoint_volt=i, factor=1.15):
            pass
        else:
            self.mysql_conn.mysql_ins_result('неисправен', '3')
            return False
        # 3.2.2.  Проверка срабатывания блока от сигнала нагрузки:
        meas_volt = self.conn_opc.read_ai('AI0')
        calc_delta_percent_mtz = 0.0029 * meas_volt ** 2 + 5.192 * meas_volt
        self.list_delta_percent_mtz[-1] = f'{calc_delta_percent_mtz:.2f}'

        calc_delta_t_mtz, inp_01, inp_02, inp_05, inp_06 = self.subtest.subtest_time_calc_mtz()
        self.logger.debug(f"время срабатывания: {calc_delta_t_mtz}мс: {inp_01 = } (False), {inp_05 = } (True)")
        self.reset_relay.stop_procedure_3()

        for wq in range(2):
            self.calc_delta_t_mtz, inp_01, inp_02, inp_05, inp_06 = self.conn_opc.ctrl_ai_code_v0(110)
            if 500.0 < self.calc_delta_t_mtz <= 9999.9:
                self.reset_protect.sbros_zashit_mtz5()
                sleep(3)
                wq += 1
                continue
            else:
                break
        # inp_01, inp_05 = self.conn_opc.simplified_read_di(['inp_01', 'inp_05'])
        if self.calc_delta_t_mtz < 10.0:
            self.list_delta_t_mtz[-1] = f'< 10'
        elif self.calc_delta_t_mtz > 500.0:
            self.list_delta_t_mtz[-1] = f'> 500'
        else:
            self.list_delta_t_mtz[-1] = f'{self.calc_delta_t_mtz:.1f}'
        self.mysql_conn.mysql_add_message(f'уставка {self.tuple_ust_mtz_num[k]} '
                                          f'дельта t: {self.calc_delta_t_mtz}')
        self.mysql_conn.mysql_add_message(f'уставка {self.tuple_ust_mtz_num[k]} '
                                          f'дельта %: {calc_delta_percent_mtz:.2f}')
        if inp_01 is False and inp_05 is True:
            self.reset_relay.stop_procedure_3()
            return True
        else:
            self.reset_relay.stop_procedure_3()
            self.mysql_conn.mysql_error(448)
            return False

    # def subtest_33(self) -> bool:
    #     """
    #     3.3. Сброс защит после проверки
    #     3.5. Расчет относительной нагрузки сигнала
    #     Δ%= 3.4364*(U4[i])/0.63
    #     :return: bool
    #     """
    #     self.reset_protect.sbros_zashit_mtz5()
    #     if self.conn_opc.subtest_read_di(test_num=3, subtest_num=3.3,
    #                                      err_code=[446, 447],
    #                                      position_inp=[True, False],
    #                                      di_xx=['inp_01', 'inp_05']):
    #         self.logger.debug("подтест 3.3 пройден")
    #         self.cli_log.lev_info("подтест 3.3 пройден", "gray")
    #         return True
    #     self.mysql_conn.mysql_ins_result('неисправен', '3')
    #     self.logger.debug("подтест 3.3 не пройден")
    #     self.cli_log.lev_warning("подтест 3.3 не пройден", "red")
    #     return False

    # def subtest_46(self) -> bool:
    #     """
    #     4.6.1. Сброс защит после проверки
    #     Определение кратности сигнала нагрузки: Δ%= 3.4364*U4[i]/0.63
    #     :return: bool
    #     """
    #     self.reset_protect.sbros_zashit_mtz5()
    #     if self.conn_opc.subtest_read_di(test_num=3, subtest_num=3.3,
    #                                      err_code=[449, 450],
    #                                      position_inp=[True, False],
    #                                      di_xx=['inp_01', 'inp_05']):
    #         self.logger.debug("тест 4.6 положение выходов соответствует")
    #         return True
    #     self.mysql_conn.mysql_ins_result('неисправен', '4')
    #     self.logger.debug("тест 4.6 положение выходов не соответствует")
    #     return False

    # def subtest_time_calc(self) -> [float, bool, bool, bool, bool]:
    #     self.logger.debug("подтест проверки времени срабатывания")
    #     for stc in range(2):
    #         self.logger.debug(f"попытка: {stc}")
    #         self.reset_protect.sbros_zashit_mtz5()
    #         delta_t_mtz, in_1, in_2, in_5, in_6 = self.conn_opc.ctrl_ai_code_v0(110)
    #         # self.in_1, self.in_5 = self.conn_opc.simplified_read_di(['inp_01', 'inp_05'])
    #         self.logger.debug(f"время срабатывания: {delta_t_mtz}, "
    #                           f"{in_1 = } is False, "
    #                           f"{in_5 = } is True")
    #         if delta_t_mtz == 9999:
    #             stc += 1
    #             continue
    #         elif delta_t_mtz != 9999 and in_1 is False and in_5 is True:
    #             break
    #         else:
    #             stc += 1
    #             continue
    #     return delta_t_mtz, in_1, in_2, in_5, in_6

    # def sbros_zashit(self):
    #     """
    #     Сброс защит.
    #     :return:
    #     """
    #     self.conn_opc.ctrl_relay('KL1', False)
    #     sleep(1.5)
    #     self.conn_opc.ctrl_relay('KL1', True)
    #     sleep(2)

    def result_test_mtz(self) -> None:
        """
        Записывает результаты проверки в БД.
        :return:
        """
        for g1 in range(len(self.list_delta_percent_mtz)):
            self.list_mtz_result.append((self.tuple_ust_mtz_num[g1],
                                         self.list_delta_percent_mtz[g1],
                                         self.list_delta_t_mtz[g1]))
        self.mysql_conn.mysql_pmz_result(self.list_mtz_result)
        for g2 in range(len(self.list_delta_percent_tzp)):
            self.list_tzp_result.append((self.tuple_ust_tzp_num[g2],
                                         self.list_delta_percent_tzp[g2],
                                         self.list_delta_t_tzp[g2]))
        self.mysql_conn.mysql_tzp_result(self.list_tzp_result)

    def st_test_mtz_5_v2_7(self) -> [bool, bool]:
        """
            Главная функция которая собирает все остальные
            :type: bool, bool
            :return:  результат теста, флаг исправности
        """
        if self.st_test_00():
            if self.st_test_10():
                if self.st_test_11():
                    if self.st_test_20():
                        if self.st_test_21():
                            if self.st_test_22():
                                if self.st_test_30():
                                    if self.st_test_40():
                                        return True, self.health_flag
        return False, self.health_flag
