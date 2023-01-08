#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__all__ = ["my_msg_2"]

import PySimpleGUI as sg


def my_msg_2(msg: str):

    font = ('Arial', 15)
    layout = [
            [sg.Text(msg, size=(60, 5), justification='center', font=font, background_color='#37474F')],
            [sg.Button('Ok', font=font, size=16, button_color='#2D3D45'),
             sg.Button('Отмена', font=font, size=16, button_color='#2D3D45'),
             sg.Button('Пропустить',  font=font, size=16, button_color='#2D3D45')]
        ]
    window = sg.Window('Внимание!', layout, element_justification='c', background_color='#37474F',
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
