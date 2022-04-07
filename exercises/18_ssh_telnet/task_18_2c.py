# -*- coding: utf-8 -*-
"""
Задание 18.2c

Скопировать функцию send_config_commands из задания 18.2b и переделать ее таким образом:

Если при выполнении команды возникла ошибка, спросить пользователя надо ли выполнять
остальные команды.

Варианты ответа [y]/n:
* y - выполнять остальные команды. Это значение по умолчанию,
  поэтому нажатие любой комбинации воспринимается как y
* n или no - не выполнять остальные команды

Функция send_config_commands по-прежнему должна возвращать кортеж из двух словарей:
* первый словарь с выводом команд, которые выполнились без ошибки
* второй словарь с выводом команд, которые выполнились с ошибками

Оба словаря в формате
* ключ - команда
* значение - вывод с выполнением команд

Проверить работу функции можно на одном устройстве.

Пример работы функции:

In [11]: result = send_config_commands(r1, commands)
Подключаюсь к 192.168.100.1...
Команда "logging 0255.255.1" выполнилась с ошибкой "Invalid input detected at '^' marker." на устройстве 192.168.100.1
Продолжать выполнять команды? [y]/n: y
Команда "logging" выполнилась с ошибкой "Incomplete command." на устройстве 192.168.100.1
Продолжать выполнять команды? [y]/n: n

In [12]: pprint(result)
({},
 {'logging': 'config term\n'
             'Enter configuration commands, one per line.  End with CNTL/Z.\n'
             'R1(config)#logging\n'
             '% Incomplete command.\n'
             '\n'
             'R1(config)#',
  'logging 0255.255.1': 'config term\n'
                        'Enter configuration commands, one per line.  End with '
                        'CNTL/Z.\n'
                        'R1(config)#logging 0255.255.1\n'
                        '                   ^\n'
                        "% Invalid input detected at '^' marker.\n"
                        '\n'
                        'R1(config)#'})

"""
import re
from pprint import pprint

import yaml
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

# списки команд с ошибками и без:
commands_with_errors = ["logging 0255.255.1", "logging", "a"]
correct_commands = ["logging buffered 20010", "ip http server"]

commands = commands_with_errors + correct_commands



def send_config_commands(device, config_commands, log=True):
    good = {}
    bad = {}
    status = True
    if log:
        print(f"Подключаюсь к {device['host']}...")
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            for command in config_commands:
                output = ssh.send_config_set(command)
                error = ""
                err = re.search(r'% ([\S\s]+?)\n',output)
                if err:
                    error = err.groups()[0]
                if "% Incomplete command" in output or "% Ambiguous command" in output or "% Invalid input" in output:
                    print(f'Команда "{command}" выполнилась с ошибкой "{error}" на устройстве {device["host"]}')
                    bad[command] = output
                    inp = input("Продолжать выполнять команды? [y]/n: ")
                    if inp == "n" or inp == "no":
                        break
                else:
                    good[command] = output
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)

    return good,bad


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)

    for dev in devices:
        pprint(send_config_commands(dev, commands))

