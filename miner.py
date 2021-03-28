'''
This module defines the behaviour of server in your Chat Application
'''
import sys
import json
import getopt
import socket
import util

# Incoming blocks
# Add the incoming blocks to the ledger


class Server:
    '''
    This is the main Server Class. You will to write Server code inside this class.
    '''

    def __init__(self, dest, port):
        self.server_addr = dest
        self.server_port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(None)
        self.sock.bind((self.server_addr, self.server_port))

        self.ledger = []
        self.peers_addresses = []

    def start(self):
        '''
        Main loop.
        continue receiving messages from Clients and processing it
        '''

        # handling incoming messages from clients or other miners
        while True:

            incoming_block, address = self.sock.recvfrom(4096)
            incoming_block = incoming_block.decode("utf-8")

            # Maintains the broadcasting list
            if incoming_block == "join":
                self.peers_addresses.append(address)

                ledger_to_send = json.dumps(self.ledger)
                self.sock.sendto(ledger_to_send.encode("utf-8"), address)
                continue

            incoming_block = json.loads(incoming_block)

            # Add the block to the ledger
            self.ledger.append(incoming_block)

            print(self.ledger)

            ledger_to_send = json.dumps(self.ledger)

            # Broadcast the updated ledger to the whole network
            for peer_address in self.peers_addresses:
                self.sock.sendto(ledger_to_send.encode("utf-8"), peer_address)


# Do not change this part of code


if __name__ == "__main__":

    PORT = 15000
    DEST = "localhost"

    SERVER = Server(DEST, PORT)
    try:
        SERVER.start()
    except (KeyboardInterrupt, SystemExit):
        exit()
