# Copyright Brave Ziazan 2018

from tkinter import *
import sys

# Called when Connect button is pressed, connects the user to the selected server
def connect(): 
    print("connect")

# Called when Disconnect button is pressed, disconnects user from the current server
def disconnect():
    print("disconnect")

# Called when File --> Quit is pressed, exits the application
def quit():
    print("Quiting...")
    sys.exit()

root = Tk()
root.wm_title("ComfyIRC")
root.minsize(width=800, height=600)
root.wm_iconbitmap("resources/icon.ico")

menubar = Menu(root)
settingsMenu = Menu(menubar, tearoff=0)
settingsMenu.add_command(label="Theme")
fileMenu = Menu(menubar, tearoff=0)
fileMenu.add_command(label="Quit", command=quit)
menubar.add_cascade(label="File", menu=fileMenu)
menubar.add_cascade(label="Settings", menu=settingsMenu)

topFrame = Frame(height=0, bd=1, relief=SUNKEN)
topFrame.pack(fill=X, padx=0, pady=0)
#topFrame.configure(background="black")
connectButton = Button(topFrame, text="Connect", command=connect)
connectButton.pack(side=LEFT)
disconnectButton = Button(topFrame, text="Disconnect", command=disconnect)
disconnectButton.pack(side=LEFT)

mainFrame = Frame(height=0, bd=1, relief=RAISED)
mainFrame.pack(fill=BOTH, expand=True, padx=0, pady=0)
mainFrame.configure(background="grey")

channelList = Listbox(mainFrame)
channelList.pack(side=LEFT, fill=Y, padx=5, pady=5)
channelList.insert(END, "channel")

userList = Listbox(mainFrame)
userList.pack(side=RIGHT, fill=Y, padx=5, pady=5)
userList.insert(END, "user")

messageFrame = Frame(mainFrame, height=0, bd=1, relief=RAISED)
messageFrame.pack(side=BOTTOM, expand=True, fill=X)
messageLable = Label(messageFrame, text="Username")
messageLable.pack(side=LEFT)
messageEntry = Entry(messageFrame)
messageEntry.pack(side=LEFT, expand=True, fill=X)

display = Text(mainFrame)
display.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)

root.config(menu=menubar)

root.mainloop()