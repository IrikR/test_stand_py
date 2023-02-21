# -*- coding: utf-8 -*-

from new_alg.try_except import TryExcept
from new_alg.alg_bdu_1 import TestBDU1


def bdu_1():
    try_except = TryExcept()
    test_bdu_1 = TestBDU1()
    try_except.full_start_test(test_bdu_1.st_test_bdu_1, None, 0)


if __name__ == '__main__':
    bdu_1()
