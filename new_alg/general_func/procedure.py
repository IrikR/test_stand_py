#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from time import sleep

from .ctrl_tv1 import *
from .modbus import *
from .exception import *
from .reset import ResetRelay

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
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))
        self.perv_obm = PervObmTV1()
        self.vtor_obm = VtorObmTV1()
        self.reset = ResetRelay()
        self.ctrl_kl = CtrlKL()
        self.read_mb = ReadMB()
        self.di_read = DIRead()
        self.ai_read = AIRead()

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
            in_b0, *_ = self.di_read.di_read('in_b0')
            self.logger.debug(f"in_b0 = {in_b0} (False)")
            if in_b0 is False:
                self.logger.debug(f"попытка: {i}, процедура 1 пройдена")
                return True
            elif in_b0 is True:
                self.logger.debug(f"попытка: {i}, процедура 1 не пройдена")
                if self.reset.sbros_perv_obm():
                    self.logger.debug("сбрасываем первичную обмотку, и пробуем еще раз")
                    i += 1
                    continue
        else:
            self.logger.warning("процедура 1 не пройдена")
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
        :return: bool
        """
        self.logger.debug("процедура 2.2")
        self.ctrl_kl.ctrl_relay('KL44', True)
        self.logger.debug("включение KL44")
        sleep(1)
        condition = self._subtest_meas_volt()
        if condition:
            self.logger.debug("процедура 2.2 пройдена")
            return True
        else:
            self.logger.warning("процедура 2.2 не пройдена")
            self.reset.stop_procedure_22()
            raise HardwareException("Выходное напряжение не соответствует заданию.\n"
                                    "Неисправность узла формирования напряжения в стенде")

    def start_procedure_24(self, coef_volt: float, setpoint_volt: float, factor: float = 1.0) -> float:
        """
        Включение контакта первичной обмотки, соответствующей напряжению U3[i]=U2[i]/Кс.
        Где U2[i] = напряжение, соответствующее i-ой уставке Сочетание контактов для напряжения U2[i]
        берем из файла «(Тор) TV1.xls»
        :param factor:
        :param coef_volt: float
        :param setpoint_volt: float
        :return: float
        """
        self.logger.debug("процедура 2.4")
        calc_volt = factor * setpoint_volt / coef_volt
        self.logger.debug(f"вычисленное U: {calc_volt:.2f}, коэффициент: {factor}")
        self.perv_obm.perv_obm_tv1(calc_volt)
        self.logger.debug("включение первичной обмотки")
        sleep(1)
        condition = self._subtest_meas_volt()
        self.logger.info(f"процедура 2.4: {calc_volt = :.2f}, {condition = }")
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
        min_volt = 4.768
        max_volt = 7.152
        self.ctrl_kl.ctrl_relay('KL60', True)
        self.logger.debug("включение KL60")
        sleep(3)
        meas_volt = self.ai_read.ai_read('AI0')
        self.logger.info(f"измеренное U: {min_volt = } <= {meas_volt = } <= {max_volt = }")
        if min_volt <= meas_volt <= max_volt:
            self.logger.debug(f"процедура 3.1 пройдена")
            return meas_volt
        else:
            self.logger.warning(f"процедура 3.1 не пройдена")
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
        self.ctrl_kl.ctrl_relay('KL54', True)
        sleep(3)
        min_volt = 41.232
        max_volt = 61.848
        meas_volt = self.ai_read.ai_read('AI0')
        self.logger.info(f'процедура 3.2 напряжение: {min_volt:.2f} <= {meas_volt:.2f} <= {max_volt:.2f}')
        if min_volt <= meas_volt <= max_volt:
            self.logger.debug(f"процедура 3.2 пройдена")
            coef_volt = meas_volt / 51.54
            return coef_volt
        else:
            self.logger.warning(f"процедура 3.2 не пройдена")
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
        meas_volt = self.ai_read.ai_read('AI0')
        self.logger.info(f'процедура 3.4 напряжение: {min_volt:.2f} <= {meas_volt:.2f} <= {max_volt:.2f}')
        if min_volt <= meas_volt <= max_volt:
            self.logger.debug(f"процедура 3.4 пройдена")
            return True
        else:
            self.logger.warning(f"процедура 3.4 не пройдена")
            self.reset.stop_procedure_3()
            return False

    def procedure_1_21_31(self) -> float:
        """
        1.1. Проверка вероятности наличия короткого замыкания на входе измерительной цепи блока.
        :return: float: напряжение
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
        :return: float: напряжение
        """
        if self.start_procedure_1():
            if self.start_procedure_21():
                meas_volt = self.start_procedure_31()
                if meas_volt != 0.0:
                    min_volt = coef_min * meas_volt
                    max_volt = coef_max * meas_volt
                    self.logger.info(f"изм. напряжение умноженное на {coef_min} и на {coef_max}: "
                                     f"{min_volt = }, {max_volt = }")
                    return min_volt, max_volt
        self.logger.warning('Неисправность узла формирования напряжения в стенде')
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
                    return coef_volt
        self.logger.warning('Неисправность узла формирования напряжения в стенде')
        raise HardwareException("Выходное напряжение не соответствует заданию.\n"
                                "Неисправность узла формирования напряжения в стенде")

    def procedure_1_24_34(self, coef_volt: float, setpoint_volt: float, factor: float = 1.0) -> bool:
        """
            выполняется последовательно процедура 1 --> 2.4 --> 3.4
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
        если происходит какая-то ошибка, выполняет те же процедуры с напряжением увеличенным в 1.1 раза.
        :param coef_volt:
        :param setpoint_volt:
        :return:
        """
        self.logger.debug("процедура \"procedure_x4_to_x5\", при неудачном выполнении процедур 1, 2.4, 3.4 "
                          "будут выполнены процедуры 1, 2.5, 3.5")
        if self.procedure_1_24_34(coef_volt=coef_volt, setpoint_volt=setpoint_volt, factor=1.0):
            return True
        else:
            self.reset.stop_procedure_3()
            if self.procedure_1_24_34(coef_volt=coef_volt, setpoint_volt=setpoint_volt, factor=1.1):
                return True
            else:
                self.logger.warning("Выходное напряжение не соответствует заданию.\n "
                                    "Неисправность узла формирования напряжения в стенде")
                raise HardwareException("Выходное напряжение не соответствует заданию.\n"
                                        "Неисправность узла формирования напряжения в стенде")

    def sbros_vtor_obm(self) -> bool:
        in_ai = self.ai_read.ai_read('AI0')
        if in_ai <= 1.1:
            return True
        if in_ai > 1.1:
            self.reset.sbros_vtor_obm()
            return True
        else:
            return False

    def _subtest_meas_volt(self) -> bool:
        """
        Функция измерения напряжения, после включения первичной обмотки.
        :return: bool
        """
        self.logger.debug("измерение U в процедуре 2.х")
        for i in range(3):
            meas_volt = self.ai_read.ai_read('AI0')
            self.logger.info(f"измерение U: {meas_volt:.2f}")
            if meas_volt <= 1.1:
                self.logger.debug("напряжение соответствует")
                return True
            elif meas_volt > 1.1:
                self.logger.warning("напряжение не соответствует")
                self.sbros_vtor_obm()
                self.logger.debug("сброс вторичной обмотки")
                self.logger.debug("повторение измерения")
                i += 1
                continue
            return False
