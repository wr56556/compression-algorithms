def bwt_encode(data, type=None):
    if type != "img":
        data = data.encode('utf-8')  # Преобразуем строку в байты
    n = len(data)
    # Создаем список индексов и сортируем их по соответствующим вращениям строки
    sorted_indices = sorted(range(n), key=lambda i: data[i:] + data[:i])
    bwt_result = bytearray(n)

    for i, idx in enumerate(sorted_indices):
        bwt_result[i] = data[idx - 1]

    original_index = sorted_indices.index(0)
    return bytes(bwt_result), original_index


def bwt_decode(bwt_result, original_index, type=None):
    n = len(bwt_result)
    count = [0] * 256
    rank = [0] * n

    # Подсчитываем количество каждого символа
    for byte in bwt_result:
        count[byte] += 1

    # Вычисляем позиции каждого символа
    total = 0
    for i in range(256):
        count[i], total = total, total + count[i]

    # Заполняем rank
    for i in range(n):
        byte = bwt_result[i]
        rank[i] = count[byte]
        count[byte] += 1

    # Восстанавливаем исходную строку
    decoded = bytearray(n)
    current_index = original_index
    for i in range(n-1, -1, -1):
        decoded[i] = bwt_result[current_index]
        current_index = rank[current_index]

    if type != "img":
        return decoded.decode('utf-8')  # Преобразуем байты обратно в строку
    else:
        return decoded

