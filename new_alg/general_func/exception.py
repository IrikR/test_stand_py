# -*- coding: utf-8 -*-
"""
Дополнительные методы исключений
    ModbusConnectException - для ошибок при соединении и считывании из OPC сервера
    HardwareException - для ошибок при неисправности стенда

"""

__all__ = ["ModbusConnectException", "HardwareException", "MySQLException"]


class ModbusConnectException(Exception):
    """Вываливается когда нет связи по modbus"""
    pass


class HardwareException(Exception):
    """Вываливается при неисправности стенда"""
    pass


class MySQLException(Exception):
    """Вываливается при отсутствии связи с БД"""
    pass