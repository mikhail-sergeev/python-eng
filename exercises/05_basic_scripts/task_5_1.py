london_co = {
    "r1": {
        "location": "21 New Globe Walk",
        "vendor": "Cisco",
        "model": "4451",
        "ios": "15.4",
        "ip": "10.255.0.1"
    },
    "r2": {
        "location": "21 New Globe Walk",
        "vendor": "Cisco",
        "model": "4451",
        "ios": "15.4",
        "ip": "10.255.0.2"
    },
    "sw1": {
        "location": "21 New Globe Walk",
        "vendor": "Cisco",
        "model": "3850",
        "ios": "3.6.XE",
        "ip": "10.255.0.101",
        "vlans": "10,20,30",
        "routing": True
    }
}

dev = input("Введите имя устройства: ")
keys = london_co[dev].keys()
keys_input=",".join(keys)
param = input("Введите имя параметра ({}): ".format(keys_input))

keys2 = keys_input.upper().split(",")

if param.upper() in keys2:
    print(london_co[dev][param.lower()])
else:
    print("Такого параметра нет")

