def bwt_encode(data):
    n = len(data)
    rotations = [data[i:] + data[:i] for i in range(n)]
    rotations_sorted = sorted(rotations)
    bwt_result = ''.join(row[-1] for row in rotations_sorted)
    original_index = rotations_sorted.index(data)
    return bwt_result, original_index


def bwt_decode(bwt_result, original_index):
    n = len(bwt_result)

    # Initialize table with empty strings
    table = [''] * n

    for i in range(n):
        # Add the BWT result as a new column to the table
        table = sorted([bwt_result[j] + table[j] for j in range(n)])

    # The original string is the one that ends with the special end character (e.g., '\0')
    return table[original_index]