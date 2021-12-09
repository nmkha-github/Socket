import socket
import threading
import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
import tkinter.scrolledtext as tkscrolled
from PIL import ImageTk, Image  #Install Pillow 
from dataManage import *
#
HOST = '127.0.0.1'  
PORT = 8000 
#
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
#
def exit(page):
    #Socket gửi request exit
    page.destroy()
def receive_account_password(conn):
    acc = conn.recv(1024).decode('utf8')
    psw = conn.recv(1024).decode('utf8')
    return acc, psw

def show(text):
    connecteduser.insert('end', text)
def send_accepted_request(conn, request):
    conn.sendall(("Accept " + request).encode('utf8'))
def get_time_connect():
    now = datetime.now()
    result = now.strftime('%d/%m/%Y %H:%M:%S')
    if now.hour < 12:
        result += "AM, "
    else:
        result += "PM, "
    return result
def show_connections(conn, addr, status):
    time = get_time_connect()
    show(time)
    show("Client's addr: (" + addr[0] + ", " + str(addr[1]) + ")\nStatus: ")
    show(status + '\n')
    
def handle_client(conn, addr):
    print("Address: ", addr)
    
    while True:
        try:
            request = conn.recv(1024).decode('utf8')
        except:
            pass
        print(request)
        if request == "SignIn":
            send_accepted_request(conn, request)
            account, password = receive_account_password(conn)
            status = "Account does not exist"
            if checkAccounts(account):
                status = SignIn(account, password)
            conn.sendall(status.encode('utf8'))
            show_connections(conn, addr, status)

# xử lí đa luồng
print("Server: ", s.getsockname())
def live_server():
    global s
    while True:
        conn, addr = s.accept()
        try:
            thr = threading.Thread(target=handle_client, args=(conn, addr))
            thr.daemon = True
            thr.start()
        except:
            print("Error")
#
def center(app,width,height): #Center app screen
    screen_width=app.winfo_screenwidth()
    screen_height=app.winfo_screenheight()-200
    x=(screen_width/2) - (width/2)
    y=(screen_height/2) - (height/2)
    app.geometry(f'{width}x{height}+{int(x)}+{int(y)}')
    return app

def MainPage():
    global mainPage
    mainPage=Toplevel()
    mainPage.title("COVID 19 SERVER MANAGEMENT")
    mainPage=center(mainPage,700,500)
    mainPage.resizable(width=False,height=False)
    lbl_welcome=tk.Label(mainPage,text="COVID 19 SERVER MANAGEMENT",font=("Helvetica", 13,"bold"),fg='black')
    lbl_ipserver=tk.Label(mainPage,text=f'SERVER IP: {HOST}',font=("Helvetica", 13,"bold"),fg='black')
    lbl_port=tk.Label(mainPage,text=f'PORT: {PORT}',font=("Helvetica", 13,"bold"),fg='black')    
    lbl_connecteduser=tk.Label(mainPage,text="Connected users: ",font=("Helvetica", 13,"bold"),fg='black')
    but_exit=tk.Button(mainPage,text="Exit",width=10,command=lambda:exit(mainPage))    
    lbl_welcome.grid(column=1,row=0,padx=60,pady=10)
    lbl_ipserver.grid(column=1,row=1,sticky='w',padx=10)
    lbl_port.grid(column=1,row=2,sticky="w",padx=10)
    lbl_connecteduser.grid(column=1,row=3)
    global connecteduser
    connecteduser = tkscrolled.ScrolledText(mainPage, font=("Helvetica", 13), bg = "white", height = 13, width = 75)
    connecteduser.grid(row=4,column=1,pady=10,padx=10)
    but_exit.grid(row=5,column=1,padx=50,pady=20)
    mainPage.protocol("WM_DELETE_WINDOW", lambda: exit(app))
    #Bật live server, lắng nghe kết nối clients
    thr = threading.Thread(target=live_server)
    thr.daemon = True
    thr.start()

    #connecteduser.delete(1.0,END) #Xóa tất cả các text. Lúc refresh hay gì thì xài
    
def runServer():
    global app
    app = Tk()
    app.title('COVID 19 SERVER MANAGEMENT')
    app=center(app,500,100)
    app.resizable(width=False,height=False)
    app.withdraw()
    MainPage() #Có socket xử lý tiếp
    app.mainloop()
runServer()
