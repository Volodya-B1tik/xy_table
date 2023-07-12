# -*- coding: utf-8 -*-
"""
Created on Tue Mar 01 12:14:59 2016

@author: gubatenko
"""

from __future__ import print_function
import binascii
import logging

# размер пакета из ПМФ в ПЭВМ (в байтах)
packet_size = {
    'OLD_OUT': 5,
    'KEY_OUT': 5,
    'STS_OUT': 36,
    'COORD_OUT': 14,
    'KEY_SET_OUT': 6,
    'KEY_OFF_CLICKED': 5,
    'RECEIPT_OFF': 5,
    'STS_PMF': 50,
    'STS_VPIPE': 97,
    'STS_VPr1': 30,
    'STS_VPr2': 30,
    'STS_VPr3': 30,
    'STS_VPr4': 30,
    'STS_VGLV': 41,
    'STS_ETH1': 65,
    'STS_ETH2': 65,
    'STS_OVHP': 14,
    'TS_RAW_32': 152,
    'TS_RAW_6x': 188,
    'MANUF_TIME_OUT': 11}

# размер поля данных пакета из ПЭВМ в ПМФ (в байтах)
data_field_size = {
    'REQ_STS': 1,
    'SET_PARAM': 16,
    'SET_DEFAULT': 1,
    'SAVE_PARAM': 1,
    'SET_MODE': 1,
    'SET_BRIT': 1,
    'SET_KEY_MODE': 1,
    'SET_OFF_MODE': 1,
    'CMD_OFF_TIMEOUT': 4,
    'SET_VGA': 9,
    'SET_KEYS': 2,
    'SET_VPIPE': 93,
    'SET_ETH1': 52,
    'SET_ETH2': 52,
    'SET_VPr1': 14,
    'SET_VPr2': 14,
    'SET_VPr3': 14,
    'SET_VPr4': 14,
    'REQ_STS_ETH1': 1,
    'REQ_STS_ETH2': 1,
    'REQ_STS_VPr1': 1,
    'REQ_STS_VPr2': 1,
    'REQ_STS_VPr3': 1,
    'REQ_STS_VPr4': 1,
    'REQ_STS_VPIPE': 1,
    'REQ_STS_VGLV': 1,
    'SET_SPLASH': 1,
    'SET_HEATER': 2,
    'SET_OVHP': 6,
    'SET_ID': 10,
    'REQ_STS_OVHP': 1,
    'SET_MAXBRIT': 1,
    'SET_PWRCODES': 9,
    'SET_BTNBRT': 4,
    'SET_MANUF_TIME': 7,
    'REQ_PWRCODES': 1,
    'REQ_TS': 1,
    'REQ_MANUF_TIME': 1,
    'ETH_VIDEO_RX': 1,
    'SET_ETH': 1}

log = logging.getLogger(__name__)


def hex2bytes(string):
    return binascii.unhexlify(string.replace(' ', ''))


def cs_calc(data):
    CS = 0
    for each in data:
        CS = CS ^ each
    return CS


def decode_packet_id(pid):
    """ Расшифровка идентификатора пакета \n
        Вход: Идентификатор пакета (int)
        Выход: Строка с названием пакета в соответствии с Протоколом ИЛВ
        ПМФ-6 по каналу RS-232"""
    if pid == 0xe1: s = 'KEY_OUT'
    elif pid == 0xe2: s = 'STS_OUT'
    elif pid == 0xe3: s = 'COORD_OUT'
    elif pid == 0xe4: s = 'KEY_SET_OUT'
    elif pid == 0xe5: s = 'KEY_OFF_CLICKED'
    elif pid == 0xe6: s = 'RECEIPT_OFF'    
    elif pid == 0xd0: s = 'STS_PMF'
    elif pid == 0xd1: s = 'STS_VPIPE'
    elif pid == 0xd2: s = 'STS_VPr1'
    elif pid == 0xd3: s = 'STS_VPr2'
    elif pid == 0xd4: s = 'STS_VPr3'
    elif pid == 0xd5: s = 'STS_VPr4'
    elif pid == 0xd6: s = 'STS_VGLV'
    elif pid == 0xd7: s = 'STS_ETH1'
    elif pid == 0xd8: s = 'STS_ETH2'
    elif pid == 0xd9: s = 'STS_OVHP'
    elif pid == 0xdb: s = 'TS_RAW_32'
    elif pid == 0xdc: s = 'TS_RAW_6x'
    elif pid == 0xdd: s = 'MANUF_TIME_OUT'    
    else: s = u'неизвестный пакет %X' % pid
    #log.debug(u'%s начало приема пакета' % s)
    return s


