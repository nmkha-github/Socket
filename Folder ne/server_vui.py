import socket
import threading
import time
PORT= 5050
HEADER =64
SERVER=socket.gethostbyname(socket.gethostname())
ADDR=(SERVER,PORT)
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)
def handle_client(conn, addr):
    print(f"NEW CONNECTION {addr} connected")
    connected=True
    while connected:
        msg_length = conn.recv(HEADER).decode('utf-8')
        if msg_length:
            msg_length=int(msg_length)
            msg=conn.recv(msg_length).decode('utf-8')
            print(f"[{addr}] {msg}")
            if msg=="X":
                connected=False
                print(f"[{addr}] DISCONNECTED")
            conn.send("Msg received".encode("utf-8"))
    conn.close()
def start():
    server.listen()
    print(f"[LISTENING] Server is listening {SERVER}")
    while True:
        conn,addr=server.accept()
        thread=threading.Thread(target=handle_client,args=(conn,addr))
        thread.start()
        print(f"[ACTIVE]{threading.active_count()-1}")

print("SERVER IS STARTING...")
start()