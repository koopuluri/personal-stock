// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Script, console} from "forge-std/Script.sol";
import {StockLedger} from "../src/StockLedger.sol";

/// @notice Deploys the single append-only ledger for a personal stock.
contract Deploy is Script {
    function run() external {
        string memory stockName = vm.envString("STOCK_NAME");
        address controller = vm.envAddress("CONTROLLER");

        vm.startBroadcast();
        StockLedger ledger = new StockLedger(stockName, controller);
        vm.stopBroadcast();

        console.log("stock name :", stockName);
        console.log("controller :", controller);
        console.log("LEDGER_ADDRESS=", address(ledger));
    }
}
