#!/usr/bin/python
import sys
import glob
import serial
import serial.tools.list_ports as port_list
from time import sleep

def search_comport(comport):
    # print("search for COMx ports...")
    # ports = list(port_list.comports())
    # for p in ports:
    #     print("{}".format(ports))
    #     if ports == comport:
    #         return True
    # if comport isn't found in ports return False
    return False

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

def main():
    serialPort = serial.Serial(
        port =  "COM3", 
        baudrate = 115200, 
        bytesize = serial.EIGHTBITS, 
        parity = serial.PARITY_EVEN, 
        stopbits = serial.STOPBITS_ONE, 
        timeout = 10, 
        xonxoff = False, 
        rtscts = False, 
        write_timeout = 5, 
        dsrdtr = False, 
        inter_byte_timeout = None, 
        exclusive = None)
    # serialPort.port = 'COM6'
    # serialPort.timeout = 1.0
    # serialPort.baudrate = 115200
    # serialPort.parity = 'N'
    # serialPort.bytesize = 8
    # serialPort.stopbits = 1
    
    # if search_comport(serialPort.port):
    #     print("{}: found".format(serialPort.port))
    # else:
    #     print("{}: not found".format(serialPort.port))
    
    # serialPort.open()
    # serialPort.write(b'download')
    # if serialPort.is_open():
        # print("port:{} is open()".format(serialPort.port))
    # else:
        # print("port:{} is not open()".format(serialPort.port))
    serialPort.write(b'A')
    serialPort.close()
    
    # serialString = ""  # Used to hold data coming over UART
    # while 1:
    #     # Wait until there is data waiting in the serial buffer
    #     if serialPort.in_waiting > 0:

    #         # Read data out of the buffer until a carraige return / new line is found
    #         serialString = serialPort.readline()

    #         # Print the contents of the serial data
    #         try:
    #             print(serialString.decode("Ascii"))
    #         except:
                # pass

if __name__ == "__main__":
    print(serial_ports())
    main()
    