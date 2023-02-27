# -*- coding: utf-8 -*-

from old_alg.alg_bmz_apsh_4_old import TestBMZAPSH4
# from new_alg.alg_bmz_apsh_4 import TestBMZAPSH4
# from new_alg.try_except import TryExcept


def bmz_apsh4():
    """
    Вариант запуска старых алгоритмов
    :return:
    """
    test_bmz = TestBMZAPSH4()
    test_bmz.full_test_bmz_apsh_4()


# def bmz_apsh4():
#     """
#     Вариант запуска новых алгоритмов
#     :return:
#     """
#     try_except = TryExcept()
#     test_bmz = TestBMZAPSH4()
#     try_except.full_start_test(test_bmz.st_test_bmz_apsh_4, None, 1)


if __name__ == "__main__":
    bmz_apsh4()
