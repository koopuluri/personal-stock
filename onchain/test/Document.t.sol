// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Test, console} from "forge-std/Test.sol";
import {Document} from "../src/Document.sol";

contract DocumentTest is Test {
    Document doc;
    address owner = address(this);
    address stranger = address(0xBEEF);

    event Published(uint256 indexed version, bytes32 contentHash, string content);

    function setUp() public {
        doc = new Document("stock");
    }

    function test_InitialState() public view {
        assertEq(doc.label(), "stock");
        assertEq(doc.owner(), owner);
        assertEq(doc.version(), 0);
        assertEq(doc.content(), "");
        assertEq(doc.latestHash(), bytes32(0));
    }

    function test_PublishIncrementsVersion() public {
        doc.publish("# v1\n");
        assertEq(doc.version(), 1);
        doc.publish("# v2\n");
        assertEq(doc.version(), 2);
    }

    function test_PublishStoresContentAndHash() public {
        string memory body = "# Stock\n\nShares outstanding: 10,000,000.\n";

        vm.expectEmit(true, false, false, true);
        emit Published(1, keccak256(bytes(body)), body);
        doc.publish(body);

        assertEq(doc.content(), body);
        assertEq(doc.latestHash(), keccak256(bytes(body)));
    }

    function test_PublishTwiceOverwrites() public {
        doc.publish("first\n");
        doc.publish("second\n");

        assertEq(doc.content(), "second\n");
        assertEq(doc.latestHash(), keccak256(bytes("second\n")));
        assertEq(doc.version(), 2);
    }

    function test_NonOwnerCannotPublish() public {
        vm.prank(stranger);
        vm.expectRevert(Document.NotOwner.selector);
        doc.publish("takeover\n");
    }

    function test_EmptyContentReverts() public {
        vm.expectRevert(Document.EmptyContent.selector);
        doc.publish("");
    }

    function test_TransferOwnership() public {
        doc.transferOwnership(stranger);
        assertEq(doc.owner(), stranger);

        vm.expectRevert(Document.NotOwner.selector);
        doc.publish("no longer mine\n");

        vm.prank(stranger);
        doc.publish("mine now\n");
        assertEq(doc.content(), "mine now\n");
    }

    function test_TransferOwnershipRejectsZero() public {
        vm.expectRevert(Document.ZeroAddress.selector);
        doc.transferOwnership(address(0));
    }

    function test_NonOwnerCannotTransferOwnership() public {
        vm.prank(stranger);
        vm.expectRevert(Document.NotOwner.selector);
        doc.transferOwnership(stranger);
    }

    /// @notice What a realistically sized document costs. Storing content is the
    ///         expensive part and is the price of the one-click read.
    function test_GasForFiveKilobyteDocument() public {
        string memory body = _document(5000);
        assertEq(bytes(body).length, 5000);

        uint256 before = gasleft();
        doc.publish(body);
        uint256 used = before - gasleft();

        console.log("publish() gas for a 5,000 byte document:", used);
        assertEq(doc.latestHash(), keccak256(bytes(body)));
    }

    /// @dev Markdown-shaped filler of an exact byte length.
    function _document(uint256 size) internal pure returns (string memory) {
        bytes memory line = bytes("Shareholders hold a claim on realized exits above the floor. ");
        bytes memory out = new bytes(size);
        for (uint256 i = 0; i < size; i++) {
            out[i] = line[i % line.length];
        }
        out[size - 1] = "\n";
        return string(out);
    }
}