def packet_cs_check(fifo):
    """ Проверка контрольной суммы (КС)\n
    Вход: Список содержащий данные (int) для вычисления КС и эталонную КС
    (последнее значение списка)
    Выход: True - если рассчетая КС совпала с эталонной, False - КС не
    совпали"""
    CS_rx = fifo.pop()
    CS = cs_calc(fifo)
    if CS != CS_rx:
        log.debug(u'КС не верна')
        return False
    else:
        pass
        #log.debug(u'КС верна')
        return True


def send_packet(ser, data):
    CS = cs_calc(data)
    send = 'FF FF '
    for d in data:
        send += "%0.2X " % d
    send += "%0.2X" % CS
    log.debug(send)
    ser.write(hex2bytes(send))


def req_sts(ser):
    """ Отправляет пакет REQ_STS в канал RS-232"""
    log.info(u'запрос статуса req_sts')
    data = [0xC1, 0]
    send_packet(ser, data)


def set_param(ser, data):
    """ Вход: список байт поля данных пакета SET_PARAM[4-19]
    Отправляет пакет SET_PARAM в канал RS-232"""
    log.info(u'установка параметров set_param=%s' % data)
    assert (len(data) == data_field_size['SET_PARAM']), 'set_param'
    data.insert(0, 0xC2)
    send_packet(ser, data)


def set_default(ser):
    """ Отправляет пакет SET_DEFAULT в канал RS-232"""
    log.info(u'восстановление заводских настроек')
    data = [0xC3, 0]
    send_packet(ser, data)


def save_param(ser):
    """ Отправляет пакет SAVE_PARAM в канал RS-232"""
    log.info(u'сохранение параметров в ПЗУ')
    data = [0xC4, 0]
    send_packet(ser, data)


def set_mode(ser, mode, bad_mode=False):
    """ Если bad_mode = False (по-умолчанию), то mode принимает строку с
    названием режима (штатный, технологический, расширенный). \n
        Если bad_mode = True, то в mode принимает любое значение от 0 до
        255."""
    log.info(u'установка режима %s' % mode)
    if not bad_mode:
        if mode == u'штатный':
            mode = 0
        elif mode == u'технологический':
            mode = 1
        elif mode == u'расширенный':
            mode = 2
        else:
            log.error(u'неправильный режим')
            return 0
    assert (0 <= mode <= 255), 'mode'
    data = [0xC5, mode]
    send_packet(ser, data)


def set_brit(ser, brightness=0xFE):
    """ Принимает число со значением яркости.
        Отправляет пакет SET_BRIT в канал RS-232"""
    log.info(u'яркость = %s' % brightness)
    assert (0 <= brightness < 0xFF), 'brightness'
    data = [0xC6, brightness]
    send_packet(ser, data)


def set_key_mode(ser, mode, bad_mode=False):
    """ Если bad_mode = False (по-умолчанию), то mode принимает строку с
    названием режима (одна кнопка, все кнопки). \n
        Если bad_mode = True, то в mode принимает любое значение от 0 до
        255 включительно."""
    log.info(u'установка режима %s' % mode)
    if not bad_mode:
        if (mode == u'одна кнопка') or (mode == 0):
            mode = 0
        elif (mode == u'все кнопки') or (mode == 1):
            mode = 1
        else:
            log.error(u'Неправильный режим передачи кнопок')
            return 0
    assert (0 <= mode <= 255), 'key mode'
    data = [0xC7, mode]
    send_packet(ser, data)


def set_vga(ser, data):
    """ Вход: список байт поля данных пакета SET_VGA[4-12]
    Отправляет пакет SET_VGA в канал RS-232"""
    log.info(u'установка параметров set_vga=%s' % data)
    assert (len(data) == data_field_size['SET_VGA']), 'set_vga'
    data.insert(0, 0xA0)
    send_packet(ser, data)


def set_keys(ser, data):
    """ Вход: список байт поля данных пакета SET_KEYs[4-5]
    Отправляет пакет SET_KEYs в канал RS-232"""
    log.info(u'установка параметров set_keys=%s' % data)
    assert (len(data) == data_field_size['SET_KEYS']), 'set_keys'
    data.insert(0, 0xA1)
    send_packet(ser, data)


def set_vpipe(ser, data):
    """ Вход: список байт поля данных пакета SET_VPIPE[4-96]
    Отправляет пакет SET_VPIPE в канал RS-232"""
    log.info(u'установка параметров set_vpipe=%s' % data)
    assert (len(data) == data_field_size['SET_VPIPE']), 'set_vpipe'
    data.insert(0, 0xA2)
    send_packet(ser, data)


