import time
import random as rand
import paho.mqtt.client as mqtt
import numpy as np
import sys
from scipy import rand


class Affichage:
    def __init__(self, ip="127.0.0.255", port=1883) -> None:
        # MQTT
        self.client = mqtt.Client(client_id="Affichage")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_msg
        self.client.connect(ip, port=port)

        self.port = port
        self.ip = ip

        self.value = None

        self.isAlive = False

    def start(self):
        self.client.connect(self.ip, port=self.port)
        self.client.subscribe("/service/output")
        self.client.subscribe("/affichage/kill")
        self.client.loop_start()

        self.isAlive = True

    def on_connect(self, client, userdata, flag, rc):
        pass

    def on_msg(self, client, userdata, msg) -> None:
        if msg.topic == "/affichage/kill":
            self.isAlive = False
            return

        if msg.topic == "/service/output":
            self.value = float(msg.payload.decode("utf-8"))

    def run(self) -> None:
        while self.isAlive:
            print(self.value)
            time.sleep(0.5)


if __name__ == "__main__":
    affichage = Affichage()
    affichage.start()
    affichage.run()
    sys.exit()
