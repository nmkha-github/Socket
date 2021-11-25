import socket
import threading
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
def get_registered():
    f = open("data.txt", 'r')
    res_list = f.readlines()
    f.close()
    return res_list
def check_account_password(account, password):
    list_account = get_registered()
    for x in list_account:
        acc = x.split(',')
        if (acc[0] == account) and (password == acc[1][:-1]):
            return 'ACCEPTED'
    return 'WRONG ACCOUNT OR PASSWORD'

def handle_client(conn, addr):
    print("Address: ", addr)
    account, password = receive_account_password(conn)
    conn.send(check_account_password(account, password).encode('utf8'))


# xử lí đa luồng
print("Server: ", s.getsockname())
print(get_registered())
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
s.close()