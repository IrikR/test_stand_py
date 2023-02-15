#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Общие модули для алгоритмов
"""

import logging
from time import sleep

from .database import *
from .exception import HardwareException
from .opc_full import ConnectOPC
from .procedure import *
from .reset import ResetProtection
from .reset import ResetRelay
from .resistance import Resistor
from .rw_result import RWError
from .utils import CLILog

__all__ = ["SubtestMTZ5", "ProcedureFull", "SubtestBDU", "Subtest2in", "SubtestBDU1M", "Subtest4in"]


class SubtestMTZ5:
    """
        Методы используемые в алгоритмах проверки МТЗ-5-2.7, МТЗ-5-2.8, МТЗ-5-4.11
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))
        self.reset_relay = ResetRelay()
        self.reset_protect = ResetProtection()
        self.conn_opc = ConnectOPC()
        self.cli_log = CLILog("info", __name__)
        self.mysql_conn = MySQLConnect()

        self.delta_t_mtz: [float, int] = 0
        self.in_1: bool = False
        self.in_2: bool = False
        self.in_5: bool = False
        self.in_6: bool = False

    def subtest_xx(self, *, test_num: int, subtest_num: float, err_code_a: int, err_code_b: int) -> bool:
        """
        3.3. Сброс защит после проверки
        3.5. Расчет относительной нагрузки сигнала
        Δ%= 3.4364*(U4[i])/0.63

        4.6.1. Сброс защит после проверки
        Определение кратности сигнала нагрузки: Δ%= 3.4364*U4[i]/0.63

        :param test_num: int номер теста
        :param subtest_num: float номер подтеста
        :param err_code_a: int код ошибки для 3.3 446, для 4.6 449
        :param err_code_b: int код ошибки для 3.3 447, для 4.6 450
        :return: bool
        """
        self.reset_protect.sbros_zashit_mtz5()
        if self.conn_opc.subtest_read_di(test_num=test_num, subtest_num=subtest_num,
                                         err_code=[err_code_a, err_code_b],
                                         position_inp=[True, False],
                                         di_xx=['inp_01', 'inp_05']):
            self.logger.debug(f"подтест {subtest_num} пройден")
            self.cli_log.lev_info(f"подтест {subtest_num} пройден", "gray")
            return True
        self.mysql_conn.mysql_ins_result('неисправен', f'{test_num}')
        self.logger.debug(f"подтест {subtest_num} не пройден")
        self.cli_log.lev_warning(f"подтест {subtest_num} не пройден", "red")
        return False

    def subtest_time_calc_mtz(self) -> [float, bool, bool, bool, bool]:
        self.logger.debug("подтест проверки времени срабатывания")
        self.cli_log.lev_info("подтест проверки времени срабатывания", "gray")
        for i in range(3):
            self.logger.debug(f"попытка: {i}")
            self.cli_log.lev_debug(f"попытка: {i}", "gray")
            self.reset_protect.sbros_zashit_mtz5()
            self.delta_t_mtz, self.in_1, self.in_2, self.in_5, self.in_6 = self.conn_opc.ctrl_ai_code_v0(110)
            # self.in_1, self.in_5 = self.conn_opc.simplified_read_di(['inp_01', 'inp_05'])
            result = f"время срабатывания: {self.delta_t_mtz}, {self.in_1 = } is False, {self.in_5 = } is True"
            self.logger.debug(result)
            self.cli_log.lev_info(result, "skyblue")
            if self.delta_t_mtz == 9999:
                i += 1
                continue
            elif self.delta_t_mtz != 9999 and self.in_1 is False and self.in_5 is True:
                break
            else:
                i += 1
                continue
        return self.delta_t_mtz, self.in_1, self.in_2, self.in_5, self.in_6


