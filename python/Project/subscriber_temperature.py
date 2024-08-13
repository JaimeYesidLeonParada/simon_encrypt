import paho.mqtt.client as mqtt
import random
import simon

key_simon = 0x0123456789ABCDEF
hostname = "localhost"
broker_port = 1883
topic = "home/temp"

def on_connect(client, userdata, flags, rc):
    print("Se connecto a MQTT " + str(rc))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    temperature_encrypted = int(msg.payload.decode())
    temperature_decrypt = simon.decipher(temperature_encrypted, key_simon)
    print("Temperature: ", (temperature_decrypt / 1000))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(hostname, broker_port, 60)
client.loop_forever()