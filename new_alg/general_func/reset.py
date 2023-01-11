#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Методы для управления реле, и сброса защит испытываемого блока.
"""

__all__ = ["ResetRelay", "ResetProtection"]

import logging

from time import sleep

from .modbus import CtrlKL
from .utils import CLILog


class ResetRelay:
    """
        Сбросы реле в различных вариациях в зависимости от алгоритма.
    """

    def __init__(self):
        self.ctrl_kl = CtrlKL()
        self.cli_log = CLILog(True, __name__)
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))

    def reset_all(self) -> None:
        self.logger.debug("отключение всех реле")
        self.cli_log.log_msg("отключение всех реле", "gray")
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
        self.cli_log.log_msg("все реле отключены", "gray")

    def sbros_perv_obm(self) -> None:
        self.logger.debug("отключение реле первичной обмотки")
        self.cli_log.log_msg("отключение реле первичной обмотки", "gray")
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
        self.logger.debug("реле первичной обмотки отключены")
        self.cli_log.log_msg("реле первичной обмотки отключены", "gray")

    def sbros_vtor_obm(self) -> None:
        self.logger.debug("отключение реле вторичной обмотки")
        self.cli_log.log_msg("отключение реле вторичной обмотки", "gray")
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
        self.cli_log.log_msg("реле вторичной обмотки отключены", "gray")

    def stop_procedure_1(self) -> None:
        self.logger.debug("отключение реле процедуры 1")
        self.cli_log.log_msg("отключение реле процедуры 1", "gray")
        self.ctrl_kl.ctrl_relay('KL62', False)
        self.ctrl_kl.ctrl_relay('KL37', False)

    def stop_procedure_21(self) -> None:
        self.stop_procedure_1()
        self.logger.debug("отключение реле процедуры 2.1")
        self.cli_log.log_msg("отключение реле процедуры 2.1", "gray")
        self.ctrl_kl.ctrl_relay('KL43', False)

    def stop_procedure_22(self) -> None:
        self.stop_procedure_1()
        self.logger.debug("отключение реле процедуры 2.2")
        self.cli_log.log_msg("отключение реле процедуры 2.2", "gray")
        self.ctrl_kl.ctrl_relay('KL44', False)

    def stop_procedure_2(self) -> None:
        self.stop_procedure_1()
        self.logger.debug("отключение реле процедуры 2")
        self.cli_log.log_msg("отключение реле процедуры 2", "gray")
        self.sbros_perv_obm()

    def stop_procedure_31(self) -> None:
        self.logger.debug("отключение реле процедуры 3.1")
        self.cli_log.log_msg("отключение реле процедуры 3.1", "gray")
        self.ctrl_kl.ctrl_relay('KL62', False)
        sleep(1)
        self.ctrl_kl.ctrl_relay('KL37', False)
        self.ctrl_kl.ctrl_relay('KL43', False)
        self.ctrl_kl.ctrl_relay('KL60', False)

    def stop_procedure_32(self) -> None:
        self.logger.debug("отключение реле процедуры 3.2")
        self.cli_log.log_msg("отключение реле процедуры 3.2", "gray")
        self.ctrl_kl.ctrl_relay('KL62', False)
        sleep(1)
        self.ctrl_kl.ctrl_relay('KL37', False)
        self.ctrl_kl.ctrl_relay('KL44', False)
        self.ctrl_kl.ctrl_relay('KL54', False)

    def stop_procedure_3(self) -> None:
        self.logger.debug("отключение реле процедуры 3")
        self.cli_log.log_msg("отключение реле процедуры 3", "gray")
        self.ctrl_kl.ctrl_relay('KL62', False)
        sleep(1)
        self.ctrl_kl.ctrl_relay('KL37', False)
        self.sbros_perv_obm()
        self.sbros_vtor_obm()

    def sbros_kl63_proc_1_21_31(self) -> None:
        """
        Используется для сброса после процедуры 1 -> 2.1 -> 3.1.
        :return:
        """
        self.ctrl_kl.ctrl_relay('KL63', False)
        self.logger.debug("отключение реле KL63")
        self.cli_log.log_msg("отключение реле KL63", "blue")
        sleep(0.1)
        self.stop_procedure_31()

    def sbros_kl63_proc_1_22_32(self) -> None:
        """
        Используется для сброса после процедуры 1 -> 2.2 -> 3.2
        :return:
        """
        self.ctrl_kl.ctrl_relay('KL63', False)
        self.logger.debug("отключение реле KL63")
        self.cli_log.log_msg("отключение реле KL63", "blue")
        sleep(0.1)
        self.stop_procedure_32()

    def sbros_kl63_proc_all(self) -> None:
        self.ctrl_kl.ctrl_relay('KL63', False)
        self.logger.debug("отключение реле KL63")
        self.cli_log.log_msg("отключение реле KL63", "blue")
        sleep(0.1)
        self.stop_procedure_3()


class ResetProtection:
    """
    Сброс защиты испытуемого блока.
    """
    def __init__(self):
        self.ctrl_kl = CtrlKL()
        self.cli_log = CLILog(True, __name__)
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))

    def sbros_zashit_mtz5(self) -> None:
        self.logger.debug("сброс защит МТЗ-5, KL1 1.5сек")
        self.cli_log.log_msg("сброс защит МТЗ-5, KL1 1.5сек", "gray")
        self.ctrl_kl.ctrl_relay('KL1', False)
        self.logger.debug("отключение KL1")
        self.cli_log.log_msg("отключение KL1", "blue")
        sleep(1.5)
        self.logger.debug("таймаут 1.5 сек, выполнен сброс защит")
        self.cli_log.log_msg("таймаут 1.5 сек, выполнен сброс защит", "gray")
        self.ctrl_kl.ctrl_relay('KL1', True)
        self.logger.debug("включение KL1")
        self.cli_log.log_msg("включение KL1", "blue")
        sleep(2)
        self.logger.debug("таймаут 2 сек, выполнен сброс защит")
        self.cli_log.log_msg("таймаут 2 сек, выполнен сброс защит", "gray")

    def sbros_zashit_kl1(self) -> None:
        self.logger.debug("сброс защит KL1 1.5сек")
        self.cli_log.log_msg("сброс защит KL1 1.5сек", "gray")
        self.ctrl_kl.ctrl_relay('KL1', True)
        self.logger.debug('включение KL1')
        self.cli_log.log_msg('включение KL1', "blue")
        sleep(1.5)
        self.logger.debug('таймаут 1.5 сек, выполнен сброс защит')
        self.cli_log.log_msg('таймаут 1.5 сек, выполнен сброс защит', "gray")
        self.ctrl_kl.ctrl_relay('KL1', False)
        self.logger.debug('отключение KL1')
        self.cli_log.log_msg('отключение KL1', "blue")
        sleep(2)
        self.logger.debug('таймаут 2 сек, выполнен сброс защит')
        self.cli_log.log_msg('таймаут 2 сек, выполнен сброс защит', "gray")

    def sbros_zashit_kl30(self, *, time_on: float = 0.5, time_off: float = 0.5) -> None:
        self.logger.debug(f"сброс защит KL30, {time_on =}, {time_off =}")
        self.cli_log.log_msg(f"сброс защит KL30, {time_on =}, {time_off =}", "gray")
        self.ctrl_kl.ctrl_relay('KL30', True)
        self.logger.debug('включение KL30')
        self.cli_log.log_msg('включение KL30', "blue")
        sleep(time_on)
        self.ctrl_kl.ctrl_relay('KL30', False)
        self.logger.debug('отключение KL30')
        self.cli_log.log_msg('отключение KL30', "blue")
        sleep(time_off)
        self.logger.debug('таймаут, выполнен сброс защит')
        self.cli_log.log_msg('таймаут, выполнен сброс защит', "gray")

    def sbros_testa_bp_0(self) -> None:
        """
        Сброс реле в алгоритме проверки БП (bp).
        Используется в тесте 2.0.
        :return:
        """
        self.logger.debug("отключение реле")
        self.cli_log.log_msg("отключение реле", "gray")
        self.ctrl_kl.ctrl_relay('KL77', False)
        sleep(0.1)
        self.ctrl_kl.ctrl_relay('KL65', False)
        sleep(0.1)
        self.ctrl_kl.ctrl_relay('KL76', False)
        self.ctrl_kl.ctrl_relay('KL66', False)
        self.ctrl_kl.ctrl_relay('KL78', False)
        self.logger.debug("отключены реле KL77, KL65, KL76, KL66, KL78")
        self.cli_log.log_msg("отключены реле KL77, KL65, KL76, KL66, KL78", "blue")

    def sbros_testa_bp_1(self) -> None:
        """
        Сброс реле в алгоритме проверки БП (bp).
        Используется в тесте 4.0 и 3.0.
        :return:
        """
        self.sbros_testa_bp_0()
        self.ctrl_kl.ctrl_relay('KL75', False)
        self.logger.debug("отключены реле KL75")
        self.cli_log.log_msg("отключены реле KL75", "blue")

    def sbros_zashit_ubtz(self) -> None:
        """
        Метод используется для сброса защит блока УБТЗ (ubtz).
        :return:
        """
        self.ctrl_kl.ctrl_relay('KL1', True)
        self.ctrl_kl.ctrl_relay('KL31', True)
        self.logger.debug("включены KL1, KL31")
        self.cli_log.log_msg("включены KL1, KL31", "blue")
        sleep(12)
        self.logger.info("таймаут 12 секунд")
        self.cli_log.log_msg("таймаут 12 секунд", "gray")
        self.ctrl_kl.ctrl_relay('KL1', False)
        self.ctrl_kl.ctrl_relay('KL31', False)
        self.logger.debug("отключены KL1, KL31")
        self.cli_log.log_msg("отключены KL1, KL31", "blue")

    def sbros_zashit_kl24(self) -> None:
        """
        Сброс защит блока через KL24.
        :return:
        """
        self.logger.debug("Сброс защит блока через KL24")
        self.cli_log.log_msg("Сброс защит блока через KL24", "gray")
        self.ctrl_kl.ctrl_relay('KL24', True)
        self.logger.debug("включение реле KL24")
        self.cli_log.log_msg("включение реле KL24", "blue")
        sleep(3)
        self.logger.debug("таймаут 3 секунды")
        self.cli_log.log_msg("таймаут 3 секунды", "gray")
        self.ctrl_kl.ctrl_relay('KL24', False)
        self.logger.debug("отключение реле KL24")
        self.cli_log.log_msg("отключение реле KL24", "blue")
