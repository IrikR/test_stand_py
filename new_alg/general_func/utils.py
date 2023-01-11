#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ctypes
from datetime import datetime

# from .exception import *

__all__ = ["CLILog"]


class CLILog:
    """
        Вывод сообщений в консоль, с цветовой дифференциацией штанов
        Цвет        Текст   Фон
        Чёрный      30      40
        Красный     31      41
        Зелёный     32      42
        Жёлтый      33      43
        Синий       34      44
        Фиолетовый  35      45
        Бирюзовый   36      46
        Белый       37      47
    """

    def __init__(self, log=None, name=__name__):
        self.log = log
        self.name = name
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

    def log_msg(self, *args) -> None:
        """
        red - для неисправности
        orange - для измерений
        blue - для управления реле
        green - для исправности
        purple - для процедур
        skyblue - для сухих контактов
        gray - для основного текста
        :param args:
        :return: string
        """

        if self.log is True:
            msg, lev = args
            if lev == 1 or lev == 'red':
                # красный Red
                print(f"\033[37m [{datetime.time(datetime.now())}] {self.name}: \033[31m {msg}")
            elif lev == 2 or lev == 'green':
                # зеленый green
                print(f"\033[37m [{datetime.time(datetime.now())}] {self.name}: \033[32m {msg}")
            elif lev == 3 or lev == 'orange':
                # оранжевый orange
                print(f"\033[37m [{datetime.time(datetime.now())}] {self.name}: \033[33m {msg}")
            elif lev == 4 or lev == 'blue':
                # синий blue
                print(f"\033[37m [{datetime.time(datetime.now())}] {self.name}: \033[34m {msg}")
            elif lev == 5 or lev == 'purple':
                # фиолетовый purple
                print(f"\033[37m [{datetime.time(datetime.now())}] {self.name}: \033[35m {msg}")
            elif lev == 6 or lev == 'skyblue':
                # голубой blue
                print(f"\033[37m [{datetime.time(datetime.now())}] {self.name}: \033[36m {msg}")
            elif lev == 7 or lev == 'gray':
                # серый
                print(f"\033[37m [{datetime.time(datetime.now())}] {self.name}: \033[37m {msg}")
            else:
                # черный, если пришел неизвестный аргумент
                print(f"\033[37m [{datetime.time(datetime.now())}] {self.name}: \033[0;0m {msg}")
        else:
            pass

    @staticmethod
    def progress_bar(percent: int=0, max_it: int=100) -> None:
        """
        Функция предназначена для отображения в терминале прогресса выполнения.
        :param percent: Текущая итерация
        :param max_it: Максимум итераций
        """
        width = 60
        percent_tek = 100 / max_it * percent
        left = width * percent // max_it
        right = width - left
        print('\r[', '#' * left, ' ' * right, ']',
              f' {percent_tek:.0f}%',
              sep='', end='', flush=True)
