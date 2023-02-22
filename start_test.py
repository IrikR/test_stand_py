# -*- coding: UTF-8 -*-

import argparse
import textwrap

from new_alg import *
from new_alg.try_except import TryExcept


def create_parser():
    """

    """
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
        self.try_except = TryExcept()

    def handler_bdu(self):
        if self.model == "1":
            test_bdu_1 = alg_bdu_1.TestBDU1()
            self.try_except.full_start_test(test_bdu_1.st_test_bdu_1, None, 0)
        elif self.model == "1m":
            test_bdu_1m = alg_bdu_1m.TestBDU1M()
            self.try_except.full_start_test(test_bdu_1m.st_test_bdu_1m, None, 0)
        elif self.model == "42":
            test_bdu_4_2 = alg_bdu_4_2.TestBDU42()
            self.try_except.full_start_test(test_bdu_4_2.st_test_bdu_4_2, None, 0)
        elif self.model == "43":
            test_bdu_4_3 = alg_bdu_4_3.TestBDU43()
            self.try_except.full_start_test(test_bdu_4_3.st_test_bdu_4_3, None, 0)
        elif self.model == "4tp":
            test_bdu = alg_bdu_014tp.TestBDU014TP()
            self.try_except.full_start_test(test_bdu.st_test_bdu_014tp, None, 0)
        elif self.model == "0":
            test_bdu = alg_bdu.TestBDU()
            self.try_except.full_start_test(test_bdu.st_test_bdu, None, 0)
        elif self.model == "d42":
            test_bdu_d4_2 = alg_bdu_d4_2.TestBDUD42()
            self.try_except.full_start_test(test_bdu_d4_2.st_test_bdu_d4_2, None, 0)
        elif self.model == "d":
            test_bdu = alg_bdu_d.TestBDUD()
            self.try_except.full_start_test(test_bdu.st_test_bdu_d, None, 0)
        elif self.model == "dr01":
            test_bdu = alg_bdu_dr01.TestBDUDR01()
            self.try_except.full_start_test(test_bdu.st_test_bdu_dr01, None, 0)
        elif self.model == "rt":
            test_bdu = alg_bdu_r_t.TestBDURT()
            self.try_except.full_start_test(test_bdu.st_test_bdu_r_t, None, 0)


class BDZ:
    """
    --block bdz >> БДЗ
    """

    def __init__(self):
        self.try_except = TryExcept()

    def bdz(self):
        test_bdz = alg_bdz.TestBDZ()
        self.try_except.full_start_test(test_bdz.st_test_bdz, None, 0)


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
        self.try_except = TryExcept()

    def handler_bki(self):
        if self.model == "1t":
            test_bki = alg_bki_1t.TestBKI1T()
            self.try_except.full_start_test(test_bki.st_test_bki_1t, None, 0)
        elif self.model == "2t":
            test_bki = alg_bki_2t.TestBKI2T()
            self.try_except.full_start_test(test_bki.st_test_bki_2t, None, 0)
        elif self.model == "6":
            test_bki = alg_bki_6_3sh.TestBKI6()
            self.try_except.full_start_test(test_bki.st_test_bki_6_3sh, None, 0)
        elif self.model == "p":
            test_bki = alg_bki_p.TestBKIP()
            self.try_except.full_start_test(test_bki.st_test_bki_p, None, 0)


class BKZ:

    def __init__(self):
        self.try_except = TryExcept()

    def bkz_3mk(self):
        test_bkz_3mk = alg_bkz_3mk.TestBKZ3MK()
        self.try_except.full_start_test(test_bkz_3mk.st_test_bkz_3mk, test_bkz_3mk.result_test_bkz_3mk, 2)


