import os
from dotenv import load_dotenv
import time
import random
import threading
from web3 import Web3
from eth_account import Account
load_dotenv()
class AutonomousAgent:
    def __init__(self, name, inbox=None, outbox=None):
        self.name = name
        self.inbox = inbox if inbox else []
        self.outbox = outbox if outbox else []
        self.handlers = {}
        self.behaviors = []

    def register_handler(self, message_type, handler):
        self.handlers[message_type] = handler

    def register_behavior(self, behavior):
        self.behaviors.append(behavior)

    def consume_messages(self):
        while True:
            if self.inbox:
                message = self.inbox.pop(0)
                for message_type, handler in self.handlers.items():
                    if message_type in message:
                        handler(message)
            time.sleep(1)  # Avoid constant polling

    def run_behaviors(self):
        while True:
            for behavior in self.behaviors:
                behavior()
            time.sleep(1)  # Run behaviors at regular intervals

    def send_message(self, message):
        self.outbox.append(message)

    def start(self):
        threading.Thread(target=self.consume_messages, daemon=True).start()
        threading.Thread(target=self.run_behaviors, daemon=True).start()

# Concrete instance implementation
def random_message_generator(agent):
    words = ["hello", "sun", "world", "space", "moon", "crypto", "sky", "ocean", "universe", "human"]
    def generate():
        message = random.choice(words) + " " + random.choice(words)
        agent.send_message(message)
    
    return generate

def hello_handler(message):
    if "hello" in message:
        print(f"Hello message received: {message}")

def erc20_balance_checker(agent, web3, token_contract, address,message):
    #def check_balance():
    if "token" in message:
        try:
            balance = token_contract.functions.balanceOf(address).call()
            print(f"ERC-20 Balance: {balance}")
            
        except Exception as e:
            print(f"Error checking balance: {e}")

def crypto_transfer_handler(web3, token_contract, sender, receiver, amount, private_key,message):
    #def transfer(message):
        
        if "crypto" in message:
            nonce = web3.eth.get_transaction_count(sender)
            gas_price=web3.eth.gas_price
            print(f"gas price:{gas_price}")
            txn = token_contract.functions.transfer(receiver, amount).build_transaction({
                'chainId': 11155111,
                'gas': 2000000,
                'gasPrice': gas_price,
                'nonce': nonce
            })
            signed_txn = web3.eth.account.sign_transaction(txn, private_key)
            txn_hash =web3.eth.send_raw_transaction(signed_txn.raw_transaction)
            #print(f"Transaction hash:{txn_hash}")
            
            print(f"Transaction hash: {web3.to_hex(txn_hash)}")
 
            
    

# Setup web3.py for Tenderly fork
def setup_web3():
    #infura_rpc_url = "https://sepolia.infura.io/v3/c4809537201441b1af9b6dd2c42da900"
    infura_rpc_url=os.getenv('INFURA_RPC_URL')
    web3 = Web3(Web3.HTTPProvider(infura_rpc_url))
    assert web3.is_connected(), "Failed to connect to the Ethereum network"

    return web3

# ERC-20 contract ABI (minimal for balance and transfer)
erc20_abi = [
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "spender",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "approve",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "symbol",
				"type": "string"
			}
		],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "spender",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "allowance",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "needed",
				"type": "uint256"
			}
		],
		"name": "ERC20InsufficientAllowance",
		"type": "error"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "sender",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "balance",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "needed",
				"type": "uint256"
			}
		],
		"name": "ERC20InsufficientBalance",
		"type": "error"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "approver",
				"type": "address"
			}
		],
		"name": "ERC20InvalidApprover",
		"type": "error"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "receiver",
				"type": "address"
			}
		],
		"name": "ERC20InvalidReceiver",
		"type": "error"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "sender",
				"type": "address"
			}
		],
		"name": "ERC20InvalidSender",
		"type": "error"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "spender",
				"type": "address"
			}
		],
		"name": "ERC20InvalidSpender",
		"type": "error"
	},
	{
		"anonymous": "false",
		"inputs": [
			{
				"indexed": "true",
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"indexed": "true",
				"internalType": "address",
				"name": "spender",
				"type": "address"
			},
			{
				"indexed": "false",
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "Approval",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "transfer",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"anonymous": "false",
		"inputs": [
			{
				"indexed": "true",
				"internalType": "address",
				"name": "from",
				"type": "address"
			},
			{
				"indexed": "true",
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"indexed": "false",
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "Transfer",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "from",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "transferFrom",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "spender",
				"type": "address"
			}
		],
		"name": "allowance",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "account",
				"type": "address"
			}
		],
		"name": "balanceOf",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "decimals",
		"outputs": [
			{
				"internalType": "uint8",
				"name": "",
				"type": "uint8"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "name",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "symbol",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "totalSupply",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]

if __name__ == "__main__":
    web3 = setup_web3()
    
    # Initialize agents
    agent1 = AutonomousAgent("Agent1")
    agent2 = AutonomousAgent("Agent2", inbox=agent1.outbox, outbox=agent1.inbox)
    
    # ERC-20 token contract setup
    token_contract = web3.eth.contract(address=os.getenv('token_contract'), abi=erc20_abi)
    sender_address = os.getenv('sender_address')
    receiver_address = os.getenv('receiver_address')
    private_key = os.getenv('private_key')
    amount=1000000000000000000
    
    # Register behaviors
    agent1.register_behavior(random_message_generator(agent1))
   

    # Register handlers
    agent1.register_handler("hello", hello_handler)
    #agent2.register_handler("crypto", crypto_transfer_handler(web3, token_contract, sender_address, receiver_address, 1, private_key,"crypto"))
    agent2.register_handler("crypto", lambda msg: crypto_transfer_handler(web3, token_contract, sender_address, receiver_address, amount, private_key, msg))
    
    # Start both agents
    agent1.start()
    agent2.start()

    # Run the agents for testing
    time.sleep(5)




    # Input loop to send messages
    try:
        while True:
            user_input = input("Enter a message to send (type 'exit' to stop): ")

            if user_input.lower() == 'exit':
                break  # Exit the loop
            if user_input.lower() == 'hello':
                hello_handler(user_input)  # Call hello_handler directly
            if user_input.lower() == 'crypto':
                crypto_transfer_handler(web3, token_contract, sender_address, receiver_address, amount, private_key,user_input)  # Call hello_handler directly
            if user_input.lower()=='token':
                erc20_balance_checker(agent2, web3, token_contract, sender_address,user_input)

            agent1.send_message(user_input)  # Send the user input as a message
    except KeyboardInterrupt:
        print("Exiting...")

    # Run the agents for a specified duration
    time.sleep(30)
 
