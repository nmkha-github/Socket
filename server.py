import socket
import threading
# Nhập 
HOST = '127.0.0.1'  
PORT = 8000        
#

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

def handle_client(conn, addr):
    print("Address: ", addr)
    account = conn.recv(1024).decode('utf8')
    print(account)
    password = conn.recv(1024).decode('utf8')
    print(password)
# xử lí đa luồng
print("Server: ", s.getsockname())
maxClientsConnected = 3
cntClientsConnected = 0
while cntClientsConnected <= maxClientsConnected:
    conn, addr = s.accept()
    
    thr = threading.Thread(target=handle_client, args=(conn, addr))
    thr.daemon = True
    thr.start()
#
print("END")
input()
s.close()