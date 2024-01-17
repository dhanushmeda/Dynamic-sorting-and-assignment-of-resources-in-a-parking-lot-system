from socket import *
import time
serverPort = 12002
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(("<Server IP>", serverPort))
print("The server is ready to receive")
x = 0
car_number=""
modifiedMessage = ""
charge_requiered = 0
cycles_offered = 0
charge_available = [0,0,0,0]
cycles_requiered = [0,0,0,0]
availability = ["","","",""]
p=0
car_leaving_number=""
while 1:
    message, clientAddress = serverSocket.recvfrom(2048)# blocking line
    print(("Got connection from", clientAddress))
    msg = message.decode('utf-8')
    l = msg.split(',')
    if int(l[0]) == 0:  # from car requesting parking;"type,charge,cycle,car-number" , type=0 coz its from car
        charge_requiered = int(l[1])
        cycles_offered = int(l[2])
        car_number=str(l[3])
        x += 1
    elif int(l[0]) == 1:
        # from plo;"type,charge1 charge2... in units,cycle1 cycle2... in MHz,availability1 availability2(availability=A,no.)"
        x += 1
        charge_available1 = l[1].split(" ")
        cycles_requiered1 = l[2].split(" ")
        for i in range(0, 4):
            charge_available[i] = int(charge_available1[i])
        for i in range(0, 4):
            cycles_requiered[i] = int(cycles_requiered1[i])
        availability = l[3].split(" ")
        if p==1:
            slot=availability.index(car_leaving_number)
            if slot==0:
                modifiedMessage="l1a"
            elif slot==1:
                modifiedMessage="l1b"
            elif slot==2:
                modifiedMessage="l2a"
            else:
                modifiedMessage="l2b"
    elif int(l[0]) == 2 :  # from car leaving the lot, change availability;"type,charge,cycle,car-number"
        p=1
        car_leaving_number=l[3]
    else:  # send slot alloted back to car
        pass
    if x == 2 and l[0]!=2 and p==0:# if msg is recieved from both car and plo
        choice = [1, 1, 1, 1]  # 1=slot assignable to car
        choice_copy = [1,1,1,1]
        # filtering according to availability
        for i in range(0, 4):
            if availability[i] != "A":
                choice[i] = 0
        for i in range(0,4):
            choice_copy[i]=choice[i]
        # filtering according to charge
        for i in range(0, 4):
            if charge_available[i] < charge_requiered:
                choice[i] = 0
        if choice==[0,0,0,0]:
            for i in range(0,4):
                choice[i]=choice_copy[i]
        for i in range(0,4):
            choice_copy[i]=choice[i]
        # filtering according to cycles
        for i in range(0, 4):
            if cycles_offered < cycles_requiered[i]:
                choice[i] = 0
        if choice==[0,0,0,0]:
            for i in range(0,4):
                choice[i]=choice_copy[i]
        z=0
        for i in choice:
            if i == 1:
                z+=1
        if z > 1:
            z = 0
            available_choices = [1000, 1000, 1000, 1000]
            for i in range(0, 4):
                if choice[i] == 1:
                    available_choices[i] = charge_available[i]
            m = min(available_choices)
            for i in range(0, 4):
                if charge_available[i] != m:
                    choice[i] = 0
                else:
                    z += 1
            print(choice,m)
            if z > 1:
                available_choices = [10000, 10000, 10000, 10000]
                for i in range(0, 4):
                    if choice[i] == 1:
                        available_choices[i] = cycles_requiered[i]
                m = min(available_choices)
                for i in range(0, 4):
                    if cycles_requiered[i] != m:
                        choice[i] = 0
        if 1 in choice:
            i=choice.index(1)
            if i==0:
                modifiedMessage="a1a"
            elif i==1:
                modifiedMessage="a1b"
            elif i==2:
                modifiedMessage="a2a"
            elif i==3:
                modifiedMessage="a2b"
        else:
            modifiedMessage="a00"  #no space available
        modifiedMessage=str(modifiedMessage+";"+car_number)
    print(modifiedMessage)
    serverSocket.sendto(modifiedMessage.encode('utf-8'), clientAddress)
print(modifiedMessage)
