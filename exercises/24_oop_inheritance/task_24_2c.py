# -*- coding: utf-8 -*-

"""
Задание 24.2c

Скопировать класс MyNetmiko из задания 24.2b.
Проверить, что метод send_command кроме команду, принимает еще и дополнительные
аргументы, например, strip_command.

Если возникает ошибка, переделать метод таким образом, чтобы он принимал
любые аргументы, которые поддерживает netmiko.


In [2]: from task_24_2c import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [4]: r1.send_command('sh ip int br', strip_command=False)
Out[4]: 'sh ip int br\nInterface                  IP-Address      OK? Method Status                Protocol\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \nEthernet0/3                192.168.230.1   YES NVRAM  up                    up      \nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      '

In [5]: r1.send_command('sh ip int br', strip_command=True)
Out[5]: 'Interface                  IP-Address      OK? Method Status                Protocol\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \nEthernet0/3                192.168.230.1   YES NVRAM  up                    up      \nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      '

"""
from netmiko.cisco.cisco_ios import CiscoIosSSH


class ErrorInCommand(Exception):
    """
    Исключение генерируется, если при выполнении команды на оборудовании,
    возникла ошибка.
    """


device_params = {
    "device_type": "cisco_ios",
    "ip": "192.168.100.1",
    "username": "cisco",
    "password": "cisco",
    "secret": "cisco",
}


class MyNetmiko(CiscoIosSSH):
    def __init__(self, **dev_params):
        super().__init__(**dev_params)
        self.enable()

    def _check_error_in_command(self, command, output):
        if "%" in output:
            err0 = output.split('%')[1].split('\n')[0]
            err = f"При выполнении команды '{command}' на устройстве {self.host} возникла ошибка -> {err0}"
            raise ErrorInCommand(err)
        return

    def send_command(self, command, **kwargs):
        ret = super().send_command(command, **kwargs)
        self._check_error_in_command(command, ret)
        return ret

    def send_config_set(self, commands):
        command_list = commands
        if type(commands) is str:
            command_list = []
            command_list.append(commands)
        num = len(command_list)
        id = 1
        result = ""
        for cmd in command_list:
            ent = True
            ex = True
            if id == 1:
                ent = True
            else:
                ent = False
            if id == num:
                ex = True
            else:
                ex = False

            ret = super().send_config_set(cmd, enter_config_mode=ent, exit_config_mode=ex)
            self._check_error_in_command(cmd, ret)
            id += 1
            result += ret

        return result


if __name__ == "__main__":
    r1 = MyNetmiko(**device_params)
    print(r1.send_command('sh ip int br',strip_command=True))
