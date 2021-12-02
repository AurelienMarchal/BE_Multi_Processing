import paho.mqtt.client as mqtt
import random as rand
import time

class Sensor:
    def __init__(self, ip='127.0.0.255', port=1883):
        self.client = mqtt.Client(client_id="Sensor")
        self.client.on_connect = self.on_connect
        self.client.connect(ip, port=port)
        self.client.loop_start()

    # Envoie un nombre aléatoire sur le réseau MQTT
    def send_rand(self):
        x = rand.uniform(-1,50)
        self.client.publish("/sensor", x)

    # Action lorsque le capteur c'est bien connecté au réseau MQTT
    def on_connect(self, client, userdata, flag, rc):
        print("Sensor connecte !")

    def run(self):
        # Envoie d'un nombre aléatoire chaque seconde
        while(True) :
            self.send_rand()
            time.sleep(1)