import socket
import threading
# Nhập 
HOST = 'localhost'  
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

# xử lí đa luồng
print("Server: ", s.getsockname())
def live_server():
    while True:
        conn, addr = s.accept()
        try:
            thr = threading.Thread(target=handle_client, args=(conn, addr))
            thr.daemon = True
            thr.start()
        except:
            print("Error")
    
# Kết thúc