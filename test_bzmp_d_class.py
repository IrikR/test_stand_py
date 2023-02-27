# -*- coding: utf-8 -*-

from old_alg.alg_bzmp_d_old import TestBZMPD
# from new_alg.alg_bzmp_d import TestBZMPD
# from new_alg.try_except import TryExcept


def bzmp_d():
    """
    Вариант запуска старых алгоритмов
    :return:
    """
    test_bzmp = TestBZMPD()
    test_bzmp.full_test_bzmp_d()


# def bzmp_d():
#     """
#     Вариант запуска новых алгоритмов
#     :return:
#     """
#     try_except = TryExcept()
#     test_bzmp = TestBZMPD()
#     try_except.full_start_test(test_bzmp.st_test_bzmp_d, None, 1)


if __name__ == "__main__":
    bzmp_d()
