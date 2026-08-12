// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title StockLedger
/// @notice An append-only journal for one personal stock.
/// @dev The contract deliberately knows nothing about agreement economics. It orders
///      versioned event envelopes, commits them to a hash chain, and emits their
///      payloads. Current state is reconstructed offchain by replaying the logs.
contract StockLedger {
    bytes32 public constant EVENT_HASH_DOMAIN = keccak256("personal-stock-ledger/event/v1");
    uint256 public constant MAX_BATCH_SIZE = 100;

    struct EventInput {
        bytes32 eventType;
        uint32 schemaVersion;
        uint64 effectiveAt;
        bytes payload;
    }

    string public stockName;
    address public controller;
    address public pendingController;
    uint256 public eventCount;
    bytes32 public head;

    event EventAppended(
        uint256 indexed sequence,
        bytes32 indexed eventType,
        uint32 indexed schemaVersion,
        uint64 effectiveAt,
        bytes32 previousHead,
        bytes32 eventHash,
        bytes payload
    );
    event ControllerTransferStarted(address indexed currentController, address indexed pendingController);
    event ControllerTransferred(address indexed previousController, address indexed newController);

    error NotController();
    error NotPendingController();
    error ZeroAddress();
    error EmptyStockName();
    error EmptyBatch();
    error BatchTooLarge();
    error InvalidEventType();
    error InvalidSchemaVersion();
    error InvalidEffectiveTime();
    error EmptyPayload();
    error UnexpectedEventCount(uint256 expected, uint256 actual);
    error UnexpectedHead(bytes32 expected, bytes32 actual);

    modifier onlyController() {
        _requireController();
        _;
    }

    constructor(string memory _stockName, address initialController) {
        if (bytes(_stockName).length == 0) revert EmptyStockName();
        if (initialController == address(0)) revert ZeroAddress();
        stockName = _stockName;
        controller = initialController;
        emit ControllerTransferred(address(0), initialController);
    }

    /// @notice Append one event, provided the caller's view of the journal is current.
    function append(uint256 expectedEventCount, bytes32 expectedHead, EventInput calldata input)
        external
        onlyController
        returns (bytes32 eventHash)
    {
        _requireCurrent(expectedEventCount, expectedHead);
        eventHash = _append(input);
    }

    /// @notice Atomically append a related group of events.
    function appendBatch(uint256 expectedEventCount, bytes32 expectedHead, EventInput[] calldata inputs)
        external
        onlyController
        returns (bytes32 newHead)
    {
        _requireCurrent(expectedEventCount, expectedHead);
        if (inputs.length == 0) revert EmptyBatch();
        if (inputs.length > MAX_BATCH_SIZE) revert BatchTooLarge();

        for (uint256 i = 0; i < inputs.length; ++i) {
            newHead = _append(inputs[i]);
        }
    }

    /// @notice Calculate the hash an event would receive at a specified position.
    function previewEventHash(uint256 sequence, bytes32 previousHead, EventInput calldata input)
        external
        view
        returns (bytes32)
    {
        return _eventHash(sequence, previousHead, input);
    }

    /// @notice Begin a two-step controller transfer.
    function transferController(address newController) external onlyController {
        if (newController == address(0)) revert ZeroAddress();
        pendingController = newController;
        emit ControllerTransferStarted(controller, newController);
    }

    /// @notice Accept control after the current controller nominates the caller.
    function acceptController() external {
        if (msg.sender != pendingController) revert NotPendingController();
        address previousController = controller;
        controller = msg.sender;
        pendingController = address(0);
        emit ControllerTransferred(previousController, msg.sender);
    }

    function _requireCurrent(uint256 expectedEventCount, bytes32 expectedHead) internal view {
        if (expectedEventCount != eventCount) {
            revert UnexpectedEventCount(expectedEventCount, eventCount);
        }
        if (expectedHead != head) revert UnexpectedHead(expectedHead, head);
    }

    function _requireController() internal view {
        if (msg.sender != controller) revert NotController();
    }

    function _append(EventInput calldata input) internal returns (bytes32 eventHash) {
        if (input.eventType == bytes32(0)) revert InvalidEventType();
        if (input.schemaVersion == 0) revert InvalidSchemaVersion();
        if (input.effectiveAt == 0) revert InvalidEffectiveTime();
        if (input.payload.length == 0) revert EmptyPayload();

        uint256 sequence = eventCount + 1;
        bytes32 previousHead = head;
        eventHash = _eventHash(sequence, previousHead, input);

        eventCount = sequence;
        head = eventHash;

        emit EventAppended(
            sequence, input.eventType, input.schemaVersion, input.effectiveAt, previousHead, eventHash, input.payload
        );
    }

    function _eventHash(uint256 sequence, bytes32 previousHead, EventInput calldata input)
        internal
        view
        returns (bytes32)
    {
        return keccak256(
            abi.encode(
                EVENT_HASH_DOMAIN,
                block.chainid,
                address(this),
                sequence,
                input.eventType,
                input.schemaVersion,
                input.effectiveAt,
                keccak256(input.payload),
                previousHead
            )
        );
    }
}
