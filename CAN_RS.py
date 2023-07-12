# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 10:34:23 2016

@author: gubatenko
"""

import serial
import binascii
import time


def hex2bytes(string):
    return binascii.unhexlify(string.replace(' ', ''))

data = '55'

com = 'COM6'
with serial.Serial(com, baudrate=9600) as ser:
    while True:    
        ser.write(hex2bytes(data))
        time.sleep(1)