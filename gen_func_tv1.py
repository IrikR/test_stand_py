#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from gen_mb_client import CtrlKL
from gen_func_utils import ResetRelay

__all__ = ["PervObmTV1", "VtorObmTV1"]


class PervObmTV1(object):
    """
    Включение первичной обмотки в зависимости от напряжения
    """

    def __init__(self):
        self.ctrl_kl = CtrlKL()
        self.reset = ResetRelay()
        self.logger = logging.getLogger(__name__)

    def perv_obm_tv1(self, calc_vol: float = 0.0):

        if calc_vol < 3.67:
            self.logger.debug(f"перв. обм. 1: на вход получили: {calc_vol:.2f}, "
                              f"< 3.67: отключение всех реле первичной обмотки")
            self.reset.sbros_perv_obm()
        elif 3.67 <= calc_vol < 3.89:
            self.logger.debug(f"перв. обм. 1: на вход получили: {calc_vol:.2f}, 3.67 <= < 3.89: KL38 == True")
            self.ctrl_kl.ctrl_relay('KL38', True)
        elif 3.89 <= calc_vol < 4.11:
            self.logger.debug(f"перв. обм. 2: на вход получили: {calc_vol:.2f}, 3.89 <= < 4.11: KL39 == True")
            self.ctrl_kl.ctrl_relay('KL39', True)
        elif 4.11 <= calc_vol < 4.35:
            self.logger.debug(f"перв. обм. 3: на вход получили: {calc_vol:.2f}, 4.11 <= < 4.35: KL40 == True")
            self.ctrl_kl.ctrl_relay('KL40', True)
        elif 4.35 <= calc_vol < 4.57:
            self.logger.debug(f"перв. обм. 4: на вход получили: {calc_vol:.2f}, 4.35 <= < 4.57: KL41 == True")
            self.ctrl_kl.ctrl_relay('KL41', True)
        elif 4.57 <= calc_vol < 4.77:
            self.logger.debug(f"перв. обм. 5: на вход получили: {calc_vol:.2f}, 4.57 <= < 4.77: KL42 == True")
            self.ctrl_kl.ctrl_relay('KL42', True)
        elif 4.77 <= calc_vol < 5.03:
            self.logger.debug(f"перв. обм. 6: на вход получили: {calc_vol:.2f}, 4.77 <= < 5.03: KL43 == True")
            self.ctrl_kl.ctrl_relay('KL43', True)
        elif 5.03 <= calc_vol < 5.25:
            self.logger.debug(f"перв. обм. 7: на вход получили: {calc_vol:.2f}, 5.03 <= < 5.25: KL44 == True")
            self.ctrl_kl.ctrl_relay('KL44', True)
        elif 5.25 <= calc_vol < 5.48:
            self.logger.debug(f"перв. обм. 8: на вход получили: {calc_vol:.2f}, 5.25 <= < 5.48: KL45 == True")
            self.ctrl_kl.ctrl_relay('KL45', True)
        elif 5.48 <= calc_vol < 5.71:
            self.logger.debug(f"перв. обм. 9: на вход получили: {calc_vol:.2f}, 5.48 <= < 5.71: KL46 == True")
            self.ctrl_kl.ctrl_relay('KL46', True)
        elif 5.71 <= calc_vol < 5.97:
            self.logger.debug(f"перв. обм. 10: на вход получили: {calc_vol:.2f}, 5.71 <= < 5.97: KL47 == True")
            self.ctrl_kl.ctrl_relay('KL47', True)
        elif 5.97 <= calc_vol < 6.31:
            self.logger.debug(f"перв. обм. 11: на вход получили: {calc_vol:.2f}, 5.97 <= < 6.31: KL38 == True")
            self.ctrl_kl.ctrl_relay('KL38', True)
        elif 6.31 <= calc_vol < 6.68:
            self.logger.debug(f"перв. обм. 12: на вход получили: {calc_vol:.2f}, 6.31 <= < 6.68: KL39 == True")
            self.ctrl_kl.ctrl_relay('KL39', True)
        elif 6.68 <= calc_vol < 7.06:
            self.logger.debug(f"перв. обм. 13: на вход получили: {calc_vol:.2f}, 6.68 <= < 7.06: KL40 == True")
            self.ctrl_kl.ctrl_relay('KL40', True)
        elif 7.06 <= calc_vol < 7.43:
            self.logger.debug(f"перв. обм. 14: на вход получили: {calc_vol:.2f}, 7.06 <= < 7.43: KL41 == True")
            self.ctrl_kl.ctrl_relay('KL41', True)
        elif 7.43 <= calc_vol < 7.75:
            self.logger.debug(f"перв. обм. 15: на вход получили: {calc_vol:.2f}, 7.43 <= < 7.75: KL42 == True")
            self.ctrl_kl.ctrl_relay('KL42', True)
        elif 7.75 <= calc_vol < 8.17:
            self.logger.debug(f"перв. обм. 16: на вход получили: {calc_vol:.2f}, 7.75 <= < 8.17: KL43 == True")
            self.ctrl_kl.ctrl_relay('KL43', True)
        elif 8.17 <= calc_vol < 8.54:
            self.logger.debug(f"перв. обм. 17: на вход получили: {calc_vol:.2f}, 8.17 <= < 8.54: KL44 == True")
            self.ctrl_kl.ctrl_relay('KL44', True)
        elif 8.54 <= calc_vol < 8.91:
            self.logger.debug(f"перв. обм. 18: на вход получили: {calc_vol:.2f}, 8.54 <= < 8.91: KL45 == True")
            self.ctrl_kl.ctrl_relay('KL45', True)
        elif 8.91 <= calc_vol < 9.29:
            self.logger.debug(f"перв. обм. 19: на вход получили: {calc_vol:.2f}, 8.91 <= < 9.29: KL46 == True")
            self.ctrl_kl.ctrl_relay('KL46', True)
        elif 9.29 <= calc_vol < 9.65:
            self.logger.debug(f"перв. обм. 20: на вход получили: {calc_vol:.2f}, 9.29 <= < 9.65: KL47 == True")
            self.ctrl_kl.ctrl_relay('KL47', True)
        elif 9.65 <= calc_vol < 10.20:
            self.logger.debug(f"перв. обм. 21: на вход получили: {calc_vol:.2f}, 9.65 <= < 10.20: KL38 == True")
            self.ctrl_kl.ctrl_relay('KL38', True)
        elif 10.20 <= calc_vol < 10.79:
            self.logger.debug(f"перв. обм. 22: на вход получили: {calc_vol:.2f}, 10.20 <= < 10.79: KL39 == True")
            self.ctrl_kl.ctrl_relay('KL39', True)
        elif 10.79 <= calc_vol < 11.41:
            self.logger.debug(f"перв. обм. 23: на вход получили: {calc_vol:.2f}, 10.79 <= < 11.41: KL40 == True")
            self.ctrl_kl.ctrl_relay('KL40', True)
        elif 11.41 <= calc_vol < 12.0:
            self.logger.debug(f"перв. обм. 24: на вход получили: {calc_vol:.2f}, 11.41 <= < 12.0: KL41 == True")
            self.ctrl_kl.ctrl_relay('KL41', True)
        elif 12.0 <= calc_vol < 12.52:
            self.logger.debug(f"перв. обм. 25: на вход получили: {calc_vol:.2f}, 12.0 <= < 12.52: KL42 == True")
            self.ctrl_kl.ctrl_relay('KL42', True)
        elif 12.52 <= calc_vol < 13.2:
            self.logger.debug(f"перв. обм. 26: на вход получили: {calc_vol:.2f}, 12.52 <= < 13.2: KL43 == True")
            self.ctrl_kl.ctrl_relay('KL43', True)
        elif 13.2 <= calc_vol < 13.79:
            self.logger.debug(f"перв. обм. 27: на вход получили: {calc_vol:.2f}, 13.2 <= < 13.79: KL44 == True")
            self.ctrl_kl.ctrl_relay('KL44', True)
        elif 13.79 <= calc_vol < 14.39:
            self.logger.debug(f"перв. обм. 28: на вход получили: {calc_vol:.2f}, 13.79 <= < 14.39: KL45 == True")
            self.ctrl_kl.ctrl_relay('KL45', True)
        elif 14.39 <= calc_vol < 15.0:
            self.logger.debug(f"перв. обм. 29: на вход получили: {calc_vol:.2f}, 14.39 <= < 15.0: KL46 == True")
            self.ctrl_kl.ctrl_relay('KL46', True)
        elif 15.0 <= calc_vol < 15.16:
            self.logger.debug(f"перв. обм. 30: на вход получили: {calc_vol:.2f}, 15.0 <= < 15.16: KL47 == True")
            self.ctrl_kl.ctrl_relay('KL47', True)
        elif 15.16 <= calc_vol < 16.03:
            self.logger.debug(f"перв. обм. 31: на вход получили: {calc_vol:.2f}, 15.16 <= < 16.03: KL38 == True")
            self.ctrl_kl.ctrl_relay('KL38', True)
        elif 16.03 <= calc_vol < 16.96:
            self.logger.debug(f"перв. обм. 32: на вход получили: {calc_vol:.2f}, 16.03 <= < 16.96: KL39 == True")
            self.ctrl_kl.ctrl_relay('KL39', True)
        elif 16.96 <= calc_vol < 17.93:
            self.logger.debug(f"перв. обм. 33: на вход получили: {calc_vol:.2f}, 16.96 <= < 17.93: KL40 == True")
            self.ctrl_kl.ctrl_relay('KL40', True)
        elif 17.93 <= calc_vol < 18.86:
            self.logger.debug(f"перв. обм. 34: на вход получили: {calc_vol:.2f}, 17.93 <= < 18.86: KL41 == True")
            self.ctrl_kl.ctrl_relay('KL41', True)
        elif 18.86 <= calc_vol < 19.67:
            self.logger.debug(f"перв. обм. 35: на вход получили: {calc_vol:.2f}, 18.86 <= < 19.67: KL42 == True")
            self.ctrl_kl.ctrl_relay('KL42', True)
        elif 19.67 <= calc_vol < 20.74:
            self.logger.debug(f"перв. обм. 36: на вход получили: {calc_vol:.2f}, 19.67 <= < 20.74: KL43 == True")
            self.ctrl_kl.ctrl_relay('KL43', True)
        elif 20.74 <= calc_vol < 21.67:
            self.logger.debug(f"перв. обм. 37: на вход получили: {calc_vol:.2f}, 20.74 <= < 21.67: KL44 == True")
            self.ctrl_kl.ctrl_relay('KL44', True)
        elif 21.67 <= calc_vol < 22.62:
            self.logger.debug(f"перв. обм. 38: на вход получили: {calc_vol:.2f}, 21.67 <= < 22.62: KL45 == True")
            self.ctrl_kl.ctrl_relay('KL45', True)
        elif 22.62 <= calc_vol < 23.57:
            self.logger.debug(f"перв. обм. 39: на вход получили: {calc_vol:.2f}, 22.62 <= < 23.57: KL46 == True")
            self.ctrl_kl.ctrl_relay('KL46', True)
        elif 23.57 <= calc_vol < 23.88:
            self.logger.debug(f"перв. обм. 40: на вход получили: {calc_vol:.2f}, 23.57 <= < 23.88: KL47 == True")
            self.ctrl_kl.ctrl_relay('KL47', True)
        elif 23.88 <= calc_vol < 25.25:
            self.logger.debug(f"перв. обм. 41: на вход получили: {calc_vol:.2f}, 23.88 <= < 25.25: KL38 == True")
            self.ctrl_kl.ctrl_relay('KL38', True)
        elif 25.25 <= calc_vol < 26.73:
            self.logger.debug(f"перв. обм. 42: на вход получили: {calc_vol:.2f}, 25.25 <= < 26.73: KL39 == True")
            self.ctrl_kl.ctrl_relay('KL39', True)
        elif 26.73 <= calc_vol < 28.25:
            self.logger.debug(f"перв. обм. 43: на вход получили: {calc_vol:.2f}, 26.73 <= < 28.25: KL40 == True")
            self.ctrl_kl.ctrl_relay('KL40', True)
        elif 28.25 <= calc_vol < 29.71:
            self.logger.debug(f"перв. обм. 44: на вход получили: {calc_vol:.2f}, 28.25 <= < 29.71: KL41 == True")
            self.ctrl_kl.ctrl_relay('KL41', True)
        elif 29.71 <= calc_vol < 31.0:
            self.logger.debug(f"перв. обм. 45: на вход получили: {calc_vol:.2f}, 29.71 <= < 31.0: KL42 == True")
            self.ctrl_kl.ctrl_relay('KL42', True)
        elif 31.0 <= calc_vol < 32.69:
            self.logger.debug(f"перв. обм. 46: на вход получили: {calc_vol:.2f}, 31.0 <= < 32.69: KL43 == True")
            self.ctrl_kl.ctrl_relay('KL43', True)
        elif 32.69 <= calc_vol < 34.15:
            self.logger.debug(f"перв. обм. 47: на вход получили: {calc_vol:.2f}, 32.69 <= < 34.15: KL44 == True")
            self.ctrl_kl.ctrl_relay('KL44', True)
        elif 34.15 <= calc_vol < 35.64:
            self.logger.debug(f"перв. обм. 48: на вход получили: {calc_vol:.2f}, 34.15 <= < 35.64: KL45 == True")
            self.ctrl_kl.ctrl_relay('KL45', True)
        elif 35.64 <= calc_vol < 37.14:
            self.logger.debug(f"перв. обм. 49: на вход получили: {calc_vol:.2f}, 35.64 <= < 37.14: KL46 == True")
            self.ctrl_kl.ctrl_relay('KL46', True)
        elif 37.14 <= calc_vol < 37.66:
            self.logger.debug(f"перв. обм. 50: на вход получили: {calc_vol:.2f}, 37.14 <= < 37.66: KL47 == True")
            self.ctrl_kl.ctrl_relay('KL47', True)
        elif 37.66 <= calc_vol < 39.82:
            self.logger.debug(f"перв. обм. 51: на вход получили: {calc_vol:.2f}, 37.66 <= < 39.82: KL38 == True")
            self.ctrl_kl.ctrl_relay('KL38', True)
        elif 39.82 <= calc_vol < 42.15:
            self.logger.debug(f"перв. обм. 52: на вход получили: {calc_vol:.2f}, 39.82 <= < 42.15: KL39 == True")
            self.ctrl_kl.ctrl_relay('KL39', True)
        elif 42.15 <= calc_vol < 44.54:
            self.logger.debug(f"перв. обм. 53: на вход получили: {calc_vol:.2f}, 42.15 <= < 44.54: KL40 == True")
            self.ctrl_kl.ctrl_relay('KL40', True)
        elif 44.54 <= calc_vol < 46.86:
            self.logger.debug(f"перв. обм. 54: на вход получили: {calc_vol:.2f}, 44.54 <= < 46.86: KL41 == True")
            self.ctrl_kl.ctrl_relay('KL41', True)
        elif 46.86 <= calc_vol < 48.89:
            self.logger.debug(f"перв. обм. 55: на вход получили: {calc_vol:.2f}, 46.86 <= < 48.89: KL42 == True")
            self.ctrl_kl.ctrl_relay('KL42', True)
        elif 48.89 <= calc_vol < 51.54:
            self.logger.debug(f"перв. обм. 56: на вход получили: {calc_vol:.2f}, 48.89 <= < 51.54: KL43 == True")
            self.ctrl_kl.ctrl_relay('KL43', True)
        elif 51.54 <= calc_vol < 53.85:
            self.logger.debug(f"перв. обм. 57: на вход получили: {calc_vol:.2f}, 51.54 <= < 53.85: KL44 == True")
            self.ctrl_kl.ctrl_relay('KL44', True)
        elif 53.85 <= calc_vol < 56.2:
            self.logger.debug(f"перв. обм. 58: на вход получили: {calc_vol:.2f}, 53.85 <= < 56.2: KL45 == True")
            self.ctrl_kl.ctrl_relay('KL45', True)
        elif 56.2 <= calc_vol < 58.57:
            self.logger.debug(f"перв. обм. 59: на вход получили: {calc_vol:.2f}, 56.2 <= < 58.57: KL46 == True")
            self.ctrl_kl.ctrl_relay('KL46', True)
        elif 58.57 <= calc_vol < 59.71:
            self.logger.debug(f"перв. обм. 60: на вход получили: {calc_vol:.2f}, 58.57 <= < 59.71: KL47 == True")
            self.ctrl_kl.ctrl_relay('KL47', True)
        elif 59.71 <= calc_vol < 63.13:
            self.logger.debug(f"перв. обм. 61: на вход получили: {calc_vol:.2f}, 59.71 <= < 63.13: KL38 == True")
            self.ctrl_kl.ctrl_relay('KL38', True)
        elif 63.13 <= calc_vol < 66.82:
            self.logger.debug(f"перв. обм. 62: на вход получили: {calc_vol:.2f}, 63.13 <= < 66.82: KL39 == True")
            self.ctrl_kl.ctrl_relay('KL39', True)
        elif 66.82 <= calc_vol < 70.62:
            self.logger.debug(f"перв. обм. 63: на вход получили: {calc_vol:.2f}, 66.82 <= < 70.62: KL40 == True")
            self.ctrl_kl.ctrl_relay('KL40', True)
        elif 70.62 <= calc_vol < 74.29:
            self.logger.debug(f"перв. обм. 64: на вход получили: {calc_vol:.2f}, 70.62 <= < 74.29: KL41 == True")
            self.ctrl_kl.ctrl_relay('KL41', True)
        elif 74.29 <= calc_vol < 77.51:
            self.logger.debug(f"перв. обм. 65: на вход получили: {calc_vol:.2f}, 74.29 <= < 77.51: KL42 == True")
            self.ctrl_kl.ctrl_relay('KL42', True)
        elif 77.51 <= calc_vol < 81.71:
            self.logger.debug(f"перв. обм. 66: на вход получили: {calc_vol:.2f}, 77.51 <= < 81.71: KL43 == True")
            self.ctrl_kl.ctrl_relay('KL43', True)
        elif 81.71 <= calc_vol < 85.37:
            self.logger.debug(f"перв. обм. 67: на вход получили: {calc_vol:.2f}, 81.71 <= < 85.37: KL44 == True")
            self.ctrl_kl.ctrl_relay('KL44', True)
        elif 85.37 <= calc_vol < 89.1:
            self.logger.debug(f"перв. обм. 68: на вход получили: {calc_vol:.2f}, 85.37 <= < 89.1: KL45 == True")
            self.ctrl_kl.ctrl_relay('KL45', True)
        elif 89.1 <= calc_vol < 92.86:
            self.logger.debug(f"перв. обм. 69: на вход получили: {calc_vol:.2f}, 89.1 <= < 92.86: KL46 == True")
            self.ctrl_kl.ctrl_relay('KL46', True)
        elif 92.86 <= calc_vol < 93.7:
            self.logger.debug(f"перв. обм. 70: на вход получили: {calc_vol:.2f}, 92.86 <= < 93.7: KL47 == True")
            self.ctrl_kl.ctrl_relay('KL47', True)
        elif 93.7 <= calc_vol < 99.07:
            self.logger.debug(f"перв. обм. 71: на вход получили: {calc_vol:.2f}, 93.7 <= < 99.07: KL38 == True")
            self.ctrl_kl.ctrl_relay('KL38', True)
        elif 99.07 <= calc_vol < 104.86:
            self.logger.debug(f"перв. обм. 72: на вход получили: {calc_vol:.2f}, 99.07 <= < 104.86: KL39 == True")
            self.ctrl_kl.ctrl_relay('KL39', True)
        elif 104.86 <= calc_vol < 110.81:
            self.logger.debug(f"перв. обм. 73: на вход получили: {calc_vol:.2f}, 104.86 <= < 110.81: KL40 == True")
            self.ctrl_kl.ctrl_relay('KL40', True)
        elif 110.81 <= calc_vol < 116.57:
            self.logger.debug(f"перв. обм. 74: на вход получили: {calc_vol:.2f}, 110.81 <= < 116.57: KL41 == True")
            self.ctrl_kl.ctrl_relay('KL41', True)
        elif 116.57 <= calc_vol < 121.63:
            self.logger.debug(f"перв. обм. 75: на вход получили: {calc_vol:.2f}, 116.57 <= < 121.63: KL42 == True")
            self.ctrl_kl.ctrl_relay('KL42', True)
        elif 121.63 <= calc_vol < 128.23:
            self.logger.debug(f"перв. обм. 76: на вход получили: {calc_vol:.2f}, 121.63 <= < 128.23: KL43 == True")
            self.ctrl_kl.ctrl_relay('KL43', True)
        elif 128.23 <= calc_vol < 133.97:
            self.logger.debug(f"перв. обм. 77: на вход получили: {calc_vol:.2f}, 128.23 <= < 133.97: KL44 == True")
            self.ctrl_kl.ctrl_relay('KL44', True)
        elif 133.97 <= calc_vol < 139.81:
            self.logger.debug(f"перв. обм. 78: на вход получили: {calc_vol:.2f}, 133.97 <= < 139.81: KL45 == True")
            self.ctrl_kl.ctrl_relay('KL45', True)
        elif 139.81 <= calc_vol < 145.71:
            self.logger.debug(f"перв. обм. 79: на вход получили: {calc_vol:.2f}, 139.81 <= < 145.71: KL46 == True")
            self.ctrl_kl.ctrl_relay('KL46', True)
        elif 145.71 <= calc_vol < 146.51:
            self.logger.debug(f"перв. обм. 80: на вход получили: {calc_vol:.2f}, 145.71 <= < 146.51: KL47 == True")
            self.ctrl_kl.ctrl_relay('KL47', True)
        elif 146.51 <= calc_vol < 154.92:
            self.logger.debug(f"перв. обм. 81: на вход получили: {calc_vol:.2f}, 146.51 <= < 154.92: KL38 == True")
            self.ctrl_kl.ctrl_relay('KL38', True)
        elif 154.92 <= calc_vol < 156.16:
            self.logger.debug(f"перв. обм. 82: на вход получили: {calc_vol:.2f}, 154.92 <= < 156.16: KL39 == True")
            self.ctrl_kl.ctrl_relay('KL39', True)
        elif 156.16 <= calc_vol < 163.97:
            self.logger.debug(f"перв. обм. 83: на вход получили: {calc_vol:.2f}, 156.16 <= < 163.97: KL38 == True")
            self.ctrl_kl.ctrl_relay('KL38', True)
        elif 163.97 <= calc_vol < 165.12:
            self.logger.debug(f"перв. обм. 84: на вход получили: {calc_vol:.2f}, 163.97 <= < 165.12: KL40 == True")
            self.ctrl_kl.ctrl_relay('KL40', True)
        elif 165.12 <= calc_vol < 173.28:
            self.logger.debug(f"перв. обм. 85: на вход получили: {calc_vol:.2f}, 165.12 <= < 173.28: KL39 == True")
            self.ctrl_kl.ctrl_relay('KL39', True)
        elif 173.28 <= calc_vol < 174.77:
            self.logger.debug(f"перв. обм. 86: на вход получили: {calc_vol:.2f}, 173.28 <= < 174.77: KL41 == True")
            self.ctrl_kl.ctrl_relay('KL41', True)
        elif 174.77 <= calc_vol < 180.04:
            self.logger.debug(f"перв. обм. 87: на вход получили: {calc_vol:.2f}, 174.77 <= < 180.04: KL40 == True")
            self.ctrl_kl.ctrl_relay('KL40', True)
        elif 180.04 <= calc_vol < 182.29:
            self.logger.debug(f"перв. обм. 88: на вход получили: {calc_vol:.2f}, 180.04 <= < 182.29: KL38 == True")
            self.ctrl_kl.ctrl_relay('KL38', True)
        elif 182.29 <= calc_vol < 184.69:
            self.logger.debug(f"перв. обм. 89: на вход получили: {calc_vol:.2f}, 182.29 <= < 184.69: KL42 == True")
            self.ctrl_kl.ctrl_relay('KL42', True)
        elif 184.69 <= calc_vol < 186.01:
            self.logger.debug(f"перв. обм. 90: на вход получили: {calc_vol:.2f}, 184.69 <= < 186.01: KL41 == True")
            self.ctrl_kl.ctrl_relay('KL41', True)
        elif 186.01 <= calc_vol < 190.19:
            self.logger.debug(f"перв. обм. 91: на вход получили: {calc_vol:.2f}, 186.01 <= < 190.19: KL38 == True")
            self.ctrl_kl.ctrl_relay('KL38', True)
        elif 190.19 <= calc_vol < 190.38:
            self.logger.debug(f"перв. обм. 92: на вход получили: {calc_vol:.2f}, 190.19 <= < 190.38: KL43 == True")
            self.ctrl_kl.ctrl_relay('KL43', True)
        elif 190.38 <= calc_vol < 194.29:
            self.logger.debug(f"перв. обм. 93: на вход получили: {calc_vol:.2f}, 190.38 <= < 194.29: KL39 == True")
            self.ctrl_kl.ctrl_relay('KL39', True)
        elif 194.29 <= calc_vol < 196.69:
            self.logger.debug(f"перв. обм. 94: на вход получили: {calc_vol:.2f}, 194.29 <= < 196.69: KL42 == True")
            self.ctrl_kl.ctrl_relay('KL42', True)
        elif 196.69 <= calc_vol < 200.51:
            self.logger.debug(f"перв. обм. 95: на вход получили: {calc_vol:.2f}, 196.69 <= < 200.51: KL39 == True")
            self.ctrl_kl.ctrl_relay('KL39', True)
        elif 200.51 <= calc_vol < 201.5:
            self.logger.debug(f"перв. обм. 96: на вход получили: {calc_vol:.2f}, 200.51 <= < 201.5: KL44 == True")
            self.ctrl_kl.ctrl_relay('KL44', True)
        elif 201.5 <= calc_vol < 202.71:
            self.logger.debug(f"перв. обм. 97: на вход получили: {calc_vol:.2f}, 201.5 <= < 202.71: KL40 == True")
            self.ctrl_kl.ctrl_relay('KL40', True)
        elif 202.71 <= calc_vol < 208.18:
            self.logger.debug(f"перв. обм. 98: на вход получили: {calc_vol:.2f}, 202.71 <= < 208.18: KL43 == True")
            self.ctrl_kl.ctrl_relay('KL43', True)
        elif 208.18 <= calc_vol < 209.49:
            self.logger.debug(f"перв. обм. 99: на вход получили: {calc_vol:.2f}, 208.18 <= < 209.49: KL40 == True")
            self.ctrl_kl.ctrl_relay('KL40', True)
        elif 209.49 <= calc_vol < 212.94:
            self.logger.debug(f"перв. обм. 100: на вход получили: {calc_vol:.2f}, 209.49 <= < 212.94: KL45 == True")
            self.ctrl_kl.ctrl_relay('KL45', True)
        elif 212.94 <= calc_vol < 213.71:
            self.logger.debug(f"перв. обм. 101: на вход получили: {calc_vol:.2f}, 212.94 <= < 213.71: KL41 == True")
            self.ctrl_kl.ctrl_relay('KL41', True)
        elif 213.71 <= calc_vol < 218.63:
            self.logger.debug(f"перв. обм. 102: на вход получили: {calc_vol:.2f}, 213.71 <= < 218.63: KL44 == True")
            self.ctrl_kl.ctrl_relay('KL44', True)
        elif 218.63 <= calc_vol < 220.0:
            self.logger.debug(f"перв. обм. 103: на вход получили: {calc_vol:.2f}, 218.63 <= < 220.0: KL46 == True")
            self.ctrl_kl.ctrl_relay('KL46', True)
        elif 220.0 <= calc_vol < 223.28:
            self.logger.debug(f"перв. обм. 104: на вход получили: {calc_vol:.2f}, 220.0 <= < 223.28: KL41 == True")
            self.ctrl_kl.ctrl_relay('KL41', True)
        elif 223.28 <= calc_vol < 224.0:
            self.logger.debug(f"перв. обм. 105: на вход получили: {calc_vol:.2f}, 223.28 <= < 224.0: KL45 == True")
            self.ctrl_kl.ctrl_relay('KL45', True)
        elif 224.0 <= calc_vol < 227.86:
            self.logger.debug(f"перв. обм. 106: на вход получили: {calc_vol:.2f}, 224.0 <= < 227.86: KL42 == True")
            self.ctrl_kl.ctrl_relay('KL42', True)
        elif 227.86 <= calc_vol < 231.43:
            self.logger.debug(f"перв. обм. 107: на вход получили: {calc_vol:.2f}, 227.86 <= < 231.43: KL47 == True")
            self.ctrl_kl.ctrl_relay('KL47', True)
        elif 231.43 <= calc_vol < 233.02:
            self.logger.debug(f"перв. обм. 108: на вход получили: {calc_vol:.2f}, 231.43 <= < 233.02: KL42 == True")
            self.ctrl_kl.ctrl_relay('KL42', True)
        elif 233.02 <= calc_vol < 233.71:
            self.logger.debug(f"перв. обм. 109: на вход получили: {calc_vol:.2f}, 233.02 <= < 233.71: KL46 == True")
            self.ctrl_kl.ctrl_relay('KL46', True)
        elif 233.71 <= calc_vol < 242.86:
            self.logger.debug(f"перв. обм. 110: на вход получили: {calc_vol:.2f}, 233.71 <= < 242.86: KL43 == True")
            self.ctrl_kl.ctrl_relay('KL43', True)
        elif 242.86 <= calc_vol < 246.4:
            self.logger.debug(f"перв. обм. 111: на вход получили: {calc_vol:.2f}, 242.86 <= < 246.4: KL47 == True")
            self.ctrl_kl.ctrl_relay('KL47', True)
        elif 246.4 <= calc_vol < 257.43:
            self.logger.debug(f"перв. обм. 112: на вход получили: {calc_vol:.2f}, 246.4 <= < 257.43: KL44 == True")
            self.ctrl_kl.ctrl_relay('KL44', True)
        elif 257.43 <= calc_vol < 268.66:
            self.logger.debug(f"перв. обм. 113: на вход получили: {calc_vol:.2f}, 257.43 <= < 268.66: KL45 == True")
            self.ctrl_kl.ctrl_relay('KL45', True)
        elif 268.66 <= calc_vol < 280.0:
            self.logger.debug(f"перв. обм. 114: на вход получили: {calc_vol:.2f}, 268.66 <= < 280.0: KL46 == True")
            self.ctrl_kl.ctrl_relay('KL46', True)
        elif 280.0 <= calc_vol < 289.29:
            self.logger.debug(f"перв. обм. 115: на вход получили: {calc_vol:.2f}, 280.0 <= < 289.29: KL47 == True")
            self.ctrl_kl.ctrl_relay('KL47', True)
        else:
            self.logger.debug(f"перв. обм. 116: на вход получили: {calc_vol:.2f}, "
                              f"отключение всех реле первичной обмотки")
            self.reset.sbros_perv_obm()


