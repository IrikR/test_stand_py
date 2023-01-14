# # -*- coding: utf-8 -*-
# """
#
# """
# __all__ = ["ReadWriteAI"]
#
# import logging
#
# from time import sleep
#
# from .exception import ModbusConnectException
# from .utils import CLILog
# from .opc_connect import ConnectOPC
#
#
#
#
# class ReadWriteAI(ConnectOPC):
#     """
#     Управление дискретными выходами контроллера через ModBus OPC Server.
#     100 запуск счетчика импульсов БКИ-1Т
#     101 запуск 1-го подтеста БКИ-6-ЗШ
#     102 запуск 2-го подтеста БКИ-6-ЗШ
#     103 измерение времени переключения длительностью до 3000мс по входам а6 и б1
#     104 измерение времени переключения длительностью до 100мс по входам а5 и б1
#     105 измерение времени переключения длительностью до 300мс по входам а5 и б1
#     106 импульсно включает KL63 на 80мс
#     107 импульсно включает KL63 на 500мс
#     108 импульсно включает KL63 на 100мс
#     109 измерение времени переключения длительностью до 500мс по входам а5 (False) и б1 (True)
#     110
#     111 измерение времени переключения длительностью до 1000мс по входам а1 (True) и b1 (True)
#     """
#     def __init__(self):
#         super().__init__()
#         self.logger = logging.getLogger(__name__)
#         self.cli_log = CLILog("info", __name__)
#
#         self.tags_value = []
#         self.analog_tags_value = []
#
#     def ctrl_ai_code_v0(self, code: int) -> [int, float]:
#         """
#         103 измерение времени переключения длительностью до 3000мс по входам а6 и б1
#         104 измерение времени переключения длительностью до 100мс по входам а5 и б1
#         105 измерение времени переключения длительностью до 300мс по входам а5 и б1
#         109 измерение времени переключения длительностью до 500мс по входам а5 (False) и б1 (True)
#         110 Запуск таймера происходит по условию замыкания DI.b1
#             Остановка таймера происходит по условию размыкания DI.a5 T1[i]
#             Пауза 500 мс
#         111 измерение времени переключения длительностью до 1000мс по входам а1 (True) и b1 (True)
#         :param code: 103, 104, 105, 109, 110, 111
#         :return:
#         """
#         self.opc['Устройство.tegs.in_num_alg'] = code
#         sleep(3)
#         in_a1, in_a2, in_a5, in_a6 = self.di_read.di_read("in_a1", "in_a2", "in_a5", "in_a6")
#         self.analog_tags_value.append(self.opc.list('Устройство.tegs')[3])
#         val = self.opc.read(self.analog_tags_value, update=1, include_error=True)
#         conv_lst = ' '.join(map(str, val))
#         list_str = conv_lst.split(', ', 5)
#         list_str[0] = list_str[0][2:-1]
#         if list_str[2] == "'Good'":
#             pass
#         else:
#             self.opc['Устройство.tegs.in_num_alg'] = 0
#             self.logger.warning(f'качество сигнала ctrl_ai_code_v0 {list_str[2]}')
#             self.cli_log.lev_info(f'качество сигнала ctrl_ai_code_v0 {list_str[2]}', "orange")
#             raise ModbusConnectException("!!! Нет связи с контроллером !!! \nПроверьте подключение компьютера к "
#                                          "шкафу \"Ethernet\" кабелем  и состояние OPC сервера.")
#
#         analog_inp_fl = float(list_str[1])
#         self.logger.info(f"ctrl_ai_code_v0 время срабатывания: {analog_inp_fl}")
#         self.cli_log.lev_info(f"ctrl_ai_code_v0 время срабатывания: {analog_inp_fl}", "orange")
#         self.opc['Устройство.tegs.in_num_alg'] = 0
#         self.logger.debug(f"ctrl_ai_code_v0 дискретные входы: {in_a1 =}, {in_a2 =}, {in_a5 =}, {in_a6 =}")
#         self.cli_log.lev_info(f"ctrl_ai_code_v0 дискретные входы: {in_a1 =}, {in_a2 =}, {in_a5 =}, {in_a6 =}", "skyblue")
#         if analog_inp_fl >= 9000.0:
#             return 9999, in_a1, in_a2, in_a5, in_a6
#         else:
#             return analog_inp_fl, in_a1, in_a2, in_a5, in_a6
#
#     def ctrl_ai_code_100(self) -> [int, float]:
#         """
#         100 запуск счетчика импульсов БКИ-1Т
#         :return: analog_inp_fl
#         """
#         self.opc['Устройство.tegs.in_num_alg'] = 100
#         sleep(3)
#
#         self.analog_tags_value.append(self.opc.list('Устройство.tegs')[0])
#         val = self.opc.read(self.analog_tags_value, update=1, include_error=True)
#         conv_lst = ' '.join(map(str, val))
#         list_str = conv_lst.split(', ', 5)
#         list_str[0] = list_str[0][2:-1]
#         if list_str[2] == "'Good'":
#             pass
#         else:
#             self.opc['Устройство.tegs.in_num_alg'] = 0
#             self.logger.warning(f'качество сигнала ctrl_ai_code_v0 {list_str[2]}')
#             self.cli_log.lev_info(f'качество сигнала ctrl_ai_code_v0 {list_str[2]}', "orange")
#             raise ModbusConnectException("!!! Нет связи с контроллером !!! \nПроверьте подключение компьютера к "
#                                          "шкафу \"Ethernet\" кабелем  и состояние OPC сервера.")
#         analog_inp_fl = float(list_str[1])
#         self.opc['Устройство.tegs.in_num_alg'] = 0
#         return analog_inp_fl
#
#     def ctrl_ai_code_101(self) -> [int, float]:
#         """
#         101 запуск 1-го подтеста БКИ-6-ЗШ
#         :return: analog_inp_fl
#         """
#         self.opc['Устройство.tegs.in_num_alg'] = 101
#         sleep(21)
#         self.analog_tags_value.append(self.opc.list('Устройство.tegs')[1])
#         val = self.opc.read(self.analog_tags_value, update=1, include_error=True)
#         conv_lst = ' '.join(map(str, val))
#         list_str = conv_lst.split(', ', 5)
#         list_str[0] = list_str[0][2:-1]
#         if list_str[2] == "'Good'":
#             pass
#         else:
#             self.opc['Устройство.tegs.in_num_alg'] = 0
#             self.logger.warning(f'качество сигнала ctrl_ai_code_v0 {list_str[2]}')
#             self.cli_log.lev_info(f'качество сигнала ctrl_ai_code_v0 {list_str[2]}', "orange")
#             raise ModbusConnectException("!!! Нет связи с контроллером !!! \nПроверьте подключение компьютера к "
#                                          "шкафу \"Ethernet\" кабелем  и состояние OPC сервера.")
#         analog_inp_fl = float(list_str[1])
#         self.opc['Устройство.tegs.in_num_alg'] = 0
#         return analog_inp_fl
#
#     def ctrl_ai_code_102(self) -> [int, float]:
#         """
#         102 запуск 2-го подтеста БКИ-6-ЗШ
#         :return: analog_inp_fl
#         """
#         self.opc['Устройство.tegs.in_num_alg'] = 102
#         sleep(3)
#         self.analog_tags_value.append(self.opc.list('Устройство.tegs')[2])
#         val = self.opc.read(self.analog_tags_value, update=1, include_error=True)
#         conv_lst = ' '.join(map(str, val))
#         list_str = conv_lst.split(', ', 5)
#         list_str[0] = list_str[0][2:-1]
#         if list_str[2] == "'Good'":
#             pass
#         else:
#             self.opc['Устройство.tegs.in_num_alg'] = 0
#             self.logger.warning(f'качество сигнала ctrl_ai_code_v0 {list_str[2]}')
#             self.cli_log.lev_info(f'качество сигнала ctrl_ai_code_v0 {list_str[2]}', "orange")
#             raise ModbusConnectException("!!! Нет связи с контроллером !!! \nПроверьте подключение компьютера к "
#                                          "шкафу \"Ethernet\" кабелем  и состояние OPC сервера.")
#         analog_inp_fl = float(list_str[1])
#         self.opc['Устройство.tegs.in_num_alg'] = 0
#         return analog_inp_fl
#
#     def ctrl_ai_code_v1(self, code: int) -> None:
#         """
#         106 импульсно включает KL63 на 80мс
#         107 импульсно включает KL63 на 500мс
#         108 импульсно включает KL63 на 100мс
#         :param code:
#         :return: None
#         """
#         self.opc['Устройство.tegs.in_num_alg'] = code
#         sleep(0.5)
#         self.opc['Устройство.tegs.in_num_alg'] = 0
#
#     def read_uint_error_4(self) -> [int, float]:
#         """
#             Считывание тега modbus error_4
#         :return:
#         """
#         self.analog_tags_value.append(self.opc.list('Устройство.tegs')[3])
#         val = self.opc.read(self.analog_tags_value, update=1, include_error=True)
#         conv_lst = ' '.join(map(str, val))
#         list_str = conv_lst.split(', ', 5)
#         list_str[0] = list_str[0][2:-1]
#         if list_str[2] == "'Good'":
#             pass
#         else:
#             self.logger.warning(f'качество сигнала read_uint_error_4 {list_str[2]}')
#             self.cli_log.lev_info(f'качество сигнала read_uint_error_4 {list_str[2]}', "red")
#             raise ModbusConnectException("!!! Нет связи с контроллером !!! \nПроверьте подключение компьютера к "
#                                          "шкафу \"Ethernet\" кабелем  и состояние OPC сервера.")
#         analog_inp_fl = float(list_str[1])
#         return analog_inp_fl
#
#     def read_uint_error_1(self) -> [int, float]:
#         """
#             считывание тега modbus error_1
#         :return analog_inp_fl: int, float
#         """
#         self.analog_tags_value.append(self.opc.list('Устройство.tegs')[1])
#         val = self.opc.read(self.analog_tags_value, update=1, include_error=True)
#         conv_lst = ' '.join(map(str, val))
#         list_str = conv_lst.split(', ', 5)
#         list_str[0] = list_str[0][2:-1]
#         if list_str[2] == "'Good'":
#             pass
#         else:
#             self.logger.warning(f'качество сигнала read_uint_error_1 {list_str[2]}')
#             self.cli_log.lev_info(f'качество сигнала read_uint_error_1 {list_str[2]}', "red")
#             raise ModbusConnectException("!!! Нет связи с контроллером !!! \nПроверьте подключение компьютера к "
#                                          "шкафу \"Ethernet\" кабелем  и состояние OPC сервера.")
#         analog_inp_fl = float(list_str[1])
#         return analog_inp_fl
#
#     def read_uint_error_2(self) -> [int, float]:
#         """
#             считывание тега modbus error_2
#         :return:
#         """
#         self.analog_tags_value.append(self.opc.list('Устройство.tegs')[2])
#         val = self.opc.read(self.analog_tags_value, update=1, include_error=True)
#         conv_lst = ' '.join(map(str, val))
#         list_str = conv_lst.split(', ', 5)
#         list_str[0] = list_str[0][2:-1]
#         if list_str[2] == "'Good'":
#             pass
#         else:
#             self.logger.warning(f'качество сигнала read_uint_error_2 {list_str[2]}')
#             self.cli_log.lev_info(f'качество сигнала read_uint_error_2 {list_str[2]}', "red")
#             raise ModbusConnectException("!!! Нет связи с контроллером !!! \nПроверьте подключение компьютера к "
#                                          "шкафу \"Ethernet\" кабелем  и состояние OPC сервера.")
#         analog_inp_fl = float(list_str[1])
#         return analog_inp_fl
#
#     def read_ai(self, teg: str) -> float:
#         """
#         Метод считывания аналоговых значений из OPC сервера, по входам измеряющим напряжение в стенде.
#         :param teg: Принимает значение тега который нужно прочитать ('AI0' или 'AI2')
#         :return: возвращает вычисленное значение напряжения в первичных величинах.
#         """
#         read_tags: list = []
#
#         analog_max_code = 27648.0
#         analog_max_ai0 = 400.0
#         analog_max_ai2 = 10.0
#
#         ai_teg_list = ['AI.AI.AI0', 'AI.AI.AI2']
#
#         read_tags.clear()
#
#         self.logger.debug("старт считывания аналоговых входов ПЛК")
#         self.cli_log.lev_info("старт считывания аналоговых входов ПЛК", "gray")
#
#         gr_ai = 'AI.AI.'
#         read_tags = self.opc.read(ai_teg_list, group=gr_ai, update=1, include_error=True)
#         self.opc.remove(gr_ai)
#         self.logger.info(f'считанные значения {read_tags}')
#         self.cli_log.lev_info(f'считанные значения {read_tags}', "orange")
#         if read_tags[0][2] == 'Good':
#             pass
#         else:
#             self.logger.warning(f'качество аналогового сигнала {read_tags[1]}')
#             self.cli_log.lev_info(f'качество аналогового сигнала {read_tags[1]}', "red")
#             raise ModbusConnectException("!!! Нет связи с контроллером !!! \nПроверьте подключение компьютера к "
#                                          "шкафу \"Ethernet\" кабелем  и состояние OPC сервера.")
#         analog_inp_ai0 = read_tags[0][1]
#         analog_inp_ai2 = read_tags[1][1]
#         if teg == 'AI0':
#             calc_volt = analog_inp_ai0 * analog_max_ai0 / analog_max_code
#             self.logger.info(f'возврат результата AI0 = {calc_volt}')
#             self.cli_log.lev_info(f'возврат результата AI0 = {calc_volt}', "orange")
#             return calc_volt
#         elif teg == 'AI2':
#             calc_volt = analog_inp_ai2 * analog_max_ai2 / analog_max_code
#             self.logger.info(f'возврат результата AI2 = {calc_volt}')
#             self.cli_log.lev_info(f'возврат результата AI2 = {calc_volt}', "orange")
#             return calc_volt
#         else:
#             self.logger.info(f'возврат результата (небыл получен аргумент) = {analog_inp_ai0}')
#             self.cli_log.lev_info(f'возврат результата (небыл получен аргумент) = {analog_inp_ai0}', "orange")
#             return analog_inp_ai0
#
#     # def opc_close(self):
#     #     self.opc.close()