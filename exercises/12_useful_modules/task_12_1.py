# -*- coding: utf-8 -*-
"""
Задание 12.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.

Функция ожидает как аргумент список IP-адресов.

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для проверки доступности IP-адреса, используйте команду ping (запуск ping через subprocess).
IP-адрес считается доступным, если выполнение команды ping отработало с кодом 0 (returncode).
Нюансы: на Windows returncode может быть равен 0 не только, когда ping был успешен,
но для задания нужно проверять именно код. Это сделано для упрощения тестов.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
import subprocess

def ping_ip_addresses(ip_list):
    ip_avail = []
    ip_unavail = []
    for ip in ip_list:
        reply = subprocess.run(['ping', '-c', '3', '-n', ip],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               encoding='utf-8')
        if reply.returncode == 0:
            ip_avail.append(ip)
        else:
            ip_unavail.append(ip)
    return ip_avail, ip_unavail



if __name__ == "__main__":
    print(ping_ip_addresses(['8.8.8.8', '1.12.3.4']))
