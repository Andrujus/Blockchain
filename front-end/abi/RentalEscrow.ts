
export const RentalEscrowABI = [
  "function rentProperty(address owner, address inspector) external payable returns (uint256 orderId)",
  "function confirmRental(uint256 orderId) external",
  "function cancelRental(uint256 orderId) external",
  "function inspectProperty(uint256 orderId, bool passed) external",
  "function releaseDeposit(uint256 orderId) external",
  "function getOrder(uint256 orderId) external view returns (address renter, address owner, address inspector, uint256 depositWei, uint8 status, bool inspectionPassed, uint256 createdAt, uint256 approvedAt, uint256 inspectedAt, uint256 closedAt)",
  "function orderCount() external view returns (uint256)",
  "event OrderCreated(uint256 indexed orderId, address indexed renter, address indexed owner, address inspector, uint256 depositWei)",
  "event OrderApproved(uint256 indexed orderId, address indexed owner)",
  "event OrderInspected(uint256 indexed orderId, address indexed inspector, bool passed)",
  "event DepositReleased(uint256 indexed orderId, address to, uint256 amountWei)",
  "event OrderCancelled(uint256 indexed orderId, address indexed renter, uint256 refundWei)"
];