class ProcedureFull:

    def __init__(self):
        self.proc = Procedure()
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))
        self.reset_relay = ResetRelay()
        self.mysql_conn = MySQLConnect()
        self.rw_error = RWError()
        self.conn_opc = ConnectOPC()
        self.cli_log = CLILog("info", __name__)

    def procedure_1_full(self, *, test_num: int = 1, subtest_num: float = 1.0, coef_min_volt: float = 0.6,
                         coef_max_volt: float = 1.1) -> bool:
        """
        1.1. Проверка вероятности наличия короткого замыкания на входе измерительной цепи блока.
        :return: Bool
        """
        self.logger.debug("СТАРТ процедуры 1, 2.1, 3.1 - проверка на КЗ")
        self.cli_log.lev_info("СТАРТ процедуры 1, 2.1, 3.1 - проверка на КЗ", "purple")
        self.mysql_conn.mysql_ins_result(f'идёт тест {subtest_num}', f'{test_num}')
        min_volt, max_volt = self.proc.procedure_1_21_31_v1(coef_min=coef_min_volt, coef_max=coef_max_volt)
        self.conn_opc.ctrl_relay('KL63', True)
        self.logger.debug("включение KL63")
        self.cli_log.lev_info("включение KL63", "blue")
        sleep(2)
        meas_volt = self.conn_opc.read_ai('AI0')
        self.logger.debug(f'напряжение после включения KL63:\t{meas_volt:.2f}\tдолжно быть '
                          f'от\t{min_volt:.2f}\tдо\t{max_volt:.2f}')
        self.cli_log.lev_info(f'напряжение после включения KL63:\t{meas_volt:.2f}\tдолжно быть '
                              f'от\t{min_volt:.2f}\tдо\t{max_volt:.2f}', "orange")
        self.reset_relay.sbros_kl63_proc_1_21_31()
        if min_volt <= meas_volt <= max_volt:
            self.mysql_conn.mysql_add_message(f'тест {subtest_num} пройден')
            self.logger.debug("напряжение соответствует")
            self.cli_log.lev_info("напряжение соответствует", "green")
            return True
        self.logger.debug("напряжение не соответствует")
        self.cli_log.lev_warning("напряжение не соответствует", "red")
        self.mysql_conn.mysql_add_message(f'тест {subtest_num} не пройден')
        self.mysql_conn.mysql_ins_result('неисправен', f'{test_num}')
        self.rw_error.rw_err(455)
        return False

    def procedure_2_full(self, *, test_num: int = 1, subtest_num: float = 1.0) -> float:
        """
        1.2. Определение коэффициента Кс отклонения фактического напряжения от номинального
        """
        self.logger.debug("Определение коэффициента Кс отклонения фактического напряжения от номинального")
        self.cli_log.lev_info("Определение коэффициента Кс отклонения фактического напряжения от номинального", "gray")
        self.mysql_conn.mysql_ins_result(f'идет тест {subtest_num}', f'{test_num}')
        coef_volt = self.proc.procedure_1_22_32()
        self.mysql_conn.mysql_add_message(f"Определение коэффициента Кс: {coef_volt}")
        self.reset_relay.stop_procedure_32()
        if coef_volt != 0.0:
            self.mysql_conn.mysql_ins_result('исправен', f'{test_num}')
            return coef_volt
        self.mysql_conn.mysql_ins_result('неисправен', f'{test_num}')
        raise HardwareException("Выходное напряжение не соответствует заданию.\n"
                                "Неисправность узла формирования напряжения в стенде")


