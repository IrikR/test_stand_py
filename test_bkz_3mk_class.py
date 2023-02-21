# -*- coding: utf-8 -*-

from new_alg.try_except import TryExcept
from new_alg.alg_bkz_3mk import TestBKZ3MK


def bkz_3mk():
    try_except = TryExcept()
    test_bkz_3mk = TestBKZ3MK()
    try_except.full_start_test(test_bkz_3mk.st_test_bkz_3mk, test_bkz_3mk.result_test_bkz_3mk, 2)

if __name__ == "__main__":
    bkz_3mk()
