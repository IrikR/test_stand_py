#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тип блока     Производитель
БДУ-Р-Т	Нет производителя
БДУ-Р-Т	ТЭТЗ-Инвест
БДУ-Р-Т	Стройэнергомаш

"""

import sys
import logging

from time import sleep

from gen_func_utils import *
from my_msgbox import *
from gen_mb_client import *
from gen_mysql_connect import *

__all__ = ["TestBDURT"]


class TestBDURT(object):

    def __init__(self):
        self.__resist = Resistor()
        self.__ctrl_kl = CtrlKL()
        self.__read_mb = ReadMB()
        self.__mysql_conn = MySQLConnect()
        self.__fault = Bug(None)

        logging.basicConfig(filename="C:\Stend\project_class\TestBDURT.log",
                            filemode="w",
                            level=logging.DEBUG,
                            encoding="utf-8",
                            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('WARNING')
        self.logger = logging.getLogger(__name__)

    def st_test_1_bdu_r_t(self) -> bool:
        self.__mysql_conn.mysql_ins_result("идет тест 1", '1')
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is False and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", '1')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(288)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(288)
            return False
        self.__mysql_conn.mysql_ins_result("исправен", "1")
        return True

    def st_test_20_bdu_r_t(self) -> bool:
        """
        Тест 2. Проверка включения/выключения блока от кнопки «Пуск/Стоп» в режиме «Вперед».
        """
        self.__mysql_conn.mysql_ins_result("идет тест 2", '2')
        self.__ctrl_kl.ctrl_relay('KL2', True)
        sleep(1)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is False and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", '2')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(290)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(291)
            return False
        return True

    def st_test_21_bdu_r_t(self) -> bool:
        """
        2.2. Включение блока от кнопки «Пуск» в режиме «Вперёд»
        2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        """
        if self.__subtest_22(2.2, 2):
            if self.__subtest_23(2.3, 2):
                return True
        return False

    def st_test_22_bdu_r_t(self) -> bool:
        """
        2.4. Выключение блока в режиме «Вперед» от кнопки «Стоп»
        """
        self.__mysql_conn.mysql_ins_result("идет тест 2.4", '2')
        self.__ctrl_kl.ctrl_relay('KL12', False)
        sleep(1)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is False and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", '2')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(296)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(297)
            return False
        self.__ctrl_kl.ctrl_relay('KL25', False)
        self.__ctrl_kl.ctrl_relay('KL1', False)
        self.__mysql_conn.mysql_ins_result("исправен", '2')
        return True

    def st_test_30_bdu_r_t(self) -> bool:
        """
        Тест 3. Проверка включения/выключения блока от кнопки «Пуск/Стоп» в режиме «Назад»
        3.1. Включение блока от кнопки «Пуск» в режиме «Назад»
        """
        self.__mysql_conn.mysql_ins_result("идет тест 3.1", '3')
        self.__ctrl_kl.ctrl_relay('KL26', True)
        self.__resist.resist_ohm(10)
        self.__ctrl_kl.ctrl_relay('KL12', True)
        sleep(1)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is False and in_a2 is True:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", '3')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(298)
            elif in_a2 is False:
                self.__mysql_conn.mysql_error(299)
            return False
        return True

    def st_test_31_bdu_r_t(self) -> bool:
        """
        3.2. Проверка удержания контактов К5.2 режима «Назад» блока во включенном состоянии
        при подключении Rш пульта управления:
        """
        self.__mysql_conn.mysql_ins_result("идет тест 3.2", '3')
        self.__ctrl_kl.ctrl_relay('KL27', True)
        self.__ctrl_kl.ctrl_relay('KL1', True)
        self.__ctrl_kl.ctrl_relay('KL25', True)
        sleep(1)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is True and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", '3')
            if in_a1 is False:
                self.__mysql_conn.mysql_error(300)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(301)
            return False
        return True

    def st_test_32_bdu_r_t(self) -> bool:
        """
        3.3. Выключение блока в режиме «Вперед» от кнопки «Стоп»
        """
        self.__mysql_conn.mysql_ins_result("идет тест 3.3", '3')
        self.__ctrl_kl.ctrl_relay('KL12', False)
        sleep(1)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is False and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", '3')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(302)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(303)
            return False
        self.__ctrl_kl.ctrl_relay('KL26', False)
        self.__ctrl_kl.ctrl_relay('KL27', False)
        self.__ctrl_kl.ctrl_relay('KL1', False)
        self.__ctrl_kl.ctrl_relay('KL25', False)
        self.__mysql_conn.mysql_ins_result("исправен", '3')
        return True

    def st_test_40_bdu_r_t(self) -> bool:
        """
        Повторяем тест 2.2. Включение блока от кнопки «Пуск» в режиме «Вперёд»
        Повторяем тест 2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        """
        if self.__subtest_22(4.1, 4):
            if self.__subtest_23(4.2, 4):
                return True
        return False

    def st_test_41_bdu_r_t(self) -> bool:
        """
        # 4. Отключение исполнительного элемента при увеличении сопротивления цепи заземления на величину свыше 50 Ом
        """
        self.__mysql_conn.mysql_ins_result("идет тест 4.3", '4')
        self.__resist.resist_10_to_50_ohm()
        sleep(1)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is False and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", '4')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(304)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(305)
            return False
        self.__ctrl_kl.ctrl_relay('KL12', False)
        self.__ctrl_kl.ctrl_relay('KL25', False)
        self.__ctrl_kl.ctrl_relay('KL1', False)
        self.__mysql_conn.mysql_ins_result("исправен", '4')
        return True

    def st_test_50_bdu_r_t(self) -> bool:
        """
        Повторяем тест 2.2. Включение блока от кнопки «Пуск» в режиме «Вперёд»
        Повторяем тест 2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        """
        if self.__subtest_22(5.1, 5):
            if self.__subtest_23(5.2, 5):
                return True
        return False

    def st_test_51_bdu_r_t(self) -> bool:
        """
        # 5. Защита от потери управляемости при замыкании проводов ДУ
        """
        self.__mysql_conn.mysql_ins_result("идет тест 5.3", '5')
        self.__ctrl_kl.ctrl_relay('KL11', True)
        sleep(1)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is False and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", '5')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(306)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(307)
            return False
        self.__ctrl_kl.ctrl_relay('KL12', False)
        self.__ctrl_kl.ctrl_relay('KL1', False)
        self.__ctrl_kl.ctrl_relay('KL25', False)
        self.__ctrl_kl.ctrl_relay('KL11', False)
        self.__mysql_conn.mysql_ins_result("исправен", '5')
        return True

    def st_test_60_bdu_r_t(self) -> bool:
        """
        Повторяем тест 2.2. Включение блока от кнопки «Пуск» в режиме «Вперёд»
        Повторяем тест 2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        """
        if self.__subtest_22(6.1, 6):
            if self.__subtest_23(6.2, 6):
                return True
        return False

    def st_test_61_bdu_r_t(self) -> bool:
        """
        # Тест 6. Защита от потери управляемости при обрыве проводов ДУ
        """
        self.__mysql_conn.mysql_ins_result("идет тест 6.3", '6')
        self.__ctrl_kl.ctrl_relay('KL12', False)
        sleep(1)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is False and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", '6')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(308)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(309)
            return False
        self.__mysql_conn.mysql_ins_result("исправен", '6')
        return True

    def st_test_70_bdu_r_t(self) -> bool:
        """
        # Тест 7. Проверка работоспособности функции "Проверка" блока
        """
        self.__mysql_conn.mysql_ins_result("идет тест 7", '7')
        self.__ctrl_kl.ctrl_relay('KL24', True)
        sleep(1)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is False and in_a2 is True:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", '7')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(310)
            elif in_a2 is False:
                self.__mysql_conn.mysql_error(311)
            return False
        self.__mysql_conn.mysql_ins_result("исправен", '7')
        return True

    def __subtest_22(self, subtest_2_num: float, test_2_num: int) -> bool:
        """
        # 2.2. Включение блока от кнопки «Пуск»
        """
        self.__mysql_conn.mysql_ins_result(f'идёт тест {subtest_2_num}', f'{test_2_num}')
        self.__resist.resist_ohm(10)
        self.__ctrl_kl.ctrl_relay('KL12', True)
        sleep(1)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is True and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", f'{test_2_num}')
            self.__fault.debug_msg(f'тест {subtest_2_num} положение выходов не соответствует', 1)
            if in_a1 is False:
                self.__mysql_conn.mysql_error(292)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(293)
            return False
        self.__fault.debug_msg(f'тест {subtest_2_num} положение выходов соответствует', 4)
        return True

    def __subtest_23(self, subtest_3_num: float, test_3_num: int) -> bool:
        """
        2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        """
        self.__mysql_conn.mysql_ins_result(f'идёт тест {subtest_3_num}', f'{test_3_num}')
        self.__ctrl_kl.ctrl_relay('KL1', True)
        self.__ctrl_kl.ctrl_relay('KL25', True)
        sleep(1)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is True and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", f'{test_3_num}')
            self.__fault.debug_msg(f'тест {subtest_3_num} положение выходов не соответствует', 1)
            if in_a1 is False:
                self.__mysql_conn.mysql_error(294)
            elif in_a2 is False:
                self.__mysql_conn.mysql_error(295)
            return False
        self.__fault.debug_msg(f'тест {subtest_3_num} положение выходов соответствует', 4)
        return True

    def __inputs_a(self):
        in_a1 = self.__read_mb.read_discrete(1)
        in_a2 = self.__read_mb.read_discrete(2)
        if in_a1 is None or in_a2 is None:
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_a1, in_a2

    def st_test_bdu_r_t(self) -> bool:
        """
        Главная функция которая собирает все остальные
        """
        if self.st_test_1_bdu_r_t():
            if self.st_test_20_bdu_r_t():
                if self.st_test_21_bdu_r_t():
                    if self.st_test_22_bdu_r_t():
                        if self.st_test_30_bdu_r_t():
                            if self.st_test_31_bdu_r_t():
                                if self.st_test_32_bdu_r_t():
                                    if self.st_test_40_bdu_r_t():
                                        if self.st_test_41_bdu_r_t():
                                            if self.st_test_50_bdu_r_t():
                                                if self.st_test_51_bdu_r_t():
                                                    if self.st_test_60_bdu_r_t():
                                                        if self.st_test_61_bdu_r_t():
                                                            if self.st_test_70_bdu_r_t():
                                                                return True
        return False


if __name__ == '__main__':
    test_bdu_r_t = TestBDURT()
    reset_test_bdu_r_t = ResetRelay()
    mysql_conn_bdu_r_t = MySQLConnect()
    fault = Bug(True)
    try:
        if test_bdu_r_t.st_test_bdu_r_t():
            mysql_conn_bdu_r_t.mysql_block_good()
            my_msg('Блок исправен', 'green')
        else:
            mysql_conn_bdu_r_t.mysql_block_bad()
            my_msg('Блок неисправен', 'red')
    except OSError:
        my_msg("ошибка системы", 'red')
    except SystemError:
        my_msg("внутренняя ошибка", 'red')
    except ModbusConnectException as mce:
        fault.debug_msg(mce, 'red')
        my_msg(f'{mce}', 'red')
    finally:
        reset_test_bdu_r_t.reset_all()
        sys.exit()
