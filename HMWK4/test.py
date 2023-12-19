def row_shifting(input_block):
     # Form the state array as a list of bytes
    byte_array = [input_block[byte_index * 8:(byte_index + 1)* 8]for byte_index in range(16)]
    shift_block = BitVector(size=0)
# Compute the new columns after row shifting
    col_1 = byte_array[0] + byte_array[13] + byte_array[10] + byte_array[7]
    col_2 = byte_array[4] + byte_array[1] + byte_array[14] + byte_array[11]
    col_3 = byte_array[8] + byte_array[5] + byte_array[2] + byte_array[15]
    col_4 = byte_array[12] + byte_array[9] + byte_array[6] + byte_array[3]
 # Construct the shifted block
    shift_block += col_1 + col_2 + col_3 + col_4
    return shift_block