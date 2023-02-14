# -*- coding: utf-8 -*-
"""
!!! НОВЫЙ НЕ ОБКАТАНЫЙ !!!

Алгоритм проверки

Тип блока: БДЗ
Производитель: Строй-энергомаш, ТЭТЗ-Инвест, нет производителя

"""

__all__ = ["TestBDZ"]

import logging
import sys
from time import sleep

from .general_func.database import *
from .general_func.exception import *
from .general_func.opc_full import ConnectOPC
from .general_func.reset import ResetRelay
from .general_func.subtest import Subtest2in
from .general_func.utils import CLILog
from .gui.msgbox_1 import *


class TestBDZ:

    def __init__(self):
        self.conn_opc = ConnectOPC()
        self.mysql_conn = MySQLConnect()
        self.subtest = Subtest2in()
        self.reset_relay = ResetRelay()
        self.cli_log = CLILog("debug", __name__)

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
        self.cli_log.lev_info(f"старт теста {__doc__}", "skyblue")
        self.conn_opc.simplified_read_di(['inp_14', 'inp_15'])
        if my_msg(self.msg_1):
            if my_msg(self.msg_2):
                return True
        return False

    def st_test_10_bdz(self) -> bool:
        """
        Тест 1. Включение/выключение блока при нормальном уровне сопротивления изоляции:
        """
        self.conn_opc.ctrl_relay('KL21', True)
        self.conn_opc.ctrl_relay('KL2', True)
        self.conn_opc.ctrl_relay('KL66', True)
        sleep(6)
        self.logger.debug("таймаут 6 сек")
        self.cli_log.lev_debug("таймаут 6 сек", "gray")
        self.conn_opc.ctrl_relay('KL84', True)
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        self.conn_opc.ctrl_relay('KL84', False)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        self.conn_opc.ctrl_relay('KL80', True)
        sleep(0.1)
        self.logger.debug("таймаут 0.1 сек")
        self.cli_log.lev_debug("таймаут 0.1 сек", "gray")
        self.conn_opc.ctrl_relay('KL24', True)
        sleep(5)
        self.logger.debug("таймаут 5 сек")
        self.cli_log.lev_debug("таймаут 5 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=1, subtest_num=1.0,
                                         err_code=[1, 1],
                                         position_inp=[True, True],
                                         di_xx=['inp_01', 'inp_02']):
            return True
        return False

    def st_test_11_bdz(self) -> bool:
        """
        1.2.	Выключение блока
        """
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        self.conn_opc.ctrl_relay('KL80', False)
        sleep(0.1)
        self.logger.debug("таймаут 0.1 сек")
        self.cli_log.lev_debug("таймаут 0.1 сек", "gray")
        self.conn_opc.ctrl_relay('KL24', False)
        sleep(5)
        self.logger.debug("таймаут 5 сек")
        self.cli_log.lev_debug("таймаут 5 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=1, subtest_num=1.1,
                                         err_code=[1, 1],
                                         position_inp=[False, False],
                                         di_xx=['inp_01', 'inp_02']):
            return True
        return False

    def st_test_20_bdz(self) -> bool:
        """
        # Тест 2. Блокировка включения при снижении уровня сопротивления изоляции:
        """
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        self.conn_opc.ctrl_relay('KL22', True)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        self.conn_opc.ctrl_relay('KL80', True)
        sleep(0.1)
        self.logger.debug("таймаут 0.1 сек")
        self.cli_log.lev_debug("таймаут 0.1 сек", "gray")
        self.conn_opc.ctrl_relay('KL24', True)
        sleep(5)
        self.logger.debug("таймаут 5 сек")
        self.cli_log.lev_debug("таймаут 5 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=2, subtest_num=2.0,
                                         err_code=[1, 1],
                                         position_inp=[False,False],
                                         di_xx=['inp_01', 'inp_02']):
            return True
        return False

    def st_test_bdz(self) -> bool:
        if self.st_test_00():
            if self.st_test_10_bdz():
                if self.st_test_11_bdz():
                    if self.st_test_20_bdz():
                        return True
        return False

    def full_test_bdz(self) -> None:
        try:
            if self.st_test_bdz():
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
