# -*- coding: utf-8 -*-

from old_alg.alg_bp_old import TestBP
# from new_alg.alg_bp import TestBP
# from new_alg.try_except import TryExcept


def bp():
    """
    Вариант запуска старых алгоритмов
    :return:
    """
    test_bp = TestBP()
    test_bp.full_test_bp()


# def bp():
#     """
#     Вариант запуска новых алгоритмов
#     :return:
#     """
#     try_except = TryExcept()
#     test_bp = TestBP()
#     try_except.full_start_test(test_bp.st_test_bp, None, 0)


if __name__ == "__main__":
    bp()