class VtorObmTV1(object):
    """
        Включение вторичной обмотки в зависимости от напряжения
    """

    def __init__(self):

        self.ctrl_kl = CtrlKL()
        self.reset = ResetRelay()
        self.logger = logging.getLogger(__name__)

    def vtor_obm_tv1(self, calc_vol: float = 0.0):

        if calc_vol < 3.66:
            self.logger.debug(f"втор. обм. 1: на вход получили: {calc_vol:.2f}, "
                              f"отключение всех реле втор. обмотки")
            self.reset.sbros_vtor_obm()
        elif 3.67 <= calc_vol <= 5.96:
            self.logger.debug(f"втор. обм. 2: на вход получили: {calc_vol:.2f}, 3.67 <= <= 5.96: KL59")
            self.ctrl_kl.ctrl_relay('KL59', True)
        elif 5.97 <= calc_vol <= 9.64:
            self.logger.debug(f"втор. обм. 3: на вход получили: {calc_vol:.2f}, 5.97 <= <= 9.64: KL58")
            self.ctrl_kl.ctrl_relay('KL58', True)
        elif 9.65 <= calc_vol <= 15.15:
            self.logger.debug(f"втор. обм. 4: на вход получили: {calc_vol:.2f}, 9.65 <= <= 15.15: KL57")
            self.ctrl_kl.ctrl_relay('KL57', True)
        elif 15.16 <= calc_vol <= 23.87:
            self.logger.debug(f"втор. обм. 5: на вход получили: {calc_vol:.2f}, 15.16 <= <= 23.87: KL56")
            self.ctrl_kl.ctrl_relay('KL56', True)
        elif 23.88 <= calc_vol <= 37.65:
            self.logger.debug(f"втор. обм. 6: на вход получили: {calc_vol:.2f}, 23.88 <= <= 37.65: KL55")
            self.ctrl_kl.ctrl_relay('KL55', True)
        elif 37.66 <= calc_vol <= 59.7:
            self.logger.debug(f"втор. обм. 7: на вход получили: {calc_vol:.2f}, 37.66 <= <= 59.7: KL54")
            self.ctrl_kl.ctrl_relay('KL54', True)
        elif 59.71 <= calc_vol <= 93.69:
            self.logger.debug(f"втор. обм. 8: на вход получили: {calc_vol:.2f}, 59.71 <= <= 93.69: KL53")
            self.ctrl_kl.ctrl_relay('KL53', True)
        elif 93.7 <= calc_vol <= 146.5:
            self.logger.debug(f"втор. обм. 9: на вход получили: {calc_vol:.2f}, 93.7 <= <= 146.5: KL52")
            self.ctrl_kl.ctrl_relay('KL52', True)
        elif 146.51 <= calc_vol <= 156.15:
            self.logger.debug(f"втор. обм. 10: на вход получили: {calc_vol:.2f}, 146.51 <= <= 156.15: KL51")
            self.ctrl_kl.ctrl_relay('KL51', True)
        elif 156.16 <= calc_vol <= 163.96:
            self.logger.debug(f"втор. обм. 11: на вход получили: {calc_vol:.2f}, 156.16 <= <= 163.96: KL50")
            self.ctrl_kl.ctrl_relay('KL50', True)
        elif 163.97 <= calc_vol <= 165.11:
            self.logger.debug(f"втор. обм. 12: на вход получили: {calc_vol:.2f}, 163.97 <= <= 165.11: KL51")
            self.ctrl_kl.ctrl_relay('KL51', True)
        elif 165.12 <= calc_vol <= 173.27:
            self.logger.debug(f"втор. обм. 13: на вход получили: {calc_vol:.2f}, 165.12 <= <= 173.27: KL50")
            self.ctrl_kl.ctrl_relay('KL50', True)
        elif 173.28 <= calc_vol <= 174.76:
            self.logger.debug(f"втор. обм. 14: на вход получили: {calc_vol:.2f}, 173.28 <= <= 174.76: KL51")
            self.ctrl_kl.ctrl_relay('KL51', True)
        elif 174.77 <= calc_vol <= 180.03:
            self.logger.debug(f"втор. обм. 15: на вход получили: {calc_vol:.2f}, 174.77 <= <= 180.03: KL50")
            self.ctrl_kl.ctrl_relay('KL50', True)
        elif 180.04 <= calc_vol <= 182.28:
            self.logger.debug(f"втор. обм. 16: на вход получили: {calc_vol:.2f}, 180.04 <= <= 182.28: KL49")
            self.ctrl_kl.ctrl_relay('KL49', True)
        elif 182.29 <= calc_vol <= 184.68:
            self.logger.debug(f"втор. обм. 17: на вход получили: {calc_vol:.2f}, 182.29 <= <= 184.68: KL51")
            self.ctrl_kl.ctrl_relay('KL51', True)
        elif 184.69 <= calc_vol <= 186.0:
            self.logger.debug(f"втор. обм. 18: на вход получили: {calc_vol:.2f}, 184.69 <= <= 186.0: KL50")
            self.ctrl_kl.ctrl_relay('KL50', True)
        elif 186.01 <= calc_vol <= 190.18:
            self.logger.debug(f"втор. обм. 19: на вход получили: {calc_vol:.2f}, 186.01 <= <= 190.18: KL48")
            self.ctrl_kl.ctrl_relay('KL48', True)
        elif 190.19 <= calc_vol <= 190.37:
            self.logger.debug(f"втор. обм. 20: на вход получили: {calc_vol:.2f}, 190.19 <= <= 190.37: KL51")
            self.ctrl_kl.ctrl_relay('KL51', True)
        elif 190.38 <= calc_vol <= 194.28:
            self.logger.debug(f"втор. обм. 21: на вход получили: {calc_vol:.2f}, 190.38 <= <= 194.28: KL49")
            self.ctrl_kl.ctrl_relay('KL49', True)
        elif 194.29 <= calc_vol <= 196.68:
            self.logger.debug(f"втор. обм. 22: на вход получили: {calc_vol:.2f}, 194.29 <= <= 196.68: KL50")
            self.ctrl_kl.ctrl_relay('KL50', True)
        elif 196.69 <= calc_vol <= 200.5:
            self.logger.debug(f"втор. обм. 23: на вход получили: {calc_vol:.2f}, 196.69 <= <= 200.5: KL48")
            self.ctrl_kl.ctrl_relay('KL48', True)
        elif 200.51 <= calc_vol <= 201.49:
            self.logger.debug(f"втор. обм. 24: на вход получили: {calc_vol:.2f}, 200.51 <= <= 201.49: KL51")
            self.ctrl_kl.ctrl_relay('KL51', True)
        elif 201.5 <= calc_vol <= 202.7:
            self.logger.debug(f"втор. обм. 25: на вход получили: {calc_vol:.2f}, 201.5 <= <= 202.7: KL49")
            self.ctrl_kl.ctrl_relay('KL49', True)
        elif 202.71 <= calc_vol <= 208.17:
            self.logger.debug(f"втор. обм. 26: на вход получили: {calc_vol:.2f}, 202.71 <= <= 208.17: KL50")
            self.ctrl_kl.ctrl_relay('KL50', True)
        elif 208.18 <= calc_vol <= 209.48:
            self.logger.debug(f"втор. обм. 27: на вход получили: {calc_vol:.2f}, 208.18 <= <= 209.48: KL48")
            self.ctrl_kl.ctrl_relay('KL48', True)
        elif 209.49 <= calc_vol <= 212.93:
            self.logger.debug(f"втор. обм. 28: на вход получили: {calc_vol:.2f}, 209.49 <= <= 212.93: KL51")
            self.ctrl_kl.ctrl_relay('KL51', True)
        elif 212.94 <= calc_vol <= 213.7:
            self.logger.debug(f"втор. обм. 29: на вход получили: {calc_vol:.2f}, 212.94 <= <= 213.7: KL49")
            self.ctrl_kl.ctrl_relay('KL49', True)
        elif 213.71 <= calc_vol <= 218.62:
            self.logger.debug(f"втор. обм. 30: на вход получили: {calc_vol:.2f}, 213.71 <= <= 218.62: KL50")
            self.ctrl_kl.ctrl_relay('KL50', True)
        elif 218.63 <= calc_vol <= 219.99:
            self.logger.debug(f"втор. обм. 31: на вход получили: {calc_vol:.2f}, 218.63 <= <= 219.99: KL51")
            self.ctrl_kl.ctrl_relay('KL51', True)
        elif 220.0 <= calc_vol <= 223.27:
            self.logger.debug(f"втор. обм. 32: на вход получили: {calc_vol:.2f}, 220.0 <= <= 223.27: KL48")
            self.ctrl_kl.ctrl_relay('KL48', True)
        elif 223.28 <= calc_vol <= 223.99:
            self.logger.debug(f"втор. обм. 33: на вход получили: {calc_vol:.2f}, 223.28 <= <= 223.99: KL50")
            self.ctrl_kl.ctrl_relay('KL50', True)
        elif 224.0 <= calc_vol < 227.87:
            self.logger.debug(f"втор. обм. 34: на вход получили: {calc_vol:.2f}, 224.0 <= < 227.87: KL49")
            self.ctrl_kl.ctrl_relay('KL49', True)
        elif 227.87 <= calc_vol <= 231.42:
            self.logger.debug(f"втор. обм. 35: на вход получили: {calc_vol:.2f}, 227.87 <= <= 231.42: KL51")
            self.ctrl_kl.ctrl_relay('KL51', True)
        elif 231.43 <= calc_vol <= 233.01:
            self.logger.debug(f"втор. обм. 36: на вход получили: {calc_vol:.2f}, 231.43 <= <= 233.01: KL48")
            self.ctrl_kl.ctrl_relay('KL48', True)
        elif 233.02 <= calc_vol <= 233.7:
            self.logger.debug(f"втор. обм. 37: на вход получили: {calc_vol:.2f}, 233.02 <= <= 233.7: KL50")
            self.ctrl_kl.ctrl_relay('KL50', True)
        elif 233.71 <= calc_vol <= 241.45:
            self.logger.debug(f"втор. обм. 38: на вход получили: {calc_vol:.2f}, 233.71 <= <= 241.45: KL49")
            self.ctrl_kl.ctrl_relay('KL49', True)
        elif 241.46 <= calc_vol <= 242.85:
            self.logger.debug(f"втор. обм. 39: на вход получили: {calc_vol:.2f}, 241.46 <= <= 242.85: KL48")
            self.ctrl_kl.ctrl_relay('KL48', True)
        elif 242.86 <= calc_vol <= 246.39:
            self.logger.debug(f"втор. обм. 40: на вход получили: {calc_vol:.2f}, 242.86 <= <= 246.39: KL50")
            self.ctrl_kl.ctrl_relay('KL50', True)
        elif 246.4 <= calc_vol <= 254.56:
            self.logger.debug(f"втор. обм. 41: на вход получили: {calc_vol:.2f}, 246.4 <= <= 254.56: KL49")
            self.ctrl_kl.ctrl_relay('KL49', True)
        elif 254.57 <= calc_vol <= 257.42:
            self.logger.debug(f"втор. обм. 42: на вход получили: {calc_vol:.2f}, 254.57 <= <= 257.42: KL48")
            self.ctrl_kl.ctrl_relay('KL48', True)
        elif 257.43 <= calc_vol <= 265.96:
            self.logger.debug(f"втор. обм. 43: на вход получили: {calc_vol:.2f}, 257.43 <= <= 265.96: KL49")
            self.ctrl_kl.ctrl_relay('KL49', True)
        elif 265.97 <= calc_vol <= 268.65:
            self.logger.debug(f"втор. обм. 44: на вход получили: {calc_vol:.2f}, 265.97 <= <= 268.65: KL48")
            self.ctrl_kl.ctrl_relay('KL48', True)
        elif 268.66 <= calc_vol <= 277.56:
            self.logger.debug(f"втор. обм. 45: на вход получили: {calc_vol:.2f}, 268.66 <= <= 277.56: KL49")
            self.ctrl_kl.ctrl_relay('KL49', True)
        elif 277.57 <= calc_vol <= 279.99:
            self.logger.debug(f"втор. обм. 46: на вход получили: {calc_vol:.2f}, 277.57 <= <= 279.99: KL48")
            self.ctrl_kl.ctrl_relay('KL48', True)
        elif 280.0 <= calc_vol <= 289.28:
            self.logger.debug(f"втор. обм. 47: на вход получили: {calc_vol:.2f}, 280.0 <= <= 289.28: KL49")
            self.ctrl_kl.ctrl_relay('KL49', True)
        elif 289.29 <= calc_vol:
            self.logger.debug(f"втор. обм. 48: на вход получили: {calc_vol:.2f}, 289.29 <= : KL48")
            self.ctrl_kl.ctrl_relay('KL48', True)
        else:
            self.logger.debug(f"втор. обм. 49: на вход получили: {calc_vol:.2f}, "
                              f"отключение всех реле втор. обмотки")
            self.reset.sbros_vtor_obm()
