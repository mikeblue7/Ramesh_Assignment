import unittest
from web3 import Web3
# ... (Your AutonomousAgent and ConcreteAgent classes)

class AgentTestCase(unittest.TestCase):
    def setUp(self):
        """Setup method to run before each test."""
        self.w3 = Web3(Web3.HTTPProvider('https://virtual.sepolia.rpc.tenderly.co/433c78cf-69be-40fa-bf92-71c781aa5fee'))
    
        self.agent1 = ConcreteAgent('[TEST_AGENT1_ADDRESS]', '[TEST_AGENT1_PRIVATE_KEY]', '[TEST_AGENT2_ADDRESS]', self.w3) 
        self.agent2 = ConcreteAgent('[TEST_AGENT2_ADDRESS]', '[TEST_AGENT2_PRIVATE_KEY]', '[TEST_AGENT1_ADDRESS]', self.w3)
        self.agent1.outbox = self.agent2.inbox
        self.agent2.outbox = self.agent1.inbox

    def test_hello_message_handling(self):
        """Test if "hello" messages are handled correctly."""
        self.agent1.send_message("hello world")
        self.agent1.process_messages()  

    def test_crypto_message_handling(self):
        """Test if "crypto" messages trigger a token transfer."""
        initial_balance_agent2 = self.agent2.erc20_contract.functions.balanceOf(self.agent2.address).call()
        self.agent1.send_message("crypto universe")
        self.agent1.process_messages()
        # Wait for the transfer to potentially complete (might need a short delay)
        time.sleep(5)  
        final_balance_agent2 = self.agent2.erc20_contract.functions.balanceOf(self.agent2.address).call()
        # Add assertion to check if agent2's balance increased by 1 token
        self.assertEqual(final_balance_agent2, initial_balance_agent2 + 1)

    def test_random_message_generation(self):
        """Test if random messages are generated."""
        initial_outbox_length = len(self.agent1.outbox)
        self.agent1.generate_random_message()
        self.assertGreater(len(self.agent1.outbox), initial_outbox_length)

    def test_token_balance_check(self):
        """Test if the token balance is retrieved correctly."""
        balance = self.agent1.check_token_balance()
        # Add assertion to check if the balance is an integer or a valid balance value

if __name__ == '__main__':
    unittest.main()