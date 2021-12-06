import socket
import threading
from Account import *
# Nhập 
HOST = '127.0.0.1'  
PORT = 8000        
#
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
#
def receive_account_password(conn):
    acc = conn.recv(1024).decode('utf8')
    psw = conn.recv(1024).decode('utf8')
    return acc, psw

def handle_client(conn, addr):
    print("Address: ", addr)
    account, password = receive_account_password(conn)
    conn.send(check_Account(account, password).encode('utf8'))


# xử lí đa luồng
print("Server: ", s.getsockname())
maxClientsConnected = 5
cntClientsConnected = 0
while True:
    if cntClientsConnected == maxClientsConnected:
        #thông báo đã tối đa client truy cập
        print("Close some Clients")
        continue
    
    conn, addr = s.accept()
    try:
        thr = threading.Thread(target=handle_client, args=(conn, addr))
        thr.daemon = True
        thr.start()
    except:
        print("Error")
    
# Kết thúc

print("END")
input()

def close_ALL():
    conx.close()
    s.close()

close_ALL()