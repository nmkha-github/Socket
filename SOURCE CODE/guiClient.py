import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image  #Install Pillow 
LARGE_FONT = ("Helvetica", 13,"bold")
class LoginPage(tk.Frame):
    def __init__(self,master,controller):
        tk.Frame.__init__(self,master)
        lbl_welcome=tk.Label(self,text="WELCOME TO COVID 19 INFORMATION",font=("Helvetica", 13,"bold"),fg='black')
        lbl_login=tk.Label(self,text="LOGIN",font=("Helvetica", 13,"bold"),fg='black')
        lbl_username=tk.Label(self,text="Username:",font=LARGE_FONT,fg='black')
        lbl_password=tk.Label(self,text="Password:",font=LARGE_FONT,fg='black')
        self.input_user=tk.Entry(self,width=30,bg='light yellow')
        self.input_pass=tk.Entry(self,width=30,bg="light yellow")
        self.result=tk.Label(self,text="",font=("Helvetica", 11,"bold"),fg='red')
        self.but_log=tk.Button(self,text="LOGIN",width=10)
        lbl_welcome.grid(column=1,row=0)
        lbl_login.grid(column=1,row=1)
        lbl_username.grid(column=0,row=2)
        lbl_password.grid(column=0,row=3)
        self.input_user.grid(column=1,row=2)
        self.input_pass.grid(column=1,row=3)
        self.but_log.grid(row=4,column=1)
        self.result.grid(row=5,column=1)
class RegistrationPage(tk.Frame):
    def _ini__(self,master):
        tk.Frame.__init__(self,master)
        lbl_test=tk.Label(self,text="Alo")
        lbl_test.pack()
class ServerApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("COVID 19 INFORMATION")
        self.geometry("500x200")
        self.resizable(width=FALSE,height=FALSE)
        frame=tk.Frame()
        loginFrame=LoginPage(frame)
        frame.pack()
        loginFrame.pack()
    # def logIn(self,frame):
    #     username = frame.input_user.get()
    #     password = frame.input_pass.get()
    #     if username == "admin" and password == "admin":
    #         #self.showFrame(HomePage)
    #         frame.result["text"] = "Login successfully."
    #     else:
    #         frame.result["text"] = "Username or password is incorrect."
app = ServerApp()
app.mainloop()