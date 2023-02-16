# -*- coding: utf-8 -*-
"""
!!! НОВЫЙ НЕ ОБКАТАНЫЙ !!!

Алгоритм проверки

Тип блока: МКЗП-6-4Ш
Производитель: ЗМТ «Энергия»

"""

__all__ = ["TestMKZP6"]

import logging
import sys
from time import sleep, time

from .general_func.database import *
from .general_func.exception import *
from .general_func.opc_full import ConnectOPC
from .general_func.procedure import *
from .general_func.reset import ResetRelay
from .general_func.utils import CLILog
from .gui.msgbox_1 import *


class TestMKZP6:

    def __init__(self):
        self.conn_opc = ConnectOPC()
        self.reset = ResetRelay()
        self.proc = Procedure()
        self.mysql_conn = MySQLConnect()
        self.cli_log = CLILog("debug", __name__)

        self.ust_1: float = 45.1
        self.ust_2: float = 15.0
        self.coef_volt: float = 0.0
        self.test_num: int = 0
        self.health_flag: bool = False

        self.msg_1: str = "Убедитесь в отсутствии других блоков или соединительных кабелей в панели разъемов D " \
                          "Подключите в разъемы X33, X34, расположенные на панели разъемов D соединительные кабеля " \
                          "для проверки блока МКЗП-6-4Ш"
        self.msg_2: str = "Нажмите несколько раз кнопку «SB5», расположенную на панели D до появления окна со временем"
        self.msg_3: str = "Если на дисплее блока горят надписи «ОТКЛ» и «ПИТАНИЕ» нажмите кнопку «ОК». " \
                          "Иначе, нажмите кнопку  «ОТМЕНА»"
        self.msg_4: str = "Блок не переходит в исходное состояние"
        self.msg_5: str = "Если на дисплее загорелась надпись «ВКЛ» и погасла надпись «ОТКЛ» нажмите кнопку «ОК». " \
                          "Иначе нажмите кнопку «ОТМЕНА»"
        self.msg_6: str = "Блок не исправен. Блок не включается от кнопки «ПУСК»"
        self.msg_7: str = "Если на дисплее погасла надпись «ВКЛ» и загорелась надпись «ОТКЛ» нажмите кнопку «ОК». " \
                          "Иначе нажмите кнопку «ОТМЕНА»"
        self.msg_8: str = "Блок не исправен. Блок не выключается от кнопки «СТОП»"
        self.msg_9: str = "Если на дисплее загорелась надпись «ВКЛ» и погасла надпись «ОТКЛ» нажмите кнопку «ОК». " \
                          "Иначе нажмите кнопку «ОТМЕНА»"
        self.msg_11: str = "Если на дисплее стали активны надписи АВАРИЯ, ВКЛ и на дисплее появилась надпись " \
                           "«НЕИСПРАВНОСТЬ БКИ» нажмите кнопку «ОК». Иначе нажмите кнопку «ОТМЕНА»"
        self.msg_12: str = "Тест 2 не пройден. Блок не исправен. Блок не контролирует неисправность «БКИ»"
        self.msg_13: str = "Нажмите кнопку «SB5» (Сброс), расположенную на панели D"
        self.msg_14: str = "Если на дисплее стали активны надписи АВАРИЯ, УТЕЧКА, ВКЛ и на дисплее появилась надпись " \
                           "«Сработала защита УТЕЧКА» нажмите кнопку «ОК». Иначе нажмите кнопку «ОТМЕНА»"
        self.msg_15: str = "Тест 2 не пройден. Блок не исправен. Блок не контролирует «Аварию БКИ»"
        self.msg_16: str = "Если на дисплее стали активны надписи ПИТАНИЕ, ОТКЛ и на дисплее появилась надпись " \
                           "«Сработала защита ЗМН» нажмите кнопку «ОК». Иначе нажмите кнопку «ОТМЕНА»"
        self.msg_17: str = "Тест 3 не пройден. Блок не исправен. Не работает ЗМН»"
        self.msg_18: str = "Если на дисплее стали активны надписи ПИТАНИЕ, ОТКЛ нажмите кнопку «ОК». " \
                           "Иначе нажмите кнопку «ОТМЕНА»"
        self.msg_19: str = "Тест 3 не пройден. Блок не исправен. Не работает сброс ЗМН"
        self.msg_20: str = "С помощью кнопок на лицевой панели установите следующие значения: - I>>> 400А;"
        self.msg_21: str = "Если на дисплее загорелась надпись «ВКЛ» и погасла надпись «ОТКЛ» нажмите кнопку «ОК». " \
                           "Иначе нажмите кнопку «ОТМЕНА»"
        self.msg_23: str = "Если на дисплее стали активны надписи АВАРИЯ, ПИТАНИЕ, ОТКЛ " \
                           "и на дисплее появилась надпись " \
                           "«Сработала защита МТЗ» нажмите кнопку «ОК». Иначе нажмите кнопку «ОТМЕНА»"
        self.msg_24: str = "Тест 4 не пройден. Блок не исправен. Блок не работает в режиме МТЗ»"
        self.msg_25: str = "Если на дисплее загорелась надпись «ВКЛ» и погасла надпись «ОТКЛ» нажмите кнопку «ОК». " \
                           "Иначе нажмите кнопку «ОТМЕНА»"
        self.msg_27: str = "Если на дисплее стали активны надписи ПИТАНИЕ, ОТКЛ и на дисплее появилась надпись  " \
                           "«Сработала защита ЗНФ» нажмите кнопку «ОК». Иначе нажмите кнопку «ОТМЕНА»"
        self.msg_28: str = "Тест 5 не пройден. Блок не исправен.Нет отключения от защиты ЗНФ»"

        logging.basicConfig(
            filename="C:\\Stend\\project_class\\log\\TestMKZP64Sh.log",
            filemode="w",
            level=logging.DEBUG,
            encoding="utf-8",
            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('WARNING')
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))

    def st_test_10(self) -> bool:
        """
        Тест 1
        :return: 
        """
        self.cli_log.lev_info(f"старт теста {__doc__}", "skyblue")
        self.conn_opc.simplified_read_di(['inp_14', 'inp_15'])
        if my_msg(self.msg_1):
            pass
        else:
            return False
        self.logger.debug('тест 1.1')
        self.mysql_conn.mysql_ins_result("идёт тест 1.1", '1')
        meas_volt_ust = self.proc.procedure_1_21_31()
        if meas_volt_ust != 0.0:
            pass
        else:
            self.logger.debug('неисправен')
            self.mysql_conn.mysql_ins_result("неисправен", '1')
            return False
        self.conn_opc.ctrl_relay('KL73', True)
        sleep(5)
        self.logger.debug("таймаут 5 сек")
        self.cli_log.lev_debug("таймаут 5 сек", "gray")
        self.conn_opc.ctrl_relay('KL90', True)
        sleep(5)
        self.logger.debug("таймаут 5 сек")
        self.cli_log.lev_debug("таймаут 5 сек", "gray")
        self.conn_opc.ctrl_relay('KL63', True)
        meas_volt = self.conn_opc.read_ai('AI0')
        self.logger.debug(f'измеренное напряжение:\t{meas_volt}')
        if 0.8 * meas_volt_ust <= meas_volt <= 1.0 * meas_volt_ust:
            pass
        else:
            self.mysql_conn.mysql_ins_result('неисправен', '1')
            self.reset.sbros_kl63_proc_1_21_31()
            return False
        self.reset.sbros_kl63_proc_1_21_31()
        return True

    def st_test_11(self) -> bool:
        self.logger.debug('тест 1.2')
        self.mysql_conn.mysql_ins_result("идёт тест 1.2", '1')
        self.coef_volt = self.proc.procedure_1_22_32()
        if self.coef_volt != 0.0:
            pass
        else:
            self.mysql_conn.mysql_ins_result('неисправен', '1')
            return False
        self.reset.stop_procedure_32()
        self.conn_opc.ctrl_relay('KL100', True)
        sleep(0.3)
        self.logger.debug("таймаут 0.3 сек")
        self.cli_log.lev_debug("таймаут 0.3 сек", "gray")
        self.conn_opc.ctrl_relay('KL21', True)
        sleep(0.3)
        self.logger.debug("таймаут 0.3 сек")
        self.cli_log.lev_debug("таймаут 0.3 сек", "gray")
        self.conn_opc.ctrl_relay('KL36', True)
        sleep(0.3)
        self.logger.debug("таймаут 0.3 сек")
        self.cli_log.lev_debug("таймаут 0.3 сек", "gray")
        self.conn_opc.ctrl_relay('KL88', True)
        sleep(2.5)
        self.logger.debug("таймаут 2.5 сек")
        self.cli_log.lev_debug("таймаут 2.5 сек", "gray")
        self.conn_opc.ctrl_relay('KL66', True)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        self.conn_opc.ctrl_relay('KL92', True)
        return True

    def st_test_12(self) -> bool:
        self.logger.debug('тест 1.3')
        self.mysql_conn.mysql_ins_result("идёт тест 1.3", '1')
        if my_msg(self.msg_2):
            if my_msg(self.msg_3):
                pass
            else:
                self.logger.debug('тест 1.3 неисправен')
                self.mysql_conn.mysql_ins_result("неисправен", '1')
                my_msg(self.msg_4)
                return False
        else:
            return False
        sleep(10)
        self.logger.debug("таймаут 10 сек")
        self.cli_log.lev_debug("таймаут 10 сек", "gray")
        self.conn_opc.ctrl_relay('KL99', True)
        return True

    def st_test_13(self) -> bool:
        self.logger.debug('тест 1.4')
        self.mysql_conn.mysql_ins_result("идёт тест 1.4", '1')
        sleep(5)
        self.logger.debug("таймаут 5 сек")
        self.cli_log.lev_debug("таймаут 5 сек", "gray")
        if my_msg(self.msg_5):
            pass
        else:
            self.logger.debug('тест 1.4 неисправен')
            self.mysql_conn.mysql_ins_result("неисправен", '1')
            my_msg(self.msg_6)
            return False
        sleep(5)
        self.logger.debug("таймаут 5 сек")
        self.cli_log.lev_debug("таймаут 5 сек", "gray")
        self.conn_opc.ctrl_relay('KL99', False)
        return True

    def st_test_14(self) -> bool:
        self.logger.debug('тест 1.5')
        self.mysql_conn.mysql_ins_result("идёт тест 1.5", '1')
        sleep(5)
        self.logger.debug("таймаут 5 сек")
        self.cli_log.lev_debug("таймаут 5 сек", "gray")
        if my_msg(self.msg_7):
            pass
        else:
            self.logger.debug('тест 1.6 неисправен')
            self.mysql_conn.mysql_ins_result("неисправен", '1')
            my_msg(self.msg_8)
            return False
        self.logger.debug('тест 1 пройден')
        self.mysql_conn.mysql_ins_result("исправен", '1')
        return True

    def st_test_20(self) -> bool:
        """
        Тест 2. Контроль изоляции
        :return:
        """
        self.logger.debug('тест 2.1')
        self.mysql_conn.mysql_ins_result("идёт тест 2.1", '2')
        sleep(5)
        self.logger.debug("таймаут 5 сек")
        self.cli_log.lev_debug("таймаут 5 сек", "gray")
        self.conn_opc.ctrl_relay('KL99', True)
        sleep(5)
        self.logger.debug("таймаут 5 сек")
        self.cli_log.lev_debug("таймаут 5 сек", "gray")
        if my_msg(self.msg_9):
            pass
        else:
            self.logger.debug('тест 2.1 неисправен')
            self.mysql_conn.mysql_ins_result("неисправен", '2')
            my_msg(self.msg_6)
            return False
        self.conn_opc.ctrl_relay('KL98', True)
        return True

    def st_test_21(self) -> bool:
        self.logger.debug('тест 2.2')
        self.mysql_conn.mysql_ins_result("идёт тест 2.2", '2')
        sleep(3)
        self.logger.debug("таймаут 3 сек")
        self.cli_log.lev_debug("таймаут 3 сек", "gray")
        if my_msg(self.msg_11):
            pass
        else:
            self.logger.debug('тест 2.2 неисправен')
            self.mysql_conn.mysql_ins_result("неисправен", '2')
            my_msg(self.msg_12)
            return False
        self.conn_opc.ctrl_relay('KL98', False)
        return True

    def st_test_22(self) -> bool:
        self.logger.debug('тест 2.3')
        self.mysql_conn.mysql_ins_result("идёт тест 2.3", '2')
        if my_msg(self.msg_13):
            pass
        else:
            return False
        sleep(5)
        self.logger.debug("таймаут 5 сек")
        self.cli_log.lev_debug("таймаут 5 сек", "gray")
        self.conn_opc.ctrl_relay('KL97', True)
        sleep(1.5)
        self.logger.debug("таймаут 1.5 сек")
        self.cli_log.lev_debug("таймаут 1.5 сек", "gray")
        if my_msg(self.msg_14):
            pass
        else:
            self.logger.debug('тест 2.3 неисправен')
            self.mysql_conn.mysql_ins_result("неисправен", '2')
            my_msg(self.msg_15)
            return False
        sleep(1.5)
        self.logger.debug("таймаут 1.5 сек")
        self.cli_log.lev_debug("таймаут 1.5 сек", "gray")
        self.conn_opc.ctrl_relay('KL97', False)
        sleep(5)
        self.logger.debug("таймаут 5 сек")
        self.cli_log.lev_debug("таймаут 5 сек", "gray")
        self.logger.debug('тест 2 пройден')
        self.mysql_conn.mysql_ins_result("исправен", '2')
        if my_msg(self.msg_13):
            pass
        else:
            return False
        return True

    def st_test_30(self) -> bool:
        """
        Тест 3. Работа защиты минимального напряжения.
        :return:
        """
        self.logger.debug('тест 3.1')
        self.mysql_conn.mysql_ins_result("идёт тест 3.1", '3')
        self.conn_opc.ctrl_relay('KL69', True)
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if my_msg(self.msg_16):
            pass
        else:
            self.logger.debug('тест 3.1 неисправен')
            self.mysql_conn.mysql_ins_result("неисправен", '3')
            my_msg(self.msg_17)
            return False
        self.conn_opc.ctrl_relay('KL69', False)
        return True

    def st_test_31(self) -> bool:
        self.logger.debug('тест 3.2')
        self.mysql_conn.mysql_ins_result("идёт тест 3.2", '3')
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        if my_msg(self.msg_13):
            if my_msg(self.msg_18):
                pass
            else:
                self.logger.debug('тест 3.2 неисправен')
                self.mysql_conn.mysql_ins_result("неисправен", '3')
                my_msg(self.msg_19)
                return False
        else:
            return False
        self.logger.debug('тест 3 пройден')
        self.mysql_conn.mysql_ins_result("исправен", '3')
        return True

    def st_test_40(self) -> bool:
        """
        # Тест 4. Проверка работоспособности токовой защиты.
        :return
        """
        self.logger.debug('тест 4.1')
        self.mysql_conn.mysql_ins_result("идёт тест 4.1", '4')
        if my_msg(self.msg_20):
            pass
        else:
            return False
        self.conn_opc.ctrl_relay('KL99', False)
        sleep(5)
        self.logger.debug("таймаут 5 сек")
        self.cli_log.lev_debug("таймаут 5 сек", "gray")
        self.conn_opc.ctrl_relay('KL99', True)
        return True

    def st_test_41(self) -> bool:
        self.logger.debug('тест 4.2')
        self.mysql_conn.mysql_ins_result("идёт тест 4.2", '4')
        sleep(5)
        self.logger.debug("таймаут 5 сек")
        self.cli_log.lev_debug("таймаут 5 сек", "gray")
        if my_msg(self.msg_21):
            pass
        else:
            self.logger.debug('тест 4.2 неисправен')
            self.mysql_conn.mysql_ins_result("неисправен", '4')
            my_msg(self.msg_6)
            return False
        return True

    def st_test_42(self) -> bool:
        if self.proc.procedure_x4_to_x5(setpoint_volt=self.ust_1, coef_volt=self.coef_volt):
            pass
        else:
            self.mysql_conn.mysql_ins_result('неисправен', '4')
            return False
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        self.conn_opc.ctrl_relay('KL63', True)
        sleep(0.5)
        self.logger.debug("таймаут 0.5 сек")
        self.cli_log.lev_debug("таймаут 0.5 сек", "gray")
        self.conn_opc.ctrl_relay('KL63', False)
        self.reset.stop_procedure_3()
        if my_msg(self.msg_23):
            pass
        else:
            self.logger.debug('тест 4.3 неисправен')
            self.mysql_conn.mysql_ins_result("неисправен", '4')
            my_msg(self.msg_24)
            return False
        if my_msg(self.msg_13):
            pass
        else:
            return False
        self.logger.debug('тест 4 пройден')
        self.mysql_conn.mysql_ins_result("исправен", '4')
        return True

    def st_test_50(self) -> bool:
        """
        Тест 5. Проверка работоспособности защит от несимметрии фаз.
        :return
        """
        self.logger.debug('тест 5.1')
        self.mysql_conn.mysql_ins_result("идёт тест 5.1", '5')
        self.conn_opc.ctrl_relay('KL99', False)
        sleep(5)
        self.logger.debug("таймаут 5 сек")
        self.cli_log.lev_debug("таймаут 5 сек", "gray")
        self.conn_opc.ctrl_relay('KL99', True)
        sleep(5)
        self.logger.debug("таймаут 5 сек")
        self.cli_log.lev_debug("таймаут 5 сек", "gray")
        if my_msg(self.msg_25):
            pass
        else:
            self.logger.debug('тест 5.1 неисправен')
            self.mysql_conn.mysql_ins_result("неисправен", '5')
            my_msg(self.msg_6)
            return False
        return True

    def st_test_51(self) -> bool:
        self.logger.debug('тест 5.2')
        self.mysql_conn.mysql_ins_result("идёт тест 5.2", '5')
        if self.proc.procedure_x4_to_x5(setpoint_volt=self.ust_2, coef_volt=self.coef_volt):
            pass
        else:
            self.mysql_conn.mysql_ins_result('неисправен', '5')
            return False
        sleep(1)
        self.logger.debug("таймаут 1 сек")
        self.cli_log.lev_debug("таймаут 1 сек", "gray")
        self.conn_opc.ctrl_relay('KL63', True)
        sleep(0.1)
        self.logger.debug("таймаут 0.1 сек")
        self.cli_log.lev_debug("таймаут 0.1 сек", "gray")
        self.conn_opc.ctrl_relay('KL81', True)
        sleep(15)
        self.logger.debug("таймаут 15 сек")
        self.cli_log.lev_debug("таймаут 15 сек", "gray")
        self.conn_opc.ctrl_relay('KL63', False)
        self.reset.stop_procedure_3()
        if my_msg(self.msg_27):
            pass
        else:
            self.logger.debug('тест 5.2 неисправен')
            self.mysql_conn.mysql_ins_result("неисправен", '5')
            my_msg(self.msg_28)
            return False
        return True

    def st_test_52(self) -> bool:
        if my_msg(self.msg_13):
            pass
        else:
            return False
        self.logger.debug('тест 5 пройден')
        self.mysql_conn.mysql_ins_result("исправен", '5')
        return True

    def st_test_mkzp_6_4sh(self) -> [bool, None]:
        if self.st_test_10():
            if self.st_test_11():
                if self.st_test_12():
                    if self.st_test_13():
                        if self.st_test_14():
                            if self.st_test_20():
                                if self.st_test_21():
                                    if self.st_test_22():
                                        if self.st_test_30():
                                            if self.st_test_31():
                                                if self.st_test_40():
                                                    if self.st_test_41():
                                                        if self.st_test_42():
                                                            if self.st_test_50():
                                                                if self.st_test_51():
                                                                    if self.st_test_52():
                                                                        return True, self.health_flag
        return False, self.health_flag

    def full_test_mkzp_6_4sh(self) -> None:
        try:
            start_time = time()
            test, health_flag = self.st_test_mkzp_6_4sh()
            end_time = time()
            time_spent = end_time - start_time
            self.cli_log.lev_info(f"Время выполнения: {time_spent}", "gray")
            self.logger.debug(f"Время выполнения: {time_spent}")
            self.mysql_conn.mysql_add_message(f"Время выполнения: {time_spent}")

            if test and not health_flag:
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
        except HardwareException as hwe:
            self.logger.debug(f'{hwe}')
            self.cli_log.lev_warning(f'{hwe}', 'red')
            my_msg(f'{hwe}', 'red')
        except AttributeError as ae:
            self.logger.debug(f"Неверный атрибут. {ae}")
            self.cli_log.lev_warning(f"Неверный атрибут. {ae}", 'red')
            my_msg(f"Неверный атрибут. {ae}", 'red')
        except ValueError as ve:
            self.logger.debug(f"Некорректное значение для переменной. {ve}")
            self.cli_log.lev_warning(f"Некорректное значение для переменной. {ve}", 'red')
            my_msg(f"Некорректное значение для переменной. {ve}", 'red')
        finally:
            self.conn_opc.full_relay_off()
            self.conn_opc.opc_close()
            sys.exit()
