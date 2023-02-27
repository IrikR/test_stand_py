# -*- coding: utf-8 -*-

from old_alg.alg_bu_apsh_m_old import TestBUAPSHM
# from new_alg.alg_bu_apsh_m import TestBUAPSHM
# from new_alg.try_except import TryExcept


def bu_apshm():
    """
    Вариант запуска старых алгоритмов
    :return:
    """
    test_bu = TestBUAPSHM()
    test_bu.full_test_bu_apsh_m()


# def bu_apshm():
#     """
#     Вариант запуска новых алгоритмов
#     :return:
#     """
#     try_except = TryExcept()
#     test_bu = TestBUAPSHM()
#     try_except.full_start_test(test_bu.st_test_bu_apsh_m, None, 0)


if __name__ == "__main__":
    bu_apshm()
