from typing import Tuple
from bitwise_tools import split_32bit_to_16bit, circular_shift_left, split_64bit_to_16bit_segments, get_bits, circular_shift_right

def encrypt(value: int, key: int) -> int:
    """
    Encripta un valor entero de 32 bits usando una clave dada.

    Args:
        value (int): El valor a encriptar, que se espera sea un entero de 32 bits.
        key (int): La clave de encriptación utilizada para generar las claves de ronda.

    Returns:
        int: El entero de 32 bits encriptado.
    """
    # Inicializar round0 con el valor de entrada enmascarado a 32 bits
    round0 = value & 0xFFFFFFFF
    
    # Generar una lista de claves de ronda usando la clave proporcionada
    keys = _list_of_keys_for(key)

    # Realizar rondas de encriptación usando cada clave de ronda
    for r_key in keys:
        # Ejecutar una ronda de encriptación usando la clave de ronda actual
        l0, r0 = _round_of_encryption(round0, r_key)
        
        # Combinar las mitades izquierda y derecha en un solo valor de 32 bits
        round0 = (l0 << 16) | (r0)
    
    # Devolver el valor encriptado final
    return round0

def decipher(value: int, key: int) -> int:
    """
    Desencripta un valor entero de 32 bits usando una clave dada.

    Args:
        value (int): El valor a desencriptar, que se espera sea un entero de 32 bits.
        key (int): La clave de desencriptación utilizada para generar las claves de ronda.

    Returns:
        int: El entero de 32 bits desencriptado.
    """
    # Inicializar round0 con el valor de entrada enmascarado a 32 bits
    round0 = value & 0xFFFFFFFF
    
    # Dividir el valor de 32 bits en dos valores de 16 bits
    ls0, rs0 = split_32bit_to_16bit(round0)
    
    # Reorganizar las mitades: colocar la parte derecha como izquierda y viceversa
    round0 = (rs0 << 16) | (ls0)
    
    # Generar una lista de claves de ronda usando la clave proporcionada
    keys = _list_of_keys_for(key)

    # Realizar rondas de desencriptación usando cada clave de ronda en orden inverso
    for r_key in reversed(keys):
        # Ejecutar una ronda de desencriptación usando la clave de ronda actual
        l0, r0 = _round_of_encryption(round0, r_key)
        
        # Combinar las mitades izquierda y derecha en un solo valor de 32 bits
        round0 = (l0 << 16) | (r0)
    
    # Devolver el valor desencriptado final
    return round0 

def _list_of_keys_for(key: int) -> list:
    """
    Genera una lista de claves de ronda para el cifrado Simon a partir de una clave dada.

    Args:
        key (int): La clave inicial utilizada para generar las claves de ronda, que se espera sea un entero de 64 bits.

    Returns:
        list: Una lista de claves de ronda generadas.
    """
    # Enmascarar la clave a 64 bits para asegurarse de que solo se utilicen 64 bits significativos
    key_64bits = key & 0xFFFFFFFFFFFFFFFF
    
    # Constante z0 utilizada para el cálculo de las claves de ronda
    z0 = 0b10110011100001101010010001011111  # Representación binaria de B386A45F
    
    # Definir el número de bits en la longitud de la clave
    bit_length = 28
    
    # Dividir la clave de 64 bits en segmentos de 16 bits y revertir el orden
    simon_keys = list(reversed(split_64bit_to_16bit_segments(key_64bits)))
    
    # Generar claves de ronda adicionales usando una función específica
    for i in range(bit_length):
        # Obtener las claves actuales para la función de generación de claves
        out_keys = simon_keys[i:]
        
        # Calcular la siguiente clave de ronda usando una función específica y una constante
        out = _key_function(out_keys, _get_constant(z0, bit_length, i))
        
        # Agregar la nueva clave generada a la lista de claves
        simon_keys.append(out)
    
    # Devolver la lista completa de claves de ronda
    return simon_keys

