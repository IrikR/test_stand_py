#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from time import time

from general_func.reset import ResetRelay
from general_func.modbus import CtrlKL


def res_rel_0():
    rr0 = ResetRelay()
    start_time = time()
    rr0.reset_all()
    stop_time = time()
    timer = stop_time - start_time
    print(timer)


def res_rel_1():
    rr1 = CtrlKL()
    start_time = time()
    rr1.reset_all_v1()
    stop_time = time()
    timer = stop_time - start_time
    print(timer)


def res_rel_2():
    rr2 = CtrlKL()
    start_time = time()
    rr2.reset_all_v2()
    stop_time = time()
    timer = stop_time - start_time
    print(timer)


if __name__ == '__main__':
    try:
        res_rel_0()
        # res_rel_1()
        # res_rel_2()
    except OSError:
        print("ошибка системы")
    except SystemError:
        print("внутренняя ошибка")
    finally:
        sys.exit()