def set_eth1(ser, data):
    """ Вход: список байт поля данных пакета SET_ETH1[4-55]
    Отправляет пакет SET_ETH1 в канал RS-232"""
    log.info(u'установка параметров set_eth1=%s' % data)
    assert (len(data) == data_field_size['SET_ETH1']), 'set_eth1'
    data.insert(0, 0xA3)
    send_packet(ser, data)


def set_eth2(ser, data):
    """ Вход: список байт поля данных пакета SET_ETH2[4-55]
    Отправляет пакет SET_ETH2 в канал RS-232"""
    log.info(u'установка параметров set_eth2=%s' % data)
    assert (len(data) == data_field_size['SET_ETH2']), 'set_eth2'
    data.insert(0, 0xA4)
    send_packet(ser, data)


def set_vpr1(ser, data):
    """ Вход: список байт поля данных пакета SET_VPr1[4-17]
    Отправляет пакет SET_VPr1 в канал RS-232"""
    log.info(u'установка параметров set_vpr1=%s' % data)
    assert (len(data) == data_field_size['SET_VPr1']), 'set_vpr1'
    data.insert(0, 0xA5)
    send_packet(ser, data)


def set_vpr2(ser, data):
    """ Вход: список байт поля данных пакета SET_VPr2[4-17]
    Отправляет пакет SET_VPr2 в канал RS-232"""
    log.info(u'установка параметров set_vpr2=%s' % data)
    assert (len(data) == data_field_size['SET_VPr2']), 'set_vpr2'
    data.insert(0, 0xA6)
    send_packet(ser, data)


def set_vpr3(ser, data):
    """ Вход: список байт поля данных пакета SET_VPr3[4-17]
    Отправляет пакет SET_VPr3 в канал RS-232"""
    log.info(u'установка параметров set_vpr3=%s' % data)
    assert (len(data) == data_field_size['SET_VPr3']), 'set_vpr3'
    data.insert(0, 0xA7)
    send_packet(ser, data)


def set_vpr4(ser, data):
    """ Вход: список байт поля данных пакета SET_VPr4[4-17]
    Отправляет пакет SET_VPr4 в канал RS-232"""
    log.info(u'установка параметров set_vpr4=%s' % data)
    assert (len(data) == data_field_size['SET_VPr4']), 'set_vpr4'
    data.insert(0, 0xA8)
    send_packet(ser, data)


def req_sts_eth1(ser):
    """ Отправляет пакет REQ_STS_ETH1 в канал RS-232"""
    log.info(u'запрос параметров req_sts_eth1')
    data = [0xA9, 0]
    send_packet(ser, data)


def req_sts_eth2(ser):
    """ Отправляет пакет REQ_STS_ETH2 в канал RS-232"""
    log.info(u'запрос параметров req_sts_eth2')
    data = [0xAA, 0]
    send_packet(ser, data)


def req_sts_vpr1(ser):
    """ Отправляет пакет REQ_STS_VPr1 в канал RS-232"""
    log.info(u'запрос параметров req_sts_vpr1')
    data = [0xAB, 0]
    send_packet(ser, data)


def req_sts_vpr2(ser):
    """ Отправляет пакет REQ_STS_VPr2 в канал RS-232"""
    log.info(u'запрос параметров req_sts_vpr2')
    data = [0xAC, 0]
    send_packet(ser, data)


def req_sts_vpr3(ser):
    """ Отправляет пакет REQ_STS_VPr3 в канал RS-232"""
    log.info(u'запрос параметров req_sts_vpr3')
    data = [0xAD, 0]
    send_packet(ser, data)


def req_sts_vpr4(ser):
    """ Отправляет пакет REQ_STS_VPr4 в канал RS-232"""
    log.info(u'запрос параметров req_sts_vpr4')
    data = [0xAE, 0]
    send_packet(ser, data)


def req_sts_vpipe(ser):
    """ Отправляет пакет REQ_STS_VPIPE в канал RS-232"""
    log.info(u'запрос параметров req_sts_vpipe')
    data = [0xAF, 0]
    send_packet(ser, data)


def req_sts_vglv(ser):
    """ Отправляет пакет REQ_STS_VGLV в канал RS-232"""
    log.info(u'запрос параметров req_sts_vglv')
    data = [0xB0, 0]
    send_packet(ser, data)


def req_sts_ovhp(ser):
    """ Отправляет пакет REQ_STS_OVHP в канал RS-232"""
    log.info(u'запрос параметров req_sts_ovhp')
    data = [0xB4, 0]
    send_packet(ser, data)


