from socket import *
serverName = "<Server IP>"
serverPort = 12002
clientSocket = socket(AF_INET, SOCK_DGRAM)
f1 = open('plo_storage.txt', 'r')#1(type),charges available,cycles needed,availability
message = f1.read()
f1.close()
clientSocket.sendto(message.encode(), (serverName, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
msg_from_server = modifiedMessage.decode()
print(msg_from_server)
l = message.split(',') #from plo_storage
print(msg_from_server)
slot = str(msg_from_server[1] + msg_from_server[2])
x = 0 #  slot in number
availability = l[3].split(" ")
if slot == "1b":
    x = 1
elif slot == "2a":
    x = 2
elif slot == "2b":
    x = 3
if msg_from_server.startswith("a"):
    z = msg_from_server.split(";")
    availability[x]=z[1].strip()
elif msg_from_server.startswith("l"):
    availability[x]='A'
s=""
for i in availability:
    s=s+i+" "
s=s.strip()
print(s)
c=l[0]+","+l[1]+","+l[2]+","+s
print(c)
f2 = open('plo_storage.txt', 'w')
f2.write(c)
f2.close()
print(c)
clientSocket.close()
