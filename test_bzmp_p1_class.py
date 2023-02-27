# -*- coding: utf-8 -*-

from old_alg.alg_bzmp_p1_old import TestBZMPP1
# from new_alg.alg_bzmp_p1 import TestBZMPP1
# from new_alg.try_except import TryExcept


def bzmp_p1():
    """
    Вариант запуска старых алгоритмов
    :return:
    """
    test_bzmp = TestBZMPP1()
    test_bzmp.full_test_bzmp_p1()


# def bzmp_p1():
#     """
#     Вариант запуска новых алгоритмов
#     :return:
#     """
#     try_except = TryExcept()
#     test_bzmp = TestBZMPP1()
#     try_except.full_start_test(test_bzmp.st_test_bzmp_p1, None, 1)


if __name__ == "__main__":
    bzmp_p1()
