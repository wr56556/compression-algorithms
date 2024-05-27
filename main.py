from PIL import Image
import requests
from io import BytesIO
from algorithms.rle import rle_decode, rle_encode
from algorithms.huffman import huffman_encode, huffman_decode
import numpy as np
from algorithms.lz77 import lz77_encode, lz77_decode
from algorithms.bwt import bwt_decode, bwt_encode
from algorithms.mtf import mtf_encode, mtf_decode

image_urls = [
    "https://cs.pikabu.ru/post_img/big/2013/03/17/6/1363508611_1596589037.jpg",  # black-white
    "https://blog.aspose.cloud/ru/imaging/grayscale-image-in-java/images/grayscale.jpg",  # gray
    "https://i.pinimg.com/564x/c5/ce/6f/c5ce6ff8d6bda2ef0f71140b8509abbf.jpg"  # color
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

# Сравнение размера исходного и raw формата
for i, img in enumerate(images):
    print(f"Original size {i}: {len(img.tobytes())} bytes")
    print(f"Raw size {i}: {len(raw_images[i])} bytes")


def calculate_entropy(text):
    counts = np.zeros(128)
    for c in text:
        counts[ord(c)] += 1
    probs = counts / len(text)
    entropy = 0
    for p in probs:
        if p !=0:
            entropy -= p*np.log2(p)
    return entropy


text = ("Mars is the fourth planet from the Sun. It was formed approximately 4.5 billion years ago,"
        " is a terrestrial planet and is the second smallest of the Solar System's planets with a diameter "
        "of 6,779 km (4,212 mi). A Martian solar day (sol) is 24.5 hours and a Martian solar year is 1.88 Earth years "
        "(687 Earth days). Mars has two small and irregular natural satellites: Phobos and Deimos. ")

print(calculate_entropy(text))


# Пример использования
original_data = b"AAAABBBCCDAA"
encoded_data = rle_encode(original_data, 1)
decoded_data = rle_decode(encoded_data, 1)

print(f"Original Data: {original_data}")
print(f"Encoded Data: {encoded_data}")
print(f"Decoded Data: {decoded_data}")

# Применение RLE к изображениям
encoded_images = [rle_encode(raw_img, 1) for raw_img in raw_images]
decoded_images = [rle_decode(enc_img, 1) for enc_img in encoded_images]

# Проверка корректности обратного преобразования
for i in range(len(raw_images)):
    assert raw_images[i] == decoded_images[i], f"Image {i} did not decode correctly"

# Оценка степени сжатия
for i in range(len(raw_images)):
    original_size = len(raw_images[i])
    encoded_size = len(encoded_images[i])
    compression_ratio = original_size / encoded_size
    print(f"Image {i} Compression Ratio: {compression_ratio:.2f}")

# Для изображения с цветом, кодируемым тремя байтами (например, RGB)
image_data = bytearray([255, 0, 0, 255, 0, 0, 255, 0, 0, 0, 255, 0])  # Пример данных
encoded_image = rle_encode(image_data, 3)
decoded_image = rle_decode(encoded_image, 3)
print(encoded_image)
print(decoded_image)

# Для текста в кодировке UTF-8
text_data = "аааббввв".encode("utf-8")
encoded_text = rle_encode(text_data, len("а".encode("utf-8")))
decoded_text = rle_decode(encoded_text, len("а".encode("utf-8")))
print(encoded_text)
print(decoded_text.decode("utf-8"))

# Пример использования Хаффмана:
data = b"example data for huffman encoding"
encoded_data, huffman_tree = huffman_encode(data)
decoded_data = huffman_decode(encoded_data, huffman_tree)

print("Original Data:", data)
print("Encoded Data:", encoded_data)
print("Decoded Data: ", decoded_data)

# Пример использования lz77
data = "ABABABAABABBBBBBBBBBBBA".encode('utf-8')
encoded_data = lz77_encode(data)
print("Encoded:", encoded_data)
decoded_data = lz77_decode(encoded_data)
print("Decoded:", decoded_data)

# Пример использования bwt
text_data = "banana"
bwt_encoded_text, original_index = bwt_encode(text_data + '\0')
print("BWT Encoded Text:", bwt_encoded_text)
print("Original Index:", original_index)
decoded_text = bwt_decode(bwt_encoded_text, original_index)
print("Decoded Text:", decoded_text)



#####################################################################################################################

# Применение Хаффмана к изображениям
huff_encoded_images = [huffman_encode(raw_img) for raw_img in raw_images]
huff_decoded_images = [huffman_decode(enc_img, huffman_tree) for enc_img, huffman_tree in huff_encoded_images]


# Проверка корректности обратного преобразования
for i in range(len(raw_images)):
    assert raw_images[i] == huff_decoded_images[i], f"Image {i} did not decode correctly"


# Оценка степени сжатия Хаффмана
for i in range(len(raw_images)):
    original_size = len(raw_images[i])
    encoded_size = len(huff_encoded_images[i][0]) // 8
    compression_ratio = (original_size / encoded_size)
    print(f"Image {i} Compression Ratio: {compression_ratio:.2f}")


# Применение lz77 к изображениям
lz77_encoded_images = [lz77_encode(raw_img) for raw_img in raw_images]
lz77_decoded_images = [lz77_decode(encoded_img) for encoded_img in lz77_encoded_images]


# Проверка корректности обратного преобразования
for i in range(len(raw_images)):
    assert raw_images[i] == lz77_decoded_images[i], f"Image {i} did not decode correctly"

# Оценка степени сжатия lz77
for i in range(len(raw_images)):
    original_size = len(raw_images[i])
    encoded_size = len(lz77_encoded_images[i])
    compression_ratio = (original_size / encoded_size)
    print(f"Image {i} Compression Ratio: {compression_ratio:.2f}")

# Применение BWT к изображениям
#bwt_encoded_images = [bwt_encode(img.decode('latin1') + '\0') for img in raw_images]
#bwt_decoded_images = [bwt_decode(bwt_img, orig_idx).encode('latin1') for bwt_img, orig_idx in bwt_encoded_images]

#bwt_encoded_image, original_index = bwt_encode(raw_images[0].decode('latin1') + '\0')
#bwt_decoded_image = bwt_decode(bwt_encoded_image, original_index).encode('latin1')

# Проверка корректности обратного преобразования
#assert raw_images[0] + b'\0' == bwt_decoded_image, f"Image {i} did not decode correctly"

# Оценка степени сжатия BWT

#original_size = len(raw_images[0])
#encoded_size = len(bwt_decoded_image)
#compression_ratio = (original_size / encoded_size)
#print(f"Image {0} Compression Ratio: {compression_ratio:.2f}")


# Применение MTF к raw изображениям

for raw_image in raw_images:
    mtf = MTF()
    encoded_image = mtf.encode(raw_image)
    decoded_image = mtf.decode(encoded_image)

    assert raw_image == decoded_image, f"Ошибка: {raw_image} != {decoded_image}"

print("Изображения успешно закодированы и декодированы с использованием MTF!")

# Пример использования для текстовых данных
text_data = "banana".encode('utf-8')
encoded_text = mtf.encode(text_data)
decoded_text = mtf.decode(encoded_text)

assert text_data == decoded_text
print("Текст успешно закодирован и декодирован с использованием MTF!")