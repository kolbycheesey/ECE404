##Pulled from lecture code examples uysed for assistance

#!/usr/bin/env python

###  DecryptForFun.py
###  Avi Kak  (kak@purdue.edu)
###  January 21, 2014, modified January 11, 2016

import sys
from BitVector import *                                                     #(A)

if len(sys.argv) is not 3:                                                  #(B)
    sys.exit('''Needs two command-line arguments, one for '''
             '''the encrypted file and the other for the '''
             '''decrypted output file''')

PassPhrase = "Hopes and dreams of a million years"                          #(C)

BLOCKSIZE = 16                                                              #(D)
numbytes = BLOCKSIZE // 8                                                   #(E)

# Reduce the passphrase to a bit array of size BLOCKSIZE:
bv_iv = BitVector(bitlist = [0]*BLOCKSIZE)                                  #(F)
for i in range(0,len(PassPhrase) // numbytes):                              #(G)
    textstr = PassPhrase[i*numbytes:(i+1)*numbytes]                         #(H)
    bv_iv ^= BitVector( textstring = textstr )                              #(I)

# Create a bitvector from the ciphertext hex string:
FILEIN = open(sys.argv[1])                                                  #(J)
encrypted_bv = BitVector( hexstring = FILEIN.read() )                       #(K)

# Get key from user: this is the brute force method
key = None
if sys.version_info[0] == 3:                                                #(L)
    key = input("\nEnter key: ")                                            #(M)
else:
    key = raw_input("\nEnter key: ")                                        #(N)
key = key.strip()                                                           #(O)

# Reduce the key to a bit array of size BLOCKSIZE:
key_bv = BitVector(bitlist = [0]*BLOCKSIZE)                                 #(P)
for i in range(0,len(key) // numbytes):                                     #(Q)
    keyblock = key[i*numbytes:(i+1)*numbytes]                               #(R)
    key_bv ^= BitVector( textstring = keyblock )                            #(S)

# Create a bitvector for storing the decrypted plaintext bit array:
msg_decrypted_bv = BitVector( size = 0 )                                    #(T)

# Carry out differential XORing of bit blocks and decryption:
previous_decrypted_block = bv_iv                                            #(U)
for i in range(0, len(encrypted_bv) // BLOCKSIZE):                          #(V)
    bv = encrypted_bv[i*BLOCKSIZE:(i+1)*BLOCKSIZE]                          #(W)
    temp = bv.deep_copy()                                                   #(X)
    bv ^=  previous_decrypted_block                                         #(Y)
    previous_decrypted_block = temp                                         #(Z)
    bv ^=  key_bv                                                           #(a)
    msg_decrypted_bv += bv                                                  #(b)

# Extract plaintext from the decrypted bitvector:
outputtext = msg_decrypted_bv.get_text_from_bitvector()                     #(c)

# Write plaintext to the output file:
FILEOUT = open(sys.argv[2], 'w')                                            #(d)
FILEOUT.write(outputtext)                                                   #(e)
FILEOUT.close()                                                             #(f)
