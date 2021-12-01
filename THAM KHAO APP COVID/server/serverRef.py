import socket
import tkinter as tk
import json
import time
import schedule
import threading
import sys
import os
from _thread import *
from tkinter import *
from tkinter import messagebox
import getAPI#file local
import getDatabase#file local
import tkinter.scrolledtext as tkscrolled
from datetime import datetime

#define
BUTTON_COLOR = "#EEE8AA"
HEADER_COLOR = "#9966FF"

#define
IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
filename='login.json'

global checkShutdown
checkShutdown = 0
def btnOut_click():
    global checkShutdown
    checkShutdown = 1
    #sys.exit(0)
    
def btnRenew_click():
    textShowUser.delete(1.0, END)
    date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    textShowUser.insert(END, date_time + "\n")
    on_active = str(threading.activeCount() - 4)
    if checkShutdown == 1:
        on_active = str(threading.activeCount() - 3)
    renew_show = ""
    renew_show = "User activing: " + on_active + "\n"
    if len(my_clients) != 0:
        renew_show += '\n'.join(map(str, my_clients))
        renew_show += "\n"
        
    textShowUser.insert(END, renew_show)
    if checkShutdown == 1:
        textShowUser.insert(END, "Database stopped updating!\n")
    print(renew_show)

def getAPIdata():
    getAPI.getData()
    schedule.every(60).minutes.do(getAPI.getData)
    while True:
        if checkShutdown == 1:
            break
        schedule.run_pending()
        time.sleep(1)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    while True:
        data = conn.recv(1024)
        #dang nhap
        if data==b'login':
            filesize = os.path.getsize(filename)
            if filesize == 0:
                print("Chua co tai khoan nao duoc dang ki")
                conn.send(b'fail')
                conn.recv(1024)
                conn.send(b'ok')
            else:
                conn.send(b'success')
                username1= conn.recv(1024)
                conn.send(b'ok')
                password1= conn.recv(1024)
                conn.send(b'ok')
                username=username1.decode(FORMAT)
                password=password1.decode(FORMAT)
                with open(filename, "r") as readinfo:
                    datastore = json.load(readinfo)
                check=False
                for person in datastore['user']:
                    if person['username']== username:
                        if person['password'] == password:
                            check=True
                  # kiem tra dang nhap     
                if check == True:
                    conn.recv(1024)
                    conn.send(b'yes')
                else:
                    conn.recv(1024)
                    conn.send(b'no')
        #dang ki
        elif data== b'signup':
            conn.send(b'ok')
            username1= conn.recv(1024)
            conn.send(b'ok')
            password1= conn.recv(1024)
            conn.send(b'ok')
            username=username1.decode(FORMAT)
            password=password1.decode(FORMAT)
            check=True
            filesize = os.path.getsize(filename)
            conn.recv(1024)
            if filesize==0:
                conn.send(b'yes')
                data = {}
                data['user'] = []
                data['user'].append({
                        'username': username,
                         'password': password
                    })
                with open ('login.json' , 'w') as writefile:
                    json.dump(data, writefile)
            else: 
                with open("login.json", "r") as readinfo:
                    datastore = json.load(readinfo)
                for person in datastore['user']:
                    if person['username'] == username:
                        check=False
                if check==True:
                    conn.send(b'yes')
                    data = {}
                    data['user'] = []
                    for person in datastore['user']:
                        data['user'].append({
                            'username' : person['username'],
                            'password': person['password'],
                        })
    
                    data['user'].append({
                        'username': username,
                         'password': password
                    })
                    with open ('login.json' , 'w') as writefile:
                        json.dump(data, writefile)
                elif check== False:
                    conn.send(b'no')
        elif data == b'search':
            conn.send(b"ok")
            name_search1 = conn.recv(1024)
            name_search = name_search1.decode(FORMAT)
            if name_search[0:3].lower() == "vn/":
                name_search_VN = name_search.replace(name_search[0:3],"")
                name_clear = clearNameInVN(name_search_VN)
                province_info = getDatabase.readDataInVN(name_clear)
                conn.send(province_info.encode())
            else:
                country_info = getDatabase.readDataByCountry(name_search)
                conn.send(country_info.encode())
        elif data==b'exit':
            for i in my_clients:
                if i == addr:
                    my_clients.remove(i)
            break
    conn.close()
    sys.exit(0)

def clearNameInVN(name_search):
    if len(name_search) > 3 or name_search.lower() == "hue":
        if name_search.lower() == "hue" or name_search.lower() == "thua thien hue":
            return "Thua Thien - Hue"
        elif name_search.lower() == "ba ria vung tau" or name_search.lower() == "vung tau" or name_search.lower() == "ba ria":
            return "Ba Ria - Vung Tau"
        elif name_search.lower().replace(".", "").replace(" ", "") == "tphcm" or name_search.lower() == "thanh pho ho chi minh" or name_search.lower() == "tp ho chi minh":
            return "TP. Ho Chi Minh"
        else:
            return name_search
    else:
        #getAPI.getNameProvinceInVN()
        res = getDatabase.readNameProvinceInVN(name_search)
        return res

def showUIServer():
        global window
        window = Tk()
        window.title('Server')
        window.geometry('396x460')
        #content UI in server
        header = Label(window, text = "SERVER MANAGER", fg=HEADER_COLOR, font=("Arial", 18))
        btnRenew = Button(window, text = "Renew", width = 6, fg = "black", bg = BUTTON_COLOR, font=("Arial", 9), command = btnRenew_click)
        global textShowUser
        textShowUser = tkscrolled.ScrolledText(window, font=("Arial", 10), bg = "white", height = 20, width = 50, wrap='word')
        date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        on_active = str(threading.activeCount() - 4)
        active_user = "User activing: " + on_active + "\n"
        textShowUser.insert(END, date_time + "\n" + active_user + "None user")
        btnOut = Button(window, text = "Stop update database", width = 18, fg = "black", bg = BUTTON_COLOR, font=("Arial", 9), command = btnOut_click)
        #place content UI in server
        header.grid(row = 0, column = 1, pady = 10, padx = 85)
        btnRenew.grid(row = 1, column = 1)
        textShowUser.grid(row = 2, column = 1, pady = 10)
        btnOut.grid(row = 3, column = 1, pady = 5)
        window.mainloop()

def runServer():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    thread1 = threading.Thread(target=showUIServer)
    thread1.start()
    global my_clients
    my_clients=[]
    while True:
        conn, addr = server.accept()
        my_clients += [addr]
        thread2 = threading.Thread(target=handle_client, args=(conn, addr))
        thread2.start()

    thread1.join()
    thread2.join()
    

    

    