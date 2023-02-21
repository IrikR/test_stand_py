# -*- coding: utf-8 -*-

from new_alg.try_except import TryExcept
from new_alg.alg_bdu_014tp import TestBDU014TP


def bdu_014tp():
    try_except = TryExcept()
    test_bdu = TestBDU014TP()
    try_except.full_start_test(test_bdu.st_test_bdu_014tp, None, 0)


if __name__ == "__main__":
    bdu_014tp()
