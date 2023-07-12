# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 21:03:48 2017

@author: User
"""

#from __future__ import division, print_function
#
#from PyQt4 import QtCore, QtGui
#
#import serial
#import rs
#import psh
#import vga
#import time
#import logging
#import sys
#import getcomports
#import graphics as gr
#import collections as coll
#import binascii
#import threading
#import gui
#import random
#import math
from test import *

def chk_111(ser):
    "ПМФ должен в режиме штатный по RS-232 выдавать OLD_OUT при касании сенсорного экрана"
    rs.set_mode(ser, u'штатный')
    time.sleep(0.2)
    clear_all_q()
    while True:    
        if old_xy:
            flag, x, y = old_xy.popleft()
            log.info(u'flag = %s, x = %s, y = %s' % (flag, x, y))
            if flag == 255: break 


def chk_112(ser):
    log.info(limiter)
    log.info(u'112 ПМФ должен в режиме штатный по RS-232 выдавать STS_OUT при получении SET_MODE')
    rs232_sts_out_q.clear()
    rs.set_mode(ser, u'штатный')
    sts_out = rx_specific_packet('STS_OUT', '232')
    if sts_out:
        if (sts_out[6] & 0x0A) == 0:
            log.info(u'установлен признак режима штатный')
        else:
            log.info(u'не установлен признак режима штатный')
    else:
        log.info(u'пакет STS_OUT не получен')
    rs232_sts_out_q.clear()
    rs.set_mode(ser, u'штатный')
    sts_out = rx_specific_packet('STS_OUT', '232')
    if sts_out:
        if (sts_out[6] & 0x0A) == 0:
            log.info(u'Установлен признак режима штатный')
        else:
            log.info(u'Не установлен признак режима штатный')        
    else:
        log.info(u'Пакет STS_OUT не получен')        


def chk_113(ser):
    log.info(limiter)
    log.info(u'113 ПМФ должен в режиме штатный по RS-232 принимать SET_MODE, устанавливать соответствующий режим работы и выдавать STS_OUT')
    chk01_set_mode(ser)


def chk_114(ser):
    log.info(limiter)
    log.info(u'114 ПМФ должен в режиме технологический по RS-232 выдавать KEY_OUT при нажатии на клавиши (в соответствующем режиме выдачи клавиш)')
    chk11_buttons(ser)


def chk_116(ser):
    log.info(limiter)
    log.info(u'116 ПМФ должен в режиме технологический по RS-232 выдавать COORD_OUT при касании сенсорного экрана')
    rs.set_mode(ser, u'технологический')
    log.info(u'touch the screen...')
    coord_out = rx_specific_packet('COORD_OUT', '232', 300)
    if coord_out:
        log.info(u'coord_out = %s' % coord_out)
    else:
        log.error(u'coord_out не принят')


def chk_117(ser):
    log.info(limiter)
    log.info(u'117 ПМФ должен в режиме технологический по RS-232 выдавать KEY_SET_OUT при нажатии на клавиши (в соответствующем режиме выдачи клавиш)')
    rs.set_mode(ser, u'технологический')
    rs.set_key_mode(ser, u'все кнопки')
    key_set_out = rx_specific_packet('KEY_SET_OUT', '232', 300)
    if key_set_out:
        log.info(u'key_set_out = %s' % key_set_out)
    else:
        log.error(u'key_set_out не принят')
        

def chk_118(ser):
    log.info(limiter)
    log.info(u'118 ПМФ должен в режиме технологический по RS-232 принимать REQ_STS и выдавать STS_OUT')
    rs.set_mode(ser, u'технологический')
    time.sleep(0.2)
    clear_all_q()
    rs.req_sts(ser)
    sts_out = rx_specific_packet('STS_OUT', '232')
    if sts_out:
        log.info(u'STS_OUT = %s' % sts_out)
    else:
        log.error(u'Пакет STS_OUT не получен')
    clear_all_q()


def chk_119(ser):
    log.info(limiter)
    log.info(u'119 ПМФ должен в режиме технологический по RS-232 принимать SET_PARAM и выдавать STS_OUT')
    rs.set_mode(ser, u'технологический')
    time.sleep(0.2)
    clear_all_q()
    param = [0xFE, 0x60, 0x60, 0x60, 0x1A, 0x1A, 0x1A, 0x68, 0x00, 0x00, 0x00, 0x07, 0x2A, 0xF0, 0x00, 0x00]
    rs.set_param(ser, param)
    sts_out = rx_specific_packet('STS_OUT', '232')
    if sts_out:
        log.info(u'STS_OUT = %s' % sts_out)
    else:
        log.error(u'Пакет STS_OUT не получен')
    clear_all_q()


def chk_120(ser):
    log.info(limiter)
    log.info(u'120 ПМФ должен в режиме технологический по RS-232 принимать SET_DEFAULT и выдавать STS_OUT')
    rs.set_mode(ser, u'технологический')
    time.sleep(0.2)
    clear_all_q()
    rs.set_default(ser)
    sts_out = rx_specific_packet('STS_OUT', '232')
    if sts_out:
        log.info(u'STS_OUT = %s' % sts_out)
    else:
        log.error(u'Пакет STS_OUT не получен')
    clear_all_q()


def chk_121(ser):
    log.info(limiter)
    log.info(u'121 ПМФ должен в режиме технологический по RS-232 принимать SAVE_PARAM и выдавть STS_OUT')
    rs.set_mode(ser, u'технологический')
    time.sleep(0.2)
    clear_all_q()
    rs.save_param(ser)
    sts_out = rx_specific_packet('STS_OUT', '232')
    if sts_out:
        log.info(u'STS_OUT = %s' % sts_out)
    else:
        log.error(u'Пакет STS_OUT не получен')
    clear_all_q()


def chk_122(ser):
    log.info(limiter)
    log.info(u'122 ПМФ должен в режиме технологический по RS-232 принимать SET_MODE и выдавать STS_OUT')
    rs.set_mode(ser, u'технологический')
    time.sleep(0.2)
    clear_all_q()
    rs.set_mode(ser, u'технологический')
    sts_out = rx_specific_packet('STS_OUT', '232')
    if sts_out:
        log.info(u'STS_OUT = %s' % sts_out)
    else:
        log.error(u'Пакет STS_OUT не получен')
    clear_all_q()


def chk_123(ser):
    log.info(limiter)
    log.info(u'123 ПМФ должен в режиме технологический по RS-232 принимать SET_BRIT')
    brightness = 0
    rs.set_mode(ser, u'технологический')
    while brightness < 255:
        rs.set_brit(ser, brightness)
        time.sleep(0.01)
        brightness += 1


def chk_124(ser):
    log.info(limiter)
    log.info(u'124 ПМФ должен в режиме технологический по RS-232 принимать SET_KEY_MODE')
    rs.set_mode(ser, u'технологический')
    rs.set_key_mode(ser, u'одна кнопка')
    rs.req_sts(ser)
    sts = rx_specific_packet('STS_OUT', '232')
    log.info(u'одна кнопка = %s' % sts)
    rs.set_key_mode(ser, u'все кнопки')
    rs.req_sts(ser)
    sts = rx_specific_packet('STS_OUT', '232')
    log.info(u'все кнопки = %s' % sts)
    time.sleep(1)
    rs.set_key_mode(ser, u'одна кнопка')


def chk_125(ser):
    log.info(limiter)
    log.info(u'125 ПМФ должен в режиме расширенный по RS-232 выдавать KEY_OUT при нажатии на клавиши (в соответствующем режиме выдачи клавиш)')
    rs.set_mode(ser, u'расширенный')
    rs.set_key_mode(ser, u'одна кнопка')
    key_test(one_point = True)
    

def chk_126(ser):
    log.info(limiter)
    log.info(u'126 ПМФ должен в режиме расширенный по RS-232 выдавать COORD_OUT при касании сенсорного экрана')
    rs.set_mode(ser, u'расширенный')
    coord_drawer_232()
    

def chk_127(ser):
    log.info(limiter)
    log.info(u'127 ПМФ должен в режиме расширенный по RS-232 выдавать KEY_SET_OUT при нажатии на клавиши (в соответствующем режиме выдачи клавиш)')
    rs.set_mode(ser, u'расширенный')
    rs.set_key_mode(ser, u'все кнопки')
    key_test(one_point = False)
    rs.set_key_mode(ser, u'одна кнопка')
    

def chk_128(ser):
    rs.set_brit(ser, 0xFE)
    log.info('asdsad')
    log.info(u'128 ПМФ должен в режиме расширенный по RS-232 принимать REQ_STS и выдавать STS_PMF')
#    rs.set_mode(ser, u'расширенный')
#    time.sleep(0.2)
#    clear_all_q()
#    rs.req_sts(ser)
#    sts_pmf = rx_specific_packet('STS_PMF', '232')
#    if sts_pmf:
#        log.info(u'STS_PMF = %s' % sts_pmf)
#    else:
#        log.error(u'Пакет STS_PMF не получен')
#    clear_all_q()


def chk_129(ser):
    log.info(limiter)
    log.info(u'129 МФ должен в режиме расширенный по RS-232 принимать SET_PARAM и выдавать STS_OUT')
    rs.set_mode(ser, u'расширенный')
    time.sleep(0.2)
    clear_all_q()
    
    vparam = 0xFE
    Ramp = 0x50
    Gamp = 0x50
    Bamp = 0x50
    Roff = 0x11
    Goff = 0x11
    Boff = 0x11
    Phase = 0x66
    Hoff = 0x00
    Voff = 0x00
    Topros = 0x06
    Tauto = 0x07
    vidif = 0xFE    
    
    param = [vparam, Ramp, Gamp, Bamp, Roff, Goff, Boff, Phase, Hoff, Voff, 0x00, Topros, Tauto, vidif, 0x00, 0x00]
    rs.set_param(ser, param)
    sts_out = rx_specific_packet('STS_OUT', '232')


    if sts_out:
        log.info(u'STS_OUT = %s' % sts_out)
        if (Ramp == sts_out[11] and
        Gamp == sts_out[12] and 
        Bamp == sts_out[13] and
        Roff == sts_out[14] and
        Goff == sts_out[15] and
        Boff == sts_out[16] and
        Phase == sts_out[17] and
        Hoff == sts_out[18] and
        Voff == sts_out[19] and
        Topros == sts_out[28] and
        Tauto == sts_out[29]):
            log.info(u'параметры совпадают')
        else:
            log.error(u'Параметры не совпадают')
    else:
        log.error(u'Пакет STS_OUT не получен')
    clear_all_q()


def chk_130(ser):
    log.info(limiter)
    log.info(u'130 ПМФ должен в режиме расширенный по RS-232 принимать SET_DEFAULT и выдавать STS_OUT')
    rs.set_mode(ser, u'расширенный')
    time.sleep(0.2)
    clear_all_q()
    rs.set_default(ser)
    sts_out = rx_specific_packet('STS_OUT', '232')
    if sts_out:
        log.info(u'STS_OUT = %s' % sts_out)
    else:
        log.error(u'Пакет STS_OUT не получен')
    clear_all_q()


def chk_131(ser):
    log.info(limiter)
    log.info(u'131 ПМФ должен в режиме расширенный по RS-232 принимать SAVE_PARAM и выдавать STS_OUT')
    rs.set_mode(ser, u'расширенный')
    time.sleep(0.2)
    clear_all_q()
    rs.save_param(ser)
    sts_out = rx_specific_packet('STS_OUT', '232')
    if sts_out:
        log.info(u'STS_OUT = %s' % sts_out)
    else:
        log.error(u'Пакет STS_OUT не получен')
    clear_all_q()


def chk_132(ser):
    log.info(limiter)
    log.info(u'132 ПМФ должен в режиме расширенный по RS-232 принимать SET_MODE и выдавать STS_PMF')
    clear_all_q()
    rs.set_mode(ser, u'расширенный')
    sts_pmf = rx_specific_packet('STS_PMF', '232')
    if sts_pmf:
        log.info(u'STS_PMF = %s' % sts_pmf)
    else:
        log.error(u'Пакет STS_PMF не получен')
    clear_all_q()
    

def chk_133(ser):
    log.info(limiter)
    log.info(u'133 ПМФ должен в режиме расширенный по RS-232 принимать SET_BRIT')
    brightness = 0
    rs.set_mode(ser, u'расширенный')
    while brightness < 255:
        rs.set_brit(ser, brightness)
        time.sleep(0.01)
        brightness += 1


def chk_134(ser):
    log.info(limiter)
    log.info(u'134 ПМФ должен в режиме расширенный по RS-232 принимать SET_KEY_MODE')
    rs.set_mode(ser, u'расширенный')
    rs.set_key_mode(ser, u'одна кнопка')
    rs.req_sts(ser)
    sts = rx_specific_packet('STS_PMF', '232')
    log.info(u'одна кнопка = %s' % sts)
    rs.set_key_mode(ser, u'все кнопки')
    rs.req_sts(ser)
    sts = rx_specific_packet('STS_PMF', '232')
    log.info(u'все кнопки = %s' % sts)
    rs.set_key_mode(ser, u'одна кнопка')
        

def chk_135(ser):
    log.info(limiter)
    log.info(u'135 ПМФ должен в режиме расширенный по RS-232 принимать SET_VGA и выдавать STS_VGLV')
    rs.set_mode(ser, u'расширенный')    
    data = [0x11, 0x22 ,0x33, 0x44, 0x55, 0x66, 0x77, 0x00, 0x00]
    rs.set_vga(ser, data)
    sts_vglv = rx_specific_packet('STS_VGLV', '232')
    if sts_vglv:
        log.info(u'STS_VGLV = %s' % sts_vglv)
    else:
        log.error(u'Пакет STS_VGLV не получен')
    clear_all_q()


def chk_136(ser):
    log.info(limiter)
    log.info(u'136 МФ должен в режиме расширенный по RS-232 принимать SET_KEYs и выдавать STS_PMF')
    rs.set_mode(ser, u'расширенный')
    Top = random.randint(5, 254)
    Tauto = random.randint(5, 254)
    data = [Top, Tauto]
    rs.set_keys(ser, data)
    sts = rx_specific_packet('STS_PMF', '232')
    if sts:
        log.info(u'STS_PMF = %s' % sts)
        if sts[39] == Top and sts[40] == Tauto:
            log.info(u'Параметры в STS_PMF соответствуют переданным в SET_KEYS')
        else:
            log.error(u'Параметры в STS_PMF не соответствуют переданным в SET_KEYS')
    else:
        log.error(u'Пакет STS_PMF не получен')
    clear_all_q()


def chk_137(ser):
    log.info(limiter)
    log.info(u'137 ПМФ должен в режиме расширенный по RS-232 принимать SET_VPIPE и выдавать STS_VPIPE')
    rs.set_mode(ser, u'расширенный')
    data = [i for i in xrange(0, 93)]
    rs.set_vpipe(ser, data)
    sts = rx_specific_packet('STS_VPIPE', '232')
    if sts:
        log.info(u'STS_VPIPE = %s' % sts)
    else:
        log.error(u'Пакет STS_VPIPE не получен')
    clear_all_q()


def chk_144(ser):
    log.info(limiter)
    log.info(u'144 ПМФ должен в режиме расширенный по RS-232 принимать REQ_STS_ETH1 и выдавать STS_ETH1')
    rs.set_mode(ser, u'расширенный')
    time.sleep(0.2)
    clear_all_q()
    rs.req_sts_eth1(ser)
    sts_eth1 = rx_specific_packet('STS_ETH1', '232')
    if sts_eth1:
        log.info(u'STS_ETH1 = %s' % sts_eth1)
    else:
        log.error(u'Пакет STS_ETH1 не получен %s' % sts_eth1)
    clear_all_q()


def chk_145(ser):
    log.info(limiter)
    log.info(u'145 ПМФ должен в режиме расширенный по RS-232 принимать REQ_STS_ETH2 и выдавать STS_ETH2')
    rs.set_mode(ser, u'расширенный')
    time.sleep(0.2)
    clear_all_q()
    rs.req_sts_eth2(ser)
    sts_eth2 = rx_specific_packet('STS_ETH2', '232')
    if sts_eth2:
        log.info(u'STS_ETH2 = %s' % sts_eth2)
    else:
        log.error(u'Пакет STS_ETH2 не получен')
    clear_all_q()


def chk_146(ser):
    log.info(limiter)
    log.info(u'146 ПМФ должен в режиме расширенный по RS-232 принимать REQ_STS_VPr1 и выдавать STS_VPr1')
    rs.set_mode(ser, u'расширенный')
    time.sleep(0.2)
    clear_all_q()
    rs.req_sts_vpr1(ser)
    sts_vpr1 = rx_specific_packet('STS_VPr1', '232')
    if sts_vpr1:
        log.info(u'STS_VPr1 = %s' % sts_vpr1)
    else:
        log.error(u'Пакет STS_VPr1 не получен')
    clear_all_q()


def chk_147(ser):
    log.info(limiter)
    log.info(u'147 ПМФ должен в режиме расширенный по RS-232 принимать REQ_STS_VPr2 и выдавать STS_VPr2')
    rs.set_mode(ser, u'расширенный')
    time.sleep(0.2)
    clear_all_q()    
    rs.req_sts_vpr2(ser)
    sts_vpr2 = rx_specific_packet('STS_VPr2', '232')
    if sts_vpr2:
        log.info(u'STS_VPr2 = %s' % sts_vpr2)
    else:
        log.error(u'Пакет STS_VPr2 не получен')
    clear_all_q()


def chk_148(ser):
    log.info(limiter)
    log.info(u'148 Требование: ПМФ должен в режиме расширенный по RS-232 принимать REQ_STS_VPr3 и выдавать STS_VPr3')
    rs.set_mode(ser, u'расширенный')
    time.sleep(0.2)
    clear_all_q()    
    rs.req_sts_vpr3(ser)
    sts_vpr3 = rx_specific_packet('STS_VPr3', '232')
    if sts_vpr3:
        log.info(u'STS_VPr3 = %s' % sts_vpr3)
    else:
        log.error(u'Пакет STS_VPr3 не получен')
    clear_all_q()


def chk_149(ser):
    log.info(limiter)
    log.info(u'149 Требование: ПМФ должен в режиме расширенный по RS-232 принимать REQ_STS_VPr4 и выдавать STS_VPr4')
    rs.set_mode(ser, u'расширенный')
    time.sleep(0.2)
    clear_all_q()    
    rs.req_sts_vpr4(ser)
    sts_vpr4 = rx_specific_packet('STS_VPr4', '232')
    if sts_vpr4:
        log.info(u'STS_VPr4 = %s' % sts_vpr4)
    else:
        log.error(u'Пакет STS_VPr4 не получен')
    clear_all_q()


def chk_150(ser):
    log.info(limiter)
    log.info(u'150 ПМФ должен в режиме расширенный по RS-232 принимать REQ_STS_VPIPE и выдавать STS_VPIPE')
    rs.set_mode(ser, u'расширенный')
    time.sleep(0.2)
    clear_all_q()
    rs.req_sts_vpipe(ser)
    sts_vpipe = rx_specific_packet('STS_VPIPE', '232')
    if sts_vpipe:
        log.info(u'STS_VPIPE = %s' % sts_vpipe)
    else:
        log.error(u'Пакет STS_VPIPE не получен')
    clear_all_q()


def chk_151(ser):
    log.info(limiter)
    log.info(u'151 ПМФ должен в режиме расширенный по RS-232 принимать REQ_STS_VGLV и выдавать STS_VGLV')
    rs.set_mode(ser, u'расширенный')
    time.sleep(0.2)
    clear_all_q()
    rs.req_sts_vglv(ser)
    sts_vglv = rx_specific_packet('STS_VGLV', '232')
    if sts_vglv:
        log.info(u'STS_VGLV = %s' % sts_vglv)
    else:
        log.error(u'Пакет STS_VGLV не получен')
    clear_all_q()


def chk_152(ser):
    log.info(limiter)
    log.info(u'ПМФ должен в режиме расширенный по RS-232 принимать REQ_STS_OVHP и выдавать STS_OVHP')
    rs.set_mode(ser, u'расширенный')
    rs.req_sts_ovhp(ser)
    sts_ovhp = rx_specific_packet('STS_OVHP', '232')
    if sts_ovhp:
        log.info(u'STS_OVHP = %s' % sts_ovhp)
    else:
        log.error(u'Пакет STS_OVHP не получен')
    clear_all_q()


def chk_153(ser):
    log.info(limiter)
    log.info(u'153 ПМФ должен в режиме расширенный по RS-232 принимать SET_SPLASH и выдавать STS_PMF')
    rs.set_mode(ser, u'расширенный')
    rs.set_splash(ser, u'вкл')
    sts_pmf = rx_specific_packet('STS_PMF', '232')
    if sts_pmf:
        log.info(u'STS_PMF = %s' % sts_pmf)
    else:
        log.error(u'Пакет STS_PMF не получен')
    clear_all_q()
    rs.set_splash(ser, u'выкл')
    sts_pmf = rx_specific_packet('STS_PMF', '232')
    if sts_pmf:
        log.info(u'STS_PMF = %s' % sts_pmf)
    else:
        log.error(u'Пакет STS_PMF не получен')
    clear_all_q()


def chk_154(ser):
    log.info(limiter)
    log.info(u'154 ПМФ должен в режиме расширенный по RS-232 принимать SET_HEATER и выдавать STS_PMF')
    rs.set_mode(ser, u'расширенный')
    rs.set_heater(ser, [0, 0])
    sts_pmf = rx_specific_packet('STS_PMF', '232')
    if sts_pmf:
        log.info(u'STS_PMF = %s' % sts_pmf)
    else:
        log.error(u'Пакет STS_PMF не получен')
    clear_all_q()


def chk_155(ser):
    log.info(limiter)
    log.info(u'155 ПМФ должен в режиме расширенный по RS-232 принимать SET_OVHP и выдавать STS_OVHP')
    rs.set_mode(ser, u'расширенный')
    rs.set_ovhp(ser, [0, 0, 0, 0, 0, 0])
    sts_ovhp = rx_specific_packet('STS_OVHP', '232')
    if sts_ovhp:
        log.info(u'STS_OVHP = %s' % sts_ovhp)
    else:
        log.error(u'Пакет STS_OVHP не получен')
    clear_all_q()


def chk_156(ser):
    log.info(limiter)
    log.info(u'156 ПМФ должен в режиме расширенный по RS-232 принимать SET_ID')
    rs.set_mode(ser, u'расширенный')
    sts = rx_specific_packet('STS_PMF', '232')
    if sts:
        ID = sts[4]
        SN = [sts[15], sts[16], sts[17], sts[18], sts[19], sts[20], sts[21], sts[22], sts[23]]
        log.info(u'ID = %s, SN = %s' % (ID, SN))
        if ID == PMF_ID: log.info(u'Pass. Идентификатор ПМФ считанный и ожидаемый совпали')
        else: log.info(u'Fail. Идентификатор ПМФ считанный и ожидаемый не совпали!')
        if SN == PMF_SN: log.info(u'Pass. Заводской номер ПМФ считанный и ожидаемый совпали')
        else: log.info(u'Fail. Заводской номер ПМФ считанный и ожидаемый не совпали!')
    else:
        log.error(u'Пакет STS_PMF не получен')
    new_data = [0x11, 48, 48, 48, 51, 0, 0, 0, 0, 0]
    rs.set_ID(ser, new_data)
    clear_all_q()
    rs.set_mode(ser, u'расширенный')
    NEW_ID = 0x11
    NEW_SN = [48, 48, 48, 51, 0, 0, 0, 0, 0]
    sts = rx_specific_packet('STS_PMF', '232')
    if sts:
        ID = sts[4]
        SN = [sts[15], sts[16], sts[17], sts[18], sts[19], sts[20], sts[21], sts[22], sts[23]]
        log.info(u'ID = %s, SN = %s' % (ID, SN))
        if ID == NEW_ID: log.info(u'Pass. Идентификатор ПМФ считанный и ожидаемый совпали')
        else: log.info(u'Fail. Идентификатор ПМФ считанный и ожидаемый не совпали!')
        if SN == NEW_SN: log.info(u'Pass. Заводской номер ПМФ считанный и ожидаемый совпали')
        else: log.info(u'Fail. Заводской номер ПМФ считанный и ожидаемый не совпали!')
    else:
        log.error(u'Пакет STS_PMF не получен')
    clear_all_q()


def chk_157(psh_ser):
    """
    Требование: ПМФ должна переходить в штатный режим работы по включению
    Источник: 1_3.3
    """
    ps = psh.psh3610(psh_ser)
    ps.setup(27, 2, 30, 0, 1, 0.5)
    time.sleep(3)



def chk_158(ser):
    log.info(limiter)
    log.info(u'158 ПМФ должна устанавливать режим работы по команде из пакета SET_MODE по RS-232')
    chk01_set_mode(ser)


def chk_161(ser):
    log.info(limiter)
    log.info(u'161 ПМФ должна выдавать OLD_OUT во время касания сенсорного экрана в режиме штатный')
    rs.set_mode(ser, u'штатный')
    clear_all_q()
    while 1:
        if old_xy:
            old_out = old_xy.pop()
            f = old_out[0]
            x = old_out[1]
            y = old_out[2]
            log.info(u'OLD_OUT: F = %s, X = %s, Y = %s' % (f,x,y))
            if x > 950 and y > 950: break

        
def chk_162(ser):
    log.info(limiter)
    log.info(u'162 ПМФ должна по прекращению касания сенсора выдавать пакет OLD_OUT с флагом прекращения касания (байт 1 равен Ffh) в режиме штатный')
    rs.set_mode(ser, u'штатный')
    time.sleep(0.2)
    clear_all_q()
    while 1:
        if old_xy:
            old_out = old_xy.pop()
            f = old_out[0]
            x = old_out[1]
            y = old_out[2]
            log.info(u'OLD_OUT: F = %s, X = %s, Y = %s' % (f,x,y))
            if (f == 255):
                log.info(u'OLD_OUT получен признак отжатия')
            if x > 950 and y > 950: break


def chk_168(ser):
    log.info(limiter)
    log.info(u'168 ПМФ должен выдавать свой идентификатор в STS_OUT')
    clear_all_q()
    rs.set_mode(ser, u'технологический')
    sts_out = rx_specific_packet('STS_OUT', '232')
    if sts_out:
        if sts_out[4] == exp_pmf_id:
            log.info('ID pass = %s' % sts_out[4])
        else:
            log.error(u'ID fail = %s' % sts_out[4])
    else:
        log.error(u'Пакет STS_OUT не получен')        

def chk_169(ser):
    log.info(limiter)
    log.info(u'169 ПМФ должен выдавать версию ПО в STS_OUT')
    clear_all_q()
    rs.set_mode(ser, u'технологический')
    sts_out = rx_specific_packet('STS_OUT', '232')
    if sts_out:
        if sts_out[5] == exp_soft_id:
            log.info('SOFT ID pass')

def chk_170(ser):
    log.info(limiter)
    log.info(u'170 ПМФ должен выдавать режим ПМФ в STS_OUT')
    clear_all_q()
    rs.set_mode(ser, u'технологический')
    sts_out = rx_specific_packet('STS_OUT', '232')
    if sts_out:
        if (sts_out[6] & 0x0A) == 2:
            log.info('pass')


def chk_171(ser):
    log.info(limiter)
    log.info(u'171 ПМФ должен выдавать режим передачи клавиш в STS_OUT')
    clear_all_q()
    rs.set_mode(ser, u'технологический')
    rs.set_key_mode(ser, u'одна кнопка')
    rs.req_sts(ser)
    sts_out = rx_specific_packet('STS_OUT', '232')
    if sts_out:
        if (sts_out[6] & 0x04) == 0:
            log.info('pass')
        else:
            log.error('fail %s' % sts_out)
            
    rs.set_key_mode(ser, u'все кнопки')
    rs.req_sts(ser)
    sts_out = rx_specific_packet('STS_OUT', '232')
    if sts_out:
        if (sts_out[6] & 0x04) == 4:
            log.info('pass')
        else:
            log.error('fail %s' % sts_out)
            
    rs.set_key_mode(ser, u'одна кнопка')
    rs.req_sts(ser)
    sts_out = rx_specific_packet('STS_OUT', '232')
    if sts_out:
        if (sts_out[6] & 0x04) == 0:
            log.info('pass')
        else:
            log.error('fail %s' % sts_out)
            

def chk_172(ser):
    log.info(limiter)
    log.info(u'172 ПМФ должен выдавать признак включения экрана-заставки в STS_OUT')
    clear_all_q()
    rs.set_mode(ser, u'технологический')
    rs.set_splash(ser, u'вкл')
    rs.req_sts(ser)
    sts_out = rx_specific_packet('STS_OUT', '232')
    if sts_out:
        if (sts_out[6] & 0x10) == 0x10:
            log.info('pass')
        else:
            log.error('fail %s' % sts_out)
    rs.set_splash(ser, u'выкл')
    rs.req_sts(ser)
    sts_out = rx_specific_packet('STS_OUT', '232')
    if sts_out:
        if (sts_out[6] & 0x10) == 0:
            log.info('pass')
        else:
            log.error('fail %s' % sts_out)


def chk_173(ser):
    log.info(limiter)
    log.info(u'173 ПМФ должен выдавать коэффициент усиления R в STS_OUT')
    rs.set_mode(ser, u'технологический')
    R = 0
    while R < MAX_VAL:
        param = [0xFE, R, 0x60, 0x60, 0x1A, 0x1A, 0x1A, 0x68, 0x00, 0x00, 0x00, 0x07, 0x2A, 0xFE, 0x00, 0x00]
        rs.set_param(ser, param)
        time.sleep(delay_sts_readback)
        clear_all_q()
        rs.req_sts(ser)
        #time.sleep(0.1)
        sts_out = rx_specific_packet('STS_OUT', '232')
        if sts_out:
            if sts_out[11] == R:
                log.info('pass')
            else:
                log.error('fail %s <> %s' % (R, sts_out[11]))
        R += 1


def chk_174(ser):
    log.info(limiter)
    log.info(u'174 ПМФ должен выдавать коэффициент усиления G в STS_OUT')
    rs.set_mode(ser, u'технологический')
    G = 0
    while G < MAX_VAL:
        param = [0xFE, 0x60, G, 0x60, 0x1A, 0x1A, 0x1A, 0x68, 0x00, 0x00, 0x00, 0x07, 0x2A, 0xF0, 0x00, 0x00]
        rs.set_param(ser, param)
        time.sleep(delay_sts_readback)
        clear_all_q()
        rs.req_sts(ser)
        sts_out = rx_specific_packet('STS_OUT', '232')
        if sts_out:
            if sts_out[12] == G:
                log.info('pass')
            else:
                log.error('fail %s <> %s' % (G, sts_out[12]))
        G += 1


def chk_175(ser):
    log.info(limiter)
    log.info(u'175 ПМФ должен выдавать коэффициент усиления B в STS_OUT')
    rs.set_mode(ser, u'технологический')
    B = 0
    while B < MAX_VAL:
        param = [0xFE, 0x60, 0x60, B, 0x1A, 0x1A, 0x1A, 0x68, 0x00, 0x00, 0x00, 0x07, 0x2A, 0xF0, 0x00, 0x00]
        rs.set_param(ser, param)
        time.sleep(delay_sts_readback)
        clear_all_q()
        rs.req_sts(ser)
        sts_out = rx_specific_packet('STS_OUT', '232')
        if sts_out:
            if sts_out[13] == B:
                log.info('pass')
            else:
                log.error('fail %s <> %s' % (B, sts_out[13]))
        B += 1
        

def chk_176(ser):
    log.info(limiter)
    log.info(u'176 ПМФ должен выдавать смещение R в STS_OUT')
    rs.set_mode(ser, u'технологический')
    R = 0
    while R < MAX_VAL:
        param = [0xFE, 0x60, 0x60, 0x60, R, 0x1A, 0x1A, 0x68, 0x00, 0x00, 0x00, 0x07, 0x2A, 0xF0, 0x00, 0x00]
        rs.set_param(ser, param)
        time.sleep(delay_sts_readback)
        clear_all_q()
        rs.req_sts(ser)
        sts_out = rx_specific_packet('STS_OUT', '232')
        if sts_out:
            if sts_out[14] == R:
                log.info('pass')
            else:
                log.error('fail %s <> %s' % (R, sts_out[14]))
        R += 1


def chk_177(ser):
    log.info(limiter)
    log.info(u'177 ПМФ должен выдавать смещение G в STS_OUT')
    rs.set_mode(ser, u'технологический')
    G = 0
    while G < MAX_VAL:
        param = [0xFE, 0x60, 0x60, 0x60, 0x1A, G, 0x1A, 0x68, 0x00, 0x00, 0x00, 0x07, 0x2A, 0xF0, 0x00, 0x00]
        rs.set_param(ser, param)
        time.sleep(delay_sts_readback)
        clear_all_q()
        rs.req_sts(ser)
        sts_out = rx_specific_packet('STS_OUT', '232')
        if sts_out:
            if sts_out[15] == G:
                log.info('pass')
            else:
                log.error('fail %s <> %s' % (G, sts_out[15]))
        G += 1


def chk_178(ser):
    log.info(limiter)
    log.info(u'178 ПМФ должен выдавать смещение B в STS_OUT')
    rs.set_mode(ser, u'технологический')
    B = 0
    while B < MAX_VAL:
        param = [0xFE, 0x60, 0x60, 0x60, 0x1A, 0x1A, B, 0x68, 0x00, 0x00, 0x00, 0x07, 0x2A, 0xF0, 0x00, 0x00]
        rs.set_param(ser, param)
        time.sleep(delay_sts_readback)
        clear_all_q()
        rs.req_sts(ser)
        sts_out = rx_specific_packet('STS_OUT', '232')
        if sts_out:
            if sts_out[16] == B:
                log.info('pass')
            else:
                log.error('fail %s <> %s' % (B, sts_out[16]))
        B += 1


def chk_179(ser):
    log.info(limiter)
    log.info(u'179 ПМФ должен выдавать фазу тактовой частоты в STS_OUT')
    rs.set_mode(ser, u'технологический')
    PHASE = 0
    while PHASE < MAX_VAL:
        param = [0xFE, 0x60, 0x60, 0x60, 0x1A, 0x1A, 0x1A, PHASE, 0x00, 0x00, 0x00, 0x07, 0x2A, 0xF0, 0x00, 0x00]
        rs.set_param(ser, param)
        time.sleep(delay_sts_readback)
        clear_all_q()
        rs.req_sts(ser)
        sts_out = rx_specific_packet('STS_OUT', '232')
        if sts_out:
            if sts_out[17] == PHASE:
                log.info('pass')
            else:
                log.error('fail %s <> %s' % (PHASE, sts_out[17]))
        PHASE += 1


def chk_180(ser):
    log.info(limiter)
    log.info(u'180 ПМФ должен выдавать смещение по горизонтали в STS_OUT')
    rs.set_mode(ser, u'технологический')
    SHIFT_H = 0
    while SHIFT_H < MAX_VAL:
        param = [0xFE, 0x60, 0x60, 0x60, 0x1A, 0x1A, 0x1A, 0x68, SHIFT_H, 0x00, 0x00, 0x07, 0x2A, 0xF0, 0x00, 0x00]
        rs.set_param(ser, param)
        time.sleep(delay_sts_readback)
        clear_all_q()
        rs.req_sts(ser)
        sts_out = rx_specific_packet('STS_OUT', '232')
        if sts_out:
            if sts_out[18] == SHIFT_H:
                log.info('pass')
            else:
                log.error('fail %s <> %s' % (SHIFT_H, sts_out[18]))
        SHIFT_H += 1


def chk_181(ser):
    log.info(limiter)
    log.info(u'181 ПМФ должен выдавать смещение по вертикали в STS_OUT')
    rs.set_mode(ser, u'технологический')
    SHIFT_V = 0
    while SHIFT_V < MAX_VAL:
        param = [0xFE, 0x60, 0x60, 0x60, 0x1A, 0x1A, 0x1A, 0x68, 0x00, SHIFT_V, 0x00, 0x07, 0x2A, 0xF0, 0x00, 0x00]
        rs.set_param(ser, param)
        time.sleep(delay_sts_readback)
        clear_all_q()
        rs.req_sts(ser)
        sts_out = rx_specific_packet('STS_OUT', '232')
        if sts_out:
            if sts_out[19] == SHIFT_V:
                log.info('pass')
            else:
                log.error('fail %s <> %s' % (SHIFT_V, sts_out[19]))
        SHIFT_V += 1


def chk_182(ser):
    log.info(limiter)
    log.info(u'182 ПМФ должен выдавать текущее значение яркости в STS_OUT')
    rs.set_mode(ser, u'технологический')
    BRIT = 0
    while BRIT < MAX_VAL:
        rs.set_brit(ser, BRIT)
        time.sleep(delay_sts_readback)
        clear_all_q()
        rs.req_sts(ser)
        sts_out = rx_specific_packet('STS_OUT', '232')
        if sts_out:
            if sts_out[20] == BRIT:
                log.info('pass')
            else:
                log.error('fail %s <> %s' % (BRIT, sts_out[20]))
        BRIT += 1


def chk_195(ser):
    log.info(limiter)
    log.info(u'195 ПМФ должен вести учет времени наработки и выдавать его в STS_OUT')
    time_delay = 10
    clear_all_q()    
    rs.set_mode(ser, u'технологический')
    sts_out = rx_specific_packet('STS_OUT', '232')
    T1 = sts_out[24] + (sts_out[25] << 7) + (sts_out[26] << 14) + (sts_out[27] << 21)
    log.info(T1)
    time.sleep(time_delay)
    rs.set_mode(ser, u'технологический')
    sts_out = rx_specific_packet('STS_OUT', '232')
    T2 = sts_out[24] + (sts_out[25] << 7) + (sts_out[26] << 14) + (sts_out[27] << 21)
    if (time_delay/60 - 1) <= (T2 - T1) <= (time_delay/60 + 1):
        log.info(u'Pass T2 = %s, T1 = %s' % (T2, T1))
    else:
        log.error(u'Fail T2 = %s, T1 = %s' % (T2, T1))
    

def chk_237(ser):
    log.info(limiter)
    log.info(u'237 ПМФ должен в STS_PMF выдавать время наработки')
    time_delay = 10
    clear_all_q()
    rs.set_mode(ser, u'расширенный')
    sts_pmf = rx_specific_packet('STS_PMF', '232')
    T1 = (sts_pmf[31] + (sts_pmf[32] << 8) + (sts_pmf[33] << 16) + (sts_pmf[34] << 24) + (sts_pmf[35] << 32)) * 0.25
    log.info(T1)
    time.sleep(time_delay)
    rs.set_mode(ser, u'расширенный')
    sts_pmf = rx_specific_packet('STS_PMF', '232')
    T2 = (sts_pmf[31] + (sts_pmf[32] << 8) + (sts_pmf[33] << 16) + (sts_pmf[34] << 24) + (sts_pmf[35] << 32)) * 0.25
    log.info(T2)
    if (time_delay - 1) <= (T2 - T1) <= (time_delay + 1):
        log.info(u'Pass T2 = %s, T1 = %s' % (T2, T1))
    else:
        log.error(u'Fail T2 = %s, T1 = %s' % (T2, T1))


def chk_276(ser):
    log.info(limiter)
    log.info(u'276 ПМФ должен игнорировать пакеты с ошибочной контрольной суммой')

    def hex2bytes(string):
        return binascii.unhexlify(string.replace(' ', ''))

    def cs_calc_bad(data):
        CS = 0
        for each in data:
            CS = CS ^ each
        return CS + 1
    
    def send_packet(ser, data):
        CS = cs_calc_bad(data)
        send = 'FF FF '
        for d in data:
            send += "%0.2X " % d
        send += "%0.2X" % CS
        ser.write(hex2bytes(send))
    
    rs.set_mode(ser, u'технологический')
    data = [0xFE, 0x77, 0x77, 0x77, 0x1A, 0x1A, 0x1A, 0x68, 0x00, 0x00, 0x00, 0x07, 0x2A, 0xF0, 0x00, 0x00]
    rs.set_param(ser, data)
    time.sleep(delay_sts_readback)
    rs.req_sts(ser)
    sts_out = rx_specific_packet('STS_OUT', '232')
    log.info(sts_out)    
    data = [0xFE, 0x55, 0x55, 0x55, 0x1A, 0x1A, 0x1A, 0x68, 0x00, 0x00, 0x00, 0x07, 0x2A, 0xF0, 0x00, 0x00]    
    data.insert(0, 0xC2)
    send_packet(ser, data)
    time.sleep(delay_sts_readback)
    clear_all_q()
    rs.req_sts(ser)
    sts_out = rx_specific_packet('STS_OUT', '232')
    if sts_out:
        if sts_out[11] == 0x55:
            log.error('fail %s' % sts_out)
        else:
            log.info('pass')

def chk_277(ser):
    log.info(limiter)
    log.info(u'277 ПМФ должен игнорироват пакеты с неправильным заголовком')

    def hex2bytes(string):
        return binascii.unhexlify(string.replace(' ', ''))

    def cs_calc_bad(data):
        CS = 0
        for each in data:
            CS = CS ^ each
        return CS
    
    def send_packet(ser, data):
        CS = cs_calc_bad(data)
        send = 'FF FF '
        for d in data:
            send += "%0.2X " % d
        send += "%0.2X" % CS
        ser.write(hex2bytes(send))
        log.info(u'направляем в ПМФ %s' % send)
    
    data = [0xFE, 0x55, 0x55, 0x55, 0x1A, 0x1A, 0x1A, 0x68, 0x00, 0x00, 0x00, 0x07, 0x2A, 0xF0, 0x00, 0x00]    
    data.insert(0, 0xFE)
    send_packet(ser, data)
    time.sleep(delay_sts_readback)
    clear_all_q()
    rs.req_sts(ser)
    sts_out = rx_specific_packet('STS_OUT', '232')


def chk_279(ser):
    log.info(limiter)
    log.info(u'279 ПМФ должна не менять значение параметра если была попытка установки недопустимого значения')
    rs.set_mode(ser, u'технологический')
    param = [0xFE, 0x07, 0x09, 0xFF, 0x10, 0x10, 0x10, 0x68, 0x00, 0x00, 0x00, 0x07, 0x2A, 0xF0, 0x00, 0x00]
    rs.set_param(ser, param)
    time.sleep(delay_sts_readback)
    clear_all_q()
    rs.req_sts(ser)
    sts_out = rx_specific_packet('STS_OUT', '232')
    if sts_out:
        if sts_out[11] == 0xFF:
            log.error('fail')
        else:
            log.info('pass STS_OUT = %s' % sts_out)





def checklist(ser, spsh='COM1'):
    """ Последовательный вызов указанных тестов 
    """
    params = (exp_pmf_id, exp_soft_id, exp_hard_id, exp_serial_id,
              exp_temp_MD, exp_temp_MI)
    errors = 0
    ps = psh.psh3610(spsh)
    log.info(u'Начало теста')
    ps.setup(27, 2, 30, 0, 1, 0.5)
    errors += chk00_start_time(ser, 1)
    errors += chk01_set_mode(ser)
    errors += chk02_stats(ser, *params)
    errors += chk03_runtime(ser, 1)
    errors += chk04_vga_resolution()
    errors += chk05_toprosa(ser, 1, 3)
    errors += chk06_brightness(ser, manual=False)
    errors += chk07_power_consumption(ps, max_power=30, resp_timeout=0.3)
    errors += chk08_splashscreen(ser)
    ps.setup(27, 2, 30, 0, 0, 0.5)
    log.info(u'Конец теста')
    log.info(u'Количество ошибок: %s' % errors)
    return errors
