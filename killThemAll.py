import paho.mqtt.client as mqtt

if __name__ == "__main__":
    client = mqtt.Client(client_id="Freddy Krueger")

    client.connect("127.0.0.255", port=1883)
    #
    # client.publish("/dataBase/kill", "burn")
    client.publish("/server/kill", "burn")
    # client.publish("/sensor/kill", "burn")
    # client.publish("/cdg/kill", "burn")