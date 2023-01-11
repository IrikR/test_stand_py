#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from time import sleep

from OpenOPC import client

from .exception import ModbusConnectException
from .utils import CLILog

__all__ = ['CtrlKL', 'ReadMB', 'DIRead', "AIRead"]


class CtrlKL:
    """
    Управление дискретными выходами контроллера через ModBus OPC Server.
    100 запуск счетчика импульсов БКИ-1Т
    101 запуск 1-го подтеста БКИ-6-ЗШ
    102 запуск 2-го подтеста БКИ-6-ЗШ
    103 измерение времени переключения длительностью до 3000мс по входам а6 и б1
    104 измерение времени переключения длительностью до 100мс по входам а5 и б1
    105 измерение времени переключения длительностью до 300мс по входам а5 и б1
    106 импульсно включает KL63 на 80мс
    107 импульсно включает KL63 на 500мс
    108 импульсно включает KL63 на 100мс
    109 измерение времени переключения длительностью до 500мс по входам а5 (False) и б1 (True)
    110
    111 измерение времени переключения длительностью до 1000мс по входам а1 (True) и b1 (True)
    """

    def __init__(self):
        self.opc = client()
        self.opc.connect('arOPC.arOpcServer.1')
        self.__dic_relay = {'KL1': 'Устройство.tg.in_perekl_rejimov_KL1',
                            'KL2': 'Устройство.tg.in_power_18V_KL2',
                            'KL3': 'Устройство.tg.in_R1_KL3',
                            'KL4': 'Устройство.tg.in_R2_KL4',
                            'KL5': 'Устройство.tg.in_R3_KL5',
                            'KL6': 'Устройство.tg.in_R4_KL6',
                            'KL7': 'Устройство.tg.in_R5_KL7',
                            'KL8': 'Устройство.tg.in_R6_KL8',
                            'KL9': 'Устройство.tg.in_R7_KL9',
                            'KL10': 'Устройство.tg.in_R8_KL10',
                            'KL11': 'Устройство.tg.in_KZ_KL11',
                            'KL12': 'Устройство.tg.in_pusk_KL12',
                            'KL13': 'Устройство.tg.in_R10_KL13',
                            'KL14': 'Устройство.tg.in_R11_KL14',
                            'KL15': 'Устройство.tg.in_R12_KL15',
                            'KL16': 'Устройство.tg.in_R13_KL16',
                            'KL17': 'Устройство.tg.in_R14_KL17',
                            'KL18': 'Устройство.tg.in_R15_KL18',
                            'KL19': 'Устройство.tg.in_R16_KL19',
                            'KL20': 'Устройство.tg.in_R17_KL20',
                            'KL21': 'Устройство.tg.in_power_36V_KL21',
                            'KL22': 'Устройство.tg.in_perekl_KI_BKI_KL22',
                            'KL23': 'Устройство.tg.in_perekl_660V_1140V_KL23',
                            'KL24': 'Устройство.tg.in_shunt_D_KL24',
                            'KL25': 'Устройство.tg.in_R_shunt_KL25',
                            'KL26': 'Устройство.tg.in_DU_KL26',
                            'KL27': 'Устройство.tg.in_cont_ser_KT_KL27',
                            'KL28': 'Устройство.tg.in_perek_18V_KL28',
                            'KL29': 'Устройство.tg.in_KL29',
                            'KL30': 'Устройство.tg.in_power_KT_KL30',
                            'KL31': 'Устройство.tg.in_perekl_kanalov_KL31',
                            'KL32': 'Устройство.tg.in_power_110V_KL32',
                            'KL33': 'Устройство.tg.in_power_15V_KL33',
                            'KL36': 'Устройство.tg.in_power_48V_KL36',
                            'KL37': 'Устройство.tg.in_puskovoi_R_KL37',
                            'KL38': 'Устройство.tg.in_perv_obm_TV1_KL38',
                            'KL39': 'Устройство.tg.in_perv_obm_TV1_KL39',
                            'KL40': 'Устройство.tg.in_perv_obm_TV1_KL40',
                            'KL41': 'Устройство.tg.in_perv_obm_TV1_KL41',
                            'KL42': 'Устройство.tg.in_perv_obm_TV1_KL42',
                            'KL43': 'Устройство.tg.in_perv_obm_TV1_KL43',
                            'KL44': 'Устройство.tg.in_perv_obm_TV1_KL44',
                            'KL45': 'Устройство.tg.in_perv_obm_TV1_KL45',
                            'KL46': 'Устройство.tg.in_perv_obm_TV1_KL46',
                            'KL47': 'Устройство.tg.in_perv_obm_TV1_KL47',
                            'KL48': 'Устройство.tg.in_vtor_obm_TV1_KL48',
                            'KL49': 'Устройство.tg.in_vtor_obm_TV1_KL49',
                            'KL50': 'Устройство.tg.in_vtor_obm_TV1_KL50',
                            'KL51': 'Устройство.tg.in_vtor_obm_TV1_KL51',
                            'KL52': 'Устройство.tg.in_vtor_obm_TV1_KL52',
                            'KL53': 'Устройство.tg.in_vtor_obm_TV1_KL53',
                            'KL54': 'Устройство.tg.in_vtor_obm_TV1_KL54',
                            'KL55': 'Устройство.tg.in_vtor_obm_TV1_KL55',
                            'KL56': 'Устройство.tg.in_vtor_obm_TV1_KL56',
                            'KL57': 'Устройство.tg.in_vtor_obm_TV1_KL57',
                            'KL58': 'Устройство.tg.in_vtor_obm_TV1_KL58',
                            'KL59': 'Устройство.tg.in_vtor_obm_TV1_KL59',
                            'KL60': 'Устройство.tg.in_KZ_obmotka_KL60',
                            'KL62': 'Устройство.tg.in_perv_gl_kont_KL62',
                            'KL63': 'Устройство.tg.in_vtor_gl_kont_KL63',
                            'KL65': 'Устройство.tg.in_KL65',
                            'KL66': 'Устройство.tg.in_power_12V_KL66',
                            'KL67': 'Устройство.tg.in_KL67',
                            'KL68': 'Устройство.tg.in_KL68',
                            'KL69': 'Устройство.tg.in_KL69',
                            'KL70': 'Устройство.tg.in_KL88',
                            'KL71': 'Устройство.tg.in_KL71',
                            'KL72': 'Устройство.tg.in_KL72',
                            'KL73': 'Устройство.tg.in_rejim_AB_VG_KL73',
                            'KL74': 'Устройство.tg.in_rejim_rabor_KL74',
                            'KL75': 'Устройство.tg.in_KL75',
                            'KL76': 'Устройство.tg.in_KL76',
                            'KL77': 'Устройство.tg.in_KL77',
                            'KL78': 'Устройство.tg.in_KL78',
                            'KL79': 'Устройство.tg.in_KL79',
                            'KL80': 'Устройство.tg.in_KL80',
                            'KL81': 'Устройство.tg.in_KL81',
                            'KL82': 'Устройство.tg.in_KL82',
                            'KL83': 'Устройство.tg.in_KL83',
                            'KL84': 'Устройство.tg.in_KL84',
                            'KL88': 'Устройство.tg.in_KL88',
                            'KL89': 'Устройство.tg.in_KL89',
                            'KL90': 'Устройство.tg.in_KL90',
                            'KL91': 'Устройство.tg.in_KL91',
                            'KL92': 'Устройство.tg.in_KL92',
                            'KL93': 'Устройство.tg.in_KL93',
                            'KL94': 'Устройство.tg.in_KL94',
                            'KL95': 'Устройство.tg.in_KL95',
                            'KL97': 'Устройство.tg.in_KL97',
                            'KL98': 'Устройство.tg.in_KL98',
                            'KL99': 'Устройство.tg.in_KL99',
                            'KL100': 'Устройство.tg.in_KL100',
                            'Q113_4': 'Устройство.tg.in_Q113_4',
                            'Q113_5': 'Устройство.tg.in_Q113_5',
                            'Q113_6': 'Устройство.tg.in_Q113_6',
                            'Q113_7': 'Устройство.tg.in_Q113_7'}

        self.__list_relay = ('Устройство.tg.in_perekl_rejimov_KL1', 'Устройство.tg.in_power_18V_KL2',
                             'Устройство.tg.in_R1_KL3', 'Устройство.tg.in_R2_KL4',
                             'Устройство.tg.in_R3_KL5', 'Устройство.tg.in_R4_KL6',
                             'Устройство.tg.in_R5_KL7', 'Устройство.tg.in_R6_KL8',
                             'Устройство.tg.in_R7_KL9', 'Устройство.tg.in_R8_KL10',
                             'Устройство.tg.in_KZ_KL11', 'Устройство.tg.in_pusk_KL12',
                             'Устройство.tg.in_R10_KL13', 'Устройство.tg.in_R11_KL14',
                             'Устройство.tg.in_R12_KL15', 'Устройство.tg.in_R13_KL16',
                             'Устройство.tg.in_R14_KL17', 'Устройство.tg.in_R15_KL18',
                             'Устройство.tg.in_R16_KL19', 'Устройство.tg.in_R17_KL20',
                             'Устройство.tg.in_power_36V_KL21', 'Устройство.tg.in_perekl_KI_BKI_KL22',
                             'Устройство.tg.in_perekl_660V_1140V_KL23', 'Устройство.tg.in_shunt_D_KL24',
                             'Устройство.tg.in_R_shunt_KL25', 'Устройство.tg.in_DU_KL26',
                             'Устройство.tg.in_cont_ser_KT_KL27', 'Устройство.tg.in_perek_18V_KL28',
                             'Устройство.tg.in_KL29', 'Устройство.tg.in_power_KT_KL30',
                             'Устройство.tg.in_perekl_kanalov_KL31', 'Устройство.tg.in_power_110V_KL32',
                             'Устройство.tg.in_power_15V_KL33', 'Устройство.tg.in_power_48V_KL36',
                             'Устройство.tg.in_puskovoi_R_KL37', 'Устройство.tg.in_perv_obm_TV1_KL38',
                             'Устройство.tg.in_perv_obm_TV1_KL39', 'Устройство.tg.in_perv_obm_TV1_KL40',
                             'Устройство.tg.in_perv_obm_TV1_KL41', 'Устройство.tg.in_perv_obm_TV1_KL42',
                             'Устройство.tg.in_perv_obm_TV1_KL43', 'Устройство.tg.in_perv_obm_TV1_KL44',
                             'Устройство.tg.in_perv_obm_TV1_KL45', 'Устройство.tg.in_perv_obm_TV1_KL46',
                             'Устройство.tg.in_perv_obm_TV1_KL47', 'Устройство.tg.in_vtor_obm_TV1_KL48',
                             'Устройство.tg.in_vtor_obm_TV1_KL49', 'Устройство.tg.in_vtor_obm_TV1_KL50',
                             'Устройство.tg.in_vtor_obm_TV1_KL51', 'Устройство.tg.in_vtor_obm_TV1_KL52',
                             'Устройство.tg.in_vtor_obm_TV1_KL53', 'Устройство.tg.in_vtor_obm_TV1_KL54',
                             'Устройство.tg.in_vtor_obm_TV1_KL55', 'Устройство.tg.in_vtor_obm_TV1_KL56',
                             'Устройство.tg.in_vtor_obm_TV1_KL57', 'Устройство.tg.in_vtor_obm_TV1_KL58',
                             'Устройство.tg.in_vtor_obm_TV1_KL59', 'Устройство.tg.in_KZ_obmotka_KL60',
                             'Устройство.tg.in_perv_gl_kont_KL62', 'Устройство.tg.in_vtor_gl_kont_KL63',
                             'Устройство.tg.in_KL65', 'Устройство.tg.in_power_12V_KL66',
                             'Устройство.tg.in_KL67', 'Устройство.tg.in_KL68',
                             'Устройство.tg.in_KL69', 'Устройство.tg.in_KL88',
                             'Устройство.tg.in_KL71', 'Устройство.tg.in_KL72',
                             'Устройство.tg.in_rejim_AB_VG_KL73', 'Устройство.tg.in_rejim_rabor_KL74',
                             'Устройство.tg.in_KL75', 'Устройство.tg.in_KL76',
                             'Устройство.tg.in_KL77', 'Устройство.tg.in_KL78',
                             'Устройство.tg.in_KL79', 'Устройство.tg.in_KL80',
                             'Устройство.tg.in_KL81', 'Устройство.tg.in_KL82',
                             'Устройство.tg.in_KL83', 'Устройство.tg.in_KL84',
                             'Устройство.tg.in_KL88', 'Устройство.tg.in_KL89',
                             'Устройство.tg.in_KL90', 'Устройство.tg.in_KL91',
                             'Устройство.tg.in_KL92', 'Устройство.tg.in_KL93',
                             'Устройство.tg.in_KL94', 'Устройство.tg.in_KL95',
                             'Устройство.tg.in_KL97', 'Устройство.tg.in_KL98',
                             'Устройство.tg.in_KL99', 'Устройство.tg.in_KL100',
                             'Устройство.tg.in_Q113_4', 'Устройство.tg.in_Q113_5',
                             'Устройство.tg.in_Q113_6', 'Устройство.tg.in_Q113_7')
        self.analog_tags_value = []
        self.logger = logging.getLogger(__name__)
        self.di_read = DIRead()
        self.cli_log = CLILog(True, __name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))

    def ctrl_relay(self, rel: str, ctrl: bool) -> None:
        kl = self.__dic_relay[f'{rel}']
        self.opc[kl] = ctrl

    def reset_all_v1(self) -> None:
        for i1 in range(len(self.__list_relay)):
            kl = self.__list_relay[i1]
            self.opc[kl] = False

    def reset_all_v2(self) -> None:
        kl = self.__dic_relay.keys()
        for i2 in kl:
            rele = self.__dic_relay[i2]
            self.opc[rele] = False

    def ctrl_ai_code_v0(self, code: int) -> [int, float]:
        """
        103 измерение времени переключения длительностью до 3000мс по входам а6 и б1
        104 измерение времени переключения длительностью до 100мс по входам а5 и б1
        105 измерение времени переключения длительностью до 300мс по входам а5 и б1
        109 измерение времени переключения длительностью до 500мс по входам а5 (False) и б1 (True)
        110 Запуск таймера происходит по условию замыкания DI.b1
            Остановка таймера происходит по условию размыкания DI.a5 T1[i]
            Пауза 500 мс
        111 измерение времени переключения длительностью до 1000мс по входам а1 (True) и b1 (True)
        :param code: 103, 104, 105, 109, 110, 111
        :return:
        """
        self.opc['Устройство.tegs.in_num_alg'] = code
        sleep(3)
        in_a1, in_a2, in_a5, in_a6 = self.di_read.di_read("in_a1", "in_a2", "in_a5", "in_a6")
        self.analog_tags_value.append(self.opc.list('Устройство.tegs')[3])
        val = self.opc.read(self.analog_tags_value, update=1, include_error=True)
        conv_lst = ' '.join(map(str, val))
        list_str = conv_lst.split(', ', 5)
        list_str[0] = list_str[0][2:-1]
        if list_str[2] == "'Good'":
            pass
        else:
            # elif list_str[2] == "'Bad'":
            self.opc['Устройство.tegs.in_num_alg'] = 0
            self.logger.warning(f'качество сигнала ctrl_ai_code_v0 {list_str[2]}')
            self.cli_log.log_msg(f'качество сигнала ctrl_ai_code_v0 {list_str[2]}', "orange")
            raise ModbusConnectException("!!! Нет связи с контроллером !!! \nПроверьте подключение компьютера к "
                                         "шкафу \"Ethernet\" кабелем  и состояние OPC сервера.")

        analog_inp_fl = float(list_str[1])
        self.logger.info(f"ctrl_ai_code_v0 время срабатывания: {analog_inp_fl}")
        self.cli_log.log_msg(f"ctrl_ai_code_v0 время срабатывания: {analog_inp_fl}", "orange")
        self.opc['Устройство.tegs.in_num_alg'] = 0
        self.logger.debug(f"ctrl_ai_code_v0 дискретные входы: {in_a1 =}, {in_a2 =}, {in_a5 =}, {in_a6 =}")
        self.cli_log.log_msg(f"ctrl_ai_code_v0 дискретные входы: {in_a1 =}, {in_a2 =}, {in_a5 =}, {in_a6 =}", "skyblue")
        if analog_inp_fl >= 9000.0:
            return 9999, in_a1, in_a2, in_a5, in_a6
        else:
            return analog_inp_fl, in_a1, in_a2, in_a5, in_a6

    def ctrl_ai_code_100(self) -> [int, float]:
        """
        100 запуск счетчика импульсов БКИ-1Т
        :return: analog_inp_fl
        """
        self.opc['Устройство.tegs.in_num_alg'] = 100
        sleep(3)

        self.analog_tags_value.append(self.opc.list('Устройство.tegs')[0])
        val = self.opc.read(self.analog_tags_value, update=1, include_error=True)
        conv_lst = ' '.join(map(str, val))
        list_str = conv_lst.split(', ', 5)
        list_str[0] = list_str[0][2:-1]
        if list_str[2] == "'Good'":
            pass
        else:
            self.opc['Устройство.tegs.in_num_alg'] = 0
            self.logger.warning(f'качество сигнала ctrl_ai_code_v0 {list_str[2]}')
            self.cli_log.log_msg(f'качество сигнала ctrl_ai_code_v0 {list_str[2]}', "orange")
            raise ModbusConnectException("!!! Нет связи с контроллером !!! \nПроверьте подключение компьютера к "
                                         "шкафу \"Ethernet\" кабелем  и состояние OPC сервера.")
        analog_inp_fl = float(list_str[1])
        self.opc['Устройство.tegs.in_num_alg'] = 0
        return analog_inp_fl

    def ctrl_ai_code_101(self) -> [int, float]:
        """
        101 запуск 1-го подтеста БКИ-6-ЗШ
        :return: analog_inp_fl
        """
        self.opc['Устройство.tegs.in_num_alg'] = 101
        sleep(21)
        self.analog_tags_value.append(self.opc.list('Устройство.tegs')[1])
        val = self.opc.read(self.analog_tags_value, update=1, include_error=True)
        conv_lst = ' '.join(map(str, val))
        list_str = conv_lst.split(', ', 5)
        list_str[0] = list_str[0][2:-1]
        if list_str[2] == "'Good'":
            pass
        else:
            self.opc['Устройство.tegs.in_num_alg'] = 0
            self.logger.warning(f'качество сигнала ctrl_ai_code_v0 {list_str[2]}')
            self.cli_log.log_msg(f'качество сигнала ctrl_ai_code_v0 {list_str[2]}', "orange")
            raise ModbusConnectException("!!! Нет связи с контроллером !!! \nПроверьте подключение компьютера к "
                                         "шкафу \"Ethernet\" кабелем  и состояние OPC сервера.")
        analog_inp_fl = float(list_str[1])
        self.opc['Устройство.tegs.in_num_alg'] = 0
        return analog_inp_fl

    def ctrl_ai_code_102(self) -> [int, float]:
        """
        102 запуск 2-го подтеста БКИ-6-ЗШ
        :return: analog_inp_fl
        """
        self.opc['Устройство.tegs.in_num_alg'] = 102
        sleep(3)
        self.analog_tags_value.append(self.opc.list('Устройство.tegs')[2])
        val = self.opc.read(self.analog_tags_value, update=1, include_error=True)
        conv_lst = ' '.join(map(str, val))
        list_str = conv_lst.split(', ', 5)
        list_str[0] = list_str[0][2:-1]
        if list_str[2] == "'Good'":
            pass
        else:
            self.opc['Устройство.tegs.in_num_alg'] = 0
            self.logger.warning(f'качество сигнала ctrl_ai_code_v0 {list_str[2]}')
            self.cli_log.log_msg(f'качество сигнала ctrl_ai_code_v0 {list_str[2]}', "orange")
            raise ModbusConnectException("!!! Нет связи с контроллером !!! \nПроверьте подключение компьютера к "
                                         "шкафу \"Ethernet\" кабелем  и состояние OPC сервера.")
        analog_inp_fl = float(list_str[1])
        self.opc['Устройство.tegs.in_num_alg'] = 0
        return analog_inp_fl

    def ctrl_ai_code_v1(self, code: int) -> None:
        """
        106 импульсно включает KL63 на 80мс
        107 импульсно включает KL63 на 500мс
        108 импульсно включает KL63 на 100мс
        :param code:
        :return: None
        """
        self.opc['Устройство.tegs.in_num_alg'] = code
        sleep(0.5)
        self.opc['Устройство.tegs.in_num_alg'] = 0


