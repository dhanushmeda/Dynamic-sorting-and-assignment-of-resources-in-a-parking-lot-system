from PIL import Image,ImageTk
from socket import *
import time
import string
from tkinter import *
print_var=""
message=""
root=Tk()
root.geometry("800x500")
def find():
    global message
    message="0,"
    print("finding")
    f1 = open("car_stroage.txt", 'r')
    file_con = f1.read()
    f1.close()
    serverName = "<Server IP>"
    serverPort = 12002
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    # message = input("Input lowercase sentence:")
    message += file_con
    print(message)
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    print((modifiedMessage.decode()))
    clientSocket.close()
    time.sleep(20)
    clientSocket1 = socket(AF_INET, SOCK_DGRAM)
    message1 = "3"
    clientSocket1.sendto(message1.encode(), (serverName, serverPort))
    modifiedMessage1, serverAddress1 = clientSocket1.recvfrom(2048)
    print((modifiedMessage1.decode()))
    modifiedMessage1_str=str(modifiedMessage1.decode())
    msg_new=modifiedMessage1_str[1] + modifiedMessage1_str[2]
    if msg_new!="00":
        Label(root, text="Car is allotted to to parking spot  " + msg_new,font=('times new roman', 12, 'bold'), bg='white', fg='navy').place(x=280, y=380)
    else:
        Label(root, text="No space available, sorry.\nCome back again later :)", font=('times new roman', 12, 'bold'),bg='white', fg='navy').place(x=280, y=380)
    clientSocket1.close()
def leave():
    global message
    message="2,"
    print("leaving")
    f1 = open("car_stroage.txt", 'r')
    file_con = f1.read()
    f1.close()
    serverName = "192.168.196.1"
    serverPort = 12002
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    message += file_con
    print(message)
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    print((modifiedMessage.decode()))
    clientSocket.close()
    time.sleep(20)
    clientSocket1 = socket(AF_INET, SOCK_DGRAM)
    message1 = "3"
    clientSocket1.sendto(message1.encode(), (serverName, serverPort))
    modifiedMessage1, serverAddress1 = clientSocket1.recvfrom(2048)
    modifiedMessage1_str=modifiedMessage1.decode()
    print((modifiedMessage1.decode()))
    Label(root, text="successfully exited parking spot "+modifiedMessage1_str[1]+modifiedMessage1_str[2], font=('times new roman', 12, 'bold'), bg='white',fg='navy').place(x=280,y=380)
    clientSocket1.close()
Label(root, text="WELCOME", font=("Times new Roman", 46, "bold","underline"),bg="light blue1", fg="navy").place(x=200, y=80)
find_button = Button(root,text="Find a spot",command=find,font=("Calibre", 15, "bold"), bg="navy",fg="white")
find_button.place(x=100,y=270)
leave_button = Button(root,text="leave your spot",command=leave,font=("Calibre", 15, "bold"), bg="navy",fg="white")
leave_button.place(x=500,y=270)
root.configure(bg="light blue1")
root.mainloop()
