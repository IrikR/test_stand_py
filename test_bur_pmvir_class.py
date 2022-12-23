#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки
Тип блока Производитель
БУР ПМВИР (пускатель)	Нет производителя

"""

import sys
import logging

from time import sleep

from gen_func_utils import *
from my_msgbox import *
from gen_mb_client import *
from gen_mysql_connect import *

__all__ = ["TestBURPMVIR"]


class TestBURPMVIR(object):

    def __init__(self):
        self.__resist = Resistor()
        self.__read_mb = ReadMB()
        self.__ctrl_kl = CtrlKL()
        self.__mysql_conn = MySQLConnect()
        self.__fault = Bug(True)

        logging.basicConfig(filename="C:\Stend\project_class\TestBURPMVIR.log",
                            filemode="w",
                            level=logging.DEBUG,
                            encoding="utf-8",
                            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('WARNING')
        self.logger = logging.getLogger(__name__)

    def st_test_10_bur_pmvir(self) -> bool:
        """
        Тест 1. Проверка исходного состояния блока:
        """
        in_a1, in_a2 = self.__inputs_a()
        self.__fault.debug_msg(f'Тест 1.0 {in_a1 = } (False), {in_a2 = } (False)', 'blue')
        if in_a1 is False and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", '1')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(166)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(167)
            return False
        self.__mysql_conn.mysql_ins_result("исправен", '1')
        return True

    def st_test_20_bur_pmvir(self) -> bool:
        """
        Тест 2. Проверка включения/выключения блока от кнопки «Пуск/Стоп» в режиме «Вперёд».
        """
        self.__ctrl_kl.ctrl_relay('KL21', True)
        in_a1, in_a2 = self.__inputs_a()
        self.__fault.debug_msg(f'Тест 2.0 {in_a1 = } (False), {in_a2 = } (False)', 'blue')
        if in_a1 is False and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", '2')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(168)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(169)
            return False
        return True

    def st_test_21_bur_pmvir(self) -> bool:
        if self.__subtest_22(2):
            if self.__subtest_23(2):
                return True
        return False

    def st_test_22_bur_pmvir(self) -> bool:
        """
        2.4. Выключение блока от кнопки «Стоп» режима «Вперёд»
        """
        self.__ctrl_kl.ctrl_relay('KL12', False)
        sleep(1)
        in_a1, in_a2 = self.__inputs_a()
        self.__fault.debug_msg(f'Тест 2.4 {in_a1 = } (False), {in_a2 = } (False)', 'blue')
        if in_a1 is False and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", '2')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(174)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(175)
            return False
        self.__ctrl_kl.ctrl_relay('KL25', False)
        self.__mysql_conn.mysql_ins_result("исправен", '2')
        return True

    def st_test_30_bur_pmvir(self) -> bool:
        """
        3. Отключение контакта «Вперёд» при увеличении сопротивления цепи заземления
        """
        if self.__subtest_22(3):
            if self.__subtest_23(3):
                return True
        return False

    def st_test_31_bur_pmvir(self) -> bool:
        """
        Формирование 100 Ом
        """
        self.__resist.resist_0_to_100_ohm()
        sleep(1)
        in_a1, in_a2 = self.__inputs_a()
        self.__fault.debug_msg(f'Тест 3.1 {in_a1 = } (False), {in_a2 = } (False)', 'blue')
        if in_a1 is False and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", '3')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(176)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(177)
            return False
        self.__mysql_conn.mysql_ins_result("исправен", '3')
        self.__ctrl_kl.ctrl_relay('KL12', False)
        self.__ctrl_kl.ctrl_relay('KL25', False)
        return True

    def st_test_40_bur_pmvir(self) -> bool:
        """
        4. Защита от потери управляемости канала «Вперёд» при замыкании проводов ДУ
        """
        if self.__subtest_22(4):
            if self.__subtest_23(4):
                return True
        return False

    def st_test_41_bur_pmvir(self) -> bool:
        self.__ctrl_kl.ctrl_relay('KL11', True)
        sleep(2)
        in_a1, in_a2 = self.__inputs_a()
        self.__fault.debug_msg(f'Тест 4.1 {in_a1 = } (False), {in_a2 = } (False)', 'blue')
        if in_a1 is False and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", '4')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(178)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(179)
            return False
        self.__mysql_conn.mysql_ins_result("исправен", '4')
        self.__ctrl_kl.ctrl_relay('KL12', False)
        self.__ctrl_kl.ctrl_relay('KL25', False)
        self.__ctrl_kl.ctrl_relay('KL11', False)
        return True

    def st_test_50_bur_pmvir(self) -> bool:
        """
        Тест 5. Защита от потери управляемости канала «Вперёд» при обрыве проводов ДУ
        """
        if self.__subtest_22(5):
            if self.__subtest_23(5):
                return True
        return False

    def st_test_51_bur_pmvir(self) -> bool:
        self.__ctrl_kl.ctrl_relay('KL12', False)
        sleep(2)
        in_a1, in_a2 = self.__inputs_a()
        self.__fault.debug_msg(f'Тест 5.1 {in_a1 = } (False), {in_a2 = } (False)', 'blue')
        if in_a1 is False and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", '5')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(180)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(181)
            return False
        self.__mysql_conn.mysql_ins_result("исправен", '5')
        self.__ctrl_kl.ctrl_relay('KL25', False)
        return True

    def st_test_60_bur_pmvir(self) -> bool:
        """
        Тест 6. Проверка включения/выключения блока от кнопки «Пуск/Стоп» в режиме «Назад».
        Переключение в режим ДУ «Назад»	KL26 - ВКЛ
        """
        self.__ctrl_kl.ctrl_relay('KL26', True)
        sleep(2)
        in_a1, in_a2 = self.__inputs_a()
        self.__fault.debug_msg(f'Тест 6.0 {in_a1 = } (False), {in_a2 = } (False)', 'blue')
        if in_a1 is False and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", '6')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(168)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(169)
            return False
        return True

    def st_test_61_bur_pmvir(self) -> bool:
        if self.__subtest_62(6):
            if self.__subtest_63(6):
                return True
        return False

    def st_test_62_bur_pmvir(self) -> bool:
        """
        6.4. Выключение блока от кнопки «Стоп» режима «Назад»
        """
        self.__ctrl_kl.ctrl_relay('KL12', False)
        sleep(2)
        in_a1, in_a2 = self.__inputs_a()
        self.__fault.debug_msg(f'Тест 6.4 {in_a1 = } (False), {in_a2 = } (False)', 'blue')
        if in_a1 is False and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", '6')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(186)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(187)
            return False
        self.__mysql_conn.mysql_ins_result("исправен", '6')
        self.__ctrl_kl.ctrl_relay('KL25', False)
        return True

    def st_test_70_bur_pmvir(self) -> bool:
        """
        7. Отключение контакта «Назад» при увеличении сопротивления цепи заземления
        """
        if self.__subtest_62(7):
            if self.__subtest_63(7):
                return True
        return False

    def st_test_71_bur_pmvir(self) -> bool:
        self.__resist.resist_0_to_100_ohm()
        sleep(2)
        in_a1, in_a2 = self.__inputs_a()
        self.__fault.debug_msg(f'Тест 7.1 {in_a1 = } (False), {in_a2 = } (False)', 'blue')
        if in_a1 is False and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", '7')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(188)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(189)
            return False
        self.__mysql_conn.mysql_ins_result("исправен", '7')
        self.__ctrl_kl.ctrl_relay('KL12', False)
        self.__ctrl_kl.ctrl_relay('KL25', False)
        return True

    def st_test_80_bur_pmvir(self) -> bool:
        """
        8. Защита от потери управляемости канала «Назад» при замыкании проводов ДУ
        """
        if self.__subtest_62(8):
            if self.__subtest_63(8):
                return True
        return False

    def st_test_81_bur_pmvir(self) -> bool:
        self.__ctrl_kl.ctrl_relay('KL11', True)
        sleep(2)
        in_a1, in_a2 = self.__inputs_a()
        self.__fault.debug_msg(f'Тест 8.1 {in_a1 = } (False), {in_a2 = } (False)', 'blue')
        if in_a1 is False and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", '8')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(190)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(191)
            return False
        self.__mysql_conn.mysql_ins_result("исправен", '8')
        self.__ctrl_kl.ctrl_relay('KL12', False)
        self.__ctrl_kl.ctrl_relay('KL25', False)
        self.__ctrl_kl.ctrl_relay('KL11', False)
        return True

    def st_test_90_bur_pmvir(self) -> bool:
        """
        Тест 9. Защита от потери управляемости канала «Назад» при обрыве проводов ДУ
        """
        if self.__subtest_62(9):
            if self.__subtest_63(9):
                return True
        return False

    def st_test_91_bur_pmvir(self) -> bool:
        self.__ctrl_kl.ctrl_relay('KL12', False)
        sleep(2)
        in_a1, in_a2 = self.__inputs_a()
        self.__fault.debug_msg(f'Тест 9.1 {in_a1 = } (False), {in_a2 = } (False)', 'blue')
        if in_a1 is False and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", '9')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(192)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(193)
            return False
        self.__mysql_conn.mysql_ins_result("исправен", '9')
        self.__ctrl_kl.ctrl_relay('KL25', False)
        return True

    def st_test_100_bur_pmvir(self) -> bool:
        """
        Тест 10. Блокировка включения блока при снижении сопротивления изоляции контролируемого присоединения
        """
        self.__resist.resist_kohm(30)
        sleep(2)
        self.__ctrl_kl.ctrl_relay('KL12', True)
        sleep(2)
        in_a1, in_a2 = self.__inputs_a()
        self.__fault.debug_msg(f'Тест 10.0 {in_a1 = } (False), {in_a2 = } (False)', 'blue')
        if in_a1 is False and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", '10')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(194)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(195)
            return False
        self.__mysql_conn.mysql_ins_result("исправен", '10')
        self.__ctrl_kl.ctrl_relay('KL12', False)
        return True

    def st_test_101_bur_pmvir(self) -> bool:
        """
        Тест 11. Проверка работы режима «Проверка БРУ»
        """
        self.__ctrl_kl.ctrl_relay('KL22', True)
        self.__ctrl_kl.ctrl_relay('KL12', True)
        sleep(2)
        in_a1, in_a2 = self.__inputs_a()
        self.__fault.debug_msg(f'Тест 10.1 {in_a1 = } (False), {in_a2 = } (False)', 'blue')
        if in_a1 is False and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", '11')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(196)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(197)
            return False
        self.__mysql_conn.mysql_ins_result("исправен", '11')
        return True

    def __subtest_22(self, test_0_num: int) -> bool:
        """
        2.2. Включение блока от кнопки «Пуск» режима «Вперёд»
        """
        self.__resist.resist_ohm(0)
        sleep(2)
        self.__ctrl_kl.ctrl_relay('KL12', True)
        sleep(2)
        in_a1, in_a2 = self.__inputs_a()
        self.__fault.debug_msg(f'Тест 2.2 {in_a1 = } (True), {in_a2 = } (False)', 'blue')
        if in_a1 is True and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", f'{test_0_num}')
            if in_a1 is False:
                self.__mysql_conn.mysql_error(170)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(171)
            return False
        return True

    def __subtest_23(self, test_1_num: int) -> bool:
        """
        2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления режима «Вперёд»:
        """
        self.__ctrl_kl.ctrl_relay('KL25', True)
        sleep(2)
        in_a1, in_a2 = self.__inputs_a()
        self.__fault.debug_msg(f'Тест 2.3 {in_a1 = } (True), {in_a2 = } (False)', 'blue')
        if in_a1 is True and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", f'{test_1_num}')
            if in_a1 is False:
                self.__mysql_conn.mysql_error(172)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(173)
            return False
        return True

    def __subtest_62(self, test_2_num: int) -> bool:
        """
        6.2. Включение блока от кнопки «Пуск» режима «Назад»
        """
        self.__resist.resist_ohm(0)
        sleep(2)
        self.__ctrl_kl.ctrl_relay('KL12', True)
        sleep(2)
        in_a1, in_a2 = self.__inputs_a()
        self.__fault.debug_msg(f'Тест 6.2 {in_a1 = } (False), {in_a2 = } (True)', 'blue')
        if in_a1 is False and in_a2 is True:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", f'{test_2_num}')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(182)
            elif in_a2 is False:
                self.__mysql_conn.mysql_error(183)
            return False
        return True

    def __subtest_63(self, test_3_num: int) -> bool:
        """
        6.3. Проверка удержания блока во включенном состоянии
        при подключении Rш пульта управления режима «Назад»:
        """
        self.__ctrl_kl.ctrl_relay('KL25', True)
        sleep(2)
        in_a1, in_a2 = self.__inputs_a()
        self.__fault.debug_msg(f'Тест 6.3 {in_a1 = } (False), {in_a2 = } (True)', 'blue')
        if in_a1 is False and in_a2 is True:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", f'{test_3_num}')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(184)
            elif in_a2 is False:
                self.__mysql_conn.mysql_error(185)
            return False
        return True

    def __inputs_a(self):
        in_a1 = self.__read_mb.read_discrete(1)
        in_a2 = self.__read_mb.read_discrete(2)
        if in_a1 is None or in_a2 is None:
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_a1, in_a2

    def st_test_bur_pmvir(self) -> bool:
        if self.st_test_10_bur_pmvir():
            pass
        else:
            return False
        if self.st_test_20_bur_pmvir():
            pass
        else:
            return False
        if self.st_test_21_bur_pmvir():
            pass
        else:
            return False
        if self.st_test_22_bur_pmvir():
            pass
        else:
            return False
        if self.st_test_30_bur_pmvir():
            pass
        else:
            return False
        if self.st_test_31_bur_pmvir():
            pass
        else:
            return False
        if self.st_test_40_bur_pmvir():
            pass
        else:
            return False
        if self.st_test_41_bur_pmvir():
            pass
        else:
            return False
        if self.st_test_50_bur_pmvir():
            pass
        else:
            return False
        if self.st_test_51_bur_pmvir():
            pass
        else:
            return False
        if self.st_test_60_bur_pmvir():
            pass
        else:
            return False
        if self.st_test_61_bur_pmvir():
            pass
        else:
            return False
        if self.st_test_62_bur_pmvir():
            pass
        else:
            return False
        if self.st_test_70_bur_pmvir():
            pass
        else:
            return False
        if self.st_test_71_bur_pmvir():
            pass
        else:
            return False
        if self.st_test_80_bur_pmvir():
            pass
        else:
            return False
        if self.st_test_81_bur_pmvir():
            pass
        else:
            return False
        if self.st_test_90_bur_pmvir():
            pass
        else:
            return False
        if self.st_test_91_bur_pmvir():
            pass
        else:
            return False
        if self.st_test_100_bur_pmvir():
            pass
        else:
            return False
        if self.st_test_101_bur_pmvir():
            pass
        else:
            return False
        return True


if __name__ == '__main__':
    test_bur_pmvir = TestBURPMVIR()
    reset_test_bur_pmvir = ResetRelay()
    mysql_conn_bur_pmvir = MySQLConnect()
    fault = Bug(True)
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
        fault.debug_msg(mce, 'red')
        my_msg(f'{mce}', 'red')
    finally:
        reset_test_bur_pmvir.reset_all()
        sys.exit()
