# -*- coding: utf-8 -*-

from new_alg.alg_tzp import TestTZP
from new_alg.try_except import TryExcept


def tzp():
    test_tzp = TestTZP()
    try_except = TryExcept()
    try_except.full_start_test(test_tzp.st_test_tzp, test_tzp.result_test_tzp, 1)


if __name__ == "__main__":
    tzp()
