# -*- coding: utf-8 -*-

from old_alg.alg_mtz_5_v2_7_old import TestMTZ5V27
# from new_alg.alg_mtz_5_v2_7 import TestMTZ5V27
# from new_alg.try_except import TryExcept


def mtz_5_v27():
    """
    Вариант запуска старых алгоритмов
    :return:
    """
    test_mtz = TestMTZ5V27()
    test_mtz.full_test_mtz_5_v2_7()


# def mtz_5_v27():
#     """
#     Вариант запуска новых алгоритмов
#     :return:
#     """
#     try_except = TryExcept()
#     test_mtz = TestMTZ5V27()
#     try_except.full_start_test(test_mtz.st_test_mtz_5_v2_7, test_mtz.result_test_mtz, 1)


if __name__ == "__main__":
    mtz_5_v27()
