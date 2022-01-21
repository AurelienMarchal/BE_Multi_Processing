import time
from math import inf

import paho.mqtt.client as mqtt
import numpy as np
import sys

from scipy import rand


class Service:
    def __init__(self, ip="127.0.0.255", port=1883) -> None:
        # MQTT
        self.client = mqtt.Client(client_id="Service")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_msg
        self.client.connect(ip, port=port)

        self.port = port
        self.ip = ip

        self.vote = np.array([None, None, None])
        self.nbVote = 0

        self.isAlive = False

    def start(self):
        self.client.connect(self.ip, port=self.port)
        self.client.subscribe("/service/kill")
        self.client.subscribe(f"/server0/output")
        self.client.subscribe(f"/server1/output")
        self.client.subscribe(f"/server2/output")
        self.client.loop_start()

        self.isAlive = True

    def on_connect(self, client, userdata, flag, rc):
        pass

    def on_msg(self, client, userdata, msg) -> None:
        if msg.topic == f"/service/kill":
            self.isAlive = False
            return

        elif msg.topic == f"/server0/output":
            try:
                self.vote[0] = float(msg.payload)
                self.nbVote += 1
            except:
                pass

        elif msg.topic == f"/server1/output":
            try:
                self.vote[1] = float(msg.payload)
                self.nbVote += 1
            except:
                pass

        elif msg.topic == f"/server2/output":
            try:
                self.vote[2] = float(msg.payload)
                self.nbVote += 1
            except:
                pass

    def run(self) -> None:
        while self.isAlive:
            if self.nbVote >= 2:

                votes = []
                for i in range(3):
                    if self.vote[i] is not None:
                        votes.append(self.vote[i])

                if len(votes) <= 1:
                    continue

                vote = np.argwhere(votes == np.amax(votes))
                self.nbVote = 0

                if len(self.vote) == 1:
                    self.isAlive = False
                else:
                    self.client.publish("/service/output", f"{self.vote[vote[0][0]]}")

                    self.vote = np.array([None, None, None])


            time.sleep(0.5)


if __name__ == "__main__":
    service = Service()
    service.start()
    service.run()

    sys.exit()
