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
        # print("body_data:{}, body_len:{}".format(body_data, body_len))
        
        return msg_frame
        # frame_data = "{}{}{}".format(HEADER, body_len, body_data)

        # print("msg:{}".format(frame_data))
        # return frame_data
        pass
    
    def main(port):

        serialPort = serial.Serial()
        
        serialPort.port =  port
        serialPort.baudrate = 115200
        serialPort.bytesize = serial.EIGHTBITS
        serialPort.parity = serial.PARITY_EVEN
        serialPort.stopbits = serial.STOPBITS_ONE
        serialPort.timeout = .1

        while not serialPort.is_open:
            print("port:{} disconnected, try to reconnect...".format(serialPort.port))
            serialPort.open()
            sleep(0.5)

        try:
            serialPort.flushInput()
            serialPort.flushOutput()
            print("port:{} is connected, send a message".format(serialPort.port))

            val = 0

            while True:
                line = serialPort.readline()
                line = line.hex()
                # data_raw = data_raw.upper()

                if line != "":
                    # my_str = str(line, 'utf-8')
                    # print(type(line))
                    print(line)
                    # print(my_str)
                    # print("data_raw:{}".format(data_raw))
                    break
                else:
                    hex_string = write_frame("5002", val)
                    # print("tx:{}".format(hex_string))
                    # prepara str to hex format
                    hex_bytes = bytes.fromhex(hex_string)
                    # serialPort.write(hex_bytes)
                    # 5AA5 06 83 5000 01 CABA
                    # 5a69204fe9

                    # val = val + 1
                    # if val > 10:
                    #     break
                    
                    # sleep(0.1)
                
        except KeyboardInterrupt:
            print("\nclosing serialPort:{}".format(serialPort.port))
            serialPort.close()
        
        finally:
            print("\ntranmission done closing serialPort:{}".format(serialPort.port))
            serialPort.close()
    
    def main2(port):
        try:
            display = dwin_conn(port, 115200)
            display.connect()
            while True:
                try:
                    
                    print("main2 is running")
                except:
                    pass
                
                sleep(5)
        except :
            print("except trig")
            pass
    
    print("OS:{}".format(sys.platform))
    print("available com port:{}".format(serial_ports()))
    main("/dev/ttyUSB0")
    