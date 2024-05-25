
def rle_encode(data, element_size):
    encoding = bytearray()
    prev_element = data[:element_size]
    count = 1

    for i in range(element_size, len(data), element_size):
        element = data[i:i + element_size]
        if element == prev_element and count < 255:
            count += 1
        else:
            encoding.append(count)
            encoding.extend(prev_element)
            prev_element = element
            count = 1

    encoding.append(count)
    encoding.extend(prev_element)

    return bytes(encoding)


def rle_decode(data, element_size):
    decoding = bytearray()

    for i in range(0, len(data), element_size + 1):
        count = data[i]
        element = data[i + 1:i + 1 + element_size]
        decoding.extend(element * count)

    return bytes(decoding)



# - Если встречается последовательность повторяющихся элементов, она кодируется как [count, элемент].
# - Если встречается последовательность уникальных элементов, она кодируется как
# [0, длина уникальной последовательности, сами уникальные элементы].
def rle_encode_full(data, element_size):
    encoding = bytearray()
    i = 0
    data_len = len(data)

    while i < data_len:
        run_length = 1
        while (i + run_length * element_size < data_len and
               data[i:i + element_size] == data[i + run_length * element_size:i + (run_length + 1) * element_size] and
               run_length < 255):
            run_length += 1

        if run_length > 1:
            encoding.append(run_length)
            encoding.extend(data[i:i + element_size])
            i += run_length * element_size
        else:
            unique_start = i
            unique_length = 0
            while (i + element_size < data_len and
                   (i + element_size >= data_len or data[i:i + element_size] != data[i + element_size:i + 2 * element_size]) and
                   unique_length < 255):
                unique_length += 1
                i += element_size

            encoding.append(0)
            encoding.append(unique_length)
            encoding.extend(data[unique_start:unique_start + unique_length * element_size])

    return bytes(encoding)


def rle_decode_full(data, element_size):
    decoding = bytearray()
    i = 0
    data_len = len(data)

    while i < data_len:
        count = data[i]
        i += 1

        if count > 0:
            element = data[i:i + element_size]
            decoding.extend(element * count)
            i += element_size
        else:
            unique_length = data[i]
            i += 1
            decoding.extend(data[i:i + unique_length * element_size])
            i += unique_length * element_size

    return bytes(decoding)