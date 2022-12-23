#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки
Тип блока Производитель
БКИ-6-3Ш

"""

import sys
import logging

from time import sleep

from gen_func_utils import *
from my_msgbox import *
from gen_mb_client import *
from gen_mysql_connect import *

__all__ = ["TestBKI6"]


class TestBKI6(object):

    def __init__(self):
        self.__resist = Resistor()
        self.__ctrl_kl = CtrlKL()
        self.__read_mb = ReadMB()
        self.__mysql_conn = MySQLConnect()
        self.__fault = Bug(True)
        self.msg_1 = 'Убедитесь в отсутствии других блоков или соединительных кабелей в панели разъемов А'
        self.msg_2 = 'Подключите в разъем, расположенный на панели разъемов А ' \
                     'соединительный кабель для проверки блока БКИ-6-3Ш'

        logging.basicConfig(filename="C:\Stend\project_class\TestBKI63Sh.log",
                            filemode="w",
                            level=logging.DEBUG,
                            encoding="utf-8",
                            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('WARNING')
        self.logger = logging.getLogger(__name__)

    def st_test_1_bki6(self) -> bool:
        """
        Тест 1. Проверка исходного состояния контактов блока при отсутствии напряжения питания
        """
        self.__inputs_a0()
        if my_msg(self.msg_1):
            if my_msg(self.msg_2):
                pass
            else:
                return False
        else:
            return False
        self.__ctrl_kl.ctrl_relay('KL22', True)
        sleep(3)
        in_a1, in_a4, in_a5, in_a6, in_a7 = self.__inputs_a()
        if in_a1 is False and in_a7 is True and in_a6 is True and in_a4 is False and in_a5 is True:
            pass
        else:
            self.__fault.debug_msg('тест 1 положение выходов не соответствует', 1)
            self.__mysql_conn.mysql_ins_result('неисправен', '1')
            if in_a1 is True or in_a7 is False:
                self.__mysql_conn.mysql_error(123)
            elif in_a6 is False:
                self.__mysql_conn.mysql_error(124)
            elif in_a4 is True and in_a5 is False:
                self.__mysql_conn.mysql_error(125)
            return False
        self.__fault.debug_msg('тест 1 положение выходов соответствует', 4)
        self.__mysql_conn.mysql_ins_result('исправен', '1')
        return True

    def st_test_20_bki6(self) -> bool:
        """
        Тест 2. Проверка работы контактов блока при подаче питания на блок и отсутствии утечки
        """
        self.__ctrl_kl.ctrl_relay('KL21', True)
        k1 = 0
        in_a1, in_a7 = self.__inputs_a1_a7()
        while in_a1 is False and in_a7 is True and k1 <= 20:
            sleep(0.2)
            in_a1, in_a7 = self.__inputs_a1_a7()
            k1 += 1
        if in_a1 is True and in_a7 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", "2")
            self.__fault.debug_msg('тест 2.0 положение выходов не соответствует', 1)
            return False
        k2 = 0
        in_a1, in_a7 = self.__inputs_a1_a7()
        while in_a1 is True and in_a7 is False and k2 <= 20:
            sleep(0.2)
            in_a1, in_a7 = self.__inputs_a1_a7()
            k1 += 1
        if in_a1 is False and in_a7 is True:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", "2")
            self.__fault.debug_msg('тест 2.0 положение выходов не соответствует', 1)
            return False
        self.__fault.debug_msg('тест 2.0 положение выходов соответствует', 4)
        return True

    def st_test_21_bki6(self) -> bool:
        """
        2.1. Проверка установившегося состояния контактов по истечению 20 сек
        """
        in_a1, in_a4, in_a5, in_a6, in_a7 = self.__inputs_a()
        if in_a1 is False and in_a7 is True and in_a6 is True and in_a4 is False and in_a5 is True:
            pass
        else:
            self.__fault.debug_msg('тест 2.1 положение выходов не соответствует', 1)
            self.__mysql_conn.mysql_ins_result('неисправен', '2')
            if in_a1 is True or in_a7 is False:
                self.__mysql_conn.mysql_error(126)
            elif in_a6 is False:
                self.__mysql_conn.mysql_error(127)
            elif in_a4 is True and in_a5 is False:
                self.__mysql_conn.mysql_error(128)
            return False
        self.__fault.debug_msg('тест 2.1 положение выходов соответствует', 4)
        self.__mysql_conn.mysql_ins_result('исправен', '2')
        return True

    def st_test_30_bki6(self) -> bool:
        """
        Тест 3. Проверка работы контактов реле К4 «Блокировка ВКЛ».
        """
        self.__ctrl_kl.ctrl_relay('KL36', True)
        sleep(1)
        in_a1, in_a4, in_a5, in_a6, in_a7 = self.__inputs_a()
        if in_a1 is False and in_a7 is True and in_a6 is True and in_a4 is False and in_a5 is True:
            pass
        else:
            self.__fault.debug_msg('тест 3.1 положение выходов не соответствует', 1)
            self.__mysql_conn.mysql_ins_result('неисправен', '3')
            if in_a1 is True or in_a7 is False:
                self.__mysql_conn.mysql_error(129)
            elif in_a6 is False:
                self.__mysql_conn.mysql_error(130)
            elif in_a4 is True and in_a5 is False:
                self.__mysql_conn.mysql_error(131)
            return False
        self.__fault.debug_msg('тест 3.1 положение выходов соответствует', 4)
        return True

    def st_test_31_bki6(self) -> bool:
        self.__ctrl_kl.ctrl_relay('KL36', False)
        k3 = 0
        in_a1, in_a7 = self.__inputs_a1_a7()
        while in_a1 is False and in_a7 is True and k3 <= 40:
            sleep(0.2)
            in_a1, in_a7 = self.__inputs_a1_a7()
            k3 += 1
        if in_a1 is True and in_a7 is False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", "3")
            self.__fault.debug_msg('тест 3.2 положение выходов не соответствует', 1)
            return False
        k4 = 0
        in_a1, in_a7 = self.__inputs_a1_a7()
        while in_a1 is True and in_a7 is False and k4 <= 40:
            sleep(0.2)
            in_a1, in_a7 = self.__inputs_a1_a7()
            k4 += 1
        if in_a1 is False and in_a7 is True:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", "3")
            self.__fault.debug_msg('тест 3.2 положение выходов не соответствует', 1)
            return False
        self.__fault.debug_msg('тест 3.2 положение выходов соответствует', 4)
        return True

    def st_test_32_bki6(self) -> bool:
        in_a1, in_a4, in_a5, in_a6, in_a7 = self.__inputs_a()
        if in_a1 is False and in_a7 is True and in_a6 is True and in_a4 is False and in_a5 is True:
            pass
        else:
            self.__fault.debug_msg('тест 3.3 положение выходов не соответствует', 1)
            self.__mysql_conn.mysql_ins_result('неисправен', '3')
            if in_a1 is True or in_a7 is False:
                self.__mysql_conn.mysql_error(132)
            elif in_a6 is False:
                self.__mysql_conn.mysql_error(133)
            elif in_a4 is True and in_a5 is False:
                self.__mysql_conn.mysql_error(134)
            return False
        self.__fault.debug_msg('тест 3.3 положение выходов соответствует', 4)
        self.__mysql_conn.mysql_ins_result('исправен', '3')
        return True

    def st_test_40_bki6(self) -> bool:
        """
        Тест 4. Проверка работы контактов реле К6 «Срабатывание БКИ»
        """
        self.__ctrl_kl.ctrl_relay('KL22', False)
        self.__resist.resist_kohm(30)
        sleep(10)
        in_a1, in_a4, in_a5, in_a6, in_a7 = self.__inputs_a()
        if in_a1 is False and in_a7 is True and in_a6 is False and in_a4 is True and in_a5 is False:
            pass
        else:
            self.__fault.debug_msg('тест 4.1 положение выходов не соответствует', 1)
            self.__mysql_conn.mysql_ins_result('неисправен', '4')
            if in_a1 is True or in_a7 is False:
                self.__mysql_conn.mysql_error(135)
            elif in_a6 is True:
                self.__mysql_conn.mysql_error(136)
            elif in_a4 is False and in_a5 is True:
                self.__mysql_conn.mysql_error(137)
            return False
        self.__fault.debug_msg('тест 4.1 положение выходов соответствует', 4)
        return True

    def st_test_41_bki6(self) -> bool:
        """
        4.2. Отключение 30 кОм
        """
        self.__resist.resist_kohm(590)
        sleep(2)
        in_a1, in_a4, in_a5, in_a6, in_a7 = self.__inputs_a()
        if in_a1 is False and in_a7 is True and in_a6 is False and in_a4 is False and in_a5 is True:
            pass
        else:
            self.__fault.debug_msg('тест 4.2 положение выходов не соответствует', 1)
            self.__mysql_conn.mysql_ins_result('неисправен', '4')
            if in_a1 is True or in_a7 is False:
                self.__mysql_conn.mysql_error(138)
            elif in_a6 is True:
                self.__mysql_conn.mysql_error(139)
            elif in_a4 is True and in_a5 is False:
                self.__mysql_conn.mysql_error(140)
            return False
        self.__fault.debug_msg('тест 4.2 положение выходов соответствует', 4)
        self.__mysql_conn.mysql_ins_result('исправен', '4')
        return True

    def st_test_50_bki6(self) -> bool:
        """
        Тест 5. Проверка исправности контактов реле К5 «Срабатывание БКИ на сигнал
        """
        self.__ctrl_kl.ctrl_relay('KL22', True)
        sleep(2)
        in_a1, in_a4, in_a5, in_a6, in_a7 = self.__inputs_a()
        if in_a1 is False and in_a7 is True and in_a6 is True and in_a4 is False and in_a5 is True:
            pass
        else:
            self.__fault.debug_msg('тест 5.1 положение выходов не соответствует', 1)
            self.__mysql_conn.mysql_ins_result('неисправен', '5')
            if in_a1 is True or in_a7 is False:
                self.__mysql_conn.mysql_error(141)
            elif in_a6 is False:
                self.__mysql_conn.mysql_error(142)
            elif in_a4 is True and in_a5 is False:
                self.__mysql_conn.mysql_error(143)
            return False
        self.__fault.debug_msg('тест 5.1 положение выходов соответствует', 4)
        return True

    def st_test_51_bki6(self) -> bool:
        self.__ctrl_kl.ctrl_relay('KL22', False)
        sleep(5)
        in_a1, in_a4, in_a5, in_a6, in_a7 = self.__inputs_a()
        if in_a1 is False and in_a7 is True and in_a6 is False and in_a4 is False and in_a5 is True:
            pass
        else:
            self.__fault.debug_msg('тест 5.2 положение выходов не соответствует', 1)
            self.__mysql_conn.mysql_ins_result('неисправен', '5')
            if in_a1 is True or in_a7 is False:
                self.__mysql_conn.mysql_error(144)
            elif in_a6 is True:
                self.__mysql_conn.mysql_error(145)
            elif in_a4 is True and in_a5 is False:
                self.__mysql_conn.mysql_error(146)
            return False
        self.__fault.debug_msg('тест 5.2 положение выходов соответствует', 4)
        self.__mysql_conn.mysql_ins_result('исправен', '5')
        return True

    def __inputs_a0(self):
        in_a0 = self.__read_mb.read_discrete(0)
        if in_a0 is None:
            # logging.error(f'нет связи с контроллером')
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_a0

    def __inputs_a(self):
        in_a1 = self.__read_mb.read_discrete(1)
        in_a4 = self.__read_mb.read_discrete(4)
        in_a5 = self.__read_mb.read_discrete(5)
        in_a6 = self.__read_mb.read_discrete(6)
        in_a7 = self.__read_mb.read_discrete(7)
        if in_a1 is None or in_a4 is None or in_a5 is None or in_a6 is None or in_a7 in None:
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_a1, in_a4, in_a5, in_a6, in_a7

    def __inputs_a1_a7(self):
        in_a1 = self.__read_mb.read_discrete(1)
        in_a7 = self.__read_mb.read_discrete(7)
        if in_a1 is None or in_a7 in None:
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_a1, in_a7

    def st_test_bki_6_3sh(self) -> bool:
        if self.st_test_1_bki6():
            if self.st_test_20_bki6():
                if self.st_test_21_bki6():
                    if self.st_test_30_bki6():
                        if self.st_test_31_bki6():
                            if self.st_test_32_bki6():
                                if self.st_test_40_bki6():
                                    if self.st_test_41_bki6():
                                        if self.st_test_50_bki6():
                                            if self.st_test_51_bki6():
                                                return True
        return False


if __name__ == '__main__':
    test_bki6 = TestBKI6()
    reset_test_bki6 = ResetRelay()
    mysql_conn_bki6 = MySQLConnect()
    fault = Bug(True)
    try:
        if test_bki6.st_test_bki_6_3sh():
            mysql_conn_bki6.mysql_block_good()
            my_msg('Блок исправен', 'green')
        else:
            mysql_conn_bki6.mysql_block_bad()
            my_msg('Блок неисправен', 'red')
    except OSError:
        my_msg("ошибка системы", 'red')
    except SystemError:
        my_msg("внутренняя ошибка", 'red')
    except ModbusConnectException as mce:
        fault.debug_msg(mce, 'red')
        my_msg(f'{mce}', 'red')
    finally:
        reset_test_bki6.reset_all()
        sys.exit()
