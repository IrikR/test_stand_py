#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки
Тип блока Производитель
БДУ-ДР.01	Нет производителя
БДУ-ДР.01	ДонЭнергоЗавод

"""

import sys
import logging

from time import sleep

from gen_func_utils import *
from my_msgbox import *
from gen_mb_client import *
from gen_mysql_connect import *

__all__ = ["TestBDUDR01"]


class TestBDUDR01(object):

    def __init__(self):
        self.__resist = Resistor()
        self.__read_mb = ReadMB()
        self.__ctrl_kl = CtrlKL()
        self.__mysql_conn = MySQLConnect()
        self.__fault = Bug(True)

        logging.basicConfig(filename="C:\Stend\project_class\TestBDUDR01.log",
                            filemode="w",
                            level=logging.DEBUG,
                            encoding="utf-8",
                            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('WARNING')
        self.logger = logging.getLogger(__name__)

    def st_test_1_bdu_dr01(self):
        """
        Тест 1. Проверка исходного состояния блока:
        :return:
        """
        self.__mysql_conn.mysql_ins_result("идёт тест 1", '1')
        in_a1, in_a2, in_a3, in_a4 = self.__inputs_a()
        if in_a1 is False and in_a2 is False and in_a3 is False and in_a4 is False:
            pass
        else:
            self.__fault.debug_msg('тест 1 положение выходов не соответствует', 1)
            self.__mysql_conn.mysql_ins_result("неисправен", '1')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(216)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(217)
            elif in_a3 is True:
                self.__mysql_conn.mysql_error(218)
            elif in_a4 is True:
                self.__mysql_conn.mysql_error(219)
            return False
        self.__fault.debug_msg('тест 1 положение выходов соответствует', 4)
        self.__mysql_conn.mysql_ins_result("исправен", '1')
        return True

    def st_test_20_bdu_dr01(self) -> bool:
        """
        Тест 2. Проверка включения/выключения канала № 1 (К1)  блока от кнопки «Пуск/Стоп».
        """
        self.__mysql_conn.mysql_ins_result("идёт тест 2.1", '2')
        self.__ctrl_kl.ctrl_relay('KL2', True)
        in_a1, in_a2, in_a3, in_a4 = self.__inputs_a()
        if in_a1 is False and in_a2 is False and in_a3 is False and in_a4 is False:
            pass
        else:
            self.__fault.debug_msg('тест 2.1 положение выходов не соответствует', 1)
            self.__mysql_conn.mysql_ins_result("неисправен", '2')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(220)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(221)
            elif in_a3 is True:
                self.__mysql_conn.mysql_error(222)
            elif in_a4 is True:
                self.__mysql_conn.mysql_error(223)
            return False
        self.__fault.debug_msg('тест 2.1 положение выходов соответствует', 4)
        return True

    def st_test_21_bdu_dr01(self) -> bool:
        """
        2.2. Включение 1 канала блока от кнопки «Пуск» 1 канала
        2.3. Проверка удержания 1 канала блока во включенном состоянии
        при подключении Rш пульта управления 1 каналом блока:
        """
        if self.__subtest_22(2.2, 2):
            if self.__subtest_23(2.3, 2):
                return True
        return False

    def st_test_22_bdu_dr01(self) -> bool:
        """
        2.4. Выключение 1 канала блока от кнопки «Стоп»
        """
        self.__mysql_conn.mysql_ins_result("идёт тест 2.4", '2')
        self.__ctrl_kl.ctrl_relay('KL12', False)
        sleep(1)
        in_a1, in_a2, in_a3, in_a4 = self.__inputs_a()
        if in_a1 is False and in_a2 is False and in_a3 is False and in_a4 is False:
            pass
        else:
            self.__fault.debug_msg('тест 2.4 положение выходов не соответствует', 1)
            self.__mysql_conn.mysql_ins_result("неисправен", '2')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(232)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(233)
            elif in_a3 is True:
                self.__mysql_conn.mysql_error(234)
            elif in_a4 is True:
                self.__mysql_conn.mysql_error(235)
            return False
        self.__fault.debug_msg('тест 2.4 положение выходов соответствует', 4)
        self.__ctrl_kl.ctrl_relay('KL25', False)
        self.__ctrl_kl.ctrl_relay('KL1', False)
        self.__mysql_conn.mysql_ins_result("исправен", '2')
        return True

    def st_test_30_bdu_dr01(self) -> bool:
        """
        Повторяем тест 2.2. Включение 1 канала блока от кнопки «Пуск» 1 канала
        Повторяем тест 2.3. Проверка удержания 1 канала блока во включенном состоянии
        при подключении Rш пульта управления 1 каналом блока:
        """
        if self.__subtest_22(3.1, 3):
            if self.__subtest_23(3.2, 3):
                return True
        return False

    def st_test_31_bdu_dr01(self) -> bool:
        """
        3. Отключение исполнительного элемента 1 канала при увеличении сопротивления цепи заземления
        """
        self.__mysql_conn.mysql_ins_result("идёт тест 3.3", '3')
        self.__resist.resist_10_to_110_ohm()
        sleep(1)
        in_a1, in_a2, in_a3, in_a4 = self.__inputs_a()
        if in_a1 is False and in_a2 is False and in_a3 is False and in_a4 is False:
            pass
        else:
            self.__fault.debug_msg('тест 3 положение выходов не соответствует', 1)
            self.__mysql_conn.mysql_ins_result("неисправен", '3')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(236)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(237)
            elif in_a3 is True:
                self.__mysql_conn.mysql_error(238)
            elif in_a4 is True:
                self.__mysql_conn.mysql_error(239)
            return False
        self.__fault.debug_msg('тест 3 положение выходов соответствует', 4)
        self.__ctrl_kl.ctrl_relay('KL12', False)
        self.__ctrl_kl.ctrl_relay('KL25', False)
        self.__ctrl_kl.ctrl_relay('KL1', False)
        self.__mysql_conn.mysql_ins_result("исправен", '3')
        return True

    def st_test_40_bdu_dr01(self) -> bool:
        """
        Повторяем тест 2.2. Включение 1 канала блока от кнопки «Пуск» 1 канала
        Повторяем тест 2.3. Проверка удержания 1 канала блока во включенном состоянии
        при подключении Rш пульта управления 1 каналом блока:
        """
        if self.__subtest_22(4.1, 4):
            if self.__subtest_23(4.2, 4):
                return True
        return False

    def st_test_41_bdu_dr01(self) -> bool:
        """
        4. Защита от потери управляемости 1 канала блока при замыкании проводов ДУ
        """
        self.__mysql_conn.mysql_ins_result("идёт тест 4.3", '4')
        self.__ctrl_kl.ctrl_relay('KL11', True)
        sleep(1)
        in_a1, in_a2, in_a3, in_a4 = self.__inputs_a()
        if in_a1 is False and in_a2 is False and in_a3 is False and in_a4 is False:
            pass
        else:
            self.__fault.debug_msg('тест 4 положение выходов не соответствует', 1)
            self.__mysql_conn.mysql_ins_result("неисправен", '4')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(240)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(241)
            elif in_a3 is True:
                self.__mysql_conn.mysql_error(242)
            elif in_a4 is True:
                self.__mysql_conn.mysql_error(243)
            return False
        self.__fault.debug_msg('тест 4 положение выходов не соответствует', 4)
        self.__ctrl_kl.ctrl_relay('KL12', False)
        self.__ctrl_kl.ctrl_relay('KL25', False)
        self.__ctrl_kl.ctrl_relay('KL1', False)
        self.__ctrl_kl.ctrl_relay('KL11', False)
        self.__mysql_conn.mysql_ins_result("исправен", '4')
        return True

    def st_test_50_bdu_dr01(self) -> bool:
        """
        Повторяем тест 2.2. Включение 1 канала блока от кнопки «Пуск» 1 канала
        Повторяем тест 2.3. Проверка удержания 1 канала блока во включенном состоянии
        при подключении Rш пульта управления 1 каналом блока:
        """
        if self.__subtest_22(5.1, 5):
            if self.__subtest_23(5.2, 5):
                return True
        return False

    def st_test_51_bdu_dr01(self) -> bool:
        """
        Тест 5. Защита от потери управляемости 1 канала блока при обрыве проводов ДУ
        """
        self.__mysql_conn.mysql_ins_result("идёт тест 5.3", '5')
        self.__ctrl_kl.ctrl_relay('KL12', False)
        sleep(1)
        in_a1, in_a2, in_a3, in_a4 = self.__inputs_a()
        if in_a1 is False and in_a2 is False and in_a3 is False and in_a4 is False:
            pass
        else:
            self.__fault.debug_msg('тест 5 положение выходов не соответствует', 1)
            self.__mysql_conn.mysql_ins_result("неисправен", '5')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(244)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(245)
            elif in_a3 is True:
                self.__mysql_conn.mysql_error(246)
            elif in_a4 is True:
                self.__mysql_conn.mysql_error(247)
            return False
        self.__fault.debug_msg('тест 5 положение выходов соответствует', 4)
        self.__ctrl_kl.ctrl_relay('KL25', False)
        self.__ctrl_kl.ctrl_relay('KL1', False)
        self.__mysql_conn.mysql_ins_result("исправен", '5')
        return True

    def st_test_60_bdu_dr01(self) -> bool:
        """
        Тест 6. Проверка включения/выключения канала № 2 (К2)  блока от кнопки «Пуск/Стоп».
        """
        self.__mysql_conn.mysql_ins_result("идёт тест 6.1", '6')
        self.__ctrl_kl.ctrl_relay('KL2', True)
        self.__ctrl_kl.ctrl_relay('KL26', True)
        self.__ctrl_kl.ctrl_relay('KL28', True)
        sleep(1)
        in_a1, in_a2, in_a3, in_a4 = self.__inputs_a()
        if in_a1 is False and in_a2 is False and in_a3 is False and in_a4 is False:
            pass
        else:
            self.__fault.debug_msg('тест 6 положение выходов не соответствует', 1)
            self.__mysql_conn.mysql_ins_result("неисправен", '6')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(248)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(249)
            elif in_a3 is True:
                self.__mysql_conn.mysql_error(250)
            elif in_a4 is True:
                self.__mysql_conn.mysql_error(251)
            return False
        self.__fault.debug_msg('тест 6 положение выходов соответствует', 4)
        return True

    def st_test_61_bdu_dr01(self) -> bool:
        """
        2.2. Включение 1 канала блока от кнопки «Пуск» 1 канала
        2.3. Проверка удержания 1 канала блока во включенном состоянии
        при подключении Rш пульта управления 1 каналом блока:
        """
        if self.__subtest_62(6.2, 6):
            if self.__subtest_63(6.3, 6):
                return True
        return False

    def st_test_62_bdu_dr01(self) -> bool:
        """
        6.4. Выключение 2 канала блока от кнопки «Стоп»
        """
        self.__mysql_conn.mysql_ins_result("идёт тест 6.3", '6')
        self.__ctrl_kl.ctrl_relay('KL12', False)
        sleep(1)
        in_a1, in_a2, in_a3, in_a4 = self.__inputs_a()
        if in_a1 is False and in_a2 is False and in_a3 is False and in_a4 is False:
            pass
        else:
            self.__fault.debug_msg('тест 6.4 положение выходов не соответствует', 1)
            self.__mysql_conn.mysql_ins_result("неисправен", '6')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(260)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(261)
            elif in_a3 is True:
                self.__mysql_conn.mysql_error(262)
            elif in_a4 is True:
                self.__mysql_conn.mysql_error(263)
            return False
        self.__fault.debug_msg('тест 6.4 положение выходов соответствует', 4)
        self.__ctrl_kl.ctrl_relay('KL25', False)
        self.__ctrl_kl.ctrl_relay('KL29', False)
        self.__mysql_conn.mysql_ins_result("исправен", '6')
        return True

    def st_test_70_bdu_dr01(self) -> bool:
        """
        Повторяем тест 2.2. Включение 1 канала блока от кнопки «Пуск» 1 канала
        Повторяем тест 2.3. Проверка удержания 1 канала блока во включенном состоянии
        при подключении Rш пульта управления 1 каналом блока:
        """
        if self.__subtest_62(7.1, 7):
            if self.__subtest_63(7.1, 7):
                return True
        return False

    def st_test_71_bdu_dr01(self) -> bool:
        """
        7. Отключение исполнительного элемента 2 канала при увеличении сопротивления цепи заземления
        """
        self.__mysql_conn.mysql_ins_result("идёт тест 7.3", '7')
        self.__resist.resist_10_to_110_ohm()
        sleep(1)
        in_a1, in_a2, in_a3, in_a4 = self.__inputs_a()
        if in_a1 is False and in_a2 is False and in_a3 is False and in_a4 is False:
            pass
        else:
            self.__fault.debug_msg('тест 7 положение выходов не соответствует', 1)
            self.__mysql_conn.mysql_ins_result("неисправен", '7')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(264)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(265)
            elif in_a3 is True:
                self.__mysql_conn.mysql_error(266)
            elif in_a4 is True:
                self.__mysql_conn.mysql_error(267)
            return False
        self.__fault.debug_msg('тест 7 положение выходов соответствует', 4)
        self.__ctrl_kl.ctrl_relay('KL12', False)
        self.__ctrl_kl.ctrl_relay('KL25', False)
        self.__ctrl_kl.ctrl_relay('KL29', False)
        self.__mysql_conn.mysql_ins_result("исправен", '7')
        return True

    def st_test_80_bdu_dr01(self) -> bool:
        """
        Повторяем тест 2.2. Включение 1 канала блока от кнопки «Пуск» 1 канала
        Повторяем тест 2.3. Проверка удержания 1 канала блока во включенном состоянии
        при подключении Rш пульта управления 1 каналом блока:
        """
        if self.__subtest_62(8.1, 8):
            if self.__subtest_63(8.1, 8):
                return True
        return False

    def st_test_81_bdu_dr01(self) -> bool:
        """
        8. Защита от потери управляемости 2 канала блока при замыкании проводов ДУ
        """
        self.__mysql_conn.mysql_ins_result("идёт тест 8.3", '8')
        self.__ctrl_kl.ctrl_relay('KL11', True)
        sleep(1)
        in_a1, in_a2, in_a3, in_a4 = self.__inputs_a()
        if in_a1 is False and in_a2 is False and in_a3 is False and in_a4 is False:
            pass
        else:
            self.__fault.debug_msg('тест 8 положение выходов не соответствует', 1)
            self.__mysql_conn.mysql_ins_result("неисправен", '8')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(268)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(269)
            elif in_a3 is True:
                self.__mysql_conn.mysql_error(270)
            elif in_a4 is True:
                self.__mysql_conn.mysql_error(271)
            return False
        self.__fault.debug_msg('тест 8 положение выходов соответствует', 4)
        self.__ctrl_kl.ctrl_relay('KL12', False)
        self.__ctrl_kl.ctrl_relay('KL25', False)
        self.__ctrl_kl.ctrl_relay('KL29', False)
        self.__ctrl_kl.ctrl_relay('KL11', False)
        self.__mysql_conn.mysql_ins_result("исправен", '8')
        return True

    def st_test_90_bdu_dr01(self) -> bool:
        """
        Повторяем тест 2.2. Включение 1 канала блока от кнопки «Пуск» 1 канала
        Повторяем тест 2.3. Проверка удержания 1 канала блока во включенном состоянии
        при подключении Rш пульта управления 1 каналом блока:
        """
        if self.__subtest_62(9.1, 9):
            if self.__subtest_63(9.1, 9):
                return True
        return False

    def st_test_91_bdu_dr01(self):
        """
        Тест 9. Защита от потери управляемости 1 канала блока при обрыве проводов ДУ
        """
        self.__mysql_conn.mysql_ins_result("идёт тест 9.3", '9')
        self.__ctrl_kl.ctrl_relay('KL12', False)
        sleep(1)
        in_a1, in_a2, in_a3, in_a4 = self.__inputs_a()
        if in_a1 is False and in_a2 is False and in_a3 is False and in_a4 is False:
            pass
        else:
            self.__fault.debug_msg('тест 9 положение выходов не соответствует', 1)
            self.__mysql_conn.mysql_ins_result("неисправен", '9')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(272)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(273)
            elif in_a3 is True:
                self.__mysql_conn.mysql_error(274)
            elif in_a4 is True:
                self.__mysql_conn.mysql_error(275)
            return False
        self.__fault.debug_msg('тест 9 положение выходов соответствует', 4)
        self.__mysql_conn.mysql_ins_result("исправен", '9')
        return True

    def __subtest_22(self, subtest_2_num: float, test_2_num: int) -> bool:
        """
        2.2. Включение 1 канала блока от кнопки «Пуск» 1 канала
        """
        self.__mysql_conn.mysql_ins_result(f'идёт тест {subtest_2_num}', f'{test_2_num}')
        self.__resist.resist_ohm(255)
        self.__resist.resist_ohm(10)
        sleep(1)
        self.__ctrl_kl.ctrl_relay('KL12', True)
        sleep(1)
        in_a1, in_a2, in_a3, in_a4 = self.__inputs_a()
        if in_a1 is True and in_a2 is True and in_a3 is False and in_a4 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", f'{test_2_num}')
            self.__fault.debug_msg(f'тест {subtest_2_num} положение выходов не соответствует', 1)
            if in_a1 is False:
                self.__mysql_conn.mysql_error(224)
            elif in_a2 is False:
                self.__mysql_conn.mysql_error(225)
            elif in_a3 is True:
                self.__mysql_conn.mysql_error(226)
            elif in_a4 is True:
                self.__mysql_conn.mysql_error(227)
            return False
        self.__fault.debug_msg(f'тест {subtest_2_num} положение выходов соответствует', 4)
        return True

    def __subtest_23(self, subtest_3_num: float, test_3_num: int) -> bool:
        """
        2.3. Проверка удержания 1 канала блока во включенном состоянии
        при подключении Rш пульта управления 1 каналом блока:
        """
        self.__mysql_conn.mysql_ins_result(f'идёт тест {subtest_3_num}', f'{test_3_num}')
        self.__ctrl_kl.ctrl_relay('KL1', True)
        self.__ctrl_kl.ctrl_relay('KL25', True)
        sleep(1)
        in_a1, in_a2, in_a3, in_a4 = self.__inputs_a()
        if in_a1 is True and in_a2 is True and in_a3 is False and in_a4 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", f'{test_3_num}')
            self.__fault.debug_msg(f'тест {subtest_3_num} положение выходов не соответствует', 1)
            if in_a1 is False:
                self.__mysql_conn.mysql_error(228)
            elif in_a2 is False:
                self.__mysql_conn.mysql_error(229)
            elif in_a3 is True:
                self.__mysql_conn.mysql_error(230)
            elif in_a4 is True:
                self.__mysql_conn.mysql_error(231)
            return False
        self.__fault.debug_msg(f'тест {subtest_3_num} положение выходов соответствует', 4)
        return True

    def __subtest_62(self, subtest_4_num: float, test_4_num: int) -> bool:
        """
        6.2. Включение 2 канала блока от кнопки «Пуск» 2 канала
        """
        self.__mysql_conn.mysql_ins_result(f'идёт тест {subtest_4_num}', f'{test_4_num}')
        self.__resist.resist_ohm(255)
        self.__resist.resist_ohm(10)
        sleep(1)
        self.__ctrl_kl.ctrl_relay('KL12', True)
        sleep(1)
        in_a1, in_a2, in_a3, in_a4 = self.__inputs_a()
        if in_a1 is False and in_a2 is False and in_a3 is True and in_a4 is True:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", f'{test_4_num}')
            self.__fault.debug_msg(f'тест {subtest_4_num} положение выходов не соответствует', 1)
            if in_a1 is True:
                self.__mysql_conn.mysql_error(252)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(253)
            elif in_a3 is False:
                self.__mysql_conn.mysql_error(254)
            elif in_a4 is False:
                self.__mysql_conn.mysql_error(255)
            return False
        self.__fault.debug_msg(f'тест {subtest_4_num} положение выходов соответствует', 4)
        return True

    def __subtest_63(self, subtest_5_num: float, test_5_num: int) -> bool:
        """
        6.3. Проверка удержания 2 канала блока во включенном состоянии
        при подключении Rш пульта управления 2 каналом блока:
        """
        self.__mysql_conn.mysql_ins_result(f'идёт тест {subtest_5_num}', f'{test_5_num}')
        self.__ctrl_kl.ctrl_relay('KL29', True)
        self.__ctrl_kl.ctrl_relay('KL25', True)
        sleep(1)
        in_a1, in_a2, in_a3, in_a4 = self.__inputs_a()
        if in_a1 is False and in_a2 is False and in_a3 is True and in_a4 is True:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", f'{test_5_num}')
            self.__fault.debug_msg(f'тест {subtest_5_num} положение выходов не соответствует', 1)
            if in_a1 is True:
                self.__mysql_conn.mysql_error(256)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(257)
            elif in_a3 is False:
                self.__mysql_conn.mysql_error(258)
            elif in_a4 is False:
                self.__mysql_conn.mysql_error(259)
            return False
        self.__fault.debug_msg(f'тест {subtest_5_num} положение выходов соответствует', 4)
        return True

    def __inputs_a(self):
        in_a1 = self.__read_mb.read_discrete(1)
        in_a2 = self.__read_mb.read_discrete(2)
        in_a3 = self.__read_mb.read_discrete(3)
        in_a4 = self.__read_mb.read_discrete(4)
        if in_a1 is None or in_a2 is None or in_a3 is None or in_a4 is None:
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_a1, in_a2, in_a3, in_a4

    def st_test_bdu_dr01(self) -> bool:
        """
        Главная функция которая собирает все остальные
        """
        if self.st_test_1_bdu_dr01():
            if self.st_test_20_bdu_dr01():
                if self.st_test_21_bdu_dr01():
                    if self.st_test_22_bdu_dr01():
                        if self.st_test_30_bdu_dr01():
                            if self.st_test_31_bdu_dr01():
                                if self.st_test_40_bdu_dr01():
                                    if self.st_test_41_bdu_dr01():
                                        if self.st_test_50_bdu_dr01():
                                            if self.st_test_51_bdu_dr01():
                                                if self.st_test_60_bdu_dr01():
                                                    if self.st_test_61_bdu_dr01():
                                                        if self.st_test_62_bdu_dr01():
                                                            if self.st_test_70_bdu_dr01():
                                                                if self.st_test_71_bdu_dr01():
                                                                    if self.st_test_80_bdu_dr01():
                                                                        if self.st_test_81_bdu_dr01():
                                                                            if self.st_test_90_bdu_dr01():
                                                                                if self.st_test_91_bdu_dr01():
                                                                                    return True
        return False


if __name__ == '__main__':
    test_bdu_dr01 = TestBDUDR01()
    reset_test_bdu_dr01 = ResetRelay()
    mysql_conn_test_bdu_dr01 = MySQLConnect()
    fault = Bug(True)
    try:
        if test_bdu_dr01.st_test_bdu_dr01():
            mysql_conn_test_bdu_dr01.mysql_block_good()
            my_msg('Блок исправен', 'green')
        else:
            mysql_conn_test_bdu_dr01.mysql_block_bad()
            my_msg('Блок неисправен', 'red')
    except OSError:
        my_msg("ошибка системы", 'red')
    except SystemError:
        my_msg("внутренняя ошибка", 'red')
    except ModbusConnectException as mce:
        fault.debug_msg(mce, 'red')
        my_msg(f'{mce}', 'red')
    finally:
        reset_test_bdu_dr01.reset_all()
        sys.exit()
