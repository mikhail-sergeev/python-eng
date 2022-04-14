# -*- coding: utf-8 -*-

"""
Задание 22.1d

Изменить класс Topology из задания 22.1c

Добавить метод add_link, который добавляет указанное соединение, если его еще
 нет в топологии.
Если соединение существует, вывести сообщение "Такое соединение существует",
Если одна из сторон есть в топологии, вывести сообщение
"Cоединение с одним из портов существует"


Создание топологии
In [7]: t = Topology(topology_example)

In [8]: t.topology
Out[8]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [9]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))

In [10]: t.topology
Out[10]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [11]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
Такое соединение существует

In [12]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/5'))
Cоединение с одним из портов существует


"""
from pprint import pprint

class Topology:
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)

    def _normalize(self, topology_dict):
        result = {}
        for port1, port2 in topology_dict.items():
            if not result.get(port1) and not result.get(port2):
                result[port1] = port2
        return result

    def delete_link(self, port1, port2):
        success = False
        if self.topology.get(port1) and self.topology.get(port1) == port2:
            success = True
            self.topology.pop(port1)
        if self.topology.get(port2) and self.topology.get(port2) == port1:
            success = True
            self.topology.pop(port2)
        if not success:
            print("Такого соединения нет")
        return

    def delete_node(self, node):
        success = False
        new_topo = {}
        for port1,port2 in self.topology.items():
            if not port1[0] == node and not port2[0] == node:
                new_topo[port1] = port2

        if len(new_topo) == len(self.topology):
            print("Такого устройства нет")

        self.topology = new_topo
        return

    def add_link(self, port1, port2):
        if (self.topology.get(port1) and self.topology.get(port1) == port2) or (self.topology.get(port2) and self.topology.get(port2) == port1):
            print("Такое соединение существует")
            return
        if self.topology.get(port1) or self.topology.get(port2):
            print("Cоединение с одним из портов существует")
            return
        self.topology[port1] = port2
        return


topology_example = {
    ("R1", "Eth0/0"): ("SW1", "Eth0/1"),
    ("R2", "Eth0/0"): ("SW1", "Eth0/2"),
    ("R2", "Eth0/1"): ("SW2", "Eth0/11"),
    ("R3", "Eth0/0"): ("SW1", "Eth0/3"),
    ("R3", "Eth0/1"): ("R4", "Eth0/0"),
    ("R3", "Eth0/2"): ("R5", "Eth0/0"),
    ("SW1", "Eth0/1"): ("R1", "Eth0/0"),
    ("SW1", "Eth0/2"): ("R2", "Eth0/0"),
    ("SW1", "Eth0/3"): ("R3", "Eth0/0"),
}


if __name__ == "__main__":
    top = Topology(topology_example)
    pprint(top.topology)
    top.add_link(("R1", "Eth0/0"), ("SW1", "Eth0/1"))
    pprint(top.topology)
