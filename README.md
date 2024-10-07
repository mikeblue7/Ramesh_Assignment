# Autonomous Agents with Web3 and ERC-20 Integration

This project implements a framework of autonomous agents in Python designed to interact with the Ethereum blockchain through the Web3 library. The agents are capable of generating random messages, checking ERC-20 token balances, and executing cryptocurrency transfers. This setup is intended for educational purposes and experimentation with decentralized applications (dApps).

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)

## Features

- **Autonomous Agents**: Two agents communicate through an inbox and outbox system.
- **Random Message Generation**: Agents send random messages to each other at regular intervals.
- **Message Handling**: Each agent can handle specific types of messages, allowing for tailored responses.
- **ERC-20 Token Interaction**: Agents can check balances and perform transfers of ERC-20 tokens.
- **Multithreading**: Agents operate their behaviors and message consumption in separate threads for concurrent execution.

## Requirements

- Python 3.x
- `web3.py` library
- `python-dotenv` library
- Access to an Ethereum node (e.g., Infura)
- ERC-20 token contract address
- Sender and receiver Ethereum addresses
- Private key for the sender address

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/<your-username>/Olas-Dev.git
   cd Olas-Dev
   ```

2. **Install Dependencies**:
   pip install web3 python-dotenv

3. **Set Up Environment Variables**:
   INFURA_RPC_URL=<your-infura-url>
   token_contract=<your-erc20-token-contract-address>
   sender_address=<your-sender-address>
   receiver_address=<your-receiver-address>
   private_key=<your-private-key>

## Usage

**Run the program**
python main.py
