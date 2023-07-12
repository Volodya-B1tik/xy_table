#/ coding=utf-8
# ebb_motion.py
# Motion control utilities for EiBotBoard
# https://github.com/evil-mad/plotink
#
# Intended to provide some common interfaces that can be used by
# EggBot, WaterColorBot, AxiDraw, and similar machines.
#
# See version() below for version number.
#
# The MIT License (MIT)
#
# Copyright (c) 2019 Windell H. Oskay, Evil Mad Scientist Laboratories
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


#import touchscreen_tests as touch
#import pmf_test as t
#from PyQt4 import QtCore
import rs
#import serial
import threading
import numpy as np
import math
import time
import ebb_serial_my as ebb_serial_my
# from . import ebb_serial_my
import graphics as gr
import collections as coll
import binascii
import copy
#from timer import Timer
PMF_TYPE = '_32' # '_6x'
COM_RS232 = 'COM12' # порт к которому подключен канал RS-232 ПМФ
COM_RS422 = 'COM2' # порт к которому подключен канал RS-422 ПМФ
# PACKET_TTL - время в секундах, которое будет приниматься один пакет,
# если за это время пакет до конца не получен то он отбрасывается
PACKET_TTL = 2
SKIP_CHECKSUM = True # пропуск проверки контрольной суммы пакетов

# очереди входных каналов для развязки потоков
mbx_232 = coll.deque()
mbx_422 = coll.deque()
mbx_can = coll.deque()
mbx_mdc = coll.deque() # прием непосредственно с дисплейного модуля

# очереди пакетов (наполняются функцией inq_switch)
rs232_old_q = coll.deque()
old_xy = coll.deque()
rs232_coord_out_q = coll.deque()
rs232_key_out_q = coll.deque()
rs232_key_set_out_q = coll.deque()
rs232_sts_out_q = coll.deque()
rs232_sts_pmf_q = coll.deque()
rs232_sts_vpipe_q = coll.deque()
rs232_sts_vpr1_q = coll.deque()
rs232_sts_vpr2_q = coll.deque()
rs232_sts_vpr3_q = coll.deque()
rs232_sts_vpr4_q = coll.deque()
rs232_sts_vglv_q = coll.deque()
rs232_sts_eth1_q = coll.deque()
rs232_sts_eth2_q = coll.deque()
rs232_sts_ovhp_q = coll.deque()
rs232_key_off_clicked_q = coll.deque()
rs232_receipt_off_q = coll.deque()
rs232_ts_raw_32_q = coll.deque()
rs232_ts_raw_6x_q = coll.deque()

rs422_coord_out_q = coll.deque()
rs422_key_out_q = coll.deque()
rs422_key_set_out_q = coll.deque()
rs422_sts_out_q = coll.deque()
rs422_sts_pmf_q = coll.deque()
rs422_sts_vpipe_q = coll.deque()
rs422_sts_vpr1_q = coll.deque()
rs422_sts_vpr2_q = coll.deque()
rs422_sts_vpr3_q = coll.deque()
rs422_sts_vpr4_q = coll.deque()
rs422_sts_vglv_q = coll.deque()
rs422_sts_eth1_q = coll.deque()
rs422_sts_eth2_q = coll.deque()
rs422_sts_ovhp_q = coll.deque()

can_coord_out_q = coll.deque()
can_key_out_q = coll.deque()

diag_levels_q = coll.deque()
red_level_6x = 3000
green_level_6x = 3800
red_level_32 = 3600
green_level_32 = 4000

# цвета
cBlack = gr.color_rgb(0, 0, 0)
cGrey = gr.color_rgb(80, 80, 80)
cRed = gr.color_rgb(255, 0, 0)
cBlue = gr.color_rgb(0, 0, 255)
cWhite = gr.color_rgb(255, 255, 255)
cGreen = gr.color_rgb(0, 255, 0)
cYellow = gr.color_rgb(255, 255, 0)
cCian = gr.color_rgb(0, 255, 255)

mdcdot_pressed_color = gr.color_rgb(0, 255, 0)
mdcdot_released_color = gr.color_rgb(255, 0, 0)

rsdot_pressed_color = gr.color_rgb(55, 0, 55)
#rsdot_released_color = gr.color_rgb(48, 0, 48)
rsdot_released_color = gr.color_rgb(255, 0, 0)
rsdot2_pressed_color = gr.color_rgb(0, 255, 255)
rsdot2_released_color = gr.color_rgb(0, 48, 48)

# параметры заводских настроек
defaults = {
    'mode': 0x00,
    'key_mode': 0x00,
    'gainR': 0x80,
    'gainG': 0x80,
    'gainB': 0x80,
    'offsetR': 0x40,
    'offsetG': 0x40,
    'offsetB': 0x40,
    'phase': 0x50,
    'offsetH': 0x00,
    'offsetV': 0x00,
    'brightness': 0xFE,
    'vidparam': 0xFE,
    'vidinterface': 0xFE,
    'topros': 0x0A,
    'tavtopovtor': 0x06}

run = True  # переменная для остановки потоков перед выходом
test_stop = False  # принудительная остановка текущего теста
test_next = False  # переход к следующему тесту

