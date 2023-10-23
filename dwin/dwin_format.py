#!/usr/bin/python
import sys

dwin_header = "5AA5"
dwin_write = "82"
dwin_read = "83"
dwin_done = "4FFB"

def size_in_byte(value):
    size = len(value)
    # 
    if size % 2 == 0:
        size = int(size / 2)
        return size
    else:
        print("{}: is invalid length, type only pair hex char".format(size))
        sys.exit(0)

def check_addr(addr):
    size = size_in_byte(addr)
    if size == 2:
        print("{}: is valid length".format(size))
        return True
    else:
        print("{}: is invalid addr length, dwin addr uses 2bytes".format(size))
        return False

def check_data(data):
    size = size_in_byte(data)
    if size:
        return True
    else:
        print("data is empty!")
        return False

def dwin_conv_to_hex(msg_frame):
    msg_frame_len = len(msg_frame)
    msg_frame_ret = ""
    # add hex notation for each byte in a string.
    for index in range(0, msg_frame_len, 2):
        str_byte = msg_frame[index:(index + 2)]
        msg_frame_ret = msg_frame_ret + "\\x" + str_byte
    # return string formated to hex value.
    return msg_frame_ret

def conv_int_to_hex(value):
    if value < 16:
        value = ("0{0:X}".format(value))
    else:
        value = ("{0:X}".format(value))
    
    return value

def dwin_validate(msg_frame):
    msg_len = len(msg_frame)
    
    if (msg_len %2) == 0:
        return True
    else:
        print("{}: is invalid length, try to use messages in pair of bytes".format(msg_frame))
        return False

def dwin_format(msg_frame):
    msg_frame = msg_frame.upper()
    
    if dwin_validate(msg_frame):
        msg_frame = dwin_conv_to_hex(msg_frame)
        return msg_frame
    else:
        return 
    
def dwin_make_frame(addr, data):
    check_addr(addr)
    # size = int((len(data) + len(addr)) / 2)
    # size = conv_int_to_hex(size)
    # msg_frame = dwin_header + size + addr + data
    # return dwin_format(msg_frame)
    

def main():
    msg_frame = "5aa50482500001"
    msg_frame = dwin_format(msg_frame)
    print("msg_frame:{}".format(msg_frame))

if __name__ == "__main__":
    main()