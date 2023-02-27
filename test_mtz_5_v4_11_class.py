# -*- coding: utf-8 -*-

from old_alg.alg_mtz_5_v4_11_old import TestMTZ5V411
# from new_alg.alg_mtz_5_v4_11 import TestMTZ5V411
# from new_alg.try_except import TryExcept


def mtz_5_v411():
    """
    Вариант запуска старых алгоритмов
    :return:
    """
    test_mtz = TestMTZ5V411()
    test_mtz.full_test_mtz_5_v4_11()


# def mtz_5_v411():
#     """
#     Вариант запуска новых алгоритмов
#     :return:
#     """
#     try_except = TryExcept()
#     test_mtz = TestMTZ5V411()
#     try_except.full_start_test(test_mtz.st_test_mtz, test_mtz.result_test_mtz, 1)


if __name__ == "__main__":
    mtz_5_v411()
