import sys
sys.path.append("..")

from algorithms.mtf import mtf_encode, mtf_decode
import numpy as np
from PIL import Image
import requests
from io import BytesIO
from algorithms.lz77 import lz77_encode, lz77_decode
from algorithms.huffman import huffman_encode, huffman_decode
from algorithms.rle import rle_encode, rle_decode
from algorithms.bwt import bwt_encode, bwt_decode

image_urls = [
    "https://cs.pikabu.ru/post_img/big/2013/03/17/6/1363508611_1596589037.jpg",  # black-white
    "https://kartin.papik.pro/uploads/posts/2023-06/1688115335_kartin-papik-pro-p-kartinki-seroe-nebo-dozhd-67.jpg",  # gray
    "https://zavodstekol.ru/source/images/cvetnoe/photo2.jpg"  # color
]

images = []
for url in image_urls:
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    images.append(img)

# Приведение изображений к одинаковому разрешению
resolution = (55, 55)
resized_images = [img.resize(resolution) for img in images]


# Конвертация в raw формат
def convert_to_raw(image):
    return image.tobytes()


raw_images = [convert_to_raw(img) for img in resized_images]

# Применение RLE к изображениям
# encoded_images = [rle_encode(raw_img, 1) for raw_img in raw_images]
# decoded_images = [rle_decode(enc_img, 1) for enc_img in encoded_images]

# Применение Хаффмана к изображениям
# encoded_images = [huffman_encode(raw_img) for raw_img in raw_images]
# decoded_images = [huffman_decode(enc_img, huffman_tree) for enc_img, huffman_tree in encoded_images]

# Применение lz77 к изображениям
# encoded_images = [lz77_encode(raw_img) for raw_img in raw_images]
# decoded_images = [lz77_decode(encoded_img) for encoded_img in encoded_images]


# encoded_images = [lz77_encode(raw_img) for raw_img in raw_images]
# decoded_images = [lz77_decode(encoded_img) for encoded_img in encoded_images]

# encoded_images = []
# original_indices = []
#
#
# for raw_img in raw_images:
#     encoded_image, original_index = bwt_encode(raw_img, type="img")
#     encoded_images.append(encoded_image)
#     original_indices.append(original_index)
#
# rle_encoded = [rle_encode(encoded_img, 1) for encoded_img in encoded_images]
# rle_decoded = [rle_decode(encoded_img, 1) for encoded_img in rle_encoded]
#
# decoded_images = [
#     bwt_decode(img, original_indices[i], type="img")
#     for i, img in enumerate(rle_decoded)
# ]


# i = 1
# bwt_encoded, original_index = bwt_encode(raw_images[i], type="img")
# mtf_encoded = mtf_encode(bwt_encoded)
# huffman_encoded, huffman_tree = huffman_encode(mtf_encoded)
# mtf_decoded = huffman_decode(huffman_encoded, huffman_tree)
# bwt_decoded = mtf_decode(mtf_decoded)
# decoded_image = bwt_decode(bwt_decoded, original_index, type="img")


# i = 2
# bwt_encoded, original_index = bwt_encode(raw_images[i], type="img")
# mtf_encoded = mtf_encode(bwt_encoded)
# rle_encoded = rle_encode(mtf_encoded, 3)
# huffman_encoded, huffman_tree = huffman_encode(rle_encoded)
#
# rle_decoded = huffman_decode(huffman_encoded, huffman_tree)
# mtf_decoded = rle_decode(rle_decoded, 3)
# bwt_decoded = mtf_decode(mtf_decoded)
#
# decoded_image = bwt_decode(bwt_decoded, original_index, type="img")

# i = 0
# lz77_encoded = lz77_encode(raw_images[i])
# huffman_encoded, huffman_tree = huffman_encode(lz77_encoded)
#
# lz77_encoded_bytes = huffman_decode(huffman_encoded, huffman_tree)
# lz77_compressed = lz77_decode(lz77_encoded_bytes)
#
# decoded_image = lz77_compressed(lz77_compressed)

j = 2
lz77_compressed = lz77_encode(raw_images[j])
# Преобразование списка кортежей в байты для дальнейшего сжатия Хаффманом
lz77_bytes = bytearray()
for item in lz77_compressed:
    offset, length, next_char = item
    lz77_bytes.extend(offset.to_bytes(2, 'big'))
    lz77_bytes.extend(length.to_bytes(2, 'big'))
    if next_char is not None:
        lz77_bytes.append(next_char)

    huffman_compressed, huffman_tree = huffman_encode(lz77_bytes)

lz77_bytes = huffman_decode(huffman_compressed, huffman_tree)

# Преобразование байтов обратно в список кортежей для декодирования LZ77
lz77_compressed = []
i = 0
while i < len(lz77_bytes):
    offset = int.from_bytes(lz77_bytes[i:i + 2], 'big')
    length = int.from_bytes(lz77_bytes[i + 2:i + 4], 'big')
    next_char = lz77_bytes[i + 4] if i + 4 < len(lz77_bytes) else None
    lz77_compressed.append((offset, length, next_char))
    i += 5

# Декодирование LZ77
decoded_image = lz77_decode(lz77_compressed)

assert raw_images[j] == decoded_image, f"Image {j} did not decode correctly"

print("All images decoded correctly")

original_size = len(raw_images[j])
encoded_size = len(huffman_compressed) // 8
compression_ratio = original_size / encoded_size
print(f"Image {j} Compression Ratio: {compression_ratio:.2f}")

# Проверка корректности обратного преобразования
# for i in range(len(raw_images)):
#     assert raw_images[i] == decoded_images[i], f"Image {i} did not decode correctly"

# print("All images decoded correctly")


# Оценка степени сжатия
# for i in range(len(raw_images)):
#     original_size = len(raw_images[i])
#     encoded_size = len(huffman_encoded[i])
#     compression_ratio = original_size / encoded_size
#     print(f"Image {i} Compression Ratio: {compression_ratio:.2f}")

# Оценка степени сжатия хаффмана
# for i in range(len(raw_images)):
#     original_size = len(raw_images[i])
#     encoded_size = len(encoded_images[i][0]) // 8
#     compression_ratio = original_size / encoded_size
#     print(f"Image {i} Compression Ratio: {compression_ratio:.2f}")


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

# def calculate_entropy(text):
#     counts = np.zeros(256)
#     for c in text:
#         counts[ord(c)] += 1
#     probs = counts / len(text) * 4 #если умножать на длину символов энтропия = 10.9 / 14.63 / 10.95
#     entropy = 0
#     for p in probs:
#         if p !=0:
#             entropy -= p*np.log2(p)
#     return entropy
#
#
# print(calculate_entropy(str(raw_images[2])))
