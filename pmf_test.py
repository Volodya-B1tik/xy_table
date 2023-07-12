# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 20:28:12 2016

@author: gubatenko
Набор тестов для проверки ПМФ
"""

from __future__ import division, print_function
#from PyQt4 import QtCore, QtGui
#import Tkinter as tk
import serial
import rs
import psh
import vga
import time
import datetime
import logging
import sys
import getcomports
import graphics as gr
import collections as coll
import binascii
import threading
#import gui
import random
import math
#import chk_nnn
#import keyboard_tests as keys
#import lcd_tests as lcd
#import power_tests as pwr
#import test_checklist as chk
import touchscreen_tests as touch
import check_kontron_function as ckf
from var import *

PMF_TYPE = '_32' # '_6x'

def inq(ser, mbx):
    #print("INQ")    
    """ Качалка данных из входного буфера COM-порта в FIFO-канала.
    Выполняется бесконечно, должна запускаться в отдельном потоке.
    1) ser - [serial.Serial] COM-порт с которого будем читать
    2) mbx - [collections.deque] FIFO-канала в которую будем писать
    """
    dat = 0
    while run:
        if ser.inWaiting() > 0:
            dat = ser.read(ser.inWaiting())
            chunk = coll.deque([int(binascii.hexlify(dat[i]), 16)
                                for i in xrange(len(dat))])
            print(dat)            
            while True:
                try:
                    mbx.append(chunk.popleft())
                except IndexError:
                    break
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
           # rs232_old_q.append(rx_byte) 
            if not packet_in_progress:
                if ff1 is False and rx_byte == 0xFF:
                    ff1 = True
                    rx_cnt = 1
                elif ff1 is True and ff2 is False and rx_byte == 0xFF:
                    ff2 = True
                    rx_cnt += 1
                elif ff1 is True and ff2 is False and rx_byte != 0xFF:
                    ff1 = False
                elif ff1 is True and ff2 is True:
                    if rx_byte != 0xFF:
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
                                print(packet)
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


def old_packet_parser():
    first_byte = False
    bytes_in_old_packet = 0
    old_packet = coll.deque()
    while run:
        if rs232_old_q:
            rx_old = rs232_old_q.popleft()
            if not first_byte:
                if rx_old == 0xBF or rx_old == 0xFF:
                    first_byte = True
                    flag = rx_old
            else:
                if rx_old == 0xFF:
                    first_byte = True
                    flag = rx_old
                else:
                    old_packet.append(rx_old)
                    bytes_in_old_packet += 1
                    if bytes_in_old_packet == 4:
                        x_coord = (old_packet[2] << 7) + old_packet[3]
                        y_coord = (old_packet[0] << 7) + old_packet[1]
                        old_xy.append((flag, x_coord, y_coord))
                        bytes_in_old_packet = 0
                        old_packet.clear()
                        first_byte = False
                        if len(old_xy) > 100:
                            old_xy.clear()


def fifo_size_out():
    while 1:
        if len(rs232_coord_out_q) > 0:
            log.debug('COORD_OUT: %s' % len(rs232_coord_out_q))
        if len(rs232_key_out_q) > 0:
            log.debug('KEY_OUT: %s' % len(rs232_key_out_q))
        if len(rs232_key_set_out_q) > 0:
            log.debug('KEY_SET_OUT: %s' % len(rs232_key_set_out_q))
        if len(rs232_sts_out_q) > 0:
            log.debug('STS_OUT: %s' % len(rs232_sts_out_q))
        if len(rs232_sts_pmf_q) > 0:
            log.debug('STS_PMF: %s' % len(rs232_sts_pmf_q))
        time.sleep(1)
#        delay = time.time()
#        while run:
#            if time.time() - delay > 10:
#                break


def resp_yes_no():
    resp = None
    while True:
        try:
            resp = int(raw_input())
            if (resp == 0) or (resp == 1):
                break
            else:
                print(u'>>> Значение должно быть 0 или 1, повторите ввод:',)
        except ValueError:
            print(u'>>> Введено недопустимое значение, повторите ввод:',)
    return resp


def resp_0_255():
    resp = None
    while True:
        try:
            resp = int(raw_input())
            if (resp >= 0) and (resp < 256):
                break
            else:
                print(u'>>> Значение должно быть от 0 до 255, '
                      u'повторите ввод:',)
        except ValueError:
            print(u'>>> Введено недопустимое значение, повторите ввод:',)
    return resp


def rx_specific_packet(packet, channel, timeout=1):
    log = logging.getLogger()
    packet_data = []
    start_time = time.clock()

    log.debug(u'ждем пакет %s в приемной очереди канала %s' % (packet, channel))
    while time.clock() < start_time + timeout:
        #QtCore.QCoreApplication.processEvents()
        if channel == '232':
            if packet == 'STS_OUT':
                if rs232_sts_out_q:
                    packet_data = rs232_sts_out_q.pop()
                    log.debug(u'взяли пакет %s из приемной очереди канала %s' % (packet, channel))
                    break
            elif packet == 'STS_PMF':
                if rs232_sts_pmf_q:
                    packet_data = rs232_sts_pmf_q.pop()
                    break
            elif packet == 'KEY_OUT':
                if rs232_key_out_q:
                    packet_data = rs232_key_out_q.pop()
                    break
            elif packet == 'KEY_SET_OUT':
                if rs232_key_set_out_q:
                    packet_data = rs232_key_set_out_q.pop()
                    break
            elif packet == 'COORD_OUT':
                if rs232_coord_out_q:
                    packet_data = rs232_coord_out_q.pop()
                    break
            elif packet == 'KEY_OFF_CLICKED':
                if rs232_key_off_clicked_q:
                    packet_data = rs232_key_off_clicked_q.pop()
                    break

            elif packet == 'STS_VGLV':
                if rs232_sts_vglv_q:
                    packet_data = rs232_sts_vglv_q.pop()
                    break
            elif packet == 'STS_ETH1':
                if rs232_sts_eth1_q:
                    packet_data = rs232_sts_eth1_q.pop()
                    break
            elif packet == 'STS_ETH2':
                if rs232_sts_eth2_q:
                    packet_data = rs232_sts_eth2_q.pop()
                    break
            elif packet == 'STS_VPr1':
                if rs232_sts_vpr1_q:
                    packet_data = rs232_sts_vpr1_q.pop()
                    break
            elif packet == 'STS_VPr2':
                if rs232_sts_vpr2_q:
                    packet_data = rs232_sts_vpr2_q.pop()
                    break
            elif packet == 'STS_VPr3':
                if rs232_sts_vpr3_q:
                    packet_data = rs232_sts_vpr3_q.pop()
                    break
            elif packet == 'STS_VPr4':
                if rs232_sts_vpr4_q:
                    packet_data = rs232_sts_vpr4_q.pop()
                    break
            elif packet == 'STS_VPIPE':
                if rs232_sts_vpipe_q:
                    packet_data = rs232_sts_vpipe_q.pop()
                    break
            elif packet == 'STS_OVHP':
                if rs232_sts_ovhp_q:
                    packet_data = rs232_sts_ovhp_q.pop()
                    break

        elif channel == '422':
            if packet == 'STS_OUT':
                if rs422_sts_out_q:
                    packet_data = rs422_sts_out_q.pop()
                    break
            elif packet == 'STS_PMF':
                if rs422_sts_pmf_q:
                    packet_data = rs422_sts_pmf_q.pop()
                    break
            elif packet == 'KEY_OUT':
                if rs422_key_out_q:
                    packet_data = rs422_key_out_q.pop()
                    break
            elif packet == 'KEY_SET_OUT':
                if rs422_key_set_out_q:
                    packet_data = rs422_key_set_out_q.pop()
                    break
            elif packet == 'COORD_OUT':
                if rs422_coord_out_q:
                    packet_data = rs422_coord_out_q.pop()
                    break
        elif channel == 'CAN':
            pass  # допилить CAN
        else:
            log.exception('BAD CHANNEL')
    return packet_data


def init(comports_required_n=2):
    """ Инициализация среды перед началом проверок
        1) Поиск СOM портов
        2) Загрузка из файла эталонов (TODO)
    """

    def autoset():
        logging.disable(logging.CRITICAL)
        tm_wait_pmf_on = 3
        com_psh = ''
        com_232 = ''
        print(u'Ищу COM-порт подкл. к PSH (надеюсь PSH включен)...')
        ports = getcomports.serial_ports()
        for port in ports:
            with serial.Serial(port, baudrate=9600) as ser:
                ps = psh.psh3610(ser)
                ps_id = ps.read_id()
                if ps_id != '':
                    print(u'Источник питания подключен к %s' % port)
                    com_psh = port
                    break
        if com_psh != '':
            print(u'Ищу COM-порт подкл. к RS-232 ПМФ (надеюсь PSH включен)...')
            ports = getcomports.serial_ports()
            ports.remove(com_psh)
            with serial.Serial(com_psh, baudrate=9600) as ser:
                ps = psh.psh3610(ser)
                ps.setup(27, 2, 30, 0, 1, 0.5)
                time.sleep(tm_wait_pmf_on)
                for port in ports:
                    with serial.Serial(port, baudrate=9600) as ser:
                        rs232_sts_out_q.clear()
                        rs.set_mode(ser, u'технологический')
                        if len(rx_specific_packet('STS_OUT', '232', 0.3)) > 0:
                            print(u'RS-232 ПМФ подключен к %s' % port)
                            com_232 = port
                            break
        else:
            print(u'PSH не был найден')
        logging.disable(logging.NOTSET)
        return com_psh, com_232

    init_dic = {}
    init_fail = False
    print(chr(12))
    print(u'Подготовка к проверке')
    print(u'>>> Использовать test.ini для настройки? [1 - да, 0 - нет]:',)
    if resp_yes_no() == 0:
        print(u'>>> Автоматически назначить COM-порты? [1 - да, 0 - нет]:',)
        if resp_yes_no() == 0:
            comports = getcomports.serial_ports()
            if len(comports) < comports_required_n:
                print(u'Не хватает доступных COM-портов, завершаю работу')
                init_fail = True
            else:
                print(u'Доступные COM-порты:', " ".join(comports))
                print(u'>>> Введите номер COM-порта подкл. к RS-232 ПМФ:',)
                while True:
                    port_232 = raw_input()
                    if ('COM' + port_232) in comports:
                        print(u'RS-232 ПМФ назначен на COM-порт №', port_232)
                        comports.remove('COM' + port_232)
                        break
                    else:
                        print(u'Неправильный номер порта, повторите попытку:',)
                print(u'Доступные COM-порты:', " ".join(comports))
                print(u'>>> Введите номер COM порта подкл. к PSH3610:',)
                while True:
                    port_psh = raw_input()
                    if ('COM' + port_psh) in comports:
                        print(u'Источник питания назначен на '
                              u'COM-порт №%s' % port_psh)
                        comports.remove('COM' + port_psh)
                        break
                    else:
                        print(u'\nНеправильный номер порта, '
                              u'повторите попытку:',)
                init_dic['RSCOM'] = 'COM' + port_232
                init_dic['PSHCOM'] = 'COM' + port_psh
        else:
            # автосет
            port_psh, port_232 = autoset()
            if (port_psh == '') or (port_232 == ''):
                init_fail = True
            else:
                init_dic['RSCOM'] = port_232
                init_dic['PSHCOM'] = port_psh
    else:
        pass  # тут ввод из файла
        print(u'Загрузка из файла пока не реализована')
        init_fail = True
    return init_dic, init_fail


def logger_close():
    """ Чистка логгера после работы """
    handlers = log.handlers[:]
    for handler in handlers:
        handler.close()
        log.removeHandler(handler)


def get_vga_modes(dev_num):
    """ Получает список режимов VGA. Список режимов используется потом в
    set_vga_resolution """
    devices = vga.devlist()
    mode_list = vga.modelist(devices[dev_num])
    return mode_list, devices


def set_vga_resolution(x, y, mode_list, devices, dev_num, ask_user):
    er = 0
    vga.change_resolution(devices[dev_num], mode_list,
                          mode_required=(32, x, y, 60, 0))
    if ask_user:
        print(u'>>> Разрешение {}х{} ? [1 - да, 0 - нет]:'.format(x, y),)
        result = resp_yes_no()
        if result == 0:
            log.error(u'Ошибка VGA {}х{}'.format(x, y))
            er += 1
    return er


def coord_q(coord_out):
    log = logging.getLogger()
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
    log.debug(cc)

#    print('f1 = %.5s, f2 = %.5s, x1,y1 = (%.5s, %.5s), \
#x2,y2 = (%.5s, %.5s) ' % (flag1, flag2, x1, y1, x2, y2))
    return x1, y1, x2, y2, flag1, flag2


def clear_all_q():
    # чистим приемные очереди
    rs232_coord_out_q.clear()
    rs232_key_out_q.clear()
    rs232_key_set_out_q.clear()
    rs232_sts_out_q.clear()
    rs232_sts_pmf_q.clear()
    rs232_sts_vpipe_q.clear()
    rs232_sts_vpr1_q.clear()
    rs232_sts_vpr2_q.clear()
    rs232_sts_vpr3_q.clear()
    rs232_sts_vpr4_q.clear()
    rs232_sts_vglv_q.clear()
    rs232_sts_eth1_q.clear()
    rs232_sts_eth2_q.clear()
    rs232_sts_ovhp_q.clear()
    rs422_coord_out_q.clear()
    rs422_key_out_q.clear()
    rs422_key_set_out_q.clear()
    rs422_sts_out_q.clear()
    rs422_sts_pmf_q.clear()
    rs422_sts_vpipe_q.clear()
    rs422_sts_vpr1_q.clear()
    rs422_sts_vpr2_q.clear()
    rs422_sts_vpr3_q.clear()
    rs422_sts_vpr4_q.clear()
    rs422_sts_vglv_q.clear()
    rs422_sts_eth1_q.clear()
    rs422_sts_eth2_q.clear()
    rs422_sts_ovhp_q.clear()
    old_xy.clear()

def sts_decription(ser, log):
#    global ser
    PMF_ID_dic = {
    0x00: u'ПМФ-3',
    0x01: u'ПМФ-4',
    0x02: u'ПМФ-5.0',
    0x03: u'ПМФ-5.1',
    0x04: u'ПМФ-5.2',
    0x10: u'ПМФ-6.0',
    0x11: u'ПМФ-6.1',
    0x12: u'ПМФ-6.2',
    0x13: u'ПМФ-6.3',
    0x14: u'ПМФ-6.4',
    0x15: u'ПМФ-6.5',
    0x16: u'ПМФ-6.6',
    0x20: u'ПМФ-6.0м',
    0x21: u'ПМФ-3.2'
    }

    vid_dict_sts = {
    0xFE: u'значение не определено',
    0xFD: u'VPIPE manual config',
    0x00: u'640х480 RGB,LVDS',
    0x01: u'800х600 RGB,LVDS',
    0x02: u'1024х768 RGB,LVDS',
    0x03: u'1024х768 Eth, 16 бит, цвет',
    0x04: u'1024х768 Eth, 8 бит, моно',
    0x05: u'1024х768 Eth, 10 бит, моно',
    0x06: u'720х576 Eth, 16 бит, цвет',
    0x07: u'720х576 Eth, 8 бит, моно',
    0x08: u'720х576  Eth, 10 бит, моно',
    0x09: u'720х400 RGB',
    0x11: u'720x576 TV1',
    0x12: u'720x576 TV2',
    0x13: u'720x576 TV3',
    0x14: u'720x576 TV4',
    0x15: u'720x576 TV5'
    }

    vid_if_dict_sts = {
    0xFE: u'значение не определено',
    0xFD: u'VPIPE manual config',
    0x00: u'RGB',
    0x01: u'LVDS',
    0x02: u'Ethernet',
    0x03: u'Splashscreen'
    }



    rs.set_mode(ser, u'технологический')
    st = rx_specific_packet('STS_OUT', '232')
    log.debug(st)
    if st:
        log.debug(u' ')
        log.debug(u'================STS_OUT DESCRIPTION=================')

        sts_out_pmfid = st[4]
        log.debug(u'STS_OUT: Идентификатор ПМФ - 0x%02X = %s' % (
        sts_out_pmfid, PMF_ID_dic.setdefault(sts_out_pmfid, u'неизвестный идентификатор ПМФ')))

        sts_out_fwid = st[5]
        log.debug(u'STS_OUT: Версия firmware - 0x%02X' % sts_out_fwid)

        sts_out_slovo = st[6]
        log.debug(u'STS_OUT: Слово режима работы - 0x%02X' % sts_out_slovo)

        b0 = (sts_out_slovo & 0x01) >> 0
        b1 = (sts_out_slovo & 0x02) >> 1
        b2 = (sts_out_slovo & 0x04) >> 2
        b3 = (sts_out_slovo & 0x08) >> 3
        b4 = (sts_out_slovo & 0x10) >> 4
        b5 = (sts_out_slovo & 0x20) >> 5
        b6 = (sts_out_slovo & 0x40) >> 6
        b7 = (sts_out_slovo & 0x80) >> 7

        if b0 == 0:
            log.debug(u'        - Резервный бит 0 установлен правильно')
        else:
            log.debug(u'        - Резервный бит 0 установлен неправильно !!!')

        if b1 == 0:
            log.debug(u'        - Штатный режим')
        else:
            log.debug(u'        - Технологический режим')

        if b2 == 0:
            log.debug(u'        - Режим передачи кнопок KEY_OUT')
        else:
            log.debug(u'        - Режим передачи кнопок KEY_SET_OUT')

        if b3 == 0:
            log.debug(u'        - Резервный бит 3 установлен правильно')
        else:
            log.debug(u'        - Резервный бит 3 установлен неправильно !!!')

        if b4 == 0:
            log.debug(u'        - Резервный бит 4 установлен правильно')
        else:
            log.debug(u'        - Резервный бит 4 установлен неправильно !!!')

        if b5 == 0:
            log.debug(u'        - Резервный бит 5 установлен правильно')
        else:
            log.debug(u'        - Резервный бит 5 установлен неправильно !!!')

        if b6 == 0:
            log.debug(u'        - Резервный бит 6 установлен правильно')
        else:
            log.debug(u'        - Резервный бит 6 установлен неправильно !!!')

        if b7 == 0:
            log.debug(u'        - Резервный бит 7 установлен правильно')
        else:
            log.debug(u'        - Резервный бит 7 установлен неправильно !!!')


        sts_out_reserv_7 = st[7]
        log.debug(u'STS_OUT: Резервное слово 7 (0x00) - 0x%02X' % sts_out_reserv_7)

        sts_out_reserv_8 = st[8]
        log.debug(u'STS_OUT: Резервное слово 8 (0x00) - 0x%02X' % sts_out_reserv_8)

        sts_out_podogrev = st[9]
        log.debug(u'STS_OUT: Состояние подогрева - 0x%02X' % sts_out_podogrev)

        sts_out_reserv_10 = st[10]
        log.debug(u'STS_OUT: Резервное слово 10 (0x00) - 0x%02X' % sts_out_reserv_10)

        sts_out_R_gain = st[11]
        log.debug(u'STS_OUT: R усиление - 0x%02X' % sts_out_R_gain)

        sts_out_G_gain = st[12]
        log.debug(u'STS_OUT: G усиление - 0x%02X' % sts_out_G_gain)

        sts_out_B_gain = st[13]
        log.debug(u'STS_OUT: B усиление - 0x%02X' % sts_out_B_gain)

        sts_out_R_offset = st[14]
        log.debug(u'STS_OUT: R смещение - 0x%02X' % sts_out_R_offset)

        sts_out_G_offset = st[15]
        log.debug(u'STS_OUT: G смещение - 0x%02X' % sts_out_G_offset)

        sts_out_B_offset = st[16]
        log.debug(u'STS_OUT: B смещение - 0x%02X' % sts_out_B_offset)

        sts_out_phase = st[17]
        log.debug(u'STS_OUT: Фаза АЦП - 0x%02X' % sts_out_phase)

        sts_out_horoff = st[18]
        log.debug(u'STS_OUT: Смещение по горизонтали - 0x%02X' % sts_out_horoff)

        sts_out_vertoff = st[19]
        log.debug(u'STS_OUT: Смещение по вертикали - 0x%02X' % sts_out_vertoff)

        sts_out_brightness = st[20]
        log.debug(u'STS_OUT: Текущая яркость - 0x%02X' % sts_out_brightness)

        sts_out_vif = st[21]
        log.debug(u'STS_OUT: Входной видеоинтерфейс - 0x%02X = %s' % (
        sts_out_vif, vid_if_dict_sts.setdefault(sts_out_vif, u'неизвестный видеоинтерфейс')))

        sts_out_vifparam = st[22]
        log.debug(u'STS_OUT: Параметры видео - 0x%02X = %s' % (
        sts_out_vifparam, vid_dict_sts.setdefault(sts_out_vifparam, u'неизвестные параметры')))

        sts_out_BIST = st[23]
        log.debug(u'STS_OUT: Самодиагностика - 0x%02X' % sts_out_BIST)
        bist_b0 = (sts_out_BIST & 0x01) >> 0
        bist_b1 = (sts_out_BIST & 0x02) >> 1
        bist_b2 = (sts_out_BIST & 0x04) >> 2
        bist_b3 = (sts_out_BIST & 0x08) >> 3
        bist_b4 = (sts_out_BIST & 0x10) >> 4
        bist_b5 = (sts_out_BIST & 0x20) >> 5
        bist_b6 = (sts_out_BIST & 0x40) >> 6
        bist_b7 = (sts_out_BIST & 0x80) >> 7

        if bist_b0 == 0:
            log.debug(u'        - Самодиагностика завершена')

            if bist_b1 == 0:
                log.debug(u'        - Резервный бит установлен правильно')
            else:
                log.debug(u'        - Резервный бит установлен неправильно !!!')

            if bist_b2 == 0:
                log.debug(u'        - Датчики температуры МИ и подсистемы подогрева ЖК-матрицы исправны')
            else:
                log.debug(u'        - Один или оба датчика температуры МИ и/или подсистемы подогрева ЖК-матрицы не исправны !!!')

            if bist_b3 == 0:
                log.debug(u'        - RGB АЦП доступен')
            else:
                log.debug(u'        - Считаное значение IDENT[7:0] из регистра 0x11h RGB АЦП ADV7403 не равно 19h !!!')

            if bist_b4 == 0:
                log.debug(u'        - Память DDR3 SDRAM инициализирована')
            else:
                log.debug(u'        - Инициализация DDR3 SDRAM не состоялась !!!')

            if bist_b5 == 0:
                log.debug(u'        - Контроллер Ethernet инициализирован')
            else:
                log.debug(u'        - Инициализация контроллера Ethernet не состоялась !!!')

            if bist_b6 == 0:
                log.debug(u'        - Сенсорный экран исправен')
            else:
                log.debug(u'        - Сенсорный экран не исправен (частично или полностью) !!!')

            if bist_b7 == 0:
                log.debug(u'        - Доступ к EPCQ исправен')
            else:
                log.debug(u'        - Отсутствует доступ к EPCQ !!!')

        else:
            log.debug(u'        - Самодиагностика не завершена !!!')

        # STS_OUT - время наработки
        tt1 = st[24]
        tt2 = st[25] << 7
        tt3 = st[26] << 14
        tt4 = st[27] << 21
        tt = tt1 + tt2 + tt3 + tt4
        h1 = int(math.floor(tt / 60))
        m1 = int(math.floor(tt - h1 * 60))
        log.debug(u'STS_OUT: время наработки - %s ч, %s мин' % (h1, m1))


        topros = st[28]
        time_topros = (1 + topros) * 25 # ms
        log.debug(u'STS_OUT: Топроса - 0x%02X = %s мс' % (topros, time_topros))

        tavtopovtor = st[29]
        time_tavtopovtor = (1 + tavtopovtor) * 5 # ms
        log.debug(u'STS_OUT: Тавnоповтора - 0x%02X = %s мс' % (tavtopovtor, time_tavtopovtor))

        tuderj_vikl = st[30]
        log.debug(u'STS_OUT: Тудерж_выкл - %s с' % tuderj_vikl)



        log.debug(u'================/END STS_OUT DESCRIPTION=============')
        log.debug(u' ')


    time.sleep(0.5)
    rs.set_mode(ser, u'расширенный')
    time.sleep(0.5)
    sts_pmf = rx_specific_packet('STS_PMF', '232', timeout=1)
    log.debug(sts_pmf)
    if sts_pmf:

        log.debug(u' ')
        log.debug(u'================STS_PMF DESCRIPTION=================')


        sts_pmf_pmfid = sts_pmf[4]
        log.debug(u'STS_PMF: Идентификатор ПМФ - 0x%02X = %s' % (
        sts_pmf_pmfid, PMF_ID_dic.setdefault(sts_pmf_pmfid, u'неизвестный идентификатор ПМФ')))

        SWID1 = sts_pmf[5]
        SWID2 = sts_pmf[6] << 7
        SWID3 = sts_pmf[7] << 14
        SWID4 = sts_pmf[8] << 21
        SWID5 = sts_pmf[9] << 28

        SWID = SWID1 + SWID2 + SWID3 + SWID4 + SWID5
        log.debug(u'Версия ПО = %s' % (SWID))

        FWID1 = sts_pmf[10]
        FWID2 = sts_pmf[11] << 7
        FWID3 = sts_pmf[12] << 14
        FWID4 = sts_pmf[13] << 21
        FWID5 = sts_pmf[14] << 28

        FWID = FWID1 + FWID2 + FWID3 + FWID4 + FWID5
        log.debug(u'Версия ПЛИС = %s' % (FWID))

        SERN = (str(sts_pmf[15]) + str(sts_pmf[16]) + str(sts_pmf[17]) +
                str(sts_pmf[18]) + str(sts_pmf[19]) + str(sts_pmf[20]) +
                str(sts_pmf[21]) + str(sts_pmf[22]) + str(sts_pmf[23]))
        log.debug(u'Заводской номер = %s' % (SERN))


        MD_temp = sts_pmf[24]
        log.debug(u'Температура МД = %s' % MD_temp)

        MI_temp = sts_pmf[25] + (sts_pmf[26] << 7)
        log.debug(u'Температура МИ = %s' % MI_temp)

        slovo = sts_pmf[27]
        bit0 = (slovo & 0x01) >> 0
        bit1 = (slovo & 0x02) >> 1
        bit2 = (slovo & 0x04) >> 2
        bit3 = (slovo & 0x08) >> 3
        bit4 = (slovo & 0x10) >> 4
        bit5 = (slovo & 0x20) >> 5
        bit6 = (slovo & 0x40) >> 6
        bit7 = (slovo & 0x80) >> 7

        if (bit0 == 1) or (bit7 == 1):
            log.debug(u'Ошибка в слове режима работы, зарезервированный бит = 1')

        if bit3 == 1:
            mode = u'расширенный'
        else:
            if bit1 == 1:
                mode = u'технологический'
            else:
                mode = u'штатный'
        log.debug(u'Режим работы = %s' % mode)

        if bit2 == 1:
            log.debug(u'Режим передачи кнопок KEY_SET_OUT')
        else:
            log.debug(u'Режим передачи кнопок KEY_OUT')

        if bit5 == 1:
            log.debug(u'Повышенная яркость (только для ПМФ-3.2')
        else:
            log.debug(u'Нормальная яркость (только для ПМФ-3.2')

        if bit6 == 1:
            log.debug(u'Подогрев включен (только для ПМФ-3.2)')
        else:
            log.debug(u'Подогрев выключен (только для ПМФ-3.2)')

        if sts_pmf[28] == 0:
            log.debug(u'Подогрев 90 Вт')
        if sts_pmf[28] == 1:
            log.debug(u'Подогрев 130 Вт')
        if sts_pmf[28] == 2:
            log.debug(u'Подогрев 170 Вт')

        if sts_pmf[29] == 0:
            log.debug(u'Подогрев запрещен')
        else:
            if sts_pmf[29] == 1:
                log.debug(u'Подогрев разрешен')
            else:
                log.debug(u'Значение не соответствует протоколу !!!')

        log.debug(u'BIST = 0x%02X' % sts_pmf[30])

        tt1 = sts_pmf[31]
        tt2 = sts_pmf[32] << 7
        tt3 = sts_pmf[33] << 14
        tt4 = sts_pmf[34] << 21
        tt5 = sts_pmf[35] << 28
        tt = tt1 + tt2 + tt3 + tt4 + tt5
        h2 = int(math.floor(tt / (4 * 3600)))
        m2 = int(math.floor((tt / (4 * 60) - h2 * 60)))
        s2 = int(math.floor((tt / 4) - m2 * 60 - h2 * 3600))

        log.debug(u'STS_PMF: Время наработки = %s ч, %s мин, %s c' % (h2, m2, s2))

        on_off_num = sts_pmf[36] + (sts_pmf[37] << 7) + (sts_pmf[38] << 14)
        log.debug(u'Количество включений = %s' % on_off_num)

        topros_2 = sts_pmf[39]
        time_topros_2 = (1 + topros_2) * 25 # ms
        log.debug(u'STS_PMF: Топроса - 0x%02X = %s мс' % (topros_2, time_topros_2))

        tavtopovtor_2 = sts_pmf[40]
        time_tavtopovtor_2 = (1 + tavtopovtor_2) * 5 # ms
        log.debug(u'STS_PMF: Тавnоповтора - 0x%02X = %s мс' % (tavtopovtor_2, time_tavtopovtor_2))

        sts_pmf_brightness = sts_pmf[41]
        log.debug(u'STS_PMF: Текущая яркость - 0x%02X' % sts_pmf_brightness)

        sts_pmf_vif = sts_pmf[42]
        log.debug(u'STS_PMF: Входной видеоинтерфейс - 0x%02X = %s' % (
        sts_pmf_vif, vid_if_dict_sts.setdefault(sts_pmf_vif, u'неизвестный видеоинтерфейс')))

        sts_pmf_vifparam = sts_pmf[43]
        log.debug(u'STS_PMF: Параметры видео - 0x%02X = %s' % (
        sts_pmf_vifparam, vid_dict_sts.setdefault(sts_pmf_vifparam, u'неизвестные параметры')))

        tuderj_vikl_2 = sts_pmf[44]
        log.debug(u'STS_PMF: Тудерж_выкл - %s с' % tuderj_vikl_2)

        din = sts_pmf[45]
        log.debug(u'STS_PMF: DIN - 0x%02X' % din)

        sts_pmf_codes = sts_pmf[46]


        bit0 = (sts_pmf_codes & 0x01) >> 0
        bit1 = (sts_pmf_codes & 0x02) >> 1
        bit2 = (sts_pmf_codes & 0x04) >> 2
        bit3 = (sts_pmf_codes & 0x08) >> 3
        bit4 = (sts_pmf_codes & 0x10) >> 4
        bit5 = (sts_pmf_codes & 0x20) >> 5
        bit6 = (sts_pmf_codes & 0x40) >> 6
        bit7 = (sts_pmf_codes & 0x80) >> 7

        log.debug(u'STS_PMF: CODE0  - %01X' % bit0)
        log.debug(u'STS_PMF: CODE1  - %01X' % bit1)
        log.debug(u'STS_PMF: CODE2  - %01X' % bit2)
        log.debug(u'STS_PMF: CODE3  - %01X' % bit3)
        log.debug(u'STS_PMF: CODE4  - %01X' % bit4)
        log.debug(u'STS_PMF: PARITY - %01X' % bit5)



        sts_pmf_reserv_47 = sts_pmf[47]
        log.debug(u'STS_PMF: Резервное слово 46 (0x00) - 0x%02X' % sts_pmf_reserv_47)

        sts_pmf_reserv_48 = sts_pmf[48]
        log.debug(u'STS_PMF: Резервное слово 46 (0x00) - 0x%02X' % sts_pmf_reserv_48)

        sts_pmf_reserv_49 = sts_pmf[49]
        log.debug(u'STS_PMF: Резервное слово 46 (0x00) - 0x%02X' % sts_pmf_reserv_49)


        log.debug(u'================/END STS_PMF DESCRIPTION=============')


def psp405_on_off(COM = 'COM16'):
    def hex2bytes(string):
        return binascii.unhexlify(string.replace(' ', ''))

    with serial.Serial(COM, baudrate=2400) as ser:
        send = '4B 4F 0D'
        ser.write(hex2bytes(send))


def fpga_access(COM = 'COM16'):
    with serial.Serial(COM, baudrate=9600) as ser:
        rs.set_mode(ser, u'расширенный')
        if ser.inWaiting() > 0:
            return 1
        else:
            return 0

def check_kontron_boot():
    n = 0
    err = 0
    ok = 0
    while n < 100:
        n += 1
        psp405_on_off()
        time.sleep(37)
        isAlive = ckf.CheckKontron()
        if isAlive:
            ok += 1
        else:
            err += 1
            time.sleep(10000)
        print(u'ОК - количество включений: %s, успешных - %s, ошибок - %s' % (n, ok, err))

        psp405_on_off()
        time.sleep(1)



def stop_threads(th_list):
    for th in th_list:
        th.join()

def full_brt(ser):
    while 1:
        rs.set_brit(ser, 0xFE)
        time.sleep(0.5)
        rs.set_brit(ser, 0x00)
        time.sleep(0.5)


def sts_requester(ser, cycles=10):
    def make_param(Top = 0x10):
        video_param = 0xFE
        R_amp = 0x32
        G_amp = 0x32
        B_amp = 0x32
        R_offset = 0x00
        G_offset = 0x00
        B_offset = 0x00
        phase = 0xCE
        hor_offset = 0x00
        ver_offset = 0x00
        rsrv = 0x00
        Toprosa = Top
        Tavto = 0x06
        video_if = 0xFE
        param = [video_param, R_amp, G_amp, B_amp, R_offset, G_offset, B_offset, phase, hor_offset, ver_offset, rsrv, Toprosa, Tavto, video_if, rsrv, rsrv]
        return param

    time.sleep(1)
    rs232_sts_out_q.clear()

    switching_period = 0.5 # seconds
    Top = 0

    for n in xrange(0, cycles):
        Top = Top + 1
        print('------ %s -------' % Top)

        a = time.time()
        rs.set_mode(ser, u'технологический')
        sts = rx_specific_packet('STS_OUT', '232', timeout=3)
        if sts == []: print("error")
        print(u' 0 время SET_MODE и STS_OUT = %s ms ' % (int((time.time() - a)*1000)))


#        a = time.time()
#        rs.set_param(ser, make_param())
#        sts = rx_specific_packet('STS_OUT', '232', timeout=3)
#        if sts == []: print("error")
#        print(u' 1 время SET_PARAM и STS_OUT = %s ms ' % (int((time.time() - a)*1000)))
#
#        a = time.time()
#        rs.set_key_mode(ser, 1)
#        print(u' 2 время SET_KEY_MODE = %s ms ' % (int((time.time() - a)*1000)))

#        a = time.time()
#        rs.req_sts(ser)
#        sts = rx_specific_packet('STS_OUT', '232', timeout=3)
#        if sts == []: print("error")
#        print(u' 3 время REQ_STS и STS_OUT = %s ms ' % (int((time.time() - a)*1000)))

#        a = time.time()
#        rs.set_default(ser)
#        sts = rx_specific_packet('STS_OUT', '232', timeout=3)
#        if sts == []: print("error")
#        print(u' 4 время SET_DEFAULT и STS_OUT = %s ms \n' % (int((time.time() - a)*1000)))

#        rs.req_sts(ser)
#        a = time.time()
#        sts = rx_specific_packet('STS_OUT', '232', timeout=3)
#        if sts == []: print("error")
#        print(u' \n 4 время между REQ_STS и STS_OUT = %s ms ' % (int((time.time() - a)*1000)))


        time.sleep(switching_period)



def logger_init():
    level = logging.DEBUG
    # создаем логгер в консоль и файл
    log = logging.getLogger()
    log.setLevel(level)
    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(name)-8s %(levelname)-6s '
                                  '%(message)s') #datefmt='%H:%M:%S'
    consoleHandler.setFormatter(formatter)
    log.addHandler(consoleHandler)
    now = datetime.datetime.now()
    filename = now.strftime("%Y_%m_%d %H-%M-%S") + '.log'
    fileHandler = logging.FileHandler(filename, mode='w')
    fileHandler.setFormatter(formatter)
    log.addHandler(fileHandler)
    return log
    #log.critical('LOGGING: name = %s, level = %s, handlers = %s' % (log.name, log.getEffectiveLevel(), log.handlers[:]))


def ts_signal_diag(ser):
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
            def request_levels(ser):
                def hex2bytes(string):
                    return binascii.unhexlify(string.replace(' ', ''))
                send = 'F7 2D 00'
                ser.write(hex2bytes(send))

            if f1 == 1:
                self.dot1_pressed = True
                self.draw_dot(x1, y1, self.dot1_pressed_color)
            else:
                if self.dot1_pressed is True:
                    self.draw_dot(x1, y1, self.dot1_released_color)
                    self.dot1_pressed = False
                    time.sleep(0.1)
                    request_levels(ser)
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

        def upd_levels(self, lvl):
                brdr = gr.Rectangle(gr.Point(0, 0), gr.Point(1023, 767))
                brdr.setOutline(cBlack)
                brdr.setFill(cBlack)
                brdr.draw(self.window)

                tt = gr.Text(gr.Point(511, 100), u'Проверка экрана raw')
                tt.draw(self.window)
                tt.setTextColor(cWhite)
                tt.setSize(16)

                xmin = 380
                x = xmin
                y = 200
                for n in xrange(52):
                    x = x + 40
                    if n % 8 == 0:
                        y = y + 14
                        x = xmin
                    tt = gr.Text(gr.Point(x, y), str(lvl[n]))
                    tt.draw(self.window)
                    if lvl[n] >= 3800:
                        tt.setTextColor(cGreen)
                    if lvl[n] >= 2000 and lvl[n] < 3800:
                        tt.setTextColor(cYellow)
                    if lvl[n] < 2000:
                        tt.setTextColor(cRed)
                    tt.setSize(10)

                for n in xrange(6):
                    x = xmin - 60
                    y = 214 + n * 14
                    tt = gr.Text(gr.Point(x, y), 'VD/VT %s-%s: ' % (n * 8 + 1, n * 8 + 8))
                    tt.draw(self.window)
                    tt.setTextColor(cWhite)
                    tt.setSize(10)

                x = xmin - 60
                y = y + 14
                tt = gr.Text(gr.Point(x, y), 'VD/VT 49-52: ')
                tt.draw(self.window)
                tt.setTextColor(cWhite)
                tt.setSize(10)

                for n in xrange(7, 12):
                    x = xmin - 60
                    y = 236 + n * 14
                    tt = gr.Text(gr.Point(x, y), 'VD/VT %s-%s: ' % (n * 8 + 1 - 4, n * 8 + 8 - 4))
                    tt.draw(self.window)
                    tt.setTextColor(cWhite)
                    tt.setSize(10)


                x = xmin
                y = 320
                for n in xrange(52, 92):
                    x = x + 40
                    if (n + 4) % 8 == 0:
                        y = y + 14
                        x = xmin
                    tt = gr.Text(gr.Point(x, y), str(lvl[n]))
                    tt.draw(self.window)
                    if lvl[n] >= 3800:
                        tt.setTextColor(cGreen)
                    if lvl[n] >= 2000 and lvl[n] < 3800:
                        tt.setTextColor(cYellow)
                    if lvl[n] < 2000:
                        tt.setTextColor(cRed)
                    tt.setSize(10)

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
        if rs232_ts_raw_q:
            lvl = rs232_ts_raw_q.popleft()
            lvl.popleft()
            lvl.popleft()
            lvl.popleft()
            lvl.pop()
            signals = []
            for n in xrange(74):
                signals.append((lvl.popleft() << 7) + lvl.popleft());
            w.upd_levels(signals)
    w.close()




def pmf_60_jakunin(ser):
    def hex2bytes(string):
        return binascii.unhexlify(string.replace(' ', ''))

    def launch_test(test_num):
        send1 = 'FF %02X 01 01 03' % test_num
        ser.write(hex2bytes(send1))
        while 1:
            if ser.inWaiting() > 0:
                dat = ser.read(ser.inWaiting())
                print(dat)
                for each in dat:
                    if each == '#': return 0

            time.sleep(1)

        print("END")

#    while 1:
    print("start time: %s:%s" % (time.localtime().tm_hour, time.localtime().tm_min))
    launch_test(7)
#        time.sleep(1)

#
#    t0 = time.clock()
#    launch_test(8)
#    print("test time - %s" % (time.clock() - t0))
#
#    t0 = time.clock()
#    launch_test(9)
#    print("test time - %s" % (time.clock() - t0))
#
#    t0 = time.clock()
#    launch_test(8)
#    print("test time - %s" % (time.clock() - t0))


def main():
#    log = logger_init()
    print(chr(12)) #очистка экрана консоли
    global run
#    log.critical(u'<<< НАЧАЛО ТЕСТИРОВАНИЯ >>>')
    def launch_threads(ser_rs232, ser_mdc):
        th1 = threading.Thread(name='rs232', target=inq, args=(ser_rs232, mbx_232))
        #th2 = threading.Thread(name='th_mdc', target=inq, args=(ser_mdc, mbx_mdc))
        th3 = threading.Thread(name='switch_232', target=inq_switch, args=(mbx_232, '232'))
        th31 = threading.Thread(name='old', target=old_packet_parser)
#        th4 = threading.Thread(name='size', target=fifo_size_out)
        th1.start()
        #th2.start()
        th3.start()
        th31.start()
#        th4.start()
        th_list = []
        th_list.append(th1)
        #th_list.append(th2)
        th_list.append(th3)
        th_list.append(th31)
#        th_list.append(th4)
        return th_list



    def set_brt_mdc(ser):
        def h2b(string):
            return binascii.unhexlify(string.replace(' ', ''))

        send1 = 'C0 10 FF 03'
        print(send1)
        ser.write(h2b(send1))


    try:

        if not False:  # init_fail:
            with serial.Serial('COM11', baudrate=9600, parity=serial.PARITY_NONE) as ser:
#                set_brt_mdc(ser)


#                w = tk.Tk()
#                mode_button = tk.Button(w)
#                mode_button['text'] = 'EXTENDED MODE'
#                mode_button['command'] = set_mode_extended
#                mode_button.pack()
#
#                brt_max_button = tk.Button(w)
#                brt_max_button['text'] = 'BRIGHTNESS MAX'
#                brt_max_button['command'] = brightness_max
#                brt_max_button.pack()
#
#                brt_min_button = tk.Button(w)
#                brt_min_button['text'] = 'BRIGHTNESS MIN'
#                brt_min_button['command'] = brightness_min
#                brt_min_button.pack()
#
#                test_button = tk.Button(w)
#                test_button['text'] = 'RUN TEST'
#                test_button['command'] = pt.main
#                test_button.pack()
#                w.mainloop()
#                log.debug('RS-232: %s' % ser)
                #with serial.Serial(COM_RS422, baudrate=19200) as ser422:
                #with serial.Serial('COM6', baudrate=9600) as psh_ser:
                th_list = launch_threads(ser, ser)  # загрузка FIFO

#                rs.set_mode(ser, u'расширенный')

#                pmf_60_jakunin(ser)

#                touch.ts_raw_visualise(ser)
#                rs.set_mode(ser, u'технологический')
#                rs.set_brit(ser, 0x50)
#                lcd.response_time_move()
#                rs.set_heater(ser,[0x00, 0x00])
#                rs.set_splash(ser, u'вкл')
##                rs.set_splash(ser, u'выкл')
#                time.sleep(1)
#                data = [28,9,0x61,0x0F,12,14,1]
#                rs.set_manuf_time(ser, data)
#                time.sleep(1)
#
#                rs.set_mode(ser, u'штатный')
#
#                time.sleep(1)
#                rs.save_param(ser)
#                rs.set_btnbrt(ser, [0xFE, 0xFE, 0x00, 0x00])


#                param = [0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x05, 0x03, 0xCD, 0x00]
#                param = [0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x05, 0x03, 0x00, 0x00]
#                param = [0x11, 0x46, 0x46, 0x46, 0x0A, 0x0A, 0x0A, 0x58, 0x00, 0x00, 0x00, 0x88, 0x77, 0xFC, 0xAB, 0x00]

#                param = [0x11, 0x46, 0x46, 0x46, 0x0A, 0x0A, 0x0A, 0x58, 0x00, 0x00, 0x00, 0x88, 0x77, 0x04, 0x00, 0x00]
#                param = [0x02, 0x46, 0x46, 0x46, 0x0A, 0x0A, 0x0A, 0x58, 0x00, 0x00, 0x00, 0x88, 0x77, 0x01, 0x00, 0x00]
#                rs.set_param(ser, param)
#                time.sleep(0.5)
#                rs.set_off_mode(ser, [7])
#                time.sleep(1)
#                rs.cmd_off_timeout(ser,[0x30, 0x55, 0x30, 0xE7])
#                time.sleep(1)
#                time.sleep(1)
#                rs.set_off_mode(ser, [3])
#                time.sleep(1)
#                rs.cmd_off_timeout(ser,[0x03, 0x55, 0x03, 0xE7])
#                for n in xrange(0, 240, 10):
#                    rs.set_btnbrt(ser, [n, n, 0x00, 0x00])
#                    time.sleep(0.5)
#                sts_requester(ser, 200)
#                full_brt(ser)
#                rs.set_ID(ser, [0x10, 0x30, 0x30, 0x31, 0x32, 0x00, 0x00, 0x00, 0x00, 0x00])
                #pwr.pmf32_set_pwrcodes(ser, 4.31, 40, 60, -3, 0, 60)
#                pwr.pmf32_set_pwrcodes(ser, 4, 60, 60, 60, 70, 60)
                #touch.trash_mark(ser)
#                touch.border(ser)
                #time.sleep(1)
                #rs.save_param(ser)
                #chk.chk01_set_mode(ser)
#                sts_decription(ser, log)
                #chk.function_control(ser, 1000, True)
#                chk.req_resp(ser)
                #chk.phase_in(ser)
#                chk.keys_brit(ser)
                #chk.SET_ID_test(ser)
#                chk.SET_BRIT_test(ser)
#                chk.SET_BRIT_roll(ser)
#                chk.VGA_LVDS_SWITCH(ser)
#                ts_signal_diag(ser)

#                touch.tap_count(ser)
#                touch.coord_delay_squares(ser)
                touch.coord_drawer_232(ser)
#                rs.set_mode(ser, u'технологический')
#                rs.set_key_mode(ser, 1)
#                keys.key_test(ser, one_point=True)
#                touch.coord_delay_test(ser)
#                touch.coord_8x8_grid_test(ser)
#                touch.coord_bug(ser)

#                rs.set_mode(ser, u'расширенный')
#                time.sleep(0.5)
#                clear_all_q()
#                flag = True
#                for n in xrange(1, 1000):
#
#                    vid = 2
#                    vif = 2
#                    #         4     5     6     7     8     9    10    11    12    13    14    15    16    17    18    19
#                    param = [vid, 0x46, 0x46, 0x46, 0x0A, 0x0A, 0x0A, 0x58, 0x00, 0x00, 0x00, 0x06, 0x0A, vif, 0x00, 0x00]
#                    rs.set_param(ser, param)
#                    log.debug(u'LVDS')
#                    flag = not flag
#                    time.sleep(5)
#
#
#                    vid = 0xFE
#                    vif = 3
#                    #         4     5     6     7     8     9    10    11    12    13    14    15    16    17    18    19
#                    param = [vid, 0x46, 0x46, 0x46, 0x0A, 0x0A, 0x0A, 0x58, 0x00, 0x00, 0x00, 0x06, 0x0A, vif, 0x00, 0x00]
#                    rs.set_param(ser, param)
#                    log.debug(u'ETH')
#                    flag = not flag
#                    time.sleep(5)



                run = False
                stop_threads(th_list)
                logger_close()
        else:
            print(u'Инициализация закончилась с ошибкой')
    except AssertionError as ae:
        print(u'Assertion: ', ae)
    except Exception as e:
        print(u'Что-то пошло не так: ', e)
    else:
        print(u'Сбоев в коде не было')
    finally:
        print(u'Это конец...',)

        return 0


def main2():
    def launch_threads(ser_rs232, ser_mdc):
        th1 = threading.Thread(name='rs232', target=inq, args=(ser_rs232, mbx_232))
        th2 = threading.Thread(name='sw', target=inq_switch, args=(mbx_232, '232'))
        th3 = threading.Thread(name='size', target=fifo_size_out)
        th1.start()
        th2.start()
        th3.start()
        th_list = []
        th_list.append(th1)
        th_list.append(th2)
        th_list.append(th3)
        return th_list

    try:
        with serial.Serial('COM11', baudrate=9600) as ser:
            rs.set_mode(ser, u'расширенный')

    except AssertionError as ae:
        print(u'Assertion: ', ae)
#    except Exception as e:
#        print(u'Что-то пошло не так: ', e)
    else:
        print(u'Сбоев в коде не было')
    finally:
        print(u'Это конец...',)
        return 0


if __name__ == "__main__":
    main()
