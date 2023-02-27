# -*- coding: utf-8 -*-

from old_alg.alg_bru_2sr_old import TestBRU2SR
# from new_alg.alg_bru_2sr import TestBRU2SR
# from new_alg.try_except import TryExcept


def bru_2sr():
    """
    Вариант запуска старых алгоритмов
    :return:
    """
    test_bru = TestBRU2SR()
    test_bru.full_test_bru_2sr()


# def bru_2sr():
#     """
#     Вариант запуска новых алгоритмов
#     :return:
#     """
#     try_except = TryExcept()
#     test_bru = TestBRU2SR()
#     try_except.full_start_test(test_bru.st_test_bru_2sr, None, 0)


if __name__ == "__main__":
    bru_2sr()