SKIP_CHECKSUM = True # пропуск проверки контрольной суммы пакетов

# очереди входных каналов для развязки потоков
mbx_232 = coll.deque()

def inq(ser, mbx):
    #print("INQ")    
    """ Качалка данных из входного буфера COM-порта в FIFO-канала.
    Выполняется бесконечно, должна запускаться в отдельном потоке.
    1) ser - [serial.Serial] COM-порт с которого будем читать
    2) mbx - [collections.deque] FIFO-канала в которую будем писать
    """
    dat = 0
    while 1:
        s = ser.inWaiting()
       # print(s)
#        time.sleep(1)
        if s > 0:
          #  print('9999999999')            
            dat = ser.read(s)
            #print(dat)
            chunk = coll.deque([int(binascii.hexlify(dat[i]), 16)
                                for i in xrange(len(dat))])
           # print('888888888888')            
            while True:
                try:
                    mbx.append(chunk.popleft())
#                    print(mbx)
                except IndexError:
                    break
               # except:
                  #  print('adfadf')
    #print('stop inq')


def inq_switch(mbx, channel):
    #print("INQ_SWTCH")
    """ Разбиралка FIFO-канала на несколько FIFO с однотипными пакетами.
    Выполняется бесконечно, должна запускаться в отдельном потоке.
    1) mbx - [collections.deque] FIFO-канала из которой будем доставать
             данные, из них лепить пакеты и складывать каждый пакет в
             свою очередь:
             ххх_coord_out_q   - очередь пакетов координат (COORD_OUT)
             ххх_key_out_q     - очередь пакетов нажатых клавиш (KEY_OUT)
             ххх_sts_out_q     - очередь пакетов статуса (STS_OUT)
             ххх_sts_pmf_q     - очередь пакетов статуса (STS_PMF)
             ххх_key_set_out_q - очередь пакетов нажатых клавиш (KEY_SET_OUT)
             , где ххх - название канала (rs232, rs422, can)
             у всех пакетов в этих очередях следующие отличия от протокола:
             а) вместо FF FF в начале каждого пакета идет FF FF FF
             это сделано чтобы индексы слов пакетов совпали с номерами
             слов в протоколе ИЛВ;
             б) последнее слово (контрольная сумма) отброшена, т.к. уже
             проверена на этапе приема пакета и чтобы количество байт в
             пакете не поменялось из-за добавленного FF в начале.
    2) channel - [str] канал которому соответствует очередь
                 ('232', '422', 'CAN')
    """

    ff1 = False
    ff2 = False
    rx_cnt = 0
    packet_in_progress = False
    packet = coll.deque()
    while run:
        if mbx:
                       
            rx_byte = mbx.popleft()
#            print(rx_byte)
           # rs232_old_q.append(rx_byte) 
            if not packet_in_progress:
                if ff1 is False and rx_byte == 0xFF:
                    ff1 = True
#                    print('ff1')
                    rx_cnt = 1
                elif ff1 is True and ff2 is False and rx_byte == 0xFF:
                    ff2 = True
#                    print(ff2)
                    rx_cnt += 1
                elif ff1 is True and ff2 is False and rx_byte != 0xFF:
                    ff1 = False
                elif ff1 is True and ff2 is True:
                    if rx_byte != 0xFF:
#                        print('idid')
                        rx_cnt += 1
                        packet_id = rs.decode_packet_id(rx_byte)
                        if packet_id == 'TS_RAW': packet_id = 'TS_RAW' + PMF_TYPE
                        if packet_id != '':
                            packet.append(rx_byte)
                            packet_in_progress = True
                            packet_start_time = time.clock()
                            
                        else:
                            ff1, ff2 = False, False
            else:
                                    
                packet.append(rx_byte)
                rx_cnt += 1
                if rx_cnt == rs.packet_size[packet_id]:
                    if  rs.packet_cs_check(packet) or SKIP_CHECKSUM:
                        [packet.appendleft(0xFF) for i in xrange(3)]
                        if channel == '232':
                            if packet_id == 'COORD_OUT':
                                rs232_coord_out_q.append(packet)
