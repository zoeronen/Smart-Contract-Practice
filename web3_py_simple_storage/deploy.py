from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

# Open SimpleStorage.sol for reading
with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# We add these two lines that freeCodeCamp forgot from the video!
print("Installing...")
install_solc("0.6.0")

# Solidity source code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# Get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# Get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# Connect to ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))  # 7545 for Ganache GUI
chain_id = 1337
my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
private_key = os.getenv(
    "PRIVATE_KEY"
)  # get private key from env! do not hard code here!

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)
print(nonce)

# 1. Build a treansaction
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)
print(transaction)

# 2. Sign a transaction
signed_txt = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# 3. Send a transaction
print("Deploying Contract!")
tx_hash = w3.eth.send_raw_transaction(signed_txt.rawTransaction)
# Wait for the transaction to be mined, and get the transaction receipt
print("Waiting for transaction to finish...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Done! Contract deployed to {tx_receipt.contractAddress}")

# Working with deployed contract:
# Contract Address (address=tx_receipt.contractAddress)
# Contract ABI (abi=abi)
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

## Call     -> Simulate making the call and getting a return value
## Transact -> Actually making a state change to the blockchain

# Initial value of favorite number:
print(simple_storage.functions.retrieve().call())
print("Updating Contract!")
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,
    }
)
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
print("Updating stored Value...")
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print("Updated!")
print(simple_storage.functions.retrieve().call())
