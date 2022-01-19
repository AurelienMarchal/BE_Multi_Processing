import threading
import time
import paho.mqtt.client as mqtt
from multiprocessing import Process, Queue
import numpy as np
import sys

from scipy import rand


class Server(Process):
    def __init__(self, restart=False, ip="127.0.0.1", port=1883) -> None:
        self.RAM = np.array([])  # Memoire vive du server

        # MQTT
        self.client = mqtt.Client(client_id="Server")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_msg
        self.client.connect(ip, port=port)

        if restart:
            # On va récup les valeurs dans la backup
            self.getBackup()

        self.mode = 0  # 0 : Mode PRIMARY / 1 : Mode BACKUP

        self.port = port
        self.ip = ip

        self.isAlive = False

    def start(self):
        self.client.connect(self.ip, port=self.port)
        self.client.subscribe("/server/kill")
        self.client.subscribe("/sensor/msg")
        self.client.subscribe("/server/getBackup")
        self.client.loop_start()

        self.isAlive = True

    def on_connect(self, client, userdata, flag, rc):
        pass

    def on_msg(self, client, userdata, msg) -> None:
        if msg.topic == "/server/kill":
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
        if msg.topic == "/server/getBackup":
            try:
                value = float(msg.payload.decode("utf-8"))
                self.RAM = np.append(self.RAM, value)

                if len(self.RAM) >= 10:
                    self.RAM = np.delete(self.RAM, 0)
            except:
                pass

    def getBackup(self):
        self.client.publish("/dataBase/getBackup", "True")

    def run(self) -> None:
        while self.isAlive:
            if self.mode == 0:  # Mode PRIMARY
                # Watchdog
                self.coupDePiedAuChienDeGarde()

                # Lecture du capteur
                # Fait de maniere implicite (stocké dans la RAM)
                # Calcul 
                value = self.calc_mean_value()
                # Affichage
                # print(f"{value}")
                self.client.publish("/server/output", value)
                # Stockage

                # print(f'Taille de la mémoire : {len(self.memory)}')

            else:  # Mode BACKUP
                pass

            time.sleep(0.5)

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
        self.client.publish("/server/state", "I'm alive")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "restart":
        server = Server(restart=True)
    else:
        server = Server()
    server.start()
    server.run()

    sys.exit()
