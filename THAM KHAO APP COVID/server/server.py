import tkinter as tk
from tkinter import *
from tkinter import messagebox
import threading    
import serverRef#file local

def runServerGUI():
    serverRef.runServer()

def readData():
    serverRef.getAPIdata()

t1 = threading.Thread(target=runServerGUI)
t2 = threading.Thread(target=readData)

t1.start()
t2.start()
  
t1.join()
t2.join()

print("Done!")    
    