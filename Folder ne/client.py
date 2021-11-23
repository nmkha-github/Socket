import socket
import threading
import time
PORT= 5050
HEADER =64
SERVER=socket.gethostbyname(socket.gethostname())
ADDR=(SERVER,PORT)
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)
def send(msg):
    message=msg.encode('utf-8')
    msg_length=len(message)
    send_length=str(msg_length).encode('utf-8')
    send_length+=b' '*(HEADER-len(send_length))
    client.send(send_length)
    client.send(message)
send("Hello World!")
send("Hello World!")
send("Hello World!")
send("Hello World!")
send("X")