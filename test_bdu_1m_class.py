# -*- coding: utf-8 -*-

from old_alg.alg_bdu_1m_old import TestBDU1M
# from new_alg.alg_bdu_1m import TestBDU1M
# from new_alg.try_except import TryExcept


def bdu_1m():
    """
    Вариант запуска старых алгоритмов
    :return:
    """
    test_bdu_1m = TestBDU1M()
    test_bdu_1m.full_test_bdu_1m()


# def bdu_1m():
#     """
#     Вариант запуска новых алгоритмов
#     :return:
#     """
#     try_except = TryExcept()
#     test_bdu_1m = TestBDU1M()
#     try_except.full_start_test(test_bdu_1m.st_test_bdu_1m, None, 0)


if __name__ == "__main__":
    bdu_1m()