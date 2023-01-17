# -*- coding: utf-8 -*-
"""
Подключение к OPC серверу.

Список тегов дискретных входов контроллера:
    'in_a0': 'Выходы.inputs.inp_00', 'in_a1': 'Выходы.inputs.inp_01',
    'in_a2': 'Выходы.inputs.inp_02', 'in_a3': 'Выходы.inputs.inp_03',
    'in_a4': 'Выходы.inputs.inp_04', 'in_a5': 'Выходы.inputs.inp_05',
    'in_a6': 'Выходы.inputs.inp_06', 'in_a7': 'Выходы.inputs.inp_07',
    'in_b0': 'Выходы.inputs.inp_08', 'in_b1': 'Выходы.inputs.inp_09',
    'in_b2': 'Выходы.inputs.inp_10', 'in_b3': 'Выходы.inputs.inp_11',
    'in_b4': 'Выходы.inputs.inp_12', 'in_b5': 'Выходы.inputs.inp_13',
    'in_b6': 'Выходы.inputs.inp_14', 'in_b7': 'Выходы.inputs.inp_15'

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

Пример использования внешнего модуля OpenOPC
    from OpenOPC import client
    opc = client()
    opc.connect('arOPC.arOpcServer.1')
    gr_di = 'Выходы.inputs.'
    args = (f"{gr_di}inp_00", f'{gr_di}inp_01')
    read_tags = opc.read(args, group=gr_di, update=1, include_error=True)
    print(read_tags)
    opc.remove(gr_di)
"""

__all__ = ["ConnectOPC"]

import logging
from time import sleep

from OpenOPC import client

from .database import MySQLConnect
from .exception import ModbusConnectException
from .rw_result import RWError, WriteCondition
from .utils import CLILog


