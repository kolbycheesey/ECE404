#!/usr/bin/env python 3.7.4

import sys
from BitVector import *

BLOCKSIZE = 16
numbytes = BLOCKSIZE // 8 # total number of bytes this should not change ever other than blocksize changes
PassPhrase = "Hopes and dreams of a million years"

#bv_iv = BitVector(bitlist = [0]*BLOCKSIZE)                                  #(F)
#for i in range(0,len(PassPhrase) // numbytes):                              #(G)
#    textstr = PassPhrase[i*numbytes:(i+1)*numbytes]                         #(H)
#    bv_iv ^= BitVector( textstring = textstr )

#FILEIN = open('encrypted.txt')
#encrypted_bv = BitVector( hexstring = FILEIN.read() )
#needed inside cryptBreak function
#print(encrypted_bv)    ## this is good

#msg_decrypted_bv = BitVector( size = 0 )

#previous_decrypted_block = bv_iv
#print(previous_decrypted_block) #this works

#Most of this function has been adapted from decrypt for fun will explain next to each line
#what it does
def cryptBreak(ciphertextFile,key_bv):
    msg_decrypted_bv = BitVector( size = 0 )                #this creates bitvector size 0
    FILEIN = open(ciphertextFile)                           #opens file with name given to ciphertextFile
    encrypted_bv = BitVector( hexstring = FILEIN.read() )   #converts encrypted files to hexstring
    bv_iv = BitVector(bitlist = [0]*BLOCKSIZE)              #bit vector  of size blocksize
    for i in range(0,len(PassPhrase) // numbytes):          #iterates through files text
        textstr = PassPhrase[i*numbytes:(i+1)*numbytes]     #breaks the text into strings
        bv_iv ^= BitVector( textstring = textstr )          #converts the string to be messed with further

    previous_decrypted_block = bv_iv                        #storage location for decrypted block

    for i in range(0, len(encrypted_bv) // BLOCKSIZE):
        bv = encrypted_bv[i*BLOCKSIZE:(i+1)*BLOCKSIZE]      #iterates through txt and looks at one blocksize at a time
        temp = bv.deep_copy()                               #deep copy it from BitVector
        bv ^= previous_decrypted_block                      #XORing
        previous_decrypted_block = temp
        bv ^= key_bv
        msg_decrypted_bv += bv
        #out = msg_decrypted_bv.get_text_from_bitvector()

    FILEIN.close()

    return msg_decrypted_bv.get_text_from_bitvector()       #exchange bitvetor to text return
    #return out

def check(decryptedMessage):
    if 'Yogi Berra' in decryptedMessage:
        print('Encryption Broken!')
        return 0
    else:
        print('Not decrypted yet')
        return 1


if __name__ == '__main__':
    filename = 'encrypted.txt'
    decryptedMessage = ''
    key = -1
    for k in range(0, 2**BLOCKSIZE):
        key_bv = BitVector(intVal=k, size=16)              #create bitvector given two inputs one being blocksize other being key
        #for i in range(0,len(key) // numbytes):
        #    keyblock = key[i*numbytes:(i+1)*numbytes]
        #    key_bv ^= BitVector( textstring = keyblock )

        decryptedMessage = cryptBreak(filename, key_bv)  #function returns the key
        #print(decryptedMessage)
        ans = check(decryptedMessage)                       #checks to make sure what we want is in there
        if(ans == 0):
            key = k
            break
    if(key != -1):
        print('Key: ', key)
        #print('The message converted is: ')
        #print(decryptedMessage)
        FILEOUT = open('solution.txt', 'w')
        FILEOUT.write(decryptedMessage)
        FILEOUT.close()
    else:
        print('You were unable to Decrypt this text, better luck next time')
