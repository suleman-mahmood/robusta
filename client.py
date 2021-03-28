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
import json


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

# key = ("9482934823", "5") # 0 - 10

# new_body = ""

# for b in body:
#     new_body.append(ord(b) - 5)

# block = {
#     head: "12312312",
#     msg_type: "financial_history | loan_request | approve",
#     body: "history_data",
# }


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

        self.role = ""
        self.encoded_username = -1
        self.my_key = -1
        self.ledger = {}

    def start(self):
        '''
        Main Loop is here
        Start by sending the server a JOIN message.
        Waits for userinput and then process it
        '''

        # Prompting the user for a list of available commands
        print("vfa: View Financial History")
        print("vlr: Check whether your pending loans requests were accepted or rejected")
        print("clr: Create a new loan request")
        print("quit: Exit out of the application")

        encoded = ""
        b = []
        for char in self.name:
            b.append(ord(char))
            encoded = encoded + str(ord(char))
        # word = "".join([chr(value) for value in b])
        # for i in range(len(b)):
        encoded = int(encoded)
        self.encoded_username = encoded

        file = open("keys.txt")
        data_file = file.read()
        for line in data_file:
            s_line = line.strip()
            s_line = s_line.split(',')
            # format.append(s_line)
            if s_line[0] == encoded:
                # if encoded in self.main.keys():
                print('welcome Back', self.name,
                      '!\nWhat do you wanna do today?')
                self.role = s_line[2]
                self.my_key = s_line[1]
                break
            else:
                self.role = input(
                    "Are you a user or a bank?\nPress 1 for bank, and\n2 for user\n")
                self.my_key = random.randrange(0, 1000)
                print("hello")

                # print(encoded, self.name)
                # self.main[encoded] = {}
        # Compute ASCII from username
        # check if key exists in a file
        # if key doesnt exist then add a random key into file

        # Request ledger from miner

        if self.role == "user":

            while True:
                # input from command line
                user_input = input()

                data_splices = user_input.split(" ")
                msg_type = data_splices[0]

                # View financial history
                if msg_type = "VFA":

                    # Read your records from the ledger and display them
                    for block in self.ledger:

                        if block["header"] == self.encoded_username and block["msg_type"] == "financial_history":
                            msg_body = block["body"]
                            print(msg_body)

                # View pending request
                elif msg_type == "VLR":

                    # Read pending requests from ledger and then display their statuses
                    for block in self.ledger:

                        if block["header"] == self.encoded_username and block["msg_type"] == "approve":
                            msg_body = block["body"]
                            print(msg_body)

                # Create loan request
                elif msg_type == "CLR":

                    # Prompt the user for information about the loan request
                    bank_name = input(
                        "Enter the bank name from which you want to request the loan from:")
                    loan_amount = input("Enter the loan amount:")

                    msg_body

                    # Create a block from your key
                    # Send the encrypted block to miner so that he can create a block for loan request

                elif msg_type == "quit":

                    # Quit the user
                    print("Quitting...")
                    break

        elif self.role == "bank"

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
        while True:

            # Recieve the incoming ledger
            incoming_ledger, address = self.sock.recvfrom(4096)

            # Decode the ledger
            incoming_ledger = incoming_ledger.decode("utf-8")

            # Convert the ledger from string to list
            incoming_ledger = json.loads(incoming_ledger)

            # Update the ledger
            self.ledger = incoming_ledger


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
