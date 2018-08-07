# Copyright Brave Ziazan, Alex Sosin 2018

import sys
import json
from tkinter import *
from ircClient import *
import threading

client = None
# Called when Connect button is pressed, connects the user to the selected server
def connect(): 
    print("connect")
    global client
    client = IRCClient(username.get(), serverName.get(), port.get())
    client.connect()
    client.sendCommand("PASS", "none")
    client.sendNick(client.username)
    client.sendCommand("USER", "test 0 * :test")
    ServerRequest(client)
    '''
    t = threading.Thread(target=client.TprintResponse)
    t.start()
    '''

# Called when Disconnect button is pressed, disconnects user from the current server
def disconnect():
    print("disconnect")
    client.sendQuit("")

# Called when File --> Quit is pressed, exits the application
def quit():
    print("Quiting...")
    sys.exit()

# Create and configure window
root = Tk()
root.wm_title("ComfyIRC")
root.minsize(width=800, height=600)
root.wm_iconbitmap("resources/icon.ico")
root.wm_attributes("-transparentcolor", "magenta")

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

topFrame = Frame(height=0, bd=1)
topFrame.pack(fill=X, padx=0, pady=0)
#topFrame.configure(background="black")
connectButton = Button(topFrame, text="Connect", command=connect)
connectButton.pack(side=LEFT)
disconnectButton = Button(topFrame, text="Disconnect", command=disconnect)
disconnectButton.pack(side=LEFT)

# Containing frame for main displays
mainFrame = Frame(height=0, bd=1)
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

# Main chat display
chatFrame = Frame(mainFrame)
chatFrame.pack(side=TOP, expand=True, fill=BOTH)
display = Text(chatFrame)
display.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)

# Chat message entry
messageFrame = Frame(chatFrame, height=0, bd=0)
messageFrame.pack(side=TOP, fill=X)
messageLabel = Label(messageFrame, text="Username")
messageLabel.pack(side=LEFT)
messageEntry = Entry(messageFrame)
messageEntry.pack(side=LEFT, expand=True, fill=X, pady=10)

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
            entry.configure(background=data["textEntryBackground"], foreground=data["textEntryText"], insertbackground=data["textEntryText"], relief=FLAT)

    def applyToListbox(lists):
        for l in lists:
            l.configure(background=data["listboxBackground"], foreground=data["listboxText"], borderwidth=0, selectborderwidth=0, relief=FLAT)

    def applyToMenu(menus):
        for menu in menus:
            menu.configure(background=data["menuBackground"], foreground=data["menuText"], relief=FLAT, activeborderwidth=0, borderwidth=0)

    def applyToFrame(frames):
        for frame in frames:
            frame.configure(background=data["frameBackground"], relief=FLAT)

    def applyToLabel(labels):
        for label in labels:
            label.configure(background=data["labelBackground"], foreground=data["labelForeground"])

    def applyToButton(buttons):
        for button in buttons:
            button.configure(background=data["buttonBackground"], foreground=data["buttonText"], relief=FLAT)
    
    display.configure(background=data["chatBackground"], foreground=data["chatText"])
    root.configure(background=data["rootBackground"])
    applyToEntry((messageEntry, serverEntry, portEntry, usernameEntry))
    applyToListbox((channelList, userList))
    #applyToMenu((menubar, themeMenu, fileMenu, settingsMenu))
    applyToFrame((mainFrame, topFrame, chatFrame, messageFrame))
    applyToLabel((messageLabel, usernameLabel, portLabel, serverLabel))
    applyToButton((connectButton, disconnectButton))
    
applyTheme()

root.mainloop()

