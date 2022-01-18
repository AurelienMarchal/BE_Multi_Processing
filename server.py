import threading
import time
import paho.mqtt.client as mqtt
from multiprocessing import Process
import numpy as np
import sys

from scipy import rand


class Server(Process):
    def __init__(self, mode=0, ip="127.0.0.1", port=1883) -> None:
        self.RAM = np.array([])  # Memoire vive du server

        # MQTT
        self.client = mqtt.Client(client_id=f"Server {mode}")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_msg
        self.client.connect(ip, port=port)

        self.mode = mode  # 0 : Mode PRIMAIRE / 1 : Mode SECONDAIRE

        self.port = port
        self.ip = ip

        self.isAlive = False

    def start(self):
        self.client.connect(self.ip, port=self.port)
        self.client.subscribe(f"/server{self.mode}/kill")
        self.client.subscribe("/sensor/msg")
        self.client.subscribe(f"/server{self.mode}")
        self.client.loop_start()

        self.isAlive = True

    def on_connect(self, client, userdata, flag, rc):
        pass

    def on_msg(self, client, userdata, msg) -> None:
        if msg.topic == f"/server{self.mode}/kill":
            self.isAlive = False
            return
        if msg.topic == "/sensor/msg":  # on reçoit un message du sensor -> on le stock dans la mémoire vive
            try:
                value = float(msg.payload.decode("utf-8"))
                self.RAM = np.append(self.RAM, value)

                if len(self.RAM) >= 10:
                    self.RAM = np.delete(self.RAM, 0)
            except:
                pass
        if msg.topic == f"/server{self.mode}":
            self.mode = 0

    def run(self) -> None:

        while self.isAlive:
            # WATCHDOG
            self.coupDePiedAuChienDeGarde()

            # LECTURE DU CAPTEUR
            # Fait de maniere implicite (stocké dans la RAM)
            # Calcul
            value = self.calc_mean_value()

            # AFFICHAGE
            # print(f"{value}")

            if self.mode == 0:  # Mode Primaire
                self.client.publish("/server0/output", value)

            # STOCKAGE DANS LA MEMOIRE VIVE
            # print(f'Taille de la mémoire : {len(self.memory)}')

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
        if len(self.RAM) == 0:
            return 0.0
        return np.mean(self.RAM)

    def simulationCrash(self):
        x = rand.uniform(1, 100)

        if x <= 1:
            self.isAlive = False
            sys.exit()

    def coupDePiedAuChienDeGarde(self):
        self.client.publish(f"/server{self.mode}/state", "I'm alive")

        pass


if __name__ == "__main__":
    if len(sys.argv) == 2:
        server = Server(mode=int(sys.argv[1]))
        server.start()
        server.run()

    sys.exit()
