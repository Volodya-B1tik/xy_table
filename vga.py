# -*- coding: utf-8 -*-
"""
Created on Wed Mar 02 22:56:33 2016

@author: User
"""

import win32api
import win32con
import pywintypes

#==============================================================================
# Ищем все видеоустройства и кладем имена в словарь [devices]. Ключ - номер
# устройства начиная с нуля.
#==============================================================================

def devlist():
    devices = {}
    n = 0
    while True:
        try:
            device = win32api.EnumDisplayDevices(None, n)
        except pywintypes.error:
            break
        else:
#            print u'Видеоадаптер №%s' % n
#            print device.DeviceName
#            print device.DeviceString
#            print device.StateFlags
#            print device.DeviceID
#            print device.DeviceKey
#            print '----------------------'
            devices[n] = device.DeviceName
            n += 1
    return devices

def modelist(device_name):
    display_modes = {}
    n = 0
    while True:
        try:
            devmode = win32api.EnumDisplaySettings(device_name, n)
        except pywintypes.error:
            break
        else:
            key = (
                   devmode.BitsPerPel, 
                   devmode.PelsWidth, 
                   devmode.PelsHeight, 
                   devmode.DisplayFrequency,
                   devmode.DisplayOrientation
                  )
            display_modes[key] = devmode
            #print key
            n += 1
    return display_modes
    
#==============================================================================
#You now have a dictionary [display_modes], keyed on the
#height, width and depth needed. All you have to do to
#switch is something like this:
#mode_required = (32, 1024, 768, 60, 0)
#devmode = display_modes[mode_required]
#win32api.ChangeDisplaySettingsEx(device_name, devmode, 0)
#==============================================================================    
    
def change_resolution(device_name, display_modes, mode_required):
    devmode = display_modes[mode_required]
    win32api.ChangeDisplaySettingsEx(device_name, devmode, 0)

def current_resolution(device_name):
    devmode = win32api.EnumDisplaySettings(device_name, win32con.ENUM_CURRENT_SETTINGS)
    key = (
            devmode.BitsPerPel, 
            devmode.PelsWidth, 
            devmode.PelsHeight, 
            devmode.DisplayFrequency,
            devmode.DisplayOrientation
            )
    print '_______ \n', key
    

