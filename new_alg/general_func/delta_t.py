# -*- coding: utf-8 -*-
"""
Модуль теста времени срабатывания защит блока
"""

__all__ = ["DeltaT"]

from time import time

from .database import MySQLConnect
from .exception import HardwareException
from .opc_full import ConnectOPC


class DeltaT:

    def __init__(self):
        self.mysql_conn = MySQLConnect()
        self.conn_opc = ConnectOPC()

    def delta_t_tzp(self, di_xx: list[str], max_dt: float = 370.0, position: bool = True) -> float:
        """
        Тест на время срабатывания защиты ТЗП
        Отсчет начинается с момента включения KL63, контроль включения на входе ПЛК (НЗ контакт, в основном это 09 вход)
        и останавливается при размыкании контакта на входе ПЛК (НР контакт, в основном это 05 вход)
        :type di_xx: list[str]
        :param di_xx: входы контроллера пример: ['inp_09', 'inp_05']
        :type max_dt: float
        :param max_dt: максимальное время, за которое должен сработать блок, по умолчанию 370
        :type position: bool
        :param position: положение контакта в исходном состоянии
        :rtype: float
        :return: время срабатывания
        """
        di_1, di_2 = di_xx
        calc_delta_t_tzp: float = 0.0
        i1: int = 0

        inp_1, *_ = self.conn_opc.simplified_read_di([di_1])

        while not inp_1 and i1 <= 10:
            inp_1, *_ = self.conn_opc.simplified_read_di([di_1])
            i1 += 1
        if not inp_1:
            raise HardwareException("Неисправность в стенде, контроль состояния вторичного главного контакта KL63")

        start_timer_tzp = time()
        inp_2, *_ = self.conn_opc.simplified_read_di([di_2])
        while inp_2 is position and calc_delta_t_tzp <= max_dt:
            inp_2, *_ = self.conn_opc.simplified_read_di([di_2])
            stop_timer_tzp = time()
            calc_delta_t_tzp = stop_timer_tzp - start_timer_tzp
            self.mysql_conn.progress_level(calc_delta_t_tzp)

        return calc_delta_t_tzp

    # метод пока не реализован
    # def _delta_t_pmz(self, ust_num: int) -> bool:
    #     """
    #     Тест на время срабатывания защиты ПМЗ
    #     :type ust_num: int
    #     :param ust_num: номер уставки
    #     :return: bool результат подтеста
    #     """
    #     for qw in range(4):
    #         self.calc_delta_t_pmz, self.inp_01, self.inp_02, \
    #             self.inp_05, self.inp_06 = self.conn_opc.ctrl_ai_code_v0(103)
    #         if 3000.0 < self.calc_delta_t_pmz:
    #             if self.reset_protection(test_num=4, subtest_num=4.1):
    #                 qw += 1
    #                 continue
    #             else:
    #                 return False
    #         elif self.calc_delta_t_pmz < 3000 and not self.inp_01 and self.inp_05 and self.inp_02 and not self.inp_06:
    #             if self.reset_protection(test_num=4, subtest_num=4.1):
    #                 return True
    #             else:
    #                 return False
    #         else:
    #             if self.reset_protection(test_num=4, subtest_num=4.1):
    #                 qw += 1
    #                 continue
    #             else:
    #                 return False
    #     return False