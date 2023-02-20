# -*- coding: utf-8 -*-
"""
Чтения и записи в БД
"""

import logging
from datetime import datetime

import mysql.connector

from .utils import CLILog

__all__ = ['MySQLConnect']


class MySQLConnect:
    _instances = None

    def __new__(cls, *args, **kwargs):
        if cls._instances is None:
            cls._instances = super().__new__(cls)

        return cls._instances

    def __init__(self):
        self.host = 'localhost'
        self.user = 'simple_user'
        self.password = 'user'
        self.database = 'simple_database'
        self.auth_plugin = 'mysql_native_password'
        self.mysql_err = mysql.connector.Error
        self.cli_log = CLILog("debug", __name__)
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))

    def connect_to_db_wr_result(self, request: str, aquery: str, result: [str]) -> None:
        try:
            with mysql.connector.connect(host=self.host, user=self.user, password=self.password,
                                         database=self.database, auth_plugin=self.auth_plugin) as conn:
                c = conn.cursor()
                c.execute(aquery)
                c.executemany(request, result)
                conn.commit()
                self.logger.info(f"записей в БД: {c.rowcount}")
                self.cli_log.lev_debug(f"записей в БД: {c.rowcount}", "gray")

        except self.mysql_err as sql_err:
            self.logger.error(f"!!! Ошибка связи с базой данных MySQL !!!\n{sql_err}")
            self.cli_log.lev_warning(f'!!! Ошибка связи с базой данных MySQL !!!\n{sql_err}', "red")

    def mysql_pmz_result(self, my_result: [str]) -> None:
        """
        Запись в БД результатов теста блока ПМЗ
        :param my_result:
        :return:
        """
        sql = 'insert into pmz_result(pmz_set, pmz_proc, pmz_time) values(%s, %s, %s)'
        aquery = 'TRUNCATE simple_database.pmz_result;'
        self.connect_to_db_wr_result(request=sql, aquery=aquery, result=my_result)

    def mysql_tzp_result(self, my_result: [str]) -> None:
        """
        Запись в БД результатов теста блока ТЗП
        :param my_result:
        :return:
        """
        sql = 'insert into tzp_result(tzp_set, tzp_proc, tzp_time) values(%s, %s, %s)'
        aquery = 'TRUNCATE simple_database.tzp_result;'
        self.connect_to_db_wr_result(request=sql, aquery=aquery, result=my_result)

    def mysql_umz_result(self, my_result: [str]) -> None:
        """
        Запись в БД результатов теста блока УМЗ
        :param my_result:
        :return:
        """
        sql = 'insert into umz_result(umz_set_ab, umz_proc_ab, umz_time_ab, umz_set_vg, umz_proc_vg, umz_time_vg) ' \
              'values(%s, %s, %s, %s, %s, %s)'
        aquery = 'TRUNCATE simple_database.umz_result;'
        self.connect_to_db_wr_result(request=sql, aquery=aquery, result=my_result)

    def mysql_ubtz_btz_result(self, my_result: [str]) -> None:
        """
        Запись в БД результатов теста блока УБТЗ
        :param my_result:
        :return:
        """
        sql = 'insert into ubtz_btz_result(ubtz_btz_ust, ubtz_btz_time) values(%s, %s)'
        aquery = 'TRUNCATE simple_database.ubtz_btz_result;'
        self.connect_to_db_wr_result(request=sql, aquery=aquery, result=my_result)

    def mysql_ubtz_tzp_result(self, my_result: [str]) -> None:
        """
        Запись в БД результатов теста проверки ТЗП, блока УБТЗ
        :param my_result:
        :return:
        """
        sql = 'insert into ubtz_tzp_result(ubtz_tzp_ust, ubtz_tzp_time) values(%s, %s)'
        aquery = 'TRUNCATE simple_database.ubtz_tzp_result;'
        self.connect_to_db_wr_result(request=sql, aquery=aquery, result=my_result)

    def connect_to_db(self, request):
        try:
            with mysql.connector.connect(host=self.host, user=self.user, password=self.password,
                                         database=self.database, auth_plugin=self.auth_plugin) as conn:
                c = conn.cursor()
                c.execute(request)
                conn.commit()
        except self.mysql_err as sql_err:
            self.logger.error(f"!!! Ошибка связи с базой данных MySQL !!!\n{sql_err}")
            self.cli_log.lev_warning(f'!!! Ошибка связи с базой данных MySQL !!!\n{sql_err}', "red")

    def mysql_ins_result(self, my_result: str, num_test: str) -> None:
        """
        Запись в БД результата подтеста, (исправен/не исправен и номер подтеста)
        :param my_result: исправен/не исправен
        :param num_test: номер теста
        :return:
        """
        request = (f"UPDATE simple_database.test_results SET result_text = '{my_result}' "
                   f"WHERE id_test_result = '{num_test}'")
        self.connect_to_db(request)

    def mysql_block_bad(self) -> None:
        """
        Запись в БД если блок неисправен.
        :return:
        """
        upd_bad = ('UPDATE simple_database.python_message SET pyth_block_bad = 1 WHERE id_pyth_mes = 1')
        upd_good = ('UPDATE simple_database.python_message SET pyth_block_good = 0 WHERE id_pyth_mes = 1')
        self.connect_to_db(upd_bad)
        self.connect_to_db(upd_good)

    def mysql_block_good(self) -> None:
        """
        Запись в БД если блок исправен.
        :return:
        """
        upd_bad = ('UPDATE simple_database.python_message SET pyth_block_bad = 0 WHERE id_pyth_mes = 1')
        upd_good = ('UPDATE simple_database.python_message SET pyth_block_good = 1 WHERE id_pyth_mes = 1')
        self.connect_to_db(upd_bad)
        self.connect_to_db(upd_good)

    def mysql_error(self, n_err: int) -> None:
        """
        Запись в БД номера неисправности
        :param n_err: номер неисправности
        :return:
        """
        upd = (f"UPDATE simple_database.python_message SET pyth_error = {n_err} WHERE id_pyth_mes = 1")
        self.connect_to_db(upd)

    def mysql_add_message(self, mess: str) -> None:
        """
        Запись в БД для динамического отслеживания прогресса испытания.
        :param mess: Текстовое сообщение
        :return:
        """
        current_date = datetime.now()
        mess = mess[:170]
        request = f"INSERT INTO simple_database.messages_alg(mess_alg_time, mess_text) " \
                  f"VALUES('{current_date}','{mess}');"
        self.logger.debug(f"{request}")
        self.connect_to_db(request)

    def progress_level(self, level: float) -> None:
        """
        Запись в БД времени прогресса выполнения испытания.
        :param level: Число с пл. точкой
        :return:
        """
        level = f'{level:.1f}'
        upd = f'UPDATE simple_database.progress SET level_progress = {level} WHERE (id_pro = 1);'
        self.connect_to_db(upd)

    def read_err(self, err_code: int) -> str:
        """
        Считывает из БД описание неисправности по номеру неисправности.
        :param err_code:
        :return text_0:
        """

        try:
            with mysql.connector.connect(host=self.host, user=self.user, password=self.password,
                                         database=self.database, auth_plugin=self.auth_plugin) as conn:
                err_select = f"SELECT * FROM errors WHERE `id_error` in ({err_code});"
                c = conn.cursor()
                c.execute(err_select)
                err_text, *_ = c.fetchall()
                conn.close()
                text_0 = err_text[1]
                return text_0
        except self.mysql_err as sql_err:
            self.logger.error(f"!!! Ошибка связи с базой данных MySQL !!!\n{sql_err}")
            self.cli_log.lev_warning(f'!!! Ошибка связи с базой данных MySQL !!!\n{sql_err}', "red")
