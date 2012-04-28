#! /usr/bin/python
import SocketServer
import json
from subprocess import check_output, CalledProcessError
import os
import shlex
import daemon
import lockfile

PORT = 50007
script_dir = './scripts/'


def execute(commands):

    if len(commands) <= 1:
        return usage()

    command = script_dir + commands[0]
    args = commands[1:]
    args.insert(0, command)

    if os.path.isfile(command):
        try:
            run = shlex.split(combine(args))
            print "Running:"
            print run
            return check_output(run)
        except CalledProcessError as err:
            return err.output

    return usage()


def usage():
    dirList = os.listdir('./scripts')
    cmds = ''
    for cmd in dirList:
        cmds += cmd + ", "
    return "Command not found. Avaliable commands are: " + cmds[:-2]


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


def main():
    HOST = "localhost"

    # Create the server, binding to localhost on port 9999
    server = GoudaBot((HOST, PORT), GoudaHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()


if __name__ == "__main__":
    context = daemon.DaemonContext(
        working_directory=os.getcwd(),
        pidfile=lockfile.FileLock(os.getcwd() + '/lock.pid'),
    )
    with context:
        main()
