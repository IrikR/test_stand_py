# -*- coding: utf-8 -*-


from old_alg.alg_bdu_4_3_old import TestBDU43
# from new_alg.alg_bdu_4_3 import TestBDU43
# from new_alg.try_except import TryExcept


def bdu_4_3():
    """
    Вариант запуска старых алгоритмов
    :return:
    """
    test_bdu_4_3 = TestBDU43()
    test_bdu_4_3.full_test_bdu_4_3()


# def bdu_4_3():
#     """
#     Вариант запуска новых алгоритмов
#     :return:
#     """
#     try_except = TryExcept()
#     test_bdu_4_3 = TestBDU43()
#     try_except.full_start_test(test_bdu_4_3.st_test_bdu_4_3, None, 0)


if __name__ == "__main__":
    bdu_4_3()
