#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки
Тип блока: БКИ-6-3Ш
Производитель:

"""

import sys
import logging

from time import sleep

from general_func.exception import *
from general_func.database import *
from general_func.modbus import *
from general_func.resistance import Resistor
from general_func.reset import ResetRelay
from general_func.subtest import ReadOPCServer
from gui.msgbox_1 import *

__all__ = ["TestBKI6"]


class TestBKI6:

    def __init__(self):
        self.resist = Resistor()
        self.ctrl_kl = CtrlKL()
        self.di_read = DIRead()
        self.mysql_conn = MySQLConnect()
        self.di_read_full = ReadOPCServer()

        self.msg_1 = 'Убедитесь в отсутствии других блоков или соединительных кабелей в панели разъемов А'
        self.msg_2 = 'Подключите в разъем, расположенный на панели разъемов А ' \
                     'соединительный кабель для проверки блока БКИ-6-3Ш'

        logging.basicConfig(
            filename="C:\\Stend\\project_class\\log\\TestBKI63Sh.log",
            filemode="w",
            level=logging.DEBUG,
            encoding="utf-8",
            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('WARNING')
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))

    def st_test_1(self) -> bool:
        """
        Тест 1. Проверка исходного состояния контактов блока при отсутствии напряжения питания
        """
        if my_msg(self.msg_1):
            if my_msg(self.msg_2):
                pass
            else:
                return False
        else:
            return False
        self.ctrl_kl.ctrl_relay('KL22', True)
        sleep(3)
        if self.di_read_full.subtest_5di(test_num=1, subtest_num=1.0, err_code_a=123, err_code_b=123, err_code_c=124,
                                         err_code_d=125, err_code_e=125, position_a=False, position_b=True,
                                         position_c=True,
                                         position_d=False, position_e=True, di_a="in_a1", di_b='in_a7', di_c='in_a6',
                                         di_d='in_a4', di_e='in_a5'):
            return True
        return False

    def st_test_20(self) -> bool:
        """
        Тест 2. Проверка работы контактов блока при подаче питания на блок и отсутствии утечки
        """
        self.ctrl_kl.ctrl_relay('KL21', True)
        if self.sub_test(test_num=2, subtest_num=2.0, iteration=20):
            return True
        return False

    def st_test_21(self) -> bool:
        """
        2.1. Проверка установившегося состояния контактов по истечению 20 сек
        """
        if self.di_read_full.subtest_5di(test_num=2, subtest_num=2.1, err_code_a=126, err_code_b=126, err_code_c=127,
                                         err_code_d=128, err_code_e=128, position_a=False, position_b=True,
                                         position_c=True,
                                         position_d=False, position_e=True, di_a="in_a1", di_b='in_a7', di_c='in_a6',
                                         di_d='in_a4', di_e='in_a5'):
            return True
        return False

    def st_test_30(self) -> bool:
        """
        Тест 3. Проверка работы контактов реле К4 «Блокировка ВКЛ».
        """
        self.ctrl_kl.ctrl_relay('KL36', True)
        sleep(1)
        if self.di_read_full.subtest_5di(test_num=3, subtest_num=3.0, err_code_a=129, err_code_b=129, err_code_c=130,
                                         err_code_d=131, err_code_e=131, position_a=False, position_b=True,
                                         position_c=True,
                                         position_d=False, position_e=True, di_a="in_a1", di_b='in_a7', di_c='in_a6',
                                         di_d='in_a4', di_e='in_a5'):
            return True
        return False

    def st_test_31(self) -> bool:
        self.ctrl_kl.ctrl_relay('KL36', False)
        if self.sub_test(test_num=3, subtest_num=3.1, iteration=40):
            return True
        return False

    def st_test_32(self) -> bool:
        """

        :return: bool
        """
        if self.di_read_full.subtest_5di(test_num=3, subtest_num=3.2, err_code_a=132, err_code_b=132, err_code_c=133,
                                         err_code_d=134, err_code_e=134, position_a=False, position_b=True,
                                         position_c=True,
                                         position_d=False, position_e=True, di_a="in_a1", di_b='in_a7', di_c='in_a6',
                                         di_d='in_a4', di_e='in_a5'):
            return True
        return False

    def st_test_40(self) -> bool:
        """
        Тест 4. Проверка работы контактов реле К6 «Срабатывание БКИ»
        """
        self.ctrl_kl.ctrl_relay('KL22', False)
        self.resist.resist_kohm(30)
        sleep(10)
        if self.di_read_full.subtest_5di(test_num=4, subtest_num=4.0, err_code_a=135, err_code_b=135, err_code_c=136,
                                         err_code_d=137, err_code_e=137, position_a=False, position_b=True,
                                         position_c=False,
                                         position_d=True, position_e=False, di_a="in_a1", di_b='in_a7', di_c='in_a6',
                                         di_d='in_a4', di_e='in_a5'):
            return True
        return False

    def st_test_41(self) -> bool:
        """
        4.2. Отключение 30 кОм
        """
        self.resist.resist_kohm(590)
        sleep(2)
        if self.di_read_full.subtest_5di(test_num=4, subtest_num=4.1, err_code_a=138, err_code_b=138, err_code_c=139,
                                         err_code_d=140, err_code_e=140, position_a=False, position_b=True,
                                         position_c=False,
                                         position_d=False, position_e=True, di_a="in_a1", di_b='in_a7', di_c='in_a6',
                                         di_d='in_a4', di_e='in_a5'):
            return True
        return False

    def st_test_50(self) -> bool:
        """
        Тест 5. Проверка исправности контактов реле К5 «Срабатывание БКИ на сигнал
        """
        self.ctrl_kl.ctrl_relay('KL22', True)
        sleep(2)
        if self.di_read_full.subtest_5di(test_num=5, subtest_num=5.0, err_code_a=141, err_code_b=141, err_code_c=142,
                                         err_code_d=143, err_code_e=143, position_a=False, position_b=True,
                                         position_c=True,
                                         position_d=False, position_e=True, di_a="in_a1", di_b='in_a7', di_c='in_a6',
                                         di_d='in_a4', di_e='in_a5'):
            return True
        return False

    def st_test_51(self) -> bool:
        self.ctrl_kl.ctrl_relay('KL22', False)
        sleep(5)
        if self.di_read_full.subtest_5di(test_num=5, subtest_num=5.1, err_code_a=144, err_code_b=144, err_code_c=145,
                                         err_code_d=146, err_code_e=146, position_a=False, position_b=True,
                                         position_c=False,
                                         position_d=False, position_e=True, di_a="in_a1", di_b='in_a7', di_c='in_a6',
                                         di_d='in_a4', di_e='in_a5'):
            return True
        return False

    def sub_test(self, *, test_num: int, subtest_num: float, iteration):
        """
        Для теста 2.0 iteration = 20.
        Для теста 3.1 iteration = 40.
        :param test_num:
        :param subtest_num:
        :param iteration:
        :return:
        """
        self.logger.debug(f"тест {test_num}, подтест {subtest_num}")
        self.mysql_conn.mysql_ins_result(f"идёт подтест {subtest_num}", f"{test_num}")
        k1 = 0
        in_a1, in_a7 = self.di_read.di_read('in_a1', 'in_a7')
        self.logger.debug(f"положение выходов блока: {in_a1 = } is True, {in_a7 = } is False")
        while in_a1 is False and in_a7 is True and k1 <= iteration:
            sleep(0.2)
            in_a1, in_a7 = self.di_read.di_read('in_a1', 'in_a7')
            self.logger.debug(f"итерация {k1} положение выходов блока: {in_a1 = } is True, {in_a7 = } is False")
            k1 += 1
        if in_a1 is True and in_a7 is False:
            self.logger.debug(f'подтест {subtest_num} положение выходов соответствует')
            self.mysql_conn.mysql_add_message(f'подтест {subtest_num} положение выходов соответствует')
        else:
            self.mysql_conn.mysql_ins_result("неисправен", f"{test_num}")
            self.logger.debug(f'подтест {subtest_num} положение выходов не соответствует')
            self.mysql_conn.mysql_add_message(f'подтест {subtest_num} положение выходов не соответствует')
            return False

        k2 = 0
        in_a1, in_a7 = self.di_read.di_read('in_a1', 'in_a7')
        while in_a1 is True and in_a7 is False and k2 <= iteration:
            sleep(0.2)
            in_a1, in_a7 = self.di_read.di_read('in_a1', 'in_a7')
            self.logger.debug(f"итерация {k2} положение выходов блока: {in_a1 = } is False, {in_a7 = } is True")
            k2 += 1
        if in_a1 is False and in_a7 is True:
            self.logger.debug(f'подтест {subtest_num} положение выходов соответствует')
            self.mysql_conn.mysql_add_message(f'подтест {subtest_num} положение выходов соответствует')
            return True
        else:
            self.mysql_conn.mysql_ins_result("неисправен", f"{test_num}")
            self.logger.debug(f'подтест {subtest_num} положение выходов не соответствует')
            self.mysql_conn.mysql_add_message(f'подтест {subtest_num} положение выходов не соответствует')
            return False

    def st_test_bki_6_3sh(self) -> bool:
        if self.st_test_1():
            if self.st_test_20():
                if self.st_test_21():
                    if self.st_test_30():
                        if self.st_test_31():
                            if self.st_test_32():
                                if self.st_test_40():
                                    if self.st_test_41():
                                        if self.st_test_50():
                                            if self.st_test_51():
                                                return True
        return False


if __name__ == '__main__':
    test_bki6 = TestBKI6()
    reset_test_bki6 = ResetRelay()
    mysql_conn_bki6 = MySQLConnect()
    try:
        if test_bki6.st_test_bki_6_3sh():
            mysql_conn_bki6.mysql_block_good()
            my_msg('Блок исправен', 'green')
        else:
            mysql_conn_bki6.mysql_block_bad()
            my_msg('Блок неисправен', 'red')
    except OSError:
        my_msg("ошибка системы", 'red')
    except SystemError:
        my_msg("внутренняя ошибка", 'red')
    except ModbusConnectException as mce:
        my_msg(f'{mce}', 'red')
    finally:
        reset_test_bki6.reset_all()
        sys.exit()
