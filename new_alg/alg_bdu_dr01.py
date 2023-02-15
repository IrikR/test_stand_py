# -*- coding: utf-8 -*-
"""
!!! НОВЫЙ НЕ ОБКАТАНЫЙ !!!

Алгоритм проверки

Тип блока: БДУ-ДР.01
Производитель: Нет производителя, ДонЭнергоЗавод

"""

__all__ = ["TestBDUDR01"]

import logging
import sys
from time import sleep, time

from .general_func.database import *
from .general_func.exception import *
from .general_func.opc_full import ConnectOPC
from .general_func.reset import ResetRelay
from .general_func.resistance import Resistor
from .general_func.subtest import Subtest4in
from .general_func.utils import CLILog
from .gui.msgbox_1 import *


class TestBDUDR01:

    def __init__(self):
        self.conn_opc = ConnectOPC()
        self.resist = Resistor()
        self.mysql_conn = MySQLConnect()
        self.subtest = Subtest4in()
        self.reset_relay = ResetRelay()
        self.cli_log = CLILog("debug", __name__)

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
        self.cli_log.lev_info(f"старт теста {__doc__}", "skyblue")
        if self.conn_opc.subtest_read_di(test_num=1, subtest_num=1.0, 
                                         err_code=[216, 217, 218, 219], 
                                         position_inp=[False, False, False, False], 
                                         di_xx=['inp_01', 'inp_02', 'inp_03', 'inp_04']):
            return True
        return False

    def st_test_20(self) -> bool:
        """
        Тест 2. Проверка включения/выключения канала № 1 (К1) блока от кнопки «Пуск/Стоп».
        """
        self.logger.debug("старт теста 2.0")
        self.conn_opc.ctrl_relay('KL2', True)
        if self.conn_opc.subtest_read_di(test_num=2, subtest_num=2.0,
                                         err_code=[220, 221, 222, 223],
                                         position_inp=[False, False, False, False],
                                         di_xx=['inp_01', 'inp_02', 'inp_03', 'inp_04']):
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
                                  di_a='inp_01', di_b='inp_02', di_c='inp_03', di_d='inp_04'):
            if self.subtest.subtest_b(test_num=2, subtest_num=2.2, relay='KL1',
                                      err_code_a=228, err_code_b=229, err_code_c=230, err_code_d=231,
                                      position_a=True, position_b=True, position_c=False, position_d=False,
                                      di_a='inp_01', di_b='inp_02', di_c='inp_03', di_d='inp_04'):
                return True
        return False

    def st_test_23(self) -> bool:
        """
        2.4. Выключение 1 канала блока от кнопки «Стоп»
        """
        self.logger.debug("старт теста 2.3")
        self.conn_opc.ctrl_relay('KL12', False)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=2, subtest_num=2.3,
                                         err_code=[232, 233, 234, 235],
                                         position_inp=[False, False, False, False],
                                         di_xx=['inp_01', 'inp_02', 'inp_03', 'inp_04']):
            self.conn_opc.ctrl_relay('KL25', False)
            self.conn_opc.ctrl_relay('KL1', False)
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
                                  di_a='inp_01', di_b='inp_02', di_c='inp_03', di_d='inp_04'):
            if self.subtest.subtest_b(test_num=3, subtest_num=3.1, relay='KL1',
                                      err_code_a=228, err_code_b=229, err_code_c=230, err_code_d=231,
                                      position_a=True, position_b=True, position_c=False, position_d=False,
                                      di_a='inp_01', di_b='inp_02', di_c='inp_03', di_d='inp_04'):
                return True
        return False

    def st_test_32(self) -> bool:
        """
        3. Отключение исполнительного элемента 1 канала при увеличении сопротивления цепи заземления
        """
        self.logger.debug("старт теста 3.2")
        self.resist.resist_10_to_110_ohm()
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=3, subtest_num=3.2,
                                         err_code=[236, 237, 238, 239],
                                         position_inp=[False, False, False, False],
                                         di_xx=['inp_01', 'inp_02', 'inp_03', 'inp_04']):
            self.conn_opc.ctrl_relay('KL12', False)
            self.conn_opc.ctrl_relay('KL25', False)
            self.conn_opc.ctrl_relay('KL1', False)
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
                                  di_a='inp_01', di_b='inp_02', di_c='inp_03', di_d='inp_04'):
            if self.subtest.subtest_b(test_num=4, subtest_num=4.1, relay='KL1',
                                      err_code_a=228, err_code_b=229, err_code_c=230, err_code_d=231,
                                      position_a=True, position_b=True, position_c=False, position_d=False,
                                      di_a='inp_01', di_b='inp_02', di_c='inp_03', di_d='inp_04'):
                return True
        return False

    def st_test_42(self) -> bool:
        """
        4. Защита от потери управляемости 1 канала блока при замыкании проводов ДУ
        """
        self.logger.debug("старт теста 4.2")
        self.conn_opc.ctrl_relay('KL11', True)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=4, subtest_num=4.3,
                                         err_code=[240, 241, 242, 243],
                                         position_inp=[False, False, False, False],
                                         di_xx=['inp_01', 'inp_02', 'inp_03', 'inp_04']):
            self.conn_opc.ctrl_relay('KL12', False)
            self.conn_opc.ctrl_relay('KL25', False)
            self.conn_opc.ctrl_relay('KL1', False)
            self.conn_opc.ctrl_relay('KL11', False)
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
                                  di_a='inp_01', di_b='inp_02', di_c='inp_03', di_d='inp_04'):
            if self.subtest.subtest_b(test_num=5, subtest_num=5.1, relay='KL1',
                                      err_code_a=228, err_code_b=229, err_code_c=230, err_code_d=231,
                                      position_a=True, position_b=True, position_c=False, position_d=False,
                                      di_a='inp_01', di_b='inp_02', di_c='inp_03', di_d='inp_04'):
                return True
        return False

    def st_test_52(self) -> bool:
        """
        Тест 5. Защита от потери управляемости 1 канала блока при обрыве проводов ДУ
        """
        self.logger.debug("старт теста 5.2")
        self.conn_opc.ctrl_relay('KL12', False)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=5, subtest_num=5.2,
                                         err_code=[244, 245, 246, 247],
                                         position_inp=[False, False, False, False],
                                         di_xx=['inp_01', 'inp_02', 'inp_03', 'inp_04']):
            self.conn_opc.ctrl_relay('KL25', False)
            self.conn_opc.ctrl_relay('KL1', False)
            return True
        return False

    def st_test_60(self) -> bool:
        """
        Тест 6. Проверка включения/выключения канала № 2 (К2) блока от кнопки «Пуск/Стоп».
        """
        self.logger.debug("старт теста 6.0")
        self.conn_opc.ctrl_relay('KL2', True)
        self.conn_opc.ctrl_relay('KL26', True)
        self.conn_opc.ctrl_relay('KL28', True)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=6, subtest_num=6.0,
                                         err_code=[248, 249, 250, 251],
                                         position_inp=[False, False, False, False],
                                         di_xx=['inp_01', 'inp_02', 'inp_03', 'inp_04']):
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
                                  di_a='inp_01', di_b='inp_02', di_c='inp_03', di_d='inp_04'):
            if self.subtest.subtest_b(test_num=6, subtest_num=6.2, relay='KL29',
                                      err_code_a=256, err_code_b=257, err_code_c=258, err_code_d=259,
                                      position_a=False, position_b=False, position_c=True, position_d=True,
                                      di_a='inp_01', di_b='inp_02', di_c='inp_03', di_d='inp_04'):
                return True
        return False

    def st_test_63(self) -> bool:
        """
        6.4. Выключение 2 канала блока от кнопки «Стоп»
        """
        self.logger.debug("старт теста 6.3")
        self.conn_opc.ctrl_relay('KL12', False)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=6, subtest_num=6.3,
                                         err_code=[260, 261, 262, 263],
                                         position_inp=[False, False, False, False],
                                         di_xx=['inp_01', 'inp_02', 'inp_03', 'inp_04']):
            self.conn_opc.ctrl_relay('KL25', False)
            self.conn_opc.ctrl_relay('KL29', False)
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
                                  di_a='inp_01', di_b='inp_02', di_c='inp_03', di_d='inp_04'):
            if self.subtest.subtest_b(test_num=7, subtest_num=7.1, relay='KL29',
                                      err_code_a=256, err_code_b=257, err_code_c=258, err_code_d=259,
                                      position_a=False, position_b=False, position_c=True, position_d=True,
                                      di_a='inp_01', di_b='inp_02', di_c='inp_03', di_d='inp_04'):
                return True
        return False

    def st_test_72(self) -> bool:
        """
        7. Отключение исполнительного элемента 2 канала при увеличении сопротивления цепи заземления
        """
        self.logger.debug("старт теста 7.2")
        self.resist.resist_10_to_110_ohm()
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=7, subtest_num=7.2,
                                         err_code=[264, 265, 266, 267],
                                         position_inp=[False, False, False, False],
                                         di_xx=['inp_01', 'inp_02', 'inp_03', 'inp_04']):
            self.conn_opc.ctrl_relay('KL12', False)
            self.conn_opc.ctrl_relay('KL25', False)
            self.conn_opc.ctrl_relay('KL29', False)
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
                                  di_a='inp_01', di_b='inp_02', di_c='inp_03', di_d='inp_04'):
            if self.subtest.subtest_b(test_num=8, subtest_num=8.1, relay='KL29',
                                      err_code_a=256, err_code_b=257, err_code_c=258, err_code_d=259,
                                      position_a=False, position_b=False, position_c=True, position_d=True,
                                      di_a='inp_01', di_b='inp_02', di_c='inp_03', di_d='inp_04'):
                return True
        return False

    def st_test_82(self) -> bool:
        """
        8. Защита от потери управляемости 2 канала блока при замыкании проводов ДУ
        """
        self.logger.debug("старт теста 8.2")
        self.conn_opc.ctrl_relay('KL11', True)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=8, subtest_num=8.2,
                                         err_code=[268, 269, 270, 271],
                                         position_inp=[False, False, False, False],
                                         di_xx=['inp_01', 'inp_02', 'inp_03', 'inp_04']):
            self.conn_opc.ctrl_relay('KL12', False)
            self.conn_opc.ctrl_relay('KL25', False)
            self.conn_opc.ctrl_relay('KL29', False)
            self.conn_opc.ctrl_relay('KL11', False)
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
                                  di_a='inp_01', di_b='inp_02', di_c='inp_03', di_d='inp_04'):
            if self.subtest.subtest_b(test_num=9, subtest_num=9.1, relay='KL29',
                                      err_code_a=256, err_code_b=257, err_code_c=258, err_code_d=259,
                                      position_a=False, position_b=False, position_c=True, position_d=True,
                                      di_a='inp_01', di_b='inp_02', di_c='inp_03', di_d='inp_04'):
                return True
        return False

    def st_test_92(self) -> bool:
        """
        Тест 9. Защита от потери управляемости 1 канала блока при обрыве проводов ДУ
        """
        self.logger.debug("старт теста 9.2")
        self.conn_opc.ctrl_relay('KL12', False)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=9, subtest_num=9.2,
                                         err_code=[272, 273, 274, 275],
                                         position_inp=[False, False, False, False],
                                         di_xx=['inp_01', 'inp_02', 'inp_03', 'inp_04']):
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

    def full_test_bdu_dr01(self) -> None:
        try:
            start_time = time()
            result_test = self.st_test_bdu_dr01()
            end_time = time()
            time_spent = end_time - start_time
            self.cli_log.lev_info(f"Время выполнения: {time_spent}", "gray")
            self.logger.debug(f"Время выполнения: {time_spent}")
            self.mysql_conn.mysql_add_message(f"Время выполнения: {time_spent}")
            if result_test:
                self.mysql_conn.mysql_block_good()
                self.logger.debug('Блок исправен')
                self.cli_log.lev_debug('Блок исправен', 'green')
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
