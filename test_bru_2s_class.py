# -*- coding: utf-8 -*-

from old_alg.alg_bru_2s_old import TestBRU2S
# from new_alg.alg_bru_2s import TestBRU2S
# from new_alg.try_except import TryExcept


def bru_2s():
    """
    Вариант запуска старых алгоритмов
    :return:
    """
    test_bru = TestBRU2S()
    test_bru.full_test_bru_2s()


# def bru_2s():
#     """
#     Вариант запуска новых алгоритмов
#     :return:
#     """
#     try_except = TryExcept()
#     test_bru = TestBRU2S()
#     try_except.full_start_test(test_bru.st_test_bru_2s, None, 0)


if __name__ == "__main__":
    bru_2s()
