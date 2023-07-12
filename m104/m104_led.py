# -*- coding: utf-8 -*-
from __future__ import division, print_function
import serial
import collections as coll
import binascii
import threading
import time



# Изменить значение PORT при необходимости
PORT = 'COM16'




rcv = coll.deque()
run = True
mbx_232 = coll.deque()

def hex2bytes(string):
    return binascii.unhexlify(string.replace(' ', ''))

def inq(ser, mbx):
    while run:
        if ser.inWaiting() > 0:
            dat = ser.read(ser.inWaiting())
            chunk = coll.deque([int(binascii.hexlify(dat[i]), 16)
                                for i in xrange(len(dat))])
            while True:
                try:
                    mbx.append(chunk.popleft())
                except IndexError:
                    break


def inq_switch(mbx, channel):
    rx_cnt = 0
    packet_in_progress = False
    packet = coll.deque()
    while run:
        if mbx:
            rx_byte = mbx.popleft()
            if not packet_in_progress:
                if (rx_byte == 0xC0):
                    rx_cnt = 1
                    packet.append(rx_byte)
                    packet_in_progress = True
            else:
                packet.append(rx_byte)
                rx_cnt += 1
                if rx_cnt == 3:
                    rcv.append(packet)
                    rx_cnt = 0
                    packet_in_progress = False
                    packet = coll.deque()


def sender(ser):
    brt = 1000
    dbrt = 1
    while 1:
        brt += dbrt
        if brt >= 1023:
            dbrt = -dbrt
        if brt <= 0:
            dbrt = -dbrt

        brt_l = brt & 0xFF
        brt_h = (brt & 0xFF00) >> 8
        send = 'C0 10 %02X %02X' % (brt_l, brt_h)
        ser.write(hex2bytes(send))
        time.sleep(0.003)
        print(brt)
    

def main():
    global run
    try:
        print(chr(12))
        with serial.Serial(PORT, baudrate=19200) as ser:
            th1 = threading.Thread(name='th_rs232', target=inq, args=(ser, mbx_232))
            th2 = threading.Thread(name='th_sw', target=inq_switch, args=(mbx_232, '232'))
            th3 = threading.Thread(name='th_cd', target=sender, args=(ser,))
            th1.start()
            th2.start()            
            th3.start()            
            while 1:
                pass
            run = False

    except AssertionError as ae:
        print(u'Assertion: ', ae)
    except Exception as e:
        print(u'Что-то пошло не так: ', e)
    else:
        print(u'Сбоев не было')
    finally:
        return 0

if __name__ == "__main__":
    main()