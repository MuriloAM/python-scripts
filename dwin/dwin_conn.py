#!/usr/bin/python
import sys
import glob
import serial
from dwin_format import serialize
from dwin_const import *

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

class DwinConn:

    def __init__(self, port, baud):
        self.s = serial.Serial(port, baud, timeout=0.1)
    
    def __del__(self):
        self.s.close()

    def update(self):
        if self.s.in_waiting > 0:
            rx_msg = self.s.readline().hex().upper()
            return rx_msg
        else:
            return None
        
    def write(self, addr, data):
        if self.s.in_waiting > 0:
            print("rx_buffer is full")
        else:
            rx = None
            tx_msg = serialize(DWIN_WRITE, addr, data)
            self.s.write(tx_msg)
            while rx is None:
                rx = self.update()
            return rx
        
    def read(self, addr, len):
        len_in_hex = "0x" + len
        len_msg = int(len_in_hex, 16)
        if len_msg > 0x7C:
            len = DWIN_READ_MAX_LEN
        tx_msg = serialize(DWIN_READ, addr, len)
        self.s.write(tx_msg)
        while self.s.in_waiting == 0:
            pass
        if self.s.in_waiting > 0:
            return self.s.readline().hex().upper()
    
    def reboot(self):
        # rst_msg = serialize(DWIN_WRITE, DWIN_SYS_RST_ADDR, DWIN_SYS_RST_DATA)
        # self.s.write(rst_msg)
        ret = self.write(DWIN_SYS_RST_ADDR, DWIN_SYS_RST_DATA)
        print("reboot ret:{}".format(ret))
    
    def get_page(self):
        page_msg = serialize(DWIN_READ, DWIN_PIC_NOW, DWIN_READ_1BYTE)
        self.s.write(page_msg)
        return self.s.readline().hex().upper()

    def set_page(self, page):
        page_msg = serialize(DWIN_WRITE, DWIN_PIC_SET, DWIN_READ_1BYTE)
        self.s.write(page_msg)
        return self.s.readline().hex().upper()

if __name__ == "__main__":
    print("OS:{}".format(sys.platform))
    print("available com port:{}".format(serial_ports()))
    # main("/dev/ttyUSB0", 115200)
