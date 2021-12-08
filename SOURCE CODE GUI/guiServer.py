import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
import tkinter.scrolledtext as tkscrolled
from PIL import ImageTk, Image  #Install Pillow 
IPSERVER="192.168.78.1"
PORT=8000
def center(app,width,height): #Center app screen
    screen_width=app.winfo_screenwidth()
    screen_height=app.winfo_screenheight()-200
    x=(screen_width/2) - (width/2)
    y=(screen_height/2) - (height/2)
    app.geometry(f'{width}x{height}+{int(x)}+{int(y)}')
    return app
# def login():
#     username=input_user_login.get()
#     password=input_pass_login.get()
#     if(username==""):
#         messagebox.showinfo(title="ALERT",message="Please type a username")
#         return
#     if(password==""):
#         messagebox.showinfo(title="ALERT",message="Please type a password")
#         return
#     if(username=="admin" and password=="admin"):
#         messagebox.showinfo(title="ALERT",message="Login successfully") 
#         loginPage.withdraw()
#         MainPage()
#         return
#     else:
#         messagebox.showinfo(title="ALERT",message="Incorrect username or password")
#         return
# def LoginPage():
#     global loginPage
#     loginPage=Toplevel()
#     loginPage.title("COVID 19 SERVER MANAGEMENT")
#     loginPage=center(loginPage,380,180)
#     #loginPage.geometry("320x200")
#     lbl_welcome=tk.Label(loginPage,text="COVID 19 SERVER MANAGEMENT",font=("Helvetica", 13,"bold"),fg='black')
#     lbl_login=tk.Label(loginPage,text="LOGIN",font=("Helvetica", 13,"bold"),fg='black')
#     lbl_username=tk.Label(loginPage,text="Username:",font=("Helvetica", 13,"bold"),fg='black')
#     lbl_password=tk.Label(loginPage,text="Password:",font=("Helvetica", 13,"bold"),fg='black')
#     loginPage.bind('<Return>',lambda e:login()) #Bấm enter
#     blank=tk.Label(loginPage,text="")
#     global input_user_login
#     global input_pass_login
#     input_user_login=tk.Entry(loginPage,width=30,font=("Helvetica", 10))
#     input_pass_login=tk.Entry(loginPage,width=30,show="*",font=("Helvetica", 10))
#     but_log=tk.Button(loginPage,text="LOGIN",width=10,command=login) #Cần socket để xử lý tiếp
#     lbl_welcome.grid(column=1,row=0)
#     lbl_login.grid(column=1,row=1)
#     lbl_username.grid(column=0,row=2)
#     lbl_password.grid(column=0,row=3)
#     input_user_login.grid(column=1,row=2)
#     input_pass_login.grid(column=1,row=3)
#     blank.grid(row=4,column=1)
#     but_log.grid(row=5,column=1)
#     loginPage.protocol("WM_DELETE_WINDOW", lambda: exit(app))
def MainPage():
    global mainPage
    mainPage=Toplevel()
    mainPage.title("COVID 19 SERVER MANAGEMENT")
    mainPage=center(mainPage,400,500)
    mainPage.resizable(width=False,height=False)
    lbl_welcome=tk.Label(mainPage,text="COVID 19 SERVER MANAGEMENT",font=("Helvetica", 13,"bold"),fg='black')
    lbl_ipserver=tk.Label(mainPage,text=f'SERVER IP: {IPSERVER}',font=("Helvetica", 13,"bold"),fg='black')
    lbl_port=tk.Label(mainPage,text=f'PORT: {PORT}',font=("Helvetica", 13,"bold"),fg='black')    
    lbl_connecteduser=tk.Label(mainPage,text="Connected users: ",font=("Helvetica", 13,"bold"),fg='black')
    lbl_welcome.grid(column=1,row=0,padx=60,pady=10)
    lbl_ipserver.grid(column=1,row=1,sticky='w',padx=10)
    lbl_port.grid(column=1,row=2,sticky="w",padx=10)
    lbl_connecteduser.grid(column=1,row=3)
    global connecteduser
    connecteduser = tkscrolled.ScrolledText(mainPage, font=("Helvetica", 13), bg = "white", height = 13, width = 40)
    connecteduser.grid(row=4,column=1,pady=10)
    connecteduser.insert(END,"Hello")  #Hàm insert text
    #connecteduser.delete(1.0,END) #Xóa tất cả các text. Lúc refresh hay gì thì xài
    connecteduser.configure(state ='disabled') #Hàm này không cho nhập
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