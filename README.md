![tor_logo_small.svg](tor_logo_small.svg)

ООО "ТОР"

+ website [https://tornaladka.ru/](https://tornaladka.ru/)
+ email [info@tornaladka.ru](mailto:info@tornaladka.ru)

> ---
![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/IrikR/test_stand_py?color=blue)
![GitHub](https://img.shields.io/github/license/irikr/test_stand_py?color=blue)
> ---
# Алгоритмы проверки блоков управления и защиты шахтных аппаратов

## Типы проверяемых блоков:
БДУ-4-2, БДУ-4-3, БДУ-Д, БДУ-Р-Т, БДУ, БДУ-1, БДУ-4, БДУ-Т, БДУ-П Х5-01, БДУ-П УХЛ 01, БДУ-П УХЛ5-03, БКИ-1, БКИ-Т, БКИ-2Т, БКИ, БКИ-П, БРУ-2С, БРУ-2СР, БУ АПШ.М, БУ ПМВИР (пускатель), БУР ПМВИР (пускатель), БДУ-1М, БДУ-Д4-2, БДУ-Д.01, БДУ-ДР.01, БКЗ-ЗМК, БКЗ-Д, БКЗ-З, БКИ-6-3Ш, БМЗ-2, БМЗ АПШ 4.0, БМЗ АПШ.М, БТЗ-3, БТЗ-Т, ММТЗ-Д, МТЗ-5 вер.2-7/0.4-2, МТЗ-5 вер.2-8/0.8-3, МТЗ-5 вер.411256002, УБТЗ, УМЗ, ПМЗ, ПМЗ-П, ТЗП, ТЗП-П

### Запуск алгоритмов
+ Вариант 1:
  > python.exe из директории в которой находится скрипты
  ```commandline
  python.exe .\test_bdu_1_class.py
  ```
+ Вариант 2:
  > Из директории в которой находится скрипт start_test.py 
  > python.exe .\start_test.py --block наименование_блока -m модель_блока
  ```commandline
  python.exe .\start_test.py --block mtz -m 27
  ```
> Для детального описания по скрипту start_test.py 
```commandline
python.exe .\start_test.py --help
```

Для запуска нового алгоритма вместо старого, необходимо открыть файл с именем `test_*_class.py`,
```python
from old_alg.alg_bdu_1m_old import TestBDU1M
# from new_alg.alg_bdu_1m import TestBDU1M


def bdu_1m():
    test_bdu_1m = TestBDU1M()
    test_bdu_1m.full_test_bdu_1m()
```
и раскоментировать строку начинающуюся со слов `from new_alg`, и закоментировать строку начинающуюся со
слов `from old_alg`
```python
# from old_alg.alg_bdu_1m_old import TestBDU1M
from new_alg.alg_bdu_1m import TestBDU1M


def bdu_1m():
    test_bdu_1m = TestBDU1M()
    test_bdu_1m.full_test_bdu_1m()
```
таким образом будет произведен вызов обновленного алгоритма проверки.
Скрипт _start_test.py_ запускает только обновленные версии.