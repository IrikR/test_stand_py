#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки

Тип блока: БУ ПМВИР (пускатель)
Производитель: Без Производителя

"""

import sys
import logging

from time import sleep

from general_func.exception import *
from general_func.database import *
from general_func.modbus import *
from general_func.subtest import SubtestBDU, ReadOPCServer
from general_func.resistance import Resistor
from general_func.reset import ResetRelay
from gui.msgbox_1 import *

__all__ = ["TestBUPMVIR"]


class TestBUPMVIR:

    def __init__(self):
        self.resist = Resistor()
        self.ctrl_kl = CtrlKL()
        self.mysql_conn = MySQLConnect()
        self.subtest = SubtestBDU()
        self.di_read_full = ReadOPCServer()
        
        logging.basicConfig(
            filename="C:\\Stend\\project_class\\log\\TestBUPMVIR.log",
            filemode="w",
            level=logging.DEBUG,
            encoding="utf-8",
            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('DEBUG')
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))

    def st_test_10(self) -> bool:
        """
        Тест 1. Проверка исходного состояния блока:
        :return: bool
        """
        if self.di_read_full.subtest_1di(test_num=1, subtest_num=1.0, err_code=47):
            pass
        else:
            return False

    def st_test_11(self) -> bool:
        """
        # 1.1. Проверка состояния контактов блока при подаче напряжения питания.
        :return: bool
        """
        self.logger.debug("старт теста 1.1")
        self.ctrl_kl.ctrl_relay('KL21', True)
        self.logger.debug("включение KL21")
        if self.di_read_full.subtest_1di(test_num=1, subtest_num=1.1, err_code=90, position=False):
            return True
        return False

    def st_test_20(self) -> bool:
        """
        2. Проверка включения/выключения блока от кнопки «Пуск/Стоп».
        2.1. Проверка исходного состояния блока.
        :return: bool
        """
        if self.subtest.subtest_a_bupmvir(test_num=2, subtest_num=2.0):
            # 2.2. Выключение блока от кнопки «Стоп» при сопротивлении 10 Ом
            self.ctrl_kl.ctrl_relay('KL12', False)
            self.logger.debug("отключение KL12")
            sleep(2)
            if self.di_read_full.subtest_1di(test_num=2, subtest_num=2.1, err_code=92, position=False):
                return True
        return False

    def st_test_30(self) -> bool:
        """
        3. Проверка блокировки включения блока при снижении сопротивления изоляции контролируемого присоединения:
        :return: bool
        """
        self.logger.debug("старт теста 3.0")
        self.ctrl_kl.ctrl_relay('KL22', True)
        self.logger.debug("включение KL22")
        self.resist.resist_ohm(10)
        sleep(2)
        self.ctrl_kl.ctrl_relay('KL12', True)
        self.logger.debug("включение KL12")
        sleep(2)
        if self.di_read_full.subtest_1di(test_num=3, subtest_num=3.0, err_code=93, position=False):
            self.ctrl_kl.ctrl_relay('KL22', False)
            self.ctrl_kl.ctrl_relay('KL12', False)
            self.logger.debug("отключение KL22, KL12")
            return True
        return False

    def st_test_40(self) -> bool:
        """
        4.  Отключение блока при увеличении сопротивления цепи заземления на величину более 100 Ом.
        :return: bool
        """
        if self.subtest.subtest_a_bupmvir(test_num=4, subtest_num=4.0):
            self.resist.resist_10_to_137_ohm()
            sleep(2)
            if self.di_read_full.subtest_1di(test_num=4, subtest_num=4.1, err_code=94, position=False):
                self.ctrl_kl.ctrl_relay('KL12', False)
                self.logger.debug("отключение KL12")
                return True
        return False

    def st_test_50(self) -> bool:
        """
        Тест 5. Защита от потери управляемости блока при замыкании проводов ДУ.
        :return: bool
        """
        if self.subtest.subtest_a_bupmvir(test_num=5, subtest_num=5.0):
            self.ctrl_kl.ctrl_relay('KL11', True)
            self.logger.debug("включение KL11")
            sleep(1)
            if self.di_read_full.subtest_1di(test_num=5, subtest_num=5.1, err_code=95, position=False):
                self.ctrl_kl.ctrl_relay('KL12', False)
                self.ctrl_kl.ctrl_relay('KL11', False)
                self.logger.debug("отключение KL12, KL11")
                return True
        return False

    def st_test_60(self) -> bool:
        """
        Тест 6. Защита от потери управляемости блока при обрыве проводов ДУ
        :return: bool
        """
        if self.subtest.subtest_a_bupmvir(test_num=6, subtest_num=6.0):
            self.ctrl_kl.ctrl_relay('KL12', False)
            self.logger.debug("отключение KL12")
            sleep(1)
            if self.di_read_full.subtest_1di(test_num=6, subtest_num=6.1, err_code=96, position=False):
                return True
        return False

    def st_test_70(self) -> bool:
        """
        7. Проверка отключения блока от срабатывания защиты УМЗ.
        :return: bool
        """
        if self.subtest.subtest_a_bupmvir(test_num=7, subtest_num=7.0):
            self.ctrl_kl.ctrl_relay('KL27', False)
            self.ctrl_kl.ctrl_relay('KL30', True)
            self.logger.debug("отключение KL27, KL30")
            sleep(2)
            self.ctrl_kl.ctrl_relay('KL27', True)
            self.logger.debug("включение KL27")
            sleep(6)
            if self.di_read_full.subtest_1di(test_num=7, subtest_num=7.1, err_code=97, position=False):
                self.ctrl_kl.ctrl_relay('KL30', False)
                self.logger.debug("отключение KL30")
                sleep(6)
                if self.di_read_full.subtest_1di(test_num=7, subtest_num=7.2, err_code=98, position=True):
                    return True
        return False

    def st_test_bu_pmvir(self) -> bool:
        """

        :return: bool
        """
        if self.st_test_10():
            if self.st_test_11():
                if self.st_test_20():
                    if self.st_test_30():
                        if self.st_test_40():
                            if self.st_test_50():
                                if self.st_test_60():
                                    if self.st_test_70():
                                        return True
        return False


if __name__ == '__main__':
    test_bu_pmvir = TestBUPMVIR()
    reset_test_bu_pmvir = ResetRelay()
    mysql_conn_bu_pmvir = MySQLConnect()
    try:
        if test_bu_pmvir.st_test_bu_pmvir():
            mysql_conn_bu_pmvir.mysql_block_good()
            my_msg('Блок исправен', 'green')
        else:
            mysql_conn_bu_pmvir.mysql_block_bad()
            my_msg('Блок неисправен', 'red')
    except OSError:
        my_msg("ошибка системы", 'red')
    except SystemError:
        my_msg("внутренняя ошибка", 'red')
    except ModbusConnectException as mce:
        my_msg(f'{mce}', 'red')
    finally:
        reset_test_bu_pmvir.reset_all()
        sys.exit()
