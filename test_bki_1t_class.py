# -*- coding: utf-8 -*-

from old_alg.alg_bki_1t_old import TestBKI1T
# from new_alg.alg_bki_1t import TestBKI1T
# from new_alg.try_except import TryExcept


def bki_1t():
    """
    Вариант запуска старых алгоритмов
    :return:
    """
    test_bki = TestBKI1T()
    test_bki.full_test_bki_1t()


# def bki_1t():
#     """
#     Вариант запуска новых алгоритмов
#     :return:
#     """
#     try_except = TryExcept()
#     test_bki = TestBKI1T()
#     try_except.full_start_test(test_bki.st_test_bki_1t, None, 0)


if __name__ == "__main__":
    bki_1t()
