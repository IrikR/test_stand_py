# -*- coding: utf-8 -*-
"""

"""
__all__ = ["WriteCondition", "RWError"]

import logging

from .database import MySQLConnect
from .utils import CLILog

class WriteCondition:

    def __init__(self):
        self.cli_log = CLILog("debug", __name__)
        self.logger = logging.getLogger(__name__)
        self.mysql_conn = MySQLConnect()
    def write_condition(self, test_num: int, subtest_num: float) -> None:
        """
        Метод для записи результатов начала теста.
        Используется для логирования и записи результатов в БД, в методах опроса дискретных входов ПЛК.
        :param test_num: Int
        :param subtest_num: Float
        :return:
        """
        self.cli_log.lev_debug(f"тест: {test_num}, подтест: {subtest_num}", "gray")
        self.logger.debug(f"тест: {test_num}, подтест: {subtest_num}")
        self.mysql_conn.mysql_ins_result(f"идёт тест {subtest_num}", f'{test_num}')
        self.mysql_conn.mysql_add_message(f"идёт тест: {subtest_num}, подтест: {test_num}")

    def write_condition_true(self, test_num: int, subtest_num: float) -> None:
        """
        Метод для записи результатов если тест успешен.
        Используется для логирования и записи результатов в БД, в методах опроса дискретных входов ПЛК.
        :param test_num:
        :param subtest_num:
        :return:
        """
        self.cli_log.lev_info("состояние выхода блока соответствует", "green")
        self.logger.debug("состояние выхода блока соответствует")
        self.mysql_conn.mysql_ins_result(f"исправен", f'{test_num}')
        self.mysql_conn.mysql_add_message(f"Исправен. тест: {subtest_num}, подтест: {test_num}")

    def write_condition_false(self, test_num: int, subtest_num: float) -> None:
        """
        Метод для записи результатов если тест не успешен.
        Используется для логирования и записи результатов в БД, в методах опроса дискретных входов ПЛК.
        :param test_num:
        :param subtest_num:
        :return:
        """
        self.cli_log.lev_warning("состояние выхода блока не соответствует", "red")
        self.logger.warning("состояние выхода блока не соответствует")
        self.mysql_conn.mysql_ins_result("неисправен", f'{test_num}')
        self.mysql_conn.mysql_add_message(f"Несправен. тест: {subtest_num}, подтест: {test_num}")


class RWError:

    def __init__(self):
        self.mysql_conn = MySQLConnect()
        self.logger = logging.getLogger(__name__)
        self.cli_log = CLILog("debug", __name__)

    def rw_err(self, err_code: int) -> None:
        """
        Метод для записи и вывода информации по коду неисправности блока
        :param err_code: int
        :return: None
        """
        self.mysql_conn.mysql_error(err_code)
        read_err = self.mysql_conn.read_err(err_code)
        self.mysql_conn.mysql_add_message(read_err)
        self.logger.debug(f'код неисправности {err_code}: {read_err}')
        self.cli_log.lev_warning(f'код неисправности {err_code}: {read_err}', "red")
