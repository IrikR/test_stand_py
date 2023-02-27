# -*- coding: utf-8 -*-

from old_alg.alg_bki_p_old import TestBKIP
# from new_alg.alg_bki_p import TestBKIP
from new_alg.try_except import TryExcept


def bki_p():
    """
    Вариант запуска старых алгоритмов
    :return:
    """
    test_bki = TestBKIP()
    test_bki.full_test_bki_p()


def bki_p():
    """
    Вариант запуска новых алгоритмов
    :return:
    """
    try_except = TryExcept()
    test_bki = TestBKIP()
    try_except.full_start_test(test_bki.st_test_bki_p, None, 0)


if __name__ == "__main__":
    bki_p()
