import socket
import select
import json
import errno
import sys

from threadpool import ThreadPool

from queue import Queue

conf = json.loads(open('netconf.json').read())


def decorate_message(msg):
    header = f"{len(msg):<{conf['header-length']}}"
    return (header + msg).encode(conf['encoding'])

class Client():
    def __init__(self):
        self.__core = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__core.connect((conf['ip'], conf['port']))
        self.__core.setblocking(False)

    def __send(self, msg):
        self.__core.send(decorate_message(msg))

    def __wait_response(self):
        res = None

        while not res:
            try:
                recv_header = self.__core.recv(conf['header-length'])
                if not len(recv_header):
                    sys.exit()

                recv_length = int(recv_header.decode(conf['encoding']).strip())
                recv = self.__core.recv(recv_length).decode(conf['encoding'])

                res = recv
            except:
                pass
        return res

    def run(self):
        command = input()
        if command:
            self.__send(command)
        res = self.__wait_response()
        print(res)

c = Client()
c.run()
