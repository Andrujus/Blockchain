// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title Nuomos Užtikrinimo Sistema (Rental Deposit Escrow)
/// @notice 3 šalys: renter (nuomininkas), owner (nuomotojas), inspector (nepriklausomas patikros atlikėjas)
/// @dev Sukurta pagal repo README aprašytą verslo modelį: depozitas laikomas kontrakte iki patikros sprendimo.
/// Modelis: PENDING -> APPROVED -> INSPECTED -> RELEASED  arba  PENDING -> CANCELLED
contract RentalEscrow {
    // ---- Types ----

    enum Status {
        NONE,       // nenaudojama (apsauga default reikšmėms)
        PENDING,    // renter sukūrė nuomą ir įnešė depozitą, laukia owner patvirtinimo
        APPROVED,   // owner patvirtino, laukia inspector patikros
        INSPECTED,  // inspector atliko patikrą (pass/fail)
        RELEASED,   // depozitas išmokėtas pagal patikrą
        CANCELLED   // atšaukta, depozitas grąžintas renter
    }

    struct RentalOrder {
        address payable renter;
        address payable owner;
        address inspector;

        uint256 depositWei;

        Status status;
        bool inspectionPassed;

        uint256 createdAt;
        uint256 approvedAt;
        uint256 inspectedAt;
        uint256 closedAt;
    }

    // ---- Storage ----

    uint256 public orderCount;
    mapping(uint256 => RentalOrder) private orders;

    // ---- Events (labai svarbu Etherscan logs + Front-End) ----

    event OrderCreated(
        uint256 indexed orderId,
        address indexed renter,
        address indexed owner,
        address inspector,
        uint256 depositWei
    );

    event OrderApproved(uint256 indexed orderId, address indexed owner);
    event OrderInspected(uint256 indexed orderId, address indexed inspector, bool passed);

    event DepositReleased(
        uint256 indexed orderId,
        address indexed to,
        uint256 amountWei
    );

    event OrderCancelled(uint256 indexed orderId, address indexed renter, uint256 refundWei);

    // ---- Errors (taupo gas ir aiškiau) ----

    error NotRenter();
    error NotOwner();
    error NotInspector();
    error InvalidState(Status expected, Status got);
    error InvalidAddress();
    error InvalidDeposit();
    error OrderNotFound();
    error TransferFailed();

    // ---- Reentrancy Guard (minimalus, be OpenZeppelin) ----

    uint256 private _locked = 1;
    modifier nonReentrant() {
        require(_locked == 1, "REENTRANCY");
        _locked = 2;
        _;
        _locked = 1;
    }

    // ---- Modifiers ----

    modifier orderExists(uint256 orderId) {
        if (orderId == 0 || orderId > orderCount) revert OrderNotFound();
        _;
    }

    modifier onlyRenter(uint256 orderId) {
        if (msg.sender != orders[orderId].renter) revert NotRenter();
        _;
    }

    modifier onlyOwner(uint256 orderId) {
        if (msg.sender != orders[orderId].owner) revert NotOwner();
        _;
    }

    modifier onlyInspector(uint256 orderId) {
        if (msg.sender != orders[orderId].inspector) revert NotInspector();
        _;
    }

    // ---- Read helpers ----

    function getOrder(uint256 orderId)
        external
        view
        orderExists(orderId)
        returns (RentalOrder memory)
    {
        return orders[orderId];
    }

    // ---- Core business functions ----

    /// @notice Renter sukuria nuomos užsakymą ir įneša depozitą
    /// @param owner Nuomotojo adresas
    /// @param inspector Nepriklausomo inspektoriaus adresas
    /// @return orderId Naujo užsakymo ID
    function rentProperty(address payable owner, address inspector)
        external
        payable
        returns (uint256 orderId)
    {
        if (owner == address(0) || inspector == address(0)) revert InvalidAddress();
        if (msg.value == 0) revert InvalidDeposit();
        if (owner == msg.sender) revert InvalidAddress(); // renter negali būti owner
        if (inspector == msg.sender) revert InvalidAddress(); // renter negali būti inspector

        orderId = ++orderCount;

        orders[orderId] = RentalOrder({
            renter: payable(msg.sender),
            owner: owner,
            inspector: inspector,
            depositWei: msg.value,
            status: Status.PENDING,
            inspectionPassed: false,
            createdAt: block.timestamp,
            approvedAt: 0,
            inspectedAt: 0,
            closedAt: 0
        });

        emit OrderCreated(orderId, msg.sender, owner, inspector, msg.value);
    }

    /// @notice Owner patvirtina nuomą
    function confirmRental(uint256 orderId)
        external
        orderExists(orderId)
        onlyOwner(orderId)
    {
        RentalOrder storage o = orders[orderId];
        if (o.status != Status.PENDING) revert InvalidState(Status.PENDING, o.status);

        o.status = Status.APPROVED;
        o.approvedAt = block.timestamp;

        emit OrderApproved(orderId, msg.sender);
    }

    /// @notice Renter gali atšaukti tik kol laukia owner patvirtinimo (PENDING)
    function cancelRental(uint256 orderId)
        external
        orderExists(orderId)
        onlyRenter(orderId)
        nonReentrant
    {
        RentalOrder storage o = orders[orderId];
        if (o.status != Status.PENDING) revert InvalidState(Status.PENDING, o.status);

        // effects
        o.status = Status.CANCELLED;
        o.closedAt = block.timestamp;

        uint256 refund = o.depositWei;
        o.depositWei = 0;

        // interaction
        (bool ok, ) = o.renter.call{value: refund}("");
        if (!ok) revert TransferFailed();

        emit OrderCancelled(orderId, msg.sender, refund);
    }

    /// @notice Inspector atlieka patikrą po to kai owner patvirtino (APPROVED)
    /// @param passed true jei būklė gera (depozitas atitenka owner), false jei bloga (grąžinamas renter)
    function inspectProperty(uint256 orderId, bool passed)
        external
        orderExists(orderId)
        onlyInspector(orderId)
    {
        RentalOrder storage o = orders[orderId];
        if (o.status != Status.APPROVED) revert InvalidState(Status.APPROVED, o.status);

        o.status = Status.INSPECTED;
        o.inspectionPassed = passed;
        o.inspectedAt = block.timestamp;

        emit OrderInspected(orderId, msg.sender, passed);
    }

    /// @notice Išmoka depozitą pagal patikros rezultatą (po INSPECTED)
    /// @dev Gali kviesti bet kas (patogu DApp’ui), bet išmoka tik pagal taisykles.
    function releaseDeposit(uint256 orderId)
        external
        orderExists(orderId)
        nonReentrant
    {
        RentalOrder storage o = orders[orderId];
        if (o.status != Status.INSPECTED) revert InvalidState(Status.INSPECTED, o.status);

        // decide receiver
        address payable to = o.inspectionPassed ? o.owner : o.renter;

        // effects
        o.status = Status.RELEASED;
        o.closedAt = block.timestamp;

        uint256 amount = o.depositWei;
        o.depositWei = 0;

        // interaction
        (bool ok, ) = to.call{value: amount}("");
        if (!ok) revert TransferFailed();

        emit DepositReleased(orderId, to, amount);
    }
}
