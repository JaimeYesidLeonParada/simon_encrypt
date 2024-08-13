from w1thermsensor import W1ThermSensor, Unit
import paho.mqtt.client as mqtt
import simon
import time

key_simon = 0x0123456789ABCDEF
hostname = "localhost"
broker_port = 1883
topic = "home/temp"

sensor = W1ThermSensor()
client = mqtt.Client()
client.connect(hostname, broker_port, 60)

while True:
    temperature = sensor.get_temperature()
    temperature_int = int(temperature * 1000)
    print("Temperature: ", temperature)
    
    temperature_encrypted = simon.encrypt(temperature_int, key_simon)
    client.publish(topic, temperature_encrypted)

    time.sleep(5)
    