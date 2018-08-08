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

    def TprintResponse(self):
        while True:
            self.printResponse()
    
    def sendPong(self, msg):
        self.sendCommand("PONG", ":" + msg.split(":")[1])

def ServerRequest(client):
    cmd = ""
    joined = False
    while(joined == False):
        resp = client.getResponse()
        msg = resp.decode(encoding=encodeType)
        print(msg.strip())
        
        '''
        if "376" in resp:
            client.joinChannel(channel)
        '''

        if "PING" in msg:
            joined = True
            print("Test")
            client.sendCommand("PONG", ":" + msg.split(":")[1])

        if "366" in msg:
            joined = True
            t = threading.Thread(target=client.printResponse)
            t.start()
    '''
    try:
        while(cmd != "/quit"):
            #Get input here
            if cmd == "/quit":
                client.sendQuit()
                quit()
            if cmd and len(cmd) > 0:
                client.sendPrivateMessage(channel, cmd)
    except KeyboardInterrupt:
        client.sendQuit()
        quit()
        t = threading.Thread(target=client.printResponse)
        t.start()
    '''
