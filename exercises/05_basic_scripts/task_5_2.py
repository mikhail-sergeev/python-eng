
ipnet = input("IP/Network: ")

ip = ipnet.split("/")[0]
masklen = int(ipnet.split("/")[1])

print("Network:")
iparr = ip.split(".")
bin_ip = "{:032b}".format(int(iparr[0])*256*256*256+int(iparr[1])*256*256+int(iparr[2])*256+int(iparr[3]))

bin_net = bin_ip[0:masklen]+"0"*(32-masklen)

net = int(bin_net,2)
n4 = net % 256
net = round((net-n4)/256)
n3 = net % 256
net = round((net-n3)/256)
n2 = net % 256
net = round((net-n2)/256)
n1 = net % 256


print("{:<8} {:<8} {:<8} {:<8}".format(n1,n2,n3,n4))
print("{:08b} {:08b} {:08b} {:08b}".format(n1,n2,n3,n4))

print("Mask:")
print("/{}".format(masklen))
m1 = min(masklen, 7)
m2 = min(masklen-8, 7)
m3 = min(masklen-16, 7)
m4 = min(masklen-24, 7)

ma = [0,128,192,224,248,252,254,255]

print("{:<8} {:<8} {:<8} {:<8}".format(ma[m1],ma[m2],ma[m3],ma[m4]))
print("{:08b} {:08b} {:08b} {:08b}".format(ma[m1],ma[m2],ma[m3],ma[m4]))



