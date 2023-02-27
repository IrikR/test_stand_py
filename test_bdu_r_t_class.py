# -*- coding: utf-8 -*-

from old_alg.alg_bdu_r_t_old import TestBDURT
# from new_alg.alg_bdu_r_t import TestBDURT
# from new_alg.try_except import TryExcept


def bdu_r_t():
    """
    Вариант запуска старых алгоритмов
    :return:
    """
    test_bdu = TestBDURT()
    test_bdu.full_test_bdu_r_t()


# def bdu_r_t():
#     """
#     Вариант запуска новых алгоритмов
#     :return:
#     """
#     try_except = TryExcept()
#     test_bdu = TestBDURT()
#     try_except.full_start_test(test_bdu.st_test_bdu_r_t, None, 0)


if __name__ == "__main__":
    bdu_r_t()
