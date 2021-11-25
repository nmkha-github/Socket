
import socket 
import threading 
import pyodbc

#socket
HOST = "127.0.0.1" 
SERVER_PORT = 65432 
FORMAT = "utf8"

# Database config
SERVER = 'MON-ASUS\SQLEXPRESS'
DATABASE = 'Socket_Account'
UID='dh' 
PWD='123456'

#option 
LOGIN = "login"
FAIL = "fail"
OK = "ok"
END = "x"

def recvList(conn):
    list = []

    item = conn.recv(1024).decode(FORMAT)

    while (item != "end"):
        
        list.append(item)
        #response
        conn.sendall(item.encode(FORMAT))
        item = conn.recv(1024).decode(FORMAT)
    
    return list

def serverLogin(conn: socket):
    print("login start")

    user = conn.recv(1024).decode(FORMAT)
    conn.sendall(user.encode(FORMAT))
    pswd = conn.recv(1024).decode(FORMAT)
    conn.sendall(pswd.encode(FORMAT))
    print(user, pswd)

    # query data: password
    cursor.execute("select pass from Account where username = ?", user)
    password = cursor.fetchone()
    data_password = password[0]
    print(data_password)
    
    # verify login
    msg = OK
    if (pswd == data_password):
        msg = OK
        print(msg)
    
    else:
        msg = FAIL
        print(msg)

    conn.sendall(msg.encode(FORMAT))



def handleClient(conn: socket, addr):
    
    print("conn:",conn.getsockname())
    
    option = conn.recv(1024).decode(FORMAT)
    print(option)
    count = 0
    while (count < 50):

        if (option == LOGIN):
            serverLogin(conn)
            option = "x"
        
        count += 1
    
    print("client" , addr, "finished")
    print(conn.getsockname(), "closed")
    conn.close()

#-----------------------main-------------

#database connection init
conx = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER=' + SERVER + 
                        '; Database=' + DATABASE + 
                        '; UID=' + UID + '; PWD=' + PWD )
cursor = conx.cursor()

# socket init
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind((HOST, SERVER_PORT))
s.listen()

print("SERVER SIDE")
print("server:", HOST, SERVER_PORT)
print("Waiting for Client")

nClient = 0
while (nClient < 1):
    try:
        conn, addr = s.accept()
        
        thr = threading.Thread(target=handleClient, args=(conn,addr))
        thr.daemon = False
        thr.start()

    except:
        print("Error")
    
    nClient += 1


print("End")

input()
s.close()
conx.close()