class BMZ:
    """
    --block bmz >> БМЗ
        --model 2     >> БМЗ 2
                apsh4 >> БМЗ АПШ 4
                apshm >> БМЗ АПШ М
    """

    def __init__(self, model):
        self.model = model
        self.try_except = TryExcept()

    def handler_bmz(self):
        if self.model == "2":
            test_bmz = alg_bmz_2.TestBMZ2()
            self.try_except.full_start_test(test_bmz.st_test_bmz_2, test_bmz.result_test_bmz_2, 1)
        elif self.model == "apsh4":
            test_bmz = alg_bmz_apsh_4.TestBMZAPSH4()
            self.try_except.full_start_test(test_bmz.st_test_bmz_apsh_4, None, 1)
        elif self.model == "apshm":
            test_bmz = alg_bmz_apsh_m.TestBMZAPSHM()
            self.try_except.full_start_test(test_bmz.st_test_bmz_apsh_m, None, 1)


class BP:

    def __init__(self):
        self.try_except = TryExcept()

    def bp(self):
        test_bp = alg_bp.TestBP()
        self.try_except.full_start_test(test_bp.st_test_bp, None, 0)


class BRU:
    """
    --block bru >> БРУ
        --model 2s  >> БРУ 2С
                2sr >> БРУ 2СР
    """

    def __init__(self, model):
        self.model = model
        self.try_except = TryExcept()

    def handler_bru(self):
        if self.model == "2s":
            test_bru = alg_bru_2s.TestBRU2S()
            self.try_except.full_start_test(test_bru.st_test_bru_2s, None, 0)
        elif self.model == "2sr":
            test_bru = alg_bru_2sr.TestBRU2SR()
            self.try_except.full_start_test(test_bru.st_test_bru_2sr, None, 0)


class BTZ:
    """
    --block btz >> БТЗ
        --model 3 >> БТЗ 3
                t >> БТЗ Т
    """

    def __init__(self, model):
        self.model = model
        self.try_except = TryExcept()

    def handler_btz(self):
        if self.model == "3":
            test_btz = alg_btz_3.TestBTZ3()
            self.try_except.full_start_test(test_btz.st_test_btz_3, test_btz.result_test_btz_3, 1)
        elif self.model == "t":
            test_btz_t = alg_btz_t.TestBTZT()
            self.try_except.full_start_test(test_btz_t.st_test_btz_t, test_btz_t.result_test_btz_t, 2)


class BU:
    """
    --block bu >> БУ
        --model apshm >> БУ АПШ-М
                pmvir >> БУ ПМВИР
    """

    def __init__(self, model):
        self.model = model
        self.try_except = TryExcept()

    def handler_bu(self):
        if self.model == "apshm":
            test_bu = alg_bu_apsh_m.TestBUAPSHM()
            self.try_except.full_start_test(test_bu.st_test_bu_apsh_m, None, 0)
        elif self.model == "pmvir":
            test_bu = alg_bu_pmvir.TestBUPMVIR()
            self.try_except.full_start_test(test_bu.st_test_bu_pmvir, None, 0)


class BUR:

    def __init__(self):
        self.try_except = TryExcept()

    def bur(self):
        test_bur = alg_bur_pmvir.TestBURPMVIR()
        self.try_except.full_start_test(test_bur.st_test_bur_pmvir, None, 0)


class BUZ:

    def __init__(self):
        self.try_except = TryExcept()

    def buz(self):
        test_buz = alg_buz_2.TestBUZ2()
        self.try_except.full_start_test(test_buz.st_test_buz_2, None, 1)


class BZMP:
    """
    --block bzmp >> БЗМП
        --model d  >> БЗМП Д
                p1 >> БЗМП П1
                p  >> БЗМП П
    """

    def __init__(self, model):
        self.model = model
        self.try_except = TryExcept()

    def handler_bzmp(self):
        if self.model == "d":
            test_bzmp = alg_bzmp_d.TestBZMPD()
            self.try_except.full_start_test(test_bzmp.st_test_bzmp_d, None, 1)
        elif self.model == "p1":
            test_bzmp = alg_bzmp_p1.TestBZMPP1()
            self.try_except.full_start_test(test_bzmp.st_test_bzmp_p1, None, 1)
        elif self.model == "p":
            test_bzmp = alg_bzmp_p.TestBZMPP()
            self.try_except.full_start_test(test_bzmp.st_test_bzmp_p, None, 1)


