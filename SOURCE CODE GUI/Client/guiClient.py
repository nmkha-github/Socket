import socket
import tkinter as tk
import sys
import json
import os
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image  # Install Pillow
from datetime import datetime, timedelta


def center(app, width, height):  # Center app screen
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()-200
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    app.geometry(f'{width}x{height}+{int(x)}+{int(y)}')
    return app


def exit(page):  # function tắt
    # Socket gửi request exit
    sys.exit()


def ConnectServer():
    global client, ip, port
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = input_ip.get()
    port = input_port.get()
    # Cảnh báo chưa nhập
    if(ip == ""):
        lbl_alert["text"] = "Please type a server IP address"
        return
    if(port == ""):
        lbl_alert["text"] = "Please type a port"
        return
    # Kết nối
    try:
        client.connect((ip, int(port)))
        lbl_alert["text"] = "Connect successfully"  # Dùng socket check
        app.withdraw()
        LoginPage()  # Có socket để check kết nối
    except:
        # IP Port ko đúng
        lbl_alert["text"] = "Failed to connect, please type again."
        print("SERVER not found")


def runClient():
    global app
    app = Tk()
    app.title('COVID 19 VIETNAM INFORMATION')
    app = center(app, 500, 170)
    # app.geometry('500x100')
    app.resizable(width=False, height=False)
    lbl_welcome = tk.Label(app, text="Enter server IP address: ", font=(
        "Helvetica", 13, "bold"), fg='black')
    global lbl_alert
    lbl_alert = tk.Label(app, text="", font=(
        "Helvetica", 10, "bold"), fg='red')
    global input_ip
    global input_port
    input_ip = tk.Entry(app, width=50)
    lbl_enterPort = tk.Label(app, text="Enter Port: ", font=(
        "Helvetica", 13, "bold"), fg='black')
    input_port = tk.Entry(app, width=50)
    lbl_welcome.pack()
    input_ip.pack()
    lbl_enterPort.pack()
    input_port.pack(pady=5)
    but_connect = tk.Button(app, text="CONNECT",
                            width=20, command=ConnectServer)
    app.bind('<Return>', lambda e: ConnectServer())  # Bấm enter
    but_connect.pack(pady=6)
    lbl_alert.pack()
    app.mainloop()


def disconnectServer(page):
    request = "Disconnect"
    client.sendall(request.encode('utf8'))
    print(client.recv(1024).decode('utf8'))
    client.close()
    page.withdraw()
    runClient()


def tempFuncion():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # request = "Reconnect"
    # client.sendall(request.encode('utf8'))
    # print(client.recv(1024).decode('utf8'))


def Reconnect():
    try:
        client.close()
        tempFuncion()
        client.close()
        disPage.withdraw()
        runClient()
    except:
        print('Reconnect unsuccessful!')


def ServerDisconnectedPage():
    global disPage
    disPage = Toplevel()
    disPage.title("COVID 19 VIETNAM INFORMATION")
    disPage.resizable(width=False, height=False)
    # set background image
    c = Canvas(disPage, height=200, width=200)
    fileName = os.path.dirname(os.path.abspath(
        __file__)) + '\\background_disconnectpage.png'
    img = ImageTk.PhotoImage(file=fileName)
    disPage.geometry(f'{img.width()}x{img.height()}')
    bg_label = Label(disPage, image=img)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    c.pack()
    reconnectBtn = tk.Button(disPage, text="Reload", font=(
        "Helvetica", 10, "bold"), fg='black', bg='#af926a', command=lambda: Reconnect())
    reconnectBtn.place(width=80, height=30, x=145, y=350)
    exitBtn = tk.Button(disPage, text="Exit", font=(
        "Helvetica", 10, "bold"), fg='black', command=lambda: exit(disPage))
    exitBtn.place(width=80, height=30, x=235, y=350)
    disPage.mainloop()


def sign_up_button():
    loginPage.withdraw()
    RegistrationPage()


def send_account_password(username, password):
    client.sendall(username.encode('utf8'))
    client.sendall(password.encode('utf8'))


