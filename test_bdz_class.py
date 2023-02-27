# -*- coding: utf-8 -*-

from old_alg.alg_bdz_old import TestBDZ
# from new_alg.alg_bdz import TestBDZ
# from new_alg.try_except import TryExcept


def bdz():
    """
    Вариант запуска старых алгоритмов
    :return:
    """
    test_bdz = TestBDZ()
    test_bdz.full_test_bdz()


# def bdz():
#     """
#     Вариант запуска новых алгоритмов
#     :return:
#     """
#     try_except = TryExcept()
#     test_bdz = TestBDZ()
#     try_except.full_start_test(test_bdz.st_test_bdz, None, 0)


if __name__ == "__main__":
    bdz()
