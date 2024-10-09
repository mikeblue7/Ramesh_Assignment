import time
import random
from web3 import Web3
import threading

# ERC-20 Token Contract Details (Sepolia Testnet)
ERC20_TOKEN_ADDRESS = "0x775712e67c9611b882E677E8E891DCC05848c4b1" 
ERC20_ABI = [
    # Add the complete ERC-20 ABI here
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    # ... other ABI elements (transfer, etc.)
]

# --- Autonomous Agent Base Class ---
class AutonomousAgent:
    def __init__(self):
        self.inbox = []
        self.outbox = []
        self.message_handlers = {}
        self.behaviors = []

    def register_message_handler(self, message_type, handler):
        self.message_handlers[message_type] = handler

    def register_behavior(self, behavior):
        self.behaviors.append(behavior)

    def send_message(self, message):
        self.outbox.append(message)

    def receive_message(self, message):
        self.inbox.append(message)

    def process_messages(self):
        while self.inbox:
            message = self.inbox.pop(0)
            # You might need more sophisticated message type checking here
            if message in self.message_handlers: 
                self.message_handlers[message](message)

    def run_behaviors(self):
        for behavior in self.behaviors:
            behavior()

    def run(self):
        while True:
            self.process_messages()
            self.run_behaviors()
            time.sleep(1)  # Adjust sleep time as needed
# --- End of AutonomousAgent Class ---


# --- Concrete Agent Class ---
class ConcreteAgent(AutonomousAgent):
    def __init__(self, address, private_key, target_address, w3):
        super().__init__()
        self.address = address
        self.private_key = private_key
        self.target_address = target_address
        self.w3 = w3
        self.erc20_contract = self.w3.eth.contract(address=ERC20_TOKEN_ADDRESS, abi=ERC20_ABI)

        self.register_behavior(self.generate_random_message)
        self.register_behavior(self.check_token_balance)
        self.register_message_handler("hello", self.handle_hello_message) # Changed to string type
        self.register_message_handler("crypto", self.handle_crypto_message) # Changed to string type

    def generate_random_message(self):
        words = ["hello", "sun", "world", "space", "moon", "crypto", "sky", "ocean", "universe", "human"]
        message = f"{random.choice(words)} {random.choice(words)}"
        self.send_message(message)
        time.sleep(2)

    def handle_hello_message(self, message):
        if "hello" in message:
            print(f"Received hello message: {message}")

    def check_token_balance(self):
        balance = self.erc20_contract.functions.balanceOf(self.address).call()
        print(f"ERC-20 token balance for {self.address}: {balance}")
        time.sleep(10)

    def handle_crypto_message(self, message):
        if "crypto" in message:
            try:
                # Implement token transfer using web3.py
                nonce = self.w3.eth.getTransactionCount(self.address)
                tx = self.erc20_contract.functions.transfer(
                    self.target_address, 1
                ).buildTransaction({
                    'from': self.address,
                    'nonce': nonce,
                    'gas': 2000000,  # Estimate gas appropriately
                    'gasPrice': self.w3.toWei('50', 'gwei')
                })
                signed_tx = self.w3.eth.account.signTransaction(
                    tx, self.private_key)
                tx_hash = self.w3.eth.sendRawTransaction(
                    signed_tx.rawTransaction)
                print(
                    f"Token transfer transaction hash: {tx_hash.hex()}")
            except Exception as e:
                print(f"Error transferring tokens: {e}")
# --- End of ConcreteAgent Class ---


# --- Agent Initialization and Connection ---
if __name__ == "__main__":
    # Web3 Connection using your Tenderly fork
    w3 = Web3(Web3.HTTPProvider('https://virtual.sepolia.rpc.tenderly.co/433c78cf-69be-40fa-bf92-71c781aa5fee'))

    # Replace with your actual addresses and private keys from your Tenderly fork
    agent1 = ConcreteAgent('[AGENT1_ADDRESS]', '[AGENT1_PRIVATE_KEY]', '[AGENT2_ADDRESS]', w3)
    agent2 = ConcreteAgent('[AGENT2_ADDRESS]', '[AGENT2_PRIVATE_KEY]', '[AGENT1_ADDRESS]', w3)

    # Connect the agents
    agent1.outbox = agent2.inbox
    agent2.outbox = agent1.inbox

    # --- Running Agents in Separate Threads ---
    def run_agent(agent):
        agent.run()

    thread1 = threading.Thread(target=run_agent, args=(agent1,))
    thread2 = threading.Thread(target=run_agent, args=(agent2,))

    thread1.start()
    thread2.start()