#                                print(packet)
                            elif packet_id == 'KEY_OUT': rs232_key_out_q.append(packet)
                            elif packet_id == 'STS_OUT': rs232_sts_out_q.append(packet)
                            elif packet_id == 'KEY_SET_OUT': rs232_key_set_out_q.append(packet)
                            elif packet_id == 'STS_PMF':  rs232_sts_pmf_q.append(packet)
                            elif packet_id == 'STS_VPIPE': rs232_sts_vpipe_q.append(packet)
                            elif packet_id == 'STS_VPr1': rs232_sts_vpr1_q.append(packet)
                            elif packet_id == 'STS_VPr2': rs232_sts_vpr2_q.append(packet)
                            elif packet_id == 'STS_VPr3': rs232_sts_vpr3_q.append(packet)
                            elif packet_id == 'STS_VPr4': rs232_sts_vpr4_q.append(packet)
                            elif packet_id == 'STS_VGLV': rs232_sts_vglv_q.append(packet)
                            elif packet_id == 'STS_ETH1': rs232_sts_eth1_q.append(packet)
                            elif packet_id == 'STS_ETH2': rs232_sts_eth2_q.append(packet)
                            elif packet_id == 'STS_OVHP': rs232_sts_ovhp_q.append(packet)
                            elif packet_id == 'KEY_OFF_CLICKED': rs232_key_off_clicked_q.append(packet)
                            elif packet_id == 'RECEIPT_OFF': rs232_receipt_off_q.append(packet)
                            elif packet_id == 'TS_RAW_32': rs232_ts_raw_32_q.append(packet)
                            elif packet_id == 'TS_RAW_6x': rs232_ts_raw_6x_q.append(packet)

                        elif channel == '422':
                            if packet_id == 'COORD_OUT': rs422_coord_out_q.append(packet)
                            elif packet_id == 'KEY_OUT': rs422_key_out_q.append(packet)
                            elif packet_id == 'STS_OUT': rs422_sts_out_q.append(packet)
                            elif packet_id == 'KEY_SET_OUT': rs422_key_set_out_q.append(packet)
                            elif packet_id == 'STS_PMF': rs422_sts_pmf_q.append(packet)
                            elif packet_id == 'STS_VPIPE': rs422_sts_vpipe_q.append(packet)
                            elif packet_id == 'STS_VPr1': rs422_sts_vpr1_q.append(packet)
                            elif packet_id == 'STS_VPr2': rs422_sts_vpr2_q.append(packet)
                            elif packet_id == 'STS_VPr3': rs422_sts_vpr3_q.append(packet)
                            elif packet_id == 'STS_VPr4': rs422_sts_vpr4_q.append(packet)
                            elif packet_id == 'STS_VGLV': rs422_sts_vglv_q.append(packet)
                            elif packet_id == 'STS_ETH1': rs422_sts_eth1_q.append(packet)
                            elif packet_id == 'STS_ETH2': rs422_sts_eth2_q.append(packet)
                            elif packet_id == 'STS_OVHP': rs422_sts_ovhp_q.append(packet)

                        elif channel == 'CAN':
                            pass  # тут допилить CAN
                        ff1, ff2 = False, False
                        packet_in_progress = False
                        packet = coll.deque()
        else:
            if packet_in_progress:
                if time.clock() > packet_start_time + PACKET_TTL:
                        ff1, ff2 = False, False
                        packet_in_progress = False
                        log.critical(u'Time to recieve is elapsed, rx buffer: % s' % packet)
                        packet = coll.deque()


def coord_q(coord_out):
    
    flag1 = coord_out[4]
    y1h = coord_out[5]
    y1l = coord_out[6]
    x1h = coord_out[7]
    x1l = coord_out[8]
    flag2 = coord_out[9]
    y2h = coord_out[10]
    y2l = coord_out[11]
    x2h = coord_out[12]
    x2l = coord_out[13]
    x1 = (x1h << 7) + x1l
    x2 = (x2h << 7) + x2l
    y1 = (y1h << 7) + y1l
    y2 = (y2h << 7) + y2l
    if flag1 == 255:
        flag1 = 0
    else:
        flag1 = 1
    if flag2 == 255:
        flag2 = 0
    else:
        flag2 = 1

    cc = ('f1 = %.5s, f2 = %.5s, x1,y1 = (%.5s, %.5s), \
x2,y2 = (%.5s, %.5s) ' % (flag1, flag2, x1, y1, x2, y2))
   

#    print('f1 = %.5s, f2 = %.5s, x1,y1 = (%.5s, %.5s), \
#x2,y2 = (%.5s, %.5s) ' % (flag1, flag2, x1, y1, x2, y2))
    return x1, y1, x2, y2, flag1, flag2
    
def coord_drawer_232(ser):
    """
    Тест
    """



   # log.info(u'Проверка сенсора (рисовалка)')
    #rs.set_mode(ser, u'технологический')
    class CoordWindow:
        def __init__(self, width, height):
            self.dot1_pressed_color = gr.color_rgb(128, 128, 255)
            self.dot1_released_color = gr.color_rgb(255, 0, 0)
            self.dot2_pressed_color = gr.color_rgb(0, 128, 255)
            self.dot2_released_color = gr.color_rgb(255, 128, 128)
            self.rsdot_radius = 16
            self.window = gr.GraphWin("PMF-6.0 Touch Screen", width, height)
            self.window.setCoords(0, 767, 1023, 0)
            self.window.setBackground(cBlack)
            self.maxitems = 10
            self.dot1_pressed = False
            self.dot2_pressed = False

            for y in xrange(1, 9, 1):
                brdr = gr.Rectangle(gr.Point(0, 0), gr.Point(1023, y*96))
                brdr.setOutline(cWhite)
                brdr.draw(self.window)
            for x in xrange(1, 9, 1):
                brdr = gr.Rectangle(gr.Point(0, 0), gr.Point(x*128, 767))
                brdr.setOutline(cWhite)
                brdr.draw(self.window)

#            self.tt = gr.Text(gr.Point(511, 60), u'Проверка сенсорного '
#                                                 u'экрана №2')
#            self.tt.draw(self.window)
#            self.tt.setTextColor(cWhite)
#            self.tt.setSize(16)

#            brdr = gr.Rectangle(gr.Point(0, 0), gr.Point(1023, 767))
#            brdr.setOutline(cWhite)
#            brdr.draw(self.window)

