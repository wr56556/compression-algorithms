def mtf_encode(data: bytes) -> bytes:
    symbol_table = list(range(256))
    encoded = []
    for byte in data:
        index = symbol_table.index(byte)
        encoded.append(index)
        # Move the used byte to the front
        symbol_table.pop(index)
        symbol_table.insert(0, byte)
    return bytes(encoded)


def mtf_decode(encoded_data: bytes) -> bytes:
    symbol_table = list(range(256))
    decoded = []
    for index in encoded_data:
        byte = symbol_table[index]
        decoded.append(byte)
        # Move the used byte to the front
        symbol_table.pop(index)
        symbol_table.insert(0, byte)
    return bytes(decoded)