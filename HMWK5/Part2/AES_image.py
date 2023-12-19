#!/usr/bin/env python 3.8
#Homework: 4
#Name: Michael Kolb
#ECN login:kolb3
#Due Date: 03/02/2021

import sys
from BitVector import*


AES_modulus = BitVector(bitstring='100011011')

a = BitVector(hexstring = '01')
b = BitVector(hexstring = '02')
c = BitVector(hexstring = '03')

#gen_tables.py
subBytesTable = []

#Arguments:
# iv: 128-bit initialization vector
# image_file: input .ppm image file name
# out_file: encrypted .ppm image file name
# key_file: String of file name containing encryption key (in ASCII)
#Function Descrption:
# Encrypts image_file using CTR mode AES and writes said file to out_file. No required return value.



def ctr_aes_image(iv,image_file,out_file, key_file):
    FILEOUT = open(out_file, 'wb')
    bv = BitVector( filename = image_file)
    count = 0
    gen_subbytes_table()
    while count < 3:
        bitvec = bv.read_bits_from_file(8)
        if(bitvec.int_val() == 10):
            count += 1
            bitvec.write_to_file(FILEOUT)
        else:
            bitvec.write_to_file(FILEOUT)
    count = 0
    while(bv.more_to_read):
        bitvec = bv.read_bits_from_file(128)
        if len(bitvec) < 128:
                hold = BitVector(intVal = 0, size = 128 - len(bitvec))
                bitvec += hold

        blockEncrypt = encrypt(iv, key_file)
        ciphertext = blockEncrypt ^ bitvec
        ciphertext.write_to_file(FILEOUT)
        increment = iv.int_val()
        increment += 1
        iv = BitVector(intVal = increment, size = 128)
        print("santiy check: ", count)
        count += 1
    
#def encrypt(file_in_name, keytxt,file_out_name):
def encrypt(bv, keytxt):#,file_out_name):
    #basically DES encrypt function goes here
    key, keysize = get_encryption_key(keytxt)  #key is already a bv from get_encryption_key
    #gen_subbytes_table()
    round_keys, key_words, numRounds = start(key, keysize)
    #print("round: ",round_keys[0],"\n\n")

    #roundCount = 0
    #FILEOUT = open(file_out_name, 'w')
    outmessage = []
    #bv = BitVector( filename = file_in_name)
    size = bv.size
    #print(size)
    count = 0
    #while(bv.more_to_read):
    while(count < size):
        bitvec = bv[count:count+128]
        count += 128
        if len(bitvec) < 128:
            hold = BitVector(intVal = 0, size = 128-len(bitvec))
            bitvec = bitvec + hold

        #print(type(round_keys))

        state_array = gen_state_array(bitvec)
        #print(state_array)
        state_array = xorRoundKey(round_keys[0], state_array) ##round_key[0]
        #print(state_array)
        state_array = gen_state_array(state_array)
        
        for x in range(numRounds):
            #print("stateA: ",state_array),"\n")
            out1 = subBytes(state_array)
            out2 = shiftRows(out1)
            if x != (numRounds - 1):
                out3 = mixCols(out2)
                out4 = xorRoundKey(round_keys[x+1], out3)
            else:
                out4 = xorRoundKey(round_keys[x+1], out2)
        
            state_array = gen_state_array(out4)            
        
        #print(state_array,"\n\n")
        for t in range(4):
            for i in range(4):
                #FILEOUT.write(state_array[t][i].get_bitvector_in_hex())
                outmessage += state_array[t][i] 
    #print(outmessage)
    outmessage = BitVector( bitstring = outmessage)
    #FILEOUT.close
    return outmessage