def set_splash(ser, mode, bad_mode=False):
    """ Если bad_mode = False (по-умолчанию), то mode принимает строку
    состояния экрана-заставки (вкл, выкл). \n
        Если bad_mode = True, то в mode принимает любое значение от 0 до
        255."""
    log.info(u'экран-заставка %s' % mode)
    if not bad_mode:
        if mode == u'выкл':
            mode = 0
        elif mode == u'вкл':
            mode = 1
        else:
            log.warning(u'Функции set_splash передан неправильный параметр')
            return 0
    if 0 <= mode <= 255:
        data = [0xB1, mode]
        send_packet(ser, data)


def set_heater(ser, data):
    """ Вход: список байт поля данных пакета SET_HEATER[4-5]
    Отправляет пакет SET_HEATER в канал RS-232"""
    log.info(u'устанока параметров подогрева set_heater=%s' % data)
    assert (len(data) == data_field_size['SET_HEATER']), 'set_heater'
    data.insert(0, 0xB2)
    send_packet(ser, data)


def set_ovhp(ser, data):
    """ Вход: список байт поля данных пакета SET_OVHP[4-9]
    Отправляет пакет SET_OVHP в канал RS-232"""
    log.info(u'установка параметров защиты от перегрева set_ovhp=%s' % data)
    assert (len(data) == data_field_size['SET_OVHP']), 'set_ovhp'
    data.insert(0, 0xB3)
    send_packet(ser, data)


def set_ID(ser, data):
    """ Вход: список байт поля данных пакета SET_ID[4-13]
    Отправляет пакет SET_ID в канал RS-232"""
    log.info(u'установка ID ПМФ = %s' % data)
    assert (len(data) == data_field_size['SET_ID']), 'set_ID'
    data.insert(0, 0xB4)
    send_packet(ser, data)


def set_off_mode(ser, data):
    log.info(u'установка режима выключения ПМФ = %s' % data)
    assert (len(data) == data_field_size['SET_OFF_MODE']), 'set_off_mode'
    data.insert(0, 0xC8)
    send_packet(ser, data)


def cmd_off_timeout(ser, data):
    log.info(u'команда выключения ПМФ = %s' % data)
    assert (len(data) == data_field_size['CMD_OFF_TIMEOUT']), 'cmd_off_timeout'
    data.insert(0, 0xC9)
    send_packet(ser, data)


def set_maxbrit(ser, data):
    log.info(u'установка максимальной яркости ПМФ = %s' % data)
    assert (len(data) == data_field_size['SET_MAXBRIT']), 'reg_maxbrit'
    data.insert(0, 0xB6)
    send_packet(ser, data)


def set_pwrcodes(ser, data):
    log.info(u'установка параметров подогрева ПМФ = %s' % data)
    assert (len(data) == data_field_size['SET_PWRCODES']), 'reg_powercodes'
    data.insert(0, 0xB7)
    send_packet(ser, data)


def set_btnbrt(ser, data):
    log.info(u'установка яркости кнопок включения и контекстных = %s' % data)
    assert (len(data) == data_field_size['SET_BTNBRT']), 'set_btnbrt'
    data.insert(0, 0xB8)
    send_packet(ser, data)


def req_pwrcodes(ser):
    """ Отправляет пакет REQ_PWRCODES в канал RS-232"""
    log.info(u'запрос параметров req_pwrcodes')
    data = [0xB9, 0]
    send_packet(ser, data)

def set_manuf_time(ser, data):
    log.info(u'установка даты и времени производства ПМФ')
    assert (len(data) == data_field_size['SET_MANUF_TIME']), 'set_manuf_time'
    data.insert(0, 0xBA)
    send_packet(ser, data)
    
def req_ts(ser):
    """ Отправляет пакет REQ_TS в канал RS-232"""
    data = [0xBB, 0]
    send_packet(ser, data)
    
def req_manuf_time(ser):
    data = [0xBC, 0]
    send_packet(ser, data)
    
def eth_video_rx(ser, data):
    assert (len(data) == data_field_size['ETH_VIDEO_RX']), 'ETH_VIDEO_RX'
    data.insert(0, 0xBD)
    send_packet(ser, data)

def set_eth(ser, eth_n):
    """ Принимает число с номером ETH 
        Отправляет пакет SET_ETH в канал RS-232"""
    assert (0 <= eth_n <= 1), 'set_eth'
    data = [0xDA, eth_n]
    send_packet(ser, data)
    