from time import sleep

DEVICE_FILE = '/sys/bus/w1/devices/28-0b2324dace8b/w1_slave'

def read_temp_raw():
    with open(DEVICE_FILE, 'r') as f:
        lines = f.readlines()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

while True:
    temperature = read_temp()
    sleep(2)
    print(f"Temperatura: {temperature:.2f}°C")
    