class SubtestBDU:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))
        self.reset_relay = ResetRelay()
        self.reset_protect = ResetProtection()
        self.conn_opc = ConnectOPC()
        self.resist = Resistor()
        self.mysql_conn = MySQLConnect()
        self.cli_log = CLILog("info", __name__)

    def subtest_a_bdu43_bru2s(self, *, test_num: int, subtest_num: float) -> bool:
        """
        2.2. Включение блока от кнопки «Пуск»
        подтест проверки блока БДУ-4-3
        подтест проверки блока БРУ-2С
        :param subtest_num: float
        :param test_num: int
        :return: bool
        """
        err_list = [21]
        position_list = [True]
        inp_xx_list = ["inp_01"]
        self.logger.debug(f"старт теста: {test_num}, подтест: {subtest_num}")
        self.cli_log.lev_info(f"старт теста: {test_num}, подтест: {subtest_num}", "gray")
        self.mysql_conn.mysql_add_message(f"старт теста: {test_num}, подтест: {subtest_num}")
        self.mysql_conn.mysql_ins_result(f"идёт тест {subtest_num}", f'{test_num}')
        self.resist.resist_ohm(0)
        self.conn_opc.ctrl_relay('KL12', True)
        self.logger.debug("включение KL12")
        self.cli_log.lev_info("включение KL12", "blue")
        sleep(1)
        if self.conn_opc.subtest_read_di(test_num=test_num, subtest_num=subtest_num, err_code=err_list,
                                         position_inp=position_list,
                                         di_xx=inp_xx_list):
            return True
        return False

    def subtest_b_bdu43_d(self, *, test_num: int, subtest_num: float) -> bool:
        """
            2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
            подтест проверки блока БДУ-4-3
            подтест проверки блока БДУ-Д
            :param test_num: int
            :param subtest_num: float
            :return bool:
        """
        err_list = [22]
        position_list = [True]
        inp_xx_list = ["inp_01"]
        self.logger.debug(f"старт теста: {test_num}, подтест: {subtest_num}")
        self.cli_log.lev_info(f"старт теста: {test_num}, подтест: {subtest_num}", "gray")
        self.mysql_conn.mysql_add_message(f"старт теста: {test_num}, подтест: {subtest_num}")
        self.mysql_conn.mysql_ins_result(f"идёт тест {subtest_num}", f'{test_num}')
        self.conn_opc.ctrl_relay('KL1', True)
        self.conn_opc.ctrl_relay('KL25', True)
        self.logger.debug('включение KL1, KL25')
        self.cli_log.lev_info('включение KL1, KL25', "blue")
        sleep(1)
        if self.conn_opc.subtest_read_di(test_num=test_num, subtest_num=subtest_num, err_code=err_list,
                                         position_inp=position_list,
                                         di_xx=inp_xx_list):
            return True
        return False

    def subtest_a_bdud(self, *, test_num: int, subtest_num: float) -> bool:
        """
        2.2. Включение блока от кнопки «Пуск»
        подтест проверки блока БДУ-Д
        :param test_num: int
        :param subtest_num: float
        :return bool:
        """
        err_list = [21]
        position_list = [True]
        inp_xx_list = ["inp_01"]
        self.logger.debug(f"старт теста: {test_num}, подтест: {subtest_num}")
        self.cli_log.lev_info(f"старт теста: {test_num}, подтест: {subtest_num}", "gray")
        self.mysql_conn.mysql_add_message(f"старт теста: {test_num}, подтест: {subtest_num}")
        self.mysql_conn.mysql_ins_result(f"идёт тест {subtest_num}", f'{test_num}')
        self.resist.resist_ohm(15)
        sleep(3)
        self.conn_opc.ctrl_relay('KL12', True)
        self.logger.debug(f'включение KL12')
        self.cli_log.lev_info('включение KL12', "blue")
        sleep(3)
        if self.conn_opc.subtest_read_di(test_num=test_num, subtest_num=subtest_num, err_code=err_list,
                                         position_inp=position_list,
                                         di_xx=inp_xx_list):
            return True
        return False

    def subtest_a_bdu014tp(self, *, test_num: int, subtest_num: float) -> bool:
        """
        Подтест проверки блока БДУ-0,1,4,Т,П
        :param subtest_num:
        :param test_num:
        :return:
        """
        err_list = [26]
        position_list = [True]
        inp_xx_list = ["inp_01"]

        self.logger.debug(f"старт теста: {test_num}, подтест: {subtest_num}")
        self.cli_log.lev_info(f"старт теста: {test_num}, подтест: {subtest_num}", "gray")
        self.mysql_conn.mysql_add_message(f"старт теста: {test_num}, подтест: {subtest_num}")
        self.mysql_conn.mysql_ins_result(f'идёт тест {subtest_num}', f'{test_num}')
        self.resist.resist_ohm(255)
        sleep(1)
        self.logger.debug("таймаут 1 секунда")
        self.cli_log.lev_debug("таймаут 1 секунда", "gray")
        self.resist.resist_ohm(10)
        sleep(2)
        self.logger.debug("таймаут 2 секунды")
        self.cli_log.lev_debug("таймаут 2 секунды", "gray")
        self.conn_opc.ctrl_relay('KL1', True)
        sleep(1)
        self.logger.debug("таймаут 1 секунда")
        self.cli_log.lev_debug("таймаут 1 секунда", "gray")
        self.conn_opc.ctrl_relay('KL12', True)
        sleep(1)
        if self.conn_opc.subtest_read_di(test_num=test_num, subtest_num=subtest_num, err_code=err_list,
                                         position_inp=position_list,
                                         di_xx=inp_xx_list):
            return True
        return False

    def subtest_b_bru2s(self, *, test_num: int, subtest_num: float) -> bool:
        """
        2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        подтест проверки блока БРУ-2С
        :param subtest_num: float
        :param test_num: int
        :return: bool
        """
        err_list = [50]
        position_list = [True]
        inp_xx_list = ["inp_01"]

        self.logger.debug(f"старт теста: {test_num}, подтест: {subtest_num}")
        self.cli_log.lev_info(f"старт теста: {test_num}, подтест: {subtest_num}", "gray")
        self.mysql_conn.mysql_add_message(f"старт теста: {test_num}, подтест: {subtest_num}")
        self.mysql_conn.mysql_ins_result(f'идёт тест {subtest_num}', f'{test_num}')
        self.conn_opc.ctrl_relay('KL25', True)
        if self.conn_opc.subtest_read_di(test_num=test_num, subtest_num=subtest_num, err_code=err_list,
                                         position_inp=position_list,
                                         di_xx=inp_xx_list):
            return True
        return False

    def subtest_a_bupmvir(self, *, test_num: int, subtest_num: float) -> bool:
        """
        2.1. Включение блока от кнопки «Пуск» при сопротивлении 10 Ом
        подтест проверки БУ-ПМВИР
        """
        err_list = [91]
        position_list = [True]
        inp_xx_list = ["inp_01"]

        self.logger.debug(f"старт теста: {test_num}, подтест: {subtest_num}")
        self.cli_log.lev_info(f"старт теста: {test_num}, подтест: {subtest_num}", "gray")
        self.mysql_conn.mysql_add_message(f"старт теста: {test_num}, подтест: {subtest_num}")
        self.mysql_conn.mysql_ins_result(f'идёт тест {subtest_num}', f'{test_num}')
        self.resist.resist_ohm(10)
        sleep(1)
        self.logger.debug("таймаут 1 секунда")
        self.cli_log.lev_debug("таймаут 1 секунда", "gray")
        self.conn_opc.ctrl_relay('KL12', True)
        sleep(3)
        self.logger.debug("таймаут 3 секунды")
        self.cli_log.lev_debug("таймаут 3 секунды", "gray")
        if self.conn_opc.subtest_read_di(test_num=test_num, subtest_num=subtest_num, err_code=err_list,
                                         position_inp=position_list,
                                         di_xx=inp_xx_list):
            return True
        return False


