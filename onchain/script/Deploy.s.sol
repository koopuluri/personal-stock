// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Script, console} from "forge-std/Script.sol";
import {Document} from "../src/Document.sol";

/// @notice Deploys the two Document instances. Run once per chain.
///         forge script onchain/script/Deploy.s.sol --root onchain --rpc-url base_sepolia
///         --account <name> --broadcast --verify
contract Deploy is Script {
    function run() external {
        vm.startBroadcast();

        Document stock = new Document("stock");
        Document agreement = new Document("agreement");

        vm.stopBroadcast();

        console.log("chain id        :", block.chainid);
        console.log("deployer / owner:", stock.owner());
        console.log("");
        console.log("STOCK_ADDRESS    =", address(stock));
        console.log("AGREEMENT_ADDRESS=", address(agreement));
        console.log("");
        console.log("Record both addresses in the top-level README.md before publishing anything.");
    }
}
