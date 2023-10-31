from dwin_conn import *
from time import sleep

display = DwinConn("/dev/ttyUSB0", 115200)
try:
    while True:
        rx = display.update()
        if rx is not None:
            print("response:{}".format(rx))
            # rx = None
            # break
        else:
            # tx = "61686564"
            # print("tx:{}".format(tx))
            err = display.write("5000", "61686564")
            if err == "5AA503824F4B":
                print("write err:OK")
            else:
                print("write err:{}".format(err))
        sleep(1)
        # rx = display.read("5000", "7D")
        # print("rx:{}".format(rx))
        
except:
    print("finalizando diplay")
    del display