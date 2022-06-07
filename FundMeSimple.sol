// SPDX-License-Identifier: LGPL-2.0-or-higher

// Smart contract that lets anyone deposit ETH into the contract
// SIMPLIFIED VERSION, NO ONE CAN WITHDRAW THE FUNDS
pragma solidity ^0.6.0;

// Get the latest ETH/USD price from chainlink price feed
import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

contract FundMe {

    mapping(address => uint256) public addressToAmountFunded;

    function fund() public payable {
        addressToAmountFunded[msg.sender] += msg.value;
    }
}

