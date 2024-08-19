# Importar las bibliotecas necesarias
from w1thermsensor import W1ThermSensor, Unit  # Biblioteca para manejar sensores de temperatura 1-Wire
import paho.mqtt.client as mqtt  # Biblioteca para el cliente MQTT
import simon  # Archivo para usar el algoritmo de cifrado Simon
import time  # Biblioteca para manejar tiempos y retrasos

# Definición de variables clave
key_simon = 0x0123456789ABCDEF  # Clave para el cifrado Simon
hostname = "192.168.137.139"  # Dirección del broker MQTT
broker_port = 1883  # Puerto del broker MQTT
topic = "home/temp"  # Tema MQTT donde se publicará la temperatura

# Inicializar el sensor de temperatura 1-Wire
sensor = W1ThermSensor()

# Crear un nuevo cliente MQTT
client = mqtt.Client()

# Conectar el cliente MQTT al broker
client.connect(hostname, broker_port, 60)

# Bucle infinito para medir y enviar temperatura periódicamente
while True:
    # Obtener la temperatura desde el sensor
    temperature = sensor.get_temperature()
    
    # Convertir la temperatura a un entero después de multiplicarla por 1000 para evitar el punto flotante
    temperature_int = int(temperature * 1000)
    
    # Imprimir la temperatura en la consola
    print("Temperature: ", temperature)
    
    # Cifrar la temperatura utilizando el algoritmo Simon con la clave proporcionada
    temperature_encrypted = simon.encrypt(temperature_int, key_simon)
    
    # Publicar la temperatura cifrada en el tema MQTT especificado
    client.publish(topic, temperature_encrypted)
    
    # Pausar el bucle durante 5 segundos antes de repetir el proceso
    time.sleep(5)

    