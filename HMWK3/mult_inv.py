#!/usr/bin/env python 3.9.1
#Homework 3
#Michael Kolb
#kolb3
#02/11/2021

## FindMI.py

#information was copied from FindMI.py however I believe that most of that code is gone now
#I do still have the system arguments and the print statements in here

import sys
NUM = 0
MOD = 0
#This function just divides two bit numbers if num = mod then it returns 1 if num < mod it returns 0
#otherwise it finds the number of times mod can go into num and returns that floored division number
def division(num, mod):

    ans = 0
    if(num == mod):
        remain = 0
        return 1
    elif num < mod:
        remain = num
        return 0

    while(mod <= num):
        num -= mod
        ans += 1

    return ans

#simple bitwise multiplication using leftshift instruction used geeks for geeks as a reference URL below
#https://www.geeksforgeeks.org/multiplication-two-numbers-shift-operator/
def multiply(x, y):
    p = 0
    i = 0
    while(y):
        if(y % 2 == 1):
            p += x << i;
        i += 1
        y = division(y,2)
        #y /= 2
    
    return p 

#grabbed intitially from FindMI then changed heavily so i still have print statements and variables but do all
#of my own work
def MI(num, mod):
   
    #NUM = num; MOD = mod done in main
    x, x_old = 0, 1
    y, y_old = 1, 0
    negx = 0
    negy = 0
    while mod:
        q = division(num,mod)
        #print('q: ',q)
        
        num, mod = mod, num % mod
        #print('num: ',num,'mod: ',mod)
        
        #temp = x
        #x = x_old - multiply(q, x)
        if negx:
            temp = x*-1
            x = x_old - (multiply(q, x)*-1)
        else:
            temp = x
            x = x_old - multiply(q, x)
        if x < 0:
            negx = 1
            x = abs(x)
        else:
            negx = 0
        x_old = temp
        #print('x: ',x,'x_old: ',x_old)
        
        #temp = y
        if negy:
            temp = y*-1
            y = y_old - (multiply(q, y)*-1)
        else:
            temp = y
            y = y_old - multiply(q, y)
        if y < 0:
            negy = 1
            y = abs(x)
        else:
            negy = 0
        y_old = temp 
        #print('y: ',y,'y_old: ',y_old)


    if num != 1:
        print("\nNO MI. However, the GCD of %d and %d is %u\n" % (NUM, MOD, num))
    else:
        MI = (x_old + MOD) % MOD
        print("\nMI of %d modulo %d is: %d\n" % (NUM, MOD, MI))


if __name__ == "__main__":
    if len(sys.argv) != 3:  
        sys.stderr.write("Usage: %s   <integer>   <modulus>\n" % sys.argv[0]) 
        sys.exit(1) 

    NUM, MOD = int(sys.argv[1]), int(sys.argv[2])
    MI(NUM, MOD)