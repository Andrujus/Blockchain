// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.26;

// This will only compile via IR
contract Order {
    // The keyword "public" makes variables
    // accessible from other contracts
    address public creator;
    address public seller;
    address public buyer;
    uint public price;
    bool public isCompleted;
    string public description;

    // Events allow clients to react to specific
    // contract changes you declare
    event OrderCreated(address indexed creator, address indexed seller, uint price, string description);
    event OrderCompleted(address indexed buyer, uint price);

    // Constructor code is only run when the contract
    // is created
    constructor(address _seller, uint _price, string memory _description) {
        creator = msg.sender;
        seller = _seller;
        price = _price;
        description = _description;
        isCompleted = false;
        emit OrderCreated(creator, seller, price, description);
    }

    // Allows the seller to complete the order
    // Can only be called by the seller
    function completeOrder() public payable {
        require(msg.sender == seller, "Only seller can complete the order");
        require(!isCompleted, "Order is already completed");
        require(msg.value == price, "Incorrect payment amount");

        isCompleted = true;
        buyer = msg.sender;
        emit OrderCompleted(buyer, price);
    }

    // Allows the buyer to retrieve the seller's address
    function getSeller() public view returns (address) {
        return seller;
    }

    // Allows anyone to check if the order is completed
    function checkOrderStatus() public view returns (bool) {
        return isCompleted;
    }

    // Allows anyone to retrieve the order description
    function getDescription() public view returns (string memory) {
        return description;
    }

    // Allows anyone to retrieve the order price
    function getPrice() public view returns (uint) {
        return price;
    }
}