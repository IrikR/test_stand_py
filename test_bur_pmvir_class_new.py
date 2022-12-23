#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки

Тип блока: БУР ПМВИР (пускатель)
Производитель: Нет производителя

"""

import logging
import sys
from time import sleep

from general_func.database import *
from general_func.exception import *
from general_func.modbus import *
from general_func.reset import ResetRelay
from general_func.resistance import Resistor
from general_func.subtest import Subtest2in, ReadOPCServer
from gui.msgbox_1 import *

__all__ = ["TestBURPMVIR"]


class TestBURPMVIR:

    def __init__(self):
        self.resist = Resistor()
        self.ctrl_kl = CtrlKL()
        self.mysql_conn = MySQLConnect()
        self.subtest = Subtest2in()
        self.di_read_full = ReadOPCServer()

        logging.basicConfig(
            filename="C:\\Stend\\project_class\\log\\TestBURPMVIR.log",
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
        if self.di_read_full.subtest_2di(test_num=1, subtest_num=1.0, err_code_a=166, err_code_b=167, position_a=False,
                                         position_b=False):
            return True
        return False

    def st_test_20(self) -> bool:
        """
        Тест 2. Проверка включения/выключения блока от кнопки «Пуск/Стоп» в режиме «Вперёд».
        2.4. Выключение блока от кнопки «Стоп» режима «Вперёд»
        """
        self.ctrl_kl.ctrl_relay('KL21', True)
        self.logger.debug("включен KL21")
        if self.di_read_full.subtest_2di(test_num=2, subtest_num=2.0, err_code_a=168, err_code_b=169, position_a=False,
                                         position_b=False):
            if self.subtest.subtest_a_bur(test_num=2, subtest_num=2.1, forward=True):
                if self.subtest.subtest_b_bur(test_num=2, subtest_num=2.2, forward=True):
                    self.ctrl_kl.ctrl_relay('KL12', False)
                    self.logger.debug("отключены KL12")
                    sleep(1)
                    if self.di_read_full.subtest_2di(test_num=2, subtest_num=2.3, err_code_a=174, err_code_b=175,
                                                     position_a=False, position_b=False):
                        self.ctrl_kl.ctrl_relay('KL25', False)
                        self.logger.debug("отключен KL25")
                        return True
        return False

    def st_test_30(self) -> bool:
        """
        3. Отключение контакта «Вперёд» при увеличении сопротивления цепи заземления
        """
        if self.subtest.subtest_a_bur(test_num=3, subtest_num=3.0, forward=True):
            if self.subtest.subtest_b_bur(test_num=3, subtest_num=3.1, forward=True):
                self.resist.resist_0_to_100_ohm()
                sleep(1)
                if self.di_read_full.subtest_2di(test_num=3, subtest_num=3.2, err_code_a=176, err_code_b=177,
                                                 position_a=False, position_b=False):
                    self.ctrl_kl.ctrl_relay('KL12', False)
                    self.ctrl_kl.ctrl_relay('KL25', False)
                    self.logger.debug("отключены KL12, KL25")
                    return True
        return False

    def st_test_40(self) -> bool:
        """
        4. Защита от потери управляемости канала «Вперёд» при замыкании проводов ДУ
        """
        if self.subtest.subtest_a_bur(test_num=4, subtest_num=4.0, forward=True):
            if self.subtest.subtest_b_bur(test_num=4, subtest_num=4.1, forward=True):
                self.ctrl_kl.ctrl_relay('KL11', True)
                self.logger.debug("включен KL11")
                sleep(2)
                if self.di_read_full.subtest_2di(test_num=4, subtest_num=4.2, err_code_a=178, err_code_b=179,
                                                 position_a=False, position_b=False):
                    self.ctrl_kl.ctrl_relay('KL12', False)
                    self.ctrl_kl.ctrl_relay('KL25', False)
                    self.ctrl_kl.ctrl_relay('KL11', False)
                    self.logger.debug("отключены KL12, KL25, KL11")
                    return True
        return False

    def st_test_50(self) -> bool:
        """
        Тест 5. Защита от потери управляемости канала «Вперёд» при обрыве проводов ДУ
        """
        if self.subtest.subtest_a_bur(test_num=5, subtest_num=5.0, forward=True):
            if self.subtest.subtest_b_bur(test_num=5, subtest_num=5.1, forward=True):
                self.ctrl_kl.ctrl_relay('KL12', False)
                self.logger.debug("отключен KL12")
                sleep(2)
                if self.di_read_full.subtest_2di(test_num=5, subtest_num=5.2, err_code_a=180, err_code_b=181,
                                                 position_a=False, position_b=False):
                    self.ctrl_kl.ctrl_relay('KL25', False)
                    self.logger.debug("отключен KL25")
                    return True
        return False

    def st_test_60(self) -> bool:
        """
        Тест 6. Проверка включения/выключения блока от кнопки «Пуск/Стоп» в режиме «Назад».
        Переключение в режим ДУ «Назад»	KL26 - ВКЛ
        """
        self.ctrl_kl.ctrl_relay('KL26', True)
        self.logger.debug("включен KL26")
        sleep(2)
        if self.di_read_full.subtest_2di(test_num=6, subtest_num=6.0, err_code_a=168, err_code_b=169, position_a=False,
                                         position_b=False):
            if self.subtest.subtest_a_bur(test_num=6, subtest_num=6.1, back=True):
                if self.subtest.subtest_b_bur(test_num=6, subtest_num=6.2, back=True):
                    # 6.4. Выключение блока от кнопки «Стоп» режима «Назад»
                    self.ctrl_kl.ctrl_relay('KL12', False)
                    self.logger.debug("отключен KL12")
                    sleep(2)
                    if self.di_read_full.subtest_2di(test_num=6, subtest_num=6.3, err_code_a=186, err_code_b=187,
                                                     position_a=False, position_b=False):
                        self.ctrl_kl.ctrl_relay('KL25', False)
                        self.logger.debug("отключен KL25")
                        return True
        return False

    def st_test_70(self) -> bool:
        """
        7. Отключение контакта «Назад» при увеличении сопротивления цепи заземления
        """
        if self.subtest.subtest_a_bur(test_num=7, subtest_num=7.0, back=True):
            if self.subtest.subtest_b_bur(test_num=7, subtest_num=7.1, back=True):
                self.resist.resist_0_to_100_ohm()
                sleep(2)
                if self.di_read_full.subtest_2di(test_num=7, subtest_num=7.2, err_code_a=188, err_code_b=189,
                                                 position_a=False, position_b=False):
                    self.ctrl_kl.ctrl_relay('KL12', False)
                    self.ctrl_kl.ctrl_relay('KL25', False)
                    self.logger.debug("отключены KL12, KL25")
                    return True
        return False

    def st_test_80(self) -> bool:
        """
        8. Защита от потери управляемости канала «Назад» при замыкании проводов ДУ
        """
        if self.subtest.subtest_a_bur(test_num=8, subtest_num=8.0, back=True):
            if self.subtest.subtest_b_bur(test_num=8, subtest_num=8.1, back=True):
                self.ctrl_kl.ctrl_relay('KL11', True)
                self.logger.debug("включен KL11")
                sleep(2)
                if self.di_read_full.subtest_2di(test_num=8, subtest_num=8.2, err_code_a=190, err_code_b=191,
                                                 position_a=False, position_b=False):
                    self.ctrl_kl.ctrl_relay('KL12', False)
                    self.ctrl_kl.ctrl_relay('KL25', False)
                    self.ctrl_kl.ctrl_relay('KL11', False)
                    self.logger.debug("отключены KL12, KL22, KL11")
                    return True
        return False

    def st_test_90(self) -> bool:
        """
        Тест 9. Защита от потери управляемости канала «Назад» при обрыве проводов ДУ
        """
        if self.subtest.subtest_a_bur(test_num=9, subtest_num=9.0, back=True):
            if self.subtest.subtest_b_bur(test_num=9, subtest_num=9.1, back=True):
                self.ctrl_kl.ctrl_relay('KL12', False)
                self.logger.debug("отключен KL12")
                sleep(2)
                if self.di_read_full.subtest_2di(test_num=9, subtest_num=9.2, err_code_a=192, err_code_b=193,
                                                 position_a=False, position_b=False):
                    self.ctrl_kl.ctrl_relay('KL25', False)
                    self.logger.debug("отключен KL25")
                    return True
        return False

    def st_test_100(self) -> bool:
        """
        Тест 10. Блокировка включения блока при снижении сопротивления изоляции контролируемого присоединения
        """
        self.resist.resist_kohm(30)
        sleep(2)
        self.ctrl_kl.ctrl_relay('KL12', True)
        self.logger.debug("включен KL12")
        sleep(2)
        if self.di_read_full.subtest_2di(test_num=10, subtest_num=10.0, err_code_a=194, err_code_b=195,
                                         position_a=False,
                                         position_b=False):
            self.ctrl_kl.ctrl_relay('KL12', False)
            self.logger.debug("отключен KL12")
            return True
        return False

    def st_test_101(self) -> bool:
        """
        Тест 11. Проверка работы режима «Проверка БРУ»
        """
        self.ctrl_kl.ctrl_relay('KL22', True)
        self.ctrl_kl.ctrl_relay('KL12', True)
        self.logger.debug("отключены KL12, KL22")
        sleep(2)
        if self.di_read_full.subtest_2di(test_num=10, subtest_num=10.1, err_code_a=196, err_code_b=197,
                                         position_a=False,
                                         position_b=False):
            return True
        return False

    def st_test_bur_pmvir(self) -> bool:
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
                                                if self.st_test_101():
                                                    return True
        return False


if __name__ == '__main__':
    test_bur_pmvir = TestBURPMVIR()
    reset_test_bur_pmvir = ResetRelay()
    mysql_conn_bur_pmvir = MySQLConnect()
    try:
        if test_bur_pmvir.st_test_bur_pmvir():
            mysql_conn_bur_pmvir.mysql_block_good()
            my_msg('Блок исправен', 'green')
        else:
            mysql_conn_bur_pmvir.mysql_block_bad()
            my_msg('Блок неисправен', 'red')
    except OSError:
        my_msg("ошибка системы", 'red')
    except SystemError:
        my_msg("внутренняя ошибка", 'red')
    except ModbusConnectException as mce:
        my_msg(f'{mce}', 'red')
    finally:
        reset_test_bur_pmvir.reset_all()
        sys.exit()
