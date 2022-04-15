# -*- coding: utf-8 -*-

"""
Задание 24.2b

Скопировать класс MyNetmiko из задания 24.2a.

Дополнить функционал метода send_config_set netmiko и добавить в него проверку
на ошибки с помощью метода _check_error_in_command.

Метод send_config_set должен отправлять команды по одной и проверять каждую на ошибки.
Если при выполнении команд не обнаружены ошибки, метод send_config_set возвращает
вывод команд.

In [2]: from task_24_2b import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [4]: r1.send_config_set('lo')
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-2-8e491f78b235> in <module>()
----> 1 r1.send_config_set('lo')

...
ErrorInCommand: При выполнении команды "lo" на устройстве 192.168.100.1 возникла ошибка "Incomplete command."

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

    def send_command(self, command):
        ret = super().send_command(command)
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
    print(r1.send_config_set('lo'))
