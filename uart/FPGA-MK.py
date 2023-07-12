# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 10:48:48 2017

@author: gubatenko
"""
from __future__ import division, print_function
import serial
import random
import binascii
import time

def hex2bytes(string):
    return binascii.unhexlify(string.replace(' ', ''))
    
def send_packet(ser, data):
    send = ''
    for d in data:
        send += "%0.2X " % d
    ser.write(hex2bytes(send))




with serial.Serial(port='COM16', 
                   baudrate=1800, 
                   bytesize=serial.EIGHTBITS, 
                   parity=serial.PARITY_EVEN, 
                   stopbits=serial.STOPBITS_ONE) as ser:

    
    print(ser)
    while 1:
        data_out = [random.randint(0, 255)]
        data_out = [0x55]        
        
        send_packet(ser, data_out)
        time.sleep(1)
        if ser.inWaiting() > 0:
            pass
            data_in = ser.read(ser.inWaiting())

#            if binascii.hexlify(str(data_in)) == '84c02b7db22624b18c78d874fbbc32d6':
#                print('GOOD')
#            else:
#                print(binascii.hexlify(str(data_in)))
        
            print(hex(data_out[0]), (binascii.hexlify(str(data_in))))
        else:
            print('empty')
        
