# -*- coding: utf-8 -*-
"""
Задание 21.2

Сделать шаблон TextFSM для обработки вывода sh ip dhcp snooping binding
и записать его в файл templates/sh_ip_dhcp_snooping.template

Вывод команды находится в файле output/sh_ip_dhcp_snooping.txt.

Шаблон должен обрабатывать и возвращать значения таких столбцов:
* mac - такого вида 00:04:A3:3E:5B:69
* ip - такого вида 10.1.10.6
* vlan - 10
* intf - FastEthernet0/10

Проверить работу шаблона с помощью функции parse_command_output из задания 21.1.
"""
import textfsm

def parse_output_to_dict(template, output):
    result = []
    with open(template) as f:
        re_table = textfsm.TextFSM(f)
        header = re_table.header
        #res = re_table.ParseText(output)
        res = re_table.ParseTextToDicts(output)
        #print(res)

    return res

# вызов функции должен выглядеть так
if __name__ == "__main__":
    with open("output/sh_ip_dhcp_snooping.txt") as f:
        output = f.read()
    result = parse_output_to_dict("templates/sh_ip_dhcp_snooping.template", output)
    print(result)
