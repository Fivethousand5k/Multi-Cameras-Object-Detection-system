from multiprocessing import Process, Pipe
import  multiprocessing as mp
import time
import psutil
def send(queue,a):
    # queue.put(1)
    # queue.put(2)
    # queue.put(3)
    while True:
        print(a)
        queue.put(a)
        # time.sleep(1)
def talk(queue,a):
    while True:
        print(a)
        queue.get()
        # time.sleep(1)
    # pipe.send(dict(name = 'Bob', spam = 42))
    # print(queue.qsize())
    # print(queue.get())
    # print(queue.qsize())
    # print(queue.get())
    # print(queue.qsize())

if __name__ == '__main__':
    mp.set_start_method(method="spawn")
    queue=mp.Queue(maxsize=3)
    a=1
    sender = Process(target = send, name = 'send', args = (queue,a))
    sender.start()

    time.sleep(5)
    a=9