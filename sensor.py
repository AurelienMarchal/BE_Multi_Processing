import paho.mqtt.client as mqtt
import random as rand
import time
import sys


class Sensor:
    def __init__(self, ip='127.0.0.255', port=1883):
        self.client = mqtt.Client(client_id="Sensor")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(ip, port=port)

        self.port = port
        self.ip = ip

        self.isAlive = False

    def start(self):
        self.client.connect(self.ip, port=self.port)
        self.client.subscribe("/sensor/kill")
        self.client.loop_start()

        self.isAlive = True

    # Envoie un nombre aléatoire sur le réseau MQTT
    def send_rand(self):
        x = rand.uniform(-1, 50)
        self.client.publish("/sensor/msg", x)

    # Action lorsque le capteur c'est bien connecté au réseau MQTT
    def on_connect(self, client, userdata, flag, rc):
        print("Sensor connecte !")

    def on_message(self, client, userdata, msg):
        if msg.topic == "/sensor/kill":
            self.isAlive = False
            return

        return

    def run(self):
        # Envoie d'un nombre aléatoire chaque seconde
        while self.isAlive:
            self.send_rand()
            time.sleep(1)


if __name__ == "__main__":
    sensor = Sensor()
    sensor.start()
    sensor.run()

    sys.exit()
