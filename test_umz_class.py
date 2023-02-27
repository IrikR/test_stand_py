# -*- coding: utf-8 -*-

from old_alg.alg_umz_old import TestUMZ
# from new_alg.alg_umz import TestUMZ
# from new_alg.try_except import TryExcept


def umz():
    """
    Вариант запуска старых алгоритмов
    :return:
    """
    test_umz = TestUMZ()
    test_umz.full_test_umz()


# def umz():
#     """
#     Вариант запуска новых алгоритмов
#     :return:
#     """
#     try_except = TryExcept()
#     test_umz = TestUMZ()
#     try_except.full_start_test(test_umz.st_test_umz, test_umz.result_test_umz, 1)


if __name__ == "__main__":
    umz()