class ReadMB:
    """
    чтение регистров из ModBus OPC Server
    """

    def __init__(self):
        self.opc = client()
        self.opc.connect('arOPC.arOpcServer.1')
        self.tags_value = []
        self.analog_tags_value = []
        self.cli_log = CLILog(True, __name__)
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))

    def read_uint_error_4(self) -> [int, float]:
        """
            Считывание тега modbus error_4
        :return:
        """
        self.analog_tags_value.append(self.opc.list('Устройство.tegs')[3])
        val = self.opc.read(self.analog_tags_value, update=1, include_error=True)
        conv_lst = ' '.join(map(str, val))
        list_str = conv_lst.split(', ', 5)
        list_str[0] = list_str[0][2:-1]
        if list_str[2] == "'Good'":
            pass
        else:
            self.logger.warning(f'качество сигнала read_uint_error_4 {list_str[2]}')
            self.cli_log.log_msg(f'качество сигнала read_uint_error_4 {list_str[2]}', "red")
            raise ModbusConnectException("!!! Нет связи с контроллером !!! \nПроверьте подключение компьютера к "
                                         "шкафу \"Ethernet\" кабелем  и состояние OPC сервера.")
        analog_inp_fl = float(list_str[1])
        return analog_inp_fl

    def read_uint_error_1(self) -> [int, float]:
        """
            считывание тега modbus error_1
        :return analog_inp_fl: int, float
        """
        self.analog_tags_value.append(self.opc.list('Устройство.tegs')[1])
        val = self.opc.read(self.analog_tags_value, update=1, include_error=True)
        conv_lst = ' '.join(map(str, val))
        list_str = conv_lst.split(', ', 5)
        list_str[0] = list_str[0][2:-1]
        if list_str[2] == "'Good'":
            pass
        else:
            self.logger.warning(f'качество сигнала read_uint_error_1 {list_str[2]}')
            self.cli_log.log_msg(f'качество сигнала read_uint_error_1 {list_str[2]}', "red")
            raise ModbusConnectException("!!! Нет связи с контроллером !!! \nПроверьте подключение компьютера к "
                                         "шкафу \"Ethernet\" кабелем  и состояние OPC сервера.")
        analog_inp_fl = float(list_str[1])
        return analog_inp_fl

    def read_uint_error_2(self) -> [int, float]:
        """
            считывание тега modbus error_2
        :return:
        """
        self.analog_tags_value.append(self.opc.list('Устройство.tegs')[2])
        val = self.opc.read(self.analog_tags_value, update=1, include_error=True)
        conv_lst = ' '.join(map(str, val))
        list_str = conv_lst.split(', ', 5)
        list_str[0] = list_str[0][2:-1]
        if list_str[2] == "'Good'":
            pass
        else:
            self.logger.warning(f'качество сигнала read_uint_error_2 {list_str[2]}')
            self.cli_log.log_msg(f'качество сигнала read_uint_error_2 {list_str[2]}', "red")
            raise ModbusConnectException("!!! Нет связи с контроллером !!! \nПроверьте подключение компьютера к "
                                         "шкафу \"Ethernet\" кабелем  и состояние OPC сервера.")
        analog_inp_fl = float(list_str[1])
        return analog_inp_fl


