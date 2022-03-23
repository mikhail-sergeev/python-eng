# -*- coding: utf-8 -*-
"""
Задание 9.3

Создать функцию get_int_vlan_map, которая обрабатывает конфигурационный
файл коммутатора и возвращает кортеж из двух словарей:
* словарь портов в режиме access, где ключи номера портов,
  а значения access VLAN (числа):
{'FastEthernet0/12': 10,
 'FastEthernet0/14': 11,
 'FastEthernet0/16': 17}

* словарь портов в режиме trunk, где ключи номера портов,
  а значения список разрешенных VLAN (список чисел):
{'FastEthernet0/1': [10, 20],
 'FastEthernet0/2': [11, 30],
 'FastEthernet0/4': [17]}

У функции должен быть один параметр config_filename, который ожидает как аргумент
имя конфигурационного файла.

Проверить работу функции на примере файла config_sw1.txt

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

def get_int_vlan_map(config_filename):
    paccess = {}
    ptrunk = {}
    cif = ""
    cmode = ""
    ctvlan = ""
    cavlan = ""
    with open(config_filename) as f:
        for line in f:
            if "interface" in line:
                cif = line.split()[1]
                cmode = ""
                ctvlan = ""
                cavlan = ""
            if "switchport mode" in line:
                cmode = line.split()[2]
            if "switchport access vlan" in line:
                cavlan = line.split()[3]
            if "switchport trunk allowed vlan" in line:
                ctvlan = line.split()[4]
            if cif and cmode and cavlan:
                paccess[cif] = int(cavlan)
                cmode = ""
            if cif and cmode and ctvlan:
                vl = []
                for v in ctvlan.split(","):
                    vl.append(int(v))
                ptrunk[cif] = vl
                cmode = ""

    return paccess, ptrunk


print(get_int_vlan_map("config_sw1.txt"))
