import tkinter as tk


# Create a window object
window = tk.Tk()

window.title("My App")
window.geometry("500x200")
window.resizable(width=False, height=False)

container = tk.Frame()

label_username = tk.Label(container, text='username')
entry_username = tk.Entry(container)
btn_login = tk.Button(container, text='login')

label_username.pack()
entry_username.pack()
btn_login.pack()

container.pack()


# Run the event loop
window.mainloop()