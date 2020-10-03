import threading
from queue import Queue

class PoolQueue(Queue):
    finished = False

    def __init__(self):
        super(PoolQueue, self).__init__()


class Worker(threading.Thread):
    def __init__(self, queue):
        super(Worker, self).__init__()
        self.queue = queue
        self.start()

    def run(self):
        while not self.queue.finished:
            if (self.queue.empty()): continue
            task = self.queue.get(True)
            f = task['f']
            args = task['args']
            kwargs = task['kwargs']
            res = f(*args, **kwargs)
            task['ret']()



class ThreadPool():
    threads = []
    queue = PoolQueue()

    def __init__(self, threads_number):
        for _ in range(0, threads_number):
            self.threads.append(Worker(self.queue))

    def add_task(self, f, *args, **kwargs):
        self.queue.put({
            'f': f,
            'args': args[0],
            'kwargs': {},
            'ret': kwargs['ret']
        }, True);


