def bwt_encode(data):
    n = len(data)
    rotations = [data[i:] + data[:i] for i in range(n)]
    rotations_sorted = sorted(rotations)
    bwt_result = ''.join(row[-1] for row in rotations_sorted)
    original_index = rotations_sorted.index(data)
    return bwt_result, original_index


def bwt_decode(bwt_result, original_index):
    n = len(bwt_result)

    table = [''] * n

    for i in range(n):
        table = sorted([bwt_result[j] + table[j] for j in range(n)])

    # Исходная строка заканчивается символом '\0'
    return table[original_index]