# -*- coding: utf-8 -*-

from old_alg.alg_btz_3_old import TestBTZ3
# from new_alg.alg_btz_3 import TestBTZ3
# from new_alg.try_except import TryExcept


def btz_3():
    """
    Вариант запуска старых алгоритмов
    :return:
    """
    test_btz = TestBTZ3()
    test_btz.full_test_btz_3()


# def btz_3():
#     """
#     Вариант запуска новых алгоритмов
#     :return:
#     """
#     try_except = TryExcept()
#     test_btz = TestBTZ3()
#     try_except.full_start_test(test_btz.st_test_btz_3, test_btz.result_test_btz_3, 1)


if __name__ == "__main__":
    btz_3()