#            for x in xrange(0, 640):
#                self.tt = gr.Line(gr.Point(x, 0), gr.Point(x, 480))
#                self.tt.setFill(gr.color_rgb((x % 256), (x % 256), (x % 256)))
#                self.tt.draw(self.window)

            # self.tmr = gr.Text(gr.Point(511, 150), u'60')
            # self.tmr.draw(self.window)
            # self.tmr.setTextColor(cYellow)
            # self.tmr.setSize(36)

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
#            y_mod = int(y * 0.5625)
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

    while test_stop is False and test_next is False:
        QtCore.QCoreApplication.processEvents()
        if rs232_coord_out_q:

            pack = rs232_coord_out_q.popleft()
           # log.info(pack)
            x1, y1, x2, y2, f1, f2 = \
                coord_q(pack)

            w.dots_process(x1, y1, x2, y2, f1, f2)
            if x2 > 950 and y2 > 950 and f2 == 1:
                break
    w.close()    

def version():  # Report version number for this document
    return "0.18"  # Dated November 29, 2019


def doABMove(port_name, delta_a, delta_b, duration):
    # Issue command to move A/B axes as: "XM,<move_duration>,<axisA>,<axisB><CR>"
    # Then, <Axis1> moves by <AxisA> + <AxisB>, and <Axis2> as <AxisA> - <AxisB>
    if port_name is not None:
        str_output = 'XM,{0},{1},{2}\r'.format(duration, delta_a, delta_b)
        ebb_serial_my.command(port_name, str_output)


def doTimedPause(port_name, n_pause):
    if port_name is not None:
        while n_pause > 0:
            if n_pause > 750:
                td = 750
            else:
                td = n_pause
                if td < 1:
                    td = 1  # don't allow zero-time moves
            ebb_serial_my.command(port_name, 'SM,{0},0,0\r'.format(td))
            n_pause -= td


def doLowLevelMove(port_name, ri1, steps1, delta_r1, ri2, steps2, delta_r2):
    # A "pre-computed" XY movement of the form
    #  "LM,RateTerm1,AxisSteps1,DeltaR1,RateTerm2,AxisSteps2,DeltaR2<CR>"
    # See http://evil-mad.github.io/EggBot/ebb.html#LM for documentation.
    # Important: Requires firmware version 2.5.1 or higher.
    if port_name is not None:
        if ((ri1 == 0 and delta_r1 == 0) or steps1 == 0) and ((ri2 == 0 and delta_r2 == 0) or steps2 == 0):
            return
        str_output = 'LM,{0},{1},{2},{3},{4},{5}\r'.format(ri1, steps1, delta_r1, ri2, steps2, delta_r2)
        ebb_serial_my.command(port_name, str_output)


def doXYMove(port_name, delta_x, delta_y, duration):
    # duration is an integer in the range from 1 to 16777215, giving time in milliseconds
    # delta_x and delta_y are integers, each in the range from -16777215 to 16777215, giving movement distance in steps
    # The minimum speed at which the EBB can generate steps for each motor is 1.31 steps/second. The maximum
    # speed is 25,000 steps/second.
    # Move X/Y axes as: "SM,<move_duration>,<axis1>,<axis2><CR>"
    # Typically, this is wired up such that axis 1 is the Y axis and axis 2 is the X axis of motion.
    # On EggBot, Axis 1 is the "pen" motor, and Axis 2 is the "egg" motor.
    if port_name is not None:
        str_output = 'SM,{0},{1},{2}\r'.format(duration,delta_y,delta_x)
        ebb_serial_my.command(port_name, str_output)


def moveDistLM(rin, delta_rin, time_ticks):
    # Calculate the number of motor steps taken using the LM command,
    # with rate factor r, delta factor delta_r, and in a given number
    # of 40 us time_ticks. Calculation is for one axis only.

    # Distance moved after n time ticks is given by (n * r + (n^2 - n)*delta_r/2) / 2^31

    n = int(time_ticks)  # Ensure that the inputs are integral.
    r = int(rin)
    delta_r = int(delta_rin)

    if n == 0:
        return 0
    else:
        np = (n * n - n) >> 1  # (n^2 - n)/2 is always an integer.
        s = (n * r) + delta_r * np
        s = s >> 31
        return s


