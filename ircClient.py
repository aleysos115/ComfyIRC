# Copyright Brave Ziazan, Alex Sosin 2018

import socket
import sys
import threading

encodeType = "UTF-8"

class IRCClient:

    # Init from UI
    def __init__(self, username, server, port):
        self.username = username
        self.server = server
        self.port = int(port)
        self.channel = None

    # Connects to server specified by the request
    def connect(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.server, self.port))

    # Returns server response
    def getResponse(self):
        try:
            return self.conn.recv(512)
        except ConnectionAbortedError:
            raise ConnectionAbortedError
        
    
    # Generic send command function 
    #TODO: Make this accept arbitrary message length and prefix
    def sendCommand(self, cmd, message):
        if message != None:
            command = ("{} {}\r\n".format(cmd, message)).encode(encoding=encodeType)
        else:
            command = ("{}\r\n".format(cmd)).encode(encoding=encodeType)
        print(command)
        self.conn.send(command)

    # Request join message - JOIN <channels> [<keys>]
    def joinChannel(self, channel):
        cmd = "JOIN"
        self.channel = channel
        self.sendCommand(cmd, channel)
    
    # Send private message to target - PRIVMSG <msgtarget> <message>
    def sendPrivateMessage(self, channel, message):
        cmd = "PRIVMSG {}".format(self.channel)
        message = ":" + message
        self.sendCommand(cmd, message)

    # Sends PART message - PART <channels> [<message>]
    def sendPart(self, channel, message):
        cmd = "PART {}".format(channel)
        if message != None:
            message = ":" + message
        self.channel = None
        self.sendCommand(cmd, message)
    
    # Sends NICK message - NICK <nickname>
    def sendNick(self, message):
        cmd = "NICK"
        self.sendCommand(cmd, message)
    
    # Sends QUIT message - QUIT [<message>]
    def sendQuit(self, message):
        cmd = "QUIT"
        if message != None:
            message = ":" + message
        self.sendCommand(cmd, message)
        self.conn.close()

    # Prints all responses from server, Should be called in thread
    def printResponse(self):
        resp = self.getResponse()
        msg = resp.decode(encoding=encodeType)
        #print(msg)
        if resp:
            msg = msg.strip().split(":")
            print("\n< {}> {}".format(msg[1].split("!")[0], msg[2].strip()))
    
    #returns stripped and cleaned version of server response as string
    def returnResponse(self):
        try:
            resp = self.getResponse()
        except ConnectionAbortedError:
            raise ConnectionAbortedError
        
        response = resp.decode(encoding=encodeType)
        char_list = [response[j] for j in range(len(response)) if ord(response[j]) in range(65536)]
        response = ''
        for j in char_list:
            response = response + j
        return response
    
    #sends pong message back to server
    def sendPong(self, msg):
        self.sendCommand("PONG", ":" + msg.split(":")[1])

#Initial ping/pong handling 
def ServerRequest(client):
    joined = False
    while(joined == False):
        resp = client.returnResponse()
        print(resp.strip())

        if "PING" in resp:
            joined = True
            client.sendPong(resp)
