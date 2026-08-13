// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Test} from "forge-std/Test.sol";
import {StockLedger} from "../src/StockLedger.sol";

contract StockLedgerTest is Test {
    StockLedger ledger;
    address stranger = address(0xBEEF);
    address successor = address(0xCAFE);

    event EventAppended(
        uint256 indexed sequence,
        bytes32 indexed eventType,
        uint64 effectiveAt,
        bytes32 previousHead,
        bytes32 eventHash,
        bytes payload
    );

    function setUp() public {
        ledger = new StockLedger("Karthik Uppuluri Stock", address(this));
    }

    function test_InitialState() public view {
        assertEq(ledger.stockName(), "Karthik Uppuluri Stock");
        assertEq(ledger.controller(), address(this));
        assertEq(ledger.pendingController(), address(0));
        assertEq(ledger.eventCount(), 0);
        assertEq(ledger.head(), bytes32(0));
    }

    function test_AppendEmitsPayloadAndAdvancesHashChain() public {
        StockLedger.EventInput memory input = _input("FORMATION", 1_785_564_800, "{}");
        bytes32 expected = ledger.previewEventHash(1, bytes32(0), input);

        vm.expectEmit(true, true, true, true);
        emit EventAppended(1, bytes32("FORMATION"), 1_785_564_800, bytes32(0), expected, bytes("{}"));
        bytes32 actual = ledger.append(0, bytes32(0), input);

        assertEq(actual, expected);
        assertEq(ledger.eventCount(), 1);
        assertEq(ledger.head(), expected);
    }

    function test_BatchIsAtomicAndChainsEveryEvent() public {
        StockLedger.EventInput[] memory inputs = new StockLedger.EventInput[](2);
        inputs[0] = _input("FORMATION", 1_785_564_800, "{}");
        inputs[1] = _input("AGREEMENT_ADOPTION", 1_785_564_801, "{\"shareholder_id\":\"holder_000000\"}");

        bytes32 first = ledger.previewEventHash(1, bytes32(0), inputs[0]);
        bytes32 second = ledger.previewEventHash(2, first, inputs[1]);
        bytes32 returnedHead = ledger.appendBatch(0, bytes32(0), inputs);

        assertEq(returnedHead, second);
        assertEq(ledger.eventCount(), 2);
        assertEq(ledger.head(), second);
    }

    function test_StaleWriterCannotAppend() public {
        ledger.append(0, bytes32(0), _input("FORMATION", 1, "{}"));

        vm.expectRevert(abi.encodeWithSelector(StockLedger.UnexpectedEventCount.selector, 0, 1));
        ledger.append(0, bytes32(0), _input("SHARE_ISSUANCE", 2, "{}"));

        vm.expectRevert(abi.encodeWithSelector(StockLedger.UnexpectedHead.selector, bytes32(0), ledger.head()));
        ledger.append(1, bytes32(0), _input("SHARE_ISSUANCE", 2, "{}"));
    }

    function test_NonControllerCannotAppend() public {
        vm.prank(stranger);
        vm.expectRevert(StockLedger.NotController.selector);
        ledger.append(0, bytes32(0), _input("FORMATION", 1, "{}"));
    }

    function test_InvalidEnvelopeAndBatchAreRejected() public {
        vm.expectRevert(StockLedger.EmptyBatch.selector);
        ledger.appendBatch(0, bytes32(0), new StockLedger.EventInput[](0));

        vm.expectRevert(StockLedger.InvalidEventType.selector);
        ledger.append(0, bytes32(0), StockLedger.EventInput(bytes32(0), 1, "{}"));

        vm.expectRevert(StockLedger.InvalidEffectiveTime.selector);
        ledger.append(0, bytes32(0), StockLedger.EventInput(bytes32("FORMATION"), 0, "{}"));

        vm.expectRevert(StockLedger.EmptyPayload.selector);
        ledger.append(0, bytes32(0), StockLedger.EventInput(bytes32("FORMATION"), 1, ""));
    }

    function test_ControllerTransferRequiresAcceptance() public {
        ledger.transferController(successor);
        assertEq(ledger.controller(), address(this));
        assertEq(ledger.pendingController(), successor);

        vm.prank(stranger);
        vm.expectRevert(StockLedger.NotPendingController.selector);
        ledger.acceptController();

        vm.prank(successor);
        ledger.acceptController();
        assertEq(ledger.controller(), successor);
        assertEq(ledger.pendingController(), address(0));

        vm.expectRevert(StockLedger.NotController.selector);
        ledger.append(0, bytes32(0), _input("FORMATION", 1, "{}"));
    }

    function test_BatchSizeIsBounded() public {
        StockLedger.EventInput[] memory inputs = new StockLedger.EventInput[](101);
        vm.expectRevert(StockLedger.BatchTooLarge.selector);
        ledger.appendBatch(0, bytes32(0), inputs);
    }

    function _input(string memory eventType, uint64 effectiveAt, string memory payload)
        internal
        pure
        returns (StockLedger.EventInput memory)
    {
        return StockLedger.EventInput(_bytes32(eventType), effectiveAt, bytes(payload));
    }

    function _bytes32(string memory value) internal pure returns (bytes32 result) {
        bytes memory data = bytes(value);
        require(data.length <= 32);
        assembly {
            result := mload(add(data, 32))
        }
    }
}