def moveTimeLM(ri, steps, delta_r):
    # Calculate how long, in 40 us ISR intervals, the LM command will take to move one axis.

    # First: Distance in steps moved after n time ticks is given by
    #  the formula: distance(time n) = (10 * r + (n^2 - n)*delta_r/2) / 2^31.
    # Use the quadratic formula to solve for possible values of n,
    # the number of time ticks needed to travel the through distance of steps.
    # As this is a floating point result, we will round down the output, and
    # then move one time step forward until we find the result.

    r = float(ri)
    d = float(delta_r)
    steps = abs(steps)  # Distance to move is absolute value of steps.

    if steps == 0:
        return 0  # No steps to take, so takes zero time.

    if delta_r == 0:
        if ri == 0:
            return 0  # No move will be made if ri and delta_r are both zero.

        # Else, case of no acceleration.
        # Simple to get actual movement time:
        # T (seconds) = (AxisSteps << 31)/(25 kHz * RateTerm)

        f = int(steps) << 31
        t = f / r
        t2 = int(math.ceil(t))
        return t2
    else:
        factor1 = (d / 2.0) - r
        factor2 = r * r - d * r + (d * d / 4.0) + (2 * d * 2147483648.0 * steps)

        if factor2 < 0:
            factor2 = 0
        factor2 = math.sqrt(factor2)
        root1 = int(math.floor((factor1 + factor2) / d))
        root2 = int(math.floor((factor1 - factor2) / d))

    if root1 < 0 and root2 < 0:
        return -1  # No plausible roots -- movement time must be greater than zero.

    if root1 < 0:
        time_ticks = root2  # Pick the positive root
    elif root2 < 0:
        time_ticks = root1  # Pick the positive root
    elif root2 < root1:  # If both are valid, pick the smaller value.
        time_ticks = root2
    else:
        time_ticks = root1

    # Now that we have an floor estimate for the time:
    # calculate how many steps occur in the estimated time.
    # Then, using that head start, calculate the
    # exact number of time ticks needed.

    dist = 0
    continue_loop = True
    while continue_loop:
        time_ticks += 1

        dist = moveDistLM(ri, delta_r, time_ticks)

        if 0 < dist < steps:
            pass
        else:
            continue_loop = False

    if dist == 0:
        time_ticks = 0

    return time_ticks


def QueryPenUp(port_name):
    if port_name is not None:
        pen_status = ebb_serial_my.query(port_name, 'QP\r')
        if pen_status[0] == '0':
            return False
        else:
            return True


def QueryPRGButton(port_name):
    if port_name is not None:
        return ebb_serial_my.query(port_name, 'QB\r')


def sendDisableMotors(port_name):
    if port_name is not None:
        ebb_serial_my.command(port_name, 'EM,0,0\r')


def sendEnableMotors(port_name, res):
    if res < 0:
        res = 0
    if res > 5:
        res = 5
    if port_name is not None:
        ebb_serial_my.command(port_name, 'EM,{0},{0}\r'.format(res))
        # If res == 0, -> Motor disabled
        # If res == 1, -> 16X microstepping
        # If res == 2, -> 8X microstepping
        # If res == 3, -> 4X microstepping
        # If res == 4, -> 2X microstepping
        # If res == 5, -> No microstepping


def sendPenDown(port_name, pen_delay):
    if port_name is not None:
        str_output = 'SP,0,{0}\r'.format(pen_delay)
        ebb_serial_my.command(port_name, str_output)


def sendPenUp(port_name, pen_delay):
    if port_name is not None:
        str_output = 'SP,1,{0}\r'.format(pen_delay)
        ebb_serial_my.command(port_name, str_output)


def PBOutConfig(port_name, pin, state):
    # Enable an I/O pin. Pin: {0,1,2, or 3}. State: {0 or 1}.
    # Note that B0 is used as an alternate pause button input.
    # Note that B1 is used as the pen-lift servo motor output.
    # Note that B3 is used as the EggBot engraver output.
    # For use with a laser (or similar implement), pin 3 is recommended

    if port_name is not None:
        # Set initial Bx pin value, high or low:
        str_output = 'PO,B,{0},{1}\r'.format(pin, state)
        ebb_serial_my.command(port_name, str_output)
        # Configure I/O pin Bx as an output
        str_output = 'PD,B,{0},0\r'.format(pin)
        ebb_serial_my.command(port_name, str_output)


def PBOutValue(port_name, pin, state):
    # Set state of the I/O pin. Pin: {0,1,2, or 3}. State: {0 or 1}.
    # Set the pin as an output with OutputPinBConfigure before using this.
    if port_name is not None:
        str_output = 'PO,B,{0},{1}\r'.format(pin, state)
        ebb_serial_my.command(port_name, str_output)


def TogglePen(port_name):
    if port_name is not None:
        ebb_serial_my.command(port_name, 'TP\r')


def setPenDownPos(port_name, servo_max):
    if port_name is not None:
        ebb_serial_my.command(port_name, 'SC,5,{0}\r'.format(servo_max))
        # servo_max may be in the range 1 to 65535, in units of 83 ns intervals. This sets the "Pen Down" position.
        # http://evil-mad.github.io/EggBot/ebb.html#SC


def setPenDownRate(port_name, pen_down_rate):
    if port_name is not None:
        ebb_serial_my.command(port_name, 'SC,12,{0}\r'.format(pen_down_rate))
        # Set the rate of change of the servo when going down.
        # http://evil-mad.github.io/EggBot/ebb.html#SC


def setPenUpPos(port_name, servo_min):
    if port_name is not None:
        ebb_serial_my.command(port_name, 'SC,4,{0}\r'.format(servo_min))
        # servo_min may be in the range 1 to 65535, in units of 83 ns intervals. This sets the "Pen Up" position.
        # http://evil-mad.github.io/EggBot/ebb.html#SC


def setPenUpRate(port_name, pen_up_rate):
    if port_name is not None:
        ebb_serial_my.command(port_name, 'SC,11,{0}\r'.format(pen_up_rate))
        # Set the rate of change of the servo when going up.
        # http://evil-mad.github.io/EggBot/ebb.html#SC


