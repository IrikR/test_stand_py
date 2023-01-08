"""

"""

__all__ = ['ModbusConnectException', 'HardwareException']


class ModbusConnectException(Exception):
    """Вываливается когда нет связи по modbus"""
    pass


class HardwareException(Exception):
    """Вываливается при неисправности стенда"""
    pass
