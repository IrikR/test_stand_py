# -*- coding: utf-8 -*-

from old_alg.alg_bdu_4_2_old import TestBDU42
# from new_alg.alg_bdu_4_2 import TestBDU42
# from new_alg.try_except import TryExcept


def bdu_4_2():
    """
    Вариант запуска старых алгоритмов
    :return:
    """
    test_bdu_4_2 = TestBDU42()
    test_bdu_4_2.full_test_bdu_4_2()


# def bdu_4_2():
#     """
#     Вариант запуска новых алгоритмов
#     :return:
#     """
#     try_except = TryExcept()
#     test_bdu_4_2 = TestBDU42()
#     try_except.full_start_test(test_bdu_4_2.st_test_bdu_4_2, None, 0)


if __name__ == "__main__":
    bdu_4_2()
