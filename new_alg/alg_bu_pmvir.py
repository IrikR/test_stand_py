# -*- coding: utf-8 -*-
"""
!!! НОВЫЙ НЕ ОБКАТАНЫЙ !!!

Алгоритм проверки

Тип блока: БУ ПМВИР (пускатель)
Производитель: Без Производителя

"""

__all__ = ["TestBUPMVIR"]

import logging
import sys
from time import sleep, time

from .general_func.database import *
from .general_func.exception import *
from .general_func.opc_full import ConnectOPC
from .general_func.reset import ResetRelay
from .general_func.resistance import Resistor
from .general_func.subtest import SubtestBDU
from .general_func.utils import CLILog
from .gui.msgbox_1 import *


class TestBUPMVIR:

    def __init__(self):
        self.conn_opc = ConnectOPC()
        self.resist = Resistor()
        self.mysql_conn = MySQLConnect()
        self.subtest = SubtestBDU()
        self.reset_relay = ResetRelay()
        self.cli_log = CLILog("debug", __name__)

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
        self.cli_log.lev_info(f"старт теста {__doc__}", "skyblue")
        if self.conn_opc.subtest_read_di(test_num=1, subtest_num=1.0,
                                         err_code=[47],
                                         position_inp=[False],
                                         di_xx=['inp_01']):
            return True
        return False

    def st_test_11(self) -> bool:
        """
        # 1.1. Проверка состояния контактов блока при подаче напряжения питания.
        :return: Bool
        """
        self.logger.debug("старт теста 1.1")
        self.cli_log.lev_info("старт теста 1.1", "gray")
        self.conn_opc.ctrl_relay('KL21', True)
        if self.conn_opc.subtest_read_di(test_num=1, subtest_num=1.1,
                                         err_code=[90],
                                         position_inp=[False],
                                         di_xx=['inp_01']):
            return True
        return False

    def st_test_20(self) -> bool:
        """
        2. Проверка включения/выключения блока от кнопки «Пуск/Стоп».
        2.1. Проверка исходного состояния блока.
        :return: Bool
        """
        if self.subtest.subtest_a_bupmvir(test_num=2, subtest_num=2.0):
            # 2.2. Выключение блока от кнопки «Стоп» при сопротивлении 10 Ом
            self.conn_opc.ctrl_relay('KL12', False)
            sleep(2)
            self.logger.debug("таймаут 2 сек")
            self.cli_log.lev_debug("таймаут 2 сек", "gray")
            if self.conn_opc.subtest_read_di(test_num=2, subtest_num=2.1,
                                             err_code=[92],
                                             position_inp=[False],
                                             di_xx=['inp_01']):
                return True
        return False

    def st_test_30(self) -> bool:
        """
        3. Проверка блокировки включения блока при снижении сопротивления изоляции контролируемого присоединения:
        :return: Bool
        """
        self.logger.debug("старт теста 3.0")
        self.cli_log.lev_info("старт теста 3.0", "gray")
        self.conn_opc.ctrl_relay('KL22', True)
        self.resist.resist_ohm(10)
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        self.conn_opc.ctrl_relay('KL12', True)
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=3, subtest_num=3.0,
                                         err_code=[93],
                                         position_inp=[False],
                                         di_xx=['inp_01']):
            self.conn_opc.ctrl_relay('KL22', False)
            self.conn_opc.ctrl_relay('KL12', False)
            return True
        return False

    def st_test_40(self) -> bool:
        """
        4.  Отключение блока при увеличении сопротивления цепи заземления на величину более 100 Ом.
        :return: Bool
        """
        if self.subtest.subtest_a_bupmvir(test_num=4, subtest_num=4.0):
            self.resist.resist_10_to_137_ohm()
            sleep(2)
            self.logger.debug("таймаут 2 сек")
            self.cli_log.lev_debug("таймаут 2 сек", "gray")
            if self.conn_opc.subtest_read_di(test_num=4, subtest_num=4.1,
                                             err_code=[94],
                                             position_inp=[False],
                                             di_xx=['inp_01']):
                self.conn_opc.ctrl_relay('KL12', False)
                return True
        return False

    def st_test_50(self) -> bool:
        """
        Тест 5. Защита от потери управляемости блока при замыкании проводов ДУ.
        :return: Bool
        """
        if self.subtest.subtest_a_bupmvir(test_num=5, subtest_num=5.0):
            self.conn_opc.ctrl_relay('KL11', True)
            sleep(1)
            self.logger.debug("таймаут 2 сек")
            self.cli_log.lev_debug("таймаут 2 сек", "gray")
            if self.conn_opc.subtest_read_di(test_num=5, subtest_num=5.1,
                                             err_code=[95],
                                             position_inp=[False],
                                             di_xx=['inp_01']):
                self.conn_opc.ctrl_relay('KL12', False)
                self.conn_opc.ctrl_relay('KL11', False)
                return True
        return False

    def st_test_60(self) -> bool:
        """
        Тест 6. Защита от потери управляемости блока при обрыве проводов ДУ
        :return: bool
        """
        if self.subtest.subtest_a_bupmvir(test_num=6, subtest_num=6.0):
            self.conn_opc.ctrl_relay('KL12', False)
            sleep(1)
            self.logger.debug("таймаут 1 сек")
            self.cli_log.lev_debug("таймаут 1 сек", "gray")
            if self.conn_opc.subtest_read_di(test_num=6, subtest_num=6.1,
                                             err_code=[96],
                                             position_inp=[False],
                                             di_xx=['inp_01']):
                return True
        return False

    def st_test_70(self) -> bool:
        """
        7. Проверка отключения блока от срабатывания защиты УМЗ.
        :return: Bool
        """
        if self.subtest.subtest_a_bupmvir(test_num=7, subtest_num=7.0):
            self.conn_opc.ctrl_relay('KL27', False)
            self.conn_opc.ctrl_relay('KL30', True)
            sleep(2)
            self.logger.debug("таймаут 2 сек")
            self.cli_log.lev_debug("таймаут 2 сек", "gray")
            self.conn_opc.ctrl_relay('KL27', True)
            sleep(6)
            self.logger.debug("таймаут 6 сек")
            self.cli_log.lev_debug("таймаут 6 сек", "gray")
            if self.conn_opc.subtest_read_di(test_num=7, subtest_num=7.1,
                                             err_code=[97],
                                             position_inp=[False],
                                             di_xx=['inp_01']):
                self.conn_opc.ctrl_relay('KL30', False)
                sleep(6)
                self.logger.debug("таймаут 6 сек")
                self.cli_log.lev_debug("таймаут 6 сек", "gray")
                if self.conn_opc.subtest_read_di(test_num=7, subtest_num=7.2,
                                                 err_code=[98],
                                                 position_inp=[True],
                                                 di_xx=['inp_01']):
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

    def full_test_bu_pmvir(self) -> None:
        try:
            start_time = time()
            result_test = self.st_test_bu_pmvir()
            end_time = time()
            time_spent = end_time - start_time
            self.cli_log.lev_info(f"Время выполнения: {time_spent}", "gray")
            self.logger.debug(f"Время выполнения: {time_spent}")
            self.mysql_conn.mysql_add_message(f"Время выполнения: {time_spent}")
            if result_test:
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
        except AttributeError as ae:
            self.logger.debug(f"Неверный атрибут. {ae}")
            self.cli_log.lev_warning(f"Неверный атрибут. {ae}", 'red')
            my_msg(f"Неверный атрибут. {ae}", 'red')
        except ValueError as ve:
            self.logger.debug(f"Некорректное значение для переменной. {ve}")
            self.cli_log.lev_warning(f"Некорректное значение для переменной. {ve}", 'red')
            my_msg(f"Некорректное значение для переменной. {ve}", 'red')
        finally:
            self.conn_opc.full_relay_off()
            self.conn_opc.opc_close()
            sys.exit()
