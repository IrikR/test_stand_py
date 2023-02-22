# -*- coding: utf-8 -*-
"""
!!! НОВЫЙ НЕ ОБКАТАНЫЙ !!!

Алгоритм проверки

Тип блока: БРУ-2СР
Производитель: Нет производителя

"""

__all__ = ["TestBRU2SR"]

import logging
from time import sleep

from .general_func.database import *
from .general_func.opc_full import ConnectOPC
from .general_func.reset import ResetRelay
from .general_func.resistance import Resistor
from .general_func.subtest import Subtest2in
from .general_func.utils import CLILog
from .gui.msgbox_1 import *


class TestBRU2SR:

    def __init__(self):
        self.conn_opc = ConnectOPC()
        self.resist = Resistor()
        self.mysql_conn = MySQLConnect()
        self.subtest = Subtest2in()
        self.reset_relay = ResetRelay()
        self.cli_log = CLILog("debug", __name__)

        logging.basicConfig(
            filename="C:\\Stend\\project_class\\log\\TestBRU2SR.log",
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
        """
        self.cli_log.lev_info(f"старт теста {__doc__}", "skyblue")
        if self.conn_opc.subtest_read_di(test_num=1, subtest_num=1.0,
                                         err_code=[57, 58],
                                         position_inp=[False, False],
                                         di_xx=['inp_01', 'inp_02']):
            return True
        return False

    def st_test_20(self) -> bool:
        """
        Тест 2. Проверка включения/выключения блока от кнопки «Пуск/Стоп» в режиме «Вперёд».
        2.2. Включение блока от кнопки «Пуск»
        2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        2.4. Выключение блока от кнопки «Стоп»
        """
        self.logger.debug("старт теста 2.0")
        self.conn_opc.ctrl_relay('KL21', True)
        if self.conn_opc.subtest_read_di(test_num=2, subtest_num=2.0,
                                         err_code=[59, 60],
                                         position_inp=[False, False],
                                         di_xx=['inp_01', 'inp_02']):
            if self.subtest.subtest_a_bdu(test_num=2, subtest_num=2.1, err_code_a=61, err_code_b=62,
                                          position_a=True, position_b=False, resist=0):
                if self.subtest.subtest_b_bdu(test_num=2, subtest_num=2.2, err_code_a=63, err_code_b=64,
                                              position_a=True, position_b=False, kl1=False):
                    self.conn_opc.ctrl_relay('KL12', False)
                    if self.conn_opc.subtest_read_di(test_num=2, subtest_num=2.3,
                                                     err_code=[65, 66],
                                                     position_inp=[False, False],
                                                     di_xx=['inp_01', 'inp_02']):
                        self.conn_opc.ctrl_relay('KL25', False)
                        return True
        return False

    def st_test_30(self) -> bool:
        """
        Повторяем подтест 2.2. Включение блока от кнопки «Пуск»
        Повторяем подтест 2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        3. Отключение контакта «Вперёд» при увеличении сопротивления цепи заземления
        """
        if self.subtest.subtest_a_bdu(test_num=3, subtest_num=3.0, err_code_a=61, err_code_b=62,
                                      position_a=True, position_b=False, resist=0):
            if self.subtest.subtest_b_bdu(test_num=3, subtest_num=3.1, err_code_a=63, err_code_b=64,
                                          position_a=True, position_b=False, kl1=False):
                self.resist.resist_ohm(150)
                sleep(1)
                self.logger.debug("таймаут 1 сек")
                self.cli_log.lev_debug("таймаут 1 сек", "gray")
                if self.conn_opc.subtest_read_di(test_num=3, subtest_num=3.2,
                                                 err_code=[67, 68],
                                                 position_inp=[False, False],
                                                 di_xx=['inp_01', 'inp_02']):
                    self.conn_opc.ctrl_relay('KL12', False)
                    self.conn_opc.ctrl_relay('KL25', False)
                    return True
        return False

    def st_test_40(self) -> bool:
        """
        Повторяем подтест 2.2. Включение блока от кнопки «Пуск»
        Повторяем подтест 2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        4. Защита от потери управляемости канала «Вперёд» при замыкании проводов ДУ
        """
        if self.subtest.subtest_a_bdu(test_num=4, subtest_num=4.0, err_code_a=61, err_code_b=62,
                                      position_a=True, position_b=False, resist=0):
            if self.subtest.subtest_b_bdu(test_num=4, subtest_num=4.1, err_code_a=63, err_code_b=64,
                                          position_a=True, position_b=False, kl1=False):
                self.conn_opc.ctrl_relay('KL11', True)
                if self.conn_opc.subtest_read_di(test_num=4, subtest_num=4.2,
                                                 err_code=[69, 70],
                                                 position_inp=[False, False],
                                                 di_xx=['inp_01', 'inp_02']):
                    self.conn_opc.ctrl_relay('KL12', False)
                    self.conn_opc.ctrl_relay('KL25', False)
                    self.conn_opc.ctrl_relay('KL11', False)
                    return True
        return False

    def st_test_50(self) -> bool:
        """
        Повторяем подтест 2.2. Включение блока от кнопки «Пуск»
        Повторяем подтест 2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        Тест 5. Защита от потери управляемости канала «Вперёд» при обрыве проводов ДУ
        """
        if self.subtest.subtest_a_bdu(test_num=5, subtest_num=5.0, err_code_a=61, err_code_b=62,
                                      position_a=True, position_b=False, resist=0):
            if self.subtest.subtest_b_bdu(test_num=5, subtest_num=5.1, err_code_a=63, err_code_b=64,
                                          position_a=True, position_b=False, kl1=False):
                self.conn_opc.ctrl_relay('KL12', False)
                if self.conn_opc.subtest_read_di(test_num=5, subtest_num=5.2,
                                                 err_code=[71, 72],
                                                 position_inp=[False, False],
                                                 di_xx=['inp_01', 'inp_02']):
                    self.conn_opc.ctrl_relay('KL25', False)
                    return True
        return False

    def st_test_60(self) -> bool:
        """
        Тест 6. Проверка включения/выключения блока от кнопки «Пуск/Стоп» в режиме «Назад».
        6.1. Включение блока от кнопки «Пуск» режима «Назад»
        6.2. Проверка удержания блока во включенном состоянии
        при подключении Rш пульта управления режима «Назад»:
        6.3. Выключение блока от кнопки «Стоп» режима «Назад»
        """
        self.logger.debug("старт теста 6.0")
        self.conn_opc.ctrl_relay('KL26', True)
        if self.conn_opc.subtest_read_di(test_num=6, subtest_num=6.0,
                                         err_code=[59, 60],
                                         position_inp=[False, False],
                                         di_xx=['inp_01', 'inp_02']):
            if self.subtest.subtest_a_bdu(test_num=6, subtest_num=6.1, err_code_a=73, err_code_b=74,
                                          position_a=False, position_b=True, resist=0):
                if self.subtest.subtest_b_bdu(test_num=6, subtest_num=6.2, err_code_a=75, err_code_b=76,
                                              position_a=False, position_b=True, kl1=False):
                    self.conn_opc.ctrl_relay('KL12', False)
                    if self.conn_opc.subtest_read_di(test_num=6, subtest_num=6.3,
                                                     err_code=[77, 78],
                                                     position_inp=[False, False],
                                                     di_xx=['inp_01', 'inp_02']):
                        self.conn_opc.ctrl_relay('KL25', False)
                        return True
        return False

    def st_test_70(self) -> bool:
        """
        Повторяем подтест 6.2. Включение блока от кнопки «Пуск» режима «Назад»
        Повторяем подтест 6.3. Проверка удержания блока во включенном состоянии
        при подключении Rш пульта управления режима «Назад»:
        7. Отключение контакта «Назад» при увеличении сопротивления цепи заземления
        """
        if self.subtest.subtest_a_bdu(test_num=7, subtest_num=7.0, err_code_a=73, err_code_b=74,
                                      position_a=False, position_b=True, resist=0):
            if self.subtest.subtest_b_bdu(test_num=7, subtest_num=7.1, err_code_a=75, err_code_b=76,
                                          position_a=False, position_b=True, kl1=False):
                self.resist.resist_ohm(150)
                if self.conn_opc.subtest_read_di(test_num=7, subtest_num=7.2,
                                                 err_code=[79, 80],
                                                 position_inp=[False, False],
                                                 di_xx=['inp_01', 'inp_02']):
                    self.conn_opc.ctrl_relay('KL12', False)
                    self.conn_opc.ctrl_relay('KL25', False)
                    return True
        return False

    def st_test_80(self) -> bool:
        """
        Повторяем подтест 6.2. Включение блока от кнопки «Пуск» режима «Назад»
        Повторяем подтест 6.3. Проверка удержания блока во включенном состоянии
        при подключении Rш пульта управления режима «Назад»:
        8. Защита от потери управляемости канала «Назад» при замыкании проводов ДУ
        """
        if self.subtest.subtest_a_bdu(test_num=8, subtest_num=8.0, err_code_a=73, err_code_b=74,
                                      position_a=False, position_b=True, resist=0):
            if self.subtest.subtest_b_bdu(test_num=8, subtest_num=8.1, err_code_a=75, err_code_b=76,
                                          position_a=False, position_b=True, kl1=False):
                self.conn_opc.ctrl_relay('KL11', True)
                if self.conn_opc.subtest_read_di(test_num=8, subtest_num=8.2,
                                                 err_code=[81, 82],
                                                 position_inp=[False, False],
                                                 di_xx=['inp_01', 'inp_02']):
                    self.conn_opc.ctrl_relay('KL12', False)
                    self.conn_opc.ctrl_relay('KL25', False)
                    self.conn_opc.ctrl_relay('KL11', False)
                    return True
        return False

    def st_test_90(self) -> bool:
        """
        Повторяем подтест 6.2. Включение блока от кнопки «Пуск» режима «Назад»
        Повторяем подтест 6.3. Проверка удержания блока во включенном состоянии
        при подключении Rш пульта управления режима «Назад»:
        Тест 9. Защита от потери управляемости канала «Назад» при обрыве проводов ДУ
        """
        if self.subtest.subtest_a_bdu(test_num=9, subtest_num=9.0, err_code_a=73, err_code_b=74,
                                      position_a=False, position_b=True, resist=0):
            if self.subtest.subtest_b_bdu(test_num=9, subtest_num=9.1, err_code_a=75, err_code_b=76,
                                          position_a=False, position_b=True, kl1=False):
                self.conn_opc.ctrl_relay('KL12', False)
                if self.conn_opc.subtest_read_di(test_num=9, subtest_num=9.2,
                                                 err_code=[83, 84],
                                                 position_inp=[False, False],
                                                 di_xx=['inp_01', 'inp_02']):
                    self.conn_opc.ctrl_relay('KL25', False)
                    return True
        return False

    def st_test_100(self) -> bool:
        """

        :return:
        """
        self.logger.debug("старт теста 10.0")
        msg_1 = "Переведите тумблер «П/А» на блоке в положение «П» и нажмите кнопку «ОК» " \
                "Если на блоке нет тумблера «П/А» нажмите кнопку «Отмена»"
        if my_msg(msg_1):
            if self.subtest.subtest_bru2sr(test_num=10, subtest_num=10.0, err_code_a=85, err_code_b=86,
                                           resist=200):
                if self.subtest.subtest_bru2sr(test_num=11, subtest_num=11.0, err_code_a=87, err_code_b=88,
                                               resist=30):
                    return True
            return False
        else:
            if self.subtest.subtest_bru2sr(test_num=11, subtest_num=11.0, err_code_a=87, err_code_b=88,
                                           resist=30):
                self.mysql_conn.mysql_ins_result('пропущен', '10')
                return True
        self.mysql_conn.mysql_ins_result('пропущен', '10')
        return False

    def st_test_bru_2sr(self) -> bool:
        """
            Главная функция которая собирает все остальные
            :type: bool
            :return:  результат теста
        """
        if self.st_test_10():
            if self.st_test_20():
                if self.st_test_30():
                    if self.st_test_40():
                        if self.st_test_50():
                            if self.st_test_60():
                                if self.st_test_70():
                                    if self.st_test_80():
                                        if self.st_test_90():
                                            if self.st_test_100():
                                                return True
        return False
