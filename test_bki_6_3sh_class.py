# -*- coding: utf-8 -*-

from old_alg.alg_bki_6_3sh_old import TestBKI6
# from new_alg.alg_bki_6_3sh import TestBKI6
# from new_alg.try_except import TryExcept


def bki_6_3sh():
    """
    Вариант запуска старых алгоритмов
    :return:
    """
    test_bki = TestBKI6()
    test_bki.full_test_bki_6_3sh()


# def bki_6_3sh():
#     """
#     Вариант запуска новых алгоритмов
#     :return:
#     """
#     try_except = TryExcept()
#     test_bki = TestBKI6()
#     try_except.full_start_test(test_bki.st_test_bki_6_3sh, None, 0)


if __name__ == "__main__":
    bki_6_3sh()
