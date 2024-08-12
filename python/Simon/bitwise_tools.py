from typing import Tuple

def split_32bit_to_16bit(value: int) -> Tuple[int, int]:
    """
    Divide un entero de 32 bits en dos enteros de 16 bits.

    Args:
        value (int): El valor de 32 bits a dividir.

    Returns:
        (int, int): Una tupla con los dos valores de 16 bits.
    """
    # Asegúrate de que el valor está dentro del rango de 32 bits sin signo
    if not (0 <= value <= 0xFFFFFFFF):
        raise ValueError("El valor debe estar en el rango de 32 bits sin signo (0 a 4294967295).")
    
    # Extraer los 16 bits más bajos
    lower_16bits = value & 0xFFFF
    # Desplazar 16 bits a la derecha y extraer los 16 bits más altos
    upper_16bits = (value >> 16) & 0xFFFF

    return upper_16bits, lower_16bits


def circular_shift_left(value: int, shift: int) -> int:
    """
    Realiza un desplazamiento circular a la izquierda de un valor dado.

    Args:
        value (int): El valor que se va a desplazar.
        shift (int): La cantidad de posiciones para desplazar.

    Returns:
        int: El valor después del desplazamiento circular.
    """
    # bit_length (int): El número de bits del valor que para nuestro caso siempre será de 16 bits
    bit_length = 16
    
    # Asegúrate de que el valor está dentro del rango del bit_length
    if not (0 <= value < (1 << bit_length)):
        raise ValueError(f"El valor debe estar en el rango de {bit_length} bits sin signo (0 a {(1 << bit_length) - 1}).")
    
    # Ajustar el desplazamiento para que esté dentro del rango del bit_length
    shift %= bit_length
    
    # Desplazamiento circular a la izquierda
    return ((value << shift) & ((1 << bit_length) - 1)) | (value >> (bit_length - shift))

def circular_shift_right(value: int, shift: int) -> int:
    """
    Realiza un desplazamiento circular a la derecha de un valor dado.

    Args:
        value (int): El valor a desplazar.
        bit_length (int): El número de bits considerados para el desplazamiento.
        shift (int): La cantidad de posiciones a desplazar.

    Returns:
        int: El valor después del desplazamiento circular a la derecha.
    """
    # bit_length (int): El número de bits del valor que para nuestro caso siempre será de 16 bits
    bit_length = 16
    
    # Asegúrate de que el desplazamiento esté en el rango válido
    shift %= bit_length
    
    # Desplazamiento circular a la derecha
    right_shifted = value >> shift
    left_shifted = (value << (bit_length - shift)) & ((1 << bit_length) - 1)
    
    return right_shifted | left_shifted

def split_64bit_to_16bit_segments(value: int) -> tuple:
    """
    Divide un valor de 64 bits en cuatro valores de 16 bits.

    Args:
        value (int): El valor de 64 bits a dividir.

    Returns:
        tuple: Una tupla que contiene cuatro valores de 16 bits.
    """
    # Asegúrate de que el valor está en el rango de 64 bits
    if not (0 <= value < (1 << 64)):
        raise ValueError("El valor debe estar en el rango de 64 bits sin signo (0 a 2^64 - 1).")

    # Extraer los segmentos de 16 bits
    segment1 = (value >> 48) & 0xFFFF  # 16 bits más significativos
    segment2 = (value >> 32) & 0xFFFF
    segment3 = (value >> 16) & 0xFFFF
    segment4 = value & 0xFFFF  # 16 bits menos significativos

    return segment1, segment2, segment3, segment4


def get_bits(value: int, bit_length: int) -> list:
    """
    Obtiene los bits de un número de forma individual.

    Args:
        value (int): El número del cual extraer los bits.
        bit_length (int): La longitud en bits del número a considerar.

    Returns:
        list: Una lista de bits (0 o 1) del número.
    """
    bits = []
    for i in range(bit_length):
        # Desplaza el bit hacia la derecha y aplica una máscara con 1 para obtener el bit
        bit = (value >> i) & 1
        bits.append(bit)
    
    # La lista se construye desde el bit menos significativo al más significativo
    return bits