def login():
    global username
    username = input_user_login.get()  # Để tạo Hi, username trong màn hình chính
    password = input_pass_login.get()
    if(username == ""):
        lbl_loginalert["text"] = "Please type a username"
        return
    if(password == ""):
        lbl_loginalert["text"] = "Please type a password"
        return
    # Kết nối
    try:
        request = "SignIn"
        client.sendall(request.encode('utf8'))
        print(client.recv(1024).decode('utf8'))
        send_account_password(username, password)
        reply = client.recv(1024).decode('utf8')
        if reply != "Login successful!":
            # Dùng socket check tài khoản mật khẩu
            lbl_loginalert["text"] = "Incorrect username or password"
            return
        loginPage.withdraw()
        # Dùng socket check tài khoản mật khẩu
        lbl_loginalert["text"] = "Login successfully"
        MainPage()
    except:
        loginPage.withdraw()
        ServerDisconnectedPage()


def LoginPage():
    global loginPage
    loginPage = Toplevel()
    loginPage.title("COVID 19 VIETNAM INFORMATION")
    loginPage = center(loginPage, 420, 190)
    loginPage.resizable(width=False, height=False)
    lbl_welcome = tk.Label(loginPage, text="COVID 19 VIETNAM INFORMATION", font=(
        "Helvetica", 13, "bold"), fg='black')
    lbl_login = tk.Label(loginPage, text="LOGIN", font=(
        "Helvetica", 13, "bold"), fg='black')
    lbl_username = tk.Label(loginPage, text="Username:", font=(
        "Helvetica", 13, "bold"), fg='black')
    lbl_password = tk.Label(loginPage, text="Password:", font=(
        "Helvetica", 13, "bold"), fg='black')
    global lbl_loginalert
    lbl_loginalert = tk.Label(loginPage, text="", font=(
        "Helvetica", 10, "bold"), fg='red')
    global input_user_login
    global input_pass_login
    input_user_login = tk.Entry(loginPage, width=30, font=("Helvetica", 10))
    input_pass_login = tk.Entry(
        loginPage, width=30, show="*", font=("Helvetica", 10))
    but_log = tk.Button(loginPage, text="LOGIN", width=10,
                        command=login)  # Cần socket để xử lý tiếp
    but_reg = tk.Button(loginPage, text="Create new account",
                        width=15, command=sign_up_button)
    but_disconnect = tk.Button(loginPage, text="Disconnect",
                               width=15, command=lambda: disconnectServer(loginPage))
    loginPage.bind('<Return>', lambda e: login())  # Bấm enter
    lbl_welcome.grid(column=1, row=0)
    lbl_login.grid(column=1, row=1)
    lbl_username.grid(column=0, row=2)
    lbl_password.grid(column=0, row=3)
    input_user_login.grid(column=1, row=2)
    input_pass_login.grid(column=1, row=3)
    lbl_loginalert.grid(row=4, column=1)
    but_reg.grid(row=5, column=0, padx=10)
    but_log.grid(row=5, column=1)
    but_disconnect.grid(row=6, column=0, padx=10, pady=5)
    loginPage.protocol("WM_DELETE_WINDOW", lambda: exit(app))


def back_to_login():
    registrationPage.withdraw()
    LoginPage()


def register():  # Socket đăng ký
    username = input_user_signup.get()
    password = input_pass_signup.get()
    confirmpassword = input_copass_signup.get()
    if(username == ""):
        lbl_registeralert["text"] = "Please type a username"
        return
    if(password == ""):
        lbl_registeralert["text"] = "Please type a password"
        return
    if(confirmpassword == ""):
        lbl_registeralert["text"] = "Please confirm your password"
        return
    if(password != confirmpassword):
        lbl_registeralert["text"] = "The password confirmation does not match"
        return
    # Kết nối
    try:
        request = "SignUp"
        client.sendall(request.encode('utf8'))
        print(client.recv(1024).decode('utf8'))
        send_account_password(username, password)
        reply = client.recv(1024).decode('utf8')
        # Dùng socket check tài khoản mật khẩu
        lbl_registeralert["text"] = reply
        return
    except:
        lbl_registeralert["text"] = "Fail to sign up"  # Đăng ký thất bại
        registrationPage.withdraw()
        ServerDisconnectedPage()


