# -*- coding: utf-8 -*-
"""
Задание 7.1

Обработать строки из файла ospf.txt и вывести информацию по каждой строке в таком
виде на стандартный поток вывода:

Prefix                10.0.24.0/24
AD/Metric             110/41
Next-Hop              10.0.13.3
Last update           3d18h
Outbound Interface    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
result = {}

with open('ospf.txt') as f:
    for line in f:
        line = line.split()
        rt, ip, ad, via, nh, ttl, iface = line
        print("{:20} {:15}".format("Prefix", ip))
        print("{:20} {:15}".format("AD/Metric", ad[1:-1]))
        print("{:20} {:15}".format("Next-Hop", nh[0:-1]))
        print("{:20} {:15}".format("Last update", ttl[0:-1]))
        print("{:20} {:15}".format("Outbound Interface", iface))
        print("")

