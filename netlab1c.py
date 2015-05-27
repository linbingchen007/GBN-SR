import socket
import netlib1
import re
import os
from netlib1 import getseq

PREFIX = ""
if os.name == 'nt':
    PREFIX = os.path.abspath(os.path.join(os.path.dirname(__file__))) + '\\'

UDP_IP = '0.0.0.0'
UDP_PORT = 88

revsock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
revsock.bind((UDP_IP, UDP_PORT))
lastack = 0
expseq = 0
revbuf = ''
while True:
        data, addr = revsock.recvfrom(1024)    
        seq = getseq(data)
        if seq == -2:
            revsock.sendto("ack:" + str(-2)+'\r\n\r\n', addr)  
            break   
        print 'expseq:'+str(expseq)
        print 'seq' + str(seq) 
        if seq != expseq:
            revsock.sendto("ack:" + str(lastack)+'\r\n\r\n', addr)
            continue
        print repr(data)
        #receive data and update the expseq and send ack pkt
        prefix = re.match(r'seq:[0-9]+\r\n\r\n',data).group(0)
        data = data[len(prefix):]
        pktlen = len(data)    
        revbuf += data
        revsock.sendto("ack:" + str(seq)+'\r\n\r\n', addr)
        #print seq
        lastack = seq
        expseq += pktlen


print "savename:",
savename = raw_input()
with open(os.name == 'nt' and PREFIX + savename or savename, 'wb') as f:
    f.write(revbuf)
    
