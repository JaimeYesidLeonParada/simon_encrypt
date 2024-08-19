# Importamos las librerías necesarias
import paho.mqtt.client as mqtt  # Librería para manejar cliente MQTT
import simon  # Archivo de cifrado Simon 

# Definimos la clave para descifrar el mensaje
key_simon = 0x0123456789ABCDEF

# Especificamos el hostname del broker MQTT y el puerto
hostname = "192.168.137.139"
broker_port = 1883  # Puerto estándar de MQTT

# Especificamos el tópico MQTT al que nos suscribiremos
topic = "home/temp"

# Función que se ejecuta cuando el cliente se conecta exitosamente al broker MQTT
def on_connect(client, userdata, flags, rc):
    # 'rc' es el código de retorno; si es 0, la conexión fue exitosa
    print("Se conectó a MQTT con código de retorno: " + str(rc))
    
    # Nos suscribimos al tópico especificado para recibir mensajes
    client.subscribe(topic)

# Función que se ejecuta cuando se recibe un mensaje en el tópico suscrito
def on_message(client, userdata, msg):
    # El mensaje recibido está cifrado, así que lo desciframos
    temperature_encrypted = int(msg.payload.decode())  # Convertimos el payload del mensaje en un entero
    temperature_decrypt = simon.decipher(temperature_encrypted, key_simon)  # Desciframos el mensaje con la clave
    
    # Mostramos la temperatura descifrada, dividiéndola por 1000 para obtener el punto decimal que se quito en el publisher
    print("Temperatura: ", (temperature_decrypt / 1000))

# Creamos una instancia del cliente MQTT
client = mqtt.Client()

# Asociamos las funciones de callback al cliente MQTT
client.on_connect = on_connect  # Callback para manejar conexión
client.on_message = on_message  # Callback para manejar mensajes

# Conectamos el cliente al broker MQTT
client.connect(hostname, broker_port, 60)  # Espera un timeout de 60 segundos para la conexión

# Iniciamos el bucle de espera de mensajes de manera indefinida
client.loop_forever()  # Mantiene el cliente en ejecución esperando mensajes
