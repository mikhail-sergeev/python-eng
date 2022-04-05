# -*- coding: utf-8 -*-
"""
Задание 17.3

Создать функцию parse_sh_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

Функция ожидает, как аргумент, вывод команды одной строкой (не имя файла).
Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.


Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt
"""
from pprint import pprint


def parse_sh_cdp_neighbors(command_output):
    result = {}
    device = ""
    stage = 0
    for line in command_output.split("\n"):
        if ">" in line and stage == 0:
            device = line.split(">")[0]
            stage = 1
            continue
        if "Device" in line and stage == 1:
            stage = 2
            continue
        if stage == 2 and line.strip():
            router,int1,int2,ttl,*other = line.split()
            *other,model,int3,int4 = line.split()
            inp = f"{int1} {int2}"
            outp = {router: f"{int3} {int4}"}
            result[inp] = outp
    return {device: result}


if __name__ == "__main__":
    with open("sh_cdp_n_sw1.txt") as f:
        pprint(parse_sh_cdp_neighbors(f.read()))
