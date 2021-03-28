'''
This module defines the behaviour of server in your Chat Application
'''
import sys
import getopt
import socket
import util

# Incoming blocks
# Add the incoming blocks to the ledger


class Server:
    '''
    This is the main Server Class. You will to write Server code inside this class.
    '''

    def __init__(self, dest, port, window):
        self.server_addr = dest
        self.server_port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(None)
        self.sock.bind((self.server_addr, self.server_port))
        self.window = window

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
            if address not in self.peers_addresses:
                self.peers_addresses.append(address)

            # Add the block to the ledger
            self.ledger.append(incoming_block)

            # Broadcast the updated ledger to the whole network
            for peer_address in self.peers_addresses:
                self.sock.sendto(self.ledger.encode("utf-8"), peer_address)


# Do not change this part of code


if __name__ == "__main__":
    def helper():
        '''
        This function is just for the sake of our module completion
        '''
        print("Server")
        print("-p PORT | --port=PORT The server port, defaults to 15000")
        print("-a ADDRESS | --address=ADDRESS The server ip or hostname, defaults to localhost")
        print("-w WINDOW | --window=WINDOW The window size, default is 3")
        print("-h | --help Print this help")

    try:
        OPTS, ARGS = getopt.getopt(sys.argv[1:],
                                   "p:a:w", ["port=", "address=", "window="])
    except getopt.GetoptError:
        helper()
        exit()

    PORT = 15000
    DEST = "localhost"
    WINDOW = 3

    for o, a in OPTS:
        if o in ("-p", "--port="):
            PORT = int(a)
        elif o in ("-a", "--address="):
            DEST = a
        elif o in ("-w", "--window="):
            WINDOW = a

    SERVER = Server(DEST, PORT, WINDOW)
    try:
        SERVER.start()
    except (KeyboardInterrupt, SystemExit):
        exit()
