import threading
import time
from multiprocessing import Process, Queue

class Server(Process):
    def __init__(self, queue_sensor : Queue, queue_data_base : Queue , nb_values = 10) -> None:
        super().__init__()
        self.queue_sensor = queue_sensor
        self.queue_data_base = queue_data_base
        self.nb_values = nb_values
        self.memory = []

    
    def run(self) -> None:
        
        while True :
            
            self.store_in_memory()
            print(self.calc_mean_value())
            #print(f'Taille de la mémoire : {len(self.memory)}')
            time.sleep(0.5)
            
    
    def store_in_memory(self):
        if not self.queue_sensor.empty():
            value = self.queue_sensor.get()
            self.memory.append(value)
            if len(self.memory) > self.nb_values:
                self.memory.pop(0)
            self.send_value_to_data_base(value)

    def send_value_to_data_base(self, value):
        self.queue_data_base.put(value)
        

    def calc_mean_value(self):
        sum = 0
        for i in range(max(0, len(self.memory) - self.nb_values), len(self.memory)):
            sum += self.memory[i]
        
        return sum/self.nb_values


