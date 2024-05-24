
def lz77_encode(data, window_size=20):
    i = 0
    output_buffer = []

    while i < len(data):
        match = (-1, -1)
        for j in range(max(0, i - window_size), i):
            k = 0
            while (i + k < len(data)) and (data[j + k] == data[i + k]):
                k += 1
            if k > match[1]:
                match = (i - j, k)

        if match[1] > 0:
            output_buffer.append((match[0], match[1], data[i + match[1]] if i + match[1] < len(data) else None))
            i += match[1] + 1
        else:
            output_buffer.append((0, 0, data[i]))
            i += 1

    return output_buffer


def lz77_decode(data):
    output_buffer = bytearray()

    for item in data:
        offset, length, next_char = item
        if offset == 0 and length == 0:
            output_buffer.append(next_char)
        else:
            start = len(output_buffer) - offset
            for _ in range(length):
                output_buffer.append(output_buffer[start])
                start += 1
            if next_char is not None:
                output_buffer.append(next_char)

    return bytes(output_buffer)
