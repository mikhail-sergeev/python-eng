# -*- coding: utf-8 -*-

"""
Задание 24.2d

Скопировать класс MyNetmiko из задания 24.2c или задания 24.2b.

Добавить параметр ignore_errors в метод send_config_set.
Если передано истинное значение, не надо выполнять проверку на ошибки и метод должен
работать точно так же как метод send_config_set в netmiko.
Если значение ложное, ошибки должны проверяться.

По умолчанию ошибки должны игнорироваться.


In [2]: from task_24_2d import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [6]: r1.send_config_set('lo')
Out[6]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#lo\n% Incomplete command.\n\nR1(config)#end\nR1#'

In [7]: r1.send_config_set('lo', ignore_errors=True)
Out[7]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#lo\n% Incomplete command.\n\nR1(config)#end\nR1#'

In [8]: r1.send_config_set('lo', ignore_errors=False)
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-8-704f2e8d1886> in <module>()
----> 1 r1.send_config_set('lo', ignore_errors=False)

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

    def send_command(self, command, **kwargs):
        ret = super().send_command(command, **kwargs)
        self._check_error_in_command(command, ret)
        return ret

    def send_config_set(self, commands, ignore_errors=True):
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
            if not ignore_errors:
                self._check_error_in_command(cmd, ret)
            id += 1
            result += ret

        return result


if __name__ == "__main__":
    r1 = MyNetmiko(**device_params)
    print(r1.send_command('sh ip int br',strip_command=True))
