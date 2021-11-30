from server import Server
from sensor import Sensor
from multiprocessing import Queue


if __name__ == '__main__':

    queue1 = Queue(maxsize=10)

    
    sensor1 = Sensor(queue1)
    server1 = Server(queue1)

    sensor1.start()
    server1.start()

