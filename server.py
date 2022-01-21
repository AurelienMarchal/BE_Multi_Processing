import time
import random as rand
import paho.mqtt.client as mqtt
import numpy as np
import sys
from scipy import rand


class Server:
    def __init__(self, id, restart=False, ip="127.0.0.255", port=1883) -> None:
        self.RAM = np.array([])  # Memoire vive du server

        # MQTT
        self.client = mqtt.Client(client_id=f"Server {id}")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_msg
        self.client.connect(ip, port=port)

        self.mode = restart  # 0 : Mode PRIMARY / 1 : Mode BACKUP

        self.port = port
        self.ip = ip

        self.id = id

        self.isAlive = False

    def start(self):
        self.client.connect(self.ip, port=self.port)
        self.client.subscribe(f"/server{self.id}/kill")
        self.client.subscribe("/sensor/msg")
        self.client.subscribe(f"/server{self.id}/getBackup")
        self.client.loop_start()

        self.isAlive = True

    def on_connect(self, client, userdata, flag, rc):
        pass

    def on_msg(self, client, userdata, msg) -> None:
        if msg.topic == "/server"+str(self.id)+"/kill":
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
        if msg.topic == "/server"+str(self.id)+"/getBackup":
            try:
                value = float(msg.payload.decode("utf-8"))
                self.RAM = np.append(self.RAM, value)

                if len(self.RAM) >= 10:
                    self.RAM = np.delete(self.RAM, 0)
            except:
                pass

            self.mode = 0

    def getBackup(self):
        self.client.publish("/dataBase/getBackup", self.id)

    def run(self) -> None:
        while self.isAlive:
            # Watchdog
            self.coupDePiedAuChienDeGarde()

            if self.mode:
                # Mode BACKUP
                self.getBackup()
            else:
                # Lecture du capteur
                # Fait de maniere implicite (stocké dans la RAM)
                # Calcul
                value = self.calc_mean_value()
                # Affichage
                self.client.publish(f"/server{self.id}/output", value)
                # Stockage


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

    def valueError(self, value) -> float:
        x = rand.uniform(1, 100)

        if x <= 5:
            value = value + rand.uniform(-1, 1)

        return value

    def coupDePiedAuChienDeGarde(self):
        self.client.publish(f"/server{self.id}/state", "I'm alive")


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[2] == "restart":
        server = Server(id=int(sys.argv[1]), restart=True)
        server.start()
        server.run()
    elif len(sys.argv) == 2:
        server = Server(id=int(sys.argv[1]))
        server.start()
        server.run()
    else:
        print("Usage : python3 server.py <id> [restart]")
    sys.exit()
