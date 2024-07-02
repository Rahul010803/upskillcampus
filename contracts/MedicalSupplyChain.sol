// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MedicalSupplyChain {
    address public owner;
    
    struct Medicine {
        uint256 id;
        string name;
        uint256 quantity;
        address supplier;
        bool available;
    }
    
    mapping(uint256 => Medicine) public medicines;
    uint256 public nextMedicineId;
    
    event MedicinePurchased(uint256 indexed id, string name, uint256 quantity, address buyer);
    event MedicineRestocked(uint256 indexed id, string name, uint256 quantity, address supplier);
    
    constructor() {
        owner = msg.sender;
        nextMedicineId = 1;
    }
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }
    
    function purchaseMedicine(uint256 _id, uint256 _quantity) external payable {
        require(medicines[_id].available, "Medicine is not available");
        require(medicines[_id].quantity >= _quantity, "Not enough quantity available");
        uint256 totalCost = _quantity * 10000000000000000; // Assuming 1 medicine unit costs 0.01 ether
        require(msg.value >= totalCost, "Insufficient payment amount");
        
        payable(owner).transfer(totalCost); // Transfer payment to owner
        
        medicines[_id].quantity -= _quantity;
        
        emit MedicinePurchased(_id, medicines[_id].name, _quantity, msg.sender);
        
        if (medicines[_id].quantity < 10) {
            autoRestockMedicine(_id);
        }
    }
    
    function autoRestockMedicine(uint256 _id) internal {
        // Implement the logic to restock the medicine automatically
        // This can involve interacting with a supplier contract or external API
        // For demonstration purposes, we'll emit an event here
        emit MedicineRestocked(_id, medicines[_id].name, 100, address(0));
    }
    
    function addMedicine(string memory _name, uint256 _quantity, address _supplier) external onlyOwner {
        medicines[nextMedicineId] = Medicine(nextMedicineId, _name, _quantity, _supplier, true);
        nextMedicineId++;
    }
    
    function updateMedicineAvailability(uint256 _id, bool _available) external onlyOwner {
        medicines[_id].available = _available;
    }
}
