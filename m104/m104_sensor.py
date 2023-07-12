# -*- coding: utf-8 -*-
from __future__ import division, print_function
import serial
import graphics as gr
import collections as coll
import binascii
import threading

# Изменить значение PORT при необходимости
PORT = 'COM19'


cBlack = gr.color_rgb(0, 0, 0)
cGrey = gr.color_rgb(80, 80, 80)
cRed = gr.color_rgb(255, 0, 0)
cBlue = gr.color_rgb(0, 0, 255)
cWhite = gr.color_rgb(255, 255, 255)
cGreen = gr.color_rgb(0, 255, 0)
cYellow = gr.color_rgb(255, 255, 0)
cCian = gr.color_rgb(0, 255, 255)
rs232_coord_out_q = coll.deque()
run = True
mbx_232 = coll.deque()


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
                if (rx_byte == 0xFF) or (rx_byte == 0xBF) or (rx_byte == 0xDF) or (rx_byte == 0x9F) :
                    rx_cnt = 1
                    packet.append(rx_byte)
                    packet_in_progress = True
            else:
                packet.append(rx_byte)
                rx_cnt += 1
                if rx_cnt == 10:
                    rs232_coord_out_q.append(packet)
                    rx_cnt = 0
                    packet_in_progress = False
                    packet = coll.deque()


def coord_q(coord_out):
    if coord_out[0] == 0xBF:
        flag1 = 1
        flag2 = 0 
    if coord_out[0] == 0x9F:
        flag1 = 1
        flag2 = 1
    if coord_out[0] == 0xFF:
        flag1 = 0
        flag2 = 0
    if coord_out[0] == 0xDF:
        flag1 = 0
        flag2 = 1
    y1h = coord_out[3]
    y1l = coord_out[4]
    x1h = coord_out[1]
    x1l = coord_out[2]
    y2h = coord_out[7]
    y2l = coord_out[8]
    x2h = coord_out[5]
    x2l = coord_out[6]
    x1 = (x1h << 7) + x1l
    x2 = (x2h << 7) + x2l
    y1 = (y1h << 7) + y1l
    y2 = (y2h << 7) + y2l
    print('f1 = %.5s, f2 = %.5s, x1,y1 = (%.5s, %.5s), x2,y2 = (%.5s, %.5s) ' % (flag1, flag2, x1, y1, x2, y2))
    return x1, y1, x2, y2, flag1, flag2


def coord_drawer_232():
    class CoordWindow:
        def __init__(self, width, height):
            self.dot1_pressed_color = gr.color_rgb(0, 0, 255)
            self.dot1_released_color = gr.color_rgb(255, 255, 255)
            self.dot2_pressed_color = gr.color_rgb(0, 255, 255)
            self.dot2_released_color = gr.color_rgb(255, 128, 128)
            self.rsdot_radius = 24
            self.window = gr.GraphWin("Touch Screen", width, height)
            self.window.setCoords(0, 767, 1023, 0)
            self.window.setBackground(cBlack)
            self.window.focus_force()
            self.window.redraw()
            self.maxitems = 1
            self.dot1_pressed = False
            self.dot2_pressed = False
            brdr = gr.Rectangle(gr.Point(0, 0), gr.Point(1023, 767))
            brdr.setOutline(cWhite)
            brdr.draw(self.window)
            tt = gr.Text(gr.Point(511, 100), u'Проверка экрана raw')
            tt.draw(self.window)
            tt.setTextColor(cWhite)
            tt.setSize(16)            
            
        def dots_process(self, x1, y1, x2, y2, f1, f2):
            if f1 == 1:
                self.dot1_pressed = True
                self.draw_dot(x1, y1, self.dot1_pressed_color)
            else:
                if self.dot1_pressed is True:
                    self.draw_dot(x1, y1, self.dot1_released_color)
                    self.dot1_pressed = False
            if f2 == 1:
                self.dot2_pressed = True
                self.draw_dot(x2, y2, self.dot2_pressed_color)
            else:
                if self.dot2_pressed is True:
                    self.draw_dot(x2, y2, self.dot2_released_color)
                    self.dot2_pressed = False
        def draw_dot(self, x, y, color):
            y_mod = int(y * 0.75)
            rsdot = gr.Circle(gr.Point(x, y_mod), self.rsdot_radius)
            rsdot.setFill(color)
            rsdot.draw(self.window)
            if len(self.window.items[:]) > self.maxitems:
                self.delitem(0)
        def delitem(self, n):
            self.window.delItem(self.window.items[n])
        def close(self):
            self.window.close()
    w = CoordWindow(1024, 768)
    while 1:
        if rs232_coord_out_q:
            pack = rs232_coord_out_q.popleft()
            x1, y1, x2, y2, f1, f2 = coord_q(pack)
            w.dots_process(x1, y1, x2, y2, f1, f2)
    w.close()


def main():
    global run
    try:
        print(chr(12))
        with serial.Serial(PORT, baudrate=115200) as ser:
            th1 = threading.Thread(name='th_rs232', target=inq, args=(ser, mbx_232))
            th2 = threading.Thread(name='th_sw', target=inq_switch, args=(mbx_232, '232'))
            th3 = threading.Thread(name='th_cd', target=coord_drawer_232,)
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