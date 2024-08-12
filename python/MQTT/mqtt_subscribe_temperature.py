import time
import paho.mqtt.client as mqtt
import random

hostname = "localhost"
broker_port = 1883
topic = "home/temp"

def on_connect(client, userdata, flags, rc):
    print("Se connecto a MQTT " + str(rc))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    print(msg.topic + " " + msg.payload.decode())

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(hostname, broker_port, 60)
client.loop_forever()
