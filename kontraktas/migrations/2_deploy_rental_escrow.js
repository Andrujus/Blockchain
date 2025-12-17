const RentalEscrow = artifacts.require("RentalEscrow");

module.exports = function (deployer) {
  deployer.deploy(RentalEscrow);
};
