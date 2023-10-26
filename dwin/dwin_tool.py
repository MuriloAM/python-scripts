#!/usr/bin/python
from dwin_format import dwin_serialize
from time import sleep

class Dwin:
    DWIN_WRITE = "82"
    DWIN_READ = "83"

    def __init__(self, width, height, port):
        self.width = width
        self.height = height
        self.port = port
    
    def write(self, addr, data):
        msg = dwin_serialize("82", addr, data)

        pass

if __name__ == "__main__":
    def main(addr, data):
        print("running main()")
        # dwin = Dwin(800, 480, "COM6")
        # dwin_msg = dwin_serialize(addr, data)
    
    dwin_addr = "5000"
    dwin_data = ""
    main(dwin_addr, dwin_data)