import paho.mqtt.client as mqtt
import random
import time

hostname = "localhost"
broker_port = 1883
topic = "home/temp"

client = mqtt.Client()
client.connect(hostname, broker_port, 60)

while True:
    client.publish(topic, str(random.randrange(1, 100)))
    time.sleep(5)
    