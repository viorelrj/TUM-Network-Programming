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

class Server():
    __core = None
    __sockets = []
    __server_socket = None
    __clients = {}
    __responses = Queue()
    __requests = Queue()

    def __init__(self, react):
        self.__core = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__core.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__core.bind((conf['ip'], conf['port']))
        self.__core.listen()
        self.__sockets = [self.__core]
        self.react = react
        print('Up and running')

    def __receive_message(self, sock, q):
        try:
            message_header = sock.recv(conf['header-length'])
            if not len(message_header):
                return False
            message_length = int(message_header.decode(conf['encoding']).strip())
            q.put({
                'sock': sock,
                'data': sock.recv(message_length).decode(conf['encoding'])
            })
        except:
            return False

    def __send_message (self, sock, msg):
        sock.send(decorate_message(msg))
    
    def __listen(self, q):
        while True:
            read_sockets, _, __ = select.select(self.__sockets, [], self.__sockets)
            for notified_socket in read_sockets:
                if notified_socket == self.__core:
                    client_socket, client_address = self.__core.accept()
                    self.__receive_message(client_socket, q)

    def __execute(self, f, src, dest):
        while True:
            if self.__requests.qsize():
                print('yeah, found a request')
                req = src.get()
                res = f(req)
                dest.put(res)

    def __respond(self, src):
        while True:
            if src.qsize():
                print('responding to client')
                package = src.get()
                self.__send_message(package['sock'], package['data'])

    def run(self):
        pool = ThreadPool(3)
        pool.add_task(self.__listen, [self.__requests])
        pool.add_task(self.__respond, [self.__responses])
        pool.add_task(self.__execute, [self.react, self.__requests, self.__responses])