class DIRead:
    """
    Чтение дискретных входов ПЛК через OPC server
    """
    def __init__(self):
        self.opc = client()
        self.opc.connect('arOPC.arOpcServer.1')
        self.cli_log = CLILog(True, __name__)
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))

        self.tags_dict = {'in_a0': 'Выходы.inputs.inp_00', 'in_a1': 'Выходы.inputs.inp_01',
                          'in_a2': 'Выходы.inputs.inp_02', 'in_a3': 'Выходы.inputs.inp_03',
                          'in_a4': 'Выходы.inputs.inp_04', 'in_a5': 'Выходы.inputs.inp_05',
                          'in_a6': 'Выходы.inputs.inp_06', 'in_a7': 'Выходы.inputs.inp_07',
                          'in_b0': 'Выходы.inputs.inp_08', 'in_b1': 'Выходы.inputs.inp_09',
                          'in_b2': 'Выходы.inputs.inp_10', 'in_b3': 'Выходы.inputs.inp_11',
                          'in_b4': 'Выходы.inputs.inp_12', 'in_b5': 'Выходы.inputs.inp_13',
                          'in_b6': 'Выходы.inputs.inp_14', 'in_b7': 'Выходы.inputs.inp_15'}

    def di_read(self, *args) -> [bool]:
        """
        Считывает в OPC сервере состояние тегов.
            from OpenOPC import client
            opc = client()
            opc.connect('arOPC.arOpcServer.1')
            gr_di = 'Выходы.inputs.'
            args = (f"{gr_di}inp_00", f'{gr_di}inp_01')
            read_tags = opc.read(args, group=gr_di, update=1, include_error=True)
            print(read_tags)
            opc.remove(gr_di)
        :param args:
        :return:
        """
        position: list = []
        tag_list = []
        read_tags = []
        read_tags.clear()

        for j in args:
            tag_list.append(self.tags_dict[j])
        self.logger.debug("старт считывания дискретных входов ПЛК")
        self.cli_log.log_msg("старт считывания дискретных входов ПЛК", "gray")
        gr_di = 'Выходы.inputs'
        read_tags = self.opc.read(tag_list, group=gr_di, update=1, include_error=True)
        self.opc.remove(gr_di)
        self.logger.info(f'считанные значения {read_tags}')
        self.cli_log.log_msg(f'считанные значения {read_tags}', "skyblue")
        if read_tags[0][2] == "Good":
            self.logger.info(f'качество дискретных сигналов {read_tags[0][2]}')
            self.cli_log.log_msg(f'качество дискретных сигналов {read_tags[0][2]}', "green")
        else:
            self.logger.warning(f'качество дискретных сигналов {read_tags[0][2]}')
            self.cli_log.log_msg(f'качество дискретных сигналов {read_tags[0][2]}', "red")
            raise ModbusConnectException("!!! Нет связи с контроллером !!! \nПроверьте подключение компьютера к "
                                         "шкафу \"Ethernet\" кабелем  и состояние OPC сервера.")
        for k in range(len(args)):
            position.append(read_tags[k][1])
        return position


