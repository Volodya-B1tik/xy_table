# -*- coding: utf-8 -*-
"""
Created on Mon Mar 07 22:45:48 2016

@author: gubatenko
"""
import time
import logging
import serial 

log = logging.getLogger("psh")

class psh3610(object):
    def __init__(self, port):
        self.com = port
        try:
            self.ser = serial.Serial(self.com, baudrate = 2400)
#            self.ser = serial.Serial(self.com, baudrate = 9600)
            print u'Порт %s открыт %s' % (self.com, self.ser.isOpen())
        except:
            print (u'Не получилось открыть порт %s' % self.com)
            raise
    
#    def __del__(self, type, value, traceback):
#        print u'Прощай жестокий мир'
#        self.ser.close()

    def rx(self, ser, timeout = 1):
        if ser.isOpen():
            t_start = time.clock()
            inbox = ''
            while time.clock() < t_start + timeout:
                while ser.inWaiting() > 0:
                    rx_byte = ser.read(1)
                    inbox += rx_byte
            return inbox

    def read_id(self, timeout = 1):
        log.info(u'PSH: запрос идентификации')
        s = '*IDN?\n'
        self.ser.write(s)
        r = self.rx(self.ser, timeout)
        if r == '':
            log.info(u'PSH: PSH не прислал данные за %s c' % timeout)
        else:
            log.info(u'PSH: PSH ответил: %s' % r)
        return r     
        
    def set_votage(self, volts, timeout = 1):
        
        get_voltage = -1.0
        log.info(u'PSH: команда на установку напряжения %s В' % volts)
        s = ':CHAN1:VOLT %s;VOLT?\n' % volts
        self.ser.write(s)
        r = self.rx(self.ser, timeout)
        if r == '':
            log.info(u'PSH: PSH не прислал данные за %s c' % timeout)
        else:
            try:
                get_voltage = float(r)
            except ValueError:
                log.info(u'PSH прислал не float')
        return get_voltage

    def set_votage_no_readback(self, volts):
        s = ':CHAN1:VOLT %s;VOLT?\n' % volts
        self.ser.write(s)
    
    def set_current(self, amps, timeout = 1):
     
        get_current = -1.0
        log.info(u'PSH: команда на установку тока %s А' % amps)
        s = ':CHAN1:CURR %s;CURR?\n' % amps
        self.ser.write(s)
        r = self.rx(self.ser, timeout)
        if r == '':
            log.info(u'PSH: PSH не прислал данные за %s c' % timeout)
        else:
            try:
                get_current = float(r)
            except ValueError:
                log.info(u'PSH: PSH прислал не float')
        return get_current
        
    def measure_current(self, timeout = 1):
        
        measured_current = -1.0
        log.info(u'PSH: команда на измерение тока')
        s = ':CHAN1:MEAS:CURR?\n'
        self.ser.write(s)
        r = self.rx(self.ser, timeout)
        if r == '':
            log.info(u'PSH: PSH не прислал данные за %s c' % timeout)
        else:
            try:
                measured_current = float(r)
            except ValueError:
                log.info(u'PSH: PSH прислал не float')
        return measured_current
    
    def measure_voltage(self, timeout = 1):

        measured_voltage = -1.0
        log.info(u'PSH: команда на измерение напряжения')
        s = ':CHAN1:MEAS:VOLT?\n'
        self.ser.write(s)
        r = self.rx(self.ser, timeout)
        if r == '':
            log.info(u'PSH: PSH не прислал данные за %s c' % timeout)
        else:
            try:
                measured_voltage = float(r)
            except ValueError:
                log.info(u'PSH: PSH прислал не float')
        return measured_voltage
    
    def set_ocp(self, ocp_state, timeout = 1):
        
        ocp = -1.0
        log.info(u'PSH: команда на вкл/выкл защиты по току: %s' % ocp_state)
        s = ':CHAN1:PROT:CURR %s;:CHAN1:PROT:CURR?\n' % ocp_state
        self.ser.write(s)
        r = self.rx(self.ser, timeout)
        if r == '':
            log.info(u'PSH: PSH не прислал данные за %s c' % timeout)
        else:
            try:
                ocp = float(r)
            except ValueError:
                log.info(u'PSH: PSH прислал не float')
        return ocp
    
    def set_ovp(self, ovp, timeout = 1):
        
        get_ovp = -1.0
        log.info(u'PSH: команда на установку защиты от перенапряжения')
        s = ':CHAN1:PROT:VOLT %s;:CHAN1:PROT:VOLT?\n' % ovp
        self.ser.write(s)
        r = self.rx(self.ser, timeout)
        if r == '':
            log.info(u'PSH: PSH не прислал данные за %s c' % timeout)
        else:
            try:
                get_ovp = float(r)
            except ValueError:
                log.info(u'PSH: PSH прислал не float')
        return get_ovp
   #TODO 
    def set_output(self, state, timeout = 1):
        
        output = -1.0
        log.info(u'PSH: команда на вкл/выкл выхода: %s' % state)
        s = ':CHAN1:OUTP:STAT %s;:CHAN1:OUTP:STAT?\n' % state
        self.ser.write(s)
        r = self.rx(self.ser, timeout)
        if r == '':
            log.info(u'PSH: PSH не прислал данные за %s c' % timeout)
        else:
            try:
                output = float(r)
                if output == 1:
                    log.info(u'PSH: выход ВКЛ')
                elif output == 0:
                    log.info(u'PSH: выход ВЫКЛ')
                else:
                    log.info(u'Ошибка! Хотели %s, получили %s' % (state, r))
            except ValueError:
                log.info(u'PSH: PSH прислал не float')
        return output
    
    def OPC(self, timeout = 1):

        output = -1.0
        s = '*OPC?\n'
        self.ser.write(s)
        r = self.rx(self.ser, timeout)
        if r == '':
            log.info(u'PSH: PSH не прислал данные за %s c' % timeout)
        else:
            try:
                output = float(r)
            except ValueError:
                log.info(u'PSH: PSH прислал не float')
        return output
    
    def setup(self, volt=27, curr=1.5, ovp=30, ocp=0, output=0, timeout=1):
        """ volt = 0-30; curr = 0-10; ovp = 0-30; ocp = 0/1; output = 0/1; \
        timeout = 0+ """
        self.set_votage(volt, timeout)
        self.set_current(curr, timeout)
        self.set_ovp(ovp, timeout)    
        self.set_ocp(ocp, timeout)
        self.set_output(output, timeout)

def test(port):
    ps = psh3610(port)
    ps.set_current(1)
   
def pmf51_test(port):
    ps = psh3610(port)
    ps.setup(volt=29, curr=1.5, ovp=30, ocp=0, output=0, timeout=1)
    
#    for i in xrange(1000):
#        ps.set_output(0)
#        time.sleep(1)
#        ps.set_output(1)
#        time.sleep(5)
#        cur = ps.measure_current()
#        print('current = %s') % cur
#        print('iterations = %s') % i
#        if cur < 0.8: break
    ps.set_output(1)
    time.sleep(1)

    for x in xrange(100):    
        for i in xrange(21, 29):
            ps.set_votage_no_readback(i)
            time.sleep(0.3)
            print('iterations = %s') % i
            
        for i in xrange(29, 21,-1):
            ps.set_votage_no_readback(i)
            time.sleep(0.3)
            print('iterations = %s') % i        
        
        

if __name__ == "__main__":
    test('COM6')
#    pmf51_test('COM6')