import socket
from netlib1 import getseq
import os
import random
import threading
import re
import sys




destaddr_tuple = [0,0]
wait_for_conc_fg = True

def server_run():
    UDP_IP = '0.0.0.0'
    UDP_PORT = 6195
    revsock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    revsock.bind((UDP_IP, UDP_PORT))
    revsock.settimeout(120)
    expackseq = 0
    #revbuf = ''
    while True:
            try:
                data, addr = revsock.recvfrom(1024)   
                global wait_for_conc_fg
                if wait_for_conc_fg :
                    print addr[0]+' is connecting.'
                    wait_for_conc_fg = False

                seq = getseq(data)   
                if seq != expackseq:
                    revsock.sendto("ack:" + str(expackseq)+'\r\n\r\n', addr)
                    print "send ack:" + str(expackseq)
                    continue
                print repr(data)
                #receive data and update the expackseq and send ack pkt
                prefix = re.match(r'seq:[0-9]+\r\n\r\n',data).group(0)
                data = data[len(prefix):]
                pktlen = len(data)    
                #revbuf += data
                revsock.sendto("ack:" + str(seq)+'\r\n\r\n', addr)
                #print seq
                expackseq += pktlen
            except socket.timeout:
                print 'recv thread was closed'
                revsock.close()
                break


def client_run():
    sdsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sdsocket.settimeout(0.5)
    expseq = 0
    #print "filename:",
    #user_input=raw_input()
    dest = (destaddr_tuple[0], destaddr_tuple[1])
    while user_input:
        print expseq
        pktlen =  len(user_input)
        user_input = 'seq:'+str(expseq)+'\r\n\r\n'+user_input
        if random.randint(0,5)!=0:
            sdsocket.sendto(user_input, dest)    
        acknowledged = False
        seqchgfg = False
        while not acknowledged:
            try:
                ACK, address = sdsocket.recvfrom(1024)
                #print ACK
                crevseq=getseq(ACK) 
                #print crevseq
                #print expseq
                if crevseq==expseq:
                    acknowledged=True
            except socket.timeout:
                print 'timeout'
                if random.randint(0,5)!=0:
                    sdsocket.sendto(user_input, dest)
        expseq += pktlen
        print repr(ACK)
        user_input = raw_input()
    sdsocket.close()

PREFIX = ""
PKTFIXEDLEN = 512

#wait_for_conc_fg = True
if len(sys.argv) == 3:
    destaddr_tuple[0] = sys.argv[1]
    destaddr_tuple[1] = int(sys.argv[2])
    client_run()
else:
    print 'waiting for connection'
    server_run()






