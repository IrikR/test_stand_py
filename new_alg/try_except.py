# -*- coding: utf-8 -*-
"""
Метод представляет собой общий метод запуска для всех алгоритмов проверки
в нее входит проверка на соответствие заданным параметрам и вывод исключений при возникновении таковых
"""

__all__ = ["TryExcept"]

import logging
import sys
from time import time

from .general_func.database import MySQLConnect
from .general_func.exception import *
from .general_func.opc_full import ConnectOPC
from .general_func.utils import CLILog
from .gui.msgbox_1 import *


class TryExcept:
    def __init__(self):
        self.cli_log = CLILog("debug", __name__)
        self.logger = logging.getLogger(__name__)
        self.conn_opc = ConnectOPC()
        self.mysql_conn = MySQLConnect()

    def _put_result(self, msg):
        """
        Запись информационного сообщения в логгер, терминал и GUI
        """
        self.logger.warning(f"{msg}")
        self.cli_log.lev_warning(f"{msg}", 'red')
        my_msg(f"{msg}", 'red')
    def _result_good(self):
        """
        Запись положительного результата
        """
        self.mysql_conn.mysql_block_good()
        self.logger.debug('Блок исправен')
        self.cli_log.lev_info('Блок исправен', 'green')
        my_msg('Блок исправен', 'green')

    def _result_bad(self):
        """
        Запись отрицательного результата
        """
        self.mysql_conn.mysql_block_bad()
        self._put_result('Блок неисправен')

    def _time_result(self, start_time, end_time):
        """
        Запись времени выполнения алгоритма проверки
        :param start_time: время начала выполнения алгоритма
        :param end_time: время окончания выполнения алгоритма
        """
        time_spent = end_time - start_time
        self.cli_log.lev_info(f"Время выполнения: {time_spent}", "gray")
        self.logger.debug(f"Время выполнения: {time_spent}")
        self.mysql_conn.mysql_add_message(f"Время выполнения: {time_spent}")

    def _not_health_flag(self, start_test):
        """
        Используется если в алгоритме проверки не используется флаг исправности
        :param start_test: алгоритм который необходимо запустить
        """
        start_time = time()
        test = start_test()
        end_time = time()
        self._time_result(start_time, end_time)
        if test is True:
            self._result_good()
        else:
            self._result_bad()

    def _one_health_flag(self, start_test, result):
        """
        Используется если в алгоритме проверки, используется один флаг исправности
        :param start_test: алгоритм который необходимо запустить
        :param result: результат выполнения алгоритма
        """
        start_time = time()
        test, health_flag_0 = start_test()
        end_time = time()
        self._time_result(start_time, end_time)
        result()
        if test and not health_flag_0:
            self._result_good()
        else:
            self._result_bad()

    def _two_health_flag(self, start_test, result):
        """
        Используется если в алгоритме проверки, используется два флага исправности
        :param start_test: алгоритм который необходимо запустить
        :param result: результат выполнения алгоритма
        """
        start_time = time()
        test, health_flag_0, health_flag_1 = start_test()
        end_time = time()
        self._time_result(start_time, end_time)
        result()
        if test and not health_flag_0 and not health_flag_1:
            self._result_good()
        else:
            self._result_bad()

    def full_start_test(self, start_test, result, health_flag: int) -> None:
        """
        Функция представляет собой общий метод запуска для всех алгоритмов проверки
        в нее входит проверка на соответствие заданным параметрам и вывод исключений при возникновении таковых
        для запуска простых алгоритмов (без результатов теста) нужно передать вторым аргументом None
        для запуска сложных алгоритмов (с результатами теста) нужно передать вторым аргументом результат
        :param start_test: алгоритм который будет проверяться
        :param result: результат проверки
        :param health_flag: количество флагов возвращаемых алгоритмом
        :return:
        """
        try:
            self.conn_opc.simplified_read_di(["inp_14", "inp_15"])
            self.mysql_conn.mysql_add_message("старт проверки блока")
            if health_flag == 0:
                self._not_health_flag(start_test)
            elif health_flag == 1:
                self._one_health_flag(start_test, result)
            elif health_flag == 2:
                self._two_health_flag(start_test, result)
            else:
                raise AttributeError("параметр health_flag должен быть 0 или 1 или 2")
        except OSError:
            self._put_result("ошибка системы")
        except SystemError:
            self._put_result("внутренняя ошибка")
        except ValueError as ve:
            self._put_result(f"{ve}, получено некорректное значение для переменной")
        except AttributeError as ae:
            self._put_result(f"Неверный атрибут. {ae}")
        except TypeError as te:
            self._put_result(f"Неверный тип. {te}")
        except ModbusConnectException as mce:
            self._put_result(f"{mce}")
        except HardwareException as hwe:
            self._put_result(f"{hwe}")
        finally:
            self.conn_opc.full_relay_off()
            self.conn_opc.opc_close()
            sys.exit()
