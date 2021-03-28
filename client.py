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

block = {
    head: "12312312",
    type_of_msg: "financial_history | loan_request | approve",
    body: "history_data",
}


class Client:
    '''
    This is the main Client Class.
    '''

    def __init__(self, username, dest, port):
        self.server_addr = dest
        self.server_port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(None)
        self.sock.bind(('', random.randint(10000, 40000)))
        self.name = username

        # Ledger variable

    def start(self):
        '''
        Main Loop is here
        Start by sending the server a JOIN message.
        Waits for userinput and then process it
        '''

        # Compute ASCII from username
        # check if key exists in a file
        # if key doesnt exist then add a random key into file

        # Update ledger from miner

        #  if customer

        while True:
            # input from command line

            # View financial history
            # Read your records from the ledger and display them

            # View pending request
            # Read pending requests from ledger and then display their statuses

            # Create loan request
            # Asks the miner to create a block for loan request

            ####

            # else bank

            # Add Financial History
            # Sends the encrypted block to miner so that he can add it to the ledger

            # View Loan Requests
            # Checks the ledger for the entries corresponding to the bank and shows all requests

            # Approve loan request
            # Sends an approve block to a miner

    def receive_handler(self):
        '''
        Waits for a message from server and process it accordingly
        '''

        # The miner sends an updated ledger everytime it changes


# Do not change this part of code
if __name__ == "__main__":

    PORT = 15000
    DEST = "localhost"
    USER_NAME = input("Enter username: ")

    # Also input the type of user (bank/customer)

    S = Client(USER_NAME, DEST, PORT)
    try:
        # Start receiving Messages
        T = Thread(target=S.receive_handler)
        T.daemon = True
        T.start()
        # Start Client
        S.start()
    except (KeyboardInterrupt, SystemExit):
        sys.exit()
