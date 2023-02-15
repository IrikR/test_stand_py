#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from time import sleep

from .exception import *
from .reset import ResetRelay
from .utils import CLILog
from .opc_full import ConnectOPC
from .ctrl_tv1 import PervObmTV1, VtorObmTV1

__all__ = ["Procedure"]


class Procedure:
    """
        U2 - это уставка
        U3 - напряжение вычисленное в процедуре 2х
        напряжение измеренное = measured voltage = measured_vol
        напряжение уставки = setpoint voltage  = setpoint_volt
        коэффициент = coef_volt
        # primary winding
        # secondary winding

        процедура 2.3: U2 =80В.
        процедура 2.6: U2 =85.6В.
        процедура 2.7: U2 =20В.
        процедура 2.8: U3[i]=1,15*U2[i]/Кс
        процедура 2.9: U2 =25.2В.
        процедура 2.10: U2 =8,2В.
        процедура 2.11: U2 =10,7В.
        процедура 2.12: U2 =38В. изменено на 80В

        процедура 3.3: (0,9…1.1)*85.6 = 77,04 до 94,16
        процедура 3.6: (0,9…1.1)*20 = 18 до 22
        процедура 3.7: (0,9…1.1)*80 = 72 до 88
        процедура 3.8: (0,9…1.1)*25.2 = от 22.68 и до 27.72
        процедура 3.9: (0,9…1.1)*8.2 = 7.38 до 9.02
        процедура 3.10: (0,9…1.1)*10.7 = 9.63 до 11.77
        процедура 3.11: (0,85…1.1)* U2[i]
        процедура 3.12: (0,9…1.1)* U2 = 72.0 до 88.0
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.perv_obm = PervObmTV1()
        self.vtor_obm = VtorObmTV1()
        self.reset = ResetRelay()
        self.conn_opc = ConnectOPC()
        self.cli_log = CLILog("info", __name__)

    def start_procedure_1(self) -> bool:
        """
        Процедура 1. сброс реле первичной и вторичной обмотки, проверка отсутствия напряжения на первичной обмотке.
        :return bool:
        """
        self.logger.debug("процедура 1")
        self.cli_log.lev_info("процедура 1", "purple")
        self.conn_opc.vtor_obm_tv1_off()
        self.conn_opc.perv_obm_tv1_off()
        self.conn_opc.ctrl_relay('KL62', True)
        sleep(1)
        self.conn_opc.ctrl_relay('KL37', True)
        sleep(1)
        for i in range(3):
            in_b0, *_ = self.conn_opc.simplified_read_di(['inp_08'])
            self.logger.debug(f"in_b0 = {in_b0} (False)")
            self.cli_log.lev_info(f"in_b0 = {in_b0} (False)", "skyblue")
            if in_b0 is False:
                self.logger.debug(f"попытка: {i}, процедура 1 пройдена")
                self.cli_log.lev_info(f"попытка: {i}, процедура 1 пройдена", "green")
                return True
            elif in_b0 is True:
                self.logger.debug(f"попытка: {i}, процедура 1 не пройдена")
                self.cli_log.lev_warning(f"попытка: {i}, процедура 1 не пройдена", "red")
                if self.conn_opc.perv_obm_tv1_off():
                    self.logger.debug("сбрасываем первичную обмотку, и пробуем еще раз")
                    self.cli_log.lev_debug("сбрасываем первичную обмотку, и пробуем еще раз", "blue")
                    i += 1
                    continue
        else:
            self.logger.warning("процедура 1 не пройдена")
            self.cli_log.lev_warning("процедура 1 не пройдена", "red")
            self.conn_opc.ctrl_relay('KL62', False)
            self.conn_opc.ctrl_relay('KL37', False)
            raise HardwareException("Выходное напряжение не соответствует заданию.\n"
                                    "Неисправность узла формирования напряжения в стенде")

    def start_procedure_21(self) -> bool:
        """
        Включение контакта первичной обмотки
        :return: bool
        """
        self.logger.debug("процедура 2.1")
        self.cli_log.lev_info("процедура 2.1", "purple")
        self.conn_opc.ctrl_relay('KL43', True)
        sleep(1)
        condition = self._subtest_meas_volt()
        if condition:
            return True
        else:
            self.reset.stop_procedure_21()
            raise HardwareException("Выходное напряжение не соответствует заданию.\n"
                                    "Неисправность узла формирования напряжения в стенде")

    def start_procedure_22(self) -> bool:
        """
        Включение контакта первичной обмотки
        :return bool:
        """
        self.logger.debug("процедура 2.2")
        self.cli_log.lev_info("процедура 2.2", "purple")
        self.conn_opc.ctrl_relay('KL44', True)
        sleep(1)
        condition = self._subtest_meas_volt()
        if condition:
            self.logger.debug("процедура 2.2 пройдена")
            self.cli_log.lev_info("процедура 2.2 пройдена", "green")
            return True
        else:
            self.logger.warning("процедура 2.2 не пройдена")
            self.cli_log.lev_warning("процедура 2.2 не пройдена", "red")
            self.reset.stop_procedure_22()
            raise HardwareException("Выходное напряжение не соответствует заданию.\n"
                                    "Неисправность узла формирования напряжения в стенде")

    def start_procedure_24(self, coef_volt: float, setpoint_volt: float, factor: float = 1.0) -> float:
        """
        Включение контакта первичной обмотки, соответствующей напряжению U3[i]=U2[i]/Кс.
        Где U2[i] = напряжение, соответствующее i-ой уставке Сочетание контактов для напряжения U2[i]
        берем из файла «(Тор) TV1.xls»
        :param factor:
        :param coef_volt: float - коэффициент напряжения
        :param setpoint_volt: float - напряжение уставки
        :param factor: float - коэффициент повышения напряжения
        :return: float
        """
        self.logger.debug("процедура 2.4")
        self.cli_log.lev_info("процедура 2.4", "purple")
        calc_volt = factor * setpoint_volt / coef_volt
        self.logger.debug(f"вычисленное U: {calc_volt:.2f}, коэффициент: {factor}")
        self.cli_log.lev_info(f"вычисленное U: {calc_volt:.2f}, коэффициент: {factor}", "orange")
        self.perv_obm.perv_obm_tv1(calc_volt)
        self.logger.debug("включение первичной обмотки")
        self.cli_log.lev_debug("включение первичной обмотки", "blue")
        sleep(1)
        condition = self._subtest_meas_volt()
        self.logger.info(f"процедура 2.4: {calc_volt = :.2f}, {condition = }")
        self.cli_log.lev_info(f"процедура 2.4: {calc_volt = :.2f}, {condition = }", "orange")
        if condition:
            return calc_volt
        else:
            self.reset.stop_procedure_2()
            raise HardwareException("Выходное напряжение не соответствует заданию.\n"
                                    "Неисправность узла формирования напряжения в стенде")

    def start_procedure_31(self) -> float:
        """
        Процедура 3.1.
        Формирование испытательного сигнала ~ 5.96В
        KL60 – ВКЛ
        :return: meas_volt: напряжение
        """
        self.logger.debug("процедура 3.1")
        self.cli_log.lev_info("процедура 3.1", "purple")
        min_volt = 4.768
        max_volt = 7.152
        self.conn_opc.ctrl_relay('KL60', True)
        sleep(3)
        meas_volt = self.conn_opc.read_ai('AI0')
        self.logger.info(f"измеренное U: {min_volt = } <= {meas_volt = } <= {max_volt = }")
        self.cli_log.lev_info(f"измеренное U: {min_volt = } <= {meas_volt = } <= {max_volt = }", "orange")
        if min_volt <= meas_volt <= max_volt:
            self.logger.debug(f"процедура 3.1 пройдена")
            self.cli_log.lev_info(f"процедура 3.1 пройдена", "green")
            return meas_volt
        else:
            self.logger.warning(f"процедура 3.1 не пройдена")
            self.cli_log.lev_warning(f"процедура 3.1 не пройдена", "red")
            self.reset.stop_procedure_31()
            raise HardwareException("Выходное напряжение не соответствует заданию.\n"
                                    "Неисправность узла формирования напряжения в стенде")

    def start_procedure_32(self) -> float:
        """
        Формирование испытательного сигнала:
        Процедура: a=2
        ~ 51,54 В
        KL54 – ВКЛ
        AI.0 * K = U21 должен быть в диапазоне (0.8…1.2)*51.54
        от 41.232 до 61.848
        :return: float: напряжение
        """
        self.logger.debug("процедура 3.2")
        self.cli_log.lev_info("процедура 3.2", "purple")
        self.conn_opc.ctrl_relay('KL54', True)
        sleep(3)
        min_volt = 41.232
        max_volt = 61.848
        meas_volt = self.conn_opc.read_ai('AI0')
        self.logger.info(f'процедура 3.2 напряжение: {min_volt:.2f} <= {meas_volt:.2f} <= {max_volt:.2f}')
        self.cli_log.lev_info(f'процедура 3.2 напряжение: {min_volt:.2f} <= {meas_volt:.2f} <= {max_volt:.2f}', "orange")
        if min_volt <= meas_volt <= max_volt:
            self.logger.debug(f"процедура 3.2 пройдена")
            self.cli_log.lev_info(f"процедура 3.2 пройдена", "green")
            coef_volt = meas_volt / 51.54
            return coef_volt
        else:
            self.logger.warning(f"процедура 3.2 не пройдена")
            self.cli_log.lev_warning(f"процедура 3.2 не пройдена", "red")
            self.reset.stop_procedure_32()
            raise HardwareException("Выходное напряжение не соответствует заданию.\n"
                                    "Неисправность узла формирования напряжения в стенде")

    def start_procedure_34(self, calc_volt: float, setpoint_volt: float) -> bool:
        """
        Подпроцедура а=4 Включение контакта вторичной обмотки, соответствующей напряжению U3[i],
        определенному в Процедуре 2: а=4.
        KL48…KL59 – ВКЛ
        Рассчитываем и сравниваем	AI.0*K=U21 должен быть в диапазоне
        (0,9…1.1)* U2[i]
        :param calc_volt: float
        :param setpoint_volt: float
        :return bool:
        """
        self.logger.debug("процедура 3.4")
        self.cli_log.lev_info("процедура 3.4", "purple")
        self.vtor_obm.vtor_obm_tv1(calc_volt)
        sleep(3)
        min_volt = 0.88 * setpoint_volt
        max_volt = 1.11 * setpoint_volt
        meas_volt = self.conn_opc.read_ai('AI0')
        self.logger.info(f'процедура 3.4 напряжение: {min_volt:.2f} <= {meas_volt:.2f} <= {max_volt:.2f}')
        self.cli_log.lev_info(f'процедура 3.4 напряжение: {min_volt:.2f} <= {meas_volt:.2f} <= {max_volt:.2f}', "orange")
        if min_volt <= meas_volt <= max_volt:
            self.logger.debug(f"процедура 3.4 пройдена")
            self.cli_log.lev_info(f"процедура 3.4 пройдена", "green")
            return True
        else:
            self.logger.warning(f"процедура 3.4 не пройдена")
            self.cli_log.lev_warning(f"процедура 3.4 не пройдена", "red")
            self.reset.stop_procedure_3()
            return False

    def procedure_1_21_31(self) -> float:
        """
        1.1. Проверка вероятности наличия короткого замыкания на входе измерительной цепи блока.
        :return float: Напряжение
        """
        if self.start_procedure_1():
            if self.start_procedure_21():
                meas_volt = self.start_procedure_31()
                if meas_volt != 0.0:
                    return meas_volt
        raise HardwareException("Выходное напряжение не соответствует заданию.\n"
                                "Неисправность узла формирования напряжения в стенде")

    def procedure_1_21_31_v1(self, coef_min: float = 0.6, coef_max: float = 1.1) -> [float, float]:
        """
        1.1. Проверка вероятности наличия короткого замыкания на входе измерительной цепи блока.
        :return float: Напряжение
        """
        if self.start_procedure_1():
            if self.start_procedure_21():
                meas_volt = self.start_procedure_31()
                if meas_volt != 0.0:
                    min_volt = coef_min * meas_volt
                    max_volt = coef_max * meas_volt
                    self.logger.info(f"изм. напряжение умноженное на {coef_min} и на {coef_max}: "
                                     f"{min_volt = }, {max_volt = }")
                    self.cli_log.lev_info(f"изм. напряжение умноженное на {coef_min} и на {coef_max}: "
                                         f"{min_volt = }, {max_volt = }", "orange")
                    return min_volt, max_volt
        self.logger.warning('Неисправность узла формирования напряжения в стенде')
        self.cli_log.lev_warning('Неисправность узла формирования напряжения в стенде', "red")
        raise HardwareException("Выходное напряжение не соответствует заданию.\n"
                                "Неисправность узла формирования напряжения в стенде")

    def procedure_1_22_32(self) -> float:
        """
        1.2. Определение коэффициента Кс отклонения фактического напряжения от номинального.
        Процедура 1. Проверка отсутствия вероятности возникновения межвиткового замыкания
            на стороне первичной обмотки TV1
        Процедура 2: a=2. Проверка отсутствия вероятности возникновения межвиткового замыкания
            на стороне вторичной обмотки TV1:
        Процедура 3: a=2. Формирование испытательного сигнала для определения поправочного коэффициента сети:
        :return: float: коэффициент сети
        """
        if self.start_procedure_1():
            if self.start_procedure_22():
                coef_volt = self.start_procedure_32()
                if coef_volt != 0.0:
                    self.logger.info(f"коэффициент сети:\t {coef_volt:.2f}")
                    self.cli_log.lev_info(f"коэффициент сети:\t {coef_volt:.2f}", "orange")
                    return coef_volt
        self.logger.warning('Неисправность узла формирования напряжения в стенде')
        self.cli_log.lev_warning('Неисправность узла формирования напряжения в стенде', "red")
        raise HardwareException("Выходное напряжение не соответствует заданию.\n"
                                "Неисправность узла формирования напряжения в стенде")

    def procedure_1_24_34(self, coef_volt: float, setpoint_volt: float, factor: float = 1.0) -> bool:
        """
        Выполняется последовательно процедура 1 --> 2.4 --> 3.4
        :param coef_volt: float - коэффициент напряжения
        :param setpoint_volt: float - напряжение уставки
        :param factor: float - коэффициент повышения напряжения
        :return: bool
        """
        if self.start_procedure_1():
            calc_volt = self.start_procedure_24(coef_volt=coef_volt, setpoint_volt=setpoint_volt, factor=factor)
            if calc_volt != 0.0:
                if self.start_procedure_34(calc_volt=calc_volt, setpoint_volt=setpoint_volt):
                    return True
        return False

    def procedure_x4_to_x5(self, coef_volt: float, setpoint_volt: float) -> bool:
        """
        Процедура последовательно выполняет процедуры 1, 2.4, 3.4,
        если происходит какая-то ошибка, выполняет те же процедуры с напряжением увеличенным в 1.1 раза
        :param coef_volt: float - коэффициент напряжения
        :param setpoint_volt: float - напряжение уставки
        :return: bool
        """
        self.logger.debug("процедура \"procedure_x4_to_x5\", при неудачном выполнении процедур 1, 2.4, 3.4 "
                          "будут выполнены процедуры 1, 2.5, 3.5")
        self.cli_log.lev_debug("процедура \"procedure_x4_to_x5\", при неудачном выполнении процедур 1, 2.4, 3.4 "
                             "будут выполнены процедуры 1, 2.5, 3.5", "purple")
        if self.procedure_1_24_34(coef_volt=coef_volt, setpoint_volt=setpoint_volt, factor=1.0):
            return True
        else:
            self.reset.stop_procedure_3()
            if self.procedure_1_24_34(coef_volt=coef_volt, setpoint_volt=setpoint_volt, factor=1.1):
                return True
            else:
                self.logger.warning("Выходное напряжение не соответствует заданию.\n "
                                    "Неисправность узла формирования напряжения в стенде")
                self.cli_log.lev_warning("Выходное напряжение не соответствует заданию.\n "
                                     "Неисправность узла формирования напряжения в стенде", "red")
                raise HardwareException("Выходное напряжение не соответствует заданию.\n"
                                        "Неисправность узла формирования напряжения в стенде")

    def sbros_vtor_obm(self) -> bool:
        in_ai = self.conn_opc.read_ai('AI0')
        if in_ai <= 1.1:
            return True
        if in_ai > 1.1:
            self.conn_opc.vtor_obm_tv1_off()
            return True
        else:
            return False

    def _subtest_meas_volt(self) -> bool:
        """
        Функция измерения напряжения, после включения первичной обмотки.
        :return: Bool
        """
        self.logger.debug("измерение U в процедуре 2.х")
        self.cli_log.lev_info("измерение U в процедуре 2.х", "purple")
        for i in range(3):
            meas_volt = self.conn_opc.read_ai('AI0')
            self.logger.info(f"измерение U: {meas_volt:.2f}")
            self.cli_log.lev_info(f"измерение U: {meas_volt:.2f}", "orange")
            if meas_volt <= 1.1:
                self.logger.debug("напряжение соответствует")
                self.cli_log.lev_info("напряжение соответствует", "green")
                return True
            elif meas_volt > 1.1:
                self.logger.warning("напряжение не соответствует")
                self.cli_log.lev_warning("напряжение не соответствует", "red")
                self.sbros_vtor_obm()
                self.logger.debug("сброс вторичной обмотки")
                self.cli_log.lev_debug("сброс вторичной обмотки", "blue")
                self.logger.debug("повторение измерения")
                self.cli_log.lev_info("повторение измерения", "gray")
                i += 1
                continue
            return False
