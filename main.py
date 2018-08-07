# Copyright Brave Ziazan, Alex Sosin 2018

import sys
import json
from tkinter import *
from ircClient import *

client = IRCClient("username", "server", "port")

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

# Create and configure window
root = Tk()
root.wm_title("ComfyIRC")
root.minsize(width=800, height=600)
root.wm_iconbitmap("resources/icon.ico")

serverName = StringVar()
serverName.set("")
port = StringVar()
port.set("")
username = StringVar()
username.set("")
usernamePref2 = StringVar()
usernamePref2.set("")
usernamePref3 = StringVar()
usernamePref3.set("")

# Top dropdown menus
menubar = Menu(root)
settingsMenu = Menu(menubar, tearoff=0)
themeMenu = Menu(settingsMenu, tearoff=0)
themeMenu.add_command(label="Dark (Default)")
themeMenu.add_command(label="Light")
settingsMenu.add_cascade(label="Theme", menu=themeMenu)
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

# Containing frame for main displays
mainFrame = Frame(height=0, bd=1, relief=RAISED)
mainFrame.pack(fill=BOTH, expand=True, padx=0, pady=0)
mainFrame.configure(background="grey")

# Display list of channels in server
channelList = Listbox(mainFrame)
channelList.pack(side=LEFT, fill=Y, padx=5, pady=5)
channelList.insert(END, "channel")

# Display list of users in channel
userList = Listbox(mainFrame)
userList.pack(side=RIGHT, fill=Y, padx=5, pady=5)
userList.insert(END, "user")

# Chat message entry
messageFrame = Frame(mainFrame, height=0, bd=1, relief=RAISED)
messageFrame.pack(side=BOTTOM, expand=True, fill=X)
messageLable = Label(messageFrame, text="Username")
messageLable.pack(side=LEFT)
messageEntry = Entry(messageFrame)
messageEntry.pack(side=LEFT, expand=True, fill=X)

# Main chat display
display = Text(mainFrame)
display.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)

serverLabel = Label(root, text="Server")
serverLabel.pack(side=LEFT)
serverEntry = Entry(root, textvariable=serverName)
serverEntry.pack(side=LEFT)
portLabel = Label(root, text="Port")
portLabel.pack(side=LEFT)
portEntry = Entry(root, textvariable=port)
portEntry.pack(side=LEFT)
usernameLabel = Label(root, text="Username")
usernameLabel.pack(side=LEFT) 
usernameEntry = Entry(root, textvariable=username)
usernameEntry.pack(side=LEFT)

root.config(menu=menubar)

def applyTheme():
    with open("themes/dark.json", "r") as json_file:
        data = json.load(json_file)

    def applyToEntry(entries):
        for entry in entries:
            entry.configure(background=data["textEntryBackground"], foreground=data["textEntryText"])

    def applyToListbox(lists):
        for l in lists:
            l.configure(background=data["listboxBackground"], foreground=data["listboxText"])

    def applyToMenu(menus):
        for menu in menus:
            menu.configure(background=data["menuBackground"], foreground=data["menuText"])
    
    display.configure(background=data["chatBackground"], foreground=data["chatText"])
    applyToEntry((messageEntry, serverEntry, portEntry, usernameEntry))
    applyToListbox((channelList, userList))
    applyToMenu((menubar, themeMenu, fileMenu))
    

applyTheme()

root.mainloop()

