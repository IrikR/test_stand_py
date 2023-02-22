# -*- coding: utf-8 -*-

from new_alg.alg_bdu_d4_2 import TestBDUD42
from new_alg.try_except import TryExcept


def bdu_d4_2():
    test_bdu_d4_2 = TestBDUD42()
    try_except = TryExcept()
    try_except.full_start_test(test_bdu_d4_2.st_test_bdu_d4_2, None, 0)


if __name__ == "__main__":
    bdu_d4_2()
