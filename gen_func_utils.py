#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ctypes
import logging

from time import time, sleep

from my_msgbox import *
from gen_mb_client import *

__all__ = ["Bug", "ResetRelay", "Resistor", "DeltaTimeNoneKL63", "ModbusConnectException", "HardwareException",
           "ResultMsg"]


class DeltaTimeNoneKL63(object):
    """
        расчет дельты времени переключения выходов блока
        Сброс или запоминание состояние таймера текущего времени CPU T0[i], сек
        KL63 - ВКЛ	DQ5:1B - ВКЛ
        Запуск таймера происходит по условию замыкания DI.b1 (контакт реле KL63)
        Остановка таймера происходит по условию размыкания DI.a6 T1[i]

    """
    def __init__(self):
        self.ctrl_kl = CtrlKL()
        self.read_mb = ReadMB()
        self.logger = logging.getLogger(__name__)

    def calc_dt(self):
        self.ctrl_kl.ctrl_relay('KL63', True)
        in_b1 = self.__inputs_b1()
        while in_b1 is False:
            in_b1 = self.__inputs_b1()
        start_timer = time()
        in_ax = self.__inputs_a6()
        while in_ax is True:
            in_ax = self.__inputs_a6()
        stop_timer = time()
        delta_t_calc = stop_timer - start_timer
        return delta_t_calc

    def __inputs_a6(self):
        in_a6 = self.read_mb.read_discrete(6)
        return in_a6

    def __inputs_b1(self):
        in_b1 = self.read_mb.read_discrete(9)
        return in_b1


class Bug(object):
    """
        Вывод сообщений в консоль, с цветовой дифференциацией штанов
    """
    def __init__(self, dbg=None):
        self.dbg = dbg
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

    def debug_msg(self, *args):
        """
        :param args: 1 or red, 2 or orange, 3 or blue, 4 or green, 5 or purple
        :return: string
        """

        if self.dbg is True:
            msg, lev = args
            if lev == 1 or lev == 'red':
                # красный Red
                print("\033[31m {}".format(msg))
            elif lev == 2 or lev == 'orange':
                # оранжевый orange
                print("\033[33m {}".format(msg))
            elif lev == 3 or lev == 'blue':
                # голубой blue
                print("\033[36m {}".format(msg))
            elif lev == 4 or lev == 'green':
                # зеленый green
                print("\033[32m {}".format(msg))
            elif lev == 5 or lev == 'purple':
                # фиолетовый purple
                print("\033[35m {}".format(msg))
            else:
                # серый, если пришел неизвестный аргумент
                print("\033[37m {}".format(msg))
        else:
            pass


class ResetRelay(object):
    """
        сбросы реле в различных вариациях в зависимости от алгоритма
    """
    def __init__(self):
        self.ctrl_kl = CtrlKL()
        self.logger = logging.getLogger(__name__)

    def sbros_zashit_kl1(self):
        self.logger.debug("сброс защит KL1 1.5сек")
        self.ctrl_kl.ctrl_relay('KL1', True)
        self.logger.debug('включение KL1')
        sleep(1.5)
        self.ctrl_kl.ctrl_relay('KL1', False)
        self.logger.debug('отключение KL1')
        sleep(2)
        self.logger.debug('таймаут 2сек')

    def sbros_zashit_kl30(self):
        self.logger.debug("сброс защит KL30 0.5сек")
        self.ctrl_kl.ctrl_relay('KL30', True)
        self.logger.debug('включение KL30')
        sleep(0.5)
        self.ctrl_kl.ctrl_relay('KL30', False)
        self.logger.debug('отключение KL30')
        sleep(0.5)
        self.logger.debug('таймаут 0.5сек')

    def sbros_zashit_kl30_1s5(self):
        self.logger.debug("сброс защит KL30 1.5сек")
        self.ctrl_kl.ctrl_relay('KL30', True)
        self.logger.debug('включение KL30')
        sleep(1.5)
        self.ctrl_kl.ctrl_relay('KL30', False)
        self.logger.debug('отключение KL30')
        sleep(2.0)
        self.logger.debug('таймаут 2сек')

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
        используется для сброса после процедуры 1 -> 2.1 -> 3.1
        :return:
        """
        self.ctrl_kl.ctrl_relay('KL63', False)
        self.logger.debug("отключение реле KL63")
        sleep(0.1)
        self.stop_procedure_31()

    def sbros_kl63_proc_1_22_32(self):
        """
        используется для сброса после процедуры 1 -> 2.2 -> 3.2
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


