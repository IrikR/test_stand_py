#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки

Тип блока: БДЗ
Производитель: Строй-энергомаш, ТЭТЗ-Инвест, нет производителя

"""

import sys
import logging

from time import sleep

from general_func.exception import *
from general_func.subtest import Subtest2in, ReadOPCServer
from general_func.database import *
from general_func.modbus import *
from general_func.reset import ResetRelay
from gui.msgbox_1 import *

__all__ = ["TestBDZ"]


class TestBDZ:

    def __init__(self):
        self.mb_ctrl = CtrlKL()
        self.di_read = DIRead()
        self.mysql_conn = MySQLConnect()
        self.subtest = Subtest2in()
        self.di_read_full = ReadOPCServer()

        self.msg_1 = "Убедитесь в отсутствии блоков в панелях разъемов. " \
                     "Вставьте испытуемый блок БДЗ в разъем Х16 на панели B"
        self.msg_2 = "Вставьте заведомо исправные блок БИ в разъем Х26 и блок БУЗ-2 в разъем Х17, " \
                     "расположенные на панели B"

        logging.basicConfig(
            filename="C:\\Stend\\project_class\\log\\TestBDZ.log",
            filemode="w",
            level=logging.DEBUG,
            encoding="utf-8",
            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('DEBUG')
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))

    def st_test_00(self) -> bool:
        self.di_read.di_read('in_a0')
        if my_msg(self.msg_1):
            if my_msg(self.msg_2):
                return True
        return False

    def st_test_10_bdz(self) -> bool:
        """
        Тест 1. Включение/выключение блока при нормальном уровне сопротивления изоляции:
        """
        self.mb_ctrl.ctrl_relay('KL21', True)
        self.mb_ctrl.ctrl_relay('KL2', True)
        self.mb_ctrl.ctrl_relay('KL66', True)
        sleep(6)
        self.mb_ctrl.ctrl_relay('KL84', True)
        sleep(2)
        self.mb_ctrl.ctrl_relay('KL84', False)
        sleep(1)
        self.mb_ctrl.ctrl_relay('KL80', True)
        sleep(0.1)
        self.mb_ctrl.ctrl_relay('KL24', True)
        sleep(5)
        if self.di_read_full.subtest_2di(test_num=1, subtest_num=1.0, err_code_a=1, err_code_b=1, position_a=True,
                                         position_b=True):
            return True
        return False

    def st_test_11_bdz(self) -> bool:
        """
        1.2.	Выключение блока
        """
        sleep(1)
        self.mb_ctrl.ctrl_relay('KL80', False)
        sleep(0.1)
        self.mb_ctrl.ctrl_relay('KL24', False)
        sleep(5)
        if self.di_read_full.subtest_2di(test_num=1, subtest_num=1.1, err_code_a=1, err_code_b=1, position_a=False,
                                         position_b=False):
            return True
        return False

    def st_test_20_bdz(self) -> bool:
        """
        # Тест 2. Блокировка включения при снижении уровня сопротивления изоляции:
        """
        sleep(1)
        self.mb_ctrl.ctrl_relay('KL22', True)
        sleep(1)
        self.mb_ctrl.ctrl_relay('KL80', True)
        sleep(0.1)
        self.mb_ctrl.ctrl_relay('KL24', True)
        sleep(5)
        if self.di_read_full.subtest_2di(test_num=2, subtest_num=2.0, err_code_a=1, err_code_b=1, position_a=False,
                                         position_b=False):
            return True
        return False

    def st_test_bdz(self) -> bool:
        if self.st_test_10_bdz():
            if self.st_test_11_bdz():
                if self.st_test_20_bdz():
                    return True
        return False


if __name__ == '__main__':
    test_bdz = TestBDZ()
    reset_test_bdz = ResetRelay()
    mysql_conn_bdz = MySQLConnect()
    try:
        if test_bdz.st_test_bdz():
            mysql_conn_bdz.mysql_block_good()
            my_msg('Блок исправен', 'green')
        else:
            mysql_conn_bdz.mysql_block_bad()
            my_msg('Блок неисправен', 'red')
    except OSError:
        my_msg("ошибка системы", 'red')
    except SystemError:
        my_msg("внутренняя ошибка", 'red')
    except ModbusConnectException as mce:
        my_msg(f'{mce}', 'red')
    finally:
        reset_test_bdz.reset_all()
        sys.exit()
