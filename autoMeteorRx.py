# v1.0 Meteor M-N2 automatic pass recording
# Written by Simon Kennedy, G0FCU, Copyright 2015,2016,2017
# v1.1 8th Nov 2015 - updated to also allow Meteor-M-N1 recording
# v1.2 1st Jan 2016 - updated to add active satellites flags
# v1.3 9th April 2017 - fixed bug that prevented termination of the gnuradioscript
import socket
import sys
import time
import subprocess
import os
import psutil

# set this variable to the minimum pass elevation you want to record
minrequiredel = 5
# set this variable to the elevation you want to start recording
minrisingel = 7
# set this variable to the elevation you want to stop recording
minsettingel = 7
# set this variable to the path to and the name of your gnuradio script for METEOR-M-1 >>>72k<<<
cmd2 = "/home/simon/Documents/Radio_Documents/LRPT_Decoder_Software/Software/meteor_qpsk_rx_hackrf_v5_M1_v2.py"
# >>>80k<<<
#cmd2 = "/home/simon/Documents/Radio_Documents/LRPT_Decoder_Software/Software/meteor_qpsk_rx_hackrf_v5_M1.py"
# set this variable to the path to and the name of your gnuradio script for METEOR-M-2
cmd3 = "/home/simon/Documents/Radio_Documents/LRPT_Decoder_Software/Software/meteor_qpsk_rx_hackrf_v5.py"
# set these variables to run Linux commands after the receiving program has been killed
POSTCMD1 = ""
POSTCMD2 = ""
POSTCMD3 = ""

#nextaos also means nextlos as predict returns one field for both (rather annoyingly)
UDP_IP = "localhost"
UDP_PORT = 1210

MESSAGE1 = "GET_SAT "
MESSAGE2 = "PREDICT "
SAT1 = "METEOR-M-1"
SAT1_ACTIVE = "N"
SAT2 = "METEOR-M-2"
SAT2_ACTIVE = "Y"
no_of_sats = 2
nextSAT1 = 9999999999
nextSAT2 = 9999999999

forever = 1
earlyend = 0
rxprogramrunning = 0
prevel = 99
nextSAT = ""
runningcmd = ""
lastSAT = ""

cmd1 = "python "

def maxele():
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    lastel = -1
    el = 0.1
    ele = 0
    notfirsttime = 0
    sock.sendto(MESSAGE2+nextSAT, (UDP_IP, UDP_PORT))
    while el > lastel:
      if notfirsttime == 1:
        lastel = el
      notfirsttime = 1
      data, addr = sock.recvfrom(73) 
      print "received message:", data
      if data[0][0] != "\x1a":
         ele = data.split(" ")[7]
         if ele == "":
            ele = data.split(" ")[6]
      el = int(ele)
      print "El:", el
    maxel = int(lastel)
    sock.close()
    return maxel

def getnextsat():
    if SAT1_ACTIVE == "Y":
        sock = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM) # UDP
        sock.sendto(MESSAGE1+SAT1, (UDP_IP, UDP_PORT))
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
#       print "received message:", data
        nextSAT1 = int(data.split("\n")[5])
        sock.close()
        print "NextSAT1 AOS/LOS:", nextSAT1
    else:
        nextSAT1 = 9999999999
    if SAT2_ACTIVE == "Y":
        sock = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM) # UDP
        sock.sendto(MESSAGE1+SAT2, (UDP_IP, UDP_PORT))
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
#       print "received message:", data
        nextSAT2 = int(data.split("\n")[5])
        sock.close()
        print "NextSAT2 AOS/LOS:", nextSAT2
    else:
        nextSAT2 = 9999999999
    if nextSAT1 < nextSAT2:
        nextSAT = SAT1
    else:
        nextSAT = SAT2
    print "nextSAT=", nextSAT
    return nextSAT

def getnextaos():
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.sendto(MESSAGE1+nextSAT, (UDP_IP, UDP_PORT))
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
#    print "received message:", data
    nextaos = int(data.split("\n")[5])
    sock.close()
#    print "getnextaos Next AOS/LOS:", nextaos
    return nextaos

