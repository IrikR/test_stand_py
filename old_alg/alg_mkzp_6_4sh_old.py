#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки

Тип блока	Производитель
МКЗП-6-4Ш	ЗМТ «Энергия»
"""

import sys
import logging

from time import sleep

from .gen_func_procedure import *
from .gen_func_utils import *
from .my_msgbox import *
from .gen_mb_client import *
from .gen_mysql_connect import *

__all__ = ["TestMKZP6"]


class TestMKZP6(object):

    def __init__(self):
        self.__reset = ResetRelay()
        self.__proc = Procedure()
        self.__read_mb = ReadMB()
        self.__ctrl_kl = CtrlKL()
        self.__mysql_conn = MySQLConnect()
        self.__fault = Bug(True)

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

        logging.basicConfig(filename="C:\Stend\project_class\TestMKZP64Sh.log",
                            filemode="w",
                            level=logging.DEBUG,
                            encoding="utf-8",
                            format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
        logging.getLogger('mysql').setLevel('WARNING')
        self.logger = logging.getLogger(__name__)

    def st_test_10(self):
        """
        Тест 1
        :return: 
        """
        self.__inputs_a0()
        if my_msg(self.msg_1):
            pass
        else:
            return False
        self.__fault.debug_msg('тест 1.1', 3)
        self.__mysql_conn.mysql_ins_result("идёт тест 1.1", '1')
        meas_volt_ust = self.__proc.procedure_1_21_31()
        if meas_volt_ust != 0.0:
            pass
        else:
            self.__fault.debug_msg('неисправен', 1)
            self.__mysql_conn.mysql_ins_result("неисправен", '1')
            return False
        self.__ctrl_kl.ctrl_relay('KL73', True)
        sleep(5)
        self.__ctrl_kl.ctrl_relay('KL90', True)
        sleep(5)
        self.__ctrl_kl.ctrl_relay('KL63', True)
        meas_volt = self.__read_mb.read_analog()
        self.__fault.debug_msg(f'измеренное напряжение:\t{meas_volt}', 2)
        if 0.8 * meas_volt_ust <= meas_volt <= 1.0 * meas_volt_ust:
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '1')
            self.__reset.sbros_kl63_proc_1_21_31()
            return False
        self.__reset.sbros_kl63_proc_1_21_31()
        return True

    def st_test_11(self) -> bool:
        self.__fault.debug_msg('тест 1.2', 3)
        self.__mysql_conn.mysql_ins_result("идёт тест 1.2", '1')
        self.coef_volt = self.__proc.procedure_1_22_32()
        if self.coef_volt != 0.0:
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '1')
            return False
        self.__reset.stop_procedure_32()
        self.__ctrl_kl.ctrl_relay('KL100', True)
        sleep(0.3)
        self.__ctrl_kl.ctrl_relay('KL21', True)
        sleep(0.3)
        self.__ctrl_kl.ctrl_relay('KL36', True)
        sleep(0.3)
        self.__ctrl_kl.ctrl_relay('KL88', True)
        sleep(2.5)
        self.__ctrl_kl.ctrl_relay('KL66', True)
        sleep(1)
        self.__ctrl_kl.ctrl_relay('KL92', True)
        return True

    def st_test_12(self) -> bool:
        self.__fault.debug_msg('тест 1.3', 3)
        self.__mysql_conn.mysql_ins_result("идёт тест 1.3", '1')
        if my_msg(self.msg_2):
            if my_msg(self.msg_3):
                pass
            else:
                self.__fault.debug_msg('тест 1.3 неисправен', 1)
                self.__mysql_conn.mysql_ins_result("неисправен", '1')
                my_msg(self.msg_4)
                return False
        else:
            return False
        sleep(10)
        self.__ctrl_kl.ctrl_relay('KL99', True)
        return True

    def st_test_13(self) -> bool:
        self.__fault.debug_msg('тест 1.4', 3)
        self.__mysql_conn.mysql_ins_result("идёт тест 1.4", '1')
        sleep(5)
        if my_msg(self.msg_5):
            pass
        else:
            self.__fault.debug_msg('тест 1.4 неисправен', 1)
            self.__mysql_conn.mysql_ins_result("неисправен", '1')
            my_msg(self.msg_6)
            return False
        sleep(5)
        self.__ctrl_kl.ctrl_relay('KL99', False)
        return True

    def st_test_14(self) -> bool:
        self.__fault.debug_msg('тест 1.5', 3)
        self.__mysql_conn.mysql_ins_result("идёт тест 1.5", '1')
        sleep(5)
        if my_msg(self.msg_7):
            pass
        else:
            self.__fault.debug_msg('тест 1.6 неисправен', 1)
            self.__mysql_conn.mysql_ins_result("неисправен", '1')
            my_msg(self.msg_8)
            return False
        self.__fault.debug_msg('тест 1 пройден', 4)
        self.__mysql_conn.mysql_ins_result("исправен", '1')
        return True

    def st_test_20(self) -> bool:
        """
        Тест 2. Контроль изоляции
        :return:
        """
        self.__fault.debug_msg('тест 2.1', 3)
        self.__mysql_conn.mysql_ins_result("идёт тест 2.1", '2')
        sleep(5)
        self.__ctrl_kl.ctrl_relay('KL99', True)
        sleep(5)
        if my_msg(self.msg_9):
            pass
        else:
            self.__fault.debug_msg('тест 2.1 неисправен', 1)
            self.__mysql_conn.mysql_ins_result("неисправен", '2')
            my_msg(self.msg_6)
            return False
        self.__ctrl_kl.ctrl_relay('KL98', True)
        return True

    def st_test_21(self) -> bool:
        self.__fault.debug_msg('тест 2.2', 3)
        self.__mysql_conn.mysql_ins_result("идёт тест 2.2", '2')
        sleep(3)
        if my_msg(self.msg_11):
            pass
        else:
            self.__fault.debug_msg('тест 2.2 неисправен', 1)
            self.__mysql_conn.mysql_ins_result("неисправен", '2')
            my_msg(self.msg_12)
            return False
        self.__ctrl_kl.ctrl_relay('KL98', False)
        return True

    def st_test_22(self) -> bool:
        self.__fault.debug_msg('тест 2.3', 3)
        self.__mysql_conn.mysql_ins_result("идёт тест 2.3", '2')
        if my_msg(self.msg_13):
            pass
        else:
            return False
        sleep(5)
        self.__ctrl_kl.ctrl_relay('KL97', True)
        sleep(1.5)
        if my_msg(self.msg_14):
            pass
        else:
            self.__fault.debug_msg('тест 2.3 неисправен', 1)
            self.__mysql_conn.mysql_ins_result("неисправен", '2')
            my_msg(self.msg_15)
            return False
        sleep(1.5)
        self.__ctrl_kl.ctrl_relay('KL97', False)
        sleep(5)
        self.__fault.debug_msg('тест 2 пройден', 3)
        self.__mysql_conn.mysql_ins_result("исправен", '2')
        if my_msg(self.msg_13):
            pass
        else:
            return False
        return True

    def st_test_30(self) -> bool:
        """
        Тест 3. Работа защиты минимального напряжения
        :return:
        """
        self.__fault.debug_msg('тест 3.1', 3)
        self.__mysql_conn.mysql_ins_result("идёт тест 3.1", '3')
        self.__ctrl_kl.ctrl_relay('KL69', True)
        sleep(1)
        if my_msg(self.msg_16):
            pass
        else:
            self.__fault.debug_msg('тест 3.1 неисправен', 1)
            self.__mysql_conn.mysql_ins_result("неисправен", '3')
            my_msg(self.msg_17)
            return False
        self.__ctrl_kl.ctrl_relay('KL69', False)
        return True

    def st_test_31(self) -> bool:
        self.__fault.debug_msg('тест 3.2', 3)
        self.__mysql_conn.mysql_ins_result("идёт тест 3.2", '3')
        sleep(1)
        if my_msg(self.msg_13):
            if my_msg(self.msg_18):
                pass
            else:
                self.__fault.debug_msg('тест 3.2 неисправен', 1)
                self.__mysql_conn.mysql_ins_result("неисправен", '3')
                my_msg(self.msg_19)
                return False
        else:
            return False
        self.__fault.debug_msg('тест 3 пройден', 3)
        self.__mysql_conn.mysql_ins_result("исправен", '3')
        return True

    def st_test_40(self) -> bool:
        """
        # Тест 4. Проверка работоспособности токовой защиты
        :return
        """
        self.__fault.debug_msg('тест 4.1', 3)
        self.__mysql_conn.mysql_ins_result("идёт тест 4.1", '4')
        if my_msg(self.msg_20):
            pass
        else:
            return False
        self.__ctrl_kl.ctrl_relay('KL99', False)
        sleep(5)
        self.__ctrl_kl.ctrl_relay('KL99', True)
        return True

    def st_test_41(self) -> bool:
        self.__fault.debug_msg('тест 4.2', 3)
        self.__mysql_conn.mysql_ins_result("идёт тест 4.2", '4')
        sleep(5)
        if my_msg(self.msg_21):
            pass
        else:
            self.__fault.debug_msg('тест 4.2 неисправен', 1)
            self.__mysql_conn.mysql_ins_result("неисправен", '4')
            my_msg(self.msg_6)
            return False
        return True

    def st_test_42(self) -> bool:
        if self.__proc.procedure_x4_to_x5(setpoint_volt=self.ust_1, coef_volt=self.coef_volt):
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '4')
            return False
        sleep(1)
        self.__ctrl_kl.ctrl_relay('KL63', True)
        sleep(0.5)
        self.__ctrl_kl.ctrl_relay('KL63', False)
        self.__reset.stop_procedure_3()
        if my_msg(self.msg_23):
            pass
        else:
            self.__fault.debug_msg('тест 4.3 неисправен', 1)
            self.__mysql_conn.mysql_ins_result("неисправен", '4')
            my_msg(self.msg_24)
            return False
        if my_msg(self.msg_13):
            pass
        else:
            return False
        self.__fault.debug_msg('тест 4 пройден', 3)
        self.__mysql_conn.mysql_ins_result("исправен", '4')
        return True

    def st_test_50(self) -> bool:
        """
        Тест 5. Проверка работоспособности защит от несимметрии фаз
        :return
        """
        self.__fault.debug_msg('тест 5.1', 3)
        self.__mysql_conn.mysql_ins_result("идёт тест 5.1", '5')
        self.__ctrl_kl.ctrl_relay('KL99', False)
        sleep(5)
        self.__ctrl_kl.ctrl_relay('KL99', True)
        sleep(5)
        if my_msg(self.msg_25):
            pass
        else:
            self.__fault.debug_msg('тест 5.1 неисправен', 1)
            self.__mysql_conn.mysql_ins_result("неисправен", '5')
            my_msg(self.msg_6)
            return False
        return True

    def st_test_51(self) -> bool:
        self.__fault.debug_msg('тест 5.2', 3)
        self.__mysql_conn.mysql_ins_result("идёт тест 5.2", '5')
        if self.__proc.procedure_x4_to_x5(setpoint_volt=self.ust_2, coef_volt=self.coef_volt):
            pass
        else:
            self.__mysql_conn.mysql_ins_result('неисправен', '5')
            return False
        sleep(1)
        self.__ctrl_kl.ctrl_relay('KL63', True)
        sleep(0.1)
        self.__ctrl_kl.ctrl_relay('KL81', True)
        sleep(15)
        self.__ctrl_kl.ctrl_relay('KL63', False)
        self.__reset.stop_procedure_3()
        if my_msg(self.msg_27):
            pass
        else:
            self.__fault.debug_msg('тест 5.2 неисправен', 1)
            self.__mysql_conn.mysql_ins_result("неисправен", '5')
            my_msg(self.msg_28)
            return False
        return True

    def st_test_52(self) -> bool:
        if my_msg(self.msg_13):
            pass
        else:
            return False
        self.__fault.debug_msg('тест 5 пройден', 4)
        self.__mysql_conn.mysql_ins_result("исправен", '5')
        return True

    def __inputs_a0(self):
        in_a0 = self.__read_mb.read_discrete(0)
        if in_a0 is None:
            # logging.error(f'нет связи с контроллером')
            raise ModbusConnectException(f'нет связи с контроллером')
        return in_a0

    def st_test_mkzp_6_4sh(self) -> bool:
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
                                                                        return True
        return False

    def full_test_mkzp(self):
        try:
            if self.st_test_mkzp_6_4sh():
                self.__mysql_conn.mysql_block_good()
                my_msg('Блок исправен', 'green')
            else:
                self.__mysql_conn.mysql_block_bad()
                my_msg('Блок неисправен', 'red')
        except OSError:
            my_msg("ошибка системы", 'red')
        except SystemError:
            my_msg("внутренняя ошибка", 'red')
        except HardwareException as hwe:
            my_msg(f'{hwe}', 'red')
        finally:
            self.__reset.reset_all()
            sys.exit()


if __name__ == '__main__':
    test_mkzp = TestMKZP6()
    test_mkzp.full_test_mkzp()
    # reset_test_mkzp = ResetRelay()
    # mysql_conn_mkzp = MySQLConnect()
    # fault = Bug(True)
    # try:
    #     if test_mkzp.st_test_mkzp_6_4sh():
    #         mysql_conn_mkzp.mysql_block_good()
    #         my_msg('Блок исправен', 'green')
    #     else:
    #         mysql_conn_mkzp.mysql_block_bad()
    #         my_msg('Блок неисправен', 'red')
    # except OSError:
    #     my_msg("ошибка системы", 'red')
    # except SystemError:
    #     my_msg("внутренняя ошибка", 'red')
    # except HardwareException as hwe:
    #     my_msg(f'{hwe}', 'red')
    # finally:
    #     reset_test_mkzp.reset_all()
    #     sys.exit()
