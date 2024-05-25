import heapq
from collections import Counter
from bitarray import bitarray


class HuffmanNode:
    def __init__(self, symbol=None, freq=0):
        self.symbol = symbol
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(freq_table):
    heap = [HuffmanNode(symbol=symbol, freq=freq) for symbol, freq in freq_table.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(freq=left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0]


def build_codes(node, prefix="", codebook={}):
    if node is not None:
        if node.symbol is not None:
            codebook[node.symbol] = prefix
        build_codes(node.left, prefix + "0", codebook)
        build_codes(node.right, prefix + "1", codebook)
    return codebook


def huffman_encode(data):
    # Шаг 1: Вычислить частоту каждого байта
    freq_table = Counter(data)

    # Шаг 2: Построить дерево Хаффмана
    huffman_tree = build_huffman_tree(freq_table)

    # Шаг 3: Построить коды из дерева Хаффмана
    huffman_codes = build_codes(huffman_tree)

    # Шаг 4: Закодировать данные с использованием кодов Хаффмана
    encoded_data = bitarray()

    huffman_codes_bitarray = {k: bitarray(v) for k, v in huffman_codes.items()}
    encoded_data.encode(huffman_codes_bitarray, data)

    # Шаг 5: Преобразовать закодированные данные в байты
    padding_length = (8 - len(encoded_data) % 8) % 8
    encoded_data.extend([0] * padding_length)
    padded_info = bitarray(f"{padding_length:08b}")

    encoded_bytes = padded_info.tobytes() + encoded_data.tobytes()

    return encoded_bytes, huffman_tree


def huffman_decode(encoded_data, huffman_tree):
    # Шаг 1: Преобразовать байты в битовую строку
    bit_string = bitarray()
    bit_string.frombytes(encoded_data)

    # Шаг 2: Удалить информацию о дополнении
    padding_length = int(bit_string[:8].to01(), 2)
    bit_string = bit_string[8:]
    if padding_length > 0:
        bit_string = bit_string[:-padding_length]

    # Шаг 3: Декодировать битовую строку с использованием дерева Хаффмана
    decoded_bytes = bytearray()
    current_node = huffman_tree

    for bit in bit_string:
        if bit == 0:
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.left is None and current_node.right is None:
            decoded_bytes.append(current_node.symbol)
            current_node = huffman_tree

    return bytes(decoded_bytes)