def setEBBLV(port_name, ebb_lv):
    # Set the EBB "Layer" Variable, an 8-bit number we can read and write.
    # (Unrelated to our plot layers; name is an historical artifact.)
    if port_name is not None:
        ebb_serial_my.command(port_name, 'SL,{0}\r'.format(ebb_lv))


def queryEBBLV(port_name):
    # Query the EBB "Layer" Variable, an 8-bit number we can read and write.
    # (Unrelated to our plot layers; name is an historical artifact.)
    if port_name is not None:
        value = ebb_serial_my.query(port_name, 'QL\r')
        try:
            ret_val = int(value)
            return value
        except:
            return None


def queryVoltage(port_name):
    # Query the EBB motor power supply input voltage.
    if port_name is not None:
        version_status = ebb_serial_my.min_version(port_name, "2.2.3")
        if not version_status:
            return True # Unable to read version, or version is below 2.2.3.
                        # In these cases, issue no voltage warning.
        else:
            raw_string = (ebb_serial_my.query(port_name, 'QC\r'))
            split_string = raw_string.split(",", 1)
            split_len = len(split_string)
            if split_len > 1:
                voltage_value = int(split_string[1])  # Pick second value only
            else:
                return True  # We haven't received a reasonable voltage string response.
                # Ignore voltage test and return.
            # Typical reading is about 300, for 9 V input.
            if voltage_value < 250:
                return False
    return True
##################

def limit_stop_y(ser): 
          
        global flag_limit_Y     
          
        a=ebb_serial_my.query(ser,"PI,C,6\r") # read pin PC6    
        try:        
         if  int(a[3]):
              flag_limit_Y=True           
          #return int(a[3])     
         
        except:    
           flag_limit_X=False
           flag_limit_Y=False
    
           ser = ebb_serial_my.testPort("COM15")
           sendEnableMotors(ser,0)
           limit_stop_btn_config(ser)
           heatup_moves(ser) 
           print ("ERROR Y")           
           return 0      
                
def limit_stop_x(ser): 
        
                 
        global flag_limit_X
        
        b=ebb_serial_my.query(ser,"PI,A,2\r") # read pin PD4
        try:        
        
            #return int(b[3])     
         if  int(b[3]):
             flag_limit_X=True 
                
        except:
           
           ser = ebb_serial_my.testPort("COM15")
           sendEnableMotors(ser,0)
           limit_stop_btn_config(ser)
           heatup_moves(ser) 
           print ("ERROR X")
           return 0

def limit_stop_btn_config(ser):
                
        ebb_serial_my.query(ser,"PD,C,6,1\r") # config pin PC6 as input
        ebb_serial_my.query(ser,"PD,A,2,1\r") # config pin PC7 as input
        
        
def state_ZERO_XY(ser,pen_up_delay_ms):   #поднять палец и отправить в HOME      
             
              global flag_limit_Y     
              global flag_limit_X
              sendPenUp(ser, pen_up_delay_ms)
              
              while (flag_limit_Y==False) :
                 limit_stop_y(ser)
                 #print("flag_limit_Y=",flag_limit_Y) 
                 doABMove(ser,-30,0,15)
              
              while (flag_limit_Y==True)  and (flag_limit_X==False) :
                 limit_stop_x(ser)
                 #print("flag_limit_X=",flag_limit_X) 
                 doABMove(ser,0,-30,15)
              
              flag_limit_X=False
              flag_limit_Y=False 
              doTimedPause(ser,300)
       
def pmf_state_Zero_grid(ser):  #выход на нуль сетки ПМФа
                            
            doABMove(ser,3750,8150,1000)
            doTimedPause(ser,1000)        #pause 1s
            
def pmf_state_Zero(ser):  #выход на нуль сетки ПМФа
            #doABMove(ser,3800,6220,1000)
            doABMove(ser,2100,6220,1000)                
            doTimedPause(ser,1000)        #pause 1s
            
            
            
       
def rect_test1(ser,DX,DY,DT,sleep,pen_down_delay_ms): 
     
    sendPenDown(ser, pen_down_delay_ms)
    doTimedPause(ser,sleep)               
    
    for i in range(0,DX,int (DX/10)):
           doABMove(ser, 0,int (DX/10),100)                      
    doTimedPause(ser,sleep)                          
                                
                                
                                
    for i in range(0,DX,int (DX/10)):
           doABMove(ser, int (DX/10),0,100)                      
    doTimedPause(ser,sleep)                                       
                              
                              
                              
    for i in range(0,DX,int (DX/10)):
           doABMove(ser, 0,int (-DX/10),100)                      
    doTimedPause(ser,sleep)                                    
                              
                            
    for i in range(0,DX,int (DX/10)):
           doABMove(ser, int (-DX/10),0,100)                      
                                     
                              


def rect_test2(ser,DX,DY,DT,sleep,pen_down_delay_ms): 
        
    doTimedPause(ser,700) 
    TogglePen(ser) 
    doTimedPause(ser,700) 
    TogglePen(ser)
    doTimedPause(ser,700)
    
    
    for i in range(0,DX,DX/10):
           doABMove(ser, 0,DX/10,100)                      
         
    doTimedPause(ser,700) 