class ConnectOPC:
    _instances = None

    def __new__(cls, *args, **kwargs):
        if cls._instances is None:
            cls._instances = super().__new__(cls)

        return cls._instances
    def __del__(self):
        ConnectOPC._instances = None

    def __init__(self):
        self.opc = client()
        self.opc.connect('arOPC.arOpcServer.1')
        self.rw_error = RWError()
        self.wr_cond = WriteCondition()
        self.mysql_conn = MySQLConnect()
        self.logger = logging.getLogger(__name__)
        self.cli_log = CLILog("info", __name__)

        self.tags_list = ['Выходы.inputs.inp_00', 'Выходы.inputs.inp_01',
                          'Выходы.inputs.inp_02', 'Выходы.inputs.inp_03',
                          'Выходы.inputs.inp_04', 'Выходы.inputs.inp_05',
                          'Выходы.inputs.inp_06', 'Выходы.inputs.inp_07',
                          'Выходы.inputs.inp_08', 'Выходы.inputs.inp_09',
                          'Выходы.inputs.inp_10', 'Выходы.inputs.inp_11',
                          'Выходы.inputs.inp_12', 'Выходы.inputs.inp_13',
                          'Выходы.inputs.inp_14', 'Выходы.inputs.inp_15']
        self.dic_relay = {'KL1': 'Устройство.tg.in_perekl_rejimov_KL1',
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
        self.list_relay = ('Устройство.tg.in_perekl_rejimov_KL1', 'Устройство.tg.in_power_18V_KL2',
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
        self.list_relay_true = (('Устройство.tg.in_perekl_rejimov_KL1', True),
                                ('Устройство.tg.in_power_18V_KL2', True),
                                ('Устройство.tg.in_R1_KL3', True),
                                ('Устройство.tg.in_R2_KL4', True),
                                ('Устройство.tg.in_R3_KL5', True),
                                ('Устройство.tg.in_R4_KL6', True),
                                ('Устройство.tg.in_R5_KL7', True),
                                ('Устройство.tg.in_R6_KL8', True),
                                ('Устройство.tg.in_R7_KL9', True),
                                ('Устройство.tg.in_R8_KL10', True),
                                ('Устройство.tg.in_KZ_KL11', True),
                                ('Устройство.tg.in_pusk_KL12', True),
                                ('Устройство.tg.in_R10_KL13', True),
                                ('Устройство.tg.in_R11_KL14', True),
                                ('Устройство.tg.in_R12_KL15', True),
                                ('Устройство.tg.in_R13_KL16', True),
                                ('Устройство.tg.in_R14_KL17', True),
                                ('Устройство.tg.in_R15_KL18', True),
                                ('Устройство.tg.in_R16_KL19', True),
                                ('Устройство.tg.in_R17_KL20', True),
                                ('Устройство.tg.in_power_36V_KL21', True),
                                ('Устройство.tg.in_perekl_KI_BKI_KL22', True),
                                ('Устройство.tg.in_perekl_660V_1140V_KL23', True),
                                ('Устройство.tg.in_shunt_D_KL24', True),
                                ('Устройство.tg.in_R_shunt_KL25', True),
                                ('Устройство.tg.in_DU_KL26', True),
                                ('Устройство.tg.in_cont_ser_KT_KL27', True),
                                ('Устройство.tg.in_perek_18V_KL28', True),
                                ('Устройство.tg.in_KL29', True),
                                ('Устройство.tg.in_power_KT_KL30', True),
                                ('Устройство.tg.in_perekl_kanalov_KL31', True),
                                ('Устройство.tg.in_power_110V_KL32', True),
                                ('Устройство.tg.in_power_15V_KL33', True),
                                ('Устройство.tg.in_power_48V_KL36', True),
                                ('Устройство.tg.in_puskovoi_R_KL37', True),
                                ('Устройство.tg.in_perv_obm_TV1_KL38', True),
                                ('Устройство.tg.in_perv_obm_TV1_KL39', True),
                                ('Устройство.tg.in_perv_obm_TV1_KL40', True),
                                ('Устройство.tg.in_perv_obm_TV1_KL41', True),
                                ('Устройство.tg.in_perv_obm_TV1_KL42', True),
                                ('Устройство.tg.in_perv_obm_TV1_KL43', True),
                                ('Устройство.tg.in_perv_obm_TV1_KL44', True),
                                ('Устройство.tg.in_perv_obm_TV1_KL45', True),
                                ('Устройство.tg.in_perv_obm_TV1_KL46', True),
                                ('Устройство.tg.in_perv_obm_TV1_KL47', True),
                                ('Устройство.tg.in_vtor_obm_TV1_KL48', True),
                                ('Устройство.tg.in_vtor_obm_TV1_KL49', True),
                                ('Устройство.tg.in_vtor_obm_TV1_KL50', True),
                                ('Устройство.tg.in_vtor_obm_TV1_KL51', True),
                                ('Устройство.tg.in_vtor_obm_TV1_KL52', True),
                                ('Устройство.tg.in_vtor_obm_TV1_KL53', True),
                                ('Устройство.tg.in_vtor_obm_TV1_KL54', True),
                                ('Устройство.tg.in_vtor_obm_TV1_KL55', True),
                                ('Устройство.tg.in_vtor_obm_TV1_KL56', True),
                                ('Устройство.tg.in_vtor_obm_TV1_KL57', True),
                                ('Устройство.tg.in_vtor_obm_TV1_KL58', True),
                                ('Устройство.tg.in_vtor_obm_TV1_KL59', True),
                                ('Устройство.tg.in_KZ_obmotka_KL60', True),
                                ('Устройство.tg.in_perv_gl_kont_KL62', True),
                                ('Устройство.tg.in_vtor_gl_kont_KL63', True),
                                ('Устройство.tg.in_KL65', True),
                                ('Устройство.tg.in_power_12V_KL66', True),
                                ('Устройство.tg.in_KL67', True),
                                ('Устройство.tg.in_KL68', True),
                                ('Устройство.tg.in_KL69', True),
                                ('Устройство.tg.in_KL88', True),
                                ('Устройство.tg.in_KL71', True),
                                ('Устройство.tg.in_KL72', True),
                                ('Устройство.tg.in_rejim_AB_VG_KL73', True),
                                ('Устройство.tg.in_rejim_rabor_KL74', True),
                                ('Устройство.tg.in_KL75', True),
                                ('Устройство.tg.in_KL76', True),
                                ('Устройство.tg.in_KL77', True),
                                ('Устройство.tg.in_KL78', True),
                                ('Устройство.tg.in_KL79', True),
                                ('Устройство.tg.in_KL80', True),
                                ('Устройство.tg.in_KL81', True),
                                ('Устройство.tg.in_KL82', True),
                                ('Устройство.tg.in_KL83', True),
                                ('Устройство.tg.in_KL84', True),
                                ('Устройство.tg.in_KL88', True),
                                ('Устройство.tg.in_KL89', True),
                                ('Устройство.tg.in_KL90', True),
                                ('Устройство.tg.in_KL91', True),
                                ('Устройство.tg.in_KL92', True),
                                ('Устройство.tg.in_KL93', True),
                                ('Устройство.tg.in_KL94', True),
                                ('Устройство.tg.in_KL95', True),
                                ('Устройство.tg.in_KL97', True),
                                ('Устройство.tg.in_KL98', True),
                                ('Устройство.tg.in_KL99', True),
                                ('Устройство.tg.in_KL100', True),
                                ('Устройство.tg.in_Q113_4', True),
                                ('Устройство.tg.in_Q113_5', True),
                                ('Устройство.tg.in_Q113_6', True),
                                ('Устройство.tg.in_Q113_7', True))
        self.list_relay_false = (('Устройство.tg.in_perekl_rejimov_KL1', False),
                                 ('Устройство.tg.in_power_18V_KL2', False),
                                 ('Устройство.tg.in_R1_KL3', False),
                                 ('Устройство.tg.in_R2_KL4', False),
                                 ('Устройство.tg.in_R3_KL5', False),
                                 ('Устройство.tg.in_R4_KL6', False),
                                 ('Устройство.tg.in_R5_KL7', False),
                                 ('Устройство.tg.in_R6_KL8', False),
                                 ('Устройство.tg.in_R7_KL9', False),
                                 ('Устройство.tg.in_R8_KL10', False),
                                 ('Устройство.tg.in_KZ_KL11', False),
                                 ('Устройство.tg.in_pusk_KL12', False),
                                 ('Устройство.tg.in_R10_KL13', False),
                                 ('Устройство.tg.in_R11_KL14', False),
                                 ('Устройство.tg.in_R12_KL15', False),
                                 ('Устройство.tg.in_R13_KL16', False),
                                 ('Устройство.tg.in_R14_KL17', False),
                                 ('Устройство.tg.in_R15_KL18', False),
                                 ('Устройство.tg.in_R16_KL19', False),
                                 ('Устройство.tg.in_R17_KL20', False),
                                 ('Устройство.tg.in_power_36V_KL21', False),
                                 ('Устройство.tg.in_perekl_KI_BKI_KL22', False),
                                 ('Устройство.tg.in_perekl_660V_1140V_KL23', False),
                                 ('Устройство.tg.in_shunt_D_KL24', False),
                                 ('Устройство.tg.in_R_shunt_KL25', False),
                                 ('Устройство.tg.in_DU_KL26', False),
                                 ('Устройство.tg.in_cont_ser_KT_KL27', False),
                                 ('Устройство.tg.in_perek_18V_KL28', False),
                                 ('Устройство.tg.in_KL29', False),
                                 ('Устройство.tg.in_power_KT_KL30', False),
                                 ('Устройство.tg.in_perekl_kanalov_KL31', False),
                                 ('Устройство.tg.in_power_110V_KL32', False),
                                 ('Устройство.tg.in_power_15V_KL33', False),
                                 ('Устройство.tg.in_power_48V_KL36', False),
                                 ('Устройство.tg.in_puskovoi_R_KL37', False),
                                 ('Устройство.tg.in_perv_obm_TV1_KL38', False),
                                 ('Устройство.tg.in_perv_obm_TV1_KL39', False),
                                 ('Устройство.tg.in_perv_obm_TV1_KL40', False),
                                 ('Устройство.tg.in_perv_obm_TV1_KL41', False),
                                 ('Устройство.tg.in_perv_obm_TV1_KL42', False),
                                 ('Устройство.tg.in_perv_obm_TV1_KL43', False),
                                 ('Устройство.tg.in_perv_obm_TV1_KL44', False),
                                 ('Устройство.tg.in_perv_obm_TV1_KL45', False),
                                 ('Устройство.tg.in_perv_obm_TV1_KL46', False),
                                 ('Устройство.tg.in_perv_obm_TV1_KL47', False),
                                 ('Устройство.tg.in_vtor_obm_TV1_KL48', False),
                                 ('Устройство.tg.in_vtor_obm_TV1_KL49', False),
                                 ('Устройство.tg.in_vtor_obm_TV1_KL50', False),
                                 ('Устройство.tg.in_vtor_obm_TV1_KL51', False),
                                 ('Устройство.tg.in_vtor_obm_TV1_KL52', False),
                                 ('Устройство.tg.in_vtor_obm_TV1_KL53', False),
                                 ('Устройство.tg.in_vtor_obm_TV1_KL54', False),
                                 ('Устройство.tg.in_vtor_obm_TV1_KL55', False),
                                 ('Устройство.tg.in_vtor_obm_TV1_KL56', False),
                                 ('Устройство.tg.in_vtor_obm_TV1_KL57', False),
                                 ('Устройство.tg.in_vtor_obm_TV1_KL58', False),
                                 ('Устройство.tg.in_vtor_obm_TV1_KL59', False),
                                 ('Устройство.tg.in_KZ_obmotka_KL60', False),
                                 ('Устройство.tg.in_perv_gl_kont_KL62', False),
                                 ('Устройство.tg.in_vtor_gl_kont_KL63', False),
                                 ('Устройство.tg.in_KL65', False),
                                 ('Устройство.tg.in_power_12V_KL66', False),
                                 ('Устройство.tg.in_KL67', False),
                                 ('Устройство.tg.in_KL68', False),
                                 ('Устройство.tg.in_KL69', False),
                                 ('Устройство.tg.in_KL88', False),
                                 ('Устройство.tg.in_KL71', False),
                                 ('Устройство.tg.in_KL72', False),
                                 ('Устройство.tg.in_rejim_AB_VG_KL73', False),
                                 ('Устройство.tg.in_rejim_rabor_KL74', False),
                                 ('Устройство.tg.in_KL75', False),
                                 ('Устройство.tg.in_KL76', False),
                                 ('Устройство.tg.in_KL77', False),
                                 ('Устройство.tg.in_KL78', False),
                                 ('Устройство.tg.in_KL79', False),
                                 ('Устройство.tg.in_KL80', False),
                                 ('Устройство.tg.in_KL81', False),
                                 ('Устройство.tg.in_KL82', False),
                                 ('Устройство.tg.in_KL83', False),
                                 ('Устройство.tg.in_KL84', False),
                                 ('Устройство.tg.in_KL88', False),
                                 ('Устройство.tg.in_KL89', False),
                                 ('Устройство.tg.in_KL90', False),
                                 ('Устройство.tg.in_KL91', False),
                                 ('Устройство.tg.in_KL92', False),
                                 ('Устройство.tg.in_KL93', False),
                                 ('Устройство.tg.in_KL94', False),
                                 ('Устройство.tg.in_KL95', False),
                                 ('Устройство.tg.in_KL97', False),
                                 ('Устройство.tg.in_KL98', False),
                                 ('Устройство.tg.in_KL99', False),
                                 ('Устройство.tg.in_KL100', False),
                                 ('Устройство.tg.in_Q113_4', False),
                                 ('Устройство.tg.in_Q113_5', False),
                                 ('Устройство.tg.in_Q113_6', False),
                                 ('Устройство.tg.in_Q113_7', False))
        self.list_perv_obm_tv1_off = (('Устройство.tg.in_perv_obm_TV1_KL38', False),
                                      ('Устройство.tg.in_perv_obm_TV1_KL39', False),
                                      ('Устройство.tg.in_perv_obm_TV1_KL40', False),
                                      ('Устройство.tg.in_perv_obm_TV1_KL41', False),
                                      ('Устройство.tg.in_perv_obm_TV1_KL42', False),
                                      ('Устройство.tg.in_perv_obm_TV1_KL43', False),
                                      ('Устройство.tg.in_perv_obm_TV1_KL44', False),
                                      ('Устройство.tg.in_perv_obm_TV1_KL45', False),
                                      ('Устройство.tg.in_perv_obm_TV1_KL46', False),
                                      ('Устройство.tg.in_perv_obm_TV1_KL47', False))
        self.list_vtor_obm_tv_off = (('Устройство.tg.in_vtor_obm_TV1_KL48', False),
                                     ('Устройство.tg.in_vtor_obm_TV1_KL49', False),
                                     ('Устройство.tg.in_vtor_obm_TV1_KL50', False),
                                     ('Устройство.tg.in_vtor_obm_TV1_KL51', False),
                                     ('Устройство.tg.in_vtor_obm_TV1_KL52', False),
                                     ('Устройство.tg.in_vtor_obm_TV1_KL53', False),
                                     ('Устройство.tg.in_vtor_obm_TV1_KL54', False),
                                     ('Устройство.tg.in_vtor_obm_TV1_KL55', False),
                                     ('Устройство.tg.in_vtor_obm_TV1_KL56', False),
                                     ('Устройство.tg.in_vtor_obm_TV1_KL57', False),
                                     ('Устройство.tg.in_vtor_obm_TV1_KL58', False),
                                     ('Устройство.tg.in_vtor_obm_TV1_KL59', False),
                                     ('Устройство.tg.in_KZ_obmotka_KL60', False))

        self.tags_value = []
        self.analog_tags_value = []
        self.result: list[str] = []

    def read_group_di(self) -> {str, bool}:
        """
        Считывает из OPC сервера состояния тегов, дискретных входов ПЛК

        :return position: {str, bool} возвращает словарь из значений {название тега, состояние}
        """
        position: dict = {}
        read_tags = []
        read_tags.clear()

        self.logger.debug("старт считывания дискретных входов ПЛК")
        self.cli_log.lev_debug("старт считывания дискретных входов ПЛК", "gray")
        gr_di = 'Выходы.inputs'
        read_tags = self.opc.read(self.tags_list, group=gr_di, update=1, include_error=True)
        self.opc.remove(gr_di)
        self.logger.debug(f'считанные значения {read_tags}')
        self.cli_log.lev_debug(f'считанные значения {read_tags}', "gray")
        if read_tags[0][2] == "Good":
            self.logger.info(f'качество дискретных сигналов {read_tags[0][2]}')
            self.cli_log.lev_info(f'качество дискретных сигналов {read_tags[0][2]}', "green")
        else:
            self.logger.warning(f'качество дискретных сигналов {read_tags[0][2]}')
            self.cli_log.lev_warning(f'качество дискретных сигналов {read_tags[0][2]}', "red")
            raise ModbusConnectException("!!! Нет связи с контроллером !!! \nПроверьте подключение компьютера к "
                                         "шкафу \"Ethernet\" кабелем  и состояние OPC сервера.")
        for k in read_tags:
            name = k[0].split(".")[2]
            position[name] = k[1]
        return position

    def subtest_read_di(self, *, test_num: int = 1, subtest_num: float = 1, err_code: [int],
                        position_inp: [bool], di_xx: [str]) -> bool:
        """
        Метод используется в алгоритмах у которых только один вход,
        для следующих используется вход in_a1
        общий тест для bdu_4_3, bdu_014tp, bdu, bdu_d, bru_2s, bu_pmvir
        для следующих используется вход in_a2
        общий тест для
        Код ошибки	30	–	Сообщение	«Блок не исправен. Контакты блока находятся в неисходном состоянии»
        :param test_num: int Номер теста
        :param subtest_num: float Номер подтеста
        :param err_code: [int] код неисправности
        :param position_inp: [bool] положение которое должен занять выход блока
        :param di_xx: [str] вход контроллера
        :return:
        """
        self.logger.debug(f"считывание дискретных входов. функция subtest_1di")
        self.cli_log.lev_debug(f"считывание дискретных входов. функция subtest_1di", "gray")
        self.wr_cond.write_condition(test_num, subtest_num)
        position_read = self.read_group_di()

        self.logger.debug(f"состояние входа: {position_read}")
        self.cli_log.lev_debug(f"состояние входа: {position_read}", "gray")
        k = 0
        for i in di_xx:
            if position_inp[k] is position_read[i]:
                self.result.append(f"{i}: должно быть: {position_inp[k]}, получили: {position_read[i]}")
                k += 1
                continue
            else:
                self.result.append(f"{i}: должно быть: {position_inp[k]}, получили: {position_read[i]}")
                self.rw_error.rw_err(err_code[k])
                self.wr_cond.write_condition_false(test_num, subtest_num)
                self.logger.debug(f"{self.result}")
                self.cli_log.lev_info(f"{self.result}", "skyblue")
                return False
        self.logger.debug(f"{self.result}")
        self.cli_log.lev_info(f"{self.result}", "skyblue")
        self.wr_cond.write_condition_true(test_num, subtest_num)
        self.result.clear()
        return True

    def simplified_read_di(self, di_a: [str]) -> [bool]:
        """
        Функция для чтения дискретных входов OPC сервера по заданному списку,
        и выдача результатов считывания
        :param di_a: [str] - Список входов контроллера
        :return []: [bool]
        """
        position_result: [bool] = []

        self.logger.debug(f"считывание дискретных входов. функция subtest_1di")
        self.cli_log.lev_debug(f"считывание дискретных входов. функция subtest_1di", "gray")
        position_read = self.read_group_di()
        self.logger.debug(f"состояние входа: {position_read}")
        self.cli_log.lev_debug(f"состояние входа: {position_read}", "gray")
        for i in di_a:
             position_result.append(position_read[i])

        return position_result

    def ctrl_relay(self, rel: str, ctrl: bool) -> None:
        """
        Функция для воздействия на конкретное реле
        :param rel: str сокращенное название реле
        :param ctrl: bool состояние в которое должен переключится
        :return: None
        """
        kl = self.dic_relay[f'{rel}']
        send_tuple = (kl, ctrl)
        self.opc.write(send_tuple)
        self.opc.remove(send_tuple)

    def _full_relay_on(self):
        """
        !!! НЕ ИСПОЛЬЗОВАТЬ !!!
        Функция включает все реле.
        """
        self.opc.write(self.list_relay_true)

    def full_relay_off(self):
        """
        Функция отключает все реле.
        """
        self.logger.debug("отключение всех реле")
        self.cli_log.lev_info("отключение всех реле", "gray")
        self.opc.write(self.list_relay_false)
        self.logger.debug("все реле отключены")
        self.cli_log.lev_info("все реле отключены", "gray")

    def perv_obm_tv1_off(self) -> None:
        self.logger.debug("отключение реле первичной обмотки")
        self.cli_log.lev_debug("отключение реле первичной обмотки", "gray")
        self.opc.write(self.list_perv_obm_tv1_off)
        self.logger.debug("реле первичной обмотки отключены")
        self.cli_log.lev_debug("реле первичной обмотки отключены", "gray")

    def vtor_obm_tv1_off(self) -> None:
        self.logger.debug("отключение реле вторичной обмотки")
        self.cli_log.lev_debug("отключение реле вторичной обмотки", "gray")
        self.opc.write(self.list_vtor_obm_tv_off)
        self.logger.debug("реле вторичной обмотки отключены")
        self.cli_log.lev_debug("реле вторичной обмотки отключены", "gray")

    def ctrl_ai_code_v0(self, code: int) -> [float, bool, bool, bool, bool]:
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
        :return analog_inp_fl: float
        :return in_a1: bool вход 1
        :return in_a2: bool вход 2
        :return in_a5: bool вход 5
        :return in_a6: bool вход 6
        """
        tags_list = ["inp_01", "inp_02", "inp_05", "inp_06"]

        self.opc['Устройство.tegs.in_num_alg'] = code
        sleep(3)

        in_a1, in_a2, in_a5, in_a6 = self.simplified_read_di(tags_list)
        self.analog_tags_value.append(self.opc.list('Устройство.tegs')[3])
        val = self.opc.read(self.analog_tags_value, update=1, include_error=True)
        conv_lst = ' '.join(map(str, val))
        list_str = conv_lst.split(', ', 5)
        list_str[0] = list_str[0][2:-1]
        if list_str[2] == "'Good'":
            pass
        else:
            self.opc['Устройство.tegs.in_num_alg'] = 0
            self.logger.warning(f'качество сигнала ctrl_ai_code_v0 {list_str[2]}')
            self.cli_log.lev_info(f'качество сигнала ctrl_ai_code_v0 {list_str[2]}', "orange")
            raise ModbusConnectException("!!! Нет связи с контроллером !!! \nПроверьте подключение компьютера к "
                                         "шкафу \"Ethernet\" кабелем  и состояние OPC сервера.")

        analog_inp_fl = float(list_str[1])
        self.logger.info(f"ctrl_ai_code_v0 время срабатывания: {analog_inp_fl}")
        self.cli_log.lev_info(f"ctrl_ai_code_v0 время срабатывания: {analog_inp_fl}", "orange")
        self.opc['Устройство.tegs.in_num_alg'] = 0
        self.logger.debug(f"ctrl_ai_code_v0 дискретные входы: {in_a1 =}, {in_a2 =}, {in_a5 =}, {in_a6 =}")
        self.cli_log.lev_info(f"ctrl_ai_code_v0 дискретные входы: {in_a1 =}, {in_a2 =}, {in_a5 =}, {in_a6 =}", "skyblue")
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
            self.cli_log.lev_info(f'качество сигнала ctrl_ai_code_v0 {list_str[2]}', "orange")
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
            self.cli_log.lev_info(f'качество сигнала ctrl_ai_code_v0 {list_str[2]}', "orange")
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
            self.cli_log.lev_info(f'качество сигнала ctrl_ai_code_v0 {list_str[2]}', "orange")
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
            self.cli_log.lev_info(f'качество сигнала read_uint_error_4 {list_str[2]}', "red")
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
            self.cli_log.lev_info(f'качество сигнала read_uint_error_1 {list_str[2]}', "red")
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
            self.cli_log.lev_info(f'качество сигнала read_uint_error_2 {list_str[2]}', "red")
            raise ModbusConnectException("!!! Нет связи с контроллером !!! \nПроверьте подключение компьютера к "
                                         "шкафу \"Ethernet\" кабелем  и состояние OPC сервера.")
        analog_inp_fl = float(list_str[1])
        return analog_inp_fl

    def read_ai(self, teg: str) -> float:
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
        self.cli_log.lev_info("старт считывания аналоговых входов ПЛК", "gray")

        gr_ai = 'AI.AI.'
        read_tags = self.opc.read(ai_teg_list, group=gr_ai, update=1, include_error=True)
        self.opc.remove(gr_ai)
        self.logger.info(f'считанные значения {read_tags}')
        self.cli_log.lev_info(f'считанные значения {read_tags}', "orange")
        if read_tags[0][2] == 'Good':
            pass
        else:
            self.logger.warning(f'качество аналогового сигнала {read_tags[1]}')
            self.cli_log.lev_info(f'качество аналогового сигнала {read_tags[1]}', "red")
            raise ModbusConnectException("!!! Нет связи с контроллером !!! \nПроверьте подключение компьютера к "
                                         "шкафу \"Ethernet\" кабелем  и состояние OPC сервера.")
        analog_inp_ai0 = read_tags[0][1]
        analog_inp_ai2 = read_tags[1][1]
        if teg == 'AI0':
            calc_volt = analog_inp_ai0 * analog_max_ai0 / analog_max_code
            self.logger.info(f'возврат результата AI0 = {calc_volt}')
            self.cli_log.lev_info(f'возврат результата AI0 = {calc_volt}', "orange")
            return calc_volt
        elif teg == 'AI2':
            calc_volt = analog_inp_ai2 * analog_max_ai2 / analog_max_code
            self.logger.info(f'возврат результата AI2 = {calc_volt}')
            self.cli_log.lev_info(f'возврат результата AI2 = {calc_volt}', "orange")
            return calc_volt
        else:
            self.logger.info(f'возврат результата (небыл получен аргумент) = {analog_inp_ai0}')
            self.cli_log.lev_info(f'возврат результата (небыл получен аргумент) = {analog_inp_ai0}', "orange")
            return analog_inp_ai0

    def opc_close(self):
        self.opc.close('arOPC.arOpcServer.1')
