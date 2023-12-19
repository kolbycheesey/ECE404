
from TcpAttack import *
import sys

#Your TcpAttack class should be named as TcpAttack
spoofIP='127.0.0.1' ; targetIP='172.16.52.184' #Will contain actual IP addresses in real script
print("Setup spoof and target")

#change around information for testing
rangeStart=1000 ; rangeEnd=1250 ; port=1236
print("Range has been set")

Tcp = TcpAttack(spoofIP,targetIP)
print("Class item set")
Tcp.scanTarget(rangeStart, rangeEnd)
print("Scan is done")

if Tcp.attackTarget(port,10):
    print("port was open to attack")
else:
    print("Wall of steel here on port: ", port)
