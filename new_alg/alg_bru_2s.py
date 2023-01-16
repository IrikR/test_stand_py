# -*- coding: utf-8 -*-
"""
!!! НОВЫЙ НЕ ОБКАТАНЫЙ !!!

Алгоритм проверки

Тип блока: БРУ-2С
Производитель: Нет производителя

"""

__all__ = ["TestBRU2S"]

import logging
import sys

from .general_func.database import *
from .general_func.exception import *
from .general_func.opc_full import ConnectOPC
from .general_func.reset import ResetRelay
from .general_func.resistance import Resistor
from .general_func.subtest import SubtestBDU
from .general_func.utils import CLILog
from .gui.msgbox_1 import *


class TestBRU2S:

    def __init__(self):
        self.conn_opc = ConnectOPC()
        self.resist = Resistor()
        self.mysql_conn = MySQLConnect()
        self.sub_test = SubtestBDU()
        self.reset_relay = ResetRelay()
        self.cli_log = CLILog("debug", __name__)

        self.msg_1 = "Переведите тумблер «П/А» на блоке в положение «П» и нажмите кнопку «ОК» " \
                     "Если на блоке нет тумблера «П/А» нажмите кнопку «Отмена»"

        logging.basicConfig(
            filename="C:\\Stend\\project_class\\log\\TestBRU2S.log",
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
        :return: bool:
        """
        self.cli_log.lev_info(f"старт теста {__doc__}", "skyblue")
        if self.conn_opc.subtest_read_di(test_num=1, subtest_num=1.0,
                                         err_code=[47],
                                         position_inp=[False],
                                         di_xx=['inp_01']):
            return True
        return False

    def st_test_20(self) -> bool:
        """
        Тест 2. Проверка включения/выключения блока от кнопки «Пуск/Стоп»
        :return: bool:
        """
        self.logger.debug(f"старт теста: 2, подтест: 0")
        self.conn_opc.ctrl_relay('KL21', True)
        self.logger.debug(f'включение KL21')
        if self.conn_opc.subtest_read_di(test_num=2, subtest_num=2.0,
                                         err_code=[48],
                                         position_inp=[False],
                                         di_xx=['inp_01']):
            return True
        return False

    def st_test_21(self) -> bool:
        """
        2.2. Включение блока от кнопки «Пуск»
        2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        :return: bool:
        """
        if self.sub_test.subtest_a_bdu43_bru2s(test_num=2, subtest_num=2.1):
            if self.sub_test.subtest_b_bru2s(test_num=2, subtest_num=2.2):
                return True
        return False

    def st_test_23(self) -> bool:
        """
        2.4. Выключение блока от кнопки «Стоп»
        :return: bool:
        """
        self.mysql_conn.mysql_add_message(f"старт теста: 2, подтест: 3")
        self.logger.debug(f"старт теста: 1, подтест: 0")
        self.conn_opc.ctrl_relay('KL12', False)
        self.logger.debug(f'отключение KL12')
        if self.conn_opc.subtest_read_di(test_num=2, subtest_num=2.3,
                                         err_code=[51],
                                         position_inp=[False],
                                         di_xx=['inp_01']):
            self.conn_opc.ctrl_relay('KL25', False)
            self.logger.debug(f'отключение KL25')
            return True
        return False

    def st_test_30(self) -> bool:
        """
        Повторяем подтесты 2.2. Включение блока от кнопки «Пуск»
        Повторяем подтесты 2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        :return: bool:
        """
        if self.sub_test.subtest_a_bdu43_bru2s(test_num=3, subtest_num=3.0):
            if self.sub_test.subtest_b_bru2s(test_num=3, subtest_num=3.1):
                return True
        return False

    def st_test_32(self) -> bool:
        """
        3. Отключение выходного контакта блока при увеличении сопротивления цепи заземления
        :return: bool:
        """
        self.logger.debug(f"старт теста: 3, подтест: 2")
        self.resist.resist_ohm(150)
        if self.conn_opc.subtest_read_di(test_num=3, subtest_num=3.2,
                                         err_code=[52],
                                         position_inp=[False],
                                         di_xx=['inp_01']):
            self.conn_opc.ctrl_relay('KL12', False)
            self.conn_opc.ctrl_relay('KL25', False)
            self.logger.debug(f'отключение KL12, KL25')
            return True
        return False

    def st_test_40(self) -> bool:
        """
        Повторяем подтесты 2.2. Включение блока от кнопки «Пуск»
        Повторяем подтесты 2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        :return: bool:
        """
        if self.sub_test.subtest_a_bdu43_bru2s(test_num=4, subtest_num=4.0):
            if self.sub_test.subtest_b_bru2s(test_num=4, subtest_num=4.1):
                return True
        return False

    def st_test_42(self) -> bool:
        """
        4. Защита от потери управляемости при замыкании проводов ДУ
        :return: bool:
        """
        self.logger.debug(f"старт теста: 4, подтест: 2")
        self.conn_opc.ctrl_relay('KL11', True)
        self.logger.debug(f'отключение KL11')
        if self.conn_opc.subtest_read_di(test_num=4, subtest_num=4.2,
                                         err_code=[53],
                                         position_inp=[False],
                                         di_xx=['inp_01']):
            self.conn_opc.ctrl_relay('KL12', False)
            self.conn_opc.ctrl_relay('KL25', False)
            self.conn_opc.ctrl_relay('KL11', False)
            self.logger.debug(f'отключение KL12, KL25, KL11')
            return True
        return False

    def st_test_50(self) -> bool:
        """
        Повторяем подтесты 2.2. Включение блока от кнопки «Пуск»
        Повторяем подтесты 2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        :return: bool:
        """
        if self.sub_test.subtest_a_bdu43_bru2s(test_num=5, subtest_num=5.0):
            if self.sub_test.subtest_b_bru2s(test_num=5, subtest_num=5.1):
                return True
        return False

    def st_test_52(self) -> bool:
        """
        Тест 5. Защита от потери управляемости блока при обрыве проводов ДУ
        :return: bool:
        """
        self.logger.debug(f"старт теста: 5, подтест: 2")
        self.conn_opc.ctrl_relay('KL12', False)
        self.logger.debug(f'отключение KL12')
        if self.conn_opc.subtest_read_di(test_num=5, subtest_num=5.2,
                                         err_code=[54],
                                         position_inp=[False],
                                         di_xx=['inp_01']):
            self.conn_opc.ctrl_relay('KL25', False)
            self.logger.debug(f'отключение KL25'
                              f'')
            return True
        return False

    def st_test_60(self) -> bool:
        """
        Тест 6.0
        :return: Bool
        """
        self.logger.debug(f"старт теста: 6, подтест: 0")
        if my_msg(self.msg_1):
            if self.subtest_6():
                self.mysql_conn.mysql_ins_result('исправен', '6')
                if self.subtest_7():
                    self.mysql_conn.mysql_ins_result('исправен', '7')
                else:
                    self.mysql_conn.mysql_ins_result('неисправен', '7')
                    return False
            else:
                self.mysql_conn.mysql_ins_result('неисправен', '6')
                return False
        else:
            if self.subtest_7():
                self.mysql_conn.mysql_ins_result('пропущен', '6')
                self.mysql_conn.mysql_ins_result('исправен', '7')
            else:
                self.mysql_conn.mysql_ins_result('пропущен', '6')
                self.mysql_conn.mysql_ins_result('неисправен', '7')
                return False
        return True

    def subtest_6(self) -> bool:
        """
        Тест 6. Блокировка включения блока при снижении сопротивления изоляции
        контролируемого присоединения до уровня предупредительной уставки.
        :return: Bool
        """
        self.logger.debug(f"старт теста: 6, подтест: 1")
        self.resist.resist_kohm(200)
        self.conn_opc.ctrl_relay('KL12', True)
        self.logger.debug(f'включение KL12')
        if self.conn_opc.subtest_read_di(test_num=6, subtest_num=6.0,
                                         err_code=[55],
                                         position_inp=[False],
                                         di_xx=['inp_01']):
            self.conn_opc.ctrl_relay('KL12', False)
            self.logger.debug(f'отключение KL12')
            return True
        return False

    def subtest_7(self) -> bool:
        """
        Тест 7. Блокировка включения блока при снижении сопротивления изоляции
        контролируемого присоединения до уровня аварийной уставки
        :return: bool
        """
        self.logger.debug(f"старт теста: 7, подтест: 0")
        self.resist.resist_kohm(30)
        self.conn_opc.ctrl_relay('KL12', True)
        self.logger.debug(f'включение KL12')
        if self.conn_opc.subtest_read_di(test_num=7, subtest_num=7.0,
                                         err_code=[56],
                                         position_inp=[False],
                                         di_xx=['inp_01']):
            self.conn_opc.ctrl_relay('KL12', False)
            self.logger.debug(f'отключение KL12')
            return True
        return False

    def st_test_bru_2s(self) -> bool:
        if self.st_test_10():
            if self.st_test_20():
                if self.st_test_21():
                    if self.st_test_23():
                        if self.st_test_30():
                            if self.st_test_32():
                                if self.st_test_40():
                                    if self.st_test_42():
                                        if self.st_test_50():
                                            if self.st_test_52():
                                                if self.st_test_60():
                                                    return True
        return False

    def full_test_bru_2s(self) -> None:
        try:
            if self.st_test_bru_2s():
                self.mysql_conn.mysql_block_good()
                self.logger.debug('Блок исправен')
                self.cli_log.lev_info('Блок исправен', 'green')
                my_msg('Блок исправен', 'green')
            else:
                self.mysql_conn.mysql_block_bad()
                self.logger.debug('Блок неисправен')
                self.cli_log.lev_warning('Блок неисправен', 'red')
                my_msg('Блок неисправен', 'red')
        except OSError:
            self.logger.debug("ошибка системы")
            self.cli_log.lev_warning("ошибка системы", 'red')
            my_msg("ошибка системы", 'red')
        except SystemError:
            self.logger.debug("внутренняя ошибка")
            self.cli_log.lev_warning("внутренняя ошибка", 'red')
            my_msg("внутренняя ошибка", 'red')
        except ModbusConnectException as mce:
            self.logger.debug(f'{mce}')
            self.cli_log.lev_warning(f'{mce}', 'red')
            my_msg(f'{mce}', 'red')
        finally:
            self.conn_opc.full_relay_off()
            self.conn_opc.opc_close()
            sys.exit()


if __name__ == '__main__':
    test_bru_2s = TestBRU2S()
    test_bru_2s.full_test_bru_2s()
    # reset_test_bru_2s = ResetRelay()
    # mysql_conn_bru_2s = MySQLConnect()
    # try:
    #     if test_bru_2s.st_test_bru_2s():
    #         mysql_conn_bru_2s.mysql_block_good()
    #         my_msg('Блок исправен', 'green')
    #     else:
    #         mysql_conn_bru_2s.mysql_block_bad()
    #         my_msg('Блок неисправен', 'red')
    # except OSError:
    #     my_msg("ошибка системы", 'red')
    # except SystemError:
    #     my_msg("внутренняя ошибка", 'red')
    # except ModbusConnectException as mce:
    #     my_msg(f'{mce}', 'red')
    # finally:
    #     reset_test_bru_2s.reset_all()
    #     sys.exit()
