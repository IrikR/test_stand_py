# -*- coding: utf-8 -*-

__all__ = ["CLILog"]

import ctypes
from datetime import datetime


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

    def lev_debug(self, msg: str, msg_color: [int, str]):
        if self.log == "debug":
            if msg_color == 7 or msg_color == 'gray':
                # серый
                print(f"\033[37m [{datetime.time(datetime.now())}] {self.name}: \033[37m {msg}")
            else:
                # черный, если пришел неизвестный аргумент
                print(f"\033[37m [{datetime.time(datetime.now())}] {self.name}: \033[0;0m {msg}")
        else:
            pass

    def lev_info(self, msg: str, msg_color: [int, str]):
        if self.log == "info" or self.log == "debug":
            if msg_color == 2 or msg_color == 'green':
                # зеленый green
                print(f"\033[37m [{datetime.time(datetime.now())}] {self.name}: \033[32m {msg}")
            elif msg_color == 3 or msg_color == 'orange':
                # оранжевый orange
                print(f"\033[37m [{datetime.time(datetime.now())}] {self.name}: \033[33m {msg}")
            elif msg_color == 4 or msg_color == 'blue':
                # синий blue
                print(f"\033[37m [{datetime.time(datetime.now())}] {self.name}: \033[34m {msg}")
            elif msg_color == 5 or msg_color == 'purple':
                # фиолетовый purple
                print(f"\033[37m [{datetime.time(datetime.now())}] {self.name}: \033[35m {msg}")
            elif msg_color == 6 or msg_color == 'skyblue':
                # голубой blue
                print(f"\033[37m [{datetime.time(datetime.now())}] {self.name}: \033[36m {msg}")
            else:
                # черный, если пришел неизвестный аргумент
                print(f"\033[37m [{datetime.time(datetime.now())}] {self.name}: \033[0;0m {msg}")
        else:
            pass

    def lev_warning(self, msg: str, msg_color: [int, str]) -> None:
        """
        red - для неисправности
        orange - для измерений
        blue - для управления реле
        green - для исправности
        purple - для процедур
        skyblue - для сухих контактов
        gray - для основного текста
        :param msg: str
        :param msg_color: int, str
        :return: string
        """

        if self.log == "warning" or self.log == "info" or self.log == "debug":
            if msg_color == 1 or msg_color == 'red':
                # красный Red
                print(f"\033[37m [{datetime.time(datetime.now())}] {self.name}: \033[31m {msg}")
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
