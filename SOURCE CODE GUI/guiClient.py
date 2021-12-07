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
app = Tk()
app.title('COVID 19 VIETNAM INFORMATION')
app=center(app,500,100)
#app.geometry('500x100')
lbl_welcome=tk.Label(app,text="Enter server IP address: ",font=("Helvetica", 13,"bold"),fg='black')
lbl_blank=tk.Label(app,text="")
input_ip = tk.Entry(app, width = 50)
lbl_welcome.pack()
input_ip.pack()
lbl_blank.pack()
def ConnectServer():
    app.withdraw()
    LoginPage() #Có socket để check kết nối
but_connect=tk.Button(app,text="CONNECT",width=20,command=ConnectServer)
app.bind('<Return>',lambda e:ConnectServer()) #Bấm enter
but_connect.pack()
def sign_up_button():      
    loginPage.withdraw()
    RegistrationPage()
def login():
    username=input_user_login.get()
    password=input_pass_login.get()
    if(username==""):
        messagebox.showinfo(title="ALERT",message="Please type a username")
        return
    if(password==""):
        messagebox.showinfo(title="ALERT",message="Please type a password")
        return
    messagebox.showinfo(title="ALERT",message="Login successfully") #Dùng socket check tài khoản mật khẩu
    loginPage.withdraw()
    MainPage()
def LoginPage():
    global loginPage
    loginPage=Toplevel()
    loginPage.title("COVID 19 VIETNAM INFORMATION")
    loginPage=center(loginPage,420,180)
    #loginPage.geometry("320x200")
    lbl_welcome=tk.Label(loginPage,text="COVID 19 VIETNAM INFORMATION",font=("Helvetica", 13,"bold"),fg='black')
    lbl_login=tk.Label(loginPage,text="LOGIN",font=("Helvetica", 13,"bold"),fg='black')
    lbl_username=tk.Label(loginPage,text="Username:",font=("Helvetica", 13,"bold"),fg='black')
    lbl_password=tk.Label(loginPage,text="Password:",font=("Helvetica", 13,"bold"),fg='black')
    blank=tk.Label(loginPage,text="")
    global input_user_login
    global input_pass_login
    input_user_login=tk.Entry(loginPage,width=30,font=("Helvetica", 10))
    input_pass_login=tk.Entry(loginPage,width=30,show="*",font=("Helvetica", 10))
    but_log=tk.Button(loginPage,text="LOGIN",width=10,command=login) #Cần socket để xử lý tiếp
    but_reg=tk.Button(loginPage,text="Create new account",width=15,command=sign_up_button)
    loginPage.bind('<Return>',lambda e:login()) #Bấm enter
    lbl_welcome.grid(column=1,row=0)
    lbl_login.grid(column=1,row=1)
    lbl_username.grid(column=0,row=2)
    lbl_password.grid(column=0,row=3)
    input_user_login.grid(column=1,row=2)
    input_pass_login.grid(column=1,row=3)
    blank.grid(row=4,column=1)
    but_reg.grid(row=5,column=0)
    but_log.grid(row=5,column=1)
    loginPage.protocol("WM_DELETE_WINDOW", lambda: exit(app))
def back_to_login():
    registrationPage.withdraw()
    LoginPage()
def register():  #Socket đăng ký
    username=input_user_signup.get()
    password=input_pass_signup.get()
    confirmpassword=input_copass_signup.get()
    if(username==""):
        messagebox.showinfo(title="ALERT",message="Please type a username")
        return
    if(password==""):
        messagebox.showinfo(title="ALERT",message="Please type a password")
        return
    if(password!=confirmpassword):
        messagebox.showinfo(title="ALERT",message="The password confirmation does not match")
        return
    messagebox.showinfo(title="ALERT",message="Your account has been created successfully") #Dùng socket check nhé
    back_to_login()
def RegistrationPage():
    global registrationPage
    registrationPage=Toplevel()
    registrationPage.title("COVID 19 VIETNAM INFORMATION")
    registrationPage=center(registrationPage,400,180)
    #registrationPage.geometry("400x180")
    lbl_login=tk.Label(registrationPage,text="REGISTER",font=("Helvetica", 13,"bold"),fg='black')
    lbl_username=tk.Label(registrationPage,text="Username:",font=("Helvetica", 13,"bold"),fg='black')
    lbl_password=tk.Label(registrationPage,text="Password:",font=("Helvetica", 13,"bold"),fg='black')
    lbl_repassword=tk.Label(registrationPage,text="Confirm password:",font=("Helvetica", 13,"bold"),fg='black')
    blank=tk.Label(registrationPage,text="")
    global input_user_signup
    global input_pass_signup
    global input_copass_signup
    input_user_signup=tk.Entry(registrationPage,width=30,font=("Helvetica", 10))
    input_pass_signup=tk.Entry(registrationPage,width=30,font=("Helvetica", 10),show="*")
    input_copass_signup=tk.Entry(registrationPage,width=30,font=("Helvetica", 10),show="*")
    but_register=tk.Button(registrationPage,text="REGISTER",width=20,command=register) #Socket
    but_backToLogin=tk.Button(registrationPage,text="Back to login",width=10,command=back_to_login)
    registrationPage.bind('<Return>',lambda e:register()) #Bấm enter
    lbl_login.grid(column=1,row=1)
    lbl_username.grid(column=0,row=2)
    lbl_password.grid(column=0,row=3)
    lbl_repassword.grid(column=0,row=4)
    input_user_signup.grid(column=1,row=2)
    input_pass_signup.grid(column=1,row=3)
    input_copass_signup.grid(column=1,row=4)
    blank.grid(column=1,row=5)
    but_backToLogin.grid(row=6,column=0)
    but_register.grid(row=6,column=1)
    registrationPage.protocol("WM_DELETE_WINDOW", lambda: exit(app))
def MainPage():
    global mainPage
    mainPage=Toplevel()
    mainPage.title("COVID 19 VIETNAM INFORMATION")
    mainPage=center(mainPage,400,500)
    # dataTree=ttk.Treeview(mainPage)
    # dataTree["column"]={""}
    lbl_welcome=tk.Label(mainPage,text="COVID 19 VIETNAM INFORMATION",font=("Helvetica", 13,"bold"),fg='black')
    blank=tk.Label(loginPage,text="")
    lbl_province=tk.Label(mainPage,text="Province: ",font=("Helvetica", 10,"bold"),fg='black')
    input_province=tk.Entry(mainPage,width=40,font=("Helvetica", 10))
    lbl_date=tk.Label(mainPage,text="Date: ",font=("Helvetica", 10,"bold"),fg='black')
    format_date = StringVar(mainPage)
    format_date.set("dd/mm/yyyy")
    input_date=tk.Entry(mainPage,width=40,font=("Helvetica", 10),textvariable=format_date)
    but_search=tk.Button(registrationPage,text="Back to login",width=10)
    lbl_welcome.grid(column=1,row=0,pady=20)
    lbl_province.grid(column=0,row=2,pady=4)
    input_province.grid(column=1,row=2,pady=4)
    lbl_date.grid(column=0,row=3,pady=4)
    input_date.grid(column=1,row=3,pady=4)
app.mainloop()