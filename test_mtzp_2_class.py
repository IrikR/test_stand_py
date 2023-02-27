# -*- coding: utf-8 -*-

from old_alg.alg_mtzp_2_old import TestMTZP2
# from new_alg.alg_mtzp_2 import TestMTZP2
# from new_alg.try_except import TryExcept


def mtzp():
    """
    Вариант запуска старых алгоритмов
    :return:
    """
    test_mtzp = TestMTZP2()
    test_mtzp.full_test_mtzp_2()


# def mtzp():
#     """
#     Вариант запуска новых алгоритмов
#     :return:
#     """
#     try_except = TryExcept()
#     test_mtzp = TestMTZP2()
#     try_except.full_start_test(test_mtzp.st_test_mtzp_2, None, 1)


if __name__ == "__main__":
    mtzp()
