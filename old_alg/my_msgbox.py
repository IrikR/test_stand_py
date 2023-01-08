#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__all__ = ["my_msg"]

import PySimpleGUI as sg


def my_msg(msg: str, bgcolor='#37474F'):
    """
    Окно для взаимодействия пользователя с алгоритмом проверки.
    По умолчанию цвет окна темно серый #37474F
    :param msg: текст который необходимо вывести в окне
    :param bgcolor: 'green': '#1E8C1E', 'darkgrey': '#37474F', 'red': '#A61E1E', 'yellow': '#CEFF00',
                    'blue': '#0FC0FC', 'purple': '#BA55D3', 'orange': '#E78E00'
    :return: bool
    """
    dict_bgcolor = {'green': '#1E8C1E', 'darkgrey': '#37474F', 'red': '#A61E1E', 'yellow': '#CEFF00',
                    'blue': '#0FC0FC', 'purple': '#BA55D3', 'orange': '#E78E00'}
    if bgcolor.startswith('#'):
        bg_color = bgcolor
    else:
        bg_color = dict_bgcolor.get(bgcolor)
    font = ('Arial', 15)
    layout = [
            [sg.Text(msg, size=(60, 5), justification='center', font=font, background_color=bg_color)],
            [sg.Button('Ok', font=font, size=16, button_color='#2D3D45', focus=True),
             sg.Button('Отмена', font=font, size=16, button_color='#2D3D45')]
        ]
    window = sg.Window('Внимание!', layout, element_justification='c', background_color=bg_color,
                       keep_on_top=True, use_default_focus=True)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Ok' or event == 'Отмена':
            break

    window.close()

    if event == 'Ok':
        return True
    elif event == 'Отмена':
        return False
    elif event == sg.WIN_CLOSED:
        return False
