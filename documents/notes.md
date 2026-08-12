### Agreement content hashes

A cryptographic content hash is a compact fingerprint of the agreement's exact bytes; it does not contain the agreement and cannot be used to reconstruct it. Keccak-256 always produces the same 32-byte hash for the same input, while any change to the text, whitespace, encoding, or line endings produces a different hash. Although collisions exist mathematically, finding different content with the same Keccak-256 hash is computationally infeasible.

In this model, the complete agreement lives in a public source repository and each released version is identified by its version label and content hash. Every adoption, amendment approval, and other signing record that depends on the agreement references that hash and provides the signer the complete agreement in retainable form. Repository URLs, commits, tags, and rendered copies help people find and read the agreement, but the hash identifies the authoritative source bytes.

Verification requires both the claimed agreement file and the trusted hash recorded in a signed document or official ledger event. A verifier hashes the candidate file and compares the result: a match establishes that it is exactly the referenced agreement, while a mismatch exposes any substitution or alteration. The repository may continue to host drafts and later releases without changing an earlier signed agreement, because only content matching the previously recorded hash can satisfy that reference.

### Issuance proceeds versus owner-transfer proceeds

The different treatment is intentional. An issuance creates new shares and dilutes existing shareholders, so its proceeds must be used with a good-faith expectation of benefiting the personal stock. A transfer of the owner's existing shares creates no new shares and does not reduce any existing shareholder's economic percentage; it gives the owner personal liquidity in exchange for surrendering part of the owner's own future participation. Its proceeds may therefore remain personal.

The principal structuring risk exists during initial capitalization: a seed financing intended to capitalize the personal stock should be executed as an issuance, not as an initial allocation to the owner followed by immediate transfers designed to avoid the issuance-proceeds requirements. Once the initial capitalization and seed issuance are completed as intended, later bona fide sales of the owner's existing shares are legitimate secondary transactions rather than circumvention.
