# -*- coding: utf-8 -*-
"""
!!! НОВЫЙ НЕ ОБКАТАНЫЙ !!!

Тип блока: БДУ-Р-Т
Производитель: Нет производителя, ТЭТЗ-Инвест, Стройэнергомаш

"""

__all__ = ["TestBDURT"]

import logging
import sys
from time import sleep

from .general_func.database import *
from .general_func.exception import *
from .general_func.opc_full import ConnectOPC
from .general_func.reset import ResetRelay
from .general_func.resistance import Resistor
from .general_func.subtest import Subtest2in
from .general_func.utils import CLILog
from .gui.msgbox_1 import *


class TestBDURT:

    def __init__(self):
        self.conn_opc = ConnectOPC()
        self.resist = Resistor()
        self.mysql_conn = MySQLConnect()
        self.subtest = Subtest2in()
        self.reset_relay = ResetRelay()
        self.cli_log = CLILog("debug", __name__)

        logging.basicConfig(
            filename="C:\\Stend\\project_class\\log\\TestBDURT.log",
            filemode="w",
            level=logging.DEBUG,
            encoding="utf-8",
            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('DEBUG')
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))

    def st_test_1(self) -> bool:
        self.cli_log.lev_info(f"старт теста {__doc__}", "skyblue")
        if self.conn_opc.subtest_read_di(test_num=1, subtest_num=1.0,
                                         err_code=[288, 288],
                                         position_inp=[False, False],
                                         di_xx=["inp_01", "inp_02"]):
            return True
        return False

    def st_test_20(self) -> bool:
        """
        Тест 2. Проверка включения/выключения блока от кнопки «Пуск/Стоп» в режиме «Вперед».
        """
        self.logger.debug("старт теста 2.0")
        self.conn_opc.ctrl_relay('KL2', True)
        self.logger.debug("включен KL2")
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=2, subtest_num=2.0,
                                         err_code=[290, 291],
                                         position_inp=[False, False],
                                         di_xx=["inp_01", "inp_02"]):
            return True
        return False

    def st_test_21(self) -> bool:
        """
        2.2. Включение блока от кнопки «Пуск» в режиме «Вперёд»
        2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        """
        if self.subtest.subtest_a_bdu(test_num=2, subtest_num=2.1, err_code_a=292, err_code_b=293,
                                      position_a=True, position_b=False):
            if self.subtest.subtest_b_bdu(test_num=2, subtest_num=2.2, err_code_a=294, err_code_b=295,
                                          position_a=True, position_b=False):
                return True
        return False

    def st_test_23(self) -> bool:
        """
        2.4. Выключение блока в режиме «Вперед» от кнопки «Стоп»
        """
        self.logger.debug("старт теста 2.3")
        self.conn_opc.ctrl_relay('KL12', False)
        self.logger.debug(' включен KL12')
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=2, subtest_num=2.3,
                                         err_code=[296, 297],
                                         position_inp=[False, False],
                                         di_xx=["inp_01", "inp_02"]):
            self.conn_opc.ctrl_relay('KL25', False)
            self.conn_opc.ctrl_relay('KL1', False)
            self.logger.debug(' отключены KL25, KL1')
            return True
        return False

    def st_test_30(self) -> bool:
        """
        Тест 3. Проверка включения/выключения блока от кнопки «Пуск/Стоп» в режиме «Назад»
        3.1. Включение блока от кнопки «Пуск» в режиме «Назад»
        """
        self.logger.debug("старт теста 3.0")
        self.conn_opc.ctrl_relay('KL26', True)
        self.logger.debug(' включен KL26')
        self.resist.resist_ohm(10)
        self.conn_opc.ctrl_relay('KL12', True)
        self.logger.debug(' включен KL12')
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=3, subtest_num=3.0,
                                         err_code=[298, 299],
                                         position_inp=[False, True],
                                         di_xx=["inp_01", "inp_02"]):
            return True
        return False

    def st_test_31(self) -> bool:
        """
        3.2. Проверка удержания контактов К5.2 режима «Назад» блока во включенном состоянии
        при подключении Rш пульта управления:
        """
        self.logger.debug("старт теста 3.1")
        self.conn_opc.ctrl_relay('KL27', True)
        self.conn_opc.ctrl_relay('KL1', True)
        self.conn_opc.ctrl_relay('KL25', True)
        self.logger.debug(' включены KL27, KL25, KL1')
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=3, subtest_num=3.1,
                                         err_code=[300, 301],
                                         position_inp=[True, False],
                                         di_xx=["inp_01", "inp_02"]):
            return True
        return False

    def st_test_32(self) -> bool:
        """
        3.3. Выключение блока в режиме «Вперед» от кнопки «Стоп»
        """
        self.logger.debug("старт теста 3.2")
        self.conn_opc.ctrl_relay('KL12', False)
        self.logger.debug(' отключен KL12')
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=3, subtest_num=3.2,
                                         err_code=[302, 303],
                                         position_inp=[False, False],
                                         di_xx=["inp_01", "inp_02"]):
            self.conn_opc.ctrl_relay('KL26', False)
            self.conn_opc.ctrl_relay('KL27', False)
            self.conn_opc.ctrl_relay('KL1', False)
            self.conn_opc.ctrl_relay('KL25', False)
            self.logger.debug(' отключены KL26, KL27, KL1, KL25')
            return True
        return False

    def st_test_40(self) -> bool:
        """
        Повторяем тест 2.2. Включение блока от кнопки «Пуск» в режиме «Вперёд»
        Повторяем тест 2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        """
        if self.subtest.subtest_a_bdu(test_num=4, subtest_num=4.0, err_code_a=292, err_code_b=293,
                                      position_a=True, position_b=False):
            if self.subtest.subtest_b_bdu(test_num=4, subtest_num=4.1, err_code_a=294, err_code_b=295,
                                          position_a=True, position_b=False):
                return True
        return False

    def st_test_42(self) -> bool:
        """
        # 4. Отключение исполнительного элемента при увеличении сопротивления цепи заземления на величину свыше 50 Ом
        """
        self.logger.debug("старт теста 4.2")
        self.resist.resist_10_to_50_ohm()
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=4, subtest_num=4.2,
                                         err_code=[304, 305],
                                         position_inp=[False, False],
                                         di_xx=["inp_01", "inp_02"]):
            self.conn_opc.ctrl_relay('KL12', False)
            self.conn_opc.ctrl_relay('KL25', False)
            self.conn_opc.ctrl_relay('KL1', False)
            self.logger.debug(' отключены KL12, KL25, KL1')
            return True
        return False

    def st_test_50(self) -> bool:
        """
        Повторяем тест 2.2. Включение блока от кнопки «Пуск» в режиме «Вперёд»
        Повторяем тест 2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        """
        if self.subtest.subtest_a_bdu(test_num=5, subtest_num=5.0, err_code_a=292, err_code_b=293,
                                      position_a=True, position_b=False):
            if self.subtest.subtest_b_bdu(test_num=5, subtest_num=5.1, err_code_a=294, err_code_b=295,
                                          position_a=True, position_b=False):
                return True
        return False

    def st_test_52(self) -> bool:
        """
        # 5. Защита от потери управляемости при замыкании проводов ДУ
        """
        self.logger.debug("старт теста 5.2")
        self.conn_opc.ctrl_relay('KL11', True)
        self.logger.debug(' включен KL11')
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=5, subtest_num=5.2,
                                         err_code=[306, 307],
                                         position_inp=[False, False],
                                         di_xx=["inp_01", "inp_02"]):
            self.conn_opc.ctrl_relay('KL12', False)
            self.conn_opc.ctrl_relay('KL1', False)
            self.conn_opc.ctrl_relay('KL25', False)
            self.conn_opc.ctrl_relay('KL11', False)
            self.logger.debug(' отключены KL12, KL1, KL25, KL11')
            return True
        return False

    def st_test_60(self) -> bool:
        """
        Повторяем тест 2.2. Включение блока от кнопки «Пуск» в режиме «Вперёд»
        Повторяем тест 2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        """
        if self.subtest.subtest_a_bdu(test_num=6, subtest_num=6.0, err_code_a=292, err_code_b=293,
                                      position_a=True, position_b=False):
            if self.subtest.subtest_b_bdu(test_num=6, subtest_num=6.1, err_code_a=294, err_code_b=295,
                                          position_a=True, position_b=False):
                return True
        return False

    def st_test_62(self) -> bool:
        """
        # Тест 6. Защита от потери управляемости при обрыве проводов ДУ
        """
        self.logger.debug("старт теста 6.2")
        self.conn_opc.ctrl_relay('KL12', False)
        self.logger.debug(' отключен KL12')
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=6, subtest_num=6.2,
                                         err_code=[308, 309],
                                         position_inp=[False, False],
                                         di_xx=["inp_01", "inp_02"]):
            return True
        return False

    def st_test_70(self) -> bool:
        """
        # Тест 7. Проверка работоспособности функции "Проверка" блока
        """
        self.logger.debug("старт теста 7.0")
        self.conn_opc.ctrl_relay('KL24', True)
        self.logger.debug(' включен KL24')
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=7, subtest_num=7.0,
                                         err_code=[310, 311],
                                         position_inp=[False, True],
                                         di_xx=["inp_01", "inp_02"]):
            return True
        return False

    def st_test_bdu_r_t(self) -> bool:
        """
        Главная функция которая собирает все остальные
        """
        if self.st_test_1():
            if self.st_test_20():
                if self.st_test_21():
                    if self.st_test_23():
                        if self.st_test_30():
                            if self.st_test_31():
                                if self.st_test_32():
                                    if self.st_test_40():
                                        if self.st_test_42():
                                            if self.st_test_50():
                                                if self.st_test_52():
                                                    if self.st_test_60():
                                                        if self.st_test_62():
                                                            if self.st_test_70():
                                                                return True
        return False

    def full_test_bdu_r_t(self) -> None:
        try:
            if self.st_test_bdu_r_t():
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
