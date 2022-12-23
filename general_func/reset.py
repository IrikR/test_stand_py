#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Методы для управления реле, и сброса защит испытываемого блока.
"""

__all__ = ["ResetRelay", "ResetProtection"]

import logging

from time import sleep

from .modbus import CtrlKL


class ResetRelay:
    """
        Сбросы реле в различных вариациях в зависимости от алгоритма.
    """

    def __init__(self):
        self.ctrl_kl = CtrlKL()
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))

    def reset_all(self):
        self.logger.debug("отключение всех реле")
        self.ctrl_kl.ctrl_relay('KL1', False)
        self.ctrl_kl.ctrl_relay('KL2', False)
        self.ctrl_kl.ctrl_relay('KL3', False)
        self.ctrl_kl.ctrl_relay('KL4', False)
        self.ctrl_kl.ctrl_relay('KL5', False)
        self.ctrl_kl.ctrl_relay('KL6', False)
        self.ctrl_kl.ctrl_relay('KL7', False)
        self.ctrl_kl.ctrl_relay('KL8', False)
        self.ctrl_kl.ctrl_relay('KL9', False)
        self.ctrl_kl.ctrl_relay('KL10', False)
        self.ctrl_kl.ctrl_relay('KL11', False)
        self.ctrl_kl.ctrl_relay('KL12', False)
        self.ctrl_kl.ctrl_relay('KL13', False)
        self.ctrl_kl.ctrl_relay('KL14', False)
        self.ctrl_kl.ctrl_relay('KL15', False)
        self.ctrl_kl.ctrl_relay('KL16', False)
        self.ctrl_kl.ctrl_relay('KL17', False)
        self.ctrl_kl.ctrl_relay('KL18', False)
        self.ctrl_kl.ctrl_relay('KL19', False)
        self.ctrl_kl.ctrl_relay('KL20', False)
        self.ctrl_kl.ctrl_relay('KL21', False)
        self.ctrl_kl.ctrl_relay('KL22', False)
        self.ctrl_kl.ctrl_relay('KL23', False)
        self.ctrl_kl.ctrl_relay('KL24', False)
        self.ctrl_kl.ctrl_relay('KL25', False)
        self.ctrl_kl.ctrl_relay('KL26', False)
        self.ctrl_kl.ctrl_relay('KL27', False)
        self.ctrl_kl.ctrl_relay('KL28', False)
        self.ctrl_kl.ctrl_relay('KL29', False)
        self.ctrl_kl.ctrl_relay('KL30', False)
        self.ctrl_kl.ctrl_relay('KL31', False)
        self.ctrl_kl.ctrl_relay('KL32', False)
        self.ctrl_kl.ctrl_relay('KL33', False)
        # #
        self.ctrl_kl.ctrl_relay('KL36', False)
        self.ctrl_kl.ctrl_relay('KL37', False)
        self.sbros_perv_obm()
        self.sbros_vtor_obm()
        self.ctrl_kl.ctrl_relay('KL60', False)
        # #
        self.ctrl_kl.ctrl_relay('KL62', False)
        self.ctrl_kl.ctrl_relay('KL63', False)
        self.ctrl_kl.ctrl_relay('KL65', False)
        self.ctrl_kl.ctrl_relay('KL66', False)
        self.ctrl_kl.ctrl_relay('KL67', False)
        self.ctrl_kl.ctrl_relay('KL68', False)
        self.ctrl_kl.ctrl_relay('KL69', False)
        # #
        self.ctrl_kl.ctrl_relay('KL70', False)
        self.ctrl_kl.ctrl_relay('KL71', False)
        self.ctrl_kl.ctrl_relay('KL72', False)
        self.ctrl_kl.ctrl_relay('KL73', False)
        self.ctrl_kl.ctrl_relay('KL74', False)
        self.ctrl_kl.ctrl_relay('KL75', False)
        self.ctrl_kl.ctrl_relay('KL76', False)
        self.ctrl_kl.ctrl_relay('KL77', False)
        self.ctrl_kl.ctrl_relay('KL78', False)
        self.ctrl_kl.ctrl_relay('KL79', False)
        self.ctrl_kl.ctrl_relay('KL80', False)
        self.ctrl_kl.ctrl_relay('KL81', False)
        self.ctrl_kl.ctrl_relay('KL82', False)
        self.ctrl_kl.ctrl_relay('KL83', False)
        self.ctrl_kl.ctrl_relay('KL84', False)
        self.ctrl_kl.ctrl_relay('KL88', False)
        self.ctrl_kl.ctrl_relay('KL89', False)
        self.ctrl_kl.ctrl_relay('KL90', False)
        self.ctrl_kl.ctrl_relay('KL91', False)
        self.ctrl_kl.ctrl_relay('KL92', False)
        self.ctrl_kl.ctrl_relay('KL93', False)
        self.ctrl_kl.ctrl_relay('KL94', False)
        self.ctrl_kl.ctrl_relay('KL95', False)
        self.ctrl_kl.ctrl_relay('KL97', False)
        self.ctrl_kl.ctrl_relay('KL98', False)
        self.ctrl_kl.ctrl_relay('KL99', False)
        self.ctrl_kl.ctrl_relay('KL100', False)
        self.ctrl_kl.ctrl_relay('Q113_4', False)
        self.ctrl_kl.ctrl_relay('Q113_5', False)
        self.ctrl_kl.ctrl_relay('Q113_6', False)
        self.ctrl_kl.ctrl_relay('Q113_7', False)
        self.logger.debug("все реле отключены")

    def sbros_perv_obm(self):
        self.logger.debug("отключение реле первичной обмотки")
        self.ctrl_kl.ctrl_relay('KL38', False)
        self.ctrl_kl.ctrl_relay('KL39', False)
        self.ctrl_kl.ctrl_relay('KL40', False)
        self.ctrl_kl.ctrl_relay('KL41', False)
        self.ctrl_kl.ctrl_relay('KL42', False)
        self.ctrl_kl.ctrl_relay('KL43', False)
        self.ctrl_kl.ctrl_relay('KL44', False)
        self.ctrl_kl.ctrl_relay('KL45', False)
        self.ctrl_kl.ctrl_relay('KL46', False)
        self.ctrl_kl.ctrl_relay('KL47', False)

    def sbros_vtor_obm(self):
        self.logger.debug("отключение реле вторичной обмотки")
        self.ctrl_kl.ctrl_relay('KL48', False)
        self.ctrl_kl.ctrl_relay('KL49', False)
        self.ctrl_kl.ctrl_relay('KL50', False)
        self.ctrl_kl.ctrl_relay('KL51', False)
        self.ctrl_kl.ctrl_relay('KL52', False)
        self.ctrl_kl.ctrl_relay('KL53', False)
        self.ctrl_kl.ctrl_relay('KL54', False)
        self.ctrl_kl.ctrl_relay('KL55', False)
        self.ctrl_kl.ctrl_relay('KL56', False)
        self.ctrl_kl.ctrl_relay('KL57', False)
        self.ctrl_kl.ctrl_relay('KL58', False)
        self.ctrl_kl.ctrl_relay('KL59', False)
        self.ctrl_kl.ctrl_relay('KL60', False)
        self.logger.debug("реле вторичной обмотки отключены")

    def stop_procedure_1(self):
        self.logger.debug("отключение реле процедуры 1")
        self.ctrl_kl.ctrl_relay('KL62', False)
        self.ctrl_kl.ctrl_relay('KL37', False)

    def stop_procedure_21(self):
        self.stop_procedure_1()
        self.logger.debug("отключение реле процедуры 2.1")
        self.ctrl_kl.ctrl_relay('KL43', False)

    def stop_procedure_22(self):
        self.stop_procedure_1()
        self.logger.debug("отключение реле процедуры 2.2")
        self.ctrl_kl.ctrl_relay('KL44', False)

    def stop_procedure_2(self):
        self.stop_procedure_1()
        self.logger.debug("отключение реле процедуры 2")
        self.sbros_perv_obm()

    def stop_procedure_31(self):
        self.logger.debug("отключение реле процедуры 3.1")
        self.ctrl_kl.ctrl_relay('KL62', False)
        sleep(1)
        self.ctrl_kl.ctrl_relay('KL37', False)
        self.ctrl_kl.ctrl_relay('KL43', False)
        self.ctrl_kl.ctrl_relay('KL60', False)

    def stop_procedure_32(self):
        self.logger.debug("отключение реле процедуры 3.2")
        self.ctrl_kl.ctrl_relay('KL62', False)
        sleep(1)
        self.ctrl_kl.ctrl_relay('KL37', False)
        self.ctrl_kl.ctrl_relay('KL44', False)
        self.ctrl_kl.ctrl_relay('KL54', False)

    def stop_procedure_3(self):
        self.logger.debug("отключение реле процедуры 3")
        self.ctrl_kl.ctrl_relay('KL62', False)
        sleep(1)
        self.ctrl_kl.ctrl_relay('KL37', False)
        self.sbros_perv_obm()
        self.sbros_vtor_obm()

    def sbros_kl63_proc_1_21_31(self):
        """
        Используется для сброса после процедуры 1 -> 2.1 -> 3.1.
        :return:
        """
        self.ctrl_kl.ctrl_relay('KL63', False)
        self.logger.debug("отключение реле KL63")
        sleep(0.1)
        self.stop_procedure_31()

    def sbros_kl63_proc_1_22_32(self):
        """
        Используется для сброса после процедуры 1 -> 2.2 -> 3.2
        :return:
        """
        self.ctrl_kl.ctrl_relay('KL63', False)
        self.logger.debug("отключение реле KL63")
        sleep(0.1)
        self.stop_procedure_32()

    def sbros_kl63_proc_all(self):
        self.ctrl_kl.ctrl_relay('KL63', False)
        self.logger.debug("отключение реле KL63")
        sleep(0.1)
        self.stop_procedure_3()


class ResetProtection:
    """
    Сброс защиты испытуемого блока.
    """
    def __init__(self):
        self.ctrl_kl = CtrlKL()
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))

    def sbros_zashit_mtz5(self):
        self.logger.debug("сброс защит МТЗ-5, KL1 1.5сек")
        self.ctrl_kl.ctrl_relay('KL1', False)
        self.logger.debug("отключение KL1")
        sleep(1.5)
        self.ctrl_kl.ctrl_relay('KL1', True)
        self.logger.debug("включение KL1")
        sleep(2)
        self.logger.debug("таймаут 2сек, выполнен сброс защит")

    def sbros_zashit_kl1(self):
        self.logger.debug("сброс защит KL1 1.5сек")
        self.ctrl_kl.ctrl_relay('KL1', True)
        self.logger.debug('включение KL1')
        sleep(1.5)
        self.ctrl_kl.ctrl_relay('KL1', False)
        self.logger.debug('отключение KL1')
        sleep(2)
        self.logger.debug('таймаут 2сек, выполнен сброс защит')

    def sbros_zashit_kl30(self, *, time_on: float = 0.5, time_off: float = 0.5):
        self.logger.debug(f"сброс защит KL30, {time_on =}, {time_off =}")
        self.ctrl_kl.ctrl_relay('KL30', True)
        self.logger.debug('включение KL30')
        sleep(time_on)
        self.ctrl_kl.ctrl_relay('KL30', False)
        self.logger.debug('отключение KL30')
        sleep(time_off)
        self.logger.debug('таймаут, выполнен сброс защит')

    def sbros_testa_bp_0(self):
        """
        Сброс реле в алгоритме проверки БП (bp).
        Используется в тесте 2.0.
        :return:
        """
        self.logger.debug("отключение реле")
        self.ctrl_kl.ctrl_relay('KL77', False)
        sleep(0.1)
        self.ctrl_kl.ctrl_relay('KL65', False)
        sleep(0.1)
        self.ctrl_kl.ctrl_relay('KL76', False)
        self.ctrl_kl.ctrl_relay('KL66', False)
        self.ctrl_kl.ctrl_relay('KL78', False)
        self.logger.debug("отключены реле KL77, KL65, KL76, KL66, KL78")

    def sbros_testa_bp_1(self):
        """
        Сброс реле в алгоритме проверки БП (bp).
        Используется в тесте 4.0 и 3.0.
        :return:
        """
        self.sbros_testa_bp_0()
        self.ctrl_kl.ctrl_relay('KL75', False)
        self.logger.debug("отключены реле KL75")

    def sbros_zashit_ubtz(self):
        """
        Метод используется для сброса защит блока УБТЗ (ubtz).
        :return:
        """
        self.ctrl_kl.ctrl_relay('KL1', True)
        self.ctrl_kl.ctrl_relay('KL31', True)
        self.logger.debug("включены KL1, KL31")
        sleep(12)
        self.logger.info("таймаут 12 секунд")
        self.ctrl_kl.ctrl_relay('KL1', False)
        self.ctrl_kl.ctrl_relay('KL31', False)
        self.logger.debug("отключены KL1, KL31")

    def sbros_zashit_kl24(self):
        """
        Сброс защит блока через KL24.
        :return:
        """
        self.ctrl_kl.ctrl_relay('KL24', True)
        sleep(3)
        self.ctrl_kl.ctrl_relay('KL24', False)
