import threading
from queue import Queue
from synchronizer import Syncrhonizer

class PoolQueue(Queue):
    finished = False

    def __init__(self):
        super(PoolQueue, self).__init__()


class Worker(threading.Thread):
    def __init__(self, queue, index):
        super(Worker, self).__init__()
        self.queue = queue
        self.start()
        self.index = index

    def run(self):
        while not self.queue.finished:
            if (self.queue.qsize() == 0): continue
            task = self.queue.get(True)
            f = task['f']
            args = task['args']
            kwargs = task['kwargs']
            f(*args, **kwargs)
            task['callback']()



class ThreadPool():
    threads = []
    __queue = PoolQueue()


    def __init__(self, threads_number):
        for index in range(threads_number):
            worker = Worker(self.__queue, index)
            self.threads.append(worker)

    def add_task(self, f, args, **kwargs):
        callback = kwargs.get('callback', lambda: None)
        self.__queue.put({
            'f': f,
            'args': args,
            'kwargs': {},
            'callback': callback
        }, True)

    def close(self):
        self.__queue.finished = True
