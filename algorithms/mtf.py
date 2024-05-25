class MTF:
    def __init__(self):
        self.symbol_table = list(range(256))

    def encode(self, data: bytes) -> bytes:
        encoded = []
        for byte in data:
            index = self.symbol_table.index(byte)
            encoded.append(index)
            # Move the used byte to the front
            self.symbol_table.pop(index)
            self.symbol_table.insert(0, byte)
        return bytes(encoded)

    def decode(self, encoded_data: bytes) -> bytes:
        decoded = []
        for index in encoded_data:
            byte = self.symbol_table[index]
            decoded.append(byte)
            # Move the used byte to the front
            self.symbol_table.pop(index)
            self.symbol_table.insert(0, byte)
        return bytes(decoded)