class Subtest2in:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))
        self.conn_opc = ConnectOPC()
        self.resist = Resistor()
        self.mysql_conn = MySQLConnect()
        self.rw_error = RWError()
        self.cli_log = CLILog("info", __name__)

    def subtest_a_bdu(self, *, test_num: int, subtest_num: float, err_code_a: int, err_code_b: int,
                      position_a: bool, position_b: bool, resist: int = 10, timeout: int = 2) -> bool:
        """
        Общий метод для блока БДУ-4-2, БДУ-Д4-2, БДУ-Д.01, БДУ-Р, БДУ-Т, БРУ-2СР, БУ-АПШ.М

        для БДУ-4-2, БДУ-Д4-2, БДУ-Д-0.1 (bdu_4_2)
            err_code : 15 и 16
            resist : 10 Ом
            position : True & True
        для БДУ-Р, БДУ-Т (bdu_r_t)
            err_code : 292 и 293
            position : True & False
            resist : 10 Ом
        для БРУ-2СР (bru_2sr)
            err_code : 61 & 62 - в прямом: 73 & 74 - в обратном
            position : True & False - в прямом: False & True - обратном
            resist : 0
        для БУ-АПШ.М (bu_apsh_m):
            err_code: в прямом 103 & 104, в обратном 113 & 114
            position: в прямом True & False, в обратном False & True
            resist: 10
            timeout: 3

        2.2. Включение блока от кнопки «Пуск»
        :param test_num:
        :param subtest_num:
        :param err_code_a:
        :param err_code_b:
        :param position_a:
        :param position_b:
        :param resist:
        :param timeout:
        :return: Bool
        """
        err_list = [err_code_a, err_code_b]
        position_list = [position_a, position_b]
        inp_xx_list = ["inp_01", "inp_02"]

        self.logger.debug(f"Общий метод, тест: {test_num}, подтест: {subtest_num}")
        self.cli_log.lev_info(f"Общий метод, тест: {test_num}, подтест: {subtest_num}", "gray")
        self.mysql_conn.mysql_ins_result(f'идёт тест {subtest_num}', f'{test_num}')
        self.mysql_conn.mysql_add_message(f"старт теста: {test_num}, подтест: {subtest_num}")
        self.resist.resist_ohm(255)
        self.resist.resist_ohm(resist)
        sleep(timeout)
        self.logger.debug(f"таймаут {timeout} сек")
        self.cli_log.lev_info(f"таймаут {timeout} сек", "gray")
        self.conn_opc.ctrl_relay('KL12', True)
        sleep(timeout)
        self.logger.debug(f"таймаут {timeout} сек")
        self.cli_log.lev_debug(f"таймаут {timeout} сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=test_num, subtest_num=subtest_num, err_code=err_list,
                                         position_inp=position_list,
                                         di_xx=inp_xx_list):
            return True
        return False

    def subtest_b_bdu(self, *, test_num: int, subtest_num: float, err_code_a: int, err_code_b: int,
                      position_a: bool, position_b: bool, kl1: bool = True) -> bool:
        """
        Общий метод для блока БДУ-4-2, БДУ-Д4-2, БДУ-Д.01, БДУ-Р, БДУ-Т, БРУ-2СР

        для БДУ-4-2, БДУ-Д4-2, БДУ-Д-0.1 (bdu_4_2)
            err_code : 7 и 8
            position : True & True
        для БДУ-Р, БДУ-Т (bdu_r_t)
            err_code : 294 и 295
            position : True & False
        для БРУ-2СР (bru_2sr)
            err_sode : 63 & 64 - в прямом : 75 и 76 - в обратном
            position : True & False - в прямом : False & True - в обратном
            KL1 : не используется, необходимо передать False

        2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:

        :param test_num:
        :param subtest_num:
        :param err_code_a:
        :param err_code_b:
        :param position_a:
        :param position_b:
        :param kl1:
        :return:
        """
        err_list = [err_code_a, err_code_b]
        position_list = [position_a, position_b]
        inp_xx_list = ["inp_01", "inp_02"]

        self.logger.debug(f"Общий метод, тест: {test_num}, подтест: {subtest_num}")
        self.cli_log.lev_info(f"Общий метод, тест: {test_num}, подтест: {subtest_num}", "gray")
        self.mysql_conn.mysql_ins_result(f'идёт тест {subtest_num}', f'{test_num}')
        self.mysql_conn.mysql_add_message(f"старт теста: {test_num}, подтест: {subtest_num}")
        if kl1 is False:
            pass
        else:
            self.conn_opc.ctrl_relay('KL1', True)
        self.conn_opc.ctrl_relay('KL25', True)
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=test_num, subtest_num=subtest_num, err_code=err_list,
                                         position_inp=position_list,
                                         di_xx=inp_xx_list):
            return True
        return False

    def subtest_a_bur(self, *, test_num: int, subtest_num: float, forward: bool = False, back: bool = False) -> bool:
        """
        Подтест алгоритма проверки блока БУР-ПМВИР
        forward = True - проверка вперед
        back = True - проверка назад
        2.2. Включение блока от кнопки «Пуск» режима «Вперёд»
        6.2. Включение блока от кнопки «Пуск» режима «Назад»
        """
        err_code_1 = 1
        err_code_2 = 1
        pos_a1 = False
        pos_a2 = False
        if forward is True:
            err_code_1 = 170
            err_code_2 = 171
            pos_a1 = True
            pos_a2 = False
        elif back is True:
            err_code_1 = 182
            err_code_2 = 183
            pos_a1 = False
            pos_a2 = True
        self.resist.resist_ohm(0)
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        self.conn_opc.ctrl_relay('KL12', True)
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")

        if self.conn_opc.subtest_read_di(test_num=test_num, subtest_num=subtest_num,
                                         err_code=[err_code_1, err_code_2],
                                         position_inp=[pos_a1, pos_a2],
                                         di_xx=['inp_01', 'inp_02']):
            return True
        return False

    def subtest_b_bur(self, *, test_num: int, subtest_num: float, forward: bool = False, back: bool = False) -> bool:
        """
        Подтест алгоритма проверки блока БУР-ПМВИР
        forward = True - проверка вперед
        back = True - проверка назад
        2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления режима «Вперёд»:
        6.3. Проверка удержания блока во включенном состоянии
        при подключении Rш пульта управления режима «Назад»:
        """
        err_code_1 = 1
        err_code_2 = 1
        pos_a1 = False
        pos_a2 = False
        if forward is True:
            err_code_1 = 172
            err_code_2 = 173
            pos_a1 = True
            pos_a2 = False
        elif back is True:
            err_code_1 = 184
            err_code_2 = 185
            pos_a1 = False
            pos_a2 = True
        self.conn_opc.ctrl_relay('KL25', True)
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=test_num, subtest_num=subtest_num,
                                         err_code=[err_code_1, err_code_2],
                                         position_inp=[pos_a1, pos_a2],
                                         di_xx=['inp_01', 'inp_02']):
            return True
        return False

    def subtest_bru2sr(self, *, test_num: int, subtest_num: float, err_code_a: int = 85, err_code_b: int = 86,
                       resist: int = 200) -> bool:
        """
        Общий подтест для алгоритма БРУ-2СР (bru_2sr)
        Тест 10. Блокировка включения блока при снижении сопротивления изоляции
        контролируемого присоединения до уровня предупредительной уставки
            resist = 200
            err_code = 85 & 86
        Тест 11. Блокировка включения блока при снижении сопротивления
        изоляции контролируемого присоединения до уровня аварийной уставки
            resist = 30
            err_code = 87 & 88
        :param test_num:
        :param subtest_num:
        :param err_code_a:
        :param err_code_b:
        :param resist:
        :return:
        """

        self.logger.debug("старт подтеста 10 и 11")
        self.cli_log.lev_info("старт подтеста 10 и 11", "gray")
        self.mysql_conn.mysql_add_message(f"тест: {test_num}, подтест: {subtest_num}")
        self.mysql_conn.mysql_ins_result(f"идет тест {subtest_num}", f"{test_num}")
        self.resist.resist_kohm(resist)
        self.conn_opc.ctrl_relay('KL12', True)
        in_a1, in_a2 = self.conn_opc.simplified_read_di(['inp_01', 'inp_02'])
        self.logger.debug(f'положение выходов блока: {in_a1 = } is False, {in_a2 = } is False')
        self.cli_log.lev_info(f'положение выходов блока: {in_a1 = } is False, {in_a2 = } is False', "skyblue")
        if in_a1 is False and in_a2 is False:
            self.conn_opc.ctrl_relay('KL12', False)
            self.mysql_conn.mysql_ins_result("исправен", f"{test_num}")
            self.mysql_conn.mysql_add_message(f"Исправен. тест: {test_num}, подтест: {subtest_num}")
            self.logger.debug(f"Исправен. тест: {test_num}, подтест: {subtest_num}")
            self.cli_log.lev_info(f"Исправен. тест: {test_num}, подтест: {subtest_num}", "green")
            return True
        else:
            self.mysql_conn.mysql_ins_result("неисправен", f"{test_num}")
            self.mysql_conn.mysql_add_message(f"Неисправен. тест: {test_num}, подтест: {subtest_num}")
            self.logger.debug(f"Неисправен. тест: {test_num}, подтест: {subtest_num}")
            self.cli_log.lev_warning(f"Неисправен. тест: {test_num}, подтест: {subtest_num}", "red")
            if in_a1 is True:
                self.rw_error.rw_err(err_code_a)
            elif in_a2 is True:
                self.rw_error.rw_err(err_code_b)
            return False


