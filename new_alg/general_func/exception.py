# -*- coding: utf-8 -*-
"""
Дополнительные методы исключений
    ModbusConnectException - для ошибок при соединений и считывании из OPC сервера
    HardwareException - для ошибок при неисправности стенда

"""

__all__ = ['ModbusConnectException', 'HardwareException']


class ModbusConnectException(Exception):
    """Вываливается когда нет связи по modbus"""
    pass


class HardwareException(Exception):
    """Вываливается при неисправности стенда"""
    pass
