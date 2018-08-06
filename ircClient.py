import socket
import sys
import threading

class IRCClient:

    #init from UI
    def __init__(self, username, server, port):
        self.username = username
        self.server = server
        self.port = port

    #Connects to server specified by the request
    def connect(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.server, self.port))

    #returns server response
    def getResponse(self):
        return self.conn.recv(512)
    
    #Generic send command function 
    #TODO: Make this accept arbitrary message length and prefix
    def sendCommand(self, cmd, message):
        command = "{} {}\r\n".format(cmd, message)
        self.conn.send(command)

    #Request join message - JOIN <channels> [<keys>]
    def joinChannel(self, channel):
        cmd = "JOIN"
        self.channel = channel
        self.sendCommand(cmd, channel)
    
    #Send private message to target - PRIVMSG <msgtarget> <message>
    def sendPrivateMessage(self, channel, message):
        cmd = "PRIVMSG {}".format(self.channel)
        message = ":" + message
        self.sendCommand(cmd, message)

    #Sends PART message - PART <channels> [<message>]
    def sendPart(self, channel, message):
        cmd = "PART {}".format(channel)
        if message != None:
            message = ":" + message
        self.sendCommand(cmd, message)
    
    #Sends NICK message - NICK <nickname>
    def sendNick(self, message):
        cmd = "NICK"
        self.sendCommand(cmd, message)
    
    #Sends QUIT message - QUIT [<message>]
    def sendQuit(self, message):
        cmd = "QUIT"
        if message != None:
            message = ":" + message
        self.sendCommand(cmd, message)

    
        
