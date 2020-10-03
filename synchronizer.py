from queue import Queue

class Syncrhonizer():
    __children = Queue()
    __finalized = False # A flag to not finalize more than once

    def __init__(self, f):
        self.f = f

    def emit(self):
        if not self.__children.qsize == True:
            self.__children.get()
        self.finalize()
    
    def add_dependency(self, **kwargs):
        count = kwargs.get('count', 1)
        for _ in range(0, count):
            self.__children.put(0)

    def get_dependency_count(self):
        return self.__children._qsize()
        
    def finalize(self):
        if (self.__children._qsize() != 0 or self.__finalized):
            return
        else:
            self.__finalized = True
            self.f()

