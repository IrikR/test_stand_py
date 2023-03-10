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

### Обновление алгоритмов проверки блоков:
1. скачать архив [алгоритмы проверки](https://github.com/IrikR/test_stand_py/archive/refs/heads/master.zip);
2. распаковать архив в любую временную директорию;
3. зайти в директорию с распакованным архивом, выделить все файлы и директории и скопировать;
4. зайти в директорию C:\Stend\project_class\;
5. выделить все файлы и директории, и удалить;
6. вставить скопированные файлы;

### Запуск алгоритмов
+ Вариант 1:
  > python.exe из директории в которой находится скрипты
  ```commandline
  python.exe .\test_bdu_1_class.py
  ```
+ Вариант 2:
  > Из директории в которой находится скрипт _start_test.py_ 
  > _python.exe .\start_test.py --block наименование_блока -m модель_блока_
  ```commandline
  python.exe .\start_test.py --block mtz -m 27
  ```
> Для детального описания по скрипту _start_test.py_ 
```commandline
python.exe .\start_test.py --help
```

Для запуска нового алгоритма вместо старого, необходимо открыть файл с именем `test_*_class.py`,
```python
from old_alg.alg_bdu_dr01_old import TestBDUDR01
# from new_alg.alg_bdu_dr01 import TestBDUDR01
# from new_alg.try_except import TryExcept

def bdu_dr01():
    test_bdu = TestBDUDR01()
    test_bdu.full_test_bdu_dr01()

# def bdu_dr01():
#     try_except = TryExcept()
#     test_bdu = TestBDUDR01()
#     try_except.full_start_test(test_bdu.st_test_bdu_dr01, None, 0)


if __name__ == "__main__":
    bdu_dr01()
```
и раскоментировать строку начинающуюся со слов `from new_alg`, и закоментировать строку начинающуюся со
слов `from old_alg`
```python
# from old_alg.alg_bdu_dr01_old import TestBDUDR01
from new_alg.alg_bdu_dr01 import TestBDUDR01
from new_alg.try_except import TryExcept

# def bdu_dr01():
#     test_bdu = TestBDUDR01()
#     test_bdu.full_test_bdu_dr01()

def bdu_dr01():
    try_except = TryExcept()
    test_bdu = TestBDUDR01()
    try_except.full_start_test(test_bdu.st_test_bdu_dr01, None, 0)


if __name__ == "__main__":
    bdu_dr01()
```
таким образом будет произведен вызов обновленного алгоритма проверки.
Скрипт _start_test.py_ запускает только обновленные версии.

Компиляция скриптов.

Для компиляции всех скриптов необходимо вызвать программу _compileall.py_, которая находится в директории **Lib** 
интерпретатора **Python**, в моем случае это _C:\Python39_x32\Lib\compileall.py_, и указать полный путь к директории 
в которой находятся скрипты, опять же в моем случае это _"D:\python_dev\dev_python_398_x32\test_stand_all_version\proj
ect_class\"_.
```commandline
C:\Python39_x32\Lib\compileall.py D:\python_dev\dev_python_398_x32\test_stand_all_version\project_class\
```
При удачном компилировании будет выведено следующее (в моем же случае)
```commandline
Compiling 'D:\\python_dev\\dev_python_398_x32\\test_stand_all_version\\project_class\\test_ubtz_class.py'...
Compiling 'D:\\python_dev\\dev_python_398_x32\\test_stand_all_version\\project_class\\test_umz_class.py'...
```
