import paho.mqtt.client as mqtt

if __name__ == "__main__":
    client = mqtt.Client(client_id="Freddy Krueger")

    client.connect("127.0.0.255", port=1883)

    client.publish("/dataBase/kill", "burn")
    client.publish("/server0/kill", "burn")
    client.publish("/server1/kill", "burn")
    client.publish("/server2/kill", "burn")
    client.publish("/sensor/kill", "burn")
    client.publish("/service/kill", "burn")
    client.publish("/cdg/kill", "burn")