# -*- coding: utf-8 -*-

"""
Задание 22.2c

Скопировать класс CiscoTelnet из задания 22.2b и изменить метод send_config_commands
добавив проверку команд на ошибки.

У метода send_config_commands должен быть дополнительный параметр strict:
* strict=True значит, что при обнаружении ошибки, необходимо сгенерировать
  исключение ValueError (значение по умолчанию)
* strict=False значит, что при обнаружении ошибки, надо только вывести
  на стандартный поток вывода сообщене об ошибке

Метод дожен возвращать вывод аналогичный методу send_config_set
у netmiko (пример вывода ниже). Текст исключения и ошибки в примере ниже.

Пример создания экземпляра класса:
In [1]: from task_22_2c import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

In [4]: commands_with_errors = ['logging 0255.255.1', 'logging', 'a']
In [5]: correct_commands = ['logging buffered 20010', 'ip http server']
In [6]: commands = commands_with_errors+correct_commands

Использование метода send_config_commands:

In [7]: print(r1.send_config_commands(commands, strict=False))
При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.
При выполнении команды "logging" на устройстве 192.168.100.1 возникла ошибка -> Incomplete command.
При выполнении команды "a" на устройстве 192.168.100.1 возникла ошибка -> Ambiguous command:  "a"
conf t
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#logging 0255.255.1
                   ^
% Invalid input detected at '^' marker.

R1(config)#logging
% Incomplete command.

R1(config)#a
% Ambiguous command:  "a"
R1(config)#logging buffered 20010
R1(config)#ip http server
R1(config)#end
R1#

In [8]: print(r1.send_config_commands(commands, strict=True))
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-8-0abc1ed8602e> in <module>
----> 1 print(r1.send_config_commands(commands, strict=True))

...

ValueError: При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.

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

    def send_config_commands(self, commands, strict=True):
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
            ans = self.telnet.read_until(b"#", timeout=5).decode("utf-8")
            result.append(ans)
            if "%" in ans:
                err0 = ans.split('%')[1].split('\n')[0]
                err = f"При выполнении команды \"{command}\" на устройстве {self.telnet.host} возникла ошибка -> {err0}"
                if strict:
                    raise ValueError(err)
                else:
                    print(err)
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
    pprint(r1.send_config_commands("logging",True))
