# Blockchain API Reference

## PoUW Consensus

::: src.blockchain.pouw_consensus.PoUWConsensus
    handler: python
    selection:
      members:
        - generate_work
        - verify_work
        - _compute_result
        - _calculate_reward

## Ethereum Connector

::: src.blockchain.eth_connector.EthereumConnector
    handler: python
    selection:
      members:
        - submit_proof
        - verify_on_chain
        - _load_contract

## Genomic Work

::: src.blockchain.pouw_consensus.GenomicWork
    handler: python

## Work Proof

::: src.blockchain.pouw_consensus.WorkProof
    handler: python

## Smart Contracts

### GenomicProofVerifier

The `GenomicProofVerifier` smart contract handles proof verification on the Ethereum blockchain.

```solidity
interface IGenomicProofVerifier {
    function submitProof(
        bytes calldata _proof,
        bytes32[] calldata _publicInputs
    ) external returns (bytes32);

    function verifyProof(bytes32 _proofId) external returns (bool);
}
```

#### Methods

- `submitProof`: Submit a genomic computation proof
- `verifyProof`: Verify a previously submitted proof

#### Events

- `ProofSubmitted`: Emitted when a new proof is submitted
- `ProofVerified`: Emitted when a proof is verified 