# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 21:57:06 2017

@author: User
"""

#import test as t
import pmf_test as t
import logging
from var import *
import rs
import graphics as gr
import math
from PyQt4 import QtCore, QtGui
import random
import time
import binascii

log = logging.getLogger(__name__)

def coord_old_out(ser):
    rs.set_mode(ser, u'штатный')
    log.info(u'Проверка OLD_OUT')

    window = gr.GraphWin("Touch Screen", 1024, 768)
    window.setCoords(0, 767, 1023, 0)
    radius = 36
    window.setBackground(cBlack)

    brdr = gr.Rectangle(gr.Point(0, 0), gr.Point(1023, 767))
    brdr.setOutline(cWhite)
    brdr.draw(window)


    xi1, yi1 = 2000, 2000
    rsdot1 = gr.Circle(gr.Point(xi1, yi1), radius)
    rsdot1.setFill(rsdot_pressed_color)
    rsdot1.draw(window)

    rsdot1_pressed = False

    while test_stop is False and test_next is False:
        #QtCore.QCoreApplication.processEvents()
        if t.old_xy:
            f1, x1, y1 = t.old_xy.popleft()
            if f1 == 0xBF:
                rsdot1.setFill(rsdot_pressed_color)
                y1_mod = int(y1 * 0.75)
                rsdot1.move(x1 - xi1, y1_mod - yi1)
                xi1 = x1
                yi1 = y1_mod
                rsdot1_pressed = True
            else:
                if rsdot1_pressed:
                    rsdot1.setFill(rsdot_released_color)
                    y1_mod = int(y1 * 0.75)
                    rsdot1.move(x1 - xi1, y1_mod - yi1)
                    xi1 = x1
                    yi1 = y1_mod
                    rsdot1_pressed = False

    window.close()


def coord_delay_test(ser):
    """ Проверка задержки выдачи координат.
    Создает окно. На окно выводятся две точки, одна из канала RS-232,
    вторая из UART который формирует МДЦ-104.
    Задержка оценивается визуально. """

    rs.set_mode(ser, u'технологический')
    log.info(u'Проверка задержки выдачи координат')

    window = gr.GraphWin("PMF-6.0 Touch Screen", 1024, 768)
    window.setCoords(0, 767, 1023, 0)
    radius = 36
    window.setBackground(cBlack)



    for y in xrange(1, 48, 1):
        brdr = gr.Rectangle(gr.Point(0, 0), gr.Point(1023, y*16))
        brdr.setOutline(cGrey)
        brdr.draw(window)
    for x in xrange(1, 64, 1):
        brdr = gr.Rectangle(gr.Point(0, 0), gr.Point(x*16, 767))
        brdr.setOutline(cGrey)
        brdr.draw(window)

    brdr = gr.Rectangle(gr.Point(0, 0), gr.Point(1023, 767))
    brdr.setOutline(cWhite)
    brdr.draw(window)

    tt = gr.Text(gr.Point(511, 40), u'Проверка сенсора')
    tt.draw(window)
    tt.setTextColor(cWhite)
    tt.setSize(24)

    # tmr = gr.Text(gr.Point(511, 150), u'60')
    # tmr.draw(window)
    # tmr.setTextColor(cYellow)
    # tmr.setSize(36)

    xi1, yi1 = 2000, 2000
    rsdot1 = gr.Circle(gr.Point(xi1, yi1), radius)
    rsdot1.setFill(rsdot_pressed_color)
    rsdot1.draw(window)

    xi2, yi2 = 2000, 2000
    rsdot2 = gr.Circle(gr.Point(xi2, yi2), radius)
    rsdot2.setFill(rsdot_pressed_color)
    rsdot2.draw(window)

    xi3, yi3 = 2000, 2000
    mdcdot1 = gr.Circle(gr.Point(xi3, yi3), radius)
    mdcdot1.setFill(mdcdot_pressed_color)
    mdcdot1.draw(window)

    xi4, yi4 = 2000, 2000
    mdcdot2 = gr.Circle(gr.Point(xi4, yi4), radius)
    mdcdot2.setFill(mdcdot_pressed_color)
    mdcdot2.draw(window)

    rsdot1_pressed = False
    rsdot2_pressed = False

    rel = 0
    while test_stop is False and test_next is False:
        #QtCore.QCoreApplication.processEvents()

        if t.rs232_coord_out_q:
            x1, y1, x2, y2, f1, f2 = t.coord_q(rs232_coord_out_q.popleft())
            if f1 == 1:
                rsdot1.setFill(rsdot_pressed_color)
                y1_mod = int(y1 * 0.75)
                rsdot1.move(x1 - xi1, y1_mod - yi1)
                xi1 = x1
                yi1 = y1_mod
                rsdot1_pressed = True
            else:
                if rsdot1_pressed:
                    rsdot1.setFill(rsdot_released_color)
                    y1_mod = int(y1 * 0.75)
                    rsdot1.move(x1 - xi1, y1_mod - yi1)
                    xi1 = x1
                    yi1 = y1_mod
                    rsdot1_pressed = False
                    rel += 1
                    tt.setText("Кол-во отжатий = %s" % rel)
            if f2 == 1:
                rsdot2.setFill(rsdot2_pressed_color)
                y2_mod = int(y2 * 0.75)
                rsdot2.move(x2 - xi2, y2_mod - yi2)
                xi2 = x2
                yi2 = y2_mod
                rsdot2_pressed = True
                tt.setText("p1 = %s , %s \n p2 = %s , %s" % (x1, y1_mod, x2, y2_mod))
            else:
                if rsdot2_pressed:
                    rsdot2.setFill(rsdot2_released_color)
                    y2_mod = int(y2 * 0.75)
                    rsdot2.move(x2 - xi2, y2_mod - yi2)
                    xi2 = x2
                    yi2 = y2_mod
                    rsdot2_pressed = False
    window.close()

def coord_bug(ser):

    rs.set_mode(ser, u'технологический')
    log.info(u'Проверка задержки выдачи координат')

    window = gr.GraphWin("PMF-6.0 Touch Screen", 1024, 768)
    window.setCoords(0, 767, 1023, 0)
    radius = 36
    window.setBackground(cBlack)

    brdr = gr.Rectangle(gr.Point(0, 0), gr.Point(1023, 767))
    brdr.setOutline(cWhite)
    brdr.draw(window)

    tt = gr.Text(gr.Point(511, 60), u'Проверка сенсорного экрана')
    tt.draw(window)
    tt.setTextColor(cWhite)
    tt.setSize(16)

    # tmr = gr.Text(gr.Point(511, 150), u'60')
    # tmr.draw(window)
    # tmr.setTextColor(cYellow)
    # tmr.setSize(36)

    xi1, yi1 = 2000, 2000
    rsdot1 = gr.Circle(gr.Point(xi1, yi1), radius)
    rsdot1.setFill(rsdot_pressed_color)
    rsdot1.draw(window)

    xi2, yi2 = 2000, 2000
    rsdot2 = gr.Circle(gr.Point(xi2, yi2), radius)
    rsdot2.setFill(rsdot_pressed_color)
    rsdot2.draw(window)

    xi3, yi3 = 2000, 2000
    mdcdot1 = gr.Circle(gr.Point(xi3, yi3), radius)
    mdcdot1.setFill(mdcdot_pressed_color)
    mdcdot1.draw(window)

    xi4, yi4 = 2000, 2000
    mdcdot2 = gr.Circle(gr.Point(xi4, yi4), radius)
    mdcdot2.setFill(mdcdot_pressed_color)
    mdcdot2.draw(window)

    rsdot1_pressed = False
    rsdot2_pressed = False

    while test_stop is False and test_next is False:
        #QtCore.QCoreApplication.processEvents()

        if t.rs232_coord_out_q:
            x1, y1, x2, y2, f1, f2 = t.coord_q(rs232_coord_out_q.popleft())
            if f1 == 1:
                rsdot1.setFill(rsdot_pressed_color)
                y1_mod = int(y1 * 0.75)
                rsdot1.move(x1 - xi1, y1_mod - yi1)
                xi1 = x1
                yi1 = y1_mod
                rsdot1_pressed = True
            else:
                if rsdot1_pressed:
                    rsdot1.setFill(rsdot_released_color)
                    y1_mod = int(y1 * 0.75)
                    rsdot1.move(x1 - xi1, y1_mod - yi1)
                    xi1 = x1
                    yi1 = y1_mod
                    rsdot1_pressed = False

                    time.sleep(0.01)
                    rsdot1.setFill(cBlack)


            if f2 == 1:
                rsdot2.setFill(rsdot_pressed_color)
                y2_mod = int(y2 * 0.75)
                rsdot2.move(x2 - xi2, y2_mod - yi2)
                xi2 = x2
                yi2 = y2_mod
                rsdot2_pressed = True
            else:
                if rsdot2_pressed:
                    rsdot2.setFill(rsdot_released_color)
                    y2_mod = int(y2 * 0.75)
                    rsdot2.move(x2 - xi2, y2_mod - yi2)
                    xi2 = x2
                    yi2 = y2_mod
                    rsdot2_pressed = False

                    time.sleep(0.01)
                    rsdot2.setFill(cBlack)

    window.close()

def coord_resolution_slide():
    """ Проверка разрешения сенсорного экрана """

    log.info(u'Проверка разрешения сенсора (скольжение)')
    window = gr.GraphWin("PMF-6.0 Touch Screen", 1024, 768)
    window.setCoords(0, 767, 1023, 0)
    window.setBackground(cBlack)

    brdr = gr.Rectangle(gr.Point(0, 0), gr.Point(1023, 767))
    brdr.setOutline(cWhite)
    brdr.draw(window)

    tt = gr.Text(gr.Point(511, 60), u'Проверка разрешения сенсорного экрана '
                                    u'при жесте "скольжение"')
    tt.draw(window)
    tt.setTextColor(cWhite)
    tt.setSize(16)

    xy = gr.Text(gr.Point(511, 100), u'x:0, y:0')
    xy.setTextColor(cWhite)
    xy.setSize(28)
    xy.setStyle("bold")
    xy.draw(window)

    res_x = set()
    res_y = set()
    xy.setText('x:%s, y:%s' % (len(res_x), len(res_y)))

    while test_stop is False and test_next is False:
        QtCore.QCoreApplication.processEvents()
        if rs232_coord_out_q:
            x1, y1, x2, y2, f1, f2 = \
                coord_q(rs232_coord_out_q.popleft())
            if f1 == 1:
                y1_mod = int(y1 * 0.75)
                xi = x1
                yi = y1_mod

                if xi in res_x:
                    pass
                else:
                    ln = gr.Line(gr.Point(xi, 0), gr.Point(xi, 767))
                    ln.setWidth(1)
                    ln.setFill(cGreen)
                    ln.draw(window)
                res_x.add(xi)
                res_y.add(yi)
                xy.undraw()
                xy.setText('x:%s, y:%s' % (len(res_x), len(res_y)))
                xy.draw(window)
                tt.undraw()
                tt.draw(window)
    window.close()


def coord_resolution_tap():
    """ Проверка разрешения сенсорного экрана """

    log.info(u'Проверка разрешения сенсора (касание)')

    window = gr.GraphWin("PMF-6.0 Touch Screen", 1024, 768)
    window.setCoords(0, 767, 1023, 0)
    window.setBackground(cBlack)

    brdr = gr.Rectangle(gr.Point(0, 0), gr.Point(1023, 767))
    brdr.setOutline(cWhite)
    brdr.draw(window)

    tt = gr.Text(gr.Point(511, 60), u'Проверка разрешения сенсорного экрана '
                                    u'при жесте "касание"')
    tt.draw(window)
    tt.setTextColor(cWhite)
    tt.setSize(16)

    xy = gr.Text(gr.Point(511, 100), u'x:0, y:0')
    xy.setTextColor(cWhite)
    xy.setSize(28)
    xy.setStyle("bold")
    xy.draw(window)

    res_x = set()
    res_y = set()
    xy.setText('x:%s, y:%s' % (len(res_x), len(res_y)))
    is_pressed = False

    while test_stop is False and test_next is False:
        QtCore.QCoreApplication.processEvents()
        if rs232_coord_out_q:
            x1, y1, x2, y2, f1, f2 = \
                coord_q(rs232_coord_out_q.popleft())
            if is_pressed:
                if f1 == 0:
                    is_pressed = False
                    y1_mod = int(y1 * 0.75)
                    xi = x1
                    yi = y1_mod

                    if xi in res_x:
                        pass
                    else:
                        ln = gr.Line(gr.Point(xi, 0), gr.Point(xi, 767))
                        ln.setWidth(1)
                        ln.setFill(cGreen)
                        ln.draw(window)
                    res_x.add(xi)
                    res_y.add(yi)
                    xy.undraw()
                    xy.setText('x:%s, y:%s' % (len(res_x), len(res_y)))
                    xy.draw(window)
                    tt.undraw()
                    tt.draw(window)
            else:
                if f1 == 1:
                    is_pressed = True
    window.close()


def coord_8x8_grid_test(ser):

    rs.set_mode(ser, u'технологический')
    log.info(u'Проверка задержки выдачи координат')

    window = gr.GraphWin("PMF-6.0 Touch Screen", 1024, 768)
    window.setCoords(0, 767, 1023, 0)
    radius = 40
    window.setBackground(cBlack)



    for y in xrange(1, 8, 1):
        brdr = gr.Rectangle(gr.Point(0, 0), gr.Point(1023, y*96))
        brdr.setOutline(cGrey)
        brdr.draw(window)
    for x in xrange(1, 8, 1):
        brdr = gr.Rectangle(gr.Point(0, 0), gr.Point(x*128, 767))
        brdr.setOutline(cGrey)
        brdr.draw(window)

    brdr = gr.Rectangle(gr.Point(0, 0), gr.Point(1023, 767))
    brdr.setOutline(cWhite)
    brdr.draw(window)

    tt = gr.Text(gr.Point(511, 40), u'Проверка сенсорного экрана')
    tt.draw(window)
    tt.setTextColor(cWhite)
    tt.setSize(16)

    # tmr = gr.Text(gr.Point(511, 150), u'60')
    # tmr.draw(window)
    # tmr.setTextColor(cYellow)
    # tmr.setSize(36)

    xi1, yi1 = 2000, 2000
    rsdot1 = gr.Circle(gr.Point(xi1, yi1), radius)
    rsdot1.setFill(rsdot_pressed_color)
    rsdot1.draw(window)

    xi2, yi2 = 2000, 2000
    rsdot2 = gr.Circle(gr.Point(xi2, yi2), radius)
    rsdot2.setFill(rsdot_pressed_color)
    rsdot2.draw(window)

    xi3, yi3 = 2000, 2000
    mdcdot1 = gr.Circle(gr.Point(xi3, yi3), radius)
    mdcdot1.setFill(mdcdot_pressed_color)
    mdcdot1.draw(window)

    xi4, yi4 = 2000, 2000
    mdcdot2 = gr.Circle(gr.Point(xi4, yi4), radius)
    mdcdot2.setFill(mdcdot_pressed_color)
    mdcdot2.draw(window)

    rsdot1_pressed = False
    rsdot2_pressed = False

    while test_stop is False and test_next is False:
        #QtCore.QCoreApplication.processEvents()

        if t.rs232_coord_out_q:
            x1, y1, x2, y2, f1, f2 = t.coord_q(rs232_coord_out_q.popleft())
            if f1 == 1:
                rsdot1.setFill(rsdot_pressed_color)
                y1_mod = int(y1 * 0.75)
                rsdot1.move(x1 - xi1, y1_mod - yi1)
                xi1 = x1
                yi1 = y1_mod
                rsdot1_pressed = True
            else:
                if rsdot1_pressed:
                    rsdot1.setFill(rsdot_released_color)
                    y1_mod = int(y1 * 0.75)
                    rsdot1.move(x1 - xi1, y1_mod - yi1)
                    xi1 = x1
                    yi1 = y1_mod
                    rsdot1_pressed = False
            if f2 == 1:
                rsdot2.setFill(rsdot2_pressed_color)
                y2_mod = int(y2 * 0.75)
                rsdot2.move(x2 - xi2, y2_mod - yi2)
                xi2 = x2
                yi2 = y2_mod
                rsdot2_pressed = True
                tt.setText("p1 = %s , %s \n p2 = %s , %s" % (x1, y1_mod, x2, y2_mod))
            else:
                if rsdot2_pressed:
                    rsdot2.setFill(rsdot2_released_color)
                    y2_mod = int(y2 * 0.75)
                    rsdot2.move(x2 - xi2, y2_mod - yi2)
                    xi2 = x2
                    yi2 = y2_mod
                    rsdot2_pressed = False
    window.close()


def coord_zone():
    """
    Проверка выдачи коородинат выходящих за диапазон \n
    0 < x < 1024\n
    0 < y < 768
    """

    log.info(u'Проверка аномальных координат сенсора')

    window = gr.GraphWin("PMF-6.0 Touch Screen", 1024, 768)
    window.setCoords(0, 767, 1023, 0)
    window.setBackground(cBlack)

    border = 0
    brdr = gr.Rectangle(gr.Point(border, border),gr.Point(1023 - border,
                        767 - border))

    brdr.setOutline(cWhite)
    brdr.draw(window)

    tt = gr.Text(gr.Point(511, 60),
                 u'Проверка выдачи коородинат выходящих за диапазон\n'
                 u'0 < x < 1024\n'
                 u'0 < y < 768')
    tt.draw(window)
    tt.setTextColor(cWhite)
    tt.setSize(16)

    bad_coord_txt_pos_x = 120
    bad_coord_txt_pos_y = 30

    p1_pressed = False
    p2_pressed = False

    while test_stop is False and test_next is False:
        QtCore.QCoreApplication.processEvents()
        if rs232_coord_out_q:
            pack = rs232_coord_out_q.popleft()
            log.info(pack)
            x1, y1, x2, y2, f1, f2 = coord_q(pack)
            if f1 == 1:
                p1_pressed = True
                y1_mod = int(y1 * 0.75)
                xi = x1
                yi = y1_mod
                if (xi > 1100 or yi > 1100):
                    ln = gr.Line(gr.Point(511, 383), gr.Point(xi, yi))
                    ln.setFill(cRed)
                    ln.draw(window)
                    tt = gr.Text(gr.Point(bad_coord_txt_pos_x,
                                          bad_coord_txt_pos_y),
                                 'point 1: x=%s, y=%s' % (xi,yi))
                    tt.setFill(cRed)
                    tt.draw(window)
                    bad_coord_txt_pos_y += 20
            else:
                if p1_pressed is True:
                    p1_pressed = False
                    log.info('dot 1 released')
                    y1_mod = int(y1 * 0.75)
                    xi = x1
                    yi = y1_mod
                    if (xi > 1100 or yi > 1100):
                        ln = gr.Line(gr.Point(511, 383), gr.Point(xi, yi))
                        ln.setFill(cRed)
                        ln.draw(window)
                        tt = gr.Text(gr.Point(bad_coord_txt_pos_x,
                                              bad_coord_txt_pos_y),
                                     'point 1: x=%s, y=%s' % (xi,yi))
                        tt.setFill(cRed)
                        tt.draw(window)
                        bad_coord_txt_pos_y += 20

            if f2 == 1:
                p2_pressed = True
                y2_mod = int(y2 * 0.75)
                xi = x2
                yi = y2_mod
                if (xi > 1100 or yi > 1100) or (xi < 1 or yi < 1):
                    ln = gr.Line(gr.Point(511, 383), gr.Point(xi, yi))
                    ln.setFill(cYellow)
                    ln.draw(window)
                    tt = gr.Text(gr.Point(bad_coord_txt_pos_x,
                                          bad_coord_txt_pos_y),
                                 'point 2: x=%.5s, y=%.5s' % (xi,yi))
                    tt.setFill(cYellow)
                    tt.draw(window)
                    bad_coord_txt_pos_y += 20
            else:
                if p2_pressed:
                    p2_pressed = False
                    log.info('dot 2 released')
                    y2_mod = int(y2 * 0.75)
                    xi = x2
                    yi = y2_mod
                    log.info(x2)
                    log.info(y2)
                    if (xi > 1100 or yi > 1100) or (xi < 1 or yi < 1):
                        ln = gr.Line(gr.Point(511, 383), gr.Point(xi, yi))
                        ln.setFill(cYellow)
                        ln.draw(window)
                        tt = gr.Text(gr.Point(bad_coord_txt_pos_x,
                                              bad_coord_txt_pos_y),
                                     'point 2: x=%.5s, y=%.5s' % (x2,y2))
                        tt.setFill(cYellow)
                        tt.draw(window)
                        bad_coord_txt_pos_y += 20

    window.close()


def coord_drawer_232(ser):
    """
    Тест
    """



    log.info(u'Проверка сенсора (рисовалка)')
    rs.set_mode(ser, u'технологический')
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
        if t.rs232_coord_out_q:

            pack = t.rs232_coord_out_q.popleft()
           # log.info(pack)
            x1, y1, x2, y2, f1, f2 = \
                t.coord_q(pack)

            w.dots_process(x1, y1, x2, y2, f1, f2)
            if x2 > 950 and y2 > 950 and f2 == 1:
                break
    w.close()


def ts_raw_visualise(ser):
    time.sleep(0.1)
    rs.req_ts(ser)
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
            tt = gr.Text(gr.Point(511, 100), u'Проверка уровней сигналов')
            tt.draw(self.window)
            tt.setTextColor(cWhite)
            tt.setSize(16)

            tt = gr.Text(gr.Point(511, 600), u'Обновление данных по нажатию кнопки F1')
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
                    time.sleep(0.1)
                    rs.req_ts(ser)
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

        def draw_bars(self, lvl):
            x = -8
            dx = 24
            ddx = 0
            y = 8
            for n in xrange(1, 43):
                x = x + dx
                tt = gr.Text(gr.Point(x, y), '%s' % (n))
                tt.draw(self.window)
                if lvl[n-1] >= green_level_32:
                    tt.setTextColor(cGreen)
                if lvl[n-1] >= red_level_32 and lvl[n-1] < green_level_32:
                    tt.setTextColor(cYellow)
                if lvl[n-1] < red_level_32:
                    tt.setTextColor(cRed)
                tt.setSize(8)
                tt.setStyle("bold")
                if n % 2 == 0: x = x + ddx

            x = 1012
            y = -10
            dy = 24
            for n in xrange(43, 75):
                y = y + dy
                tt = gr.Text(gr.Point(x, y), '%s' % (n))
                tt.draw(self.window)
                if lvl[n-1] >= green_level_32:
                    tt.setTextColor(cGreen)
                if lvl[n-1] >= red_level_32 and lvl[n-1] < green_level_32:
                    tt.setTextColor(cYellow)
                if lvl[n-1] < red_level_32:
                    tt.setTextColor(cRed)
#                if (n == 43) or (n == 74): tt.setTextColor(cGrey)
                tt.setSize(8)
                tt.setStyle("bold")

        def upd_levels_32(self, lvl):
                brdr = gr.Rectangle(gr.Point(0, 0), gr.Point(1023, 767))
                brdr.setOutline(cBlack)
                brdr.setFill(cBlack)
                brdr.draw(self.window)

                tt = gr.Text(gr.Point(511, 100), u'Проверка уровней сигналов')
                tt.draw(self.window)
                tt.setTextColor(cWhite)
                tt.setSize(16)

                tt = gr.Text(gr.Point(511, 600),
                u'Обновление данных по нажатию кнопки F1\n Уровень сигнала должен быть не менее %s' % green_level_32)
                tt.draw(self.window)
                tt.setTextColor(cWhite)
                tt.setSize(16)

                self.draw_bars(lvl)

                xmin = 380
                x = xmin
                y = 200
                for n in xrange(42):
                    x = x + 40
                    if n % 8 == 0:
                        y = y + 14
                        x = xmin
                    tt = gr.Text(gr.Point(x, y), str(lvl[n]))
                    tt.draw(self.window)
                    if lvl[n] >= green_level_32:
                        tt.setTextColor(cGreen)
                    if lvl[n] >= red_level_32 and lvl[n] < green_level_32:
                        tt.setTextColor(cYellow)
                    if lvl[n] < red_level_32:
                        tt.setTextColor(cRed)
                    tt.setSize(10)

                for n in xrange(5):
                    x = xmin - 60
                    y = 214 + n * 14
                    tt = gr.Text(gr.Point(x, y), 'VD/VT %s-%s: ' % (n * 8 + 1, n * 8 + 8))
                    tt.draw(self.window)
                    tt.setTextColor(cWhite)
                    tt.setSize(10)

                x = xmin - 60
                y = y + 14
                tt = gr.Text(gr.Point(x, y), 'VD/VT 41-42: ')
                tt.draw(self.window)
                tt.setTextColor(cWhite)
                tt.setSize(10)

                for n in xrange(6, 10):
                    x = xmin - 60
                    y = 236 + n * 14
                    tt = gr.Text(gr.Point(x, y), 'VD/VT %s-%s: ' % (n * 8 + 1 - 6, n * 8 + 8 - 6))
                    tt.draw(self.window)
                    tt.setTextColor(cWhite)
                    tt.setSize(10)

                x = xmin
                y = 306
                for n in xrange(42, 74):
                    x = x + 40
                    if (n + 6) % 8 == 0:
                        y = y + 14
                        x = xmin
                    tt = gr.Text(gr.Point(x, y), str(lvl[n]))
                    tt.draw(self.window)
                    if lvl[n] >= green_level_32:
                        tt.setTextColor(cGreen)
                    if lvl[n] >= red_level_32 and lvl[n] < green_level_32:
                        tt.setTextColor(cYellow)
                    if lvl[n] < red_level_32:
                        tt.setTextColor(cRed)
                    tt.setSize(10)

        def upd_levels_menu(self, lvl):
                brdr = gr.Rectangle(gr.Point(0, 0), gr.Point(1023, 767))
                brdr.setOutline(cBlack)
                brdr.setFill(cBlack)
                brdr.draw(self.window)

                brdr = gr.Rectangle(gr.Point(256, 128), gr.Point(767, 639))
                brdr.setOutline(cWhite)
                brdr.setFill(cBlack)
                brdr.draw(self.window)

                tt = gr.Text(gr.Point(512, 158), u'СЕНСОРНЫЙ ЭКРАН')
                tt.draw(self.window)
                tt.setTextColor(cWhite)
                tt.setSize(10)

                brdr = gr.Rectangle(gr.Point(432, 400), gr.Point(592, 520))
                brdr.setOutline(cWhite)
                brdr.setFill(cBlack)
                brdr.draw(self.window)

                tt = gr.Text(gr.Point(512, 366), u'Максимум - 4095 ')
                tt.draw(self.window)
                tt.setTextColor(cWhite)
                tt.setSize(10)

                tt = gr.Text(gr.Point(432, 390), '1')
                tt.draw(self.window)
                tt.setTextColor(cWhite)
                tt.setSize(10)

                tt = gr.Text(gr.Point(586, 390), '42')
                tt.draw(self.window)
                tt.setTextColor(cWhite)
                tt.setSize(10)

                tt = gr.Text(gr.Point(604, 406), '43')
                tt.draw(self.window)
                tt.setTextColor(cWhite)
                tt.setSize(10)

                tt = gr.Text(gr.Point(604, 512), '74')
                tt.draw(self.window)
                tt.setTextColor(cWhite)
                tt.setSize(10)


#                self.draw_bars(lvl)

                xmin = 400
                x = xmin
                y = 180
                for n in xrange(42):
                    x = x + 40
                    if n % 8 == 0:
                        y = y + 14
                        x = xmin
                    tt = gr.Text(gr.Point(x, y), str(lvl[n]))
                    tt.draw(self.window)
                    if lvl[n] >= green_level_32:
                        tt.setTextColor(cWhite)
                    if lvl[n] >= red_level_32 and lvl[n] < green_level_32:
                        tt.setTextColor(cCian)
                    if lvl[n] < red_level_32:
                        tt.setTextColor(cCian)
                    tt.setSize(10)

                for n in xrange(5):
                    x = xmin - 60
                    y = 194 + n * 14
                    tt = gr.Text(gr.Point(x, y), 'VD/VT %s-%s: ' % (n * 8 + 1, n * 8 + 8))
                    tt.draw(self.window)
                    tt.setTextColor(cWhite)
                    tt.setSize(10)

                x = xmin - 60
                y = y + 14
                tt = gr.Text(gr.Point(x, y), 'VD/VT 41-42: ')
                tt.draw(self.window)
                tt.setTextColor(cWhite)
                tt.setSize(10)

                for n in xrange(6, 10):
                    x = xmin - 60
                    y = 210 + n * 14
                    tt = gr.Text(gr.Point(x, y), 'VD/VT %s-%s: ' % (n * 8 + 1 - 6, n * 8 + 8 - 6))
                    tt.draw(self.window)
                    tt.setTextColor(cWhite)
                    tt.setSize(10)

                x = xmin
                y = 280
                for n in xrange(42, 74):
                    x = x + 40
                    if (n + 6) % 8 == 0:
                        y = y + 14
                        x = xmin
                    tt = gr.Text(gr.Point(x, y), str(lvl[n]))
                    tt.draw(self.window)
                    if lvl[n] >= green_level_32:
                        tt.setTextColor(cWhite)
                    if lvl[n] >= red_level_32 and lvl[n] < green_level_32:
                        tt.setTextColor(cCian)
                    if lvl[n] < red_level_32:
                        tt.setTextColor(cCian)
                    tt.setSize(10)

#                brdr = gr.Rectangle(gr.Point(392, 380), gr.Point(632, 520))
#                brdr.setOutline(cWhite)
#                brdr.setFill(cBlack)
#                brdr.draw(self.window)




        def delitem(self, n):
            self.window.delItem(self.window.items[n])
        def close(self):
            self.window.close()

    w = CoordWindow(1024, 768)
    F1_pressed = False

    while 1:
        QtCore.QCoreApplication.processEvents()
        if t.rs232_coord_out_q:
            pack = t.rs232_coord_out_q.popleft()
            x1, y1, x2, y2, f1, f2 = \
                t.coord_q(pack)

            w.dots_process(x1, y1, x2, y2, f1, f2)
            if x2 > 950 and y2 > 950 and f2 == 1:
                break

        if t.rs232_ts_raw_32_q:
            lvl = t.rs232_ts_raw_32_q.popleft()
            lvl.popleft()
            lvl.popleft()
            lvl.popleft()
            lvl.popleft()
            signals = []
            for n in xrange(74):
                signals.append((lvl.popleft() << 7) + lvl.popleft());
            w.upd_levels_32(signals)

#        if t.rs232_ts_raw_32_q:
#            lvl = t.rs232_ts_raw_32_q.popleft()
#            lvl.popleft()
#            lvl.popleft()
#            lvl.popleft()
#            lvl.popleft()
#            signals = []
#            for n in xrange(74):
#                signals.append((lvl.popleft() << 7) + lvl.popleft());
#            w.upd_levels_menu(signals)


        if t.rs232_ts_raw_6x_q:
            lvl = t.rs232_ts_raw_6x_q.popleft()
            lvl.popleft()
            lvl.popleft()
            lvl.popleft()
            lvl.popleft()
            signals = []
            for n in xrange(92):
                signals.append((lvl.popleft() << 7) + lvl.popleft());
            w.upd_levels_6x(signals)

        if t.rs232_key_out_q:
           key_packet = t.rs232_key_out_q.popleft()
           if key_packet[4] == 0x21:
               F1_pressed = True
               F1_timer = time.clock()
        if (F1_pressed and (time.clock() - F1_timer)) > 0.5:
            F1_pressed = False
            F1_timer = time.clock()
            rs.req_ts(ser)




    w.close()



def coord_delay_squares(ser):

    rs.set_mode(ser, u'технологический')
    class CoordWindow:
        def __init__(self, width, height):
            self.window = gr.GraphWin("PMF Touch Screen", width, height)
            self.window.setCoords(0, 767, 1023, 0)
            self.window.setBackground(cBlack)
            self.left_corner_x = 0
            self.left_corner_y = 0
            self.sqare_side = 96
            self.square = gr.Rectangle(gr.Point(self.left_corner_x, self.left_corner_y), gr.Point(self.sqare_side, self.sqare_side))
            self.square.setOutline(cWhite)
            self.square.setFill(cBlue)
            self.square.draw(self.window)

        def proc(self, x1, y1, x2, y2, f1, f2):
            if f1 == 1:
                y1 = int(y1 * 0.75)
                if x1 > self.left_corner_x and x1 < self.left_corner_x + self.sqare_side:
                    if y1 > self.left_corner_y and y1 < self.left_corner_y + self.sqare_side:
                        new_x = random.randint(0, 1024 - self.sqare_side)
                        new_y = random.randint(0, 768 - self.sqare_side)
                        self.square.move(new_x - self.left_corner_x, new_y - self.left_corner_y)
                        self.left_corner_x = new_x
                        self.left_corner_y = new_y

        def close(self):
            self.window.close()

    w = CoordWindow(1024, 768)

    while test_stop is False and test_next is False:
        QtCore.QCoreApplication.processEvents()
        if t.rs232_coord_out_q:
            pack = t.rs232_coord_out_q.popleft()
            x1, y1, x2, y2, f1, f2 = \
                t.coord_q(pack)

            w.proc(x1, y1, x2, y2, f1, f2)
    w.close()


def tap_count(ser):

    rs.set_mode(ser, u'технологический')
    class CoordWindow:
        def __init__(self, width, height):
            self.window = gr.GraphWin("PMF Touch Screen", width, height)
            self.window.setCoords(0, 767, 1023, 0)
            self.window.setBackground(cBlack)
            self.left_corner_x = 0
            self.left_corner_y = 0
            self.sqare_side = 64
            self.square = gr.Rectangle(gr.Point(self.left_corner_x, self.left_corner_y), gr.Point(self.sqare_side, self.sqare_side))
            self.square.setOutline(cWhite)
            self.square.setFill(cBlue)
            self.square.draw(self.window)
            self.pressed = False
            self.timer = 0
            self.taps = 0
            self.halt = False

        def proc(self, x1, y1, x2, y2, f1, f2):
            if not self.halt:
                dx = self.sqare_side
                if f1 == 1:
                    self.pressed = True
                    if self.timer == 0:
                        self.timer = time.clock()
                else:
                    if self.pressed is True:
                        self.square.move(dx, 0)
                        self.left_corner_x += dx
                        self.taps += 1
                        print(self.taps)
                        self.pressed = False
                        if self.left_corner_x > 1024 - dx * 2:
                            tot_time = time.clock() - self.timer
                            ave_time = tot_time / self.taps
                            print(tot_time)
                            print(ave_time)
                            self.halt = True


        def close(self):
            self.window.close()

    w = CoordWindow(1024, 768)

    while test_stop is False and test_next is False:
        QtCore.QCoreApplication.processEvents()
        if t.rs232_coord_out_q:
            pack = t.rs232_coord_out_q.popleft()
            x1, y1, x2, y2, f1, f2 = \
                t.coord_q(pack)

            w.proc(x1, y1, x2, y2, f1, f2)
    w.close()


def coord_accuracy():
    """Тест точности определения координат
    Отображает круг радиусом (R + E) мм в координатах которые передал
    сенсорный экран
    R - минимальный радиус объекта касания (4 мм)
    E - заданная ошибка определения координат (2.6 мм)

    Опреатор касается экрана объектом диаметром 8 мм и смотрит не выступает ли
    объект за границы нарисованного круга. Если не выступает, то ошибка
    определения координат меньше заданной.
    """

    def process(x, y, x1, y1):
        #y1 = y1 * 0.75

        distance_x_pix = "{:.1f}".format(x1 - x) + ' pix  '

        distance_y_pix = "{:.1f}".format(y1 - y) + ' pix  '

        distance_in_mm = ("{:.1f}".format((math.sqrt(
                                ((x1 - x) * 0.2055) ** 2 +
                                ((y1 - y) * 0.2055) ** 2))) + ' mm  ' +
                                distance_x_pix + distance_y_pix)
        tt.setText(distance_in_mm)
    stick_rad_pix = (8 / 2) / 0.2055
    error_pix = 2.6 / 0.2055
    aim_radius_in_pixels = int(math.ceil((stick_rad_pix + error_pix)))
    window = gr.GraphWin("Touch Screen Accuracy", 1024, 768)
    window.setCoords(0, 767, 1023, 0)
    window.setBackground(cBlack)
    border = 0
    brdr = gr.Rectangle(gr.Point(border, border), gr.Point(1023 - border,
                                                           767 - border))
    brdr.setOutline(cWhite)
    brdr.draw(window)

    tt = gr.Text(gr.Point(511, 20), u'Проверка ошибки определения коородинат')
    tt.draw(window)
    tt.setTextColor(cWhite)
    tt.setSize(16)

    target_on = False
    dx = 0
    dy = 0
    x = 0
    y = 0

    while test_stop is False and test_next is False:
        QtCore.QCoreApplication.processEvents()

        if not target_on:
            if dx == 0 and dy == 0:
                pass
            else:
                x = x + dx
                y = y + dy

            aim = gr.Circle(gr.Point(x, y), aim_radius_in_pixels)
            aim.setOutline(cWhite)
            aim.setFill(cGrey)
            aim.draw(window)
            vln = gr.Line(gr.Point(x, 0), gr.Point(x, 767))
            vln.setFill(cGreen)
            vln.draw(window)
            hln = gr.Line(gr.Point(0, y), gr.Point(1023, y))
            hln.setFill(cGreen)
            hln.draw(window)
            target_on = True

        if t.rs232_coord_out_q:
            pack = t.rs232_coord_out_q.popleft()
            x1, y1, x2, y2, f1, f2 = t.coord_q(pack)

            y1 = y1 * 0.75
            target_on = False
            dx, dy = x1-x, y1-y
            for item in window.items[:]:
                item.undraw()
            tt.draw(window)

            process(x, y, x1, y1)

        if t.rs232_key_out_q:
            pack = t.rs232_key_out_q.popleft()
            key = pack[4]
            if key == 0x26:
                break
    window.close()

def coord_accuracy_measure(ser):
    """Тест точности определения координат
    Отображает круг радиусом (R + E) мм в произвольном месте экрана
    R - минимальный радиус объекта касания (4 мм)
    E - заданная ошибка определения координат (2.6 мм)
    Опреатор касается экрана объектом диаметром 8 мм и смотрит на
    расчитанную ошибку определения координат.
    """
    rs.set_mode(ser, u'технологический')
    def process(x, y, x1, y1):
        y1 = y1 * 0.75

        distance_x_pix = "{:.1f}".format(x1 - x) + ' pix  '

        distance_y_pix = "{:.1f}".format(y1 - y) + ' pix  '

        distance_in_mm = ("{:.1f}".format((math.sqrt(
                                ((x1 - x) * 0.2055) ** 2 +
                                ((y1 - y) * 0.2055) ** 2))) + ' mm  ' +
                                distance_x_pix + distance_y_pix)
        tt.setText(distance_in_mm)
    stick_rad_pix = (8 / 2) / 0.2055
    error_pix = 2.6 / 0.2055
    aim_radius_in_pixels = int(math.ceil((stick_rad_pix + error_pix)))
    window = gr.GraphWin("Touch Screen Accuracy", 1024, 768)
    window.setCoords(0, 767, 1023, 0)
    window.setBackground(cBlack)
    border = 0
    brdr = gr.Rectangle(gr.Point(border, border), gr.Point(1023 - border,
                                                           767 - border))
    brdr.setOutline(cWhite)
    brdr.draw(window)

    tt = gr.Text(gr.Point(511, 20), u'Проверка ошибки определения коородинат')
    tt.draw(window)
    tt.setTextColor(cWhite)
    tt.setSize(16)

    target_on = False
    dx = 0
    dy = 0
    x = 0
    y = 0

    while test_stop is False and test_next is False:
        QtCore.QCoreApplication.processEvents()

        if not target_on:
            if dx == 0 and dy == 0:
                x = random.randint(20, 1004)
                y = random.randint(20, 748)
            else:
                x = x + dx
                y = y + dy

            aim = gr.Circle(gr.Point(x, y), aim_radius_in_pixels)
            aim.setOutline(cWhite)
            aim.setFill(cGrey)
            aim.draw(window)
            vln = gr.Line(gr.Point(x, 0), gr.Point(x, 767))
            vln.setFill(cGreen)
            vln.draw(window)
            hln = gr.Line(gr.Point(0, y), gr.Point(1023, y))
            hln.setFill(cGreen)
            hln.draw(window)
            target_on = True

        if t.rs232_coord_out_q:
            pack = t.rs232_coord_out_q.popleft()
            x1, y1, x2, y2, f1, f2 = t.coord_q(pack)
            process(x, y, x1, y1)

        if t.rs232_key_out_q:
            pack = t.rs232_key_out_q.popleft()
            key = pack[4]
            if key == 0x21:
                target_on = False
                dx, dy = 0, 0
                for item in window.items[:]:
                    item.undraw()
                tt.draw(window)

            if key == 0x24:
                target_on = False
                dx, dy = 1, 0
                for item in window.items[:]:
                    item.undraw()
                tt.draw(window)

            if key == 0x25:
                target_on = False
                dx, dy = -1, 0
                for item in window.items[:]:
                    item.undraw()
                tt.draw(window)

            if key == 0x29:
                target_on = False
                dx, dy = 0, 1
                for item in window.items[:]:
                    item.undraw()
                tt.draw(window)

            if key == 0x2A:
                target_on = False
                dx, dy = 0, -1
                for item in window.items[:]:
                    item.undraw()
                tt.draw(window)

            if key == 0x26:
                break

    window.close()


def trash_mark(ser):
    def draw_marks(marks):
        for each in marks:
            x = each[0]
            y = each[1]
            mark = gr.Circle(gr.Point(x, y), 3)
            mark.setOutline(cWhite)
            mark.setFill(cRed)
            mark.draw(window)

    def draw_aim(x, y, bg):
        aim_radius_in_pixels = 3
        vln = gr.Line(gr.Point(x, 0), gr.Point(x, 767))
        vln.setFill(cGreen)
        vln.draw(window)
        hln = gr.Line(gr.Point(0, y), gr.Point(1023, y))
        hln.setFill(cGreen)
        hln.draw(window)
        aim = gr.Circle(gr.Point(x, y), aim_radius_in_pixels)
        if bg == 0:
            aim.setFill(cWhite)
            aim.setOutline(cGrey)
        else:
            aim.setFill(cWhite)
            aim.setOutline(cGrey)
        aim.draw(window)

    rs.set_mode(ser, u'технологический')
    marks = []

    window = gr.GraphWin("Marks", 1024, 768)
    window.setCoords(0, 767, 1023, 0)
    window.setBackground(cBlack)


    target_on = False
    dx = 0
    dy = 0
    x = 0
    y = 0
    bg = 0

    while test_stop is False and test_next is False:
        QtCore.QCoreApplication.processEvents()

        if not target_on:
            if dx == 0 and dy == 0:
                pass
            else:
                x = x + dx
                y = y + dy

            draw_aim(x, y, bg)
            target_on = True

        if t.rs232_coord_out_q:
            target_on = False
            pack = t.rs232_coord_out_q.popleft()
            x, y, x2, y2, f1, f2 = t.coord_q(pack)
            y = int(y * 0.75)
            dx, dy = 0, 0
            for item in window.items[:]:
                item.undraw()

        if t.rs232_key_out_q:
            pack = t.rs232_key_out_q.popleft()
            t.rs232_key_out_q.clear()
            key = pack[4]

            if key == 0x21:
                target_on = False
                dx, dy = 0, 0
                bg = 0
                window.setBackground(cBlack)
                for item in window.items[:]:
                    item.undraw()

            if key == 0x22:
                target_on = False
                dx, dy = 0, 0
                bg = 1
                window.setBackground(cWhite)
                for item in window.items[:]:
                    item.undraw()

            if key == 0x28:
                dx, dy = 0, 0
                marks.append((x,y))

            if key == 0x25:
                target_on = False
                dx, dy = 1, 0
                for item in window.items[:]:
                    item.undraw()

            if key == 0x24:
                target_on = False
                dx, dy = -1, 0
                for item in window.items[:]:
                    item.undraw()

            if key == 0x2A:
                target_on = False
                dx, dy = 0, 1
                for item in window.items[:]:
                    item.undraw()

            if key == 0x29:
                target_on = False
                dx, dy = 0, -1
                for item in window.items[:]:
                    item.undraw()

            if key == 0x26:
                log.info(marks)
                draw_marks(marks)
    window.close()


def border(ser):

    rs.set_mode(ser, u'технологический')

    window = gr.GraphWin("Border", 1024, 768)
    window.setCoords(0, 767, 1023, 0)
    window.setBackground(cBlack)
    xmin, xmax, ymin, ymax = 1000, 0, 1000, 0

    while test_stop is False and test_next is False:
        QtCore.QCoreApplication.processEvents()

        if t.rs232_coord_out_q:
            pack = t.rs232_coord_out_q.popleft()
            x, y, x2, y2, f1, f2 = t.coord_q(pack)
            y = int(y * 0.75)
            if xmin > x: xmin = x
            if xmax < x: xmax = x
            if ymin > y: ymin = y
            if ymax < y: ymax = y

            mark = gr.Point(x, y)
            mark.setOutline(cWhite)
            mark.setFill(cWhite)
            mark.draw(window)
            log.info("xmin=%s, xmax=%s, ymin=%s, ymax=%s" % (xmin, xmax, ymin, ymax))

    window.close()
