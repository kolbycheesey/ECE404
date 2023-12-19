#!/bin/sh
#Homework Number: 09
#Name: Michael Kolb
#ECN Login: kolb3
#Due Date: 04/06/2021

#remove all rules or chains
iptables -t filter -F       #flush
iptables -t filter -X       #delete
iptables -t nat -F
iptables -t nat -X

iptables -A INPUT -p all -i lo -j ACCEPT        #used in the lecture, accepts all locally generated packets

#for all outgoing packets change their source IP to my own machine
modprobe ip_nat_ftp
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
#iptables -t nat -A POSTROUTING -s eth0 -j SNAT
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j DNAT --to-destination 192.128.232.130

#echo after prerouting

#block all new packets coming from yahoo.com
iptables -A INPUT -s yahoo.com -j DROP 

#block computer from being pinged by all other hosts (ping uses icmp echo)
iptables -A  INPUT -p icmp --icmp-type echo-request -j REJECT --reject-with icmp-host-prohibited #want to see the print statements also not sure if 'all' is needed, didnt need all

#echo after pinging

#setup port-forward from unused port of my choice to port 22 (may have to enable connections on the unused port)
iptables -t nat -A PREROUTING -p tcp --dport 1236 -j DNAT --to-destination 192.128.232.130:22
iptables -A FORWARD -p tcp --dport 22 -j ACCEPT

#echo after port-forward

#Allow ssh access, port 22, to my machine from only engineering.purdue.edu domain
iptables -A INPUT -p tcp ! -s engineering.purdue.edu --dport 22 -j DROP

#echo engineering.purdue.edu

#assumption: running httpd server on my machine that can make entire home directory available to the outside world
#rule to prevent DoS attacks by limiting connection requests to 30 per min after 60 connections have been made
#if [(iptables -A INPUT -p icmp --icmp-type echo-request -m connlimit --connlimit-above 60)]
#    then
iptables -A INPUT -p tcp -d 192.128.232.130 --dport 80 --syn -m connlimit --connlimit-above 60  -m limit --limit 30/min -j ACCEPT      #believe this will only allow a connection every 2 seconds
#    fi
#apparentally an if statement doesn't work like that

#drop any other packets if they are not caught by the above rules
iptables -A INPUT -p all -j REJECT --reject-with icmp-host-prohibited      #want printable statements at this time might remove for turn in
