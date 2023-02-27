# -*- coding: utf-8 -*-

# from old_alg.alg_bdu_dr01_old import TestBDUDR01
from new_alg.alg_bdu_dr01 import TestBDUDR01
from new_alg.try_except import TryExcept

# def bdu_dr01():
#     test_bdu = TestBDUDR01()
#     test_bdu.full_test_bdu_dr01()

def bdu_dr01():
    try_except = TryExcept()
    test_bdu = TestBDUDR01()
    try_except.full_start_test(test_bdu.st_test_bdu_dr01, None, 0)


if __name__ == "__main__":
    bdu_dr01()
