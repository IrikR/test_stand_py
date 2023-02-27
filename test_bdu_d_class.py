# -*- coding: utf-8 -*-


from old_alg.alg_bdu_d_old import TestBDUD
# from new_alg.alg_bdu_d import TestBDUD
# from new_alg.try_except import TryExcept


def bdu_d():
    """
    Вариант запуска старых алгоритмов
    :return:
    """
    test_bdu = TestBDUD()
    test_bdu.full_test_bdu_d()


# def bdu_d():
#     """
#     Вариант запуска новых алгоритмов
#     :return:
#     """
#     try_except = TryExcept()
#     test_bdu = TestBDUD()
#     try_except.full_start_test(test_bdu.st_test_bdu_d, None, 0)


if __name__ == "__main__":
    bdu_d()
