# -*- coding: utf-8 -*-

from old_alg.alg_bur_pmvir_old import TestBURPMVIR
# from new_alg.alg_bur_pmvir import TestBURPMVIR
# from new_alg.try_except import TryExcept


def bur():
    """
    Вариант запуска старых алгоритмов
    :return:
    """
    test_bur = TestBURPMVIR()
    test_bur.full_test_bur_pmvir()


# def bur():
#     """
#     Вариант запуска новых алгоритмов
#     :return:
#     """
#     try_except = TryExcept()
#     test_bur = TestBURPMVIR()
#     try_except.full_start_test(test_bur.st_test_bur_pmvir, None, 0)


if __name__ == "__main__":
    bur()
