#!/usr/bin/python
import sys

DWIN_HEADER = "5AA5"

def size_in_byte(value):
    size = len(value)
    # 
    if size % 2 == 0:
        size = int(size / 2)
        return size
    else:
        print("{}: is invalid length, type only pair hex char".format(size))
        sys.exit(0)


def conv_int_to_hex(value):
    if value < 16:
        value = ("0{0:X}".format(value))
    else:
        value = ("{0:X}".format(value))
    
    return value

def check_addr(addr):
    addr_len = size_in_byte(addr)
    if addr_len != 2:
        print("{}: is invalid addr length, dwin addr uses 2bytes".format(addr_len))
        sys.exit(0)

def check_comm(comm):
    comm_len =  size_in_byte(comm)
    if comm_len != 1:
        print("{}: is invalid comm length".format(comm_len))
        sys.exit(0)

def check_data(data):
    data_len = size_in_byte(data)
    if data_len == 0:
        print("data can't be null")
        sys.exit(0)

def get_pack_len(comm, addr, data):
    pack_len = comm + addr + data
    pack_len = int(len(pack_len) / 2)
    pack_len = conv_int_to_hex(pack_len)
    # print("pack_len:{}".format)
    return pack_len

def dwin_conv_to_hex(msg_frame):
    msg_frame = msg_frame.upper()
    msg_frame_len = len(msg_frame)
    msg_frame_ret = ""
    # add hex notation for each byte in a string.
    for index in range(0, msg_frame_len, 2):
        str_byte = msg_frame[index:(index + 2)]
        msg_frame_ret = msg_frame_ret + "\\x" + str_byte
    # return string formated to hex value.
    return msg_frame_ret

def dwin_make_frame(comm, addr, data):
    # check addr, it has to be 2bytes size
    check_addr(addr)
    # check data, it has to be at least 2bytes, cannot be null
    check_data(data)
    # packge_len of command + addr + data
    check_comm(comm)
    pack_len = get_pack_len(comm, addr, data)
    # print("pack_len:{} bytes".format(pack_len))
    # concatenate DWIN_HEADER + package_len + command + addr + data
    out_frame = DWIN_HEADER + pack_len + comm + addr + data
    # convert to hex represented string
    out_frame = dwin_conv_to_hex(out_frame)
    # print("dwin_out:{}".format(out_frame))
    # return package frame
    return out_frame

def main():
    dwin_frame = dwin_make_frame("82", "5000", "82508090AAdEcadeafcedafafe")
    print("frame_out:{}".format(dwin_frame))

if __name__ == "__main__":
    main()