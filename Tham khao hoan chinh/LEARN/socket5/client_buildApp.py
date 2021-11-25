import tkinter as tk

        
class StartPage(tk.Frame):
    def __init__(self, parent, appController):
        tk.Frame.__init__(self, parent)

        label_title = tk.Label(self, text="LOG IN")
        label_user = tk.Label(self, text="username ")
        label_pswd = tk.Label(self, text="password ")

        self.label_notice = tk.Label(self,text="",bg="bisque2")
        self.entry_user = tk.Entry(self,width=20,bg='light yellow')
        self.entry_pswd = tk.Entry(self,width=20,bg='light yellow')

        button_log = tk.Button(self,text="LOG IN", command=lambda: appController.showPage(HomePage) ) 
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


app = App()
app.showPage(HomePage)
app.mainloop()
    