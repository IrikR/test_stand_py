# -*- coding: utf-8 -*-

from old_alg.alg_bki_2t_old import TestBKI2T
# from new_alg.alg_bki_2t import TestBKI2T
# from new_alg.try_except import TryExcept


def bki_2t():
    """
    Вариант запуска старых алгоритмов
    :return:
    """
    test_bki = TestBKI2T()
    test_bki.full_test_bki_2t()


# def bki_2t():
#     """
#     Вариант запуска новых алгоритмов
#     :return:
#     """
#     try_except = TryExcept()
#     test_bki = TestBKI2T()
#     try_except.full_start_test(test_bki.st_test_bki_2t, None, 0)


if __name__ == "__main__":
    bki_2t()
