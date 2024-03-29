import socket
import os
import threading
import schedule
import time
import sys
import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
import tkinter.scrolledtext as tkscrolled
from PIL import ImageTk, Image  # Install Pillow
from dataManage import *
#
PORT = 8000
#
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), PORT))
s.listen()
HOST = s.getsockname()[0]
#


def exit(page):
    sys.exit()


def receive_account_password(conn):
    acc = conn.recv(1024).decode('utf8')
    psw = conn.recv(1024).decode('utf8')
    return acc, psw


def receive_province_date(conn):
    province = conn.recv(1024).decode('utf8')
    date = conn.recv(1024).decode('utf8')
    return province, date


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


def show_connections(conn, addr, status, color="Black"):
    time = get_time_connect()
    show(time)
    show("Client's addr: (" + addr[0] + ", " + str(addr[1]) + ")" + "\n")
    show("Status: " + status + '\n')
    connecteduser.see('end')


def handle_client(conn, addr):
    global running
    running = True
    print("Address: ", addr)
    show_connections(conn, addr, "Connected")
    account = ''
    isReconnected = False
    while running:
        try:
            request = conn.recv(1024).decode('utf8') 
            if running == False:
                break
            print(len(request))
            if request == "SignIn":
                send_accepted_request(conn, request)
                account, password = receive_account_password(conn)
                status = "Account does not exist."
                if checkAccounts(account):
                    status = SignIn(account, password)
                conn.sendall(status.encode('utf8'))
                show_connections(conn, addr, status +
                                 " (user: " + account + ")")
            if request == "SignUp":
                send_accepted_request(conn, request)
                account, password = receive_account_password(conn)
                status = SignUp(account, password)
                conn.sendall(status.encode('utf8'))
                show_connections(conn, addr, status)
            if request == "Disconnect":
                send_accepted_request(conn, request)
                show_connections(conn, addr, "Client has been disconnected")
                my_clients.remove(addr)
                break
            if request == "LogOut":
                send_accepted_request(conn, request)
                show_connections(
                    conn, addr, "User (" + account + ") logged out.")
            if request == "Search":
                send_accepted_request(conn, request)
                province, date = receive_province_date(conn)
                date_list = date.split("/")
                if len(date_list) == 3:
                    date = date_list[2]
                    if len(date_list[1]) < 2:
                        date += '0'
                    date += date_list[1]
                    if len(date_list[0]) < 2:
                        date += '0'
                    date += date_list[0]
                search_result = SearchData(province, date)
                if (not('not found' in search_result)):
                    search_result = json.dumps(
                        search_result, ensure_ascii=False)
                conn.sendall(search_result.encode('utf8'))
                show_connections(conn, addr, "User (" + account + ") search.")
            if request == 'Reconnect':
                isReconnected = True
                send_accepted_request(conn, request)
                show_connections(conn, addr, "Client reconnected.")
            if request == "":  # Kiểm tra client còn sống hay không
                send_accepted_request(conn, "Check live")
        except:  # nếu có lỗi do client ngắt kết nối
            if (isReconnected == False):
                show_connections(conn, addr, "Client has been shutdown.")
            else:
                isReconnected = True
            break
    conn.close()



print("Server: ", s.getsockname())

my_clients = []


def live_server():
    global s
    while True:
        try:
            conn, addr = s.accept()
            my_clients.append(addr)
            thr = threading.Thread(target=handle_client, args=(conn, addr))
            thr.daemon = True
            thr.start()
        except:
            show_connections(conn, addr, "Client has been disconnected.")

#


def center(app, width, height):
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()-200
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    app.geometry(f'{width}x{height}+{int(x)}+{int(y)}')
    return app


def left(app, width, height): 
    app.geometry(f'{width}x{height}+{0}+{0}')
    return app


def refresh():
    connecteduser.delete(1.0, END)


running = True


def disconnectAll():
    global running
    global my_clients
    running = False
    while len(my_clients) > 0:
        client = my_clients[len(my_clients) - 1]
        show_connections(False, client, 'Client has been disconnected.')
        my_clients.remove(client)


def MainPage():
    global mainPage
    mainPage = Toplevel()
    mainPage.title("COVID 19 SERVER MANAGEMENT")
    mainPage.iconbitmap(bitmap=os.getcwd() + "\\logo.ico")
    mainPage = left(mainPage, 740, 500)
    mainPage.geometry()
    mainPage.resizable(width=False, height=False)
    lbl_welcome = tk.Label(mainPage, text="COVID 19 SERVER MANAGEMENT", font=(
        "Helvetica", 13, "bold"), fg='black')
    lbl_connecteduser = tk.Label(mainPage, text="Connected users: ", font=(
        "Helvetica", 13, "bold"), fg='black')
    frame_but = tk.Frame(mainPage)
    but_exit = tk.Button(frame_but, text="Exit", width=10,
                         command=lambda: exit(mainPage))
    but_refresh = tk.Button(frame_but, text="Refresh",
                            width=10, command=refresh)
    but_disconnectAll = tk.Button(
        frame_but, text="Disconnect all", width=12, command=disconnectAll)
    blank = tk.Label(frame_but, text="                          ")
    lbl_ipserver = tk.Label(frame_but, text=f'SERVER IP: {HOST}', font=(
        "Helvetica", 13, "bold"), fg='black')
    lbl_port = tk.Label(frame_but, text=f'PORT: {PORT}', font=(
        "Helvetica", 13, "bold"), fg='black')
    lbl_welcome.grid(column=1, row=0, padx=60, pady=10)
    lbl_ipserver.grid(column=1, row=1, sticky='w', padx=10)
    lbl_port.grid(column=1, row=2, sticky="w", padx=10)
    blank.grid(column=2, row=1, padx=70)
    but_refresh.grid(column=3, row=1, sticky="w", padx=7)
    but_disconnectAll.grid(column=4, row=1, sticky="w", padx=7)
    but_exit.grid(column=5, row=1, sticky="w", padx=7)
    lbl_connecteduser.grid(column=1, row=3)
    global connecteduser
    connecteduser = tkscrolled.ScrolledText(mainPage, font=(
        "Helvetica", 13), bg="white", height=13, width=76)
    connecteduser.grid(row=4, column=1, pady=10, padx=10)
    frame_but.grid(row=2, column=1, sticky="w")
    mainPage.protocol("WM_DELETE_WINDOW", lambda: exit(app))
    # Bật live server, lắng nghe kết nối clients
    global thr
    thr = threading.Thread(target=live_server)
    thr.daemon = True
    thr.start()


def runServer():
    global app
    app = Tk()
    app.title('COVID 19 SERVER MANAGEMENT')
    app = center(app, 500, 100)
    app.resizable(width=False, height=False)
    app.withdraw()
    MainPage()  # Có socket xử lý tiếp
    app.mainloop()


def update60m():
    update_data()
    schedule.every().hours.do(update_data)
    while True:
        schedule.run_pending()
        time.sleep(1)


thr1 = threading.Thread(target=update60m)
thr1.daemon = True
thr1.start()
runServer()
