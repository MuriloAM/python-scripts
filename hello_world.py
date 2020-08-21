#!usr/bin/python

import time
import threading
import queue

class myThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print ("Starting " + self.name)
        # Get lock to synchronize threads
        threadLock.acquire()
        print_time(self.name, self.counter, 3)
        # Free lock to release next thread
        threadLock.release()

def print_time(threadName, delay, counter):
    while counter:
        time.sleep(delay)
        print ("%d %s: %s" % (counter, threadName, time.ctime(time.time())))
        counter -= 1
            

if __name__ == "__main__":
    # variables.
    threadLock = threading.Lock()
    threadList = []

    # creating queues.
    #queueLock = threading.Lock()
    counterQueue = queue.Queue(10)

    # creating threads.
    thread1 = myThread(1, "Thread-1", 1)
    thread2 = myThread(2, "Thread-2", 2)
    # starting threads.
    thread1.start()
    thread2.start()
    # adding thread to threadList.
    threadList.append(thread1)
    threadList.append(thread2)

    # main loop
    while True:
        time.sleep(0.1)