def getcurrentel():
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.sendto(MESSAGE1+nextSAT, (UDP_IP, UDP_PORT))
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
#    print "received message:", data
    tempce = data.split("\n")[4]
#    print "tempce:", tempce, "Length:", len(tempce)
    currentel = abs(int(float(tempce)))
    sock.close()
#    print "Current El:", currentel
    return currentel

nextSAT = getnextsat()
nextaos = getnextaos()
lastaos = nextaos

if (SAT1_ACTIVE == "Y") and (SAT2_ACTIVE == "Y"):
    no_of_sats = 2
    
while forever:
    currenttime = int(time.time())
    print "Current time:", currenttime
    nextaos = getnextaos()
    print "Next AOS/LOS:", nextaos

#if aos has not been reached then sleep 60s before waking
#up to check again
    if currenttime < lastaos:
        print "Last AOS:", lastaos, " Sleep 60 seconds..." 
        time.sleep(60)
        if earlyend == 1:
           nextaos = getnextaos()
           print "Early end next AOS/LOS:", nextaos," Early end Last AOS:", lastaos 
           if nextaos > lastaos:
              print "in if statement"
              lastaos = nextaos
              earlyend = 0
    else:
        print "Last AOS:", lastaos
        print "Reset nextaos"
        lastaos = nextaos
# check if maximum elevation exceeds preset paramater
        maxel = maxele()
        print "Max El:", maxel, "Min el:", minrequiredel
# check max elevation of this pass to see if it exceeds
# minimum required elevation
        if minrequiredel <= maxel:
           prevel = 99
# run rx program
# not sure if this if statement is really required
           if rxprogramrunning == 0:
# only start recording when start elevation reached
               currentel = getcurrentel()
               while currentel < minrisingel:
                   currentel = getcurrentel()
                   if currentel != prevel:
                       print "Current El:", currentel, "Start recording at el:", minrisingel
                       prevel = currentel
               print "Call rx program"
               rxprogramrunning = 1
               if nextSAT == SAT1:
                   pid = subprocess.Popen(cmd1 + cmd2, shell=True).pid
                   runningcmd = cmd2
               else:
                   pid = subprocess.Popen(cmd1 + cmd3, shell=True).pid
                   runningcmd = cmd3
               print "Pid=", pid
        else:
            print "Not starting recording as max elevation of pass of ", maxel, "does not exceed min required elevation of ", minrequiredel         
            
        while currenttime + 1200 > nextaos:
            currenttime = int(time.time())
# call nextaos routine
            nextaos = getnextaos()
# stop recording if minimum setting elevation reached
            currentel = getcurrentel()
            if currentel != prevel:
                print "Current El:", currentel, "Stop recording at el:", minsettingel
                prevel = currentel
            if currentel < minsettingel:
# set flag to show the process was ended early
                earlyend = 1
                break
                
# kill pid as nextaos is now > 20 mins in the future
        print "Kill rx program"
        if rxprogramrunning == 1:
            for process in psutil.process_iter():
                if process.cmdline() == ['python', runningcmd]:
                   print('Process found. Terminating it.')
                   process.terminate()
                   if POSTCMD1 != "":
                      subprocess.call(POSTCMD1, shell=True)
                   if POSTCMD2 != "":
                      subprocess.call(POSTCMD2, shell=True) 
                   if POSTCMD3 != "":
                      subprocess.call(POSTCMD3, shell=True) 
                   break
        else:
            print('Process not running so will not try to kill it...')
        lastSAT = nextSAT
        while (rxprogramrunning == 1) and (no_of_sats > 1) and (lastSAT == nextSAT):
            if SAT1_ACTIVE == "N" or SAT2_ACTIVE == "N":
                break
            nextSAT = getnextsat()
            time.sleep(10)
            nextaos = getnextaos()
        rxprogramrunning = 0
#        print "before lastaos=nextaos:", lastaos, nextaos
        lastaos = nextaos
#        print "after lastaos=nextaos:", lastaos, nextaos
        lastel = 0
        el = 0.1
        notfirsttime = 0

    

    




