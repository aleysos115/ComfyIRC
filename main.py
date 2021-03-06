# Copyright Brave Ziazan, Alex Sosin 2018

import sys
import json
from tkinter import *
from ircClient import *
import threading
import tkinter.scrolledtext as st
import time

client = None

#center thread loop for message recvieve 
def TreturnResponse():
    response322 = ""
    while True:
        try:
            response = client.returnResponse()
        except ConnectionAbortedError:
            break
        if "PING" in response:
            client.sendPong(response)
        if "322" in response:
            response322 = response322 + response
            if "323" in response322:
                populateChannels(response322)
                response322 = ""
        elif "353" in response:
            populateUsers(response)
            print(response)

        else:
            populateDisplay(response)

def TretrieveInfo():
    while True:
        client.sendCommand("LIST", None)
        if(client.channel != None):
            time.sleep(2)
            client.sendCommand("NAMES", client.channel)
        time.sleep(10)

#populates center display
def populateDisplay(response):
    display.insert(END, response)
    display.see(END)
    return response

#populates Channel list
def populateChannels(response):
    channelList.delete(0, END)
    channelList.insert(END, "CHANNELS")
    Lresp = response.splitlines()
    for line in Lresp:
        if "322" in line:
            hashIndex = line.find('#')
            colonIndex = line.find(':', hashIndex)
            channelList.insert(END, line[hashIndex:colonIndex])

def populateUsers(response):
    response = response.splitlines()
    response = response[0]
    userList.delete(0, END)
    userList.insert(END, "USERS")

    users = response[response.find(":", 1) + 1:]
    users = users.split(' ')
    for user in users:
        userList.insert(END, user)

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

    t = threading.Thread(target=TreturnResponse)
    t.start()
    
    tInfoThread = threading.Thread(target=TretrieveInfo)
    tInfoThread.start()

# Called when Disconnect button is pressed, disconnects user from the current server
def disconnect():
    print("disconnect")
    client.sendQuit(None)

# Called when Join button is pressed, has user join the selected channel
def join():
    print("join")

# Called when Leave button is pressed, has user leave the selected channel
def leave():
    client.sendPart(client.channel, None)
    print("leave")

# Sends the message entered into the message entry, and clears the message entry
def send():
    print("send")
    msg = message.get()
    if msg[0] == '/':
        print("Send")
        spaceIndex = msg.find(" ")
        cmd = msg[1:spaceIndex]
        if spaceIndex != -1:
            param = msg[spaceIndex + 1:]
        else:
            param = None
        if cmd == "JOIN":
            client.joinChannel(param)
        else:
            client.sendCommand(cmd, param)
        #Handle command
    elif client.channel != None:
        populateDisplay("<{}> {}\r\n".format(client.username, msg))
        client.sendPrivateMessage(client.channel, msg)
    else:
        display.insert(END, "Please join a channel before sending a message through /JOIN <channelName>")

    message.set("")

# This is called when Return key is pressed and the message entry has focus, exists because the callback for a button press doesn't require an event arg, but a keybind does
def _send(event):
    send()

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

message = StringVar()
message.set("")

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

# Top frame
topFrame = Frame(height=0, bd=1)
topFrame.pack(fill=X, padx=0, pady=0)
#topFrame.configure(background="black")
connectButton = Button(topFrame, text="Connect", command=connect)
connectButton.pack(side=LEFT)
disconnectButton = Button(topFrame, text="Disconnect", command=disconnect)
disconnectButton.pack(side=LEFT)
joinButton = Button(topFrame, text="Join", command=join)
joinButton.pack(side=LEFT)
leaveButton = Button(topFrame, text="Leave", command=leave)
leaveButton.pack(side=LEFT, expand=False)

serverSelectorFrame = Frame(topFrame, height=0, bd=1)
serverSelectorFrame.pack(side=LEFT, fill=X, expand=True)
var = StringVar()
serverSelector = OptionMenu(serverSelectorFrame, var, "one", "two", "three")
serverSelector.pack(side=LEFT, fill=X, expand=True)
addServerButton = Button(serverSelectorFrame, text="+")
addServerButton.pack(side=LEFT)

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
display = st.ScrolledText(chatFrame)
display.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)

# Chat message entry
messageFrame = Frame(chatFrame, height=0, bd=0)
messageFrame.pack(side=TOP, fill=X)
messageLabel = Label(messageFrame, text="Username")
messageLabel.pack(side=LEFT)
messageEntry = Entry(messageFrame, textvariable=message)
messageEntry.pack(side=LEFT, expand=True, fill=X, pady=10)
sendButton = Button(messageFrame, text="Send", command=send)
sendButton.pack(side=LEFT)
messageEntry.bind("<Return>", _send)

# Entries for server connection information
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
            button.configure(background=data["buttonBackground"], foreground=data["buttonText"], relief=FLAT, activebackground="#333333", activeforeground="white", padx=5)
    
    display.configure(background=data["chatBackground"], foreground=data["chatText"])
    root.configure(background=data["rootBackground"])
    serverSelectorFrame.configure(padx=10, pady=5)
    serverSelector.configure(background="#161616", foreground="#ffffff", borderwidth=0, relief=FLAT, padx=10, highlightthickness=0)

    applyToEntry((messageEntry, serverEntry, portEntry, usernameEntry))
    applyToListbox((channelList, userList))
    #applyToMenu((menubar, themeMenu, fileMenu, settingsMenu))
    applyToFrame((mainFrame, topFrame, serverSelectorFrame, chatFrame, messageFrame))
    applyToLabel((messageLabel, usernameLabel, portLabel, serverLabel))
    applyToButton((connectButton, disconnectButton, joinButton, leaveButton, addServerButton, sendButton))
    
applyTheme()

# Preferences window
prefWindow = Toplevel()
prefWindow.title("Preferences")
prefWindowWidth = 600
prefWindowHeight = 450
prefWindow.minsize(width=prefWindowWidth, height=prefWindowHeight)
prefWindow.maxsize(width=prefWindowWidth, height=prefWindowHeight)
prefWindow.withdraw()

root.mainloop()

