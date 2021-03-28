# Robusta

Robusta is the solution to help financial institutions qualify borrowers for loan and credit.

## Installation

There is no installation required for the app. However, make sure that python3 is correctly installed and updated on your machine so that the app functins correctly without any issues.

## Usage

Use the following command line argument to start the application

Windows:
```bash
py miner.py
py client.py
```
Linux/MacOs:
```bash
python3 miner.py
python3 client.py
```

Run these commands on two separate terminals.

## Description

The miner command will run the miner program which will recieve blocks from all the clients and add the block to the end of the blockchain. 
It maintains and records the ledger which is broadcasted to all the nodes in the network (other miners or clients) once a new block is added to the blockchain.

There are two enttites for clients:
1- Bank 
2- User

The Bank is a financial institution which will create transactions from the app and these transactiosn will be added to the blockchain.
However, the bank uses the public key of the clients to encrypt their transaction and then it is requested to be added on the blockchain.
This enforces privacy as only the clients possssing the private key can access their transaction information created by the banks.
The banks also don't have any access to the financial history of their own or other clients enabling data privacy.

The users are the normal audience for the app. They will login and request any loan applications from the banks of their choice.
Upon requesting a loan, the clients aggree to share their financial history with the banks so that they can evaluate them based on their history.
The clients also have the ability to see their own financial history through the app which is only accessible and available to them, as all their data 
is encrypted on the blockchain
