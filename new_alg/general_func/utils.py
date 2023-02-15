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

        red - для неисправности
        orange - для измерений
        blue - для управления реле
        green - для исправности
        purple - для процедур
        skyblue - для сухих контактов
        gray - для основного текста
    """

    def __init__(self, log=None, name=__name__):
        self.log = log
        self.name = name
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

    def color_print(self, *args):
        color_level: dict = {"black": 30,
                             "red": 31,
                             "green": 32,
                             "orange": 33,
                             "blue": 34,
                             "purple": 35,
                             "skyblue": 36,
                             "gray": 37,
                             "reset": 0}
        msg, color_msg = args
        color = color_level[color_msg] if color_msg in color_level else 0
        print(f"\033[37m [{datetime.time(datetime.now())} [{self.log}] {self.name}] : \033[{color}m {msg}")

    def lev_debug(self, msg: str, msg_color: str) -> None:
        """
        Функция вывода сообщений в консоль уровня DEBUG
        params msg: сообщение
        params msg_color: цвет сообщения
        return
        """
        if self.log == "debug" or self.log is True:
            self.color_print(msg, msg_color)

    def lev_info(self, msg: str, msg_color: str) -> None:
        """
        Функция вывода сообщений в консоль уровня INFO
        params msg: сообщение
        params msg_color: цвет сообщения
        return
        """
        if self.log == "info" or self.log == "debug":
            self.color_print(msg, msg_color)

    def lev_warning(self, msg: str, msg_color: str) -> None:
        """
        Функция вывода сообщений в консоль уровня WARNING
        params msg: сообщение
        params msg_color: цвет сообщения
        return
        """
        if self.log == "warning" or self.log == "info" or self.log == "debug":
            self.color_print(msg, msg_color)

    @staticmethod
    def progress_bar(percent: int = 0, max_it: int = 100) -> None:
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
