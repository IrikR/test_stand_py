# -*- coding: utf-8 -*-

from old_alg.alg_bmz_2_old import TestBMZ2
# from new_alg.alg_bmz_2 import TestBMZ2
# from new_alg.try_except import TryExcept


def bmz_2():
    """
    Вариант запуска старых алгоритмов
    :return:
    """
    test_bmz = TestBMZ2()
    test_bmz.full_test_bmz_2()


# def bmz_2():
#     """
#     Вариант запуска новых алгоритмов
#     :return:
#     """
#     try_except = TryExcept()
#     test_bmz = TestBMZ2()
#     try_except.full_start_test(test_bmz.st_test_bmz_2, test_bmz.result_test_bmz_2, 1)


if __name__ == "__main__":
    bmz_2()
