# -*- coding: utf-8 -*-

from old_alg.alg_ubtz_old import TestUBTZ
# from new_alg.alg_ubtz import TestUBTZ
# from new_alg.try_except import TryExcept


def ubtz():
    """
    Вариант запуска старых алгоритмов
    :return:
    """
    test_ubtz = TestUBTZ()
    test_ubtz.full_test_ubtz()


# def ubtz():
#     """
#     Вариант запуска новых алгоритмов
#     :return:
#     """
#     try_except = TryExcept()
#     test_ubtz = TestUBTZ()
#     try_except.full_start_test(test_ubtz.st_test_ubtz, test_ubtz.result_test_ubtz, 1)


if __name__ == "__main__":
    ubtz()
