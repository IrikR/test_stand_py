# -*- coding: utf-8 -*-

from old_alg.alg_bu_pmvir_old import TestBUPMVIR
# from new_alg.alg_bu_pmvir import TestBUPMVIR
# from new_alg.try_except import TryExcept


def bu_pmvir():
    """
    Вариант запуска старых алгоритмов
    :return:
    """
    test_bu = TestBUPMVIR()
    test_bu.full_test_bu_pmvir()


# def bu_pmvir():
#     """
#     Вариант запуска новых алгоритмов
#     :return:
#     """
#     try_except = TryExcept()
#     test_bu = TestBUPMVIR()
#     try_except.full_start_test(test_bu.st_test_bu_pmvir, None, 0)


if __name__ == "__main__":
    bu_pmvir()