class SubtestBDU1M:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))
        self.conn_opc = ConnectOPC()
        self.resist = Resistor()
        self.mysql_conn = MySQLConnect()
        self.cli_log = CLILog("info", __name__)

    def subtest_a(self, *, test_num: int, subtest_num: float) -> bool:
        """
            2.2. Включение блока от кнопки «Пуск»
        """
        self.mysql_conn.mysql_ins_result(f'идёт тест {subtest_num}', f'{test_num}')
        self.logger.debug(f"старт теста {test_num}, подтест {subtest_num}")
        self.cli_log.lev_info(f"старт теста {test_num}, подтест {subtest_num}", "gray")
        self.conn_opc.ctrl_relay('KL22', True)
        self.conn_opc.ctrl_relay('KL1', False)
        self.conn_opc.ctrl_relay('KL25', False)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        self.resist.resist_ohm(10)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        self.conn_opc.ctrl_relay('KL12', True)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=test_num, subtest_num=subtest_num, err_code=[203],
                                         position_inp=[True],
                                         di_xx=['inp_02']):
            return True
        return False

    def subtest_b(self, *, test_num: int, subtest_num: float) -> bool:
        """
            2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        """
        self.mysql_conn.mysql_ins_result(f'идёт тест {subtest_num}', f'{test_num}')
        self.logger.debug(f"старт теста {test_num}, подтест {subtest_num}")
        self.cli_log.lev_info(f"старт теста {test_num}, подтест {subtest_num}", "gray")
        self.conn_opc.ctrl_relay('KL1', True)
        self.conn_opc.ctrl_relay('KL22', False)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        self.conn_opc.ctrl_relay('KL25', True)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=test_num, subtest_num=subtest_num, err_code=[205],
                                         position_inp=[True],
                                         di_xx=['inp_02']):
            return True
        return False


