#!/usr/bin/python
import time
import threading
import queue

class tskOut(threading.Thread):
    def __init__(self, threadID, name, pQueue):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.pQueue = pQueue
    def run(self):
        print("starting:%s" %(self.name))
        while True:
            # Get lock to synchronize threads
            queueLock.acquire()
            if not self.pQueue.empty():
                data = self.pQueue.get()
                # Free lock to release next thread
                queueLock.release()
                # Show the command typed.
                print("command:%s" %(data))
            

class tskIn(threading.Thread):
    def __init__(self, threadID, name, pQueue):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.pQueue = pQueue
    def run(self):
        print("starting:%s" %(self.name))

        while True:
            command = input("$")
            if command == "new_comm" :
                # Fill the queue
                self.pQueue.put(command)
                queueLock.release()     


# main program.
if __name__ == "__main__":
    # Create new queues.
    pQueueOut = queue.Queue(10)
    queueLock = threading.Lock()

    # treads
    #threadLock = threading.Lock()
    threads = []

    # Create new threads.
    tsk_in_1 = tskIn(1, "tskIn", pQueueOut)
    tsk_out_1 = tskOut(2, "tskOut", pQueueOut)

    # Start new threads.
    tsk_out_1.start()
    tsk_in_1.start()

    # Add threads to thread list
    threads.append(tsk_out_1)
    threads.append(tsk_in_1)

    while True:
        time.sleep(0.3)