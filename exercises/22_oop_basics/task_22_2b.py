# -*- coding: utf-8 -*-

"""
Задание 22.2b

Скопировать класс CiscoTelnet из задания 22.2a и добавить метод send_config_commands.


Метод send_config_commands должен уметь отправлять одну команду конфигурационного
режима и список команд.
Метод должен возвращать вывод аналогичный методу send_config_set у netmiko
(пример вывода ниже).

Пример создания экземпляра класса:
In [1]: from task_22_2b import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

Использование метода send_config_commands:

In [5]: r1.send_config_commands('logging 10.1.1.1')
Out[5]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#logging 10.1.1.1\r\nR1(config)#end\r\nR1#'

In [6]: r1.send_config_commands(['interface loop55', 'ip address 5.5.5.5 255.255.255.255'])
Out[6]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#interface loop55\r\nR1(config-if)#ip address 5.5.5.5 255.255.255.255\r\nR1(config-if)#end\r\nR1#'

"""
import telnetlib
import time
from pprint import pprint

from textfsm import clitable

class CiscoTelnet:
    def __init__(self, ip, username, password, secret):
        self.telnet = telnetlib.Telnet(ip)
        self.telnet.read_until(b"Username")
        self._write_line(username)
        self.telnet.read_until(b"Password")
        self._write_line(password)
        index, m, output = self.telnet.expect([b">", b"#"])
        if index == 0:
            self.telnet.write(b"enable\n")
            self.telnet.read_until(b"Password")
            self._write_line(secret)
            self.telnet.read_until(b"#", timeout=5)
        self._write_line("terminal length 0")
        self.telnet.read_until(b"#", timeout=5)
        time.sleep(3)
        self.telnet.read_very_eager()

    def _write_line(self, line):
        self.telnet.write(line.encode("utf-8") + b"\n")
        return

    def send_show_command(self, command, parse=True, templates="templates", index="index"):
        self._write_line(command)
        output = self.telnet.read_until(b"#", timeout=5).decode("utf-8")
        result = output.replace("\r\n", "\n")
        if parse:
            cli_table = clitable.CliTable(index, templates)
            cli_table.ParseCmd(result, {'Command': command, 'Vendor': 'cisco_ios'})
            data_rows = [list(row) for row in cli_table]
            header = list(cli_table.header)
            result = []
            for data in data_rows:
                item0 = zip(header, data)
                item = dict(item0)
                result.append(item)
        return result

    def send_config_commands(self, commands):
        command_list = []
        result = []
        if type(commands) is str:
            command_list = [commands]
        else:
            command_list = commands
        self._write_line("conf t")
        result.append(self.telnet.read_until(b"(config)#", timeout=5).decode("utf-8"))
        for command in command_list:
            self._write_line(command)
            result.append(self.telnet.read_until(b"#", timeout=5).decode("utf-8"))
        self._write_line("end")
        result.append(self.telnet.read_until(b"#", timeout=5).decode("utf-8"))
        return "".join(result)


r1_params = {
    'ip': '192.168.100.1',
    'username': 'cisco',
    'password': 'cisco',
    'secret': 'cisco'
}

if __name__ == "__main__":
    r1 = CiscoTelnet(**r1_params)
    pprint(r1.send_config_commands('logging 10.1.1.1'))
