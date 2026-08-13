// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Script, console} from "forge-std/Script.sol";
import {StockLedger} from "../src/StockLedger.sol";

/// @notice Appends a batch compiled and validated by ledger_events.py.
contract Append is Script {
    function run() external {
        address ledgerAddress = vm.envAddress("LEDGER_ADDRESS");
        string memory batchPath = vm.envString("COMPILED_BATCH_PATH");
        string memory json = vm.readFile(batchPath);

        require(vm.parseJsonUint(json, ".chain_id") == block.chainid, "batch targets another chain");
        require(vm.parseJsonAddress(json, ".stock_contract") == ledgerAddress, "batch targets another ledger");

        uint256 expectedCount = vm.parseJsonUint(json, ".expected_event_count");
        bytes32 expectedHead = vm.parseJsonBytes32(json, ".expected_head");
        uint256 length = vm.parseJsonUint(json, ".event_count");
        StockLedger.EventInput[] memory inputs = new StockLedger.EventInput[](length);

        for (uint256 i = 0; i < length; ++i) {
            string memory base = string.concat(".events[", vm.toString(i), "]");
            uint256 effectiveAt = vm.parseJsonUint(json, string.concat(base, ".effective_at"));
            require(effectiveAt <= type(uint64).max, "effective time overflow");

            inputs[i] = StockLedger.EventInput({
                eventType: vm.parseJsonBytes32(json, string.concat(base, ".event_type")),
                effectiveAt: uint64(effectiveAt),
                payload: vm.parseJsonBytes(json, string.concat(base, ".payload"))
            });
        }

        StockLedger ledger = StockLedger(ledgerAddress);
        console.log("ledger        :", ledgerAddress);
        console.log("events before :", ledger.eventCount());
        console.log("batch size    :", length);

        vm.startBroadcast();
        ledger.appendBatch(expectedCount, expectedHead, inputs);
        vm.stopBroadcast();

        console.log("APPENDED_FROM=", expectedCount + 1);
        console.log("APPENDED_TO=", ledger.eventCount());
        console.log("NEW_HEAD=");
        console.logBytes32(ledger.head());
    }
}
