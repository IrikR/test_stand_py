#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from OpenOPC import client
from time import sleep

__all__ = ['CtrlKL', 'ReadMB']

opc = client()
opc.connect('arOPC.arOpcServer.1')


class CtrlKL(object):
    """
    управление дискретными выходами контроллера через ModBus OPC Server
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
    relay = {'KL1': 'Устройство.tg.in_perekl_rejimov_KL1',
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

    list_relay = ('Устройство.tg.in_perekl_rejimov_KL1', 'Устройство.tg.in_power_18V_KL2',
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
                  'Устройство.tg.in_puskovoi_R_KL37','Устройство.tg.in_perv_obm_TV1_KL38',
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

    def ctrl_relay(self, rel, ctrl):
        # self.rel = rel
        # self.ctrl = ctrl
        # kl = self.relay.get(self.rel)
        kl = self.relay[f'{rel}']
        # opc[kl] = self.ctrl
        opc[kl] = ctrl

    def reset_all_v1(self):
        for i in range(len(self.list_relay)):
            kl = self.list_relay[i]
            # sleep(0.1)
            opc[kl] = False

    def reset_all_v2(self):
        kl = self.relay.keys()
        for i in kl:
            rele = self.relay[i]
            # sleep(0.1)
            opc[rele] = False

    def ctrl_ai_code_v0(self, code):
        """
        103 измерение времени переключения длительностью до 3000мс по входам а6 и б1
        104 измерение времени переключения длительностью до 100мс по входам а5 и б1
        105 измерение времени переключения длительностью до 300мс по входам а5 и б1
        109 измерение времени переключения длительностью до 500мс по входам а5 (False) и б1 (True)
        110 Запуск таймера происходит по условию замыкания DI.b1
            Остановка таймера происходит по условию размыкания DI.a5 T1[i]
            Пауза 500 мс
        111 измерение времени переключения длительностью до 1000мс по входам а1 (True) и b1 (True)
        :param code:
        :return:
        """
        self.code = code
        opc['Устройство.tegs.in_num_alg'] = self.code
        sleep(3)
        analog_tags_value = []
        analog_tags_value.append(opc.list('Устройство.tegs')[3])
        val = opc.read(analog_tags_value, update=1, include_error=True)
        conv_lst = ' '.join(map(str, val))
        list_str = conv_lst.split(', ', 5)
        list_str[0] = list_str[0][2:-1]
        if list_str[2] == "'Good'":
            analog_inp_fl = float(list_str[1])
        else:
            opc['Устройство.tegs.in_num_alg'] = 0
            return 9999
        opc['Устройство.tegs.in_num_alg'] = 0
        if analog_inp_fl <= 3000:
            return analog_inp_fl
        else:
            return 9999

    @staticmethod
    def ctrl_ai_code_100():
        """
        100 запуск счетчика импульсов БКИ-1Т
        :return: analog_inp_fl
        """
        opc['Устройство.tegs.in_num_alg'] = 100
        sleep(3)
        analog_tags_value = []
        analog_tags_value.append(opc.list('Устройство.tegs')[0])
        val = opc.read(analog_tags_value, update=1, include_error=True)
        conv_lst = ' '.join(map(str, val))
        list_str = conv_lst.split(', ', 5)
        list_str[0] = list_str[0][2:-1]
        if list_str[2] == "'Good'":
            pass
        else:
            opc['Устройство.tegs.in_num_alg'] = 0
            return 9999
        analog_inp_fl = float(list_str[1])
        opc['Устройство.tegs.in_num_alg'] = 0
        return analog_inp_fl

    @staticmethod
    def ctrl_ai_code_101():
        """
        101 запуск 1-го подтеста БКИ-6-ЗШ
        :return: analog_inp_fl
        """
        opc['Устройство.tegs.in_num_alg'] = 101
        sleep(21)
        analog_tags_value = []
        analog_tags_value.append(opc.list('Устройство.tegs')[1])
        val = opc.read(analog_tags_value, update=1, include_error=True)
        conv_lst = ' '.join(map(str, val))
        list_str = conv_lst.split(', ', 5)
        list_str[0] = list_str[0][2:-1]
        if list_str[2] == "'Good'":
            pass
        else:
            opc['Устройство.tegs.in_num_alg'] = 0
            return 9999
        analog_inp_fl = float(list_str[1])
        opc['Устройство.tegs.in_num_alg'] = 0
        return analog_inp_fl

    @staticmethod
    def ctrl_ai_code_102():
        """
        102 запуск 2-го подтеста БКИ-6-ЗШ
        :return: analog_inp_fl
        """
        opc['Устройство.tegs.in_num_alg'] = 102
        sleep(3)
        analog_tags_value = []
        analog_tags_value.append(opc.list('Устройство.tegs')[2])
        val = opc.read(analog_tags_value, update=1, include_error=True)
        conv_lst = ' '.join(map(str, val))
        list_str = conv_lst.split(', ', 5)
        list_str[0] = list_str[0][2:-1]
        if list_str[2] == "'Good'":
            pass
        else:
            opc['Устройство.tegs.in_num_alg'] = 0
            return 9999
        analog_inp_fl = float(list_str[1])
        opc['Устройство.tegs.in_num_alg'] = 0
        return analog_inp_fl

    def ctrl_ai_code_v1(self, code):
        """
        106 импульсно включает KL63 на 80мс
        107 импульсно включает KL63 на 500мс
        108 импульсно включает KL63 на 100мс
        :param code:
        :return:
        """
        self.code = code
        opc['Устройство.tegs.in_num_alg'] = self.code
        sleep(0.5)
        opc['Устройство.tegs.in_num_alg'] = 0


class ReadMB(object):
    """
    чтение регистров из ModBus OPC Server
    """

    def read_discrete(self, tag_index):
        self.tag_index = tag_index
        tags_value = []
        tags_value.append(opc.list('Выходы.inputs')[self.tag_index])
        val = opc.read(tags_value, update=1, include_error=True)
        conv_lst = ' '.join(map(str, val))
        list_str = conv_lst.split(', ', 5)
        list_str[0] = list_str[0][2:-1]
        if list_str[2] == "'Good'":
            return eval(list_str[1])
        else:
            return None

    # def read_discrete_v1(self, **kwargs):
    #     di = {'in_a0': 0, 'in_a1': 1, 'in_a2': 2, 'in_a3': 3, 'in_a4': 4, 'in_a5': 5, 'in_a6': 6, 'in_a7': 7,
    #           'in_b0': 8, 'in_b1': 9, 'in_b2': 10, 'in_b3': 11, 'in_b4': 12, 'in_b5': 13}
    #     tags_value = []
    #     tags_value.append(opc.list('Выходы.inputs')[self.tag_index])
    #     val = opc.read(tags_value, update=1, include_error=True)
    #     conv_lst = ' '.join(map(str, val))
    #     list_str = conv_lst.split(', ', 5)
    #     list_str[0] = list_str[0][2:-1]
    #     if list_str[2] == "'Good'":
    #         return eval(list_str[1])
    #     else:
    #         return None

    @staticmethod
    def read_analog():
        """
            #in_analog_real := INT_TO_REAL(#in_analog);
            #out_analog := ((#in_analog_real - #analog_min_code) * (#analog_max - #analog_min)) /
            (#analog_max_code - #analog_min_code) + #analog_min;
        :return:
        """
        analog_max_code = 27648.0
        # analog_min_code = 0
        analog_max = 400
        # analog_min = 0
        analog_tags_value = []
        analog_tags_value.append(opc.list('AI.AI')[0])
        val = opc.read(analog_tags_value, update=1, include_error=True)
        conv_lst = ' '.join(map(str, val))
        list_str = conv_lst.split(', ', 5)
        list_str[0] = list_str[0][2:-1]
        if list_str[2] == "'Good'":
            analog_inp_fl = float(list_str[1])
            # meas_volt = analog_inp_fl / 69.12
            # meas_volt = ((analog_inp_fl - analog_min_code) * (analog_max - analog_min)) / \
            #             (analog_max_code - analog_min_code) + analog_min
            meas_volt = analog_inp_fl * analog_max / analog_max_code
            return meas_volt
        else:
            return 999

    @staticmethod
    def read_analog_ai2():
        """
            #in_analog_real := INT_TO_REAL(#in_analog);
            #out_analog := ((#in_analog_real - #analog_min_code) * (#analog_max - #analog_min)) /
            (#analog_max_code - #analog_min_code) + #analog_min;
        :return:
        """
        analog_max_code = 27648.0
        analog_min_code = 0
        analog_max = 10
        analog_min = 0
        analog_tags_value = []
        analog_tags_value.append(opc.list('AI.AI')[2])
        val = opc.read(analog_tags_value, update=1, include_error=True)
        conv_lst = ' '.join(map(str, val))
        list_str = conv_lst.split(', ', 5)
        list_str[0] = list_str[0][2:-1]
        if list_str[2] == "'Good'":
            analog_inp_fl = float(list_str[1])
            # meas_volt = analog_inp_fl / 69.12
            meas_volt = ((analog_inp_fl - analog_min_code) * (analog_max - analog_min)) / \
                        (analog_max_code - analog_min_code) + analog_min
            return meas_volt
        else:
            return 999

    @staticmethod
    def read_uint_error_4():
        """
            считывание тега модбас error_4
        :return:
        """
        analog_tags_value = []
        analog_tags_value.append(opc.list('Устройство.tegs')[3])
        val = opc.read(analog_tags_value, update=1, include_error=True)
        conv_lst = ' '.join(map(str, val))
        list_str = conv_lst.split(', ', 5)
        list_str[0] = list_str[0][2:-1]
        if list_str[2] == "'Good'":
            analog_inp_fl = float(list_str[1])
            return analog_inp_fl
        else:
            return 999

    @staticmethod
    def read_uint_error_1():
        """
            считывание тега модбас error_4
        :return:
        """
        analog_tags_value = []
        analog_tags_value.append(opc.list('Устройство.tegs')[1])
        val = opc.read(analog_tags_value, update=1, include_error=True)
        conv_lst = ' '.join(map(str, val))
        list_str = conv_lst.split(', ', 5)
        list_str[0] = list_str[0][2:-1]
        if list_str[2] == "'Good'":
            analog_inp_fl = float(list_str[1])
            return analog_inp_fl
        else:
            return 999

    @staticmethod
    def read_uint_error_2():
        """
            считывание тега модбас error_4
        :return:
        """
        analog_tags_value = []
        analog_tags_value.append(opc.list('Устройство.tegs')[2])
        val = opc.read(analog_tags_value, update=1, include_error=True)
        conv_lst = ' '.join(map(str, val))
        list_str = conv_lst.split(', ', 5)
        list_str[0] = list_str[0][2:-1]
        if list_str[2] == "'Good'":
            analog_inp_fl = float(list_str[1])
            return analog_inp_fl
        else:
            return 999
