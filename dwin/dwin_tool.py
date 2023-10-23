#!/usr/bin/python
from dwin_format import dwin_make_frame

class Dwin:
    def __init__(self, width, height, port):
        self.width = width
        self.height = height
        self.port = port
    

def main():
    dwin = Dwin(800, 480, "COM6")

if __name__ == "__main__":
    main()