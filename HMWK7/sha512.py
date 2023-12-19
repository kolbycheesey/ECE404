#!/usr/bin/env python 3.8
#Homework: 7
#Name: Michael Kolb
#ECN login:kolb3
#Due Date: 03/19/2021

import sys 
from BitVector import *
import warnings
warnings.filterwarnings(action="ignore")
import hashlib

#K values found on page 44 and 45 of lecture 15
K = ["428a2f98d728ae22", "7137449123ef65cd", "b5c0fbcfec4d3b2f",
     "e9b5dba58189dbbc", "3956c25bf348b538", "59f111f1b605d019",
     "923f82a4af194f9b", "ab1c5ed5da6d8118", "d807aa98a3030242",
     "12835b0145706fbe", "243185be4ee4b28c", "550c7dc3d5ffb4e2",
     "72be5d74f27b896f", "80deb1fe3b1696b1", "9bdc06a725c71235",
     "c19bf174cf692694", "e49b69c19ef14ad2", "efbe4786384f25e3",
     "0fc19dc68b8cd5b5", "240ca1cc77ac9c65", "2de92c6f592b0275",
     "4a7484aa6ea6e483", "5cb0a9dcbd41fbd4", "76f988da831153b5",
     "983e5152ee66dfab", "a831c66d2db43210", "b00327c898fb213f",
     "bf597fc7beef0ee4", "c6e00bf33da88fc2", "d5a79147930aa725",
     "06ca6351e003826f", "142929670a0e6e70", "27b70a8546d22ffc",
     "2e1b21385c26c926", "4d2c6dfc5ac42aed", "53380d139d95b3df",
     "650a73548baf63de", "766a0abb3c77b2a8", "81c2c92e47edaee6",
     "92722c851482353b", "a2bfe8a14cf10364", "a81a664bbc423001",
     "c24b8b70d0f89791", "c76c51a30654be30", "d192e819d6ef5218",
     "d69906245565a910", "f40e35855771202a", "106aa07032bbd1b8",
     "19a4c116b8d2d0c8", "1e376c085141ab53", "2748774cdf8eeb99",
     "34b0bcb5e19b48a8", "391c0cb3c5c95a63", "4ed8aa4ae3418acb",
     "5b9cca4f7763e373", "682e6ff3d6b2b8a3", "748f82ee5defb2fc",
     "78a5636f43172f60", "84c87814a1f0ab72", "8cc702081a6439ec",
     "90befffa23631e28", "a4506cebde82bde9", "bef9a3f7b2c67915",
     "c67178f2e372532b", "ca273eceea26619c", "d186b8c721c0c207",
     "eada7dd6cde0eb1e", "f57d4f7fee6ed178", "06f067aa72176fba",
     "0a637dc5a2c898a6", "113f9804bef90dae", "1b710b35131c471b",
     "28db77f523047d84", "32caab7b40c72493", "3c9ebe0a15c9bebc",
     "431d67c49c100d4c", "4cc5d4becb3e42b6", "597f299cfc657e2a",
     "5fcb6fab3ad6faec", "6c44198c4a475817"]


#need k to be a bitvector
Kbv = [BitVector(hexstring = value) for value in K]

