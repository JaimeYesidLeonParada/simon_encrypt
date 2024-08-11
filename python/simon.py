from typing import Tuple
from bitwise_tools import split_32bit_to_16bit, circular_shift_left, split_64bit_to_16bit_segments, get_bits, circular_shift_right

def encrypt(value: int, key: int) -> int:
    round0 = value & 0xFFFFFFFF 
    keys = _list_of_keys_for(key)

    for r_key in keys:
        l0, r0 = _round_of_encryption(round0, r_key)
        round0 = (l0 << 16) | (r0)
        
    return round0

def decrypt(value: int, key: int) -> int:
    round0 = value & 0xFFFFFFFF
    ls0, rs0 = split_32bit_to_16bit(round0)
    round0 = (rs0 << 16) | (ls0)
    keys = _list_of_keys_for(key)
    
    for r_key in reversed(keys):
        l0, r0 = _round_of_encryption(round0, r_key)
        round0 = (l0 << 16) | (r0)
        
    return round0 

def _list_of_keys_for(key: int) -> list:
    key_64bits = key & 0xFFFFFFFFFFFFFFFF
    z0 = 0b10110011100001101010010001011111 # B386A45F
    bit_length = 28
    simon_keys = list(reversed(split_64bit_to_16bit_segments(key_64bits)))
    
    for i in range(bit_length):
        out_keys = simon_keys[i:]
        out = _key_function(out_keys, _get_constant(z0, bit_length, i))
        simon_keys.append(out)
    
    return simon_keys

def _round_of_encryption(value_32bit: int, key_16bit: int) -> Tuple[int, int]:
    l0, r0 = split_32bit_to_16bit(value_32bit)
    k0 = key_16bit

    s1 = circular_shift_left(l0, 1)  # Desplazar 1 posición a la izquierda
    s2 = circular_shift_left(l0, 2)  # Desplazar 1 posición a la izquierda
    s8 = circular_shift_left(l0, 8)  # Desplazar 1 posición a la izquierda

    step1 = s1 & s8 # Step 1 = Operación AND entre s1 y s8

    step2 = r0 ^ step1 # Step 2 = Operación XOR entre el step 1 y r0

    step3 = s2 ^ step2 # Step 3 = Operacion XOR entre Step 2 y s2

    step4 = step3 ^ k0 # Step 4 = Operacion XOR entre paso 3 y la key

    l1 = step4 #
    r1 = l0
    
    return l1, r1

def _get_constant(constant: int, bit_length: int, index: int) -> int:
    """
    Obtiene la constante dependiendo del indice
    """
    constant1 = 0xFFFD
    constant2 = 0xFFFC
    
    bits = get_bits(constant, bit_length)
    bit = bits[index]
    
    if bit == 1:
        return constant1
    else:
        return constant2
    
def _key_function(keys, constant: int) -> int:
    if not isinstance(keys, list) or len(keys) != 4:
        raise ValueError("El parámetro debe ser una lista de exactamente 4 elementos.")
    
    step1 = circular_shift_right(keys[3], 3)
    step2 = step1 ^ keys[1]
    step3 = circular_shift_right(step2, 1)
    step4 = keys[0] ^ step2
    step5 = step3 ^ step4
    out = step5 ^ constant
    
    return out
    
