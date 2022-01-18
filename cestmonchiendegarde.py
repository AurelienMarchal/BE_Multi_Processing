import subprocess

import paho.mqtt.client as mqtt
import random as rand
import time
import sys

from datetime import datetime

class ChiengDeGarde:
    def __init__(self, ip='127.0.0.255', port=1883):
        self.client = mqtt.Client(client_id="ChiengDeGarde")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(ip, port=port)

        self.port = port
        self.ip = ip

        self.lastPing = datetime.now()

        self.isAlive = False

    def start(self):
        self.client.connect(self.ip, port=self.port)
        self.client.subscribe("/cdg/kill")
        self.client.subscribe("/server0/state")
        self.client.loop_start()

        self.isAlive = True

    # Action lorsque le capteur c'est bien connecté au réseau MQTT
    def on_connect(self, client, userdata, flag, rc):
        print("C'est mon chien connecte !")

    def on_message(self, client, userdata, msg):
        if msg.topic == "/cdg/kill":
            self.isAlive = False
            return

        if msg.topic == "/server0/state":
            self.lastPing = datetime.now()

        return

    def run(self):
        # Envoie d'un nombre aléatoire chaque seconde
        while self.isAlive:
            self.stalker()
            time.sleep(1)

    def stalker(self):
        t = datetime.now()
        d = t - self.lastPing

        if d.total_seconds() >= 3:
            print("Wouf, le server est dead")
            self.client.publish("/server1", "")
        pass


if __name__ == "__main__":
    cdg = ChiengDeGarde()
    cdg.start()
    cdg.run()

    sys.exit()
