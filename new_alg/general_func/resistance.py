#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Методы для управления реле которые воздействуют на сопротивления.
"""

__all__ = ["Resistor"]

import logging

from .utils import CLILog
from .opc_full import ConnectOPC


class Resistor:
    """
        R1		1,2	    Ом	KL3
        R2		2,1	    Ом	KL4
        R3		3,4	    Ом	KL5
        R4		6,9	    Ом	KL6
        R5		15	    Ом	KL7
        R6		29,1	Ом	KL8
        R7		61,3	Ом	KL9
        R8		127,6	Ом	KL10
        R9		46,3	Ом	KL1
        R10		3,9	    кОм	KL13
        R11		4,24	кОм	KL14
        R12		8,82	кОм	KL15
        R13		17,48	кОм	KL16
        R14		35,2	кОм	KL17
        R15		75	    кОм	KL18
        R16		150	    кОм	KL19
        R17		295,5	кОм	KL20
        R18		183,3	кОм
    """

    def __init__(self):
        self.conn_opc = ConnectOPC()
        self.cli_log = CLILog("info", __name__)
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))

    def resist_ohm(self, ohm: int) -> None:

        if ohm == 0:
            self.conn_opc.ctrl_relay('KL3', True)
            self.conn_opc.ctrl_relay('KL4', True)
            self.conn_opc.ctrl_relay('KL5', True)
            self.conn_opc.ctrl_relay('KL6', True)
            self.conn_opc.ctrl_relay('KL7', True)
            self.conn_opc.ctrl_relay('KL8', True)
            self.conn_opc.ctrl_relay('KL9', True)
            self.conn_opc.ctrl_relay('KL10', True)
            self.logger.debug("включено 0 ом")
            self.cli_log.lev_info("включено 0 ом", "blue")
        elif ohm == 10:
            self.conn_opc.ctrl_relay('KL3', False)
            self.conn_opc.ctrl_relay('KL4', False)
            self.conn_opc.ctrl_relay('KL5', True)
            self.conn_opc.ctrl_relay('KL6', False)
            self.conn_opc.ctrl_relay('KL7', True)
            self.conn_opc.ctrl_relay('KL8', True)
            self.conn_opc.ctrl_relay('KL9', True)
            self.conn_opc.ctrl_relay('KL10', True)
            self.logger.debug("включено 10 ом")
            self.cli_log.lev_info("включено 10 ом", "blue")
        elif ohm == 15:
            self.conn_opc.ctrl_relay('KL3', True)
            self.conn_opc.ctrl_relay('KL4', True)
            self.conn_opc.ctrl_relay('KL5', True)
            self.conn_opc.ctrl_relay('KL6', True)
            self.conn_opc.ctrl_relay('KL7', False)
            self.conn_opc.ctrl_relay('KL8', True)
            self.conn_opc.ctrl_relay('KL9', True)
            self.conn_opc.ctrl_relay('KL10', True)
            self.logger.debug("включено 15 ом")
            self.cli_log.lev_info("включено 15 ом", "blue")
        elif ohm == 20:
            self.conn_opc.ctrl_relay('KL3', True)
            self.conn_opc.ctrl_relay('KL4', False)
            self.conn_opc.ctrl_relay('KL5', False)
            self.conn_opc.ctrl_relay('KL6', True)
            self.conn_opc.ctrl_relay('KL7', False)
            self.conn_opc.ctrl_relay('KL8', True)
            self.conn_opc.ctrl_relay('KL9', True)
            self.conn_opc.ctrl_relay('KL10', True)
            self.logger.debug("включено 20 ом")
            self.cli_log.lev_info("включено 20 ом", "blue")
        elif ohm == 35:
            self.conn_opc.ctrl_relay('KL3', False)
            self.conn_opc.ctrl_relay('KL4', False)
            self.conn_opc.ctrl_relay('KL5', False)
            self.conn_opc.ctrl_relay('KL6', True)
            self.conn_opc.ctrl_relay('KL7', True)
            self.conn_opc.ctrl_relay('KL8', False)
            self.conn_opc.ctrl_relay('KL9', True)
            self.conn_opc.ctrl_relay('KL10', True)
            self.logger.debug("включено 35 ом")
            self.cli_log.lev_info("включено 35 ом", "blue")
        elif ohm == 46:
            self.conn_opc.ctrl_relay('KL3', True)
            self.conn_opc.ctrl_relay('KL4', False)
            self.conn_opc.ctrl_relay('KL5', True)
            self.conn_opc.ctrl_relay('KL6', True)
            self.conn_opc.ctrl_relay('KL7', False)
            self.conn_opc.ctrl_relay('KL8', False)
            self.conn_opc.ctrl_relay('KL9', True)
            self.conn_opc.ctrl_relay('KL10', True)
            self.logger.debug("включено 46 ом")
            self.cli_log.lev_info("включено 46 ом", "blue")
        elif ohm == 50:
            self.conn_opc.ctrl_relay('KL3', False)
            self.conn_opc.ctrl_relay('KL4', False)
            self.conn_opc.ctrl_relay('KL5', False)
            self.conn_opc.ctrl_relay('KL6', True)
            self.conn_opc.ctrl_relay('KL7', False)
            self.conn_opc.ctrl_relay('KL8', False)
            self.conn_opc.ctrl_relay('KL9', True)
            self.conn_opc.ctrl_relay('KL10', True)
            self.logger.debug("включено 50 ом")
            self.cli_log.lev_info("включено 50 ом", "blue")
        elif ohm == 100:
            self.conn_opc.ctrl_relay('KL3', True)
            self.conn_opc.ctrl_relay('KL4', True)
            self.conn_opc.ctrl_relay('KL5', False)
            self.conn_opc.ctrl_relay('KL6', False)
            self.conn_opc.ctrl_relay('KL7', True)
            self.conn_opc.ctrl_relay('KL8', False)
            self.conn_opc.ctrl_relay('KL9', False)
            self.conn_opc.ctrl_relay('KL10', True)
            self.logger.debug("включено 100 ом")
            self.cli_log.lev_info("включено 100 ом", "blue")
        elif ohm == 110:
            self.conn_opc.ctrl_relay('KL3', False)
            self.conn_opc.ctrl_relay('KL4', True)
            self.conn_opc.ctrl_relay('KL5', False)
            self.conn_opc.ctrl_relay('KL6', True)
            self.conn_opc.ctrl_relay('KL7', False)
            self.conn_opc.ctrl_relay('KL8', False)
            self.conn_opc.ctrl_relay('KL9', False)
            self.conn_opc.ctrl_relay('KL10', True)
            self.logger.debug("включено 110 ом")
            self.cli_log.lev_info("включено 110 ом", "blue")
        elif ohm == 150:
            self.conn_opc.ctrl_relay('KL3', False)
            self.conn_opc.ctrl_relay('KL4', True)
            self.conn_opc.ctrl_relay('KL5', True)
            self.conn_opc.ctrl_relay('KL6', False)
            self.conn_opc.ctrl_relay('KL7', False)
            self.conn_opc.ctrl_relay('KL8', True)
            self.conn_opc.ctrl_relay('KL9', True)
            self.conn_opc.ctrl_relay('KL10', False)
            self.logger.debug("включено 150 ом")
            self.cli_log.lev_info("включено 150 ом", "blue")
        elif ohm == 255:
            self.conn_opc.ctrl_relay('KL3', False)
            self.conn_opc.ctrl_relay('KL4', False)
            self.conn_opc.ctrl_relay('KL5', False)
            self.conn_opc.ctrl_relay('KL6', False)
            self.conn_opc.ctrl_relay('KL7', False)
            self.conn_opc.ctrl_relay('KL8', False)
            self.conn_opc.ctrl_relay('KL9', False)
            self.conn_opc.ctrl_relay('KL10', False)
            self.logger.debug("включено 255 ом")
            self.cli_log.lev_info("включено 255 ом", "blue")

    def resist_kohm(self, kohm: int) -> None:

        if kohm == 0:
            self.conn_opc.ctrl_relay('KL13', True)
            self.conn_opc.ctrl_relay('KL14', True)
            self.conn_opc.ctrl_relay('KL15', True)
            self.conn_opc.ctrl_relay('KL16', True)
            self.conn_opc.ctrl_relay('KL17', True)
            self.conn_opc.ctrl_relay('KL18', True)
            self.conn_opc.ctrl_relay('KL19', True)
            self.conn_opc.ctrl_relay('KL20', True)
            self.logger.debug("включено 0 ком")
            self.cli_log.lev_info("включено 0 ком", "blue")
        if kohm == 12:
            self.conn_opc.ctrl_relay('KL13', False)
            self.conn_opc.ctrl_relay('KL14', True)
            self.conn_opc.ctrl_relay('KL15', False)
            self.conn_opc.ctrl_relay('KL16', True)
            self.conn_opc.ctrl_relay('KL17', True)
            self.conn_opc.ctrl_relay('KL18', True)
            self.conn_opc.ctrl_relay('KL19', True)
            self.conn_opc.ctrl_relay('KL20', True)
            self.logger.debug("включено 12 ком")
            self.cli_log.lev_info("включено 12 ком", "blue")
        if kohm == 21:
            self.conn_opc.ctrl_relay('KL13', True)
            self.conn_opc.ctrl_relay('KL14', False)
            self.conn_opc.ctrl_relay('KL15', True)
            self.conn_opc.ctrl_relay('KL16', False)
            self.conn_opc.ctrl_relay('KL17', True)
            self.conn_opc.ctrl_relay('KL18', True)
            self.conn_opc.ctrl_relay('KL19', True)
            self.conn_opc.ctrl_relay('KL20', True)
            self.logger.debug("включено 21 ком")
            self.cli_log.lev_info("включено 21 ком", "blue")
        elif kohm == 26:
            self.conn_opc.ctrl_relay('KL13', True)
            self.conn_opc.ctrl_relay('KL14', True)
            self.conn_opc.ctrl_relay('KL15', False)
            self.conn_opc.ctrl_relay('KL16', False)
            self.conn_opc.ctrl_relay('KL17', True)
            self.conn_opc.ctrl_relay('KL18', True)
            self.conn_opc.ctrl_relay('KL19', True)
            self.conn_opc.ctrl_relay('KL20', True)
            self.logger.debug("включено 26 ком")
            self.cli_log.lev_info("включено 26 ком", "blue")
        elif kohm == 30:
            self.conn_opc.ctrl_relay('KL13', False)
            self.conn_opc.ctrl_relay('KL14', True)
            self.conn_opc.ctrl_relay('KL15', False)
            self.conn_opc.ctrl_relay('KL16', False)
            self.conn_opc.ctrl_relay('KL17', True)
            self.conn_opc.ctrl_relay('KL18', True)
            self.conn_opc.ctrl_relay('KL19', True)
            self.conn_opc.ctrl_relay('KL20', True)
            self.logger.debug("включено 30 ком")
            self.cli_log.lev_info("включено 30 ком", "blue")
        elif kohm == 61:
            self.conn_opc.ctrl_relay('KL13', True)
            self.conn_opc.ctrl_relay('KL14', True)
            self.conn_opc.ctrl_relay('KL15', False)
            self.conn_opc.ctrl_relay('KL16', False)
            self.conn_opc.ctrl_relay('KL17', False)
            self.conn_opc.ctrl_relay('KL18', True)
            self.conn_opc.ctrl_relay('KL19', True)
            self.conn_opc.ctrl_relay('KL20', True)
            self.logger.debug("включено 61 ком")
            self.cli_log.lev_info("включено 61 ком", "blue")
        elif kohm == 65:
            self.conn_opc.ctrl_relay('KL13', True)
            self.conn_opc.ctrl_relay('KL14', False)
            self.conn_opc.ctrl_relay('KL15', False)
            self.conn_opc.ctrl_relay('KL16', False)
            self.conn_opc.ctrl_relay('KL17', False)
            self.conn_opc.ctrl_relay('KL18', True)
            self.conn_opc.ctrl_relay('KL19', True)
            self.conn_opc.ctrl_relay('KL20', True)
            self.logger.debug("включено 65 ком")
            self.cli_log.lev_info("включено 65 ком", "blue")
        elif kohm == 100:
            self.conn_opc.ctrl_relay('KL13', False)
            self.conn_opc.ctrl_relay('KL14', False)
            self.conn_opc.ctrl_relay('KL15', True)
            self.conn_opc.ctrl_relay('KL16', False)
            self.conn_opc.ctrl_relay('KL17', True)
            self.conn_opc.ctrl_relay('KL18', False)
            self.conn_opc.ctrl_relay('KL19', True)
            self.conn_opc.ctrl_relay('KL20', True)
            self.logger.debug("включено 100 ком")
            self.cli_log.lev_info("включено 100 ком", "blue")
        elif kohm == 200:
            self.conn_opc.ctrl_relay('KL13', False)
            self.conn_opc.ctrl_relay('KL14', False)
            self.conn_opc.ctrl_relay('KL15', False)
            self.conn_opc.ctrl_relay('KL16', True)
            self.conn_opc.ctrl_relay('KL17', False)
            self.conn_opc.ctrl_relay('KL18', True)
            self.conn_opc.ctrl_relay('KL19', False)
            self.conn_opc.ctrl_relay('KL20', True)
            self.logger.debug("включено 200 ком")
            self.cli_log.lev_info("включено 200 ком", "blue")
        elif kohm == 220:
            self.conn_opc.ctrl_relay('KL13', False)
            self.conn_opc.ctrl_relay('KL14', False)
            self.conn_opc.ctrl_relay('KL15', False)
            self.conn_opc.ctrl_relay('KL16', False)
            self.conn_opc.ctrl_relay('KL17', False)
            self.conn_opc.ctrl_relay('KL18', True)
            self.conn_opc.ctrl_relay('KL19', False)
            self.conn_opc.ctrl_relay('KL20', True)
            self.logger.debug("включено 220 ком")
            self.cli_log.lev_info("включено 220 ком", "blue")
        elif kohm == 590:
            self.conn_opc.ctrl_relay('KL13', False)
            self.conn_opc.ctrl_relay('KL14', False)
            self.conn_opc.ctrl_relay('KL15', False)
            self.conn_opc.ctrl_relay('KL16', False)
            self.conn_opc.ctrl_relay('KL17', False)
            self.conn_opc.ctrl_relay('KL18', False)
            self.conn_opc.ctrl_relay('KL19', False)
            self.conn_opc.ctrl_relay('KL20', False)
            self.logger.debug("включено 590 ком")
            self.cli_log.lev_info("включено 590 ком", "blue")

    def resist_10_to_20_ohm(self) -> None:
        self.conn_opc.ctrl_relay('KL3', True)
        self.conn_opc.ctrl_relay('KL6', True)
        self.conn_opc.ctrl_relay('KL8', True)
        self.conn_opc.ctrl_relay('KL9', True)
        self.conn_opc.ctrl_relay('KL10', True)
        self.logger.debug("переключение с 10 ом на 20 ом")
        self.cli_log.lev_info("переключение с 10 ом на 20 ом", "blue")

    def resist_10_to_35_ohm(self) -> None:
        self.conn_opc.ctrl_relay('KL5', False)
        self.conn_opc.ctrl_relay('KL6', True)
        self.conn_opc.ctrl_relay('KL8', False)
        self.logger.debug("переключение с 10 ом на 35 ом")
        self.cli_log.lev_info("переключение с 10 ом на 35 ом", "blue")

    def resist_10_to_100_ohm(self) -> None:
        self.conn_opc.ctrl_relay('KL9', False)
        self.conn_opc.ctrl_relay('KL8', False)
        self.logger.debug("переключение с 10 ом на 100 ом")
        self.cli_log.lev_info("переключение с 10 ом на 100 ом", "blue")

    def resist_10_to_46_ohm(self) -> None:
        self.conn_opc.ctrl_relay('KL7', False)
        self.conn_opc.ctrl_relay('KL6', True)
        self.conn_opc.ctrl_relay('KL8', False)
        self.logger.debug("переключение с 10 ом на 46 ом")
        self.cli_log.lev_info("переключение с 10 ом на 46 ом", "blue")

    def resist_10_to_50_ohm(self) -> None:
        self.conn_opc.ctrl_relay('KL7', False)
        self.conn_opc.ctrl_relay('KL5', False)
        self.conn_opc.ctrl_relay('KL6', True)
        self.conn_opc.ctrl_relay('KL8', False)
        self.logger.debug("переключение с 10 ом на 50 ом")
        self.cli_log.lev_info("переключение с 10 ом на 50 ом", "blue")

    def resist_10_to_110_ohm(self) -> None:
        self.conn_opc.ctrl_relay('KL9', False)
        self.conn_opc.ctrl_relay('KL4', True)
        self.conn_opc.ctrl_relay('KL5', False)
        self.conn_opc.ctrl_relay('KL8', False)
        self.conn_opc.ctrl_relay('KL6', True)
        self.conn_opc.ctrl_relay('KL7', False)
        self.logger.debug("переключение с 10 ом на 110 ом")
        self.cli_log.lev_info("переключение с 10 ом на 110 ом", "blue")

    def resist_35_to_110_ohm(self) -> None:
        self.conn_opc.ctrl_relay('KL9', False)
        self.conn_opc.ctrl_relay('KL7', False)
        self.logger.debug("переключение с 35 ом на 110 ом")
        self.cli_log.lev_info("переключение с 35 ом на 110 ом", "blue")

    def resist_10_to_137_ohm(self) -> None:
        self.conn_opc.ctrl_relay('KL10', False)
        self.logger.debug("переключение с 10 ом на 137 ом")
        self.cli_log.lev_info("переключение с 10 ом на 137 ом", "blue")

    def resist_0_to_50_ohm(self) -> None:
        self.conn_opc.ctrl_relay('KL3', False)
        self.conn_opc.ctrl_relay('KL4', False)
        self.conn_opc.ctrl_relay('KL5', False)
        self.conn_opc.ctrl_relay('KL7', False)
        self.conn_opc.ctrl_relay('KL8', False)
        self.logger.debug("переключение с 0 ом на 50 ом")
        self.cli_log.lev_info("переключение с 0 ом на 50 ом", "blue")

    def resist_0_to_100_ohm(self) -> None:
        self.conn_opc.ctrl_relay('KL5', False)
        self.conn_opc.ctrl_relay('KL6', False)
        self.conn_opc.ctrl_relay('KL8', False)
        self.conn_opc.ctrl_relay('KL9', False)
        self.logger.debug("переключение с 0 ом на 100 ом")
        self.cli_log.lev_info("переключение с 0 ом на 100 ом", "blue")

    def resist_0_to_63_ohm(self) -> None:
        self.conn_opc.ctrl_relay('KL9', False)
        self.conn_opc.ctrl_relay('KL4', False)
        self.logger.debug("переключение с 0 ом на 63 ом")
        self.cli_log.lev_info("переключение с 0 ом на 63 ом", "blue")

    def resist_220_to_100_kohm(self) -> None:
        self.conn_opc.ctrl_relay('KL18', False)
        self.conn_opc.ctrl_relay('KL19', True)
        self.conn_opc.ctrl_relay('KL17', True)
        self.conn_opc.ctrl_relay('KL15', True)
        self.logger.debug("переключение с 220 ком на 100 ком")
        self.cli_log.lev_info("переключение с 220 ком на 100 ком", "blue")
