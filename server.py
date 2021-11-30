import threading
import time
from multiprocessing import Process, Queue

class Server(Process):
    def __init__(self, queue : Queue, nb_values = 10) -> None:
        super().__init__()
        self.queue = queue
        self.nb_values = nb_values
        self.memory = []

    
    def run(self) -> None:
        
        while True :
            
            self.store_in_memory()
            print(self.calc_mean_value())
            print(len(self.memory))
            time.sleep(0.5)
            
    
    def store_in_memory(self):
        if not self.queue.empty():
            self.memory.append(self.queue.get())


    def calc_mean_value(self):
        sum = 0
        for i in range(max(0, len(self.memory) - self.nb_values), len(self.memory)):
            sum += self.memory[i]
        
        return sum/self.nb_values


