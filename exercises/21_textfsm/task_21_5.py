# -*- coding: utf-8 -*-
"""
Задание 21.5

Создать функцию send_and_parse_command_parallel.

Функция send_and_parse_command_parallel должна запускать в
параллельных потоках функцию send_and_parse_show_command из задания 21.4.

Параметры функции send_and_parse_command_parallel:
* devices - список словарей с параметрами подключения к устройствам
* command - команда
* templates_path - путь к каталогу с шаблонами TextFSM
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать словарь:
* ключи - IP-адрес устройства с которого получен вывод
* значения - список словарей (вывод который возвращает функция send_and_parse_show_command)

Пример словаря:
{'192.168.100.1': [{'address': '192.168.100.1',
                    'intf': 'Ethernet0/0',
                    'protocol': 'up',
                    'status': 'up'},
                   {'address': '192.168.200.1',
                    'intf': 'Ethernet0/1',
                    'protocol': 'up',
                    'status': 'up'}],
 '192.168.100.2': [{'address': '192.168.100.2',
                    'intf': 'Ethernet0/0',
                    'protocol': 'up',
                    'status': 'up'},
                   {'address': '10.100.23.2',
                    'intf': 'Ethernet0/1',
                    'protocol': 'up',
                    'status': 'up'}]}

Проверить работу функции на примере вывода команды sh ip int br
и устройствах из devices.yaml.
"""

import yaml
from pprint import pprint
from textfsm import clitable
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

def send_and_parse_command(device, command, templates_path):
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            output = ssh.send_command(command)
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)
    cli_table = clitable.CliTable("index", templates_path)
    cli_table.ParseCmd(output, {'Command': command, 'Vendor': 'cisco_ios'})
    data_rows = [list(row) for row in cli_table]
    header = list(cli_table.header)
    result = []
    for data in data_rows:
        item0 = zip(header, data)
        item = dict(item0)
        result.append(item)
    return result

def send_and_parse_command_parallel(devices, command, templates_path, limit=3):
    """
    :param device_dict: словарь с параметрами подключения к одному устройству
    :param command: команда, которую надо выполнить
    :param templates_path: путь к каталогу с шаблонами TextFSM
    :param limit: максимальное количество параллельных потоков (по умолчанию 3)
    :return: ключи - имена переменных в шаблоне TextFSM, значения - части вывода, которые соответствуют переменным
    """
    result = {}
    with ThreadPoolExecutor(max_workers=limit) as executor:
        ret = executor.map(send_and_parse_command, devices, repeat(command), repeat(templates_path))
        for dev, out in zip(devices, ret):
            result[dev['host']] = out

    return result

if __name__ == "__main__":
    command = "sh ip int br"
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    pprint(send_and_parse_command_parallel(devices, command, "templates"))
