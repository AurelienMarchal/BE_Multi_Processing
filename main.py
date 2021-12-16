from multiprocessing import Queue

import subprocess

if __name__ == '__main__':

    # queue1_sensor = Queue(maxsize=10)
    # queue1_data_base = Queue(maxsize=10)

    # sensor1 = Sensor(queue1_sensor)
    # server1 = Server(queue_sensor = queue1_sensor, queue_data_base = queue1_data_base)
    # data_base1 = DataBase(queue1_data_base)

    subprocess.Popen("python3 server.py")
    subprocess.Popen("python3 sensor.py")
    subprocess.Popen("python3 data_base.py")
