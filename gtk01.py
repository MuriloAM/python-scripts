#!/usr/bin/python
import time
import threading
import queue
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class tskGUI(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print("starting:%s" %(self.name))
        win = MyWindow()
        win.connect("destroy", Gtk.main_quit)
        win.show_all()
        Gtk.main()
        print("runing:%s" %self.name)
        #while True:
        time.sleep(5)
        print("stoping:%s" %self.name)

class tskKeyBoard(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print("starting:%s" %(self.name))
        
        while True:
            input("$:")

class tskShow(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print("starting:%s" %(self.name))
        while True:
            print("ola mundo")


class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Hello World")

        self.button = Gtk.Button(label="Click Here")
        self.button.connect("clicked", self.on_button_clicked)
        self.add(self.button)

    def on_button_clicked(self, widget):
        print("Hello World")


# main program.
if __name__ == "__main__":
    threadLock = threading.Lock()
    threads = []
    # Create new threads.
    #tsk_gui = tskGUI(1, "GUI")
    tsk_teclado = tskKeyBoard(1, "KeyBoard")
    tsk_show = tskShow(2, "tskShow")

    # Start new threads.
    #tsk_gui.start()
    tsk_teclado.start()
    tsk_show.start()

    # Add threads to thread list
    #threads.append(tsk_gui)
    threads.append(tsk_teclado)
    threads.append(tsk_show)

    while True:
        time.sleep(0.3)