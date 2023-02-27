# -*- coding: utf-8 -*-

from old_alg.alg_pmz_old import TestPMZ
# from new_alg.alg_pmz import TestPMZ
# from new_alg.try_except import TryExcept


def pmz():
    """
    Вариант запуска старых алгоритмов
    :return:
    """
    test_pmz = TestPMZ()
    test_pmz.full_test_pmz()


# def pmz():
#     """
#     Вариант запуска новых алгоритмов
#     :return:
#     """
#     try_except = TryExcept()
#     test_pmz = TestPMZ()
#     try_except.full_start_test(test_pmz.st_test_pmz, test_pmz.result_test_pmz, 1)


if __name__ == "__main__":
    pmz()
