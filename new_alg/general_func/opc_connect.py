# # -*- coding: utf-8 -*-
# """
#
# """
#
# __all__ = ["ConnectOPC"]
#
# from OpenOPC import client
#
#
# class ConnectOPC:
#     # _instance = None
#     # __instance = None
#
#     _instances = None
#
#     # def __new__(cls, *args, **kwargs):
#     #     if cls not in cls._instances:
#     #         instance = super().__new__(cls)
#     #         cls._instances[cls] = instance
#     #     return cls._instances[cls]
#
#     def __new__(cls, *args, **kwargs):
#         if cls._instances is None:
#             # print(cls)
#             cls._instances = super().__new__(cls)
#             # print(cls._instances)
#
#         return cls._instances
#
#     # def __call__(cls, *args, **kwargs):
#     #     if cls not in cls._instances:
#     #         cls._instances[cls] = super(ConnectOPC, cls).__call__(*args, **kwargs)
#     #     return cls._instances[cls]
#     def __del__(self):
#         ConnectOPC._instances = None
#
#     def __init__(self):
#         # super().__init__()
#         # print(__name__)
#         self.opc = client()
#         self.opc.connect('arOPC.arOpcServer.1')
#
#     def opc_conn(self):
#         return self.opc
#
#     def opc_close(self):
#         self.opc.close('arOPC.arOpcServer.1')
#
#     def opc_read(self):
#         self.opc.read()
#
