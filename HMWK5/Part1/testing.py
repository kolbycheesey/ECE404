import x931
from BitVector import *
v0 = BitVector(textstring='computersecurity')

dt = BitVector(intVal = 99, size = 128)
listX931 = x931.x931(v0,dt,3,'keyX931.txt')

#check print
print('{}\n{}\n{}'.format(int(listX931[0]),int(listX931[1]),int(listX931[2])))