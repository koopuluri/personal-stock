// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Script, console} from "forge-std/Script.sol";
import {Document} from "../src/Document.sol";

/// @notice Publishes a file to a Document contract, byte for byte.
///         Content is never modified or normalized here — whatever is on disk is what
///         goes onchain. Canonicalization is enforced beforehand by
///         onchain/script/check.sh.
///
///         DOC_ADDRESS=0x... DOC_PATH="$PWD/documents/stock.md" \
///           forge script onchain/script/Publish.s.sol --root onchain \
///           --rpc-url base_sepolia --account <name> --broadcast
contract Publish is Script {
    function run() external {
        address docAddress = vm.envAddress("DOC_ADDRESS");
        string memory path = vm.envString("DOC_PATH");

        string memory content = vm.readFile(path);
        bytes32 contentHash = keccak256(bytes(content));

        Document doc = Document(docAddress);

        console.log("contract     :", docAddress);
        console.log("label        :", doc.label());
        console.log("path         :", path);
        console.log("bytes        :", bytes(content).length);
        console.log("content hash :", vm.toString(contentHash));
        console.log("from version :", doc.version());

        vm.startBroadcast();
        uint256 gasBefore = gasleft();
        doc.publish(content);
        uint256 gasUsed = gasBefore - gasleft();
        vm.stopBroadcast();

        console.log("");
        console.log("PUBLISHED_VERSION=", doc.version());
        console.log("PUBLISHED_HASH   =", vm.toString(doc.latestHash()));
        console.log("GAS_USED         =", gasUsed);

        require(doc.latestHash() == contentHash, "onchain hash != file hash");
    }
}
