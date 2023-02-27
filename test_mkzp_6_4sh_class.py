# -*- coding: utf-8 -*-

from old_alg.alg_mkzp_6_4sh_old import TestMKZP6
# from new_alg.alg_mkzp_6_4sh import TestMKZP6
# from new_alg.try_except import TryExcept


def mkzp():
    """
    Вариант запуска старых алгоритмов
    :return:
    """
    test_mkzp = TestMKZP6()
    test_mkzp.full_test_mkzp()


# def mkzp():
#     """
#     Вариант запуска новых алгоритмов
#     :return:
#     """
#     try_except = TryExcept()
#     test_mkzp = TestMKZP6()
#     try_except.full_start_test(test_mkzp.st_test_mkzp_6_4sh, None, 1)


if __name__ == "__main__":
    mkzp()
