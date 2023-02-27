# -*- coding: utf-8 -*-

from old_alg.alg_buz_2_old import TestBUZ2
# from new_alg.alg_buz_2 import TestBUZ2
# from new_alg.try_except import TryExcept


def buz():
    """
    Вариант запуска старых алгоритмов
    :return:
    """
    test_buz = TestBUZ2()
    test_buz.full_test_buz_2()


# def buz():
#     """
#     Вариант запуска новых алгоритмов
#     :return:
#     """
#     try_except = TryExcept()
#     test_buz = TestBUZ2()
#     try_except.full_start_test(test_buz.st_test_buz_2, None, 1)


if __name__ == "__main__":
    buz()
