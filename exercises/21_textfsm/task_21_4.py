# -*- coding: utf-8 -*-
"""
Задание 21.4

Создать функцию send_and_parse_show_command.

Параметры функции:
* device_dict - словарь с параметрами подключения к одному устройству
* command - команда, которую надо выполнить
* templates_path - путь к каталогу с шаблонами TextFSM
* index - имя индекс файла, значение по умолчанию "index"

Функция должна подключаться к одному устройству, отправлять команду show
с помощью netmiko, а затем парсить вывод команды с помощью TextFSM.

Функция должна возвращать список словарей с результатами обработки
вывода команды (как в задании 21.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br
и устройствах из devices.yaml.
"""
import yaml
from pprint import pprint
from textfsm import clitable
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)


def send_and_parse_show_command(device_dict, command, templates_path, index="index"):
    """
    :param device_dict: словарь с параметрами подключения к одному устройству
    :param command: команда, которую надо выполнить
    :param templates_path: путь к каталогу с шаблонами TextFSM
    :param index: имя индекс файла, значение по умолчанию "index"
    :return: ключи - имена переменных в шаблоне TextFSM, значения - части вывода, которые соответствуют переменным
    """
    try:
        with ConnectHandler(**device_dict) as ssh:
            ssh.enable()
            output = ssh.send_command(command)
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)
    cli_table = clitable.CliTable(index, templates_path)
    cli_table.ParseCmd(output, {'Command': command, 'Vendor': 'cisco_ios'})
    data_rows = [list(row) for row in cli_table]
    header = list(cli_table.header)
    result = []
    for data in data_rows:
        item0 = zip(header,data)
        item = dict(item0)
        result.append(item)
    return result

if __name__ == "__main__":
    command = "sh ip int br"
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    for dev in devices:
        pprint(send_and_parse_show_command(dev, command, "templates"))
