#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
!!! НА ИСПЫТАНИИ !!!

Алгоритм проверки
Тип блока: БДУ
Производитель: Без Производителя, Углеприбор

"""


import sys
import logging

from time import sleep

from .general_func.exception import *
from .general_func.subtest import SubtestBDU, ReadOPCServer
from .general_func.database import *
from .general_func.modbus import *
from .general_func.resistance import Resistor
from .general_func.reset import ResetRelay
from .gui.msgbox_1 import *
from .general_func.utils import CLILog

__all__ = ["TestBDU"]


class TestBDU:

    def __init__(self):
        self.resist = Resistor()
        self.ctrl_kl = CtrlKL()
        self.mysql_conn = MySQLConnect()
        self.sub_test = SubtestBDU()
        self.di_read_full = ReadOPCServer()
        self.reset = ResetRelay()
        self.cli_log = CLILog(True)

        logging.basicConfig(
            filename="C:\\Stend\\project_class\\log\\TestBDU.log",
            filemode="w",
            level=logging.DEBUG,
            encoding="utf-8",
            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('DEBUG')
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))

    def st_test_10(self) -> bool:
        """
        Тест 1. проверка исходного состояния блока
        """
        self.cli_log.log_msg("старт теста блока БДУ", "gray")
        if self.di_read_full.subtest_1di(test_num=1, subtest_num=1.0, err_code=47, di_a='in_a1'):
            return True
        return False

    def st_test_20(self) -> bool:
        """
        Тест-2 Проверка включения/отключения блока от кнопки пуск
        """
        self.logger.debug(f"старт теста: 2, подтест: 0")
        self.cli_log.log_msg(f"старт теста: 2, подтест: 0", "gray")
        self.ctrl_kl.ctrl_relay('KL2', True)
        self.logger.debug(f'включение KL2')
        self.cli_log.log_msg(f'включение KL2', "blue")
        sleep(3)
        if self.di_read_full.subtest_1di(test_num=2, subtest_num=2.0, err_code=21, position=False, di_a='in_a1'):
            return True
        return False

    def st_test_21(self) -> bool:
        """
        Тест-2.2 Проверка канала блока от кнопки "Пуск"
        """
        self.logger.debug(f"старт теста: 2, подтест: 1")
        self.cli_log.log_msg(f"старт теста: 2, подтест: 1", "gray")
        self.resist.resist_ohm(10)
        sleep(3)
        self.ctrl_kl.ctrl_relay('KL12', True)
        self.logger.debug(f'включение KL12')
        self.cli_log.log_msg(f'включение KL12', 'blue')
        sleep(3)
        if self.di_read_full.subtest_1di(test_num=2, subtest_num=2.1, err_code=21, position=True, di_a='in_a1'):
            return True
        return False

    def st_test_22(self) -> bool:
        """
        Тест 2.3 Выключение канала блока от кнопки «Пуск» при сопротивлении 10 Ом
        """
        self.logger.debug(f"старт теста: 2, подтест: 2")
        self.cli_log.log_msg(f"старт теста: 2, подтест: 2", "gray")
        sleep(3)
        self.ctrl_kl.ctrl_relay('KL12', False)
        self.logger.debug(f'отключение KL12')
        self.cli_log.log_msg(f'отключение KL12', "blue")
        sleep(3)
        if self.di_read_full.subtest_1di(test_num=2, subtest_num=2.2, err_code=21, position=False, di_a='in_a1'):
            return True
        return False

    def st_test_30(self) -> bool:
        """
        Тест-3. Удержание исполнительного элемента при сопротивлении цепи заземления до 35 Ом
        """
        self.logger.debug(f"старт теста: 3, подтест: 0")
        self.cli_log.log_msg(f"старт теста: 3, подтест: 0", "gray")
        sleep(3)
        self.ctrl_kl.ctrl_relay('KL12', True)
        self.logger.debug(f'включение KL12')
        self.cli_log.log_msg(f'включение KL12', "blue")
        sleep(0.5)
        # Отключаем KL5, KL8 для формирования 35 Ом
        self.ctrl_kl.ctrl_relay('KL5', False)
        self.ctrl_kl.ctrl_relay('KL8', False)
        self.logger.debug(f'отключение KL5, KL8')
        self.cli_log.log_msg(f'отключение KL5, KL8', "blue")
        sleep(1)
        if self.di_read_full.subtest_1di(test_num=3, subtest_num=3.0, err_code=28, position=False, di_a='in_a1'):
            return True
        return False

    def st_test_40(self) -> bool:
        """
        Тест 4. Отключение исполнительного элемента при сопротивлении цепи заземления свыше 50 Ом
        """
        self.logger.debug(f"старт теста: 4, подтест: 0")
        self.cli_log.log_msg(f"старт теста: 4, подтест: 0", "gray")
        self.ctrl_kl.ctrl_relay('KL7', False)
        self.ctrl_kl.ctrl_relay('KL9', False)
        self.ctrl_kl.ctrl_relay('KL4', True)
        self.ctrl_kl.ctrl_relay('KL6', True)
        self.ctrl_kl.ctrl_relay('KL10', True)
        self.logger.debug(f'включение KL4, KL6, KL10, отключение KL7, KL9')
        self.cli_log.log_msg(f'включение KL4, KL6, KL10, отключение KL7, KL9', "blue")
        if self.di_read_full.subtest_1di(test_num=4, subtest_num=4.0, err_code=29, position=False, di_a='in_a1'):
            sleep(0.5)
            self.ctrl_kl.ctrl_relay('KL12', False)
            self.logger.debug(f'отключение KL12')
            self.cli_log.log_msg(f'отключение KL12', "blue")
            return True
        return False

    def st_test_50(self) -> bool:
        """
        Тест 5. Защита от потери управляемости при замыкании проводов ДУ
        """
        self.logger.debug(f"старт теста: 5, подтест: 0")
        self.cli_log.log_msg(f"старт теста: 5, подтест: 0", "gray")
        self.resist.resist_ohm(10)
        sleep(1)
        self.ctrl_kl.ctrl_relay('KL12', True)
        self.logger.debug(f'включение KL12')
        self.cli_log.log_msg(f'включение KL12', "blue")
        sleep(0.5)
        self.ctrl_kl.ctrl_relay('KL11', True)
        self.logger.debug(f'включение KL11')
        self.cli_log.log_msg(f'включение KL11', "blue")
        sleep(1)
        if self.di_read_full.subtest_1di(test_num=5, subtest_num=5.0, err_code=3, position=False, di_a='in_a1'):
            self.ctrl_kl.ctrl_relay('KL12', False)
            self.ctrl_kl.ctrl_relay('KL11', False)
            self.ctrl_kl.ctrl_relay('KL1', False)
            self.logger.debug(f'отключение KL12, KL11, KL1')
            self.cli_log.log_msg(f'отключение KL12, KL11, KL1', "blue")
            return True
        return False

    def st_test_60(self) -> bool:
        """
        Тест 6. Защита от потери управляемости при обрыве проводов ДУ
        """
        self.logger.debug(f"старт теста: 6, подтест: 0")
        self.cli_log.log_msg(f"старт теста: 6, подтест: 0", "gray")
        self.resist.resist_ohm(10)
        sleep(1)
        self.ctrl_kl.ctrl_relay('KL12', True)
        self.logger.debug(f'включение KL12')
        self.cli_log.log_msg(f'включение KL12', "blue")
        sleep(1)
        self.ctrl_kl.ctrl_relay('KL12', False)
        self.logger.debug(f'отключение KL12')
        self.cli_log.log_msg(f'отключение KL12', "blue")
        sleep(1)
        if self.di_read_full.subtest_1di(test_num=6, subtest_num=6.0, err_code=4, position=False, di_a='in_a1'):
            return True
        return False

    def st_test_bdu(self) -> bool:
        """
            Главная функция которая собирает все остальные
        """
        if self.st_test_10():
            if self.st_test_20():
                if self.st_test_21():
                    if self.st_test_22():
                        if self.st_test_30():
                            if self.st_test_40():
                                if self.st_test_50():
                                    if self.st_test_60():
                                        return True
        return False

    def full_test_bdu(self):

        try:
            if self.st_test_bdu():
                self.mysql_conn.mysql_block_good()
                my_msg('Блок исправен', 'green')
            else:
                self.mysql_conn.mysql_block_bad()
                my_msg('Блок неисправен', 'red')
        except OSError:
            my_msg("ошибка системы", 'red')
        except SystemError:
            my_msg("внутренняя ошибка", 'red')
        except ModbusConnectException as mce:
            my_msg(f'{mce}', 'red')
        finally:
            self.reset.reset_all()
            sys.exit()


if __name__ == '__main__':
    test_bdu = TestBDU()
    test_bdu.full_test_bdu()
    # reset_test_bdu = ResetRelay()
    # mysql_conn_test_bdu = MySQLConnect()
    # try:
    #     if test_bdu.st_test_bdu():
    #         mysql_conn_test_bdu.mysql_block_good()
    #         my_msg('Блок исправен', 'green')
    #     else:
    #         mysql_conn_test_bdu.mysql_block_bad()
    #         my_msg('Блок неисправен', 'red')
    # except OSError:
    #     my_msg("ошибка системы", 'red')
    # except SystemError:
    #     my_msg("внутренняя ошибка", 'red')
    # except ModbusConnectException as mce:
    #     my_msg(f'{mce}', 'red')
    # finally:
    #     reset_test_bdu.reset_all()
    #     sys.exit()
