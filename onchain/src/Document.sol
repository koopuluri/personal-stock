// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title Document
/// @notice A single markdown document published onchain. One instance per document;
///         the contract address is the namespace.
/// @dev The current content lives in storage so anyone can read it in one click on
///      Basescan's "Read Contract" tab. That legibility is the point, and it is what
///      the extra gas buys.
///
///      Published versions are permanent and irreversible. There is no edit, no
///      delete, and no upgrade path. A mistake is corrected by publishing the next
///      version, never by pretending the previous one did not happen.
///
///      The transaction history IS the document's version history: every publish
///      emits `Published` carrying the full content, so every version ever published
///      remains recoverable from this contract's logs even though storage holds only
///      the latest one.
contract Document {
    /// @notice Human-readable name for this document, e.g. "stock" or "agreement".
    string public label;
    /// @notice The only address permitted to publish.
    address public owner;
    /// @notice Number of publishes so far. 0 means nothing has been published yet.
    uint256 public version;
    /// @notice The current document, verbatim. Overwritten by each publish.
    string public content;
    /// @notice keccak256 of the exact bytes of `content`.
    bytes32 public latestHash;

    /// @notice Emitted on every publish. These logs are the version history.
    event Published(uint256 indexed version, bytes32 contentHash, string content);
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    error NotOwner();
    error EmptyContent();
    error ZeroAddress();

    modifier onlyOwner() {
        if (msg.sender != owner) revert NotOwner();
        _;
    }

    constructor(string memory _label) {
        label = _label;
        owner = msg.sender;
    }

    /// @notice Publish a new version. Irreversible.
    /// @param newContent The document bytes, exactly as they should be published.
    function publish(string calldata newContent) external onlyOwner {
        if (bytes(newContent).length == 0) revert EmptyContent();
        content = newContent;
        latestHash = keccak256(bytes(newContent));
        version += 1;
        emit Published(version, latestHash, newContent);
    }

    /// @notice Hand publishing rights to a new address.
    function transferOwnership(address newOwner) external onlyOwner {
        if (newOwner == address(0)) revert ZeroAddress();
        emit OwnershipTransferred(owner, newOwner);
        owner = newOwner;
    }
}