def RegistrationPage():
    global registrationPage
    registrationPage = Toplevel()
    registrationPage.title("COVID 19 VIETNAM INFORMATION")
    registrationPage = center(registrationPage, 450, 180)
    # registrationPage.geometry("400x180")
    registrationPage.resizable(width=False, height=False)
    lbl_login = tk.Label(registrationPage, text="REGISTER",
                         font=("Helvetica", 13, "bold"), fg='black')
    lbl_username = tk.Label(registrationPage, text="Username:", font=(
        "Helvetica", 13, "bold"), fg='black')
    lbl_password = tk.Label(registrationPage, text="Password:", font=(
        "Helvetica", 13, "bold"), fg='black')
    lbl_repassword = tk.Label(registrationPage, text="Confirm password:", font=(
        "Helvetica", 13, "bold"), fg='black')
    global lbl_registeralert
    lbl_registeralert = tk.Label(
        registrationPage, text="", font=("Helvetica", 10, "bold"), fg='red')
    global input_user_signup
    global input_pass_signup
    global input_copass_signup
    input_user_signup = tk.Entry(
        registrationPage, width=40, font=("Helvetica", 10))
    input_pass_signup = tk.Entry(
        registrationPage, width=40, font=("Helvetica", 10), show="*")
    input_copass_signup = tk.Entry(
        registrationPage, width=40, font=("Helvetica", 10), show="*")
    but_register = tk.Button(
        registrationPage, text="REGISTER", width=20, command=register)  # Socket
    but_disconnect = tk.Button(registrationPage, text="Disconnect",
                               width=15, command=lambda: disconnectServer(registrationPage))
    but_backToLogin = tk.Button(
        registrationPage, text="Back to login", width=15, command=back_to_login)
    registrationPage.bind('<Return>', lambda e: register())  # Bấm enter
    lbl_login.grid(column=1, row=1)
    lbl_username.grid(column=0, row=2)
    lbl_password.grid(column=0, row=3)
    lbl_repassword.grid(column=0, row=4)
    input_user_signup.grid(column=1, row=2)
    input_pass_signup.grid(column=1, row=3)
    input_copass_signup.grid(column=1, row=4)
    lbl_registeralert.grid(column=1, row=5)
    but_backToLogin.grid(row=6, column=0)
    but_register.grid(row=6, column=1)
    but_disconnect.grid(row=7, column=0)
    registrationPage.protocol("WM_DELETE_WINDOW", lambda: exit(app))


def send_date_province(date, province):
    client.sendall(date.encode('utf8'))
    client.sendall(province.encode('utf8'))


def Search():  # Dùng socket để chỉnh
    date = input_date.get()
    province = input_province.get()
    if(province == ''):
        messagebox.showinfo("Alert", "Please type a province.")
        return
    try:
        request = "Search"
        client.sendall(request.encode('utf8'))
        print(client.recv(1024).decode('utf8'))

        client.sendall(province.encode('utf8'))
        client.sendall(date.encode('utf8'))
        data_recv = client.recv(1024).decode('utf8')
        if "not found!" in data_recv:
            lbl_resultprovince['text'] = data_recv
            lbl_resultnewcases["text"] = ''
            lbl_resultdeaths["text"] = ''
            lbl_resulttotalcases["text"] = ''
        else:
            data_recv = json.loads(data_recv)
            lbl_resultprovince["text"] = data_recv['province']
            lbl_resultnewcases["text"] = data_recv['newCases']
            lbl_resultdeaths["text"] = data_recv['deaths']
            lbl_resulttotalcases["text"] = data_recv['cases']
    except:
        mainPage.withdraw()
        ServerDisconnectedPage()


def logOut():
    # Dùng socket để logout
    try:  # Nếu có thể gửi và nhận thì server vẫn còn sống
        client.sendall("LogOut".encode('utf8'))  # Gửi request cho server
        print(client.recv(1024).decode('utf8'))  # Nhận reply accept từ server
        mainPage.withdraw()
        LoginPage()
    except:
        mainPage.withdraw()
        ServerDisconnectedPage()