def start(key_bv, keysize):
    key_words = []
    #keysize, key_bv = get_key(keytxt) ## should change
    if keysize == 128:    
        key_words = gen_key_schedule_128(key_bv)
    elif keysize == 192:    
        key_words = gen_key_schedule_192(key_bv)
    elif keysize == 256:    
        key_words = gen_key_schedule_256(key_bv)
    else:
        sys.exit("wrong keysize --- aborting")
    key_schedule = []
    #print("\nEach 32-bit word of the key schedule is shown as a sequence of 4 one-byte integers:")
    for word_index,word in enumerate(key_words):
        keyword_in_ints = []
        for i in range(4):
            keyword_in_ints.append(word[i*8:i*8+8].intValue())
    #    if word_index % 4 == 0: print("\n")
    #    print("word %d:  %s" % (word_index, str(keyword_in_ints)))
        key_schedule.append(keyword_in_ints)
    num_rounds = None
    if keysize == 128: num_rounds = 10
    if keysize == 192: num_rounds = 12
    if keysize == 256: num_rounds = 14
    #print("num_rounds: " , num_rounds)
    round_keys = [None for i in range(num_rounds+1)]
    for i in range(num_rounds+1):
        round_keys[i] = (key_words[i*4] + key_words[i*4+1] + key_words[i*4+2] + key_words[i*4+3])    
    #print("\n\nRound keys in hex (first key for input block):\n")
    #for round_key in round_keys:
    #    print(round_key)
    
    return(round_keys,key_words,num_rounds)

#Generate state array
def gen_state_array(bitvec):
    sArray = [[0 for x in range(4)] for y in range(4)]

    for i in range(4):
        for j in range(4):
            sArray[i][j] = bitvec[32*i + 8*j: 32*i + 8*(j+1)]  #page 5 of lecture 8
    return sArray

def subBytes(stateArray):
    for x in range(4):
        for y in range(4):
            stateArray[x][y] = BitVector(intVal=subBytesTable[int(stateArray[x][y])], size=8)
        
    return stateArray

#update to make sure that shiftrows is working, did some looking around stack overflow and some testing
def rotate(array,n): 
    return array[n:] + array[:n]

#copied and altered from generate_round_kkeys.py
def get_encryption_key(keytxt):
    key = ""
    FILEIN = open(keytxt)
    #gathered from gen_encryption_key.py will change to work with my script
    key = FILEIN.read()

    #if len(key) != 8:
    #    print("\nKey generation needs 8 characters exactly.  Try again.\n")

    key = BitVector(textstring = key)
    keysize = len(key)          ##might consider changing to just /8 instead of floor divide
    #print("keysize: ",keysize, key) ## check
    FILEIN.close
    return key, keysize

def shiftRows(stateArray):
    trans = [list(x) for x in zip(*stateArray)]
    for n in range(4):
        trans[n] = rotate(trans[n], n)
    fixTrans = [list(x) for x in zip(*trans)] ## is rows trans if so remove
    #print(trans)
    return fixTrans

def mixCols(stateArray):
    finalArray =[[0 for x in range(4)] for y in range(4)]
    n = 8
    transposed = [list(x) for x in zip(*stateArray)]

    for x in range(4):
        if x == 0:
            for j in range(4):
                finalArray[x][j] = (b.gf_multiply_modular(transposed[0][j], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[1][j], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[2][j], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[3][j], AES_modulus, n))
        if x == 1:
            for i in range(4):
                finalArray[x][i] = (a.gf_multiply_modular(transposed[0][i], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[1][i], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[2][i], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[3][i], AES_modulus, n))
        if x == 2:
            for t in range(4):
                finalArray[x][t] = (a.gf_multiply_modular(transposed[0][t], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[1][t], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[2][t], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[3][t], AES_modulus, n))
        if x == 3:
            for p in range(4):
                finalArray[i][p] = (c.gf_multiply_modular(transposed[0][p], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[1][p], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[2][p], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[3][p], AES_modulus, n))
    revert = [list(y) for y in zip(*finalArray)]
    return revert

    def gee(keyword, round_constant, subBytesTable):
        rotated_word = keyword.deep_copy()
    rotated_word << 8
    newword = BitVector(size = 0)
    for i in range(4):
        newword += BitVector(intVal = subBytesTable[rotated_word[8*i:8*i+8].intValue()], size = 8)
    newword[:8] ^= round_constant
    round_constant = round_constant.gf_multiply_modular(BitVector(intVal = 0x02), AES_modulus, 8)
    return newword, round_constant

def gee(keyword, round_constant, subBytesTable):
    rotated_word = keyword.deep_copy()
    rotated_word << 8
    newword = BitVector(size = 0)
    for i in range(4):
        newword += BitVector(intVal = subBytesTable[rotated_word[8*i:8*i+8].intValue()], size = 8)
    newword[:8] ^= round_constant
    round_constant = round_constant.gf_multiply_modular(BitVector(intVal = 0x02), AES_modulus, 8)
    return newword, round_constant

