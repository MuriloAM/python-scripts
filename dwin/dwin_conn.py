#!/usr/bin/python
import sys
import glob
import serial
import serial.tools.list_ports as port_list
from time import sleep
from dwin_format import dwin_serialize
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
            # print("rx_msg:{}".format(rx_msg))
            return rx_msg
        else:
            return None
        
    def write(self, addr, data):
        if self.s.in_waiting > 0:
            print("rx_buffer is full")
        else:
            rx = None
            tx_msg = dwin_serialize(DWIN_WRITE, addr, data)
            self.s.write(tx_msg)
            while rx is None:
                rx = self.update()
            return rx
        
    def read(self, addr, len):
        len_in_hex = "0x" + len
        len_msg = int(len_in_hex, 16)
        if len_msg > 0x7C:
            len = "7C"
        tx_msg = dwin_serialize(DWIN_READ, addr, len)
        self.s.write(tx_msg)
        while self.s.in_waiting == 0:
            pass
        if self.s.in_waiting > 0:
            return self.s.readline().hex().upper()
    
    def reboot(self):
        rst_msg = dwin_serialize(DWIN_WRITE, SYS_RST_ADDR, SYS_RST_DATA)
        self.s.write(rst_msg)
    
    def get_page(self):
        page_msg = dwin_serialize(DWIN_READ, PIC_NOW, "01")
        self.s.write(page_msg)
        return self.s.readline().hex().upper()

    def set_page(self, page):
        page_msg = dwin_serialize(DWIN_WRITE, PIC_SET, "01")
        self.s.write(page_msg)
        return self.s.readline().hex().upper()

if __name__ == "__main__":
    def write_frame(addr, data):
        HEADER = "5AA5"
        if data < 16:
            data = ("0{0:X}".format(data))
        else:
            data = ("{0:X}".format(data))
        
        body_data = "82{}{}".format(addr, data)
        body_len = int(len(body_data) / 2)

        if body_len < 16:
            body_len = ("0{0:X}".format(body_len))
        else:
            body_len = ("{0:X}".format(body_len))

        msg_frame = "{}{}{}".format(HEADER, body_len, body_data)
        
        return msg_frame
    
    def main(port, baud):

        serialPort = serial.Serial(port, baud, timeout= 0.1)

        while not serialPort.is_open:
            print("port:{} disconnected, try to reconnect...".format(serialPort.port))
            serialPort.open()
            sleep(0.5)

        try:
            serialPort.flushInput()
            serialPort.flushOutput()
            print("name:{}, port:{} is connected, send a message".format(serialPort.name, serialPort.port))

            val = 0

            while True:
                if serialPort.in_waiting > 0:
                    print("tem algo na serial, len:{}".format(serialPort.in_waiting))
                    msg_in = serialPort.readline()
                    print("rx:{}".format(msg_in.hex().upper()))
                elif val < 10:
                    hex_string = write_frame(5002, val)
                    print("tx:{}".format(hex_string))
                    # prepara str to hex format
                    hex_bytes = bytes.fromhex(hex_string)
                    serialPort.write(hex_bytes)
                    val = val + 1
                    sleep(1)
                
        except KeyboardInterrupt:
            print("\nclosing serialPort:{}".format(serialPort.port))
            serialPort.close()
        
        finally:
            print("\ntranmission done closing serialPort:{}".format(serialPort.port))
            serialPort.close()
    
    print("OS:{}".format(sys.platform))
    print("available com port:{}".format(serial_ports()))
    main("/dev/ttyUSB0", 115200)