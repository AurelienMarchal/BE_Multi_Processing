from multiprocessing.queues import Queue
import queue
import threading
import time
import random
from multiprocessing import Process, Queue


class Sensor(Process):
    def __init__(self, queue : Queue) -> None:
        super().__init__()
        self.queue = queue

    
    def run(self) -> None:

        while True:
            self.queue.put(random.randint(0, 10))
            #print(self.queue.qsize())
            time.sleep(0.2)