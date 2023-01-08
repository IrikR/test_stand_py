#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__all__ = ["my_msg_3"]

import PySimpleGUI as sg


def my_msg_3(msg: str, bgcolor='#37474F', btncolor='#2D3D45', fontcolor='#1F1F1F'):
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
    font = ('Arial', 16)

    layout = [
            [sg.Text(msg, size=(60, 5), justification='center', font=font, background_color=bg_color)],
            [sg.Button('Ok', font=font, size=16, button_color=btncolor, fontcolor=fontcolor),
             sg.Button('Отмена', font=font, size=16, button_color=btncolor),
             sg.Button('Пропустить',  font=font, size=16, button_color=btncolor)]
        ]
    window = sg.Window('Внимание!', layout, element_justification='c', background_color=bg_color,
                       keep_on_top=True, use_default_focus=True)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Ok' or event == 'Отмена' or event == 'Пропустить':
            break

    window.close()

    if event == 'Ok':
        return 0
    elif event == 'Отмена':
        return 1
    elif event == 'Пропустить':
        return 2
    elif event == sg.WIN_CLOSED:
        return 1
