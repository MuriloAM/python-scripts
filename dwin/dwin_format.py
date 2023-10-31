#!/usr/bin/python
import sys

HEADER = "5AA5"
ADDR_LEN = 2

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

def check_comm(cmd):
    comm_len =  size_in_byte(cmd)
    if comm_len != 1:
        print("{}: is invalid cmd length".format(comm_len))
        sys.exit(0)

def check_data(data):
    data_len = size_in_byte(data)
    if data_len == 0:
        print("data can't be null")
        sys.exit(0)

def get_pack_len(cmd, addr, data):
    pack_len = cmd + addr + data
    pack_len = int(len(pack_len) / 2)
    pack_len = conv_int_to_hex(pack_len)
    return pack_len

def serialize(cmd, addr, data):
    """ Check cmd addr and data sizes create a frame with header and message size
        convert all frame bytes to hex-string to be able to be transmitted via serial.
        
        addr len is 2(bytes)
        cmd len is 2(bytes)
        data cannot be less than 1byte

        frame format:
        header + size + cmd + addr + data(bytes)
        5AA5     04     82    5000   01         -> write 01B on addr 0x5000
        5AA5     04     83    5000   01         -> read 01 byte from addr 0x5000

        write confirmation:
        header + size + cmd + response(bytes)
        5AA5     03     82    4FFB

    """
    # check addr, it has to be 2bytes size
    check_addr(addr)
    # check data, it has to be at least 2bytes, cannot be null
    check_data(data)
    # packge_len of command + addr + data
    check_comm(cmd)
    pack_len = get_pack_len(cmd, addr, data)
    # mount a frame to trasmit
    out_frame = HEADER + pack_len + cmd + addr + data
    out_frame = out_frame.upper()
    out_frame = bytes.fromhex(out_frame)
    return out_frame

def deserialize(data):
    return data.upper().hex()

if __name__ == "__main__":
    def main():
        dwin_frame = serialize("82", "5000", "01")
        print("frame_out:{}".format(dwin_frame))
    
    main()