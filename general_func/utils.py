#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ctypes
import logging

from time import time

from .modbus import DIRead, CtrlKL
from .exception import *

__all__ = ["Bug", "DeltaTimeNoneKL63"]


class DeltaTimeNoneKL63:
    """
        Расчет дельты времени переключения выходов блока
        Сброс или запоминание состояние таймера текущего времени CPU T0[i], сек
        KL63 - ВКЛ	DQ5:1B - ВКЛ
        Запуск таймера происходит по условию замыкания DI.b1 (контакт реле KL63)
        Остановка таймера происходит по условию размыкания DI.a6 T1[i]

    """

    def __init__(self):
        self.ctrl_kl = CtrlKL()
        self.di_read = DIRead()
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))

    def calc_dt(self):
        self.ctrl_kl.ctrl_relay('KL63', True)
        in_b1 = self.__inputs_b1()
        while in_b1 is False:
            in_b1 = self.__inputs_b1()
        start_timer = time()
        in_ax = self.__inputs_a6()
        while in_ax is True:
            in_ax = self.__inputs_a6()
        stop_timer = time()
        delta_t_calc = stop_timer - start_timer
        return delta_t_calc

    def __inputs_a6(self):
        in_a6, *_ = self.di_read.di_read('in_a6')
        return in_a6

    def __inputs_b1(self):
        in_b1, *_ = self.di_read.di_read('in_b1')
        return in_b1


class Bug:
    """
        Вывод сообщений в консоль, с цветовой дифференциацией штанов
    """

    def __init__(self, dbg=None):
        self.dbg = dbg
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

    def debug_msg(self, *args):
        """
        :param args:
        :return: string
        """

        if self.dbg is True:
            msg, lev = args
            if lev == 1 or lev == 'red':
                # красный Red
                print("\033[31m {}".format(msg))
            elif lev == 2 or lev == 'orange':
                # оранжевый orange
                print("\033[33m {}".format(msg))
            elif lev == 3 or lev == 'blue':
                # голубой blue
                print("\033[36m {}".format(msg))
            elif lev == 4 or lev == 'green':
                # зеленый green
                print("\033[32m {}".format(msg))
            elif lev == 5 or lev == 'purple':
                # фиолетовый purple
                print("\033[35m {}".format(msg))
            else:
                # серый, если пришел неизвестный аргумент
                print("\033[37m {}".format(msg))
        else:
            pass


# class ResultMsg:
#     """
#     исправность/неисправность блока
#     """
#
#     def __init__(self):
#         self.reset = ResetRelay()
#
#     def test_error(self, test_number):
#         # msg = (f'Тест: {test_number} не пройден')
#         # my_msg(msg)
#         self.reset.reset_all()
#
#     def test_good(self):
#         # msg = "Тестирование завершено:\nБлок исправен "
#         # my_msg(msg)
#         self.reset.reset_all()


if __name__ == '__main__':
    try:
        pass
        # read_di = ReadDI()
#         # st_timer = time()
#         # a = read_mb.read_discrete(0)
#         # b = read_mb.read_discrete(1)
#         # c = read_mb.read_discrete(2)
#         # d = read_mb.read_discrete(3)
#         # e = read_mb.read_discrete(4)
#         # f = read_mb.read_discrete(5)
#         # g = read_mb.read_discrete(6)
#         # h = read_mb.read_discrete(7)
#         # j = read_mb.read_discrete(8)
#         # k = read_mb.read_discrete(9)
#         # l = read_mb.read_discrete(10)
#         # q = read_mb.read_discrete(11)
#         # a, b, c = read_mb.read_discrete_v1('in_a0', 'in_a1', 'in_a2')
#         # a = read_mb.read_discrete_v1('in_a0')
#         # a, b, c, d, e, f, g, h, j, k, l, q = read_mb.read_discrete_v1('in_a0', 'in_a1', 'in_a2', 'in_a3', 'in_a4',
#         #                                                               'in_a5', 'in_a6', 'in_a7', 'in_b0', 'in_b1',
#         #                                                               'in_b2', 'in_b3')
#         # stop_timer = time()
#         # print(a, b, c, d, e, f, g, h, j, k, l, q)
#         #
#         # # print(a, b, c)
#         # # print(a)
#         # print(type(a))
#         # print(stop_timer - st_timer)
#         # in_1, in_5, in_6 = read_di.inputs_di("in_a0, in_a5, in_a6")
#         # print(in_1, in_5, in_6)
#         in_2, *_ = read_di.inputs_di("in_a2")
#         print(in_2)
#         # in_4, in_7 = read_di.inputs_di("in_a4", "in_a7")
#         # print(in_4, in_7)
#         # in_3 = read_di.inputs_di("in_a3")
#         # print(in_3)
#         in_a0, in_a1 = read_di.inputs_di_1('in_a0', 'in_a1')
#         print(in_a0, in_a1)
    except IOError:
        print('системная ошибка')
    except ModbusConnectException as mce:
        print(mce)
    finally:
        print('end')
