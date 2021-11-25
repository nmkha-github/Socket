import tkinter as tk
import socket

HOST = "127.0.0.1"
SERVER_PORT = 65432
FORMAT = "utf8"

LOGIN = "login"
FAIL = "fail"
OK = "ok"
        
class StartPage(tk.Frame):
    def __init__(self, parent, appController):
        tk.Frame.__init__(self, parent)

        label_title = tk.Label(self, text="LOG IN")
        label_user = tk.Label(self, text="username ")
        label_pswd = tk.Label(self, text="password ")

        self.label_notice = tk.Label(self,text="",bg="bisque2")
        self.entry_user = tk.Entry(self,width=20,bg='light yellow')
        self.entry_pswd = tk.Entry(self,width=20,bg='light yellow')

        button_log = tk.Button(self,text="LOG IN", command=lambda: appController.logIn(self, client) ) 
        button_log.configure(width=10)
        
        label_title.pack()
        label_user.pack()
        self.entry_user.pack()
        label_pswd.pack()
        self.entry_pswd.pack()
        self.label_notice.pack()

        button_log.pack()

class HomePage(tk.Frame):
    def __init__(self, parent, appController):
        tk.Frame.__init__(self, parent)

        label_title = tk.Label(self, text="HOME PAGE")
        btn_logout = tk.Button(self, text="log out", command=lambda: appController.showPage(StartPage))

        label_title.pack()
        btn_logout.pack()        
    
class App(tk.Tk):
    def __init__(self): 
        tk.Tk.__init__(self)

        self.title("My App")
        self.geometry("500x200")
        self.resizable(width=False, height=False)

        #self.protocol("WM_DELETE_WINDOW", self.on_closing)

        container = tk.Frame()
        container.configure(bg="red")

        container.pack(side="top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        self.frames = {}
        for F in (StartPage, HomePage):
            frame = F(container, self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[F] = frame 


        self.frames[StartPage].tkraise()
        
    def showPage(self, FrameClass):
        self.frames[FrameClass].tkraise()
    
    def logIn(self,curFrame,sck: socket):
        try:
            user = curFrame.entry_user.get()
            pswd = curFrame.entry_pswd.get()

            if user == "" or pswd == "":
                curFrame.label_notice["text"] = "Fields cannot be empty"
                return 

            print(user, pswd)
            
            # send command option
            option = LOGIN
            sck.sendall(option.encode(FORMAT))
            
            # send account info
            sck.sendall(user.encode(FORMAT))
            sck.recv(1024)
            sck.sendall(pswd.encode(FORMAT))
            sck.recv(1024)

            # recv login check
            msg = sck.recv(1024).decode(FORMAT)
            if (msg == FAIL):
                curFrame.label_notice["text"] = "invalid password"
                return

            else:
                self.showPage(HomePage)


        except:
            
            print("Error: Server is not responding")

#--------------------------main------------------------
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect( (HOST, SERVER_PORT) )



print("CLIENT SIDE")

app = App()
app.mainloop()
    