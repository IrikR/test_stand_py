# -*- coding: utf-8 -*-
"""
!!! НОВЫЙ НЕ ОБКАТАНЫЙ !!!

Алгоритм проверки

Тип блока: БКИ-6-3Ш
Производитель:

"""

__all__ = ["TestBKI6"]

import logging
import sys
from time import sleep

from .general_func.database import *
from .general_func.exception import *
from .general_func.opc_full import ConnectOPC
from .general_func.reset import ResetRelay
from .general_func.resistance import Resistor
from .general_func.utils import CLILog
from .gui.msgbox_1 import *


class TestBKI6:

    def __init__(self):
        self.conn_opc = ConnectOPC()
        self.resist = Resistor()
        self.mysql_conn = MySQLConnect()
        self.reset_relay = ResetRelay()
        self.cli_log = CLILog("debug", __name__)

        self.msg_1 = 'Убедитесь в отсутствии других блоков или соединительных кабелей в панели разъемов А'
        self.msg_2 = 'Подключите в разъем, расположенный на панели разъемов А ' \
                     'соединительный кабель для проверки блока БКИ-6-3Ш'

        logging.basicConfig(
            filename="C:\\Stend\\project_class\\log\\TestBKI63Sh.log",
            filemode="w",
            level=logging.DEBUG,
            encoding="utf-8",
            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('WARNING')
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))

    def st_test_1(self) -> bool:
        """
        Тест 1. Проверка исходного состояния контактов блока при отсутствии напряжения питания
        """
        self.cli_log.lev_info(f"старт теста {__doc__}", "skyblue")
        if my_msg(self.msg_1):
            if my_msg(self.msg_2):
                pass
            else:
                return False
        else:
            return False
        self.conn_opc.ctrl_relay('KL22', True)
        sleep(3)
        if self.conn_opc.subtest_read_di(test_num=1, subtest_num=1.0,
                                         err_code=[123, 123, 124, 125, 125],
                                         position_inp=[False, True, True, False, True],
                                         di_xx=['inp_01', 'inp_07', 'inp_06', 'inp_04', 'inp_05']):
            return True
        return False

    def st_test_20(self) -> bool:
        """
        Тест 2. Проверка работы контактов блока при подаче питания на блок и отсутствии утечки
        """
        self.conn_opc.ctrl_relay('KL21', True)
        if self.sub_test(test_num=2, subtest_num=2.0, iteration=20):
            return True
        return False

    def st_test_21(self) -> bool:
        """
        2.1. Проверка установившегося состояния контактов по истечению 20 сек
        """
        if self.conn_opc.subtest_read_di(test_num=2, subtest_num=2.1,
                                         err_code=[126, 126, 127, 128, 128],
                                         position_inp=[False, True, True, False, True],
                                         di_xx=['inp_01', 'inp_07', 'inp_06', 'inp_04', 'inp_05']):
            return True
        return False

    def st_test_30(self) -> bool:
        """
        Тест 3. Проверка работы контактов реле К4 «Блокировка ВКЛ».
        """
        self.conn_opc.ctrl_relay('KL36', True)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=3, subtest_num=3.0,
                                         err_code=[129, 129, 130, 131, 131],
                                         position_inp=[False, True, True, False, True],
                                         di_xx=['inp_01', 'inp_07', 'inp_06', 'inp_04', 'inp_05']):
            return True
        return False

    def st_test_31(self) -> bool:
        self.conn_opc.ctrl_relay('KL36', False)
        if self.sub_test(test_num=3, subtest_num=3.1, iteration=40):
            return True
        return False

    def st_test_32(self) -> bool:
        """

        :return: bool
        """
        if self.conn_opc.subtest_read_di(test_num=3, subtest_num=3.2,
                                         err_code=[132, 132, 133, 134, 134],
                                         position_inp=[False, True, True, False, True],
                                         di_xx=['inp_01', 'inp_07', 'inp_06', 'inp_04', 'inp_05']):
            return True
        return False

    def st_test_40(self) -> bool:
        """
        Тест 4. Проверка работы контактов реле К6 «Срабатывание БКИ»
        """
        self.conn_opc.ctrl_relay('KL22', False)
        self.resist.resist_kohm(30)
        sleep(10)
        self.logger.debug("таймаут 10 сек")
        self.cli_log.lev_debug("таймаут 10 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=4, subtest_num=4.0,
                                         err_code=[135, 135, 136, 137, 137],
                                         position_inp=[False, True, False, True, False],
                                         di_xx=['inp_01', 'inp_07', 'inp_06', 'inp_04', 'inp_05']):
            return True
        return False

    def st_test_41(self) -> bool:
        """
        4.2. Отключение 30 кОм
        """
        self.resist.resist_kohm(590)
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=4, subtest_num=4.1,
                                         err_code=[138, 138, 139, 140, 140],
                                         position_inp=[False, True, False, False, True],
                                         di_xx=['inp_01', 'inp_07', 'inp_06', 'inp_04', 'inp_05']):
            return True
        return False

    def st_test_50(self) -> bool:
        """
        Тест 5. Проверка исправности контактов реле К5 «Срабатывание БКИ на сигнал
        """
        self.conn_opc.ctrl_relay('KL22', True)
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=5, subtest_num=5.0,
                                         err_code=[141, 141, 142, 143, 143],
                                         position_inp=[False, True, True, False, True],
                                         di_xx=['inp_01', 'inp_07', 'inp_06', 'inp_04', 'inp_05']):
            return True
        return False

    def st_test_51(self) -> bool:
        self.conn_opc.ctrl_relay('KL22', False)
        sleep(5)
        self.logger.debug("таймаут 5 сек")
        self.cli_log.lev_debug("таймаут 5 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=5, subtest_num=5.1,
                                         err_code=[144, 144, 145, 146, 146],
                                         position_inp=[False, True, False, False, True],
                                         di_xx=['inp_01', 'inp_07', 'inp_06', 'inp_04', 'inp_05']):
            return True
        return False

    def sub_test(self, *, test_num: int, subtest_num: float, iteration) -> bool:
        """
        Для теста 2.0 iteration = 20.
        Для теста 3.1 iteration = 40.
        :param test_num:
        :param subtest_num:
        :param iteration:
        :return:
        """
        self.logger.debug(f"тест {test_num}, подтест {subtest_num}")
        self.mysql_conn.mysql_ins_result(f"идёт подтест {subtest_num}", f"{test_num}")
        k1 = 0
        inp_01, inp_07 = self.conn_opc.simplified_read_di(['inp_01', 'inp_07'])
        self.logger.debug(f"положение выходов блока: {inp_01 = } is True, {inp_07 = } is False")
        while inp_01 is False and inp_07 is True and k1 <= iteration:
            sleep(0.2)
            inp_01, inp_07 = self.conn_opc.simplified_read_di(['inp_01', 'inp_07'])
            self.logger.debug(f"итерация {k1} положение выходов блока: {inp_01 = } is True, {inp_07 = } is False")
            k1 += 1
        if inp_01 is True and inp_07 is False:
            self.logger.debug(f'подтест {subtest_num} положение выходов соответствует')
            self.mysql_conn.mysql_add_message(f'подтест {subtest_num} положение выходов соответствует')
        else:
            self.mysql_conn.mysql_ins_result("неисправен", f"{test_num}")
            self.logger.debug(f'подтест {subtest_num} положение выходов не соответствует')
            self.mysql_conn.mysql_add_message(f'подтест {subtest_num} положение выходов не соответствует')
            return False

        k2 = 0
        inp_01, inp_07 = self.conn_opc.simplified_read_di(['inp_01', 'inp_07'])
        while inp_01 is True and inp_07 is False and k2 <= iteration:
            sleep(0.2)
            inp_01, inp_07 = self.conn_opc.simplified_read_di(['inp_01', 'inp_07'])
            self.logger.debug(f"итерация {k2} положение выходов блока: {inp_01 = } is False, {inp_07 = } is True")
            k2 += 1
        if inp_01 is False and inp_07 is True:
            self.logger.debug(f'подтест {subtest_num} положение выходов соответствует')
            self.mysql_conn.mysql_add_message(f'подтест {subtest_num} положение выходов соответствует')
            return True
        else:
            self.mysql_conn.mysql_ins_result("неисправен", f"{test_num}")
            self.logger.debug(f'подтест {subtest_num} положение выходов не соответствует')
            self.mysql_conn.mysql_add_message(f'подтест {subtest_num} положение выходов не соответствует')
            return False

    def st_test_bki_6_3sh(self) -> bool:
        if self.st_test_1():
            if self.st_test_20():
                if self.st_test_21():
                    if self.st_test_30():
                        if self.st_test_31():
                            if self.st_test_32():
                                if self.st_test_40():
                                    if self.st_test_41():
                                        if self.st_test_50():
                                            if self.st_test_51():
                                                return True
        return False

    def full_test_bki_6_3sh(self) -> None:
        try:
            if self.st_test_bki_6_3sh():
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
    test_bki6 = TestBKI6()
    test_bki6.full_test_bki_6_3sh()
    # reset_test_bki6 = ResetRelay()
    # mysql_conn_bki6 = MySQLConnect()
    # try:
    #     if test_bki6.st_test_bki_6_3sh():
    #         mysql_conn_bki6.mysql_block_good()
    #         my_msg('Блок исправен', 'green')
    #     else:
    #         mysql_conn_bki6.mysql_block_bad()
    #         my_msg('Блок неисправен', 'red')
    # except OSError:
    #     my_msg("ошибка системы", 'red')
    # except SystemError:
    #     my_msg("внутренняя ошибка", 'red')
    # except ModbusConnectException as mce:
    #     my_msg(f'{mce}', 'red')
    # finally:
    #     reset_test_bki6.reset_all()
    #     sys.exit()