class AIRead:
    """
    Класс для считывания аналоговых значений из OPC сервера.
    """
    def __init__(self):
        self.opc = client()
        self.opc.connect('arOPC.arOpcServer.1')
        self.cli_log = CLILog(True, __name__)
        self.logger = logging.getLogger(__name__)

    def ai_read(self, teg: str) -> float:
        """
        Метод считывания аналоговых значений из OPC сервера, по входам измеряющим напряжение в стенде.
        :param teg: Принимает значение тега который нужно прочитать ('AI0' или 'AI2')
        :return: возвращает вычисленное значение напряжения в первичных величинах.
        """
        read_tags: list = []

        analog_max_code = 27648.0
        analog_max_ai0 = 400.0
        analog_max_ai2 = 10.0

        ai_teg_list = ['AI.AI.AI0', 'AI.AI.AI2']

        read_tags.clear()

        self.logger.debug("старт считывания аналоговых входов ПЛК")
        self.cli_log.log_msg("старт считывания аналоговых входов ПЛК", "gray")

        gr_ai = 'AI.AI.'
        read_tags = self.opc.read(ai_teg_list, group=gr_ai, update=1, include_error=True)
        self.opc.remove(gr_ai)
        self.logger.info(f'считанные значения {read_tags}')
        self.cli_log.log_msg(f'считанные значения {read_tags}', "orange")
        if read_tags[0][2] == 'Good':
            pass
        else:
            self.logger.warning(f'качество аналогового сигнала {read_tags[1]}')
            self.cli_log.log_msg(f'качество аналогового сигнала {read_tags[1]}', "red")
            raise ModbusConnectException("!!! Нет связи с контроллером !!! \nПроверьте подключение компьютера к "
                                         "шкафу \"Ethernet\" кабелем  и состояние OPC сервера.")
        analog_inp_ai0 = read_tags[0][1]
        analog_inp_ai2 = read_tags[1][1]
        if teg == 'AI0':
            calc_volt = analog_inp_ai0 * analog_max_ai0 / analog_max_code
            self.logger.info(f'возврат результата AI0 = {calc_volt}')
            self.cli_log.log_msg(f'возврат результата AI0 = {calc_volt}', "orange")
            return calc_volt
        elif teg == 'AI2':
            calc_volt = analog_inp_ai2 * analog_max_ai2 / analog_max_code
            self.logger.info(f'возврат результата AI2 = {calc_volt}')
            self.cli_log.log_msg(f'возврат результата AI2 = {calc_volt}', "orange")
            return calc_volt
        else:
            self.logger.info(f'возврат результата (небыл получен аргумент) = {analog_inp_ai0}')
            self.cli_log.log_msg(f'возврат результата (небыл получен аргумент) = {analog_inp_ai0}', "orange")
            return analog_inp_ai0


