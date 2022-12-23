#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки

Тип блока	Производитель	    Уникальный номер
БРУ-2СР	Нет производителя

"""

import sys
import logging

from time import sleep

from my_msgbox import *
from gen_func_utils import *
from gen_mb_client import *
from gen_mysql_connect import *

__all__ = ["TestBRU2SR"]


class TestBRU2SR(object):

    def __init__(self):
        self.__resist = Resistor()
        self.__read_mb = ReadMB()
        self.__ctrl_kl = CtrlKL()
        self.__mysql_conn = MySQLConnect()
        self.__fault = Bug(None)

        logging.basicConfig(filename="C:\Stend\project_class\TestBRU2SR.log",
                            filemode="w",
                            level=logging.DEBUG,
                            encoding="utf-8",
                            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('WARNING')
        self.logger = logging.getLogger(__name__)

    def st_test_10_bru_2sr(self) -> bool:
        """
        Тест 1. Проверка исходного состояния блока:
        """
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is False and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '1')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(57)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(58)
            return False
        self.__mysql_conn.mysql_ins_result('исправен', '1')
        return True

    def st_test_20_bru_2sr(self) -> bool:
        """
        Тест 2. Проверка включения/выключения блока от кнопки «Пуск/Стоп» в режиме «Вперёд».
        """
        self.__ctrl_kl.ctrl_relay('KL21', True)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is False and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '2')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(59)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(60)
            return False
        return True

    def st_test_21_bru_2sr(self) -> bool:
        """
        2.2. Включение блока от кнопки «Пуск»
        2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        """
        if self.__subtest_22(2.2, 2):
            if self.__subtest_23(2.3, 2):
                return True
        return False

    def st_test_22_bru_2sr(self) -> bool:
        """
        2.4. Выключение блока от кнопки «Стоп»
        """
        self.__ctrl_kl.ctrl_relay('KL12', False)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is False and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '2')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(65)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(66)
            return False
        self.__ctrl_kl.ctrl_relay('KL25', False)
        self.__mysql_conn.mysql_ins_result('исправен', '2')
        return True

    def st_test_30_bru_2sr(self) -> bool:
        """
        Повторяем подтест 2.2. Включение блока от кнопки «Пуск»
        Повторяем подтест 2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        """
        if self.__subtest_22(3.1, 3):
            if self.__subtest_23(3.2, 3):
                return True
        return False

    def st_test_31_bru_2sr(self) -> bool:
        """
        3. Отключение контакта «Вперёд» при увеличении сопротивления цепи заземления
        """
        self.__resist.resist_ohm(150)
        sleep(1)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is False and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '3')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(67)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(68)
            return False
        self.__ctrl_kl.ctrl_relay('KL12', False)
        self.__ctrl_kl.ctrl_relay('KL25', False)
        self.__mysql_conn.mysql_ins_result('исправен', '3')
        return True

    def st_test_40_bru_2sr(self) -> bool:
        """
        Повторяем подтест 2.2. Включение блока от кнопки «Пуск»
        Повторяем подтест 2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        """
        if self.__subtest_22(4.1, 4):
            if self.__subtest_23(4.2, 4):
                return True
        return False

    def st_test_41_bru_2sr(self) -> bool:
        """
        4. Защита от потери управляемости канала «Вперёд» при замыкании проводов ДУ
        """
        self.__ctrl_kl.ctrl_relay('KL11', True)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is False and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '4')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(69)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(70)
            return False
        self.__ctrl_kl.ctrl_relay('KL12', False)
        self.__ctrl_kl.ctrl_relay('KL25', False)
        self.__ctrl_kl.ctrl_relay('KL11', False)
        self.__mysql_conn.mysql_ins_result('исправен', '4')
        return True

    def st_test_50_bru_2sr(self) -> bool:
        """
        Повторяем подтест 2.2. Включение блока от кнопки «Пуск»
        Повторяем подтест 2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        """
        if self.__subtest_22(5.1, 5):
            if self.__subtest_23(5.2, 5):
                return True
        return False

    def st_test_51_bru_2sr(self) -> bool:
        """
        Тест 5. Защита от потери управляемости канала «Вперёд» при обрыве проводов ДУ
        """
        self.__ctrl_kl.ctrl_relay('KL12', False)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is False and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '5')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(71)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(72)
            return False
        self.__ctrl_kl.ctrl_relay('KL25', False)
        self.__mysql_conn.mysql_ins_result('исправен', '5')
        return True

    def st_test_60_bru_2sr(self) -> bool:
        """
        Тест 6. Проверка включения/выключения блока от кнопки «Пуск/Стоп» в режиме «Назад».
        """
        self.__ctrl_kl.ctrl_relay('KL26', True)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is False and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '6')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(59)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(60)
            return False
        return True

    def st_test_61_bru_2sr(self) -> bool:
        """
        6.2. Включение блока от кнопки «Пуск» режима «Назад»
        6.3. Проверка удержания блока во включенном состоянии
        при подключении Rш пульта управления режима «Назад»:
        """
        if self.__subtest_62(6.2, 6):
            if self.__subtest_63(6.3, 6):
                return True
        return False

    def st_test_62_bru_2sr(self) -> bool:
        """
        6.4. Выключение блока от кнопки «Стоп» режима «Назад»
        """
        self.__ctrl_kl.ctrl_relay('KL12', False)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is False and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '6')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(77)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(78)
            return False
        self.__ctrl_kl.ctrl_relay('KL25', False)
        self.__mysql_conn.mysql_ins_result('исправен', '6')
        return True

    def st_test_70_bru_2sr(self) -> bool:
        """
        Повторяем подтест 6.2. Включение блока от кнопки «Пуск» режима «Назад»
        Повторяем подтест 6.3. Проверка удержания блока во включенном состоянии
        при подключении Rш пульта управления режима «Назад»:
        """
        if self.__subtest_62(7.1, 7):
            if self.__subtest_63(7.2, 7):
                return True
        return False

    def st_test_71_bru_2sr(self) -> bool:
        """
        7. Отключение контакта «Назад» при увеличении сопротивления цепи заземления
        """
        self.__resist.resist_ohm(150)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is False and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '7')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(79)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(80)
            return False
        self.__ctrl_kl.ctrl_relay('KL12', False)
        self.__ctrl_kl.ctrl_relay('KL25', False)
        self.__mysql_conn.mysql_ins_result('исправен', '7')
        return True

    def st_test_80_bru_2sr(self) -> bool:
        """
        Повторяем подтест 6.2. Включение блока от кнопки «Пуск» режима «Назад»
        Повторяем подтест 6.3. Проверка удержания блока во включенном состоянии
        при подключении Rш пульта управления режима «Назад»:
        """
        if self.__subtest_62(8.1, 8):
            if self.__subtest_63(8.2, 8):
                return True
        return False

    def st_test_81_bru_2sr(self) -> bool:
        """
        8. Защита от потери управляемости канала «Назад» при замыкании проводов ДУ
        """
        self.__ctrl_kl.ctrl_relay('KL11', True)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is False and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '8')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(81)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(82)
            return False
        self.__ctrl_kl.ctrl_relay('KL12', False)
        self.__ctrl_kl.ctrl_relay('KL25', False)
        self.__ctrl_kl.ctrl_relay('KL11', False)
        self.__mysql_conn.mysql_ins_result('исправен', '8')
        return True

    def st_test_90_bru_2sr(self) -> bool:
        """
        Повторяем подтест 6.2. Включение блока от кнопки «Пуск» режима «Назад»
        Повторяем подтест 6.3. Проверка удержания блока во включенном состоянии
        при подключении Rш пульта управления режима «Назад»:
        """
        if self.__subtest_62(9.1, 9):
            if self.__subtest_63(9.2, 9):
                return True
        return False

    def st_test_91_bru_2sr(self) -> bool:
        """
        Тест 9. Защита от потери управляемости канала «Назад» при обрыве проводов ДУ
        """
        self.__ctrl_kl.ctrl_relay('KL12', False)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is False and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '9')
            if in_a1 is True:
                self.__mysql_conn.mysql_error(83)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(84)
            return False
        self.__ctrl_kl.ctrl_relay('KL25', False)
        self.__mysql_conn.mysql_ins_result('исправен', '9')
        return True

    def st_test_100_bru_2sr(self) -> bool:
        msg_1 = "Переведите тумблер «П/А» на блоке в положение «П» и нажмите кнопку «ОК» " \
                "Если на блоке нет тумблера «П/А» нажмите кнопку «Отмена»"
        if my_msg(msg_1):
            if self.__subtest_10():
                self.__mysql_conn.mysql_ins_result('исправен', '10')
                if self.__subtest_11():
                    self.__mysql_conn.mysql_ins_result('исправен', '11')
                else:
                    self.__mysql_conn.mysql_ins_result('неисправен', '11')
                    return False
            else:
                self.__mysql_conn.mysql_ins_result('неисправен', '10')
                return False
        else:
            if self.__subtest_11():
                self.__mysql_conn.mysql_ins_result('пропущен', '10')
                self.__mysql_conn.mysql_ins_result('исправен', '11')
            else:
                self.__mysql_conn.mysql_ins_result('пропущен', '10')
                self.__mysql_conn.mysql_ins_result('неисправен', '11')
                return False
        return True
    
    def __subtest_22(self, subtest_0_num: float, test_0_num: int) -> bool:
        """
        # 2.2. Включение блока от кнопки «Пуск» режима «Вперёд»
        """
        self.__mysql_conn.mysql_ins_result(f'идёт тест {subtest_0_num}', f'{test_0_num}')
        self.__resist.resist_ohm(0)
        self.__ctrl_kl.ctrl_relay('KL12', True)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is True and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result(f'неисправен', f'{test_0_num}')
            self.__fault.debug_msg(f'подтест {subtest_0_num} не пройден', 1)
            if in_a1 is False:
                self.__mysql_conn.mysql_error(61)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(62)
            return False
        self.__fault.debug_msg(f'подтест {subtest_0_num} пройден', 3)
        return True

    def __subtest_23(self, subtest_1_num: float, test_1_num: int) -> bool:
        """
        2.3. Проверка удержания блока во включенном состоянии при
        подключении Rш пульта управления режима «Вперёд»:
        """
        self.__mysql_conn.mysql_ins_result(f'идёт тест {subtest_1_num}', f'{test_1_num}')
        self.__ctrl_kl.ctrl_relay('KL25', True)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is True and in_a2 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result(f'неисправен', f'{test_1_num}')
            self.__fault.debug_msg(f'подтест {subtest_1_num} не пройден', 1)
            if in_a1 is False:
                self.__mysql_conn.mysql_error(63)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(64)
            return False
        self.__fault.debug_msg(f'подтест {subtest_1_num} пройден', 3)
        return True

    def __subtest_62(self, subtest_2_num: float, test_2_num: int) -> bool:
        """
        6.2. Включение блока от кнопки «Пуск» режима «Назад»
        """
        self.__mysql_conn.mysql_ins_result(f'идёт тест {subtest_2_num}', f'{test_2_num}')
        self.__resist.resist_ohm(0)
        self.__ctrl_kl.ctrl_relay('KL12', True)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is False and in_a2 is True:
            pass
        else:
            self.__mysql_conn.mysql_ins_result(f'неисправен', f'{test_2_num}')
            self.__fault.debug_msg(f'подтест {subtest_2_num} не пройден', 1)
            if in_a1 is True:
                self.__mysql_conn.mysql_error(73)
            elif in_a2 is False:
                self.__mysql_conn.mysql_error(74)
            return False
        self.__fault.debug_msg(f'подтест {subtest_2_num} пройден', 3)
        return True

    def __subtest_63(self, subtest_3_num: float, test_3_num: int) -> bool:
        """
        6.3. Проверка удержания блока во включенном состоянии
        при подключении Rш пульта управления режима «Назад»:
        """
        self.__mysql_conn.mysql_ins_result(f'идёт тест {subtest_3_num}', f'{test_3_num}')
        self.__ctrl_kl.ctrl_relay('KL25', True)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is False and in_a2 is True:
            pass
        else:
            self.__mysql_conn.mysql_ins_result(f'неисправен', f'{test_3_num}')
            self.__fault.debug_msg(f'подтест {subtest_3_num} не пройден', 1)
            if in_a1 is True:
                self.__mysql_conn.mysql_error(75)
            elif in_a2 is False:
                self.__mysql_conn.mysql_error(76)
            return False
        self.__fault.debug_msg(f'подтест {subtest_3_num} пройден', 3)
        return True
    
    def __subtest_10(self) -> bool:
        """
        Тест 10. Блокировка включения блока при снижении сопротивления изоляции
        контролируемого присоединения до уровня предупредительной уставки
        """
        self.__resist.resist_kohm(200)
        self.__ctrl_kl.ctrl_relay('KL12', True)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is False and in_a2 is False:
            pass
        else:
            if in_a1 is True:
                self.__mysql_conn.mysql_error(85)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(86)
            return False
        self.__ctrl_kl.ctrl_relay('KL12', False)
        return True
    
    def __subtest_11(self) -> bool:
        """
        Тест 11. Блокировка включения блока при снижении сопротивления
        изоляции контролируемого присоединения до уровня аварийной уставки
        """
        self.__resist.resist_kohm(30)
        self.__ctrl_kl.ctrl_relay('KL12', True)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 is False and in_a2 is False:
            pass
        else:
            if in_a1 is True:
                self.__mysql_conn.mysql_error(87)
            elif in_a2 is True:
                self.__mysql_conn.mysql_error(88)
            return False
        self.__ctrl_kl.ctrl_relay('KL12', False)
        return True
    
    def __inputs_a(self):
        in_a1 = self.__read_mb.read_discrete(1)
        in_a2 = self.__read_mb.read_discrete(2)
        if in_a1 is None or in_a2 is None:
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_a1, in_a2

    def st_test_bru_2sr(self) -> bool:
        if self.st_test_10_bru_2sr():
            if self.st_test_20_bru_2sr():
                if self.st_test_21_bru_2sr():
                    if self.st_test_22_bru_2sr():
                        if self.st_test_30_bru_2sr():
                            if self.st_test_31_bru_2sr():
                                if self.st_test_40_bru_2sr():
                                    if self.st_test_41_bru_2sr():
                                        if self.st_test_50_bru_2sr():
                                            if self.st_test_51_bru_2sr():
                                                if self.st_test_60_bru_2sr():
                                                    if self.st_test_61_bru_2sr():
                                                        if self.st_test_62_bru_2sr():
                                                            if self.st_test_70_bru_2sr():
                                                                if self.st_test_71_bru_2sr():
                                                                    if self.st_test_80_bru_2sr():
                                                                        if self.st_test_81_bru_2sr():
                                                                            if self.st_test_90_bru_2sr():
                                                                                if self.st_test_91_bru_2sr():
                                                                                    if self.st_test_100_bru_2sr():
                                                                                        return True
        return False


if __name__ == '__main__':
    test_bru_2sr = TestBRU2SR()
    reset_test_bru_2sr = ResetRelay()
    mysql_conn_bru_2sr = MySQLConnect()
    fault = Bug(True)
    try:
        if test_bru_2sr.st_test_bru_2sr():
            mysql_conn_bru_2sr.mysql_block_good()
            my_msg('Блок исправен', 'green')
        else:
            mysql_conn_bru_2sr.mysql_block_bad()
            my_msg('Блок неисправен', 'red')
    except OSError:
        my_msg("ошибка системы", 'red')
    except SystemError:
        my_msg("внутренняя ошибка", 'red')
    except ModbusConnectException as mce:
        fault.debug_msg(mce, 'red')
        my_msg(f'{mce}', 'red')
    finally:
        reset_test_bru_2sr.reset_all()
        sys.exit()
