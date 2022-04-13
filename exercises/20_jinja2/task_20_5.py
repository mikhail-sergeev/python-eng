# -*- coding: utf-8 -*-
"""
Задание 20.5

Создать шаблоны templates/gre_ipsec_vpn_1.txt и templates/gre_ipsec_vpn_2.txt,
которые генерируют конфигурацию IPsec over GRE между двумя маршрутизаторами.

Шаблон templates/gre_ipsec_vpn_1.txt создает конфигурацию для одной стороны туннеля,
а templates/gre_ipsec_vpn_2.txt - для второй.

Примеры итоговой конфигурации, которая должна создаваться на основе шаблонов в файлах:
cisco_vpn_1.txt и cisco_vpn_2.txt.

Шаблоны надо создавать вручную, скопировав части конфига в соответствующие шаблоны.

Создать функцию create_vpn_config, которая использует эти шаблоны
для генерации конфигурации VPN на основе данных в словаре data.

Параметры функции:
* template1 - имя файла с шаблоном, который создает конфигурацию для одной строны туннеля
* template2 - имя файла с шаблоном, который создает конфигурацию для второй строны туннеля
* data_dict - словарь со значениями, которые надо подставить в шаблоны

Функция должна возвращать кортеж с двумя конфигурациями (строки),
которые получены на основе шаблонов.

Примеры конфигураций VPN, которые должна возвращать функция create_vpn_config в файлах
cisco_vpn_1.txt и cisco_vpn_2.txt.
"""
from pprint import pprint

import yaml
from jinja2 import Environment, FileSystemLoader

data = {
    "tun_num": 10,
    "wan_ip_1": "192.168.100.1",
    "wan_ip_2": "192.168.100.2",
    "tun_ip_1": "10.0.1.1 255.255.255.252",
    "tun_ip_2": "10.0.1.2 255.255.255.252",
}

def create_vpn_config(template1, template2, data_dict):
    templ_dir = template1.split("/")[0]
    templ1_file = template1.split("/")[1]
    templ2_file = template2.split("/")[1]
    env = Environment(loader=FileSystemLoader(templ_dir), trim_blocks=True)
    t1 = env.get_template(templ1_file)
    t2 = env.get_template(templ2_file)
    conf1 = t1.render(data_dict)
    conf2 = t2.render(data_dict)
    return conf1,conf2

# так должен выглядеть вызов функции
if __name__ == "__main__":
    template1_file = "templates/gre_ipsec_vpn_1.txt"
    template2_file = "templates/gre_ipsec_vpn_2.txt"
    pprint(create_vpn_config(template1_file, template2_file, data))
