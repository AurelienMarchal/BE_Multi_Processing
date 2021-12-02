from data_base import DataBase
from server import Server
from sensor import Sensor
from multiprocessing import Queue


if __name__ == '__main__':

    queue1_sensor = Queue(maxsize=10)
    queue1_data_base = Queue(maxsize=10)
    
    sensor1 = Sensor(queue1_sensor)
    server1 = Server(queue_sensor = queue1_sensor, queue_data_base = queue1_data_base)
    data_base1 = DataBase(queue1_data_base)


    sensor1.start()
    server1.start()
    data_base1.start()

