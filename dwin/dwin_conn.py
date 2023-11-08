#!/usr/bin/python
import sys
import glob
import serial
from dwin_format import serialize
from dwin_const import *
from time import sleep

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

    def verify(self, rx_msg, addr, len=None):
        if not rx_msg.startswith(DWIN_HEADER):
            return False
        # take only command from rx_msg
        comm = rx_msg[6:8]
        # verify write command response 
        if comm == DWIN_WRITE:
            data = rx_msg[8:]
            if data == DWIN_CONFIRM:
                return True
            else:
                return False
        # verify read command response and return only msg
        elif comm == DWIN_READ:
            # check if addr match
            rx_addr = rx_msg[8:12]
            if rx_addr != addr:
                return False
            # check if rx_len match
            rx_len = rx_msg[12:14]
            rx_len = int(rx_len, 16)
            len = int(len, 16)
            if rx_len != len:
                return False
            # split rx_msg 
            return rx_msg[14:]
    
    def update(self):
        rx_msg = None
        while self.s.in_waiting > 0:
            if rx_msg == None:
                rx_msg = ""
            rx = self.s.readline().hex().upper()
            rx_msg = rx_msg + rx
        return rx_msg
        
    def write(self, addr, data):
        if self.s.in_waiting > 0:
            print("rx_buffer is full")
        else:
            rx = None
            tx_msg = serialize(DWIN_WRITE, addr, data)
            self.s.write(tx_msg)
            while rx is None:
                rx = self.update()
            return self.verify(rx, addr)
        
    def read(self, addr, len):
        rx = None
        len_in_hex = "0x" + len
        len_msg = int(len_in_hex, 16)
        if len_msg > 0x7C:
            len = DWIN_READ_MAX_LEN
        tx_msg = serialize(DWIN_READ, addr, len)
        self.s.write(tx_msg)
        while rx is None:
            rx = self.update()
        return self.verify(rx, addr, len)
    
    def reboot(self):
        if self.write(DWIN_SYS_RST_ADDR, DWIN_SYS_RST_DATA):
            sleep(1)
            if self.s.in_waiting > 0:
                self.s.reset_input_buffer()
            return True
        else:
            return False
    
    def get_page(self):
        page = self.read(DWIN_PIC_NOW, DWIN_READ_1BYTE)
        page = page[14:]
        return int(page)

    def set_page(self, page):
        my_str = "{}{:04X}".format(DWIN_PIC_SET_EN, page)
        return self.write(DWIN_PIC_SET, my_str)

if __name__ == "__main__":
    print("OS:{}".format(sys.platform))
    print("available com port:{}".format(serial_ports()))
    # main("/dev/ttyUSB0", 115200)
