# -*- coding: utf-8 -*-
"""
Created on Mon Oct 03 15:47:27 2016

@author: zhirnov
"""
from __future__ import division, print_function

def CheckKontron(local_ip = "192.168.208.101", local_port = 2000, remote_ip = "192.168.208.100", remote_port = 2000):
    """
        Sends data "PCI0:TEST?\n"
        Returns True in case of valid Kontron acknolegement
    """
    
    import socket
    import binascii
    from datetime import datetime

    data = "PCI0:TEST?\n"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3.0)
    try:
        sock.connect((remote_ip, remote_port))
        sock.sendto(data, (remote_ip, remote_port))
        print("sent " + str(datetime.now()) + " " + data)
        #binascii.hexlify(data)
        ack_pack = bytearray(sock.recv(64))
    except socket.timeout:
        ack_pack = 0
    except socket.error, e:
        ack_pack = 0
        sock.close()
        pass
        #raise e
    sock.close()
    if (ack_pack != 0):
        print("recv " + str(datetime.now()) + " " + ack_pack)
        #binascii.hexlify(ack_pack)

    return bool(ack_pack)

if __name__ == '__main__':

    print("Result: %d" % CheckKontron(local_ip = "localhost", local_port = 2000, remote_ip = "localhost", remote_port = 2001))




