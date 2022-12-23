#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки
Тип блока: БДУ-ДР.01
Производитель: Нет производителя, ДонЭнергоЗавод

"""

import sys
import logging

from time import sleep

from general_func.exception import *
from general_func.subtest import Subtest4in, ReadOPCServer
from general_func.database import *
from general_func.modbus import *
from general_func.resistance import Resistor
from general_func.reset import ResetRelay
from gui.msgbox_1 import *


__all__ = ["TestBDUDR01"]


class TestBDUDR01:

    def __init__(self):
        self.resist = Resistor()
        self.ctrl_kl = CtrlKL()
        self.mysql_conn = MySQLConnect()
        self.subtest = Subtest4in()
        self.di_read_full = ReadOPCServer()

        logging.basicConfig(
            filename="C:\\Stend\\project_class\\log\\TestBDUDR01.log",
            filemode="w",
            level=logging.DEBUG,
            encoding="utf-8",
            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('DEBUG')
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))

    def st_test_1(self) -> bool:
        """
        Тест 1. Проверка исходного состояния блока:
        :return:
        :rtype bool:
        """
        if self.di_read_full.subtest_4di(test_num=1, subtest_num=1.0, err_code_a=216, err_code_b=217, err_code_c=218,
                                         err_code_d=219, position_a=False, position_b=False, position_c=False,
                                         position_d=False, di_a='in_a1', di_b='in_a2', di_c='in_a3', di_d='in_a4'):
            return True
        return False

    def st_test_20(self) -> bool:
        """
        Тест 2. Проверка включения/выключения канала № 1 (К1) блока от кнопки «Пуск/Стоп».
        """
        self.logger.debug("старт теста 2.0")
        self.ctrl_kl.ctrl_relay('KL2', True)
        self.logger.debug("включен KL2")
        if self.di_read_full.subtest_4di(test_num=2, subtest_num=2.0, err_code_a=220, err_code_b=221, err_code_c=222,
                                         err_code_d=223, position_a=False, position_b=False, position_c=False,
                                         position_d=False, di_a='in_a1', di_b='in_a2', di_c='in_a3', di_d='in_a4'):
            return True
        return False

    def st_test_21(self) -> bool:
        """
        2.2. Включение 1 канала блока от кнопки «Пуск» 1 канала
        2.3. Проверка удержания 1 канала блока во включенном состоянии
        при подключении Rш пульта управления 1 каналом блока:
        """
        if self.subtest.subtest_a(test_num=2, subtest_num=2.1, resistance=10,
                                  err_code_a=224, err_code_b=225, err_code_c=226, err_code_d=227,
                                  position_a=True, position_b=True, position_c=False, position_d=False,
                                  di_a='in_a1', di_b='in_a2', di_c='in_a3', di_d='in_a4'):
            if self.subtest.subtest_b(test_num=2, subtest_num=2.2, relay='KL1',
                                      err_code_a=228, err_code_b=229, err_code_c=230, err_code_d=231,
                                      position_a=True, position_b=True, position_c=False, position_d=False,
                                      di_a='in_a1', di_b='in_a2', di_c='in_a3', di_d='in_a4'):
                return True
        return False

    def st_test_23(self) -> bool:
        """
        2.4. Выключение 1 канала блока от кнопки «Стоп»
        """
        self.logger.debug("старт теста 2.3")
        self.ctrl_kl.ctrl_relay('KL12', False)
        self.logger.debug("отключен KL12")
        sleep(1)
        if self.di_read_full.subtest_4di(test_num=2, subtest_num=2.3, err_code_a=232, err_code_b=233, err_code_c=234,
                                         err_code_d=235, position_a=False, position_b=False, position_c=False,
                                         position_d=False, di_a='in_a1', di_b='in_a2', di_c='in_a3', di_d='in_a4'):
            self.ctrl_kl.ctrl_relay('KL25', False)
            self.ctrl_kl.ctrl_relay('KL1', False)
            self.logger.debug("отключены KL1, KL25")
            return True
        return False

    def st_test_30(self) -> bool:
        """
        Повторяем тест 2.2. Включение 1 канала блока от кнопки «Пуск» 1 канала
        Повторяем тест 2.3. Проверка удержания 1 канала блока во включенном состоянии
        при подключении Rш пульта управления 1 каналом блока:
        """
        if self.subtest.subtest_a(test_num=3, subtest_num=3.0, resistance=10,
                                  err_code_a=224, err_code_b=225, err_code_c=226, err_code_d=227,
                                  position_a=True, position_b=True, position_c=False, position_d=False,
                                  di_a='in_a1', di_b='in_a2', di_c='in_a3', di_d='in_a4'):
            if self.subtest.subtest_b(test_num=3, subtest_num=3.1, relay='KL1',
                                      err_code_a=228, err_code_b=229, err_code_c=230, err_code_d=231,
                                      position_a=True, position_b=True, position_c=False, position_d=False,
                                      di_a='in_a1', di_b='in_a2', di_c='in_a3', di_d='in_a4'):
                return True
        return False

    def st_test_32(self) -> bool:
        """
        3. Отключение исполнительного элемента 1 канала при увеличении сопротивления цепи заземления
        """
        self.logger.debug("старт теста 3.2")
        self.resist.resist_10_to_110_ohm()
        sleep(1)
        if self.di_read_full.subtest_4di(test_num=3, subtest_num=3.2, err_code_a=236, err_code_b=237, err_code_c=238,
                                         err_code_d=239, position_a=False, position_b=False, position_c=False,
                                         position_d=False, di_a='in_a1', di_b='in_a2', di_c='in_a3', di_d='in_a4'):
            self.ctrl_kl.ctrl_relay('KL12', False)
            self.ctrl_kl.ctrl_relay('KL25', False)
            self.ctrl_kl.ctrl_relay('KL1', False)
            self.logger.debug("отключены KL12, KL25, KL1")
            return True
        return False

    def st_test_40(self) -> bool:
        """
        Повторяем тест 2.2. Включение 1 канала блока от кнопки «Пуск» 1 канала
        Повторяем тест 2.3. Проверка удержания 1 канала блока во включенном состоянии
        при подключении Rш пульта управления 1 каналом блока:
        """
        if self.subtest.subtest_a(test_num=4, subtest_num=4.0, resistance=10,
                                  err_code_a=224, err_code_b=225, err_code_c=226, err_code_d=227,
                                  position_a=True, position_b=True, position_c=False, position_d=False,
                                  di_a='in_a1', di_b='in_a2', di_c='in_a3', di_d='in_a4'):
            if self.subtest.subtest_b(test_num=4, subtest_num=4.1, relay='KL1',
                                      err_code_a=228, err_code_b=229, err_code_c=230, err_code_d=231,
                                      position_a=True, position_b=True, position_c=False, position_d=False,
                                      di_a='in_a1', di_b='in_a2', di_c='in_a3', di_d='in_a4'):
                return True
        return False

    def st_test_42(self) -> bool:
        """
        4. Защита от потери управляемости 1 канала блока при замыкании проводов ДУ
        """
        self.logger.debug("старт теста 4.2")
        self.ctrl_kl.ctrl_relay('KL11', True)
        self.logger.debug("включен KL11")
        sleep(1)
        if self.di_read_full.subtest_4di(test_num=4, subtest_num=4.3, err_code_a=240, err_code_b=241, err_code_c=242,
                                         err_code_d=243, position_a=False, position_b=False, position_c=False,
                                         position_d=False, di_a='in_a1', di_b='in_a2', di_c='in_a3', di_d='in_a4'):
            self.ctrl_kl.ctrl_relay('KL12', False)
            self.ctrl_kl.ctrl_relay('KL25', False)
            self.ctrl_kl.ctrl_relay('KL1', False)
            self.ctrl_kl.ctrl_relay('KL11', False)
            self.logger.debug("отключены KL12, KL25, KL1, KL11")
            return True
        return False

    def st_test_50(self) -> bool:
        """
        Повторяем тест 2.2. Включение 1 канала блока от кнопки «Пуск» 1 канала
        Повторяем тест 2.3. Проверка удержания 1 канала блока во включенном состоянии
        при подключении Rш пульта управления 1 каналом блока:
        """
        if self.subtest.subtest_a(test_num=5, subtest_num=5.0, resistance=10,
                                  err_code_a=224, err_code_b=225, err_code_c=226, err_code_d=227,
                                  position_a=True, position_b=True, position_c=False, position_d=False,
                                  di_a='in_a1', di_b='in_a2', di_c='in_a3', di_d='in_a4'):
            if self.subtest.subtest_b(test_num=5, subtest_num=5.1, relay='KL1',
                                      err_code_a=228, err_code_b=229, err_code_c=230, err_code_d=231,
                                      position_a=True, position_b=True, position_c=False, position_d=False,
                                      di_a='in_a1', di_b='in_a2', di_c='in_a3', di_d='in_a4'):
                return True
        return False

    def st_test_52(self) -> bool:
        """
        Тест 5. Защита от потери управляемости 1 канала блока при обрыве проводов ДУ
        """
        self.logger.debug("старт теста 5.2")
        self.ctrl_kl.ctrl_relay('KL12', False)
        self.logger.debug("отключен KL12")
        sleep(1)
        if self.di_read_full.subtest_4di(test_num=5, subtest_num=5.2, err_code_a=244, err_code_b=245, err_code_c=246,
                                         err_code_d=247, position_a=False, position_b=False, position_c=False,
                                         position_d=False, di_a='in_a1', di_b='in_a2', di_c='in_a3', di_d='in_a4'):
            self.ctrl_kl.ctrl_relay('KL25', False)
            self.ctrl_kl.ctrl_relay('KL1', False)
            self.logger.debug("отключены KL1, KL25")
            return True
        return False

    def st_test_60(self) -> bool:
        """
        Тест 6. Проверка включения/выключения канала № 2 (К2) блока от кнопки «Пуск/Стоп».
        """
        self.logger.debug("старт теста 6.0")
        self.ctrl_kl.ctrl_relay('KL2', True)
        self.ctrl_kl.ctrl_relay('KL26', True)
        self.ctrl_kl.ctrl_relay('KL28', True)
        self.logger.debug("включены KL2, KL26, KL28")
        sleep(1)
        if self.di_read_full.subtest_4di(test_num=6, subtest_num=6.0, err_code_a=248, err_code_b=249, err_code_c=250,
                                         err_code_d=251, position_a=False, position_b=False, position_c=False,
                                         position_d=False, di_a='in_a1', di_b='in_a2', di_c='in_a3', di_d='in_a4'):
            return True
        return False

    def st_test_61(self) -> bool:
        """
        2.2. Включение 1 канала блока от кнопки «Пуск» 1 канала
        2.3. Проверка удержания 1 канала блока во включенном состоянии
        при подключении Rш пульта управления 1 каналом блока:
        """
        if self.subtest.subtest_a(test_num=6, subtest_num=6.1, resistance=10,
                                  err_code_a=252, err_code_b=253, err_code_c=254, err_code_d=255,
                                  position_a=False, position_b=False, position_c=True, position_d=True,
                                  di_a='in_a1', di_b='in_a2', di_c='in_a3', di_d='in_a4'):
            if self.subtest.subtest_b(test_num=6, subtest_num=6.2, relay='KL29',
                                      err_code_a=256, err_code_b=257, err_code_c=258, err_code_d=259,
                                      position_a=False, position_b=False, position_c=True, position_d=True,
                                      di_a='in_a1', di_b='in_a2', di_c='in_a3', di_d='in_a4'):
                return True
        return False

    def st_test_63(self) -> bool:
        """
        6.4. Выключение 2 канала блока от кнопки «Стоп»
        """
        self.logger.debug("старт теста 6.3")
        self.ctrl_kl.ctrl_relay('KL12', False)
        self.logger.debug("отключен KL12")
        sleep(1)
        if self.di_read_full.subtest_4di(test_num=6, subtest_num=6.3, err_code_a=260, err_code_b=261, err_code_c=262,
                                         err_code_d=263, position_a=False, position_b=False, position_c=False,
                                         position_d=False, di_a='in_a1', di_b='in_a2', di_c='in_a3', di_d='in_a4'):
            self.ctrl_kl.ctrl_relay('KL25', False)
            self.ctrl_kl.ctrl_relay('KL29', False)
            self.logger.debug("отключены KL25, KL29")
            return True
        return False

    def st_test_70(self) -> bool:
        """
        Повторяем тест 2.2. Включение 1 канала блока от кнопки «Пуск» 1 канала
        Повторяем тест 2.3. Проверка удержания 1 канала блока во включенном состоянии
        при подключении Rш пульта управления 1 каналом блока:
        """
        if self.subtest.subtest_a(test_num=7, subtest_num=7.0, resistance=10,
                                  err_code_a=252, err_code_b=253, err_code_c=254, err_code_d=255,
                                  position_a=False, position_b=False, position_c=True, position_d=True,
                                  di_a='in_a1', di_b='in_a2', di_c='in_a3', di_d='in_a4'):
            if self.subtest.subtest_b(test_num=7, subtest_num=7.1, relay='KL29',
                                      err_code_a=256, err_code_b=257, err_code_c=258, err_code_d=259,
                                      position_a=False, position_b=False, position_c=True, position_d=True,
                                      di_a='in_a1', di_b='in_a2', di_c='in_a3', di_d='in_a4'):
                return True
        return False

    def st_test_72(self) -> bool:
        """
        7. Отключение исполнительного элемента 2 канала при увеличении сопротивления цепи заземления
        """
        self.logger.debug("старт теста 7.2")
        self.resist.resist_10_to_110_ohm()
        sleep(1)
        if self.di_read_full.subtest_4di(test_num=7, subtest_num=7.2, err_code_a=264, err_code_b=265, err_code_c=266,
                                         err_code_d=267, position_a=False, position_b=False, position_c=False,
                                         position_d=False, di_a='in_a1', di_b='in_a2', di_c='in_a3', di_d='in_a4'):
            self.ctrl_kl.ctrl_relay('KL12', False)
            self.ctrl_kl.ctrl_relay('KL25', False)
            self.ctrl_kl.ctrl_relay('KL29', False)
            self.logger.debug("отключены KL12, KL25, KL29")
            return True
        return False

    def st_test_80(self) -> bool:
        """
        Повторяем тест 2.2. Включение 1 канала блока от кнопки «Пуск» 1 канала
        Повторяем тест 2.3. Проверка удержания 1 канала блока во включенном состоянии
        при подключении Rш пульта управления 1 каналом блока:
        """
        if self.subtest.subtest_a(test_num=8, subtest_num=8.0, resistance=10,
                                  err_code_a=252, err_code_b=253, err_code_c=254, err_code_d=255,
                                  position_a=False, position_b=False, position_c=True, position_d=True,
                                  di_a='in_a1', di_b='in_a2', di_c='in_a3', di_d='in_a4'):
            if self.subtest.subtest_b(test_num=8, subtest_num=8.1, relay='KL29',
                                      err_code_a=256, err_code_b=257, err_code_c=258, err_code_d=259,
                                      position_a=False, position_b=False, position_c=True, position_d=True,
                                      di_a='in_a1', di_b='in_a2', di_c='in_a3', di_d='in_a4'):
                return True
        return False

    def st_test_82(self) -> bool:
        """
        8. Защита от потери управляемости 2 канала блока при замыкании проводов ДУ
        """
        self.logger.debug("старт теста 8.2")
        self.ctrl_kl.ctrl_relay('KL11', True)
        self.logger.debug("включен KL11")
        sleep(1)
        if self.di_read_full.subtest_4di(test_num=8, subtest_num=8.2,
                                         err_code_a=268, err_code_b=269, err_code_c=270, err_code_d=271,
                                         position_a=False, position_b=False, position_c=False, position_d=False,
                                         di_a='in_a1', di_b='in_a2', di_c='in_a3', di_d='in_a4'):
            self.ctrl_kl.ctrl_relay('KL12', False)
            self.ctrl_kl.ctrl_relay('KL25', False)
            self.ctrl_kl.ctrl_relay('KL29', False)
            self.ctrl_kl.ctrl_relay('KL11', False)
            self.logger.debug("отключены KL12, KL25, KL29, KL11")
            return True
        return False

    def st_test_90(self) -> bool:
        """
        Повторяем тест 2.2. Включение 1 канала блока от кнопки «Пуск» 1 канала
        Повторяем тест 2.3. Проверка удержания 1 канала блока во включенном состоянии
        при подключении Rш пульта управления 1 каналом блока:
        """
        if self.subtest.subtest_a(test_num=9, subtest_num=9.0, resistance=10,
                                  err_code_a=252, err_code_b=253, err_code_c=254, err_code_d=255,
                                  position_a=False, position_b=False, position_c=True, position_d=True,
                                  di_a='in_a1', di_b='in_a2', di_c='in_a3', di_d='in_a4'):
            if self.subtest.subtest_b(test_num=9, subtest_num=9.1, relay='KL29',
                                      err_code_a=256, err_code_b=257, err_code_c=258, err_code_d=259,
                                      position_a=False, position_b=False, position_c=True, position_d=True,
                                      di_a='in_a1', di_b='in_a2', di_c='in_a3', di_d='in_a4'):
                return True
        return False

    def st_test_92(self):
        """
        Тест 9. Защита от потери управляемости 1 канала блока при обрыве проводов ДУ
        """
        self.logger.debug("старт теста 9.2")
        self.ctrl_kl.ctrl_relay('KL12', False)
        self.logger.debug("отключен KL12")
        sleep(1)
        if self.di_read_full.subtest_4di(test_num=9, subtest_num=9.2,
                                         err_code_a=272, err_code_b=273, err_code_c=274, err_code_d=275,
                                         position_a=False, position_b=False, position_c=False, position_d=False,
                                         di_a='in_a1', di_b='in_a2', di_c='in_a3', di_d='in_a4'):
            return True
        return False

    def st_test_bdu_dr01(self) -> bool:
        """
        Главная функция которая собирает все остальные
        """
        if self.st_test_1():
            if self.st_test_20():
                if self.st_test_21():
                    if self.st_test_23():
                        if self.st_test_30():
                            if self.st_test_32():
                                if self.st_test_40():
                                    if self.st_test_42():
                                        if self.st_test_50():
                                            if self.st_test_52():
                                                if self.st_test_60():
                                                    if self.st_test_61():
                                                        if self.st_test_63():
                                                            if self.st_test_70():
                                                                if self.st_test_72():
                                                                    if self.st_test_80():
                                                                        if self.st_test_82():
                                                                            if self.st_test_90():
                                                                                if self.st_test_92():
                                                                                    return True
        return False


if __name__ == '__main__':
    test_bdu_dr01 = TestBDUDR01()
    reset_test_bdu_dr01 = ResetRelay()
    mysql_conn_test_bdu_dr01 = MySQLConnect()
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
        my_msg(f'{mce}', 'red')
    finally:
        reset_test_bdu_dr01.reset_all()
        sys.exit()
