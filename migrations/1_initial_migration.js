const MyContract = artifacts.require("MedicalSupplyChain");

module.exports = function(deployer) {
  deployer.deploy(MyContract);
};
