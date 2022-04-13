# -*- coding: utf-8 -*-
"""
Задание 20.5a

Создать функцию configure_vpn, которая использует
шаблоны из задания 20.5 для настройки VPN на маршрутизаторах
на основе данных в словаре data.

Параметры функции:
* src_device_params - словарь с параметрами подключения к устройству 1
* dst_device_params - словарь с параметрами подключения к устройству 2
* src_template - имя файла с шаблоном, который создает конфигурацию для строны 1
* dst_template - имя файла с шаблоном, который создает конфигурацию для строны 2
* vpn_data_dict - словарь со значениями, которые надо подставить в шаблоны

Функция должна настроить VPN на основе шаблонов
и данных на каждом устройстве с помощью netmiko.
Функция возвращает кортеж с выводом команд с двух
маршрутизаторов (вывод, которые возвращает метод netmiko send_config_set).
Первый элемент кортежа - вывод с первого устройства (строка),
второй элемент кортежа - вывод со второго устройства.

При этом, в словаре data не указан номер интерфейса Tunnel,
который надо использовать.
Номер надо определить самостоятельно на основе информации с оборудования.
Если на маршрутизаторе нет интерфейсов Tunnel,
взять номер 0, если есть взять ближайший свободный номер,
но одинаковый для двух маршрутизаторов.

Например, если на маршрутизаторе src такие интерфейсы: Tunnel1, Tunnel4.
А на маршрутизаторе dest такие: Tunnel2, Tunnel3, Tunnel8.
Первый свободный номер одинаковый для двух маршрутизаторов будет 5.
И надо будет настроить интерфейс Tunnel 5.

Для этого задания тест проверяет работу функции на первых двух устройствах
из файла devices.yaml. И проверяет, что в выводе есть команды настройки
интерфейсов, но при этом не проверяет настроенные номера тунелей и другие команды.
Они должны быть, но тест упрощен, чтобы было больше свободы выполнения.
"""
from pprint import pprint
import logging

from task_20_5 import create_vpn_config
import yaml
import re
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

regex = r'Tu(\d+)'
'''
data = {
    "tun_num": None,
    "wan_ip_1": "192.168.100.1",
    "wan_ip_2": "192.168.100.2",
    "tun_ip_1": "10.0.1.1 255.255.255.252",
    "tun_ip_2": "10.0.1.2 255.255.255.252",
}
'''
data = {
    "tun_num": None,
    "wan_ip_1": "80.241.1.1",
    "wan_ip_2": "90.18.10.2",
    "tun_ip_1": "10.255.1.1 255.255.255.252",
    "tun_ip_2": "10.255.1.2 255.255.255.252",
}


def send_show_command(dev, command):
    try:
        with ConnectHandler(**dev) as ssh:
            ssh.enable()
            output = ssh.send_command(command)
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)
    return output

def send_config_commands(device, config_commands):
    output = ""
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            output += ssh.send_config_set(config_commands)
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)
    return output

def configure_vpn(src_device_params, dst_device_params, src_template, dst_template, vpn_data_dict):
    logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
    if_list1 = send_show_command(src_device_params,"sh int descr")
    if_list2 = send_show_command(dst_device_params,"sh int descr")
    reg1 = re.findall(regex,if_list1)
    reg2 = re.findall(regex,if_list2)
    tunnel_all = list(range(0,4096))
    for num in reg1:
        dnum = int(num)
        if dnum in tunnel_all:
            tunnel_all.remove(dnum)
    for num in reg2:
        dnum = int(num)
        if dnum in tunnel_all:
            tunnel_all.remove(dnum)
    data["tun_num"] = tunnel_all[0]
    logging.debug(f"Choosen tunnel: {tunnel_all[0]}")
    templ1, templ2 = create_vpn_config(src_template, dst_template, vpn_data_dict)
    logging.debug("--- Template 1 ---")
    logging.debug(templ1)
    logging.debug("--- Template 2 ---")
    logging.debug(templ2)
    logging.debug("--- Template END ---")

    t1 = templ1.split("\n")
    t2 = templ2.split("\n")
    ret1 = send_config_commands(src_device_params,t1)
    ret2 = send_config_commands(dst_device_params,t2)
    logging.debug("--- Config 1 ---")
    logging.debug(ret1)
    logging.debug("--- Config 2 ---")
    logging.debug(ret2)
    logging.debug("--- Config END ---")

    return ret1,ret2


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    dev1 = devices[0]
    dev2 = devices[1]
    template1_file = "templates/gre_ipsec_vpn_1.txt"
    template2_file = "templates/gre_ipsec_vpn_2.txt"
    pprint(configure_vpn(dev1, dev2,template1_file, template2_file,data))
