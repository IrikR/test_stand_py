# -*- coding: utf-8 -*-

from new_alg.alg_btz_t import TestBTZT
from new_alg.try_except import TryExcept


def btz_t():
    test_btz_t = TestBTZT()
    try_except = TryExcept()
    try_except.full_start_test(test_btz_t.st_test_btz_t, test_btz_t.result_test_btz_t, 2)


if __name__ == "__main__":
    btz_t()
