from dwin_conn import *

display = DwinConn("/dev/ttyUSB0", 115200)
display.write("5000", "61686564")
del display