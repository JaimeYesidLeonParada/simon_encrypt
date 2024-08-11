import simon

temperature = 0x00FF00FF  #16711935
key_64bits = 0x0123456789ABCDEF

temperature_encrypted = simon.encrypt(temperature, key_64bits)
print("Temperature crypted: ", hex(temperature_encrypted))


temperature_decrypt = simon.decrypt(temperature_encrypted, key_64bits)
print("Temperature decrypted: ", hex(temperature_decrypt))

# Temperature crypted:  0xa2_8a_a9_32