# -*- coding: utf-8 -*-

# from old_alg.alg_bmz_apsh_m_old import *
from new_alg.alg_bmz_apsh_m import TestBMZAPSHM
from new_alg.try_except import TryExcept

def bmz_apshm():
    test_bmz = TestBMZAPSHM()
    try_except = TryExcept()
    try_except.full_start_test(test_bmz.st_test_bmz_apsh_m, None, 1)


if __name__ == "__main__":
    bmz_apshm()
