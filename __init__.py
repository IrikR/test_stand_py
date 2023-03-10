#!/usr/bin/env python 3
# -*- coding: utf-8 -*-

"""
алгоритмы проверки блоков защит:
    Тип блока	            Производитель
    БДУ-4-2                 Нет производителя, ДонЭнергоЗавод, ИТЭП
    БДУ-4-3	                Без Производителя, Углеприбор
    БДУ-Д	                ДИГ
    БДУ-Р-Т	                Нет производителя, ТЭТЗ-Инвест, Стройэнергомаш
    БДУ	                    Без Производителя, Углеприбор
    БДУ-1	                Без Производителя, Углеприбор
    БДУ-4	                Без Производителя, Углеприбор
    БДУ-Т	                Без Производителя, Углеприбор, ТЭТЗ-Инвест, Строй-ЭнергоМаш
    БДУ-П Х5-01	            Пульсар
    БДУ-П УХЛ 01	        Пульсар
    БДУ-П УХЛ5-03	        Пульсар
    БКИ-1	                нет производителя, Углеприбор
    БКИ-Т	                нет производителя, Углеприбор, ТЭТЗ-Инвест, СтройЭнергоМаш
    БКИ-2Т	                нет производителя, ТЭТЗ-Инвест, Строй-энерго
    БКИ	                    нет производителя, Углеприбор
    БКИ-П	                Пульсар
    БРУ-2С	                Нет производителя
    БРУ-2СР	                Нет производителя
    БУ АПШ.М	            Без Производителя, Горэкс-Светотехника
    БУ ПМВИР (пускатель)	Без Производителя
    БУР ПМВИР (пускатель)	Нет производителя
    БДУ-1М	                Нет производителя, Пульсар
    БДУ-Д4-2	            Нет производителя, ДонЭнергоЗавод
    БДУ-Д.01	            Без Производителя
    БДУ-ДР.01	            Нет производителя, ДонЭнергоЗавод
    БКЗ-3МК	                Без Производителя, ДонЭнергоЗавод, ИТЭП
    БКЗ-Д	                Без Производителя, ДонЭнергоЗавод
    БКЗ-З	                Без Производителя, ДонЭнергоЗавод, ИТЭП
    БКИ-6-3Ш
    БМЗ-2	                Нет производителя, ТЭТЗ-Инвест, Строй-энергомаш
    БМЗ АПШ 4.0	            Нет производителя, Горэкс-Светотехника
    БМЗ АПШ.М	            Нет производителя, Электроаппарат-Развитие
    БТЗ-3	                Нет производителя, ТЭТЗ-Инвест, Строй-энергомаш, Углеприбор
    БТЗ-Т                   Нет производителя, ТЭТЗ-Инвест, Строй-энергомаш, Углеприбор
    ММТЗ-Д	                Нет производителя, ДонЭнергоЗавод
    МТЗ-5 вер.2-7/0.4-2	    Электромашина
    МТЗ-5 вер.2-8/0.8-3	    Электромашина
    МТЗ-5 вер.411256002	    Электромашина
    УБТЗ                    Нет производителя, Горэкс-Светотехника
    УМЗ                     Нет производителя
    ПМЗ                     Нет производителя, Углеприбор
    ПМЗ-П                   Нет производителя, Пульсар
    ТЗП                     Нет производителя, Углеприбор
    ТЗП-П                   Нет производителя, Пульсар
    БДЗ                     нет производителя, Строй-энергомаш, ТЭТЗ-Инвест
    БЗМП-П                  Пульсар
    БЗМП-П1                 Пульсар
    БП                      нет производителя, Строй-энергомаш, ТЭТЗ-Инвест
    БУЗ-2                   нет производителя, Строй-энергомаш, ТЭТЗ-Инвест
    БЗМП-Д                  ДИГ, ООО
    МТЗП-2
    МКЗП-6-4Ш

"""

__version__ = '0.5.0'

__all__ = ("new_alg", "old_alg", "test_bdu_1_class", "test_bdu_1m_class", "test_bdu_4_2_class",
           "test_bdu_4_3_class", "test_bdu_014tp_class", "test_bdu_d4_2_class", "test_bdu_d_class",
           "test_bdu_dr01_class", "test_bdu_r_t_class", "test_bdz_class", "test_bki_1t_class", "test_bki_2t_class",
           "test_bki_6_3sh_class", "test_bki_p_class", "test_bkz_3mk_class", "test_bmz_2_class", "test_btz_3_class",
           "test_btz_t_class", "test_buz_2_class", "test_bp_class", "test_tzp_class", "test_pmz_class",
           "test_ubtz_class", "test_umz_class", "test_mtzp_2_class", "test_mtz_5_v2_7_class", "test_mtz_5_v2_8_class",
           "test_mmtz_d_class", "test_bzmp_d_class", "test_bzmp_p1_class", "test_bzmp_p_class", "test_bru_2s_class",
           "test_bru_2sr_class", "test_bu_pmvir_class", "test_bur_pmvir_class", "test_mtz_5_v4_11_class",
           "test_bu_apsh_m_class", "test_bmz_apsh_4_class", "test_bmz_apsh_m_class", "test_mkzp_6_4sh_class")

__author__ = '<konstantin.devyaterikov@tornaladka.ru>' \
             '<osiris365@gmail.com>, ' \
             '<vladilen.aborin@tornaladka.ru>, '
