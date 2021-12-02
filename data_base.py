from multiprocessing import Process, Queue
import os
import time

class DataBase(Process):
    COUNT = 0
    def __init__(self, queue : Queue, max_size = 10000) -> None:
        super().__init__()
        self.queue = queue
        self.max_size = max_size
        
        self.folder = f'./Memory/{self.COUNT}_server_storage'
        self.file_path = self.folder + '/data.txt'
        
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
            os.mkdir(self.folder)
        with open(self.file_path, mode='w') as f:
            f.write("-- IL S'AGIT DU FICHER DANS LEQUEL LES DONNES SONT STOCKEES --\n")
        f.close()
        self.COUNT += 1

    
    def run(self) -> None:
        while True:
            #print(f'Taille queue data_base : {self.queue.qsize()}')
            self.store_in_memory()
            time.sleep(0.1)



    
    def store_in_memory(self):

        if not self.queue.empty():
            value = self.queue.get()

            with open(self.file_path, mode='a') as f:
                f.write(f'{value}\n')
            f.close()