#    TogglePen(ser) 
#    doTimedPause(ser,700) 
#    TogglePen(ser)
#    doTimedPause(ser,700)
#   
    for i in range(0,DX,DX/10):
           doABMove(ser, DY/10,0,100)                      
    doTimedPause(ser,700) 
#    TogglePen(ser)
#    doTimedPause(ser,700)
#    TogglePen(ser)
#    doTimedPause(ser,700)             
#                            
    for i in range(0,DX,DX/10):
               doABMove(ser, 0,-DX/10,100)                      
    doTimedPause(ser,700) 
#    TogglePen(ser)
#    doTimedPause(ser,700)                                  
#    TogglePen(ser)   
#    doTimedPause(ser,700)                      
#    
    
    for i in range(0,DX,DX/10):
               doABMove(ser, -DY/10,0,100)                      
    doTimedPause(ser,700) 
#    TogglePen(ser)
#    doTimedPause(ser,700)                                
#    TogglePen(ser)                          
#    doTimedPause(ser,700)
#   

       
def reset_controller():
     print (ebb_serial_my.query(ser,"CS\r"))
     # print (ebb_serial_my.query(ser,"R\r")) 
     # sendEnableMotors(ser,1)
      #limit_stop_btn_config(ser)               
                         
   
     
def ebb_stop():
     ebb_serial_my.query(ser,"ES\r")
     
def ebb_clear():
     ebb_serial_my.query(ser,"CS\r")     
     
def ebb_reset():
     print(ebb_serial_my.query(ser,"R\r"))  

def byk_byk(ser, pen_down_delay_ms):
    sendPenDown(ser, pen_down_delay_ms)
    time.sleep(0.3)    
    sendPenUp(ser, pen_down_delay_ms)
    time.sleep(0.3)             

def long_pause(seconds):
    for i in range(seconds*2):
          doTimedPause(ser,500)        
##################



def servo_timeout(port_name, timeout_ms, state=None):
    # Set the EBB servo motor timeout.
    # The EBB will cut power to the pen-lift servo motor after a given
    # time delay since the last X/Y/Z motion command.
    # It can also optionally set an immediate on/off state.
    # 
    # The time delay timeout_ms is given in ms. A value of 0 will
    # disable the automatic power-off feature.
    #
    # The state parameter is given as 0 or 1, to turn off or on
    # servo power immediately, respectively.
    #
    # This feature requires EBB hardware v 2.5.0 and firmware 2.6.0
    #
    # Reference: http://evil-mad.github.io/EggBot/ebb.html#SR
    #
    if port_name is not None:
        version_status = ebb_serial_my.min_version(port_name, "2.6.0")
        if not version_status:
            return      # Unable to read version, or version is below 2.6.0.
        else:
            if state is None:
                str_output = 'SR,{0}\r'.format(timeout_ms)
            else:
                str_output = 'SR,{0},{1}\r'.format(timeout_ms, state)
            ebb_serial_my.command(port_name, str_output)




def grid_prepare(ser,X_len,Y_len, X_grid,Y_grid,hor_vert):
   d_x=0
   d_y=0
   global arr_out   
   global flag_touch_push
   heatup_moves(ser)   
   long_pause(1)        
   state_ZERO_XY(ser,100) 
   pmf_state_Zero(ser)
   long_pause(1)
   i=0
   
   d_x1=0
   d_y1=0
   d_y2=0
   d_x2=0
   
   X_stp = (X_len/(X_grid))                      
   Y_stp = (Y_len/(Y_grid))
   arr=[[[0, 0]] * X_grid for i in range(Y_grid)]
   
   for y in range(Y_grid):     
       for x in range(X_grid):
           a= int((x*X_stp)+(X_stp/2))
           b =int((y*Y_stp)+(Y_stp/2))
           arr[x][y] = [a,b]
   #print (arr)
  
   if hor_vert==1: 
        arr = np.rot90(arr, 1)   #rotating
        arr = arr[::-1]
   
   
   for x in range(1,X_grid,2):  #переворот строки через строку (змейка)
       arr[x]=arr[x][::-1]

 #  print(arr)
 #  print("________")
   
   arr_out=[[0,0]]*(X_grid*Y_grid)
   arr_out=sum(arr,[])
  
 #  print (arr_out)
       
    


     
   for x in range(0,X_grid):
       for y in range(0,Y_grid):
           
           d_x1=arr[x][y][0]
           d_y1=arr[x][y][1]
           
           d_x=d_x1-d_x2
           d_y=d_y1-d_y2
          
          #print(d_x,d_y)
                      
           doABMove(ser,d_y,d_x,200)
           sendPenDown(ser,1000)
           sendPenUp(ser, 1000)
           
           
           d_x2=d_x1
           d_y2=d_y1
            
           
   state_ZERO_XY(ser,100)
    



