#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
!!! НА ИСПЫТАНИИ !!!

Алгоритм проверки
Тип блока: БДУ
Производитель: Без Производителя, Углеприбор

"""

__all__ = ["TestBDU"]

import logging
import sys
from time import sleep

from .general_func.database import *
from .general_func.exception import *
from .general_func.opc_full import ConnectOPC
from .general_func.reset import ResetRelay
from .general_func.resistance import Resistor
from .general_func.subtest import SubtestBDU
from .general_func.utils import CLILog
from .gui.msgbox_1 import *


class TestBDU:

    def __init__(self):
        self.conn_opc = ConnectOPC()
        self.resist = Resistor()
        self.mysql_conn = MySQLConnect()
        self.sub_test = SubtestBDU()
        self.reset = ResetRelay()
        self.cli_log = CLILog("debug", __name__)

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
        self.cli_log.lev_info("старт теста блока БДУ", "gray")
        if self.conn_opc.subtest_read_di(test_num=1, subtest_num=1.0, err_code=[47], position_inp=[False],
                                         di_xx=['inp_01']):
            return True
        return False

    def st_test_20(self) -> bool:
        """
        Тест-2 Проверка включения/отключения блока от кнопки пуск
        """
        self.logger.debug(f"старт теста: 2, подтест: 0")
        self.cli_log.lev_info(f"старт теста: 2, подтест: 0", "gray")
        self.conn_opc.ctrl_relay('KL2', True)
        self.logger.debug(f'включение KL2')
        self.cli_log.lev_info(f'включение KL2', "blue")
        sleep(3)
        self.logger.debug("таймаут 3 сек")
        self.cli_log.lev_debug("таймаут 3 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=2, subtest_num=2.0, err_code=[21], position_inp=[False],
                                         di_xx=['inp_01']):
            return True
        return False

    def st_test_21(self) -> bool:
        """
        Тест-2.2 Проверка канала блока от кнопки "Пуск"
        """
        self.logger.debug(f"старт теста: 2, подтест: 1")
        self.cli_log.lev_info(f"старт теста: 2, подтест: 1", "gray")
        self.resist.resist_ohm(10)
        sleep(3)
        self.logger.debug("таймаут 3 сек")
        self.cli_log.lev_debug("таймаут 3 сек", "gray")
        self.conn_opc.ctrl_relay('KL12', True)
        self.logger.debug(f'включение KL12')
        self.cli_log.lev_info(f'включение KL12', 'blue')
        sleep(3)
        self.logger.debug("таймаут 3 сек")
        self.cli_log.lev_debug("таймаут 3 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=2, subtest_num=2.1, err_code=[21], position_inp=[True],
                                         di_xx=['inp_01']):
            return True
        return False

    def st_test_22(self) -> bool:
        """
        Тест 2.3 Выключение канала блока от кнопки «Пуск» при сопротивлении 10 Ом
        """
        self.logger.debug(f"старт теста: 2, подтест: 2")
        self.cli_log.lev_info(f"старт теста: 2, подтест: 2", "gray")
        sleep(3)
        self.logger.debug("таймаут 3 сек")
        self.cli_log.lev_debug("таймаут 3 сек", "gray")
        self.conn_opc.ctrl_relay('KL12', False)
        self.logger.debug(f'отключение KL12')
        self.cli_log.lev_info(f'отключение KL12', "blue")
        sleep(3)
        self.logger.debug("таймаут 3 сек")
        self.cli_log.lev_debug("таймаут 3 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=2, subtest_num=2.2, err_code=[21], position_inp=[False],
                                         di_xx=['inp_01']):
            return True
        return False

    def st_test_30(self) -> bool:
        """
        Тест-3. Удержание исполнительного элемента при сопротивлении цепи заземления до 35 Ом
        """
        self.logger.debug(f"старт теста: 3, подтест: 0")
        self.cli_log.lev_info(f"старт теста: 3, подтест: 0", "gray")
        sleep(3)
        self.logger.debug("таймаут 3 сек")
        self.cli_log.lev_debug("таймаут 3 сек", "gray")
        self.conn_opc.ctrl_relay('KL12', True)
        self.logger.debug(f'включение KL12')
        self.cli_log.lev_info(f'включение KL12', "blue")
        sleep(0.5)
        self.logger.debug("таймаут 0.5 сек")
        self.cli_log.lev_debug("таймаут 0.5 сек", "gray")
        # Отключаем KL5, KL8 для формирования 35 Ом
        self.conn_opc.ctrl_relay('KL5', False)
        self.conn_opc.ctrl_relay('KL8', False)
        self.logger.debug(f'отключение KL5, KL8')
        self.cli_log.lev_info(f'отключение KL5, KL8', "blue")
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=3, subtest_num=3.0, err_code=[28], position_inp=[False],
                                         di_xx=['inp_01']):
            return True
        return False

    def st_test_40(self) -> bool:
        """
        Тест 4. Отключение исполнительного элемента при сопротивлении цепи заземления свыше 50 Ом
        """
        self.logger.debug(f"старт теста: 4, подтест: 0")
        self.cli_log.lev_info(f"старт теста: 4, подтест: 0", "gray")
        self.conn_opc.ctrl_relay('KL7', False)
        self.conn_opc.ctrl_relay('KL9', False)
        self.conn_opc.ctrl_relay('KL4', True)
        self.conn_opc.ctrl_relay('KL6', True)
        self.conn_opc.ctrl_relay('KL10', True)
        self.logger.debug(f'включение KL4, KL6, KL10, отключение KL7, KL9')
        self.cli_log.lev_info(f'включение KL4, KL6, KL10, отключение KL7, KL9', "blue")
        if self.conn_opc.subtest_read_di(test_num=4, subtest_num=4.0, err_code=[29], position_inp=[False],
                                         di_xx=['inp_01']):
            sleep(0.5)
            self.logger.debug("таймаут 0.5 сек")
            self.cli_log.lev_debug("таймаут 0.5 сек", "gray")
            self.conn_opc.ctrl_relay('KL12', False)
            self.logger.debug(f'отключение KL12')
            self.cli_log.lev_info(f'отключение KL12', "blue")
            return True
        return False

    def st_test_50(self) -> bool:
        """
        Тест 5. Защита от потери управляемости при замыкании проводов ДУ
        """
        self.logger.debug(f"старт теста: 5, подтест: 0")
        self.cli_log.lev_info(f"старт теста: 5, подтест: 0", "gray")
        self.resist.resist_ohm(10)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        self.conn_opc.ctrl_relay('KL12', True)
        self.logger.debug(f'включение KL12')
        self.cli_log.lev_info(f'включение KL12', "blue")
        sleep(0.5)
        self.logger.debug("таймаут 0.5 сек")
        self.cli_log.lev_debug("таймаут 0.5 сек", "gray")
        self.conn_opc.ctrl_relay('KL11', True)
        self.logger.debug(f'включение KL11')
        self.cli_log.lev_info(f'включение KL11', "blue")
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=5, subtest_num=5.0, err_code=[3], position_inp=[False],
                                         di_xx=['inp_01']):
            self.conn_opc.ctrl_relay('KL12', False)
            self.conn_opc.ctrl_relay('KL11', False)
            self.conn_opc.ctrl_relay('KL1', False)
            self.logger.debug(f'отключение KL12, KL11, KL1')
            self.cli_log.lev_info(f'отключение KL12, KL11, KL1', "blue")
            return True
        return False

    def st_test_60(self) -> bool:
        """
        Тест 6. Защита от потери управляемости при обрыве проводов ДУ
        """
        self.logger.debug(f"старт теста: 6, подтест: 0")
        self.cli_log.lev_info(f"старт теста: 6, подтест: 0", "gray")
        self.resist.resist_ohm(10)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        self.conn_opc.ctrl_relay('KL12', True)
        self.logger.debug(f'включение KL12')
        self.cli_log.lev_info(f'включение KL12', "blue")
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        self.conn_opc.ctrl_relay('KL12', False)
        self.logger.debug(f'отключение KL12')
        self.cli_log.lev_info(f'отключение KL12', "blue")
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=6, subtest_num=6.0, err_code=[4], position_inp=[False],
                                         di_xx=['inp_01']):
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

    def full_test_bdu(self) -> None:

        try:
            if self.st_test_bdu():
                self.mysql_conn.mysql_block_good()
                self.logger.debug('Блок исправен')
                self.cli_log.lev_info('Блок исправен', 'green')
                my_msg('Блок исправен', 'green')
            else:
                self.mysql_conn.mysql_block_bad()
                self.logger.debug('Блок неисправен')
                self.cli_log.lev_warning('Блок неисправен', 'red')
                my_msg('Блок неисправен', 'red')
        except OSError:
            self.logger.debug("ошибка системы")
            self.cli_log.lev_warning("ошибка системы", 'red')
            my_msg("ошибка системы", 'red')
        except SystemError:
            self.logger.debug("внутренняя ошибка")
            self.cli_log.lev_warning("внутренняя ошибка", 'red')
            my_msg("внутренняя ошибка", 'red')
        except ModbusConnectException as mce:
            self.logger.debug(f'{mce}')
            self.cli_log.lev_warning(f'{mce}', 'red')
            my_msg(f'{mce}', 'red')
        finally:

            self.conn_opc.full_relay_off()
            self.conn_opc.opc_close()
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
