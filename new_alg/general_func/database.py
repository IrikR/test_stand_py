#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Класс mysql для чтения и записи в БД
"""

import logging
from datetime import datetime

import mysql.connector

from .utils import CLILog


__all__ = ['MySQLConnect']


class MySQLConnect:

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

    def mysql_ins_result(self, my_result: str, num_test: str) -> None:
        """
        Запись в БД результата подтеста, (исправен/не исправен и номер подтеста)
        :param my_result: исправен/не исправен
        :param num_test: номер теста
        :return:
        """
        # my_result = my_result
        # num_test = num_test
        try:
            conn = mysql.connector.connect(host=self.host, user=self.user, password=self.password,
                                           database=self.database, auth_plugin=self.auth_plugin)
            c = conn.cursor()
            retrive = ('UPDATE simple_database.test_results SET result_text = "' + my_result +
                       '" WHERE id_test_result = "' + num_test + '"')
            c.execute(retrive)
            conn.commit()
            conn.close()
        except self.mysql_err:
            self.logger.error('!!! Ошибка связи с базой данных MySQL !!!')
            self.cli_log.lev_warning('!!! Ошибка связи с базой данных MySQL !!!', "red")

    def mysql_pmz_result(self, my_result: [str]) -> None:
        """
        Запись в БД результатов теста блока ПМЗ
        :param my_result:
        :return:
        """
        # my_result = my_result
        sql = 'insert into pmz_result(pmz_set, pmz_proc, pmz_time) values(%s, %s, %s)'

        try:
            conn = mysql.connector.connect(host=self.host, user=self.user, password=self.password,
                                           database=self.database, auth_plugin=self.auth_plugin)
            c = conn.cursor()
            aquery = 'TRUNCATE simple_database.pmz_result;'
            c.execute(aquery)
            c.executemany(sql, my_result)
            conn.commit()
            self.logger.info(f"записей в БД: {c.rowcount}")
            self.cli_log.lev_debug(f"записей в БД: {c.rowcount}", "gray")
            conn.close()
        except self.mysql_err:
            self.logger.error(f"!!! Ошибка связи с базой данных MySQL !!!")
            self.cli_log.lev_warning('!!! Ошибка связи с базой данных MySQL !!!', "red")

    def mysql_tzp_result(self, my_result: [str]) -> None:
        """
        Запись в БД результатов теста блока ТЗП
        :param my_result:
        :return:
        """
        # self.my_result = my_result
        sql = 'insert into tzp_result(tzp_set, tzp_proc, tzp_time) values(%s, %s, %s)'

        try:
            conn = mysql.connector.connect(host=self.host, user=self.user, password=self.password,
                                           database=self.database, auth_plugin=self.auth_plugin)
            c = conn.cursor()
            aquery = 'TRUNCATE simple_database.tzp_result;'
            c.execute(aquery)
            c.executemany(sql, my_result)
            conn.commit()
            self.logger.info(f"записей в БД: {c.rowcount}")
            self.cli_log.lev_debug(f"записей в БД: {c.rowcount}", "gray")
            conn.close()
        except self.mysql_err:
            self.logger.error(f"!!! Ошибка связи с базой данных MySQL !!!")
            self.cli_log.lev_warning('!!! Ошибка связи с базой данных MySQL !!!', "red")

    def mysql_umz_result(self, my_result: [str]) -> None:
        """
        Запись в БД результатов теста блока УМЗ
        :param my_result:
        :return:
        """
        # self.my_result = my_result
        sql = 'insert into umz_result(umz_set_ab, umz_proc_ab, umz_time_ab, umz_set_vg, umz_proc_vg, umz_time_vg) ' + \
              'values(%s, %s, %s, %s, %s, %s)'
        try:
            conn = mysql.connector.connect(host=self.host, user=self.user, password=self.password,
                                           database=self.database, auth_plugin=self.auth_plugin)
            c = conn.cursor()
            aquery = 'TRUNCATE simple_database.umz_result;'
            c.execute(aquery)
            c.executemany(sql, my_result)
            conn.commit()
            self.logger.info(f"записей в БД: {c.rowcount}")
            self.cli_log.lev_debug(f"записей в БД: {c.rowcount}", "gray")
            conn.close()
        except self.mysql_err:
            self.logger.error(f"!!! Ошибка связи с базой данных MySQL !!!")
            self.cli_log.lev_warning('!!! Ошибка связи с базой данных MySQL !!!', "red")

    def mysql_ubtz_btz_result(self, my_result: [str]) -> None:
        """
        Запись в БД результатов теста блока УБТЗ
        :param my_result:
        :return:
        """
        # self.my_result = my_result
        sql = 'insert into ubtz_btz_result(ubtz_btz_ust, ubtz_btz_time) ' + 'values(%s, %s)'
        try:
            conn = mysql.connector.connect(host=self.host, user=self.user, password=self.password,
                                           database=self.database, auth_plugin=self.auth_plugin)
            c = conn.cursor()
            aquery = 'TRUNCATE simple_database.ubtz_btz_result;'
            c.execute(aquery)
            c.executemany(sql, my_result)
            conn.commit()
            self.logger.info(f"записей в БД: {c.rowcount}")
            self.cli_log.lev_debug(f"записей в БД: {c.rowcount}", "gray")
            conn.close()
        except self.mysql_err:
            self.logger.error(f"!!! Ошибка связи с базой данных MySQL !!!")
            self.cli_log.lev_warning('!!! Ошибка связи с базой данных MySQL !!!', "red")

    def mysql_ubtz_tzp_result(self, my_result: [str]) -> None:
        """
        Запись в БД результатов теста проверки ТЗП, блока УБТЗ
        :param my_result:
        :return:
        """
        # self.my_result = my_result
        sql = 'insert into ubtz_tzp_result(ubtz_tzp_ust, ubtz_tzp_time) ' + 'values(%s, %s)'
        try:
            conn = mysql.connector.connect(host=self.host, user=self.user, password=self.password,
                                           database=self.database, auth_plugin=self.auth_plugin)
            c = conn.cursor()
            aquery = 'TRUNCATE simple_database.ubtz_tzp_result;'
            c.execute(aquery)
            c.executemany(sql, my_result)
            conn.commit()
            self.logger.info(f"записей в БД: {c.rowcount}")
            self.cli_log.lev_debug(f"записей в БД: {c.rowcount}", "gray")
            conn.close()
        except self.mysql_err:
            self.logger.error(f"!!! Ошибка связи с базой данных MySQL !!!")
            self.cli_log.lev_warning('!!! Ошибка связи с базой данных MySQL !!!', "red")

    def mysql_connect(self, request: str) -> None:
        """
        Подключение к БД
        :param request:
        :return:
        """
        # self.request = request
        try:
            conn = mysql.connector.connect(host=self.host, user=self.user, password=self.password,
                                           database=self.database, auth_plugin=self.auth_plugin)
            c = conn.cursor()
            c.execute(request)
            conn.commit()
            conn.close()
        except self.mysql_err:
            self.logger.error(f"!!! Ошибка связи с базой данных MySQL !!!")
            self.cli_log.lev_warning('!!! Ошибка связи с базой данных MySQL !!!', "red")

    def mysql_block_bad(self) -> None:
        """
        Запись в БД если блок неисправен.
        :return:
        """
        upd_bad = ('UPDATE simple_database.python_message SET pyth_block_bad = 1 WHERE id_pyth_mes = 1')
        upd_good = ('UPDATE simple_database.python_message SET pyth_block_good = 0 WHERE id_pyth_mes = 1')
        self.mysql_connect(upd_bad)
        self.mysql_connect(upd_good)

    def mysql_block_good(self) -> None:
        """
        Запись в БД если блок исправен.
        :return:
        """
        upd_bad = ('UPDATE simple_database.python_message SET pyth_block_bad = 0 WHERE id_pyth_mes = 1')
        upd_good = ('UPDATE simple_database.python_message SET pyth_block_good = 1 WHERE id_pyth_mes = 1')
        self.mysql_connect(upd_bad)
        self.mysql_connect(upd_good)

    def mysql_error(self, n_err: int) -> None:
        """
        Запись в БД номера неисправности
        :param n_err: номер неисправности
        :return:
        """
        # self.n_err = n_err
        upd = ('UPDATE simple_database.python_message SET pyth_error = "' + str(n_err) + '" WHERE id_pyth_mes = 1')
        self.mysql_connect(upd)

    def mysql_add_message(self, mess: str) -> None:
        """
        Запись в БД для динамического отслеживания прогресса испытания.
        :param mess: Текстовое сообщение
        :return:
        """
        # self.mess = mess
        mytime = datetime.now()
        mess = mess[:170]
        request = "INSERT INTO simple_database.messages_alg(mess_alg_time, mess_text) " \
                  "VALUES('" + str(mytime) + "','" + mess + "'); "
        self.logger.debug(f"{request}")
        try:
            conn = mysql.connector.connect(host=self.host, user=self.user, password=self.password,
                                           database=self.database, auth_plugin=self.auth_plugin)
            c = conn.cursor()
            c.execute(request)
            conn.commit()
            conn.close()
        except self.mysql_err:
            self.logger.error('Ошибка связи с базой данных MySQL.')
            self.cli_log.lev_warning('!!! Ошибка связи с базой данных MySQL !!!', "red")

    def progress_level(self, level: float) -> None:
        """
        Запись в БД времени прогресса выполнения испытания.
        :param level: Число с пл. точкой
        :return:
        """
        level = f'{level:.1f}'
        upd = f'UPDATE simple_database.progress SET level_progress = {level} WHERE (id_pro = 1);'
        self.mysql_connect(upd)

    def read_err(self, err_code: int) -> str:
        """
        Считывает из БД описание неисправности по номеру неисправности.
        :param err_code:
        :return text_0:
        """
        with mysql.connector.connect(host=self.host, user=self.user, password=self.password,
                                     database=self.database, auth_plugin=self.auth_plugin) as conn:
            try:
                err_select = f'SELECT * FROM errors WHERE `id_error` in ({err_code});'
                c = conn.cursor()
                c.execute(err_select)
                err_text, *_ = c.fetchall()
                conn.close()
                text_0 = err_text[1]
                # text_1 = text_0[1]
                return text_0
            except self.mysql_err:
                self.logger.error(f"!!! Ошибка связи с базой данных MySQL !!!")
                self.cli_log.lev_warning('!!! Ошибка связи с базой данных MySQL !!!', "red")


if __name__ == '__main__':
    __mysql = MySQLConnect()
    result = __mysql.read_err(222)
    print(result)
    __mysql.mysql_add_message(result)
