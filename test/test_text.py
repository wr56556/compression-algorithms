import sys
sys.path.append("..")
import numpy as np
from algorithms.rle import rle_decode, rle_encode
from algorithms.huffman import huffman_encode, huffman_decode
from algorithms.lz77 import lz77_encode, lz77_decode
from algorithms.bwt import bwt_decode, bwt_encode
from algorithms.mtf import mtf_encode, mtf_decode


with open('data/Kononenko_Maksim__Vladimir_Vladimirovich_www.Litmir.net_88219.txt', 'r', encoding="utf-8") as file:
     book_data = file.read().replace('\n', '')

with open('data/enwik7.txt', 'r', encoding="utf-8") as file:
    enwik_data = file.read()


#original_data = book_data[:50000]
#original_data = enwik_data.encode("utf-8")
original_data = book_data.encode("utf-8")
#original_data = book_data[:10000] + '\0'

#encoded_text = rle_encode(original_data, 3)
#decoded_text = rle_decode(encoded_text, 3)

#encoded_text, huffman_tree = huffman_encode(original_data)
#decoded_text = huffman_decode(encoded_text, huffman_tree)

#encoded_text = lz77_encode(original_data)
#decoded_text = lz77_decode(encoded_text)


# encoded_text, original_index = bwt_encode(original_data)
# rle_encoded = rle_encode(encoded_text, 1)
# rle_decoded = rle_decode(rle_encoded, 1)
# decoded_text = bwt_decode(rle_decoded, original_index)


# bwt_encoded, index = bwt_encode(original_data)
# mtf_encoded = mtf_encode(bwt_encoded)
# huffman_encoded, huffman_tree = huffman_encode(mtf_encoded)
# mtf_decoded_bytes = huffman_decode(huffman_encoded, huffman_tree)
# mtf_decoded = list(mtf_decoded_bytes)
# bwt_decoded = mtf_decode(mtf_decoded)
# decoded_text = bwt_decode(bwt_decoded, index)

# bwt_encoded, original_index = bwt_encode(original_data)
# mtf_encoded = mtf_encode(bwt_encoded)
# rle_encoded = rle_encode(mtf_encoded, 3)
# huffman_encoded, huffman_tree = huffman_encode(rle_encoded)
#
# rle_decoded = huffman_decode(huffman_encoded, huffman_tree)
# mtf_decoded = rle_decode(rle_decoded, 3)
# bwt_decoded = mtf_decode(mtf_decoded)
#
# decoded_text = bwt_decode(bwt_decoded, original_index)


lz77_encoded_data = lz77_encode(original_data)
flat_lz77_data = bytearray()
for item in lz77_encoded_data:
    offset, length, next_char = item
    flat_lz77_data.extend(offset.to_bytes(2, 'big'))
    flat_lz77_data.extend(length.to_bytes(2, 'big'))
    flat_lz77_data.append(next_char if next_char is not None else 0)

huffman_encoded_data, huffman_tree = huffman_encode(flat_lz77_data)
flat_lz77_data = huffman_decode(huffman_encoded_data, huffman_tree)

lz77_decoded_data = []

for i in range(0, len(flat_lz77_data), 5):
    offset = int.from_bytes(flat_lz77_data[i:i + 2], 'big')
    length = int.from_bytes(flat_lz77_data[i + 2:i + 4], 'big')
    next_char = flat_lz77_data[i + 4]
    lz77_decoded_data.append((offset, length, next_char if next_char != 0 else None))

decoded_text = lz77_decode(lz77_decoded_data)

print(f"Оригинальный размер: {sys.getsizeof(original_data)}")
print(f"Сжатый размер: {sys.getsizeof(huffman_encoded_data)}")
compression_ratio = sys.getsizeof(original_data) / sys.getsizeof(huffman_encoded_data)
print(f"Compression Ratio: {compression_ratio:.2f}")


# Проверка корректности обратного преобразования
assert decoded_text == original_data, "Decoded data does not match the original data!"
print("Decoded data matches the original data.")


# def calculate_entropy(text):
#     counts = np.zeros(256)
#     for c in text:
#         counts[ord(c)] += 1
#     probs = counts / len(text)
#     entropy = 0
#     for p in probs:
#         if p !=0:
#             entropy -= p*np.log2(p)
#     return entropy
#
#
# print(calculate_entropy(str(original_data)))