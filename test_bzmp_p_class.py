# -*- coding: utf-8 -*-

from old_alg.alg_bzmp_p_old import TestBZMPP
# from new_alg.alg_bzmp_p import TestBZMPP
# from new_alg.try_except import TryExcept


def bzmp_p():
    """
    Вариант запуска старых алгоритмов
    :return:
    """
    test_bzmp = TestBZMPP()
    test_bzmp.full_test_bzmp_p()


# def bzmp_p():
#     """
#     Вариант запуска новых алгоритмов
#     :return:
#     """
#     try_except = TryExcept()
#     test_bzmp = TestBZMPP()
#     try_except.full_start_test(test_bzmp.st_test_bzmp_p, None, 1)


if __name__ == "__main__":
    bzmp_p()
