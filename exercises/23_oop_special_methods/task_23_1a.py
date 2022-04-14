# -*- coding: utf-8 -*-

"""
Задание 23.1a

Скопировать и изменить класс IPAddress из задания 23.1.

Добавить два строковых представления для экземпляров класса IPAddress.
Как дожны выглядеть строковые представления, надо определить из вывода ниже:

Создание экземпляра
In [5]: ip1 = IPAddress('10.1.1.1/24')

In [6]: str(ip1)
Out[6]: 'IP address 10.1.1.1/24'

In [7]: print(ip1)
IP address 10.1.1.1/24

In [8]: ip1
Out[8]: IPAddress('10.1.1.1/24')

In [9]: ip_list = []

In [10]: ip_list.append(ip1)

In [11]: ip_list
Out[11]: [IPAddress('10.1.1.1/24')]

In [12]: print(ip_list)
[IPAddress('10.1.1.1/24')]

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

    def __str__(self):
        return f"IP address {self.ip}/{self.mask}"

    def __repr__(self):
        return f"IPAddress('{self.ip}/{self.mask}')"

if __name__ == "__main__":
    a = IPAddress('10.10.1.12/25')
    print(a)