class CtrlRead:
    """
    Состояние дискретных выходов ПЛК
    """
    def __init__(self):
        self.opc = client()
        self.opc.connect('arOPC.arOpcServer.1')
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler(self.logger.setLevel(10)))

        self.relay_dict = {'KL1': 'Устройство.tg.in_perekl_rejimov_KL1',
                           'KL2': 'Устройство.tg.in_power_18V_KL2',
                           'KL3': 'Устройство.tg.in_R1_KL3',
                           'KL4': 'Устройство.tg.in_R2_KL4',
                           'KL5': 'Устройство.tg.in_R3_KL5',
                           'KL6': 'Устройство.tg.in_R4_KL6',
                           'KL7': 'Устройство.tg.in_R5_KL7',
                           'KL8': 'Устройство.tg.in_R6_KL8',
                           'KL9': 'Устройство.tg.in_R7_KL9',
                           'KL10': 'Устройство.tg.in_R8_KL10',
                           'KL11': 'Устройство.tg.in_KZ_KL11',
                           'KL12': 'Устройство.tg.in_pusk_KL12',
                           'KL13': 'Устройство.tg.in_R10_KL13',
                           'KL14': 'Устройство.tg.in_R11_KL14',
                           'KL15': 'Устройство.tg.in_R12_KL15',
                           'KL16': 'Устройство.tg.in_R13_KL16',
                           'KL17': 'Устройство.tg.in_R14_KL17',
                           'KL18': 'Устройство.tg.in_R15_KL18',
                           'KL19': 'Устройство.tg.in_R16_KL19',
                           'KL20': 'Устройство.tg.in_R17_KL20',
                           'KL21': 'Устройство.tg.in_power_36V_KL21',
                           'KL22': 'Устройство.tg.in_perekl_KI_BKI_KL22',
                           'KL23': 'Устройство.tg.in_perekl_660V_1140V_KL23',
                           'KL24': 'Устройство.tg.in_shunt_D_KL24',
                           'KL25': 'Устройство.tg.in_R_shunt_KL25',
                           'KL26': 'Устройство.tg.in_DU_KL26',
                           'KL27': 'Устройство.tg.in_cont_ser_KT_KL27',
                           'KL28': 'Устройство.tg.in_perek_18V_KL28',
                           'KL29': 'Устройство.tg.in_KL29',
                           'KL30': 'Устройство.tg.in_power_KT_KL30',
                           'KL31': 'Устройство.tg.in_perekl_kanalov_KL31',
                           'KL32': 'Устройство.tg.in_power_110V_KL32',
                           'KL33': 'Устройство.tg.in_power_15V_KL33',
                           'KL36': 'Устройство.tg.in_power_48V_KL36',
                           'KL37': 'Устройство.tg.in_puskovoi_R_KL37',
                           'KL38': 'Устройство.tg.in_perv_obm_TV1_KL38',
                           'KL39': 'Устройство.tg.in_perv_obm_TV1_KL39',
                           'KL40': 'Устройство.tg.in_perv_obm_TV1_KL40',
                           'KL41': 'Устройство.tg.in_perv_obm_TV1_KL41',
                           'KL42': 'Устройство.tg.in_perv_obm_TV1_KL42',
                           'KL43': 'Устройство.tg.in_perv_obm_TV1_KL43',
                           'KL44': 'Устройство.tg.in_perv_obm_TV1_KL44',
                           'KL45': 'Устройство.tg.in_perv_obm_TV1_KL45',
                           'KL46': 'Устройство.tg.in_perv_obm_TV1_KL46',
                           'KL47': 'Устройство.tg.in_perv_obm_TV1_KL47',
                           'KL48': 'Устройство.tg.in_vtor_obm_TV1_KL48',
                           'KL49': 'Устройство.tg.in_vtor_obm_TV1_KL49',
                           'KL50': 'Устройство.tg.in_vtor_obm_TV1_KL50',
                           'KL51': 'Устройство.tg.in_vtor_obm_TV1_KL51',
                           'KL52': 'Устройство.tg.in_vtor_obm_TV1_KL52',
                           'KL53': 'Устройство.tg.in_vtor_obm_TV1_KL53',
                           'KL54': 'Устройство.tg.in_vtor_obm_TV1_KL54',
                           'KL55': 'Устройство.tg.in_vtor_obm_TV1_KL55',
                           'KL56': 'Устройство.tg.in_vtor_obm_TV1_KL56',
                           'KL57': 'Устройство.tg.in_vtor_obm_TV1_KL57',
                           'KL58': 'Устройство.tg.in_vtor_obm_TV1_KL58',
                           'KL59': 'Устройство.tg.in_vtor_obm_TV1_KL59',
                           'KL60': 'Устройство.tg.in_KZ_obmotka_KL60',
                           'KL62': 'Устройство.tg.in_perv_gl_kont_KL62',
                           'KL63': 'Устройство.tg.in_vtor_gl_kont_KL63',
                           'KL65': 'Устройство.tg.in_KL65',
                           'KL66': 'Устройство.tg.in_power_12V_KL66',
                           'KL67': 'Устройство.tg.in_KL67',
                           'KL68': 'Устройство.tg.in_KL68',
                           'KL69': 'Устройство.tg.in_KL69',
                           'KL70': 'Устройство.tg.in_KL88',
                           'KL71': 'Устройство.tg.in_KL71',
                           'KL72': 'Устройство.tg.in_KL72',
                           'KL73': 'Устройство.tg.in_rejim_AB_VG_KL73',
                           'KL74': 'Устройство.tg.in_rejim_rabor_KL74',
                           'KL75': 'Устройство.tg.in_KL75',
                           'KL76': 'Устройство.tg.in_KL76',
                           'KL77': 'Устройство.tg.in_KL77',
                           'KL78': 'Устройство.tg.in_KL78',
                           'KL79': 'Устройство.tg.in_KL79',
                           'KL80': 'Устройство.tg.in_KL80',
                           'KL81': 'Устройство.tg.in_KL81',
                           'KL82': 'Устройство.tg.in_KL82',
                           'KL83': 'Устройство.tg.in_KL83',
                           'KL84': 'Устройство.tg.in_KL84',
                           'KL88': 'Устройство.tg.in_KL88',
                           'KL89': 'Устройство.tg.in_KL89',
                           'KL90': 'Устройство.tg.in_KL90',
                           'KL91': 'Устройство.tg.in_KL91',
                           'KL92': 'Устройство.tg.in_KL92',
                           'KL93': 'Устройство.tg.in_KL93',
                           'KL94': 'Устройство.tg.in_KL94',
                           'KL95': 'Устройство.tg.in_KL95',
                           'KL97': 'Устройство.tg.in_KL97',
                           'KL98': 'Устройство.tg.in_KL98',
                           'KL99': 'Устройство.tg.in_KL99',
                           'KL100': 'Устройство.tg.in_KL100',
                           'Q113_4': 'Устройство.tg.in_Q113_4',
                           'Q113_5': 'Устройство.tg.in_Q113_5',
                           'Q113_6': 'Устройство.tg.in_Q113_6',
                           'Q113_7': 'Устройство.tg.in_Q113_7'}

    def ctrl_read(self, relay: str):

        # position: list = []
        # tag_list = []
        read_tags = []
        read_tags.clear()

        # for j1 in args:
        tag = self.relay_dict[relay]
        print(tag)
        # self.logger.debug("старт считывания дискретных входов ПЛК")
        gr_ctrl = 'Устройство.tg.'
        read_tags = self.opc.read(tag, group=gr_ctrl, update=1, include_error=True)
        print(read_tags)
        self.opc.remove(gr_ctrl)
        # self.logger.debug(f'считанные значения {read_tags}')
        # if read_tags[0][2] != 'Good':
        #     self.logger.warning(f'качество сигнала {read_tags[0][2]}')
        #     raise ModbusConnectException("!!! Нет связи с контроллером !!! \nПроверьте подключение компьютера к "
        #                                  "шкафу \"Ethernet\" кабелем  и состояние OPC сервера.")
        # for k in range(len(args)):
        position = read_tags[0]
        return position