def _round_of_encryption(value_32bit: int, key_16bit: int) -> Tuple[int, int]:
    """
    Realiza una ronda de encriptación Simon en un valor de 32 bits usando una clave de 16 bits.

    Args:
        value_32bit (int): El valor de 32 bits a encriptar.
        key_16bit (int): La clave de 16 bits utilizada en la ronda de encriptación.

    Returns:
        Tuple[int, int]: Una tupla que contiene los valores encriptados de 16 bits (l1, r1).
    """
    # Dividir el valor de 32 bits en dos partes de 16 bits: l0 (izquierda) y r0 (derecha)
    l0, r0 = split_32bit_to_16bit(value_32bit)
    
    # Asignar la clave de 16 bits a k0
    k0 = key_16bit

    # Realizar desplazamientos circulares a la izquierda
    s1 = circular_shift_left(l0, 1)  # Desplazar l0 una posición a la izquierda
    s2 = circular_shift_left(l0, 2)  # Desplazar l0 dos posiciones a la izquierda
    s8 = circular_shift_left(l0, 8)  # Desplazar l0 ocho posiciones a la izquierda

    # Paso 1: Operación AND entre s1 y s8
    step1 = s1 & s8

    # Paso 2: Operación XOR entre el resultado del paso 1 y r0
    step2 = r0 ^ step1

    # Paso 3: Operación XOR entre el resultado del paso 2 y s2
    step3 = s2 ^ step2

    # Paso 4: Operación XOR entre el resultado del paso 3 y la clave k0
    step4 = step3 ^ k0

    # Asignar el resultado de step4 a l1 y l0 a r1
    l1 = step4
    r1 = l0
    
    # Devolver los nuevos valores l1 y r1
    return l1, r1

def _get_constant(constant: int, bit_length: int, index: int) -> int:
    """
    Obtiene una constante dependiendo del índice del bit de la constante principal.

    Args:
        constant (int): La constante base de la cual se extraen los bits.
        bit_length (int): La longitud en bits que se considera para la constante.
        index (int): El índice del bit que se evalúa para determinar qué constante retornar.

    Returns:
        int: Retorna constant1 si el bit es 1, de lo contrario retorna constant2.
    """
    # Obtener los bits de la constante según la longitud especificada
    bits = get_bits(constant, bit_length)
    
    # Obtener el bit en la posición del índice especificado
    bit = bits[index]
    
    # Retornar constant1 si el bit es 1, o constant2 si el bit es 0
    return 0xFFFD if bit == 1 else 0xFFFC

    
def _key_function(keys, constant: int) -> int:
    """
    Calcula una nueva clave de ronda usando una lista de claves y una constante.

    Args:
        keys (list): Lista de 4 claves enteras utilizadas para calcular la nueva clave.
        constant (int): Constante utilizada en el cálculo de la nueva clave.

    Returns:
        int: La nueva clave calculada.

    Raises:
        ValueError: Si el parámetro `keys` no es una lista de exactamente 4 elementos.
    """
    # Verificar que keys sea una lista con exactamente 4 elementos
    if not isinstance(keys, list) or len(keys) != 4:
        raise ValueError("El parámetro debe ser una lista de exactamente 4 elementos.")
    
    # Paso 1: Desplazamiento circular a la derecha de keys[3] por 3 posiciones
    step1 = circular_shift_right(keys[3], 3)
    
    # Paso 2: Operación XOR entre step1 y keys[1]
    step2 = step1 ^ keys[1]
    
    # Paso 3: Desplazamiento circular a la derecha de step2 por 1 posición
    step3 = circular_shift_right(step2, 1)
    
    # Paso 4: Operación XOR entre keys[0] y step2
    step4 = keys[0] ^ step2
    
    # Paso 5: Operación XOR entre step3 y step4
    step5 = step3 ^ step4
    
    # Operación XOR final entre step5 y la constante
    out = step5 ^ constant
    
    # Retornar la nueva clave calculada
    return out    
