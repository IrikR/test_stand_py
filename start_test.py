# -*- coding: UTF-8 -*-

import argparse
import textwrap

from new_alg import *
from old_alg import *


def create_parser():
    pars = argparse.ArgumentParser(
        prog='test stand',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
                     Программа по тестированию блоков защиты.
                     ---------------------------------------------------------------------------
                     Компания ООО \"Тор\" город Пермь.
                     Телефон номер:     +7
                     Электронная почта: info@tornaladka.ru
                     ---------------------------------------------------------------------------
                     Примеры использования:
                     python.exe .\start_test.py --block mtz --model 27
                        или
                     python.exe .\start_test.py --block bdu --model dr01
                        или
                     python.exe .\start_test.py --block tzp
                     '''),
        add_help=False
    )

    parent_group = pars.add_argument_group("параметры")
    parent_group.add_argument("-h", "--help", action="help", help="справка")

    parent_group.add_argument('--version', action='version', version='%(prog)s 0.4.0', help=' версия программы')

    parent_group.add_argument("-b", "--block", action="store",
                              help='''указание на тип блока:\
                               bdu >> БДУ, bdz >> БДЗ, bki >> БКИ, bkz >> БЛЯ, bmz >> БМЗ, bp >> БП, bru >> БРУ, 
                               btz >> БТЗ, 
                               bu >> БУ, bur >> БУР, buz >> БУЗ, bzmp >> БЗМП, mkzp >> МКЗП, mmtz >> ММТЗ, mtz >> МТЗ, 
                               mtzp >> МТЗП, pmz >> ПМЗ, tzp >> ТЗП, ubtz >> УБТЗ, umz >> УМЗ''',
                              choices=['bdu', 'bdz', 'bki', 'bkz', 'bmz', 'bp', 'bru', 'btz', 'bu', 'bur', 'buz',
                                       'bzmp', 'mkzp', 'mmtz', 'mtz', 'mtzp', 'pmz', 'tzp', 'ubtz', 'umz'],
                              dest="block",
                              metavar="тип блока")

    parent_group.add_argument('-m', '--model', action='store', dest='model',
                              help='''модель блока: 1 >> БДУ 1, 1m >> БДУ 1М, 42 >> БДУ 4-2, 43 >> БДУ 4-3, 
                              4 >> БДУ 4, t >> БДУ Т, p >> БДУ П, d42 >> БДУ Д4-2, d >> БДУ Д, dr01 >> БДУ ДР01, 
                              rt >> БДУ РТ,  >> БДУ, 1t >> БКИ 1Т, 2t >> БКИ 2Т, 6 >> БКИ 6-3Ш, p >> БКИ П, 2 >> БМЗ 2, 
                              apsh4 >> БМЗ АПШ-4, apshm >> БМЗ АПШ-М, 2s >> БРУ 2С, 2sr >> БРУ 2СР, 3 >> БТЗ 3, 
                              t >> БТЗ Т, apshm >> БУ АПШ-М, pmvir >> БУ ПМВИР, d >> БЗМП Д, p1 >> БЗМП П1, p >> БЗМП П, 
                              27 >> МТЗ 5 вар 2-7, 28 >> МТЗ 5 вар 2-8, 41 >> МТЗ 5 вар 4-11''',
                              metavar='модель блока',
                              choices=['1', '1m', '1t', '2', '27', '28', '2s', '2sr', '2t', '3', '4', '41', '42', '43',
                                       '6', 'apsh4', 'apshm', 'd', 'd42', 'dr01', 'p', 'p1', 'pmvir', 'rt', 't'])

    return pars.parse_args()


class BDU:
    """
    --block bdu >> БДУ
        --model 1    >> БДУ 1,
                1m   >> БДУ 1М,
                42   >> БДУ 4-2,
                43   >> БДУ 4-3,
                4    >> БДУ 4,
                t    >> БДУ Т,
                p    >> БДУ П,
                d42  >> БДУ Д4-2,
                d    >> БДУ Д,
                dr01 >> БДУ ДР01,
                rt   >> БДУ РТ,
                     >> БДУ
    """

    def __init__(self, model):
        self.model = model

    def handler_bdu(self):
        if self.model == "1":
            test_bdu_1 = alg_bdu_1.TestBDU1()
            test_bdu_1.full_test_bdu_1()
        elif self.model == "1m":
            test_bdu_1m = alg_bdu_1m_old.TestBDU1M()
            test_bdu_1m.full_test_bdu_1m()
        elif self.model == "42":
            test_bdu_4_2 = alg_bdu_4_2_old.TestBDU42()
            test_bdu_4_2.full_test_bdu_4_2()
        elif self.model == "43":
            test_bdu_4_3 = alg_bdu_4_3_old.TestBDU43()
            test_bdu_4_3.full_test_bdu_4_3()
        elif self.model == "4tp":
            test_bdu = alg_bdu_014tp.TestBDU014TP()
            test_bdu.full_test_bdu_014tp()
        elif self.model == "0":
            test_bdu = alg_bdu.TestBDU()
            test_bdu.full_test_bdu()
        elif self.model == "d42":
            test_bdu_d4_2 = alg_bdu_d4_2.TestBDUD42()
            test_bdu_d4_2.full_test_bdu_d4_2()
        elif self.model == "d":
            test_bdu = alg_bdu_d_old.TestBDUD()
            test_bdu.full_test_bdu_d()
        elif self.model == "dr01":
            test_bdu = alg_bdu_dr01_old.TestBDUDR01()
            test_bdu.full_test_bdu_dr01()
        elif self.model == "rt":
            test_bdu = alg_bdu_r_t_old.TestBDURT()
            test_bdu.full_test_bdu_r_t()


class BDZ:
    """
    --block bdz >> БДЗ
    """

    def __init__(self):
        pass

    @staticmethod
    def bdz():
        test_bdz = alg_bdz_old.TestBDZ()
        test_bdz.full_test_bdz()


class BKI:
    """
    --block bki >> БКИ
        --model 1t >> БКИ 1Т
                2t >> БКИ 2Т
                6  >> БКИ 6 3Ш
                p  >> БКИ П
    """

    def __init__(self, model):
        self.model = model

    def handler_bki(self):
        if self.model == "1t":
            test_bki = alg_bki_1t_old.TestBKI1T()
            test_bki.full_test_bki_1t()
        elif self.model == "2t":
            test_bki = alg_bki_2t_old.TestBKI2T()
            test_bki.full_test_bki_2t()
        elif self.model == "6":
            test_bki = alg_bki_6_3sh_old.TestBKI6()
            test_bki.full_test_bki_6_3sh()
        elif self.model == "p":
            test_bki = alg_bki_p_old.TestBKIP()
            test_bki.full_test_bki_p()


def bkz_3mk():
    test_bkz_3mk = alg_bkz_3mk.TestBKZ3MK()
    test_bkz_3mk.full_test_bkz_3mk()


class BMZ:
    """
    --block bmz >> БМЗ
        --model 2     >> БМЗ 2
                apsh4 >> БМЗ АПШ 4
                apshm >> БМЗ АПШ М
    """

    def __init__(self, model):
        self.model = model

    def handler_bmz(self):
        if self.model == "2":
            test_bmz = alg_bmz_2_old.TestBMZ2()
            test_bmz.full_test_bmz_2()
        elif self.model == "apsh4":
            test_bmz = alg_bmz_apsh_4_old.TestBMZAPSH4()
            test_bmz.full_test_bmz_apsh_4()
        elif self.model == "apshm":
            test_bmz = alg_bmz_apsh_m_old.TestBMZAPSHM()
            test_bmz.full_test_bmz_apsh_m()


def bp():
    test_bp = alg_bp_old.TestBP()
    test_bp.full_test_bp()


class BRU:
    """
    --block bru >> БРУ
        --model 2s  >> БРУ 2С
                2sr >> БРУ 2СР
    """

    def __init__(self, model):
        self.model = model

    def handler_bru(self):
        if self.model == "2s":
            test_bru = alg_bru_2s_old.TestBRU2S()
            test_bru.full_test_bru_2s()
        elif self.model == "2sr":
            test_bru = alg_bru_2sr_old.TestBRU2SR()
            test_bru.full_test_bru_2sr()


class BTZ:
    """
    --block btz >> БТЗ
        --model 3 >> БТЗ 3
                t >> БТЗ Т
    """

    def __init__(self, model):
        self.model = model

    def handler_btz(self):
        if self.model == "3":
            test_btz = alg_btz_3_old.TestBTZ3()
            test_btz.full_test_btz_3()
        elif self.model == "t":
            test_btz_t = alg_btz_t.TestBTZT()
            test_btz_t.full_test_btz_t()


class BU:
    """
    --block bu >> БУ
        --model apshm >> БУ АПШ-М
                pmvir >> БУ ПМВИР
    """

    def __init__(self, model):
        self.model = model

    def handler_bu(self):
        if self.model == "apshm":
            test_bu = alg_bu_apsh_m_old.TestBUAPSHM()
            test_bu.full_test_bu_apsh_m()
        elif self.model == "pmvir":
            test_bu = alg_bu_pmvir_old.TestBUPMVIR()
            test_bu.full_test_bu_pmvir()


def bur():
    test_bur = alg_bur_pmvir_old.TestBURPMVIR()
    test_bur.full_test_bur_pmvir()


def buz():
    test_buz = alg_buz_2_old.TestBUZ2()
    test_buz.full_test_buz_2()


class BZMP:
    """
    --block bzmp >> БЗМП
        --model d  >> БЗМП Д
                p1 >> БЗМП П1
                p  >> БЗМП П
    """

    def __init__(self, model):
        self.model = model

    def handler_bzmp(self):
        if self.model == "d":
            test_bzmp = alg_bzmp_d_old.TestBZMPD()
            test_bzmp.full_test_bzmp_d()
        elif self.model == "p1":
            test_bzmp = alg_bzmp_p1_old.TestBZMPP1()
            test_bzmp.full_test_bzmp_p1()
        elif self.model == "p":
            test_bzmp = alg_bzmp_p_old.TestBZMPP()
            test_bzmp.full_test_bzmp_p()


def mkzp():
    test_mkzp = alg_mkzp_6_4sh_old.TestMKZP6()
    test_mkzp.full_test_mkzp()


def mmtz():
    test_mmtz = alg_mmtz_d_old.TestMMTZD()
    test_mmtz.full_test_mmtz_d()


class MTZ:
    """
    --block mtz >> МТЗ
        --model 27 >> МТЗ 5 вар 2-7
                28 >> МТЗ 5 вар 2-8
                41 >> МТЗ 5 вар 4-11
    """

    def __init__(self, model):
        self.model = model

    def handler_mtz(self):
        if self.model == "27":
            test_mtz = alg_mtz_5_v2_7_old.TestMTZ5V27()
            test_mtz.full_test_mtz_5_v2_7()
        elif self.model == "28":
            test_mtz = alg_mtz_5_v2_8_old.TestMTZ5V28()
            test_mtz.full_test_mtz_5_v2_8()
        elif self.model == "41":
            test_mtz = alg_mtz_5_v4_11_old.TestMTZ5V411()
            test_mtz.full_test_mtz_5_v4_11()


def mtzp():
    test_mtzp = alg_mtzp_2_old.TestMTZP2()
    test_mtzp.full_test_mtzp_2()


def pmz():
    test_pmz = alg_pmz_old.TestPMZ()
    test_pmz.full_test_pmz()


def tzp():
    test_tzp = alg_tzp.TestTZP()
    test_tzp.full_test_tzp()


def ubtz():
    test_ubtz = alg_ubtz_old.TestUBTZ()
    test_ubtz.full_test_ubtz()


def umz():
    test_umz = alg_umz_old.TestUMZ()
    test_umz.full_test_umz()


def handler():
    arg = create_parser()
    if arg.block == "bdu":
        if arg.model is None:
            BDU("0").handler_bdu()
        elif arg.model == "1":
            BDU("1").handler_bdu()
        elif arg.model == "1m":
            BDU("1m").handler_bdu()
        elif arg.model == "42":
            BDU("42").handler_bdu()
        elif arg.model == "43":
            BDU("43").handler_bdu()
        elif arg.model == "4" or arg.model == "t" or arg.model == "p":
            BDU("4tp").handler_bdu()
        elif arg.model == "d42":
            BDU("d42").handler_bdu()
        elif arg.model == "d":
            BDU("d").handler_bdu()
        elif arg.model == "dr01":
            BDU("dr01").handler_bdu()
        elif arg.model == "rt":
            BDU("rt").handler_bdu()
        else:
            print(BDU.__doc__)
    elif arg.block == "bdz":
        BDZ.bdz()
    elif arg.block == "bki":
        if arg.model == "1t":
            BKI("1t").handler_bki()
        elif arg.model == "2t":
            BKI("2t").handler_bki()
        elif arg.model == "6":
            BKI("6").handler_bki()
        elif arg.model == "p":
            BKI("p").handler_bki()
        else:
            print(BKI.__doc__)
    elif arg.block == "bkz":
        bkz_3mk()
    elif arg.block == "bmz":
        if arg.model == "2":
            BMZ("2").handler_bmz()
        elif arg.model == "apsh4":
            BMZ("apsh4").handler_bmz()
        elif arg.model == "apshm":
            BMZ("apshm").handler_bmz()
        else:
            print(BMZ.__doc__)
    elif arg.block == "bp":
        bp()
    elif arg.block == "bru":
        if arg.model == "2s":
            BRU("2s").handler_bru()
        elif arg.model == "2sr":
            BRU("2sr").handler_bru()
        else:
            print(BRU.__doc__)
    elif arg.block == "btz":
        if arg.model == "3":
            BTZ("3").handler_btz()
        elif arg.model == "t":
            BTZ("t").handler_btz()
        else:
            print(BTZ.__doc__)
    elif arg.block == "bu":
        if arg.model == "apshm":
            BU("apshm").handler_bu()
        elif arg.model == "pmvir":
            BU("pmvir").handler_bu()
        else:
            print(BU.__doc__)
    elif arg.block == "bur":
        bur()
    elif arg.block == "buz":
        buz()
    elif arg.block == "bzmp":
        if arg.model == "d":
            BZMP("d").handler_bzmp()
        elif arg.model == "p1":
            BZMP("p1").handler_bzmp()
        elif arg.model == "p":
            BZMP("p").handler_bzmp()
        else:
            print(BZMP.__doc__)
    elif arg.block == "mkzp":
        mkzp()
    elif arg.block == "mmtz":
        mmtz()
    elif arg.block == "mtz":
        if arg.model == "27":
            MTZ("27").handler_mtz()
        elif arg.model == "28":
            MTZ("28").handler_mtz()
        elif arg.model == "41":
            MTZ("41").handler_mtz()
        else:
            print(MTZ.__doc__)
    elif arg.block == "mtzp":
        mtzp()
    elif arg.block == "pmz":
        pmz()
    elif arg.block == "tzp":
        tzp()
    elif arg.block == "ubtz":
        ubtz()
    elif arg.block == "umz":
        umz()
    else:
        print(help)


if __name__ == '__main__':
    handler()
