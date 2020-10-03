from queue import Queue
import time

class Syncrhonizer():
    children = Queue()

    def __init__(self, f):
        self.f = f

    def emit(self):
        # print('trying')
        self.children.get()
        self.finalize()
        
    def finalize(self):
        print(self.f)
        if (self.children.not_empty):
            return
        self.f()

