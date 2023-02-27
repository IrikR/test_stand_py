# -*- coding: utf-8 -*-

from old_alg.alg_mtz_5_v2_8_old import TestMTZ5V28
# from new_alg.alg_mtz_5_v2_8 import TestMTZ5V28
# from new_alg.try_except import TryExcept


def mtz_5_v28():
    """
    Вариант запуска старых алгоритмов
    :return:
    """
    test_mtz = TestMTZ5V28()
    test_mtz.full_test_mtz_5_v2_8()


# def mtz_5_v28():
#     """
#     Вариант запуска новых алгоритмов
#     :return:
#     """
#     try_except = TryExcept()
#     test_mtz = TestMTZ5V28()
#     try_except.full_start_test(test_mtz.st_test_mtz, test_mtz.result_test_mtz, 1)


if __name__ == "__main__":
    mtz_5_v28()
