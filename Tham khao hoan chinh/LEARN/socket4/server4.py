
import socket 
import threading 
import pyodbc

#192.168.1.119
HOST = "127.0.0.1" 
SERVER_PORT = 65432 
FORMAT = "utf8"

LOGIN = "login"

def recvList(conn):
    list = []

    item = conn.recv(1024).decode(FORMAT)

    while (item != "end"):
        
        list.append(item)
        #response
        conn.sendall(item.encode(FORMAT))
        item = conn.recv(1024).decode(FORMAT)
    
    return list

def serverLogin(conn):

    # recv account from client
    client_account = recvList(conn)

    # query data: password
    cursor.execute("select pass from Account where username = ?", client_account[0])
    password = cursor.fetchone()
    data_password = password[0]
    print(data_password)

    msg = "ok"
    if (client_account[1] == data_password):
        msg = "Login successfully"
        print(msg)

    
    else:
        msg = "Invalid password"
        print(msg)

    conn.sendall(msg.encode(FORMAT))

    



def handleClient(conn: socket, addr):
    
    print("conn:",conn.getsockname())
    
    msg = None
    while (msg != "x"):
        msg = conn.recv(1024).decode(FORMAT)
        print("client ",addr, "says", msg)

        if (msg == LOGIN):
            #response
            conn.sendall(msg.encode(FORMAT))
            serverLogin(conn)
    
    
    print("client" , addr, "finished")
    print(conn.getsockname(), "closed")
    conn.close()

#-----------------------main-------------

conx = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};\
                        SERVER=MON-ASUS\SQLEXPRESS; Database=Socket_Account;\
                        UID=dh; PWD=123456;')
cursor = conx.cursor()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

s.bind((HOST, SERVER_PORT))
s.listen()

print("SERVER SIDE")
print("server:", HOST, SERVER_PORT)
print("Waiting for Client")

nClient = 0
while (nClient < 3):
    try:
        conn, addr = s.accept()
        
        thr = threading.Thread(target=handleClient, args=(conn,addr))
        thr.daemon = False
        thr.start()

    except:
        print("Error")
    
    nClient += 1


print("End")

s.close();
conx.close()

