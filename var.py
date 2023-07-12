# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 23:58:07 2017

@author: User
"""
import graphics as gr
import collections as coll


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