def SHA512(filein):
    infile = open(filein, 'r')
    temp = infile.read()
    #print(temp)
    bv = BitVector(textstring = temp)

    #print(bv)

    infile.close


    #8 64 bit words found on page 43 of lecture 15
    h0 = BitVector(hexstring = '6a09e667f3bcc908')
    h1 = BitVector(hexstring = 'bb67ae8584caa73b')
    h2 = BitVector(hexstring = '3c6ef372fe94f82b')
    h3 = BitVector(hexstring = 'a54ff53a5f1d36f1')
    h4 = BitVector(hexstring = '510e527fade682d1')
    h5 = BitVector(hexstring = '9b05688c2b3e6c1f')
    h6 = BitVector(hexstring = '1f83d9abfb41bd6b')
    h7 = BitVector(hexstring = '5be0cd19137e2179')

    #step 1, padding
    lenbv = bv.length()
    #hold = BitVector(bitstring='1')
    #print(hold)
    bv1 = bv + BitVector(bitstring='1')
    #print(bv1)
    #bv += hold
    lenbv1 = bv1.length()
    numz = [0] * ((896 - lenbv1) % 1024)   #zero list
    bv2 = bv1 + BitVector(bitlist = numz)
    bv3 = BitVector(intVal = lenbv, size = 128)
    bv4 = bv2 + bv3
    #print("bv4: ", len(bv4))

    #intialize 80 words for storing message schedule 
    words = [None] * 80

    for i in range(0, bv4.length(), 1024):
        block = bv4[i:i+1024]
    
        #step 2, words 0-16 much like SHA256 but needs to be scaled up to 512

        words[0:16] = [block[n:n+64] for n in range(0,1024,64)]

        #expansion now
        for q in range(16,80):
            wone = words[q-2]
            wtwo = words[q-15]

            #page 44 in lecture 15
            sigma0 = (wtwo.deep_copy() >> 1) ^ (wtwo.deep_copy() >> 8) ^ (wtwo.deep_copy().shift_right(7))
            sigma1 = (wone.deep_copy() >> 19) ^ (wone.deep_copy() >> 61) ^ (wone.deep_copy().shift_right(6))

            #might need to change some variables around
            words[q] = BitVector(intVal = (int(words[q-16]) + int(sigma0) + int(words[q-7]) + int(sigma1)) & 0xFFFFFFFFFFFFFFFF, size = 64)
            #print(words[q])

        #step 3, round based processing
        a,b,c,d,e,f,g,h = h0,h1,h2,h3,h4,h5,h6,h7

        for p in range(0,80):
            #page 45 lecture 15
            ch = (e & f) ^ ((~e) & g)
            maj = (a & b) ^ (a & c) ^ (b & c)
            sum_a = ((a.deep_copy()) >> 28) ^ ((a.deep_copy()) >> 34) ^ ((a.deep_copy()) >> 39)
            sum_e = ((e.deep_copy()) >> 14) ^ ((e.deep_copy()) >> 18) ^ ((e.deep_copy()) >> 41)
            t1 = BitVector(intVal = (int(h) + int(ch) + int(sum_e) + int(words[p]) + int(Kbv[p])) & 0xFFFFFFFFFFFFFFFF, size = 64)
            t2 = BitVector(intVal = (int(sum_a) + int(maj)) & 0xFFFFFFFFFFFFFFFF, size = 64)

            h = g
            g = f
            f = e
            e = BitVector(intVal = (int(d) + int(t1)) & 0xFFFFFFFFFFFFFFFF, size=64)
            d = c
            c = b
            b = a
            a = BitVector(intVal = (int(t1) + int(t2)) & 0xFFFFFFFFFFFFFFFF, size=64)

        #step 4, copied and scaled from SHA256.py
        h0 = BitVector( intVal = (int(h0) + int(a)) & 0xFFFFFFFFFFFFFFFF, size=64 )
        h1 = BitVector( intVal = (int(h1) + int(b)) & 0xFFFFFFFFFFFFFFFF, size=64 )
        h2 = BitVector( intVal = (int(h2) + int(c)) & 0xFFFFFFFFFFFFFFFF, size=64 )
        h3 = BitVector( intVal = (int(h3) + int(d)) & 0xFFFFFFFFFFFFFFFF, size=64 )
        h4 = BitVector( intVal = (int(h4) + int(e)) & 0xFFFFFFFFFFFFFFFF, size=64 )
        h5 = BitVector( intVal = (int(h5) + int(f)) & 0xFFFFFFFFFFFFFFFF, size=64 )
        h6 = BitVector( intVal = (int(h6) + int(g)) & 0xFFFFFFFFFFFFFFFF, size=64 )
        h7 = BitVector( intVal = (int(h7) + int(h)) & 0xFFFFFFFFFFFFFFFF, size=64 )


    #create the hased message
    msghash = h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7
    #print(msghash)
    hashhex = msghash.getHexStringFromBitVector()

    return hashhex

#above code was adapated from the SHA256.py we were given from lecture 15 along with
#notes from lecture 15
if __name__ == '__main__':
    
    if len(sys.argv) != 3:
        sys.stderr.write("Need three args executable, input file and output file")
        sys.exit(1)

    filein = sys.argv[1]
    fileout = sys.argv[2]

    msg = SHA512(filein)
    outfile = open(fileout, 'w')
    outfile.write(msg)
    outfile.close
    infile = open(filein, 'r')
    comp = infile.read()
    if msg == hashlib.sha512(comp.encode('utf-8')).hexdigest():
        print("Ouput Matches!")
        print("Done!")
        infile.close
    else:
        print("There is an error check the output in: ", fileout)
        infile.close

