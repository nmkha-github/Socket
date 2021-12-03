import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image  #Install Pillow 
def center(app,width,height): #Center app screen
    screen_width=app.winfo_screenwidth()
    screen_height=app.winfo_screenheight()-200
    x=(screen_width/2) - (width/2)
    y=(screen_height/2) - (height/2)
    app.geometry(f'{width}x{height}+{int(x)}+{int(y)}')
    return app
def login():
    username=input_user_login.get()
    password=input_pass_login.get()
    if(username==""):
        messagebox.showinfo(title="ALERT",message="Please type a username")
        return
    if(password==""):
        messagebox.showinfo(title="ALERT",message="Please type a password")
        return
    
    messagebox.showinfo(title="ALERT",message="Login successfully") #Dùng socket check nhé
    loginPage.withdraw()
    MainPage()
def LoginPage():
    global loginPage
    loginPage=Toplevel()
    loginPage.title("COVID 19 SERVER MANAGEMENT")
    loginPage=center(loginPage,380,180)
    #loginPage.geometry("320x200")
    lbl_welcome=tk.Label(loginPage,text="COVID 19 SERVER MANAGEMENT",font=("Helvetica", 13,"bold"),fg='black')
    lbl_login=tk.Label(loginPage,text="LOGIN",font=("Helvetica", 13,"bold"),fg='black')
    lbl_username=tk.Label(loginPage,text="Username:",font=("Helvetica", 13,"bold"),fg='black')
    lbl_password=tk.Label(loginPage,text="Password:",font=("Helvetica", 13,"bold"),fg='black')
    blank=tk.Label(loginPage,text="")
    global input_user_login
    global input_pass_login
    input_user_login=tk.Entry(loginPage,width=30,font=("Helvetica", 10))
    input_pass_login=tk.Entry(loginPage,width=30,show="*",font=("Helvetica", 10))
    but_log=tk.Button(loginPage,text="LOGIN",width=10,command=login) #Cần socket để xử lý tiếp
    lbl_welcome.grid(column=1,row=0)
    lbl_login.grid(column=1,row=1)
    lbl_username.grid(column=0,row=2)
    lbl_password.grid(column=0,row=3)
    input_user_login.grid(column=1,row=2)
    input_pass_login.grid(column=1,row=3)
    blank.grid(row=4,column=1)
    but_log.grid(row=5,column=1)
    loginPage.protocol("WM_DELETE_WINDOW", lambda: exit(app))
app = Tk()
app.title('COVID 19 SERVER MANAGEMENT')
app=center(app,500,100)
app.withdraw()
LoginPage() #Có socket xử lý tiếp
def MainPage():
    global mainPage
    mainPage=Toplevel()
    mainPage.title("COVID 19 SERVER MANAGEMENT")
    mainPage=center(mainPage,400,500)
app.mainloop()