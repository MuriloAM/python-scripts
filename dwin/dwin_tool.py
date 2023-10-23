#!/usr/bin/python
from dwin_format import dwin_make_frame

class Dwin:
    def __init__(self, width, height, port):
        self.width = width
        self.height = height
        self.port = port
    
    def write_ram(self, addr, data):
        msg_frame = dwin_make_frame(addr, data)
        print("msg_frame:{}".format(msg_frame))

def main():
    dwin = Dwin(800, 480, "COM6")
    dwin.write_ram("5000", "8476")

if __name__ == "__main__":
    main()