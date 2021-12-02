import threading
import time
import paho.mqtt.client as mqtt
from multiprocessing import Process, Queue
import data_base
import numpy as np

class Server(Process):
    def __init__(self, ip="127.0.0.1", port=1883) -> None:
        self.RAM = np.array([]) # Memoire vive du server
        
        # MQTT
        self.client = mqtt.Client(client_id="Server")
        self.client.on.connect = self.on_connect
        self.client.on.message = self.on_msg
        self.client.connect(ip, port=port)
        self.client.subscribe("/sensor")
        self.client.loop_start()

        self.mode = 0 # 0 : Mode PRIMARY / 1 : Mode BACKUP

    def on_connect(self, client, userdata, flag, rc):
        pass

    def on_msg(self, client, userdata, msg) -> None :
        if msg.topic == "/sensor": # on reçoit un message du sensor -> on le stock dans la mémoire vive
            try:
                self.RAM.append(float(msg.payload.decode("utf-8")))
                if (len(self.RAM) >= 10):
                    self.AM = np.delete(self.RAM, 0)
            except:
                pass
    
    def run(self) -> None:
        
        while True :
            if (self.mode == 0): # Mode PRIMARY           
                # Watchdog
                self.coupDePiedAuChienDeGarde()
                # Lecture du capteur
                    # Fait de maniere implicite (stocké dans la RAM)
                # Calcul 
                value = self.calc_mean_value()
                # Affichage
                print(f"{value}")
                # Stockage
                
                
                #print(f'Taille de la mémoire : {len(self.memory)}')

            else : # Mode BACKUP
                pass

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
        return np.mean(self.RAM)

    def coupDePiedAuChienDeGarde(self):
        # ToDo Gestion de la faute -> mode BACKUP
        self.mode = 0