class Subtest4in:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))
        self.conn_opc = ConnectOPC()
        self.resist = Resistor()
        self.mysql_conn = MySQLConnect()
        self.rw_error = RWError()
        self.cli_log = CLILog("info", __name__)

    def subtest_a(self, *, test_num: int = 1, subtest_num: float = 1.0, resistance: int = 10,
                  err_code_a: int = 1, err_code_b: int = 1, err_code_c: int = 1, err_code_d: int = 1,
                  position_a: bool = False, position_b: bool = False,
                  position_c: bool = False, position_d: bool = False,
                  di_a: str = 'in_a0', di_b: str = 'inp_01', di_c: str = 'inp_02', di_d: str = 'inp_03') -> bool:
        """
        Общий подтест для БДУ-ДР.01
        2.2. Включение 1 канала блока от кнопки «Пуск» 1 канала
        # общий подтест для алгоритма БДУ-ДР.01 (bdu_dr01)
            err_code: 1-й канал 224, 225, 226, 227, 2-й канал 252, 253, 254, 255
            position: 1-й канал True & True & False & False, 2-й канал False & False & True & True
        :param resistance: сопротивление
        :param test_num: номер теста
        :param subtest_num: номер подтеста
        :param err_code_a: код ошибки для 1-го выхода
        :param err_code_b: код ошибки для 2-го выхода
        :param err_code_c: код ошибки для 3-го выхода
        :param err_code_d: код ошибки для 4-го выхода
        :param position_a: положение. Которое должен занять 1-й выход блока
        :param position_b: положение. Которое должен занять 2-й выход блока
        :param position_c: положение. Которое должен занять 3-й выход блока
        :param position_d: положение. Которое должен занять 4-й выход блока
        :param di_a: 1-й вход контроллера
        :param di_b: 2-й вход контроллера
        :param di_c: 3-й вход контроллера
        :param di_d: 4-й вход контроллера
        :return:
        """
        self.logger.debug(f"старт теста {test_num}, подтест {subtest_num}")
        self.cli_log.lev_info(f"старт теста {test_num}, подтест {subtest_num}", "gray")
        self.mysql_conn.mysql_ins_result(f'идёт тест {subtest_num}', f'{test_num}')
        self.mysql_conn.mysql_add_message(f"идёт тест: {test_num}, подтест: {subtest_num}")
        self.resist.resist_ohm(255)
        self.resist.resist_ohm(resistance)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        self.conn_opc.ctrl_relay('KL12', True)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=test_num, subtest_num=subtest_num,
                                         err_code=[err_code_a, err_code_b, err_code_c, err_code_d],
                                         position_inp=[position_a, position_b, position_c, position_d],
                                         di_xx=[di_a, di_b, di_c, di_d]):
            return True
        return False

    def subtest_b(self, *, test_num: int = 1, subtest_num: float = 1.0, relay: str = 'KL1',
                  err_code_a: int = 1, err_code_b: int = 1, err_code_c: int = 1, err_code_d: int = 1,
                  position_a: bool = False, position_b: bool = False,
                  position_c: bool = False, position_d: bool = False,
                  di_a: str = 'in_a0', di_b: str = 'inp_01', di_c: str = 'inp_02', di_d: str = 'inp_03') -> bool:
        """
        Общий подтест для БДУ-ДР.01
        2.3. Проверка удержания 1 канала блока во включенном состоянии
        при подключении Rш пульта управления 1 каналом блока:
        6.3. Проверка удержания 2 канала блока во включенном состоянии
        при подключении Rш пульта управления 2 каналом блока:
        # общий подтест для алгоритма БДУ-ДР.01 (bdu_dr01)
            err_code: 1-й канал 228, 229, 230, 231, 2-й канал 256, 257, 258, 259
            position: 1-й канал True & True & False & False, 2-й канал False & False & True & True
            relay:  1-й канал KL1, 2-й канал KL29
        :param relay: номер реле в формате 'KL1'
        :param test_num: номер теста
        :param subtest_num: номер подтеста
        :param err_code_a: код ошибки для 1-го выхода
        :param err_code_b: код ошибки для 2-го выхода
        :param err_code_c: код ошибки для 3-го выхода
        :param err_code_d: код ошибки для 4-го выхода
        :param position_a: положение. Которое должен занять 1-й выход блока
        :param position_b: положение. Которое должен занять 2-й выход блока
        :param position_c: положение. Которое должен занять 3-й выход блока
        :param position_d: положение. Которое должен занять 4-й выход блока
        :param di_a: 1-й вход контроллера
        :param di_b: 2-й вход контроллера
        :param di_c: 3-й вход контроллера
        :param di_d: 4-й вход контроллера
        :return:
        """
        self.logger.debug(f"старт теста {test_num}, подтест {subtest_num}")
        self.cli_log.lev_info(f"старт теста {test_num}, подтест {subtest_num}", "gray")
        self.mysql_conn.mysql_ins_result(f'идёт тест {subtest_num}', f'{test_num}')
        self.mysql_conn.mysql_add_message(f"идёт тест: {test_num}, подтест: {subtest_num}")
        self.conn_opc.ctrl_relay(relay, True)
        self.conn_opc.ctrl_relay('KL25', True)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=test_num, subtest_num=subtest_num,
                                         err_code=[err_code_a, err_code_b, err_code_c, err_code_d],
                                         position_inp=[position_a, position_b, position_c, position_d],
                                         di_xx=[di_a, di_b, di_c, di_d]):
            return True
        return False