class MKZP:

    def __init__(self):
        self.try_except = TryExcept()

    def mkzp(self):
        test_mkzp = alg_mkzp_6_4sh.TestMKZP6()
        self.try_except.full_start_test(test_mkzp.st_test_mkzp_6_4sh, None, 1)


class MMTZ:

    def __init__(self):
        self.try_except = TryExcept()

    def mmtz(self):
        test_mmtz = alg_mmtz_d.TestMMTZD()
        self.try_except.full_start_test(test_mmtz.st_test_mmtz_d, None, 1)


class MTZ:
    """
    --block mtz >> МТЗ
        --model 27 >> МТЗ 5 вар 2-7
                28 >> МТЗ 5 вар 2-8
                41 >> МТЗ 5 вар 4-11
    """

    def __init__(self, model):
        self.model = model
        self.try_except = TryExcept()

    def handler_mtz(self):
        if self.model == "27":
            test_mtz = alg_mtz_5_v2_7.TestMTZ5V27()
            self.try_except.full_start_test(test_mtz.st_test_mtz_5_v2_7, test_mtz.result_test_mtz, 1)
        elif self.model == "28":
            test_mtz = alg_mtz_5_v2_8.TestMTZ5V28()
            self.try_except.full_start_test(test_mtz.st_test_mtz, test_mtz.result_test_mtz, 1)
        elif self.model == "41":
            test_mtz = alg_mtz_5_v4_11.TestMTZ5V411()
            self.try_except.full_start_test(test_mtz.st_test_mtz, test_mtz.result_test_mtz, 1)


class MTZP:

    def __init__(self):
        self.try_except = TryExcept()

    def mtzp(self):
        test_mtzp = alg_mtzp_2.TestMTZP2()
        self.try_except.full_start_test(test_mtzp.st_test_mtzp_2, None, 1)


class PMZ:

    def __init__(self):
        self.try_except = TryExcept()

    def pmz(self):
        test_pmz = alg_pmz.TestPMZ()
        self.try_except.full_start_test(test_pmz.st_test_pmz, test_pmz.result_test_pmz, 1)


class TZP:

    def __init__(self):
        self.try_except = TryExcept()

    def tzp(self):
        test_tzp = alg_tzp.TestTZP()
        self.try_except.full_start_test(test_tzp.st_test_tzp, test_tzp.result_test_tzp, 1)


class UBTZ:

    def __init__(self):
        self.try_except = TryExcept()

    def ubtz(self):
        test_ubtz = alg_ubtz.TestUBTZ()
        self.try_except.full_start_test(test_ubtz.st_test_ubtz, test_ubtz.result_test_ubtz, 1)


class UMZ:

    def __init__(self):
        self.try_except = TryExcept()

    def umz(self):
        test_umz = alg_umz.TestUMZ()
        self.try_except.full_start_test(test_umz.st_test_umz, test_umz.result_test_umz, 1)


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
        BDZ().bdz()
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
        BKZ().bkz_3mk()
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
        BP().bp()
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
        BUR().bur()
    elif arg.block == "buz":
        BUZ().buz()
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
        MKZP().mkzp()
    elif arg.block == "mmtz":
        MMTZ().mmtz()
    elif arg.block == "mtz":
        if arg.model == "27":
            MTZ("27").handler_mtz()
        elif arg.model == "28":
            MTZ("28").handler_mtz()
        elif arg.model == "41":
            MTZ("41").handler_mtz()
        else:
            print(MTZ("err").__doc__)
    elif arg.block == "mtzp":
        MTZP().mtzp()
    elif arg.block == "pmz":
        PMZ().pmz()
    elif arg.block == "tzp":
        TZP().tzp()
    elif arg.block == "ubtz":
        UBTZ().ubtz()
    elif arg.block == "umz":
        UMZ().umz()
    else:
        print("используйте:\n python.exe .\start_test.py --help \n для получения справки")


if __name__ == '__main__':
    handler()