def calc_processing(rs232_coord_out_q,ser1):
     global arr_out
     global d_x
     global d_y
     global d_x1
     global d_y1

     global flag_touch_push 
     global x_ebb
     global y_ebb
     global err_x
     global err_y
     n=0
     tme_new=0.0
     tme_old=0.0
     while 1:
        
        try:
                     
            val = rs232_coord_out_q.popleft()
            val=coord_q(val)
           
            if val[4] and flag_touch_push==0: 
                       

                    flag_touch_push=1                             
                    
                                                         
                                                                               
                    x_th=((17150/1023) * val[0])/100
                    y_th=((12880/1023) * (1023-val[1]))/100
                   
                        
                                       
                    
                    
                    
                    tme_new=time.clock()
                    tme=tme_new-tme_old
                    tme_old=tme_new               
                    #print(tme)
                    
                    if (not n):
                        
                             print("plot->",n,"touch->", x_th, y_th, "ebb->", arr_out[n][0]/100, arr_out[n][1]/100, "err->",x_th-arr_out[n][0]/100,y_th-arr_out[n][1]/100)   
                    
                    if (n>0) and (1<tme<2.5):
                                        
                              print("plot->",n,"touch->", x_th, y_th, "ebb->", arr_out[n][0]/100, arr_out[n][1]/100, "err->",x_th-arr_out[n][0]/100,y_th-arr_out[n][1]/100,"time->",tme)
                              n=n+1 
                    
                    else : 
                        print ("Position",n+1,"NO PUSHED")            
#                    a=time.clock()
#                    tme_new=a-tme_old
#                    print("up",tme_new,tme_old,a)
#                    tme_old=copy.copy(tme_new)
#                    print("down",tme_new,tme_old,a)
#                    
                    
            
            if not val[4]:
                    flag_touch_push=0
                    
        except IndexError:
            pass
            
 
def test_while():
    while 1:
           a=29000
           b=20000
           setPenUpPos(ser, a)
           setPenDownPos(ser,b)
           
           sendPenDown(ser,1000)
           sendPenUp(ser, 1000)
           time.sleep(0.1)






def main1(ser,ser1):
    
    th1 = threading.Thread(name='ebb', target=grid_prepare, args=(ser,17150,12880,4,4,0,))
    th2 = threading.Thread(name='rs232', target=inq, args=(ser1, mbx_232))    
    th3 = threading.Thread(name='switch_232', target=inq_switch, args=(mbx_232, '232'))
    th4 = threading.Thread(name='calc_proc', target=calc_processing, args=(rs232_coord_out_q,ser1,))
    th5 = threading.Thread(name='graph', target=coord_drawer_232, args=(ser1,))
    th6 = threading.Thread(name='test', target=test_while,args=())
    
   
    th1.start()
    th2.start()
    th3.start()
    th4.start()    
   # th5.start()
   # th6.start()    
     
          


def heatup_moves(ser):
    MAX_SPEED = 25000  # steps/s
       
    DY = 1620*6
    DX = 2120*6
    DT = 4000
    dist = max(DX, DY)
    speed = int(dist * 1000 / DT)
    assert speed < MAX_SPEED, 'Too fast!'
    setPenUpPos(ser, 20000)
    setPenDownPos(ser, 29000)
    time.sleep(1)
    
    sendEnableMotors(ser,   1)
      
                # If res == 0, -> Motor disabled
                # If res == 1, -> 16X microstepping
                # If res == 2, -> 8X microstepping
                # If res == 3, -> 4X microstepping
                # If res == 4, -> 2X microstepping
                # If res == 5, -> No microstepping    
#    doABMove(ser,0,1000,1000)   
#    doABMove(ser,1000,0,1000)
#    doABMove(ser,0,-1000,1000)   
#    doABMove(ser,-1000,0,1000)
                
                
                
       


#    while 1:
#        print (time.strftime("WORK TIME:" + "%H" ":" + "%M" + ":" + "%S"))
#        long_pause(1)        
#        state_ZERO_XY(ser,pen_up_delay_ms) 
#        pmf_state_Zero_grid(ser)
#        long_pause(1)
#        
#        
#       for i in range(10):    
#        
#           rect_test1(ser,DX,DY,DT,sleep,pen_down_delay_ms)
#         
#            # rect_test2(ser,DX,DY,DT,sleep,pen_down_delay_ms)
             
                   
 

#    while 1:
#        long_pause(1)        
#        state_ZERO_XY(ser,pen_up_delay_ms) 
#        pmf_state_Zero(ser)
#        long_pause(1)
#        i= not (i)
#        grid_prepare(ser,17150,12880,8,8 ,i)
        
                 
                            
              
              
             
              

if __name__ == "__main__":
   
   arr_out =[]  
   x_ebb=0
   y_ebb=0
   err_x=0
   err_y=0
   
   
   flag_touch_push=False
   flag_limit_X=False
   flag_limit_Y=False   
   ser = ebb_serial_my.testPort("COM6")
   ser1=serial.Serial('COM11', baudrate=9600, parity=serial.PARITY_NONE)
   rs.set_mode(ser1, u'технологический')
   main1(ser,ser1) 
  
       
   
  # print (time.strftime("START TIME:" + "%H" ":" + "%M" + ":" + "%S"))
    
#    flag_limit_X=False
#    flag_limit_Y=False
#    
#    ser = ebb_serial_my.testPort("COM6")
#    #grid_prepare(ser,6000,6000, 6,6)
#    sendEnableMotors(ser,0)
#    limit_stop_btn_config(ser)
#    heatup_moves(ser)
#    
#    




