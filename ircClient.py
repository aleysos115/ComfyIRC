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
    
    #TODO: Make this accept arbitrary message length and prefix
    def sendCommand(self, cmd, message):
        command = "{} {}\r\n".format(cmd, message)
        self.conn.send(command)

    def joinChannel(self, channel):
        cmd = "JOIN"
        self.channel = channel
        self.sendCommand(cmd, channel)
    
    def sendPrivateMessage(self, channel, message):
        cmd = "PRIVMSG {}".format(self.channel)
        message = ":" + message
        self.sendCommand(cmd, message)

    def sendPart(self, channel, message):
        cmd = "PART {}".format(channel)
        if message != None:
            message = ":" + message
        self.sendCommand(cmd, message)
    

    
        
