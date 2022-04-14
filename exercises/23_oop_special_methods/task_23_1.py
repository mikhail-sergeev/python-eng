# -*- coding: utf-8 -*-

"""
Задание 23.1

В этом задании необходимо создать класс IPAddress.

При создании экземпляра класса, как аргумент передается IP-адрес и маска,
а также должна выполняться проверка корректности адреса и маски:
* Адрес считается корректно заданным, если он:
   - состоит из 4 чисел разделенных точкой
   - каждое число в диапазоне от 0 до 255
* маска считается корректной, если это число в диапазоне от 8 до 32 включительно

Если маска или адрес не прошли проверку, необходимо сгенерировать
исключение ValueError с соответствующим текстом (вывод ниже).

Также, при создании класса, должны быть созданы два атрибута экземпляра:
ip и mask, в которых содержатся адрес и маска, соответственно.

Пример создания экземпляра класса:
In [1]: ip = IPAddress('10.1.1.1/24')

Атрибуты ip и mask
In [2]: ip1 = IPAddress('10.1.1.1/24')

In [3]: ip1.ip
Out[3]: '10.1.1.1'

In [4]: ip1.mask
Out[4]: 24

Проверка корректности адреса (traceback сокращен)
In [5]: ip1 = IPAddress('10.1.1/24')
---------------------------------------------------------------------------
...
ValueError: Incorrect IPv4 address

Проверка корректности маски (traceback сокращен)
In [6]: ip1 = IPAddress('10.1.1.1/240')
---------------------------------------------------------------------------
...
ValueError: Incorrect mask

"""
from pprint import pprint



class IPAddress:
    def __init__(self, ipaddr):
        err = ""
        try:
            self.ip = ipaddr.split('/')[0]
            ipbits = self.ip.split('.')
            if not len(ipbits) == 4:
                err = "Incorrect IP"
            for bit in ipbits:
                if int(bit) not in range(0,255):
                    err = "Incorrect IP"
        except (IndentationError, ValueError):
            err = "Incorrect IP"
        try:
            self.mask = int(ipaddr.split('/')[1])
            if self.mask not in range(8,32):
                err = "Incorrect mask"
        except (IndentationError, ValueError):
            err = "Incorrect mask"
        if err:
            raise ValueError(err)

if __name__ == "__main__":
    a = IPAddress('10.10a.1.12/25')
    pprint(a.ip)
    pprint(a.mask)
