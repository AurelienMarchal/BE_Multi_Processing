from multiprocessing import Process, Queue
import paho.mqtt.client as mqtt
import os
import time
import sys


class DataBase(Process):

    COUNT = 0

    def __init__(self, ip='127.0.0.255', port=1883):
        super().__init__()

        self.queue = Queue()
        self.isAlive = False

        self.client = mqtt.Client(client_id="DataBase")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(ip, port=port)

        self.folder = f'./Memory/{self.COUNT}_server_storage'
        self.file_path = self.folder + '/data.txt'

        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
            os.mkdir(self.folder)
        with open(self.file_path, mode='w') as f:
            f.write("-- IL S'AGIT DU FICHER DANS LEQUEL LES DONNES SONT STOCKEES --\n")
        f.close()
        self.COUNT += 1

        self.port = port
        self.ip = ip

    def start(self):
        self.client.connect(self.ip, port=self.port)
        self.client.subscribe("/server0/output")
        self.client.subscribe("/dataBase/kill")
        self.client.loop_start()
        self.isAlive = True

    def run(self) -> None:
        while self.isAlive:

            time.sleep(0.1)

    def on_connect(self, client, userdata, flag, rc):
        print("DataBase connecte !")

    def on_message(self, client, userdata, msg):
        if msg.topic == "/dataBase/kill":
            self.isAlive = False
            return

        if msg.topic == "/server0/output":
            value = float(msg.payload.decode("utf-8"))
            self.store_in_memory(value)
        return

    def store_in_memory(self, value):
        with open(self.file_path, mode='a') as f:
            f.write(f'{value}\n')
        f.close()


if __name__ == "__main__":
    dataBase = DataBase()
    dataBase.start()
    dataBase.run()

    sys.exit()
