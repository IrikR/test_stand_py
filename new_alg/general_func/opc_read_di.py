# # -*- coding: utf-8 -*-
# """
# Метод опроса дискретных входов контроллера через OPC сервер.
# В классе ConnectOPC создается подключение к серверу и происходит групповой опрос всех дискретных входов.
# Класс ReadDIFromOPC наследуется от ConnectOPC, и в функции subtest_read_di происходит обработка считанных значений
# и выдача результата.
#
# """
# __all__ = ["ReadDIFromOPC", "ConnectOPC"]
#
# import logging
#
# # from OpenOPC import client
#
# from .database import MySQLConnect
# from .exception import ModbusConnectException
# from .rw_result import RWError, WriteCondition
# from .utils import CLILog
# from .opc_connect import ConnectOPC
#
#
# class ReadDIFromOPC(ConnectOPC):
#     """
#         Подключение к OPC серверу.
#         Список тегов дискретных входов контроллера:
#             'in_a0': 'Выходы.inputs.inp_00', 'in_a1': 'Выходы.inputs.inp_01',
#             'in_a2': 'Выходы.inputs.inp_02', 'in_a3': 'Выходы.inputs.inp_03',
#             'in_a4': 'Выходы.inputs.inp_04', 'in_a5': 'Выходы.inputs.inp_05',
#             'in_a6': 'Выходы.inputs.inp_06', 'in_a7': 'Выходы.inputs.inp_07',
#             'in_b0': 'Выходы.inputs.inp_08', 'in_b1': 'Выходы.inputs.inp_09',
#             'in_b2': 'Выходы.inputs.inp_10', 'in_b3': 'Выходы.inputs.inp_11',
#             'in_b4': 'Выходы.inputs.inp_12', 'in_b5': 'Выходы.inputs.inp_13',
#             'in_b6': 'Выходы.inputs.inp_14', 'in_b7': 'Выходы.inputs.inp_15'
#         """
#     def __init__(self):
#         super().__init__()
#         self.rw_error = RWError()
#         self.wr_cond = WriteCondition()
#         self.mysql_conn = MySQLConnect()
#         self.logger = logging.getLogger(__name__)
#         self.cli_log = CLILog("info", __name__)
#
#         self.tags_list = ['Выходы.inputs.inp_00', 'Выходы.inputs.inp_01',
#                           'Выходы.inputs.inp_02', 'Выходы.inputs.inp_03',
#                           'Выходы.inputs.inp_04', 'Выходы.inputs.inp_05',
#                           'Выходы.inputs.inp_06', 'Выходы.inputs.inp_07',
#                           'Выходы.inputs.inp_08', 'Выходы.inputs.inp_09',
#                           'Выходы.inputs.inp_10', 'Выходы.inputs.inp_11',
#                           'Выходы.inputs.inp_12', 'Выходы.inputs.inp_13',
#                           'Выходы.inputs.inp_14', 'Выходы.inputs.inp_15']
#
#         self.result: list[str] = []
#
#     def di_read(self) -> {str, bool}:
#         """
#         Считывает в OPC сервере состояние тегов.
#             from OpenOPC import client
#             opc = client()
#             opc.connect('arOPC.arOpcServer.1')
#             gr_di = 'Выходы.inputs.'
#             args = (f"{gr_di}inp_00", f'{gr_di}inp_01')
#             read_tags = opc.read(args, group=gr_di, update=1, include_error=True)
#             print(read_tags)
#             opc.remove(gr_di)
#         :return:
#         """
#         position: dict = {}
#         read_tags = []
#         read_tags.clear()
#
#         self.logger.debug("старт считывания дискретных входов ПЛК")
#         self.cli_log.lev_debug("старт считывания дискретных входов ПЛК", "gray")
#         gr_di = 'Выходы.inputs'
#         read_tags = self.opc.read(self.tags_list, group=gr_di, update=1, include_error=True)
#         self.opc.remove(gr_di)
#         self.logger.debug(f'считанные значения {read_tags}')
#         self.cli_log.lev_debug(f'считанные значения {read_tags}', "gray")
#         if read_tags[0][2] == "Good":
#             self.logger.info(f'качество дискретных сигналов {read_tags[0][2]}')
#             self.cli_log.lev_info(f'качество дискретных сигналов {read_tags[0][2]}', "green")
#         else:
#             self.logger.warning(f'качество дискретных сигналов {read_tags[0][2]}')
#             self.cli_log.lev_warning(f'качество дискретных сигналов {read_tags[0][2]}', "red")
#             raise ModbusConnectException("!!! Нет связи с контроллером !!! \nПроверьте подключение компьютера к "
#                                          "шкафу \"Ethernet\" кабелем  и состояние OPC сервера.")
#         for k in read_tags:
#             name = k[0].split(".")[2]
#             position[name] = k[1]
#         return position
#
#     def subtest_read_di(self, *, test_num: int = 1, subtest_num: float = 1, err_code: [int],
#                         position_inp: [bool], di_a: [str]) -> bool:
#         """
#         Метод используется в алгоритмах у которых только один вход,
#         для следующих используется вход in_a1
#         общий тест для bdu_4_3, bdu_014tp, bdu, bdu_d, bru_2s, bu_pmvir
#         для следующих используется вход in_a2
#         общий тест для
#         Код ошибки	30	–	Сообщение	«Блок не исправен. Контакты блока находятся в неисходном состоянии».
#         :param test_num: Номер теста
#         :param subtest_num: Номер подтеста
#         :param err_code: код неисправности
#         :param position_inp: положение которое должен занять выход блока
#         :param di_a: вход контроллера
#         :return:
#         """
#         self.logger.debug(f"считывание дискретных входов. функция subtest_1di")
#         self.cli_log.lev_debug(f"считывание дискретных входов. функция subtest_1di", "gray")
#         self.wr_cond.write_condition(test_num, subtest_num)
#         position_read = self.di_read()
#
#         self.logger.debug(f"состояние входа: {position_read}")
#         self.cli_log.lev_debug(f"состояние входа: {position_read}", "gray")
#         k = 0
#         for i in di_a:
#             if position_inp[k] is position_read[i]:
#                 self.result.append(f"{i}: должно быть: {position_inp[k]}, получили: {position_read[i]}")
#                 k += 1
#                 continue
#             else:
#                 self.rw_error.rw_err(err_code[k])
#                 self.wr_cond.write_condition_false(test_num, subtest_num)
#                 return False
#         self.logger.debug(f"{self.result}")
#         self.cli_log.lev_info(f"{self.result}", "skyblue")
#         self.wr_cond.write_condition_true(test_num, subtest_num)
#         self.result.clear()
#         return True
#
#     # def opc_close(self):
#     #     self.opc.close('arOPC.arOpcServer.1')
