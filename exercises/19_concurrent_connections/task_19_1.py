# -*- coding: utf-8 -*-
"""
Задание 19.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.
Проверка IP-адресов должна выполняться параллельно в разных потоках.

Параметры функции ping_ip_addresses:
* ip_list - список IP-адресов
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для выполнения задания можно создавать любые дополнительные функции.

Для проверки доступности IP-адреса, используйте ping.

Подсказка о работе с concurrent.futures:
Если необходимо пинговать несколько IP-адресов в разных потоках,
надо создать функцию, которая будет пинговать один IP-адрес,
а затем запустить эту функцию в разных потоках для разных
IP-адресов с помощью concurrent.futures (это надо сделать в функции ping_ip_addresses).
"""
from concurrent.futures import ThreadPoolExecutor
import logging
import subprocess
from pprint import pprint

def ping_addr(ip):
    alive = False
    result = subprocess.run(['ping', '-c', '3', '-n', ip], stdout=subprocess.DEVNULL)
    if result.returncode == 0:
        alive = True
    return alive

def ping_ip_addresses(ip_list, limit=3):
    alive = []
    dead = []
    with ThreadPoolExecutor(max_workers=limit) as executor:
        ret = executor.map(ping_addr, ip_list)
        for ip, state in zip(ip_list, ret):
            if state:
                alive.append(ip)
            else:
                dead.append(ip)
    return alive,dead

if __name__ == "__main__":
    pprint(ping_ip_addresses(["8.8.8.8", "1.1.1.1","10.175.0.1"],5))