if __name__ == '__main__':
    try:
        read_mb = DIRead()
        # read_mb = ReadMB()
        # read_ctrl = CtrlRead()
        read_ai = AIRead()
        # st_timer = time()
        # a = read_mb.read_discrete(0)
        # b = read_mb.read_discrete(1)
        # c = read_mb.read_discrete(2)
        # d = read_mb.read_discrete(3)
        # e = read_mb.read_discrete(4)
        # f = read_mb.read_discrete(5)
        # g = read_mb.read_discrete(6)
        # h = read_mb.read_discrete(7)
        # j = read_mb.read_discrete(8)
        # k = read_mb.read_discrete(9)
        # l = read_mb.read_discrete(10)
        # q = read_mb.read_discrete(11)
        a, b, c = read_mb.di_read('in_a0', 'in_a1', 'in_a2')
        # a = read_mb.read_discrete_v1('in_a0')
        # a, b, c, d, e, f, g, h, j, k, l, q = read_mb.read_discrete_v1('in_a0', 'in_a1', 'in_a2', 'in_a3', 'in_a4',
        #                                                               'in_a5', 'in_a6', 'in_a7', 'in_b0', 'in_b1',
        #                                                               'in_b2', 'in_b3')
        # # stop_timer = time()
        # print(a, b, c, d, e, f, g, h, j, k, l, q)
        #
        # # print(a, b, c)
        # # print(a)
        # print(type(a))
        # print(stop_timer - st_timer)
        # in_1, in_5, in_6 = read_mb.inputs_a(1, 5, 6)
        # print(in_1, in_5, in_6)
        # read_mb.di_read('in_b1')
        for i in range(100):
            in_b1, *_ = read_mb.di_read('in_b1')
            print(in_b1)
        # # read_mb.di_read('in_a3')
        # in_a3, *_ = read_mb.di_read('in_a3')
        # print(in_a3)
    #     in_a0 = read_mb.read_discrete('inp_00')
    #     read_mb.di_read('in_a0', 'in_a1')
    #     read_mb.di_read('in_a0', 'in_a1', 'in_b0', 'in_a5')
    #     in_a0, in_a1, in_b0, in_a5 = read_mb.di_read('in_a0', 'in_a1', 'in_b0', 'in_a5')
    #     print(in_a0, in_a1, in_b0, in_a5)
        # in_a7, in_b3, in_b5, in_a6 = read_mb.di_read('in_a7', 'in_b3', 'in_b5', 'in_a6')
        # print(in_a7, in_b3, in_b5, in_a6)
        # in_a2, in_a4 = read_mb.di_read('in_a3', 'in_a4')
        # print(in_a3, in_a4)
        # print(in_a0, in_a1, in_b0, in_b1)
        # KL1 = read_ctrl.ctrl_read('KL1')
        # print(KL1)
        # st_time = time()
        # for i in range(20):
        #     ai0_res = read_ai.ai_read('AI0')
        #     ai2_res = read_ai.ai_read('AI2')
        #
        #     print(ai0_res)
        #     print(ai2_res)
        # stop_time = time()
        # print(stop_time - st_time)
        ai0 = read_ai.ai_read('AI0')
        ai2 = read_ai.ai_read('AI2')
        print(ai0, ai2)
    except IOError:
        print('системная ошибка')
    except ModbusConnectException as mce:
        print(mce)
    finally:
        print('finally: скрипт выполнен')
