# import socket programming library
import socket
import random
# import thread module
from _thread import *
import threading

print_lock = threading.Lock()

host = ""
port = 50100

# thread function
def threaded(c):
    while True:
        data = c.recv(1024)
        if not data:
            print('Bye')

            # lock released on exit
            print_lock.release()#
            break
        keep_alive_str = 'Keep Alive'.decode()
        if c.recv(keep_alive_str):
            c
        # if c.recv('Keep Alive'.decode()):
        #     if c.recv('cmd1'.decode()):
        #         n = random.randint(1, 100)
        #         c.send(str(n).encode())
        # send back the string to client
        c.send(data)

    # connection closed
    c.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen(5)
    print("socket is listening")
    while True:
        c, addr = s.accept()
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])
        start_new_thread(threaded, (c,))

    s.close()
