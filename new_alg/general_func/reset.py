#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Методы для управления реле, и сброса защит испытываемого блока.
"""

__all__ = ["ResetRelay", "ResetProtection"]

import logging

from time import sleep

from .wr_do_to_opc import CtrlKL
from .utils import CLILog


class ResetRelay(CtrlKL):
    """
        Сбросы реле в различных вариациях в зависимости от алгоритма.
    """

    def __init__(self):
        super().__init__()
        self.cli_log = CLILog("info", __name__)
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))

    def stop_procedure_1(self) -> None:
        self.logger.debug("отключение реле процедуры 1")
        self.cli_log.lev_info("отключение реле процедуры 1", "gray")
        self.ctrl_relay('KL62', False)
        self.ctrl_relay('KL37', False)

    def stop_procedure_21(self) -> None:
        self.stop_procedure_1()
        self.logger.debug("отключение реле процедуры 2.1")
        self.cli_log.lev_info("отключение реле процедуры 2.1", "gray")
        self.ctrl_relay('KL43', False)

    def stop_procedure_22(self) -> None:
        self.stop_procedure_1()
        self.logger.debug("отключение реле процедуры 2.2")
        self.cli_log.lev_info("отключение реле процедуры 2.2", "gray")
        self.ctrl_relay('KL44', False)

    def stop_procedure_2(self) -> None:
        self.stop_procedure_1()
        self.logger.debug("отключение реле процедуры 2")
        self.cli_log.lev_info("отключение реле процедуры 2", "gray")
        self.perv_obm_tv1_off()

    def stop_procedure_31(self) -> None:
        self.logger.debug("отключение реле процедуры 3.1")
        self.cli_log.lev_info("отключение реле процедуры 3.1", "gray")
        self.ctrl_relay('KL62', False)
        sleep(1)
        self.ctrl_relay('KL37', False)
        self.ctrl_relay('KL43', False)
        self.ctrl_relay('KL60', False)

    def stop_procedure_32(self) -> None:
        self.logger.debug("отключение реле процедуры 3.2")
        self.cli_log.lev_info("отключение реле процедуры 3.2", "gray")
        self.ctrl_relay('KL62', False)
        sleep(1)
        self.ctrl_relay('KL37', False)
        self.ctrl_relay('KL44', False)
        self.ctrl_relay('KL54', False)

    def stop_procedure_3(self) -> None:
        self.logger.debug("отключение реле процедуры 3")
        self.cli_log.lev_info("отключение реле процедуры 3", "gray")
        self.ctrl_relay('KL62', False)
        sleep(1)
        self.ctrl_relay('KL37', False)
        self.perv_obm_tv1_off()
        self.vtor_obm_tv1_off()

    def sbros_kl63_proc_1_21_31(self) -> None:
        """
        Используется для сброса после процедуры 1 -> 2.1 -> 3.1.
        :return:
        """
        self.ctrl_relay('KL63', False)
        self.logger.debug("отключение реле KL63")
        self.cli_log.lev_info("отключение реле KL63", "blue")
        sleep(0.1)
        self.stop_procedure_31()

    def sbros_kl63_proc_1_22_32(self) -> None:
        """
        Используется для сброса после процедуры 1 -> 2.2 -> 3.2
        :return:
        """
        self.ctrl_relay('KL63', False)
        self.logger.debug("отключение реле KL63")
        self.cli_log.lev_info("отключение реле KL63", "blue")
        sleep(0.1)
        self.stop_procedure_32()

    def sbros_kl63_proc_all(self) -> None:
        self.ctrl_relay('KL63', False)
        self.logger.debug("отключение реле KL63")
        self.cli_log.lev_info("отключение реле KL63", "blue")
        sleep(0.1)
        self.stop_procedure_3()


class ResetProtection(CtrlKL):
    """
    Сброс защиты испытуемого блока.
    """
    def __init__(self):
        super().__init__()
        self.cli_log = CLILog(True, __name__)
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))

    def sbros_zashit_mtz5(self) -> None:
        self.logger.debug("сброс защит МТЗ-5, KL1 1.5сек")
        self.cli_log.lev_info("сброс защит МТЗ-5, KL1 1.5сек", "gray")
        self.ctrl_relay('KL1', False)
        self.logger.debug("отключение KL1")
        self.cli_log.lev_info("отключение KL1", "blue")
        sleep(1.5)
        self.logger.debug("таймаут 1.5 сек, выполнен сброс защит")
        self.cli_log.lev_info("таймаут 1.5 сек, выполнен сброс защит", "gray")
        self.ctrl_relay('KL1', True)
        self.logger.debug("включение KL1")
        self.cli_log.lev_info("включение KL1", "blue")
        sleep(2)
        self.logger.debug("таймаут 2 сек, выполнен сброс защит")
        self.cli_log.lev_info("таймаут 2 сек, выполнен сброс защит", "gray")

    def sbros_zashit_kl1(self) -> None:
        self.logger.debug("сброс защит KL1 1.5сек")
        self.cli_log.lev_info("сброс защит KL1 1.5сек", "gray")
        self.ctrl_relay('KL1', True)
        self.logger.debug('включение KL1')
        self.cli_log.lev_info('включение KL1', "blue")
        sleep(1.5)
        self.logger.debug('таймаут 1.5 сек, выполнен сброс защит')
        self.cli_log.lev_info('таймаут 1.5 сек, выполнен сброс защит', "gray")
        self.ctrl_relay('KL1', False)
        self.logger.debug('отключение KL1')
        self.cli_log.lev_info('отключение KL1', "blue")
        sleep(2)
        self.logger.debug('таймаут 2 сек, выполнен сброс защит')
        self.cli_log.lev_info('таймаут 2 сек, выполнен сброс защит', "gray")

    def sbros_zashit_kl30(self, *, time_on: float = 0.5, time_off: float = 0.5) -> None:
        self.logger.debug(f"сброс защит KL30, {time_on =}, {time_off =}")
        self.cli_log.lev_info(f"сброс защит KL30, {time_on =}, {time_off =}", "gray")
        self.ctrl_relay('KL30', True)
        self.logger.debug('включение KL30')
        self.cli_log.lev_info('включение KL30', "blue")
        sleep(time_on)
        self.ctrl_relay('KL30', False)
        self.logger.debug('отключение KL30')
        self.cli_log.lev_info('отключение KL30', "blue")
        sleep(time_off)
        self.logger.debug('таймаут, выполнен сброс защит')
        self.cli_log.lev_info('таймаут, выполнен сброс защит', "gray")

    def sbros_testa_bp_0(self) -> None:
        """
        Сброс реле в алгоритме проверки БП (bp).
        Используется в тесте 2.0.
        :return:
        """
        self.logger.debug("отключение реле")
        self.cli_log.lev_info("отключение реле", "gray")
        self.ctrl_relay('KL77', False)
        sleep(0.1)
        self.ctrl_relay('KL65', False)
        sleep(0.1)
        self.ctrl_relay('KL76', False)
        self.ctrl_relay('KL66', False)
        self.ctrl_relay('KL78', False)
        self.logger.debug("отключены реле KL77, KL65, KL76, KL66, KL78")
        self.cli_log.lev_info("отключены реле KL77, KL65, KL76, KL66, KL78", "blue")

    def sbros_testa_bp_1(self) -> None:
        """
        Сброс реле в алгоритме проверки БП (bp).
        Используется в тесте 4.0 и 3.0.
        :return:
        """
        self.sbros_testa_bp_0()
        self.ctrl_relay('KL75', False)
        self.logger.debug("отключены реле KL75")
        self.cli_log.lev_info("отключены реле KL75", "blue")

    def sbros_zashit_ubtz(self) -> None:
        """
        Метод используется для сброса защит блока УБТЗ (ubtz).
        :return:
        """
        self.ctrl_relay('KL1', True)
        self.ctrl_relay('KL31', True)
        self.logger.debug("включены KL1, KL31")
        self.cli_log.lev_info("включены KL1, KL31", "blue")
        sleep(12)
        self.logger.info("таймаут 12 секунд")
        self.cli_log.lev_info("таймаут 12 секунд", "gray")
        self.ctrl_relay('KL1', False)
        self.ctrl_relay('KL31', False)
        self.logger.debug("отключены KL1, KL31")
        self.cli_log.lev_info("отключены KL1, KL31", "blue")

    def sbros_zashit_kl24(self) -> None:
        """
        Сброс защит блока через KL24.
        :return:
        """
        self.logger.debug("Сброс защит блока через KL24")
        self.cli_log.lev_info("Сброс защит блока через KL24", "gray")
        self.ctrl_relay('KL24', True)
        self.logger.debug("включение реле KL24")
        self.cli_log.lev_info("включение реле KL24", "blue")
        sleep(3)
        self.logger.debug("таймаут 3 секунды")
        self.cli_log.lev_info("таймаут 3 секунды", "gray")
        self.ctrl_relay('KL24', False)
        self.logger.debug("отключение реле KL24")
        self.cli_log.lev_info("отключение реле KL24", "blue")
