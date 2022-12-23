#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from time import sleep

from gen_func_tv1 import *
from gen_func_utils import *
from gen_mb_client import *

__all__ = ["Procedure"]


class Procedure(object):
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
        self.ctrl_kl = CtrlKL()
        self.read_mb = ReadMB()
        self.fault = Bug(True)

        self.coef_volt: float
        self.setpoint_volt: float
        self.calc_volt: float

    def start_procedure_1(self) -> bool:
        """
        Процедура 1. сброс реле первичной и вторичной обмотки, проверка отсутствия напряжения на первичной обмотке.
        :return: bool
        """
        self.logger.debug("процедура 1")
        self.reset.sbros_vtor_obm()
        self.logger.debug("сброс вторичной обмотки")
        self.reset.sbros_perv_obm()
        self.logger.debug("сброс первичной обмотки")
        self.ctrl_kl.ctrl_relay('KL62', True)
        self.logger.debug("включение KL62")
        sleep(1)
        self.ctrl_kl.ctrl_relay('KL37', True)
        self.logger.debug("включение KL37")
        sleep(1)
        for i in range(3):
            in_b0 = self.read_mb.read_discrete(8)
            self.logger.debug(f"in_b0 = {in_b0} (False)")
            if in_b0 is False:
                self.fault.debug_msg(f"попытка: {i}, процедура 1 пройдена", 'green')
                self.logger.debug("процедура 1 пройдена")
                return True
            elif in_b0 is True:
                self.logger.debug(f"попытка: {i}, процедура 1 не пройдена")
                if self.reset.sbros_perv_obm():
                    self.logger.debug("сбрасываем первичную обмотку, и пробуем еще раз")
                    i += 1
                    continue
        else:
            self.logger.warning("процедура 1 не пройдена")
            self.fault.debug_msg("процедура 1 не пройдена", 'red')
            self.ctrl_kl.ctrl_relay('KL62', False)
            self.logger.debug("отключение KL62")
            self.ctrl_kl.ctrl_relay('KL37', False)
            self.logger.debug("отключение KL37")
            raise HardwareException("Выходное напряжение не соответствует заданию.\n"
                                    "Неисправность узла формирования напряжения в стенде")

    def start_procedure_21(self) -> bool:
        """
        Включение контакта первичной обмотки
        :return: bool
        """
        self.logger.debug("процедура 2.1")
        self.ctrl_kl.ctrl_relay('KL43', True)
        self.logger.debug("включение KL43")
        sleep(1)
        if self.__subtest_meas_volt():
            self.logger.debug("процедура 2.1 пройдена")
            self.fault.debug_msg("процедура 2.1 пройдена", 'green')
            return True
        else:
            self.logger.warning("процедура 2.1 не пройдена")
            self.fault.debug_msg("процедура 2.1 не пройдена", 'red')
            self.reset.stop_procedure_21()
            raise HardwareException("Выходное напряжение не соответствует заданию.\n"
                                    "Неисправность узла формирования напряжения в стенде")

    def start_procedure_22(self) -> bool:
        """
        Включение контакта первичной обмотки
        :return: bool
        """
        self.logger.debug("процедура 2.2")
        self.ctrl_kl.ctrl_relay('KL44', True)
        self.logger.debug("включение KL44")
        sleep(1)
        if self.__subtest_meas_volt():
            self.logger.debug("процедура 2.2 пройдена")
            self.fault.debug_msg("процедура 2.2 пройдена", 'green')
            return True
        else:
            self.logger.warning("процедура 2.2 не пройдена")
            self.fault.debug_msg("процедура 2.2 не пройдена", 'red')
            self.reset.stop_procedure_22()
            raise HardwareException("Выходное напряжение не соответствует заданию.\n"
                                    "Неисправность узла формирования напряжения в стенде")

    def start_procedure_24(self, coef_volt: float, setpoint_volt: float) -> float:
        """
        Включение контакта первичной обмотки, соответствующей напряжению U3[i]=U2[i]/Кс.
        Где U2[i] = напряжение, соответствующее i-ой уставке Сочетание контактов для напряжения U2[i]
        берем из файла «(Тор) TV1.xls»
        :param coef_volt: float
        :param setpoint_volt: float
        :return: float
        """
        self.logger.debug("процедура 2.4")
        calc_volt = setpoint_volt / coef_volt
        self.logger.debug(f"вычисленное U: {calc_volt}")
        self.perv_obm.perv_obm_tv1(calc_volt)
        self.logger.debug("включение первичной обмотки")
        sleep(1)
        if self.__subtest_meas_volt():
            self.logger.debug("процедура 2.4 пройдена")
            self.fault.debug_msg(f"процедура 2.4 пройдена, {calc_volt = :.2f}", 'green')
            return calc_volt
        else:
            self.logger.warning("процедура 2.4 не пройдена")
            self.fault.debug_msg(f"процедура 2.4 не пройдена, {calc_volt = :.2f}", 'red')
            self.reset.stop_procedure_2()
            raise HardwareException("Выходное напряжение не соответствует заданию.\n"
                                    "Неисправность узла формирования напряжения в стенде")

    def start_procedure_25(self, coef_volt: float, setpoint_volt: float) -> float:
        """
        Включение контакта первичной обмотки, соответствующей напряжению U3[i]=1,1*U2[i]/Кс.
        Где U2[i] = напряжение, соответствующее i-ой уставке Сочетание контактов для напряжения U2[i]
        берем из файла «(Тор) TV1.xls»
        :param coef_volt: float
        :param setpoint_volt: float
        :return: float
        """
        self.logger.debug("процедура 2.5")
        calc_volt = 1.1 * setpoint_volt / coef_volt
        self.logger.debug(f"вычисленное U: {calc_volt}")
        self.perv_obm.perv_obm_tv1(calc_volt)
        self.logger.debug("включение первичной обмотки")
        sleep(1)
        if self.__subtest_meas_volt():
            self.logger.debug("процедура 2.5 пройдена")
            self.fault.debug_msg(f"процедура 2.5 пройдена, {calc_volt = :.2f}", 'green')
            return calc_volt
        else:
            self.logger.warning("процедура 2.5 не пройдена")
            self.fault.debug_msg(f"процедура 2.5 не пройдена, {calc_volt = :.2f}", 'red')
            self.reset.stop_procedure_2()
            raise HardwareException("Выходное напряжение не соответствует заданию.\n"
                                    "Неисправность узла формирования напряжения в стенде")

    def __subtest_meas_volt(self) -> bool:
        """
        Функция измерения напряжения, после включения первичной обмотки.
        :return: bool
        """
        self.logger.debug("измерение U в процедуре 2.х")
        for i in range(3):
            meas_volt = self.read_mb.read_analog()
            self.logger.debug(f"измерение U: {meas_volt}")
            self.fault.debug_msg(f'измеренное напряжение в процедуре 2.х:\t {meas_volt:.2f}', 'orange')
            if meas_volt <= 1.1:
                self.logger.debug("напряжение соответствует")
                return True
            elif meas_volt > 1.1:
                self.logger.warning("напряжение не соответствует")
                self.sbros_vtor_obm()
                self.logger.debug("сброс вторичной обмотки")
                i += 1
                self.logger.debug("повторение измерения")
                continue
            return False

    def start_procedure_31(self) -> float:
        """
        a=1
        Формирование испытательного сигнала
        ~ 5.96В
        KL60 – ВКЛ
        :return: float: напряжение
        """
        self.logger.debug("процедура 3.1")
        min_volt = 4.768
        max_volt = 7.152
        self.ctrl_kl.ctrl_relay('KL60', True)
        self.logger.debug("включение KL60")
        sleep(3)
        meas_volt = self.read_mb.read_analog()
        self.logger.debug(f"измеренное U: {min_volt} <= {meas_volt} <= {max_volt}")
        self.fault.debug_msg(f'процедура 3.1 напряжение:\t  '
                             f'{min_volt:.2f} <= {meas_volt:.2f} <= {max_volt:.2f}', 'orange')
        if min_volt <= meas_volt <= max_volt:
            self.logger.debug(f"процедура 3.1 пройдена")
            self.fault.debug_msg("процедура 3.1 пройдена", 'green')
            return meas_volt
        else:
            self.logger.warning(f"процедура 3.1 не пройдена")
            self.fault.debug_msg("процедура 3.1 не пройдена", 'red')
            self.reset.stop_procedure_31()
            raise HardwareException("Выходное напряжение не соответствует заданию.\n"
                                    "Неисправность узла формирования напряжения в стенде")

    def start_procedure_32(self) -> float:
        """
        a=2	Формирование испытательного сигнала
        ~ 51,54 В
        KL54 – ВКЛ
        AI.0*K=U21 должен быть в диапазоне (0.8…1.2)*51.54
        от 41.232 до 61.848
        :return: float: напряжение
        """
        self.ctrl_kl.ctrl_relay('KL54', True)
        sleep(3)
        min_volt = 41.232
        max_volt = 61.848
        meas_volt = self.read_mb.read_analog()
        self.logger.debug(f"измеренное U: {min_volt} <= {meas_volt} <= {max_volt}")
        self.fault.debug_msg(f'процедура 3.2 напряжение: '
                             f'{min_volt:.2f} <= {meas_volt:.2f} <= {max_volt:.2f}', 'orange')
        if min_volt <= meas_volt <= max_volt:
            self.logger.debug(f"процедура 3.2 пройдена")
            self.fault.debug_msg("процедура 3.2 пройдена", 'green')
            coef_volt = meas_volt / 51.54
            return coef_volt
        else:
            self.logger.warning(f"процедура 3.2 не пройдена")
            self.fault.debug_msg("процедура 3.2 не пройдена", 'red')
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
        :return: bool
        """
        self.vtor_obm.vtor_obm_tv1(calc_volt)
        sleep(3)
        min_volt = 0.88 * setpoint_volt
        max_volt = 1.11 * setpoint_volt
        meas_volt = self.read_mb.read_analog()
        self.logger.debug(f"измеренное U: {min_volt} <= {meas_volt} <= {max_volt}")
        self.fault.debug_msg(f'процедура 3.4 напряжение: '
                             f'{min_volt:.2f} <= {meas_volt:.2f} <= {max_volt:.2f}', 'orange')
        if min_volt <= meas_volt <= max_volt:
            self.logger.debug(f"процедура 3.4 пройдена")
            self.fault.debug_msg("процедура 3.4 пройдена", 'green')
            return True
        else:
            self.logger.warning(f"процедура 3.4 не пройдена")
            self.fault.debug_msg("процедура 3.4 не пройдена", 'red')
            self.reset.stop_procedure_3()
            return False

    def start_procedure_35(self, calc_volt: float, setpoint_volt: float) -> bool:
        """
        Подпроцедура а=5 Включение контакта вторичной обмотки, соответствующей напряжению U3[i],
        определенному в Процедуре 2: а=5.
        KL48…KL59 – ВКЛ
        Рассчитываем и сравниваем	AI.0*K=U21 должен быть в диапазоне
        (0,9…1.1)* 1,1*U2[i] = 0.99 до 1.21
        :param calc_volt: float
        :param setpoint_volt: float
        :return: bool
        """
        self.vtor_obm.vtor_obm_tv1(calc_volt)
        sleep(3)
        min_volt = 0.9 * setpoint_volt
        max_volt = 1.1 * setpoint_volt
        meas_volt = self.read_mb.read_analog()
        self.logger.debug(f"измеренное U: {min_volt} <= {meas_volt} <= {max_volt}")
        self.fault.debug_msg(f'процедура 3.5 напряжение: '
                             f'{min_volt:.2f} <= {meas_volt:.2f} <= {max_volt:.2f}', 'orange')
        if min_volt <= meas_volt <= max_volt:
            self.logger.debug(f"процедура 3.5 пройдена")
            self.fault.debug_msg("процедура 3.5 пройдена", 'green')
            return True
        else:
            self.logger.warning(f"процедура 3.5 не пройдена")
            self.fault.debug_msg("процедура 3.5 не пройдена", 'red')
            self.reset.stop_procedure_3()
            return False

    def procedure_1_21_31(self) -> float:
        """
        1.1. Проверка вероятности наличия короткого замыкания на входе измерительной цепи блока
        :return: float: напряжение
        """
        if self.start_procedure_1():
            if self.start_procedure_21():
                meas_volt = self.start_procedure_31()
                if meas_volt != 0.0:
                    return meas_volt
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
                    self.fault.debug_msg(f'коэффициент сети:\t {coef_volt:.2f}', 'orange')
                    return coef_volt
        raise HardwareException("Выходное напряжение не соответствует заданию.\n"
                                "Неисправность узла формирования напряжения в стенде")

    def procedure_1_24_34(self, coef_volt: float, setpoint_volt: float) -> bool:
        """
            выполняется последовательно процедура 1 --> 2.4 --> 3.4
            :return: bool
        """
        if self.start_procedure_1():
            calc_volt = self.start_procedure_24(coef_volt=coef_volt, setpoint_volt=setpoint_volt)
            if calc_volt != 0.0:
                if self.start_procedure_34(calc_volt=calc_volt, setpoint_volt=setpoint_volt):
                    return True
        return False

    def procedure_1_25_35(self, coef_volt: float, setpoint_volt: float) -> bool:
        """
            выполняется последовательно процедура 1 --> 2.5 --> 3.5
            :return: bool
        """
        if self.start_procedure_1():
            calc_volt = self.start_procedure_25(coef_volt=coef_volt, setpoint_volt=setpoint_volt)
            if calc_volt != 0.0:
                if self.start_procedure_35(calc_volt=calc_volt, setpoint_volt=setpoint_volt):
                    return True
        return False

    def procedure_x4_to_x5(self, coef_volt: float, setpoint_volt: float) -> bool:
        self.logger.debug("процедура \"procedure_x4_to_x5\", при неудачном выполнении процедур 1, 2.4, 3.4 "
                          "будут выполнены процедуры 1, 2.5, 3.5")
        if self.procedure_1_24_34(coef_volt, setpoint_volt):
            return True
        else:
            self.reset.stop_procedure_3()
            if self.procedure_1_25_35(coef_volt, setpoint_volt):
                return True
            else:
                self.logger.debug("Выходное напряжение не соответствует заданию.\n "
                                  "Неисправность узла формирования напряжения в стенде")
                raise HardwareException("Выходное напряжение не соответствует заданию.\n"
                                        "Неисправность узла формирования напряжения в стенде")

    def sbros_vtor_obm(self) -> bool:
        in_ai = self.read_mb.read_analog()
        if in_ai <= 1.1:
            return True
        if in_ai > 1.1:
            self.reset.sbros_vtor_obm()
            return True
        else:
            return False

    # def sbros_perv_obm(self) -> bool:
    #     self.reset.sbros_perv_obm()
    #     sleep(0.1)
    #     in_b0 = self.read_mb.read_discrete(8)
    #     if in_b0 is False:
    #         return True
    #     elif in_b0 is True:
    #         self.reset.sbros_perv_obm()
    #         return True
    #     else:
    #         return False

    # def start_procedure_23(self, coef_volt: float) -> float:
    #     """
    #     Включение контакта первичной обмотки, соответствующей напряжению U3=U2/Кс.
    #     Где U2 =80В.
    #     Сочетание контактов берем из файла «(Тор) TV1.xls»
    #     :param coef_volt: float
    #     :return: float
    #     """
    #     self.logger.debug("процедура 2.3")
    #     calc_volt = 80.0 / coef_volt
    #     self.logger.debug(f"вычисленное U: {calc_volt}")
    #     self.perv_obm.perv_obm_tv1(calc_volt)
    #     self.logger.debug("включение первичной обмотки")
    #     sleep(1)
    #     if self.__subtest_meas_volt():
    #         self.logger.debug("процедура 2.3 пройдена")
    #         self.fault.debug_msg(f"процедура 2.3 пройдена, {calc_volt = :.2f}", 'green')
    #         return calc_volt
    #     else:
    #         self.logger.warning("процедура 2.3 не пройдена")
    #         self.fault.debug_msg(f"процедура 2.3 не пройдена, {calc_volt = :.2f}", 'red')
    #         self.reset.stop_procedure_2()
    #         raise HardwareException("Выходное напряжение не соответствует заданию.\n"
    #                                 "Неисправность узла формирования напряжения в стенде")

    # def start_procedure_26(self, coef_volt: float) -> float:
    #     """
    #     Включение контакта первичной обмотки, соответствующей напряжению U3=U2/Кс.
    #     Где U2 =85.6В.
    #     Сочетание контактов берем из файла «(Тор) TV1.xls»
    #     :param coef_volt: float
    #     :return: float
    #     """
    #     self.logger.debug("процедура 2.6")
    #     calc_volt = 85.6 / coef_volt
    #     self.logger.debug(f"вычисленное U: {calc_volt}")
    #     self.perv_obm.perv_obm_tv1(calc_volt)
    #     self.logger.debug("включение первичной обмотки")
    #     sleep(1)
    #     if self.__subtest_meas_volt():
    #         self.logger.debug("процедура 2.6 пройдена")
    #         self.fault.debug_msg(f"процедура 2.6 пройдена, {calc_volt = :.2f}", 'green')
    #         return calc_volt
    #     else:
    #         self.logger.warning("процедура 2.6 не пройдена")
    #         self.fault.debug_msg(f"процедура 2.6 не пройдена, {calc_volt = :.2f}", 'red')
    #         self.reset.stop_procedure_2()
    #         raise HardwareException("Выходное напряжение не соответствует заданию.\n"
    #                                 "Неисправность узла формирования напряжения в стенде")

    # def start_procedure_27(self, coef_volt: float) -> float:
    #     """
    #     Включение контакта первичной обмотки, соответствующей напряжению U3=U2/Кс.
    #     Где U2 =20В.
    #     Сочетание контактов берем из файла «(Тор) TV1.xls»
    #     :param coef_volt: float
    #     :return: float
    #     """
    #     self.logger.debug("процедура 2.7")
    #     calc_volt = 20 / coef_volt
    #     self.logger.debug(f"вычисленное U: {calc_volt}")
    #     self.perv_obm.perv_obm_tv1(calc_volt)
    #     self.logger.debug("включение первичной обмотки")
    #     sleep(1)
    #     if self.__subtest_meas_volt():
    #         self.logger.debug("процедура 2.7 пройдена")
    #         self.fault.debug_msg(f"процедура 2.7 пройдена, {calc_volt = :.2f}", 'green')
    #         return calc_volt
    #     else:
    #         self.logger.warning("процедура 2.7 не пройдена")
    #         self.fault.debug_msg(f"процедура 2.7 не пройдена, {calc_volt = :.2f}", 'red')
    #         self.reset.stop_procedure_2()
    #         raise HardwareException("Выходное напряжение не соответствует заданию.\n"
    #                                 "Неисправность узла формирования напряжения в стенде")

    # def start_procedure_28(self, coef_volt: float, setpoint_volt: float) -> float:
    #     """
    #     Включение контакта первичной обмотки, соответствующей напряжению U3[i]=1,15*U2[i]/Кс.
    #     Где U2[i] = напряжение, соответствующее i-ой уставке Сочетание контактов для напряжения U2[i]
    #     берем из файла «(Тор) TV1.xls»
    #     :param coef_volt: float
    #     :param setpoint_volt: float
    #     :return: float
    #     """
    #     self.logger.debug("процедура 2.8")
    #     calc_volt = 1.15 * setpoint_volt / coef_volt
    #     self.logger.debug(f"вычисленное U: {calc_volt}")
    #     self.perv_obm.perv_obm_tv1(calc_volt)
    #     self.logger.debug("включение первичной обмотки")
    #     sleep(1)
    #     if self.__subtest_meas_volt():
    #         self.logger.debug("процедура 2.8 пройдена")
    #         self.fault.debug_msg(f"процедура 2.8 пройдена, {calc_volt = :.2f}", 'green')
    #         return calc_volt
    #     else:
    #         self.logger.warning("процедура 2.8 не пройдена")
    #         self.fault.debug_msg(f"процедура 2.8 не пройдена, {calc_volt = :.2f}", 'red')
    #         self.reset.stop_procedure_2()
    #         raise HardwareException("Выходное напряжение не соответствует заданию.\n"
    #                                 "Неисправность узла формирования напряжения в стенде")

    # def start_procedure_29(self, coef_volt: float) -> float:
    #     """
    #     Включение контакта первичной обмотки, соответствующей напряжению U3=U2/Кс.
    #     Где U2 =25.2В.
    #     Сочетание контактов берем из файла «(Тор) TV1.xls»TV1.xls»
    #     :param coef_volt: float
    #     :return: float
    #     """
    #     self.logger.debug("процедура 2.9")
    #     calc_volt = 25.2 / coef_volt
    #     self.logger.debug(f"вычисленное U: {calc_volt}")
    #     self.perv_obm.perv_obm_tv1(calc_volt)
    #     self.logger.debug("включение первичной обмотки")
    #     sleep(1)
    #     if self.__subtest_meas_volt():
    #         self.logger.debug("процедура 2.9 пройдена")
    #         self.fault.debug_msg(f"процедура 2.9 пройдена, {calc_volt = :.2f}", 'green')
    #         return calc_volt
    #     else:
    #         self.logger.warning("процедура 2.9 не пройдена")
    #         self.fault.debug_msg(f"процедура 2.9 не пройдена, {calc_volt = :.2f}", 'red')
    #         self.reset.stop_procedure_2()
    #         raise HardwareException("Выходное напряжение не соответствует заданию.\n"
    #                                 "Неисправность узла формирования напряжения в стенде")

    # def start_procedure_210(self, coef_volt: float) -> float:
    #     """
    #     Включение контакта первичной обмотки, соответствующей напряжению U3=U2/Кс.
    #     Где U2 =8,2В.
    #     Сочетание контактов берем из файла «(Тор) TV1.xls»TV1.xls»
    #     :param coef_volt: float
    #     :return: float
    #     """
    #     self.logger.debug("процедура 2.10")
    #     calc_volt = 8.2 / coef_volt
    #     self.logger.debug(f"вычисленное U: {calc_volt}")
    #     self.perv_obm.perv_obm_tv1(calc_volt)
    #     self.logger.debug("включение первичной обмотки")
    #     sleep(1)
    #     if self.__subtest_meas_volt():
    #         self.logger.debug("процедура 2.10 пройдена")
    #         self.fault.debug_msg(f"процедура 2.10 пройдена, {calc_volt = :.2f}", 'green')
    #         return calc_volt
    #     else:
    #         self.logger.warning("процедура 2.10 не пройдена")
    #         self.fault.debug_msg(f"процедура 2.10 не пройдена, {calc_volt = :.2f}", 'red')
    #         self.reset.stop_procedure_2()
    #         raise HardwareException("Выходное напряжение не соответствует заданию.\n"
    #                                 "Неисправность узла формирования напряжения в стенде")

    # def start_procedure_211(self, coef_volt: float) -> float:
    #     """
    #     Включение контакта первичной обмотки, соответствующей напряжению U3=U2/Кс.
    #     Где U2 =10,7В.
    #     Сочетание контактов берем из файла «(Тор) TV1.xls»TV1.xls»
    #     :param coef_volt: float
    #     :return: float
    #     """
    #     self.logger.debug("процедура 2.11")
    #     calc_volt = 10.7 / coef_volt
    #     self.logger.debug(f"вычисленное U: {calc_volt}")
    #     self.perv_obm.perv_obm_tv1(calc_volt)
    #     self.logger.debug("включение первичной обмотки")
    #     sleep(1)
    #     if self.__subtest_meas_volt():
    #         self.logger.debug("процедура 2.11 пройдена")
    #         self.fault.debug_msg(f"процедура 2.11 пройдена, {calc_volt = :.2f}", 'green')
    #         return calc_volt
    #     else:
    #         self.logger.warning("процедура 2.11 не пройдена")
    #         self.fault.debug_msg(f"процедура 2.11 не пройдена, {calc_volt = :.2f}", 'red')
    #         self.reset.stop_procedure_2()
    #         raise HardwareException("Выходное напряжение не соответствует заданию.\n"
    #                                 "Неисправность узла формирования напряжения в стенде")

    # def start_procedure_212(self, coef_volt: float) -> float:
    #     """
    #     Включение контакта первичной обмотки, соответствующей напряжению U3=U2/Кс.
    #     Где U2 =38В. изменено на 80В
    #     Сочетание контактов берем из файла «(Тор) TV1.xls»
    #     :param coef_volt: float
    #     :return: float
    #     """
    #     self.logger.debug("процедура 2.12")
    #     calc_volt = 80.0 / coef_volt
    #     self.logger.debug(f"вычисленное U: {calc_volt}")
    #     self.perv_obm.perv_obm_tv1(calc_volt)
    #     self.logger.debug("включение первичной обмотки")
    #     sleep(1)
    #     if self.__subtest_meas_volt():
    #         self.logger.debug("процедура 2.12 пройдена")
    #         self.fault.debug_msg(f"процедура 2.12 пройдена, {calc_volt = :.2f}", 'green')
    #         return calc_volt
    #     else:
    #         self.logger.warning("процедура 2.12 не пройдена")
    #         self.fault.debug_msg(f"процедура 2.12 не пройдена, {calc_volt = :.2f}", 'red')
    #         self.reset.stop_procedure_2()
    #         raise HardwareException("Выходное напряжение не соответствует заданию.\n"
    #                                 "Неисправность узла формирования напряжения в стенде")

    # def start_procedure_33(self, calc_volt: float) -> bool:
    #     """
    #     Подпроцедуры а=3, a=6, a=7	Включение контакта вторичной обмотки, соответствующей напряжению U3,
    #     определенному в Процедуре 2:
    #     KL48…KL59 – ВКЛ
    #     AI.0*K=U21 должен быть в диапазоне
    #     (0,9…1.1)*85.6 = 77,04 до 94,16
    #     :param calc_volt: float
    #     :return: bool
    #     """
    #     self.vtor_obm.vtor_obm_tv1(calc_volt)
    #     sleep(3)
    #     min_volt = 77.04
    #     max_volt = 94.17
    #     meas_volt = self.read_mb.read_analog()
    #     self.logger.debug(f"измеренное U: {min_volt} <= {meas_volt} <= {max_volt}")
    #     self.fault.debug_msg(f'процедура 3.3 напряжение: '
    #                          f'{min_volt:.2f} <= {meas_volt:.2f} <= {max_volt:.2f}', 'orange')
    #     if min_volt <= meas_volt <= max_volt:
    #         self.logger.debug(f"процедура 3.3 пройдена")
    #         self.fault.debug_msg("процедура 3.3 пройдена", 'green')
    #         return True
    #     else:
    #         self.logger.warning(f"процедура 3.3 не пройдена")
    #         self.fault.debug_msg("процедура 3.3 не пройдена", 'red')
    #         self.reset.stop_procedure_3()
    #         raise HardwareException("Выходное напряжение не соответствует заданию.\n"
    #                                 "Неисправность узла формирования напряжения в стенде")

    # def start_procedure_36(self, calc_volt: float) -> bool:
    #     """
    #     Подпроцедуры а=3, a=6, a=7	Включение контакта вторичной обмотки, соответствующей напряжению U3,
    #     определенному в Процедуре 2: а=3.
    #     KL48…KL59 – ВКЛ
    #     Рассчитываем и сравниваем	AI.0*K=U21 должен быть в диапазоне
    #     (0,9…1.1)*20 = 18 до 22
    #     :param calc_volt: float
    #     :return: bool
    #     """
    #     self.vtor_obm.vtor_obm_tv1(calc_volt)
    #     sleep(3)
    #     min_volt = 18.0
    #     max_volt = 22.0
    #     meas_volt = self.read_mb.read_analog()
    #     self.logger.debug(f"измеренное U: {min_volt} <= {meas_volt} <= {max_volt}")
    #     self.fault.debug_msg(f'процедура 3.6 напряжение: '
    #                          f'{min_volt:.2f} <= {meas_volt:.2f} <= {max_volt:.2f}', 'orange')
    #     if min_volt <= meas_volt <= max_volt:
    #         self.logger.debug(f"процедура 3.6 пройдена")
    #         self.fault.debug_msg("процедура 3.6 пройдена", 'green')
    #         return True
    #     else:
    #         self.logger.warning(f"процедура 3.6 не пройдена")
    #         self.fault.debug_msg("процедура 3.6 не пройдена", 'red')
    #         self.reset.stop_procedure_3()
    #         raise HardwareException("Выходное напряжение не соответствует заданию.\n"
    #                                 "Неисправность узла формирования напряжения в стенде")

    # def start_procedure_37(self, calc_volt: float) -> bool:
    #     """
    #     а=3, a=6, a=7	Включение контакта вторичной обмотки, соответствующей напряжению U3,
    #     определенному в Процедуре 2: а=3.
    #     KL48…KL59 – ВКЛ
    #     Рассчитываем и сравниваем	AI.0*K=U21 должен быть в диапазоне
    #     (0,9…1.1)*80 = 72 до 88
    #     :param calc_volt: float
    #     :return: bool
    #     """
    #     self.vtor_obm.vtor_obm_tv1(calc_volt)
    #     sleep(3)
    #     min_volt = 72.0
    #     max_volt = 88.0
    #     meas_volt = self.read_mb.read_analog()
    #     self.logger.debug(f"измеренное U: {min_volt} <= {meas_volt} <= {max_volt}")
    #     self.fault.debug_msg(f'процедура 3.7 напряжение: '
    #                          f'{min_volt:.2f} <= {meas_volt:.2f} <= {max_volt:.2f}', 'orange')
    #     if min_volt <= meas_volt <= max_volt:
    #         self.logger.debug(f"процедура 3.7 пройдена")
    #         self.fault.debug_msg("процедура 3.7 пройдена", 'green')
    #         return True
    #     else:
    #         self.logger.warning(f"процедура 3.7 не пройдена")
    #         self.fault.debug_msg("процедура 3.7 не пройдена", 'red')
    #         self.reset.stop_procedure_3()
    #         raise HardwareException("Выходное напряжение не соответствует заданию.\n"
    #                                 "Неисправность узла формирования напряжения в стенде")

    # def start_procedure_38(self, calc_volt: float) -> bool:
    #     """
    #     а=3, a=6, a=7	Включение контакта вторичной обмотки, соответствующей напряжению U3,
    #     определенному в Процедуре 2: а=3.
    #     KL48…KL59 – ВКЛ
    #     Рассчитываем и сравниваем	AI.0*K=U21 должен быть в диапазоне
    #     AI.0*K=U21 должен быть в диапазоне
    #     (0,9…1.1)*25.2 = от 22.68 и до 27.72
    #     :param calc_volt: float
    #     :return: bool
    #     """
    #     self.vtor_obm.vtor_obm_tv1(calc_volt)
    #     sleep(3)
    #     min_volt = 22.68
    #     max_volt = 27.72
    #     meas_volt = self.read_mb.read_analog()
    #     self.logger.debug(f"измеренное U: {min_volt} <= {meas_volt} <= {max_volt}")
    #     self.fault.debug_msg(f'процедура 3.8 напряжение: '
    #                          f'{min_volt:.2f} <= {meas_volt:.2f} <= {max_volt:.2f}', 'orange')
    #     if min_volt <= meas_volt <= max_volt:
    #         self.logger.debug(f"процедура 3.8 пройдена")
    #         self.fault.debug_msg("процедура 3.8 пройдена", 'green')
    #         return True
    #     else:
    #         self.logger.warning(f"процедура 3.8 не пройдена")
    #         self.fault.debug_msg("процедура 3.8 не пройдена", 'red')
    #         self.reset.stop_procedure_3()
    #         raise HardwareException("Выходное напряжение не соответствует заданию.\n"
    #                                 "Неисправность узла формирования напряжения в стенде")

    # def start_procedure_39(self, calc_volt: float) -> bool:
    #     """
    #     Включение контакта вторичной обмотки, соответствующей напряжению U3,
    #     определенному в Процедуре 2
    #     KL48…KL59 – ВКЛ
    #     Рассчитываем и сравниваем	AI.0*K=U21 должен быть в диапазоне
    #     AI.0*K=U21 должен быть в диапазоне
    #     (0,9…1.1)*8.2 = 7.38 до 9.02
    #     :param calc_volt: float
    #     :return: bool
    #     """
    #     self.vtor_obm.vtor_obm_tv1(calc_volt)
    #     sleep(3)
    #     min_volt = 7.38
    #     max_volt = 9.02
    #     meas_volt = self.read_mb.read_analog()
    #     self.logger.debug(f"измеренное U: {min_volt} <= {meas_volt} <= {max_volt}")
    #     self.fault.debug_msg(f'процедура 3.9 напряжение: '
    #                          f'{min_volt:.2f} <= {meas_volt:.2f} <= {max_volt:.2f}', 'orange')
    #     if min_volt <= meas_volt <= max_volt:
    #         self.logger.debug(f"процедура 3.9 пройдена")
    #         self.fault.debug_msg("процедура 3.9 пройдена", 'green')
    #         return True
    #     else:
    #         self.logger.warning(f"процедура 3.9 не пройдена")
    #         self.fault.debug_msg("процедура 3.9 не пройдена", 'red')
    #         self.reset.stop_procedure_3()
    #         raise HardwareException("Выходное напряжение не соответствует заданию.\n"
    #                                 "Неисправность узла формирования напряжения в стенде")

    # def start_procedure_310(self, calc_volt: float) -> bool:
    #     """
    #     Включение контакта вторичной обмотки, соответствующей напряжению U3,
    #     определенному в Процедуре 2
    #     KL48…KL59 – ВКЛ
    #     Рассчитываем и сравниваем	AI.0*K=U21 должен быть в диапазоне
    #     AI.0*K=U21 должен быть в диапазоне
    #     (0,9…1.1)*10.7 = 9.63 до 11.77
    #     :param calc_volt: float
    #     :return: bool
    #     """
    #     self.vtor_obm.vtor_obm_tv1(calc_volt)
    #     sleep(3)
    #     min_volt = 9.63
    #     max_volt = 11.77
    #     meas_volt = self.read_mb.read_analog()
    #     self.logger.debug(f"измеренное U: {min_volt} <= {meas_volt} <= {max_volt}")
    #     self.fault.debug_msg(f'процедура 3.10 напряжение: '
    #                          f'{min_volt:.2f} <= {meas_volt:.2f} <= {max_volt:.2f}', 'orange')
    #     if min_volt <= meas_volt <= max_volt:
    #         self.logger.debug(f"процедура 3.10 пройдена")
    #         self.fault.debug_msg("процедура 3.10 пройдена", 'green')
    #         return True
    #     else:
    #         self.logger.warning(f"процедура 3.10 не пройдена")
    #         self.fault.debug_msg("процедура 3.10 не пройдена", 'red')
    #         self.reset.stop_procedure_3()
    #         raise HardwareException("Выходное напряжение не соответствует заданию.\n"
    #                                 "Неисправность узла формирования напряжения в стенде")

    # def start_procedure_311(self, calc_volt: float, setpoint_volt: float) -> bool:
    #     """
    #     а=4	Включение контакта вторичной обмотки, соответствующей напряжению U3[i],
    #     определенному в Процедуре 2: а=4.
    #     KL48…KL59 – ВКЛ
    #     Рассчитываем и сравниваем	AI.0*K=U21 должен быть в диапазоне
    #     (0,85…1.1)* U2[i]
    #     :param calc_volt: float
    #     :param setpoint_volt: float
    #     :return: bool
    #     """
    #     self.vtor_obm.vtor_obm_tv1(calc_volt)
    #     sleep(3)
    #     min_volt = 0.85 * setpoint_volt
    #     max_volt = 1.1 * setpoint_volt
    #     meas_volt = self.read_mb.read_analog()
    #     self.logger.debug(f"измеренное U: {min_volt} <= {meas_volt} <= {max_volt}")
    #     self.fault.debug_msg(f'процедура 3.11 напряжение: '
    #                          f'{min_volt:.2f} <= {meas_volt:.2f} <= {max_volt:.2f}', 'orange')
    #     if min_volt <= meas_volt <= max_volt:
    #         self.logger.debug(f"процедура 3.11 пройдена")
    #         self.fault.debug_msg("процедура 3.11 пройдена", 'green')
    #         return True
    #     else:
    #         self.logger.warning(f"процедура 3.11 не пройдена")
    #         self.fault.debug_msg("процедура 3.11 не пройдена", 'red')
    #         self.reset.stop_procedure_3()
    #         raise HardwareException("Выходное напряжение не соответствует заданию.\n"
    #                                 "Неисправность узла формирования напряжения в стенде")

    # def start_procedure_312(self, calc_volt: float) -> bool:
    #     """
    #     а=12
    #     Включение контакта вторичной обмотки, соответствующей напряжению U3, определенному в Процедуре 2: а=12.
    #     KL48…KL59 – ВКЛ
    #     Рассчитываем и сравниваем	AI.0*K=U21 должен быть в диапазоне
    #     (0,9…1.1)* U2 = 72.0 до 88.0
    #     :param calc_volt: float
    #     :return: bool
    #     """
    #     self.vtor_obm.vtor_obm_tv1(calc_volt)
    #     sleep(3)
    #     min_volt = 72.0
    #     max_volt = 88.0
    #     meas_volt = self.read_mb.read_analog()
    #     self.logger.debug(f"измеренное U: {min_volt} <= {meas_volt} <= {max_volt}")
    #     self.fault.debug_msg(f'процедура 3.12 напряжение: '
    #                          f'{min_volt:.2f} <= {meas_volt:.2f} <= {max_volt:.2f}', 'orange')
    #     if min_volt <= meas_volt <= max_volt:
    #         self.logger.debug(f"процедура 3.12 пройдена")
    #         self.fault.debug_msg("процедура 3.12 пройдена", 'green')
    #         return True
    #     else:
    #         self.logger.warning(f"процедура 3.12 не пройдена")
    #         self.fault.debug_msg("процедура 3.12 не пройдена", 'red')
    #         self.reset.stop_procedure_3()
    #         raise HardwareException("Выходное напряжение не соответствует заданию.\n"
    #                                 "Неисправность узла формирования напряжения в стенде")
