access_template = [
    "switchport mode access", "switchport access vlan {}",
    "switchport nonegotiate", "spanning-tree portfast",
    "spanning-tree bpduguard enable"
]

trunk_template = [
    "switchport trunk encapsulation dot1q", "switchport mode trunk",
    "switchport trunk allowed vlan {}"
]

templ = {"access":access_template, "trunk":trunk_template}
templq = {"access":"Vlan: ", "trunk":"Vlans list: "}
mode = input("Interface mode (access/trunk): ")
interface = input("Interface name: ")
vlan = input(templq[mode])

t = "\n".join(templ[mode])
out = "interface {}".format(interface) + "\n" + t.format(vlan)
print(out)

