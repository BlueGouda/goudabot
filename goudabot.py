#! /usr/bin/python
import SocketServer
import json
import argparse

PORT = 50007

USAGE = "This a gouda bot! usage: gouda build OR gouda init name"

def execute(commands):
 
    if len(commands) <= 1:
        return USAGE
    
    dir = commands[0]
    command = commands[1].lower()
    
    if command == "build":
        build(dir)
        return "Project at " + dir + " built!"
    
    elif command == "init" and len(commands) > 2:
        init(commands[2])
        return "Project " + commands[2] + " initiated."
    
    return USAGE

def build(dir):
    print "building " + dir

def init(name):
    print "init " + name

class GoudaHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        result = execute(json.loads(self.data))
        self.request.sendall(result)

class GoudaBot(SocketServer.TCPServer):
    allow_reuse_address = True



if __name__ == "__main__":
    HOST = "localhost"
    # Create the server, binding to localhost on port 9999
    server = GoudaBot((HOST, PORT), GoudaHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()