# -*- coding: utf-8 -*-

from old_alg.alg_mmtz_d_old import TestMMTZD
# from new_alg.alg_mmtz_d import TestMMTZD
# from new_alg.try_except import TryExcept


def mmtz():
    """
    Вариант запуска старых алгоритмов
    :return:
    """
    test_mmtz = TestMMTZD()
    test_mmtz.full_test_mmtz_d()


# def mmtz():
#     """
#     Вариант запуска новых алгоритмов
#     :return:
#     """
#     try_except = TryExcept()
#     test_mmtz = TestMMTZD()
#     try_except.full_start_test(test_mmtz.st_test_mmtz_d, None, 1)


if __name__ == "__main__":
    mmtz()
