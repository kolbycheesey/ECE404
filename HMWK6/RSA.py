
import sys
from BitVector import *
from PrimeGenerator import * 


e = 65537 #given by pdf
def encrypt(filein, key):
    array = []
    encrypt = []
    encrypted = []
    FILEIN = open(filein, 'r')
    bv = BitVector(filename = filename)
    size = filname.getsize()
    count = (size // 16) + 1
    for i in range(0,count):
        encrypt.append(bv.read_bits_from_file(128))
    if(len(encrypt[-1]) < 128):
        encrypt[-1] = encrypt.pad_from_right(len(encrypt) - 128)       ##might need to be len(encrypt) - 128
    #pad information to make 256
    for i in encrypt:
        i.pad_from_left(128)
    
    for i in encrypt:
        encrypted.appened(pow(i, e, key))

    print("encrypted: ",encrypted)        #sanity check
    return encrypted
    
        


#Standard GCD function but also found at geeksforgeeks.org
def gcd(a,b):
    if a == 0: return b;
    if b == 0: return a;
    if a == b: return a;

    if a > b:
        return gcd(a-b, b)
    return gcd(a, b-a)

def genp():
    #code got from prime generator.py
    num_of_bits_desired = 128 #int(sys.argv[1])                              
    generator = PrimeGenerator( bits = num_of_bits_desired )
    while(1):                 
        p_term = generator.findPrime()
        print("Prime returned p: %d" % p_term) #sanity check will want to comment out
        #check to make sure left most bit is 1
        lead = p_term >> 128
        if !lead: continue
        if(gcd(p_term - 1, e) == 1): break      #check gcd
    While(1):
        q_term = generator.findPrime()
        lead = q_term >> 128
        if p == q:
            #print("same number")
            continue
        if !lead: continue      #this should work I think
        if(gcd(p_term - 1, e) == 1): break       #check gcd
    print("Prime returned p: %d" % p_term) #sanity check will want to comment out
    print("Prime returned q: %d" % q_term) #sanity check will want to comment out
    return p, q 

def c_rem():

#this function is to help get the extra pieces I will need for the RSA algo
def helper(p,q):
    totient = (p-1) * (q-1)
    mod = p * q
    bv = BitVector(intVal = totient)
    newe = BitVector(intVal = e)
    multiinv = int(newe.multiplicative_inverse(mod))
    return multiiv, mod, totient


#Main function
if __name__ == '__main__':
    if(len(sys.argv) > 6):
        sys.exit('Wrong number of inputs')
    action = sys.argv[1]

    if(action == "-g"):
        file1 = sys.argv[2]
        file2 = sys.argv[3]
        p, q = gen()
        FILEOUT = open(file1, 'w')
        FILEOUT1 = open(fil2, 'w')
        FILEOUT.write(p)
        FILEOUT1.write(q)
        


    elif(action == "-e"):
        file1 = sys.argv[2]     #message.txt
        file2 = sys.argv[3]     #p
        file3 = sys.argv[4]     #q
        file4 = sys.argv[5]     #encrypted.txt
        ######################
        mi, mod, tot = helper(p,q) # maybe put this in each the decrypt and encrypt
        encrypted = encrypt(file1, mod)

        print("type encrypt: ",type(encrypted))
        FILEOUT = open(file4, 'w')
        for i in encrypted:
            enc_bv = Bitvector(intVal = i, size = 256)
            FILEOUT.write(enc_bv.get_bitvector_in_hex())
        print("FINISHED ENCRYPT")

    
    elif(action == "-d"):
        file1 = sys.argv[2]     #decrypted.txt
        file2 = sys.argv[3]     #p
        file3 = sys.argv[4]     #q
        file4 = sys.argv[5]     #decrypted.txt
