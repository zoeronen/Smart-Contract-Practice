from brownie import accounts, config, SimpleStorage


def read_contract():
    ## Get first deployed contract
    # simple_storage = SimpleStorage[0]
    ## Get last deployed contract
    simple_storage = SimpleStorage[-1]
    print(simple_storage.retrieve())


def main():
    read_contract()
