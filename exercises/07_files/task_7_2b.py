# -*- coding: utf-8 -*-
"""
Задание 7.2b

Переделать скрипт из задания 7.2a: вместо вывода на стандартный поток вывода,
скрипт должен записать полученные строки в файл

Имена файлов нужно передавать как аргументы скрипту:
 * имя исходного файла конфигурации
 * имя итогового файла конфигурации

При этом, должны быть отфильтрованы строки, которые содержатся в списке ignore
и строки, которые начинаются на '!'.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

from sys import argv

ignore = ["duplex", "alias", "configuration"]
conf = argv[1]
conf_new = argv[2]

with open(conf) as f, open(conf_new, 'w') as f2:
    c = f.read().rstrip().split('\n')
    for line in c:
        if line[0] != "!":
            ign = False
            for i in ignore:
                if i in line:
                    ign = True
            if not ign:
                f2.write(line+"\n")
