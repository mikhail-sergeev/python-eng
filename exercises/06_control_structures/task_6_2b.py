# -*- coding: utf-8 -*-
"""
Задание 6.2b

Сделать копию скрипта задания 6.2a.

Дополнить скрипт: Если адрес был введен неправильно, запросить адрес снова.

Если адрес задан неправильно, выводить сообщение: 'Неправильный IP-адрес'
Сообщение "Неправильный IP-адрес" должно выводиться только один раз,
даже если несколько пунктов выше не выполнены.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

error = True
addr = ""

while error:
    error = False
    addr = input("Please enter IP: ")
    try:
        for i in addr.split("."):
            if not 0 <= int(i) <= 255:
                error = True
        oct1 = int(addr.split(".")[0])
        dcount = len(addr.split("."))
        if dcount != 4:
            error = True
    except ValueError:
        error = True
    if error:
        print("Неправильный IP-адрес")
    elif 0 < oct1 <= 223:
        print("unicast")
    elif 0 < oct1 <= 239:
        print("multicast")
    elif addr=="255.255.255.255":
        print("local broadcast")
    elif addr=="0.0.0.0":
        print("unassigned")
    else:
        print("unused")
