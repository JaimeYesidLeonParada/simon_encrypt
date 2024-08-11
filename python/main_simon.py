import simon

temperature = 16711935 #0x00FF00FF
key_64bits = 0x0123456789ABCDEF

temperature_encrypted = simon.encrypt(temperature, key_64bits)
print("Temperature crypted: ", hex(temperature_encrypted))

# Temperature crypted:  0xa2_8a_a9_32