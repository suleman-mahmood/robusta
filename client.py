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
        self.server_dest = ("localhost", port)

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

        encoded = ""
        # b = []
        for char in self.name:
            # b.append(ord(char))
            encoded = encoded + str(ord(char))
        # word = "".join([chr(value) for value in b])
        # for i in range(len(b)):
        encoded = int(encoded)
        self.encoded_username = encoded
        found_user = False
        file = open("keys.txt")
        data_file = file.readlines()

        for line in data_file:
            s_line = line.strip()
            # s_line = line
            s_line = s_line.split(' ')
            # format.append(s_line)
            if s_line[0] == str(encoded):
                # if encoded in self.main.keys():
                print('welcome Back', self.name,
                      '!\nWhat do you wanna do today?')
                self.role = s_line[2]
                self.my_key = s_line[1]
                found_user = True
                break
        file.close()
        if found_user is False:
            temp = input(
                "Are you a user or a bank?\nPress 1 for bank, and\n2 for user\n")
            if temp == '1':
                self.role = "bank"
            elif temp == '2':
                self.role = "user"
            self.my_key = random.randrange(0, 500)
            file = open('keys.txt', 'a')
            file.write('\n')
            write_to = str(encoded) + " " + str(self.my_key) + " " + self.role
            # print(write_to)
            file.write(write_to)
            # Close the file
            file.close()

            # print(encoded, self.name)
            # self.main[encoded] = {}
        # Compute ASCII from username
        # check if key exists in a file
        # if key doesnt exist then add a random key into file

        # Request ledger from miner
        self.sock.sendto("join".encode("utf-8"), self.server_dest)

        if self.role == "user":

            # Prompting the user for a list of available commands
            print("vfa: View Financial History")
            print(
                "vlr: Check whether your pending loans requests were accepted or rejected")
            print("clr: Create a new loan request")
            print("help: Display these list of commands again")
            print("quit: Exit out of the application")

            while True:
                # input from command line
                user_input = input()

                data_splices = user_input.split(" ")
                msg_type = data_splices[0]

                # View financial history
                if msg_type == "vfa":

                    # Read your records from the ledger and display them
                    for block in self.ledger:

                        if block["header"] == self.encoded_username and block["msg_type"] == "financial_history":
                            msg_body = block["body"]

                            # Decrypt the msg
                            decrypted_body = self.decrypt_string(
                                msg_body, self.my_key)

                            print(decrypted_body)

                # View pending request
                elif msg_type == "vlr":

                    # Read pending requests from ledger and then display their statuses
                    for block in self.ledger:

                        if block["header"] == self.encoded_username and block["msg_type"] == "approve":
                            msg_body = block["body"]

                            # Decrypt the msg
                            decrypted_body = self.decrypt_string(
                                msg_body, self.my_key)

                            print(decrypted_body)

                # Create loan request
                elif msg_type == "clr":

                    # Prompt the user for information about the loan request
                    bank_name = input(
                        "Enter the bank name from which you want to request the loan from:")
                    loan_amount = input("Enter the loan amount:")

                    # Compute the Ascii of the bank
                    encoded_bank_name = ""

                    for char in bank_name:
                        encoded_bank_name += str(ord(char))

                    encoded_bank_name = int(encoded_bank_name)

                    # Create the body of the msg
                    new_body = str(self.encoded_username) + " " + loan_amount

                    # Decrypt the msg
                    encrypted_body = self.encrypt_string(new_body, self.my_key)

                    # Create a block for loan request
                    new_block = {
                        "header": encoded_bank_name,
                        "msg_type": "loan_request",
                        "body": encrypted_body,
                    }

                    new_block = json.dumps(new_block)

                    # Send the encrypted block to miner so that he can create a block for loan request
                    self.sock.sendto(new_block.encode(
                        "utf-8"), self.server_dest)

                elif msg_type == "quit":

                    # Quit the user
                    print("Quitting...")
                    break

        elif self.role == "bank":

            # Prompting the bank for a list of available commands
            print("afh: Add a financial transaction for a user")
            print("vlr: View all loan requests")
            print("alr: Approve loan requests")
            print("help: Display these list of commands again")
            print("quit: Exit out of the application")

            while True:
                # input from command line
                user_input = input()

                data_splices = user_input.split(" ")
                msg_type = data_splices[0]

                # Add Financial History
                if msg_type == "afh":

                    # Sends the encrypted block to miner so that he can add it to the ledger
                    print("Enter the transaction in the following format:")
                    print("<Sender Name> <Receiver Name> <Amount transferred>")

                    transaction_body = input()
                    data_splices = transaction_body.split(' ')

                    # Compute the Ascii for sender
                    encoded_sender_name = ""

                    for char in data_splices[0]:
                        encoded_sender_name += str(ord(char))

                    encoded_sender_name = int(encoded_sender_name)

                    # Compute the Ascii for receiver
                    encoded_receiver_name = ""

                    for char in data_splices[1]:
                        encoded_receiver_name += str(ord(char))

                    encoded_receiver_name = int(encoded_receiver_name)

                    # Create the body of the msg for sender
                    new_body_sender = "Paid $" + \
                        data_splices[2] + " to " + data_splices[1]

                    # Create the body of the msg for reciever
                    new_body_receiver = "Received $" + \
                        data_splices[2] + " from " + data_splices[0]

                    # Find the keys for sender and reciever
                    sender_key = -1
                    receiver_key = -1

                    file = open("keys.txt")
                    data_file = file.readlines()

                    for line in data_file:
                        s_line = line.strip()
                        s_line = s_line.split(' ')

                        if s_line[0] == str(encoded_sender_name):
                            sender_key = s_line[1]

                        elif s_line[0] == str(encoded_receiver_name):
                            receiver_key = s_line[1]

                    # encrypt the msg
                    encrypted_sender = self.encrypt_string(
                        new_body_sender, sender_key)
                    encrypted_receiver = self.encrypt_string(
                        new_body_receiver, receiver_key)

                    # Create a block for sender
                    new_block_sender = {
                        "header": encoded_sender_name,
                        "msg_type": "financial_history",
                        "body": encrypted_sender,
                    }

                    # Create a block for receiver
                    new_block_receiver = {
                        "header": encoded_receiver_name,
                        "msg_type": "financial_history",
                        "body": encrypted_receiver,
                    }

                    new_block_sender = json.dumps(new_block_sender)
                    new_block_receiver = json.dumps(new_block_receiver)

                    # Send the encrypted block to miner so that he can create a block for transaction
                    self.sock.sendto(new_block_sender.encode(
                        "utf-8"), self.server_dest)
                    self.sock.sendto(new_block_receiver.encode(
                        "utf-8"), self.server_dest)

                # View Loan Requests
                elif msg_type == "vlr":

                    # Checks the ledger for the entries corresponding to the bank and shows all requests
                    for block in self.ledger:

                        if block["header"] == self.encoded_username and block["msg_type"] == "loan_request":
                            msg_body = block["body"]

                            # Decrypt the msg
                            decrypted_body = self.decrypt_string(
                                msg_body, self.my_key)

                            print(decrypted_body)

                # Approve loan request
                elif msg_type == "alr":

                    # Sends an approve block to a miner

                    # Checks the ledger for the entries corresponding to the bank and shows all requests
                    for block in self.ledger:

                        if block["header"] == self.encoded_username and block["msg_type"] == "loan_request":
                            msg_body = block["body"]

                            # Decrypt the msg
                            decrypted_body = self.decrypt_string(
                                msg_body, self.my_key)
                            encoded_username = decrypted_body[0]
                            loan_amount = decrypted_body[1]

                            # Find the key for requestee
                            key = -1

                            file = open("keys.txt")
                            data_file = file.readlines()

                            for line in data_file:
                                s_line = line.strip()
                                s_line = s_line.split(' ')

                                if s_line[0] == str(encoded_username):
                                    key = s_line[1]
                                    break

                            # Show all the financial history for this user
                            # Read records from the ledger and display them
                            for block in self.ledger:

                                if block["header"] == encoded_username and block["msg_type"] == "financial_history":
                                    msg_body = block["body"]

                                    # Decrypt the msg
                                    decrypted_body = self.decrypt_string(
                                        msg_body, key)

                                    print(decrypted_body)

                            is_approve = input(
                                "Do you wish to approve this loan request? (y/n):")

                            status = "Approved"

                            if is_approve == "n":
                                status = "Rejected"

                            encrypted_body = self.encrypt_string(status, key)

                            # Create a block for approving
                            new_block = {
                                "header": encoded_username,
                                "msg_type": "approve",
                                "body": encrypted_body,
                            }

                            new_block = json.dumps(new_block)

                            # Send the encrypted block to miner so that he can create a block for loan request
                            self.sock.sendto(new_block.encode(
                                "utf-8"), self.server_dest)

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

    # Encrypts the string using key
    def encrypt_string(self, msg, key):

        encrypted_string = ""

        key = int(key)

        for char in msg:
            encrypted_string += chr(ord(char) + key)

        return encrypted_string

    # Decrytps the string using the same key
    def decrypt_string(self, msg, key):

        decrypted_string = ""

        key = int(key)

        for char in msg:
            decrypted_string += chr(ord(char) - key)

        return decrypted_string


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