class Resistor(object):
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
        self.ctrl_kl = CtrlKL()
        self.logger = logging.getLogger(__name__)

    def resist_ohm(self, ohm):

        if ohm == 0:
            self.ctrl_kl.ctrl_relay('KL3', True)
            self.ctrl_kl.ctrl_relay('KL4', True)
            self.ctrl_kl.ctrl_relay('KL5', True)
            self.ctrl_kl.ctrl_relay('KL6', True)
            self.ctrl_kl.ctrl_relay('KL7', True)
            self.ctrl_kl.ctrl_relay('KL8', True)
            self.ctrl_kl.ctrl_relay('KL9', True)
            self.ctrl_kl.ctrl_relay('KL10', True)
            self.logger.debug("включение 0 ом")
        elif ohm == 10:
            self.ctrl_kl.ctrl_relay('KL3', False)
            self.ctrl_kl.ctrl_relay('KL4', False)
            self.ctrl_kl.ctrl_relay('KL5', True)
            self.ctrl_kl.ctrl_relay('KL6', False)
            self.ctrl_kl.ctrl_relay('KL7', True)
            self.ctrl_kl.ctrl_relay('KL8', True)
            self.ctrl_kl.ctrl_relay('KL9', True)
            self.ctrl_kl.ctrl_relay('KL10', True)
            self.logger.debug("включение 10 ом")
        elif ohm == 15:
            self.ctrl_kl.ctrl_relay('KL3', True)
            self.ctrl_kl.ctrl_relay('KL4', True)
            self.ctrl_kl.ctrl_relay('KL5', True)
            self.ctrl_kl.ctrl_relay('KL6', True)
            self.ctrl_kl.ctrl_relay('KL7', False)
            self.ctrl_kl.ctrl_relay('KL8', True)
            self.ctrl_kl.ctrl_relay('KL9', True)
            self.ctrl_kl.ctrl_relay('KL10', True)
            self.logger.debug("включение 15 ом")
        elif ohm == 20:
            self.ctrl_kl.ctrl_relay('KL3', True)
            self.ctrl_kl.ctrl_relay('KL4', False)
            self.ctrl_kl.ctrl_relay('KL5', False)
            self.ctrl_kl.ctrl_relay('KL6', True)
            self.ctrl_kl.ctrl_relay('KL7', False)
            self.ctrl_kl.ctrl_relay('KL8', True)
            self.ctrl_kl.ctrl_relay('KL9', True)
            self.ctrl_kl.ctrl_relay('KL10', True)
            self.logger.debug("включение 20 ом")
        elif ohm == 35:
            self.ctrl_kl.ctrl_relay('KL3', False)
            self.ctrl_kl.ctrl_relay('KL4', False)
            self.ctrl_kl.ctrl_relay('KL5', False)
            self.ctrl_kl.ctrl_relay('KL6', True)
            self.ctrl_kl.ctrl_relay('KL7', True)
            self.ctrl_kl.ctrl_relay('KL8', False)
            self.ctrl_kl.ctrl_relay('KL9', True)
            self.ctrl_kl.ctrl_relay('KL10', True)
            self.logger.debug("включение 35 ом")
        elif ohm == 46:
            self.ctrl_kl.ctrl_relay('KL3', True)
            self.ctrl_kl.ctrl_relay('KL4', False)
            self.ctrl_kl.ctrl_relay('KL5', True)
            self.ctrl_kl.ctrl_relay('KL6', True)
            self.ctrl_kl.ctrl_relay('KL7', False)
            self.ctrl_kl.ctrl_relay('KL8', False)
            self.ctrl_kl.ctrl_relay('KL9', True)
            self.ctrl_kl.ctrl_relay('KL10', True)
            self.logger.debug("включение 46 ом")
        elif ohm == 50:
            self.ctrl_kl.ctrl_relay('KL3', False)
            self.ctrl_kl.ctrl_relay('KL4', False)
            self.ctrl_kl.ctrl_relay('KL5', False)
            self.ctrl_kl.ctrl_relay('KL6', True)
            self.ctrl_kl.ctrl_relay('KL7', False)
            self.ctrl_kl.ctrl_relay('KL8', False)
            self.ctrl_kl.ctrl_relay('KL9', True)
            self.ctrl_kl.ctrl_relay('KL10', True)
            self.logger.debug("включение 50 ом")
        elif ohm == 100:
            self.ctrl_kl.ctrl_relay('KL3', True)
            self.ctrl_kl.ctrl_relay('KL4', True)
            self.ctrl_kl.ctrl_relay('KL5', False)
            self.ctrl_kl.ctrl_relay('KL6', False)
            self.ctrl_kl.ctrl_relay('KL7', True)
            self.ctrl_kl.ctrl_relay('KL8', False)
            self.ctrl_kl.ctrl_relay('KL9', False)
            self.ctrl_kl.ctrl_relay('KL10', True)
            self.logger.debug("включение 100 ом")
        elif ohm == 110:
            self.ctrl_kl.ctrl_relay('KL3', False)
            self.ctrl_kl.ctrl_relay('KL4', True)
            self.ctrl_kl.ctrl_relay('KL5', False)
            self.ctrl_kl.ctrl_relay('KL6', True)
            self.ctrl_kl.ctrl_relay('KL7', False)
            self.ctrl_kl.ctrl_relay('KL8', False)
            self.ctrl_kl.ctrl_relay('KL9', False)
            self.ctrl_kl.ctrl_relay('KL10', True)
            self.logger.debug("включение 110 ом")
        elif ohm == 150:
            self.ctrl_kl.ctrl_relay('KL3', False)
            self.ctrl_kl.ctrl_relay('KL4', True)
            self.ctrl_kl.ctrl_relay('KL5', True)
            self.ctrl_kl.ctrl_relay('KL6', False)
            self.ctrl_kl.ctrl_relay('KL7', False)
            self.ctrl_kl.ctrl_relay('KL8', True)
            self.ctrl_kl.ctrl_relay('KL9', True)
            self.ctrl_kl.ctrl_relay('KL10', False)
            self.logger.debug("включение 150 ом")
        elif ohm == 255:
            self.ctrl_kl.ctrl_relay('KL3', False)
            self.ctrl_kl.ctrl_relay('KL4', False)
            self.ctrl_kl.ctrl_relay('KL5', False)
            self.ctrl_kl.ctrl_relay('KL6', False)
            self.ctrl_kl.ctrl_relay('KL7', False)
            self.ctrl_kl.ctrl_relay('KL8', False)
            self.ctrl_kl.ctrl_relay('KL9', False)
            self.ctrl_kl.ctrl_relay('KL10', False)
            self.logger.debug("включение 255 ом")
        
    def resist_kohm(self, kohm):

        if kohm == 0:
            self.ctrl_kl.ctrl_relay('KL13', True)
            self.ctrl_kl.ctrl_relay('KL14', True)
            self.ctrl_kl.ctrl_relay('KL15', True)
            self.ctrl_kl.ctrl_relay('KL16', True)
            self.ctrl_kl.ctrl_relay('KL17', True)
            self.ctrl_kl.ctrl_relay('KL18', True)
            self.ctrl_kl.ctrl_relay('KL19', True)
            self.ctrl_kl.ctrl_relay('KL20', True)
            self.logger.debug("включение 0 ком")
        if kohm == 12:
            self.ctrl_kl.ctrl_relay('KL13', False)
            self.ctrl_kl.ctrl_relay('KL14', True)
            self.ctrl_kl.ctrl_relay('KL15', False)
            self.ctrl_kl.ctrl_relay('KL16', True)
            self.ctrl_kl.ctrl_relay('KL17', True)
            self.ctrl_kl.ctrl_relay('KL18', True)
            self.ctrl_kl.ctrl_relay('KL19', True)
            self.ctrl_kl.ctrl_relay('KL20', True)
            self.logger.debug("включение 12 ком")
        if kohm == 21:
            self.ctrl_kl.ctrl_relay('KL13', True)
            self.ctrl_kl.ctrl_relay('KL14', False)
            self.ctrl_kl.ctrl_relay('KL15', True)
            self.ctrl_kl.ctrl_relay('KL16', False)
            self.ctrl_kl.ctrl_relay('KL17', True)
            self.ctrl_kl.ctrl_relay('KL18', True)
            self.ctrl_kl.ctrl_relay('KL19', True)
            self.ctrl_kl.ctrl_relay('KL20', True)
            self.logger.debug("включение 21 ком")
        elif kohm == 26:
            self.ctrl_kl.ctrl_relay('KL13', True)
            self.ctrl_kl.ctrl_relay('KL14', True)
            self.ctrl_kl.ctrl_relay('KL15', False)
            self.ctrl_kl.ctrl_relay('KL16', False)
            self.ctrl_kl.ctrl_relay('KL17', True)
            self.ctrl_kl.ctrl_relay('KL18', True)
            self.ctrl_kl.ctrl_relay('KL19', True)
            self.ctrl_kl.ctrl_relay('KL20', True)
            self.logger.debug("включение 26 ком")
        elif kohm == 30:
            self.ctrl_kl.ctrl_relay('KL13', False)
            self.ctrl_kl.ctrl_relay('KL14', True)
            self.ctrl_kl.ctrl_relay('KL15', False)
            self.ctrl_kl.ctrl_relay('KL16', False)
            self.ctrl_kl.ctrl_relay('KL17', True)
            self.ctrl_kl.ctrl_relay('KL18', True)
            self.ctrl_kl.ctrl_relay('KL19', True)
            self.ctrl_kl.ctrl_relay('KL20', True)
            self.logger.debug("включение 30 ком")
        elif kohm == 61:
            self.ctrl_kl.ctrl_relay('KL13', True)
            self.ctrl_kl.ctrl_relay('KL14', True)
            self.ctrl_kl.ctrl_relay('KL15', False)
            self.ctrl_kl.ctrl_relay('KL16', False)
            self.ctrl_kl.ctrl_relay('KL17', False)
            self.ctrl_kl.ctrl_relay('KL18', True)
            self.ctrl_kl.ctrl_relay('KL19', True)
            self.ctrl_kl.ctrl_relay('KL20', True)
            self.logger.debug("включение 61 ком")
        elif kohm == 65:
            self.ctrl_kl.ctrl_relay('KL13', True)
            self.ctrl_kl.ctrl_relay('KL14', False)
            self.ctrl_kl.ctrl_relay('KL15', False)
            self.ctrl_kl.ctrl_relay('KL16', False)
            self.ctrl_kl.ctrl_relay('KL17', False)
            self.ctrl_kl.ctrl_relay('KL18', True)
            self.ctrl_kl.ctrl_relay('KL19', True)
            self.ctrl_kl.ctrl_relay('KL20', True)
            self.logger.debug("включение 65 ком")
        elif kohm == 100:
            self.ctrl_kl.ctrl_relay('KL13', False)
            self.ctrl_kl.ctrl_relay('KL14', False)
            self.ctrl_kl.ctrl_relay('KL15', True)
            self.ctrl_kl.ctrl_relay('KL16', False)
            self.ctrl_kl.ctrl_relay('KL17', True)
            self.ctrl_kl.ctrl_relay('KL18', False)
            self.ctrl_kl.ctrl_relay('KL19', True)
            self.ctrl_kl.ctrl_relay('KL20', True)
            self.logger.debug("включение 100 ком")
        elif kohm == 200:
            self.ctrl_kl.ctrl_relay('KL13', False)
            self.ctrl_kl.ctrl_relay('KL14', False)
            self.ctrl_kl.ctrl_relay('KL15', False)
            self.ctrl_kl.ctrl_relay('KL16', True)
            self.ctrl_kl.ctrl_relay('KL17', False)
            self.ctrl_kl.ctrl_relay('KL18', True)
            self.ctrl_kl.ctrl_relay('KL19', False)
            self.ctrl_kl.ctrl_relay('KL20', True)
            self.logger.debug("включение 200 ком")
        elif kohm == 220:
            self.ctrl_kl.ctrl_relay('KL13', False)
            self.ctrl_kl.ctrl_relay('KL14', False)
            self.ctrl_kl.ctrl_relay('KL15', False)
            self.ctrl_kl.ctrl_relay('KL16', False)
            self.ctrl_kl.ctrl_relay('KL17', False)
            self.ctrl_kl.ctrl_relay('KL18', True)
            self.ctrl_kl.ctrl_relay('KL19', False)
            self.ctrl_kl.ctrl_relay('KL20', True)
            self.logger.debug("включение 220 ком")
        elif kohm == 590:
            self.ctrl_kl.ctrl_relay('KL13', False)
            self.ctrl_kl.ctrl_relay('KL14', False)
            self.ctrl_kl.ctrl_relay('KL15', False)
            self.ctrl_kl.ctrl_relay('KL16', False)
            self.ctrl_kl.ctrl_relay('KL17', False)
            self.ctrl_kl.ctrl_relay('KL18', False)
            self.ctrl_kl.ctrl_relay('KL19', False)
            self.ctrl_kl.ctrl_relay('KL20', False)
            self.logger.debug("включение 590 ком")
        
    def resist_10_to_20_ohm(self):
        self.ctrl_kl.ctrl_relay('KL3', True)
        self.ctrl_kl.ctrl_relay('KL6', True)
        self.ctrl_kl.ctrl_relay('KL8', True)
        self.ctrl_kl.ctrl_relay('KL9', True)
        self.ctrl_kl.ctrl_relay('KL10', True)
        self.logger.debug("переключение с 10 ом на 20 ом")

    def resist_10_to_35_ohm(self):
        self.ctrl_kl.ctrl_relay('KL5', False)
        self.ctrl_kl.ctrl_relay('KL6', True)
        self.ctrl_kl.ctrl_relay('KL8', False)
        self.logger.debug("переключение с 10 ом на 35 ом")
        
    def resist_10_to_100_ohm(self):
        self.ctrl_kl.ctrl_relay('KL9', False)
        self.ctrl_kl.ctrl_relay('KL8', False)
        self.logger.debug("переключение с 10 ом на 100 ом")

    def resist_10_to_46_ohm(self):
        self.ctrl_kl.ctrl_relay('KL7', False)
        self.ctrl_kl.ctrl_relay('KL6', True)
        self.ctrl_kl.ctrl_relay('KL8', False)
        self.logger.debug("переключение с 10 ом на 46 ом")

    def resist_10_to_50_ohm(self):
        self.ctrl_kl.ctrl_relay('KL7', False)
        self.ctrl_kl.ctrl_relay('KL5', False)
        self.ctrl_kl.ctrl_relay('KL6', True)
        self.ctrl_kl.ctrl_relay('KL8', False)
        self.logger.debug("переключение с 10 ом на 50 ом")

    def resist_10_to_110_ohm(self):
        self.ctrl_kl.ctrl_relay('KL9', False)
        self.ctrl_kl.ctrl_relay('KL4', True)
        self.ctrl_kl.ctrl_relay('KL5', False)
        self.ctrl_kl.ctrl_relay('KL8', False)
        self.ctrl_kl.ctrl_relay('KL6', True)
        self.ctrl_kl.ctrl_relay('KL7', False)
        self.logger.debug("переключение с 10 ом на 110 ом")

    def resist_35_to_110_ohm(self):
        self.ctrl_kl.ctrl_relay('KL9', False)
        self.ctrl_kl.ctrl_relay('KL7', False)
        self.logger.debug("переключение с 35 ом на 110 ом")

    def resist_10_to_137_ohm(self):
        self.ctrl_kl.ctrl_relay('KL10', False)
        self.logger.debug("переключение с 10 ом на 137 ом")

    def resist_0_to_50_ohm(self):
        self.ctrl_kl.ctrl_relay('KL3', False)
        self.ctrl_kl.ctrl_relay('KL4', False)
        self.ctrl_kl.ctrl_relay('KL5', False)
        self.ctrl_kl.ctrl_relay('KL7', False)
        self.ctrl_kl.ctrl_relay('KL8', False)
        self.logger.debug("переключение с 0 ом на 50 ом")

    def resist_0_to_100_ohm(self):
        self.ctrl_kl.ctrl_relay('KL5', False)
        self.ctrl_kl.ctrl_relay('KL6', False)
        self.ctrl_kl.ctrl_relay('KL8', False)
        self.ctrl_kl.ctrl_relay('KL9', False)
        self.logger.debug("переключение с 0 ом на 100 ом")

    def resist_0_to_63_ohm(self):
        self.ctrl_kl.ctrl_relay('KL9', False)
        self.ctrl_kl.ctrl_relay('KL4', False)
        self.logger.debug("переключение с 0 ом на 63 ом")

    def resist_220_to_100_kohm(self):
        self.ctrl_kl.ctrl_relay('KL18', False)
        self.ctrl_kl.ctrl_relay('KL19', True)
        self.ctrl_kl.ctrl_relay('KL17', True)
        self.ctrl_kl.ctrl_relay('KL15', True)
        self.logger.debug("переключение с 220 ком на 100 ком")
        

class ModbusConnectException(Exception):
    """вываливается когда нет связи по modbus"""
    pass


class HardwareException(Exception):
    """вываливается при неиспраности стенда"""
    pass


class ResultMsg(object):
    """
    исправность/неисправность блока
    """
    def __init__(self):
        self.reset = ResetRelay()

    def test_error(self, test_number):
        msg = (f'Тест: {test_number} не пройден')
        my_msg(msg)
        self.reset.reset_all()

    def test_good(self):
        msg = "Тестирование завершено:\nБлок исправен "
        my_msg(msg)
        self.reset.reset_all()