def MainPage():
    global mainPage
    mainPage = Toplevel()
    mainPage.title("COVID 19 VIETNAM INFORMATION")
    mainPage = center(mainPage, 430, 500)
    mainPage.resizable(width=False, height=False)
    lbl_hiuser = tk.Label(mainPage, text=f'Hi, {username}', font=(
        "Helvetica", 10, "bold"), fg='black')
    but_disconnect = tk.Button(
        mainPage, text="Disconnect", width=15, command=lambda: disconnectServer(mainPage))
    lbl_welcome = tk.Label(mainPage, text="COVID 19 VIETNAM INFORMATION", font=(
        "Helvetica", 13, "bold"), fg='black')
    blank = tk.Label(loginPage, text="")
    global input_province
    lbl_province = tk.Label(mainPage, text="Province: ", font=(
        "Helvetica", 10, "bold"), fg='black')
    input_province = tk.Entry(mainPage, width=40, font=("Helvetica", 10))
    lbl_date = tk.Label(mainPage, text="Date: ", font=(
        "Helvetica", 10, "bold"), fg='black')
    global input_date
    input_date = ttk.Combobox(mainPage, width=38, font=(
        "Helvetica", 10), state="readonly")
    date_time_now = datetime.now().strftime("%d/%m/%Y")
    data_time_yesterday = (datetime.now()-timedelta(1)).strftime("%d/%m/%Y")
    data_time_previous = (datetime.now()-timedelta(2)).strftime("%d/%m/%Y")
    input_date['value'] = (
        date_time_now, data_time_yesterday, data_time_previous)
    input_date.current(0)
    but_search = tk.Button(mainPage, text="Search", width=10, command=Search)
    lbl_result = tk.Label(mainPage, text="Result", font=(
        "Helvetica", 13, "bold"), fg='black')  # Hàm search
    lbl_note = tk.Label(mainPage, text=f'Note: You can just choose a date from {data_time_previous} to {date_time_now}.', font=(
        "Helvetica", 10, "bold"), fg='black')
    lbl_provinceresult = tk.Label(mainPage, text="Province:", font=(
        "Helvetica", 13, "bold"), fg='black')
    lbl_totalcases = tk.Label(mainPage, text="Total cases:", font=(
        "Helvetica", 13, "bold"), fg='black')
    lbl_newcases = tk.Label(mainPage, text="New cases:", font=(
        "Helvetica", 13, "bold"), fg='black')
    lbl_deaths = tk.Label(mainPage, text="Total deaths:",
                          font=("Helvetica", 13, "bold"), fg='black')
    but_exit = tk.Button(mainPage, text="Exit", width=10,
                         command=lambda: exit(mainPage))
    global lbl_resultdeaths
    global lbl_resultnewcases
    global lbl_resultprovince
    global lbl_resulttotalcases
    lbl_resultprovince = tk.Label(
        mainPage, text="", font=("Helvetica", 13, "bold"), fg='red')
    lbl_resulttotalcases = tk.Label(
        mainPage, text="", font=("Helvetica", 13, "bold"), fg='red')
    lbl_resultnewcases = tk.Label(
        mainPage, text="", font=("Helvetica", 13, "bold"), fg='red')
    lbl_resultdeaths = tk.Label(mainPage, text="", font=(
        "Helvetica", 13, "bold"), fg='red')
    but_logout = tk.Button(mainPage, text="Logout", width=10, command=logOut)
    lbl_hiuser.grid(columnspan=2, row=0, sticky="w", padx=10)
    but_logout.grid(column=0, row=1, sticky="w", pady=10, padx=10)
    but_disconnect.grid(column=1, row=1, sticky="w")
    lbl_welcome.grid(columnspan=2, row=2, pady=10, padx=10)
    lbl_province.grid(column=0, row=3, pady=4)
    input_province.grid(column=1, row=3, pady=4, sticky="w")
    lbl_date.grid(column=0, row=4, pady=4)
    input_date.grid(column=1, row=4, pady=4, sticky="w")
    but_search.grid(column=1, row=6, pady=10, sticky="w", padx=50)
    lbl_note.grid(columnspan=2, row=7, padx=20)
    lbl_result.grid(columnspan=2, row=8, padx=70)
    lbl_provinceresult.grid(column=0, row=9, padx=10, sticky="w")
    lbl_totalcases.grid(column=0, row=10, padx=8, sticky="w")
    lbl_deaths.grid(column=0, row=11, padx=8, sticky="w")
    lbl_newcases.grid(column=0, row=12, padx=10, sticky="w")
    lbl_resultprovince.grid(column=1, row=9, sticky="w")
    lbl_resulttotalcases.grid(column=1, row=10, sticky="w")
    lbl_resultdeaths.grid(column=1, row=11, sticky="w")
    lbl_resultnewcases.grid(column=1, row=12, sticky="w")
    but_exit.grid(column=1, row=13, sticky="w", padx=50, pady=20)
    mainPage.protocol("WM_DELETE_WINDOW", lambda: exit(app))

runClient()
