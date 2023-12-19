from AES_image import ctr_aes_image
from BitVector import *
import time

start_time = time.time()

iv = BitVector(textstring='computersecurity') #iv will be 128 bits
ctr_aes_image(iv,'image.ppm','enc_image1.ppm','keyCTR.txt')


print(" --- %s seconds to run ---",(time.time()-start_time))
