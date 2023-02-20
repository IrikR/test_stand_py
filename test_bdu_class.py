# -*- coding: utf-8 -*-

from new_alg.try_except import TryExcept
from new_alg.alg_bdu import TestBDU


def bdu():
    try_except = TryExcept()
    test_bdu = TestBDU()
    try_except.full_start_test(test_bdu.st_test_bdu, None, 0)

if __name__ == "__main__":
    bdu()
