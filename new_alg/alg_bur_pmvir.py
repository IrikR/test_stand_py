# -*- coding: utf-8 -*-
"""
!!! НОВЫЙ НЕ ОБКАТАНЫЙ !!!

Алгоритм проверки

Тип блока: БУР ПМВИР (пускатель)
Производитель: Нет производителя

"""

__all__ = ["TestBURPMVIR"]

import logging
import sys
from time import sleep

from .general_func.database import *
from .general_func.exception import *
from .general_func.opc_full import ConnectOPC
from .general_func.reset import ResetRelay
from .general_func.resistance import Resistor
from .general_func.subtest import Subtest2in
from .general_func.utils import CLILog
from .gui.msgbox_1 import *


class TestBURPMVIR:

    def __init__(self):
        self.conn_opc = ConnectOPC()
        self.resist = Resistor()
        self.mysql_conn = MySQLConnect()
        self.subtest = Subtest2in()
        self.reset_relay = ResetRelay()
        self.cli_log = CLILog("debug", __name__)

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
        self.cli_log.lev_info(f"старт теста {__doc__}", "skyblue")
        if self.conn_opc.subtest_read_di(test_num=1, subtest_num=1.0,
                                         err_code=[166, 167],
                                         position_inp=[False, False],
                                         di_xx=['inp_01', 'inp_02']):
            return True
        return False

    def st_test_20(self) -> bool:
        """
        Тест 2. Проверка включения/выключения блока от кнопки «Пуск/Стоп» в режиме «Вперёд».
        2.4. Выключение блока от кнопки «Стоп» режима «Вперёд»
        """
        self.conn_opc.ctrl_relay('KL21', True)
        self.logger.debug("включен KL21")
        if self.conn_opc.subtest_read_di(test_num=2, subtest_num=2.0,
                                         err_code=[168, 169],
                                         position_inp=[False, False],
                                         di_xx=['inp_01', 'inp_02']):
            if self.subtest.subtest_a_bur(test_num=2, subtest_num=2.1, forward=True):
                if self.subtest.subtest_b_bur(test_num=2, subtest_num=2.2, forward=True):
                    self.conn_opc.ctrl_relay('KL12', False)
                    self.logger.debug("отключены KL12")
                    sleep(1)
                    self.logger.debug("таймаут 1 сек")
                    self.cli_log.lev_debug("таймаут 1 сек", "gray")
                    if self.conn_opc.subtest_read_di(test_num=2, subtest_num=2.3,
                                                     err_code=[174, 175],
                                                     position_inp=[False, False],
                                                     di_xx=['inp_01', 'inp_02']):
                        self.conn_opc.ctrl_relay('KL25', False)
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
                self.logger.debug("таймаут 1 сек")
                self.cli_log.lev_debug("таймаут 1 сек", "gray")
                if self.conn_opc.subtest_read_di(test_num=3, subtest_num=3.2,
                                                 err_code=[176, 177],
                                                 position_inp=[False, False],
                                                 di_xx=['inp_01', 'inp_02']):
                    self.conn_opc.ctrl_relay('KL12', False)
                    self.conn_opc.ctrl_relay('KL25', False)
                    self.logger.debug("отключены KL12, KL25")
                    return True
        return False

    def st_test_40(self) -> bool:
        """
        4. Защита от потери управляемости канала «Вперёд» при замыкании проводов ДУ
        """
        if self.subtest.subtest_a_bur(test_num=4, subtest_num=4.0, forward=True):
            if self.subtest.subtest_b_bur(test_num=4, subtest_num=4.1, forward=True):
                self.conn_opc.ctrl_relay('KL11', True)
                self.logger.debug("включен KL11")
                sleep(2)
                self.logger.debug("таймаут 2 сек")
                self.cli_log.lev_debug("таймаут 2 сек", "gray")
                if self.conn_opc.subtest_read_di(test_num=4, subtest_num=4.2,
                                                 err_code=[178, 179],
                                                 position_inp=[False, False],
                                                 di_xx=['inp_01', 'inp_02']):
                    self.conn_opc.ctrl_relay('KL12', False)
                    self.conn_opc.ctrl_relay('KL25', False)
                    self.conn_opc.ctrl_relay('KL11', False)
                    self.logger.debug("отключены KL12, KL25, KL11")
                    return True
        return False

    def st_test_50(self) -> bool:
        """
        Тест 5. Защита от потери управляемости канала «Вперёд» при обрыве проводов ДУ
        """
        if self.subtest.subtest_a_bur(test_num=5, subtest_num=5.0, forward=True):
            if self.subtest.subtest_b_bur(test_num=5, subtest_num=5.1, forward=True):
                self.conn_opc.ctrl_relay('KL12', False)
                self.logger.debug("отключен KL12")
                sleep(2)
                self.logger.debug("таймаут 2 сек")
                self.cli_log.lev_debug("таймаут 2 сек", "gray")
                if self.conn_opc.subtest_read_di(test_num=5, subtest_num=5.2,
                                                 err_code=[180, 181],
                                                 position_inp=[False, False],
                                                 di_xx=['inp_01', 'inp_02']):
                    self.conn_opc.ctrl_relay('KL25', False)
                    self.logger.debug("отключен KL25")
                    return True
        return False

    def st_test_60(self) -> bool:
        """
        Тест 6. Проверка включения/выключения блока от кнопки «Пуск/Стоп» в режиме «Назад».
        Переключение в режим ДУ «Назад»	KL26 - ВКЛ
        """
        self.conn_opc.ctrl_relay('KL26', True)
        self.logger.debug("включен KL26")
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=6, subtest_num=6.0,
                                         err_code=[168, 169],
                                         position_inp=[False, False],
                                         di_xx=['inp_01', 'inp_02']):
            if self.subtest.subtest_a_bur(test_num=6, subtest_num=6.1, back=True):
                if self.subtest.subtest_b_bur(test_num=6, subtest_num=6.2, back=True):
                    # 6.4. Выключение блока от кнопки «Стоп» режима «Назад»
                    self.conn_opc.ctrl_relay('KL12', False)
                    self.logger.debug("отключен KL12")
                    sleep(2)
                    self.logger.debug("таймаут 2 сек")
                    self.cli_log.lev_debug("таймаут 2 сек", "gray")
                    if self.conn_opc.subtest_read_di(test_num=6, subtest_num=6.3,
                                                     err_code=[186, 187],
                                                     position_inp=[False, False],
                                                     di_xx=['inp_01', 'inp_02']):
                        self.conn_opc.ctrl_relay('KL25', False)
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
                self.logger.debug("таймаут 2 сек")
                self.cli_log.lev_debug("таймаут 2 сек", "gray")
                if self.conn_opc.subtest_read_di(test_num=7, subtest_num=7.2,
                                                 err_code=[188, 189],
                                                 position_inp=[False, False],
                                                 di_xx=['inp_01', 'inp_02']):
                    self.conn_opc.ctrl_relay('KL12', False)
                    self.conn_opc.ctrl_relay('KL25', False)
                    self.logger.debug("отключены KL12, KL25")
                    return True
        return False

    def st_test_80(self) -> bool:
        """
        8. Защита от потери управляемости канала «Назад» при замыкании проводов ДУ
        """
        if self.subtest.subtest_a_bur(test_num=8, subtest_num=8.0, back=True):
            if self.subtest.subtest_b_bur(test_num=8, subtest_num=8.1, back=True):
                self.conn_opc.ctrl_relay('KL11', True)
                self.logger.debug("включен KL11")
                sleep(2)
                self.logger.debug("таймаут 2 сек")
                self.cli_log.lev_debug("таймаут 2 сек", "gray")
                if self.conn_opc.subtest_read_di(test_num=8, subtest_num=8.2,
                                                 err_code=[190, 191],
                                                 position_inp=[False, False],
                                                 di_xx=['inp_01', 'inp_02']):
                    self.conn_opc.ctrl_relay('KL12', False)
                    self.conn_opc.ctrl_relay('KL25', False)
                    self.conn_opc.ctrl_relay('KL11', False)
                    self.logger.debug("отключены KL12, KL22, KL11")
                    return True
        return False

    def st_test_90(self) -> bool:
        """
        Тест 9. Защита от потери управляемости канала «Назад» при обрыве проводов ДУ
        """
        if self.subtest.subtest_a_bur(test_num=9, subtest_num=9.0, back=True):
            if self.subtest.subtest_b_bur(test_num=9, subtest_num=9.1, back=True):
                self.conn_opc.ctrl_relay('KL12', False)
                self.logger.debug("отключен KL12")
                sleep(2)
                self.logger.debug("таймаут 2 сек")
                self.cli_log.lev_debug("таймаут 2 сек", "gray")
                if self.conn_opc.subtest_read_di(test_num=9, subtest_num=9.2,
                                                 err_code=[192, 193],
                                                 position_inp=[False, False],
                                                 di_xx=['inp_01', 'inp_02']):
                    self.conn_opc.ctrl_relay('KL25', False)
                    self.logger.debug("отключен KL25")
                    return True
        return False

    def st_test_100(self) -> bool:
        """
        Тест 10. Блокировка включения блока при снижении сопротивления изоляции контролируемого присоединения
        """
        self.resist.resist_kohm(30)
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        self.conn_opc.ctrl_relay('KL12', True)
        self.logger.debug("включен KL12")
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=10, subtest_num=10.0,
                                         err_code=[194, 195],
                                         position_inp=[False, False],
                                         di_xx=['inp_01', 'inp_02']):
            self.conn_opc.ctrl_relay('KL12', False)
            self.logger.debug("отключен KL12")
            return True
        return False

    def st_test_101(self) -> bool:
        """
        Тест 11. Проверка работы режима «Проверка БРУ»
        """
        self.conn_opc.ctrl_relay('KL22', True)
        self.conn_opc.ctrl_relay('KL12', True)
        self.logger.debug("отключены KL12, KL22")
        sleep(2)
        self.logger.debug("таймаут 2 сек")
        self.cli_log.lev_debug("таймаут 2 сек", "gray")
        if self.conn_opc.subtest_read_di(test_num=10, subtest_num=10.1,
                                         err_code=[196, 197],
                                         position_inp=[False, False],
                                         di_xx=['inp_01', 'inp_02']):
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

    def full_test_bur_pmvir(self) -> None:
        try:
            if self.st_test_bur_pmvir():
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
    test_bur_pmvir = TestBURPMVIR()
    test_bur_pmvir.full_test_bur_pmvir()
    # reset_test_bur_pmvir = ResetRelay()
    # mysql_conn_bur_pmvir = MySQLConnect()
    # try:
    #     if test_bur_pmvir.st_test_bur_pmvir():
    #         mysql_conn_bur_pmvir.mysql_block_good()
    #         my_msg('Блок исправен', 'green')
    #     else:
    #         mysql_conn_bur_pmvir.mysql_block_bad()
    #         my_msg('Блок неисправен', 'red')
    # except OSError:
    #     my_msg("ошибка системы", 'red')
    # except SystemError:
    #     my_msg("внутренняя ошибка", 'red')
    # except ModbusConnectException as mce:
    #     my_msg(f'{mce}', 'red')
    # finally:
    #     reset_test_bur_pmvir.reset_all()
    #     sys.exit()
