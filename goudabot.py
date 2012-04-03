#! /usr/bin/python
import SocketServer
import json
from subprocess import check_output, CalledProcessError
from os import path
import shlex

PORT = 50007

USAGE = "This a gouda bot! usage: gouda script [arg ...]"
script_dir = './scripts/'


def execute(commands):
 
    if len(commands) <= 1:
        return USAGE
    
    command = script_dir + commands[0]
    args = commands[1:]
    args.insert(0, command)

    if path.isfile(command):
        try:
            return check_output(shlex.split(combine(args)))
        except CalledProcessError as err: 
            return err.output

    return USAGE

def combine(lis):
    result = ''
    for i in lis:
        result += str(i) + " "
    return result[:-1]

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