def gen_key_schedule_128(key_bv):
    #byte_sub_table = gen_subbytes_table()
    #  We need 44 keywords in the key schedule for 128 bit AES.  Each keyword is 32-bits
    #  wide. The 128-bit AES uses the first four keywords to xor the input block with.
    #  Subsequently, each of the 10 rounds uses 4 keywords from the key schedule. We will
    #  store all 44 keywords in the following list:
    key_words = [None for i in range(44)]
    round_constant = BitVector(intVal = 0x01, size=8)
    for i in range(4):
        key_words[i] = key_bv[i*32 : i*32 + 32]
    for i in range(4,44):
        if i%4 == 0:
            kwd, round_constant = gee(key_words[i-1], round_constant, subBytesTable)
            key_words[i] = key_words[i-4] ^ kwd
        else:
            key_words[i] = key_words[i-4] ^ key_words[i-1]
    return key_words

def gen_key_schedule_192(key_bv):
    #byte_sub_table = gen_subbytes_table()
    #  We need 52 keywords (each keyword consists of 32 bits) in the key schedule for
    #  192 bit AES.  The 192-bit AES uses the first four keywords to xor the input
    #  block with.  Subsequently, each of the 12 rounds uses 4 keywords from the key
    #  schedule. We will store all 52 keywords in the following list:
    key_words = [None for i in range(52)]
    round_constant = BitVector(intVal = 0x01, size=8)
    for i in range(6):
        key_words[i] = key_bv[i*32 : i*32 + 32]
    for i in range(6,52):
        if i%6 == 0:
            kwd, round_constant = gee(key_words[i-1], round_constant, subBytesTable)
            key_words[i] = key_words[i-6] ^ kwd
        else:
            key_words[i] = key_words[i-6] ^ key_words[i-1]
    return key_words

def gen_key_schedule_256(key_bv):
    #byte_sub_table = gen_subbytes_table()
    #  We need 60 keywords (each keyword consists of 32 bits) in the key schedule for
    #  256 bit AES. The 256-bit AES uses the first four keywords to xor the input
    #  block with.  Subsequently, each of the 14 rounds uses 4 keywords from the key
    #  schedule. We will store all 60 keywords in the following list:
    key_words = [None for i in range(60)]
    round_constant = BitVector(intVal = 0x01, size=8)
    #print(subBytesTable) why is this empty
    for i in range(8):
        key_words[i] = key_bv[i*32 : i*32 + 32]
    for i in range(8,60):
        if i%8 == 0:
            kwd, round_constant = gee(key_words[i-1], round_constant, subBytesTable)
            key_words[i] = key_words[i-8] ^ kwd
        elif (i - (i//8)*8) < 4:
            key_words[i] = key_words[i-8] ^ key_words[i-1]
        elif (i - (i//8)*8) == 4:
            key_words[i] = BitVector(size = 0)
            for j in range(4):
                key_words[i] += BitVector(intVal = 
                                 subBytesTable[key_words[i-1][8*j:8*j+8].intValue()], size = 8)
            key_words[i] ^= key_words[i-8] 
        elif ((i - (i//8)*8) > 4) and ((i - (i//8)*8) < 8):
            key_words[i] = key_words[i-8] ^ key_words[i-1]
        else:
            sys.exit("error in key scheduling algo for i = %d" % i)
    return key_words

def gen_subbytes_table():
    hold = BitVector(bitstring='01100011')
    for i in range(0, 256):
        q = BitVector(intVal = i, size=8).gf_MI(AES_modulus, 8) if i != 0 else BitVector(intVal=0)
        q1,q2,q3,q4 = [q.deep_copy() for x in range(4)]
        q ^= (q1 >> 4) ^ (q2 >> 5) ^ (q3 >> 6) ^ (q4 >> 7) ^ hold
        subBytesTable.append(int(q))
    #return subBytesTable    

def xorRoundKey(round_key, state_array):
    tempKey = BitVector(size = 0)
    #print(type(tempKey))
    for x in range(4):
        for y in range(4):
            tempKey += state_array[x][y]

    #print(type(tempKey))
    #print("temp: ",tempKey)
    #print("\nround:",round_key)
    tempKey ^= round_key
    return tempKey