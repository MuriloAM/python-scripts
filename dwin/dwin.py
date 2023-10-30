from dwin_conn import *

display = DwinConn("/dev/ttyUSB0", 115200)
display.write("5000", "61686564")
rx = display.read("5000", "7D")
print("rx:{}".format(rx))
del display