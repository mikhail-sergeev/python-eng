# -*- coding: utf-8 -*-
"""
Задание 9.3a

Сделать копию функции get_int_vlan_map из задания 9.3.

Дополнить функцию: добавить поддержку конфигурации, когда настройка access-порта
выглядит так:
    interface FastEthernet0/20
        switchport mode access
        duplex auto

То есть, порт находится в VLAN 1

В таком случае, в словарь портов должна добавляться информация, что порт в VLAN 1
Пример словаря:
    {'FastEthernet0/12': 10,
     'FastEthernet0/14': 11,
     'FastEthernet0/20': 1 }

У функции должен быть один параметр config_filename, который ожидает
как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw2.txt

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
            if cif and cmode and line == "!":
                paccess[cif] = 1
                cmode = ""
            if cif and cmode and ctvlan:
                vl = []
                for v in ctvlan.split(","):
                    vl.append(int(v))
                ptrunk[cif] = vl
                cmode = ""

    return paccess, ptrunk


print(get_int_vlan_map("config_sw2.txt"))
