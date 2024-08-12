from w1thermsensor import W1ThermSensor, Unit
import time

sensor = W1ThermSensor()

while True:
    temperature_in_celsius = sensor.get_temperature()
    print("Temperature in Celsius: ", temperature_in_celsius)
    time.sleep(5)