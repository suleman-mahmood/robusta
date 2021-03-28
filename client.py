'''
This module defines the behaviour of a client in your Chat Application
'''
import sys
import getopt
import socket
import random
from threading import Thread
import os
import util


'''
Write your code inside this class.
In the start() function, you will read user-input and act accordingly.
receive_handler() function is running another thread and you have to listen
for incoming messages in this function.
'''

# blochain = [
#     block1,
#     block2,
#     ...,
# ]

# block = {
#     head: "12312312",
#     body: "transaction data"
# }

# key = ("9482934823", "5") # 0 - 10

# new_body = ""

# for b in body:
#     new_body.append(ord(b) - 5)


class Client:
    '''
    This is the main Client Class.
    '''

    def __init__(self, username, dest, port, window_size):
        self.server_addr = dest
        self.server_port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(None)
        self.sock.bind(('', random.randint(10000, 40000)))
        self.name = username
        self.window = window_size

    def start(self):
        '''
        Main Loop is here
        Start by sending the server a JOIN message.
        Waits for userinput and then process it
        '''

    def receive_handler(self):
        '''
        Waits for a message from server and process it accordingly
        '''


# Do not change this part of code
if __name__ == "__main__":

    PORT = 15000
    DEST = "localhost"
    USER_NAME = input("Enter username: ")
    WINDOW_SIZE = 3

    S = Client(USER_NAME, DEST, PORT, WINDOW_SIZE)
    try:
        # Start receiving Messages
        T = Thread(target=S.receive_handler)
        T.daemon = True
        T.start()
        # Start Client
        S.start()
    except (KeyboardInterrupt, SystemExit):
        sys.exit()
