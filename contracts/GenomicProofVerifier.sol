// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "./ZKVerifier.sol"; // Import ZK-SNARKs verifier

contract GenomicProofVerifier is Ownable {
    struct GenomicProof {
        bytes proof;
        bytes32[] publicInputs;
        uint256 timestamp;
        bool verified;
    }
    
    mapping(bytes32 => GenomicProof) public proofs;
    ZKVerifier public zkVerifier;
    
    event ProofSubmitted(bytes32 indexed proofId, bytes32[] publicInputs);
    event ProofVerified(bytes32 indexed proofId, bool success);
    
    constructor(address _zkVerifier) {
        zkVerifier = ZKVerifier(_zkVerifier);
    }
    
    function submitProof(bytes calldata _proof, bytes32[] calldata _publicInputs) 
        external 
        returns (bytes32)
    {
        bytes32 proofId = keccak256(abi.encodePacked(_proof, _publicInputs));
        
        proofs[proofId] = GenomicProof({
            proof: _proof,
            publicInputs: _publicInputs,
            timestamp: block.timestamp,
            verified: false
        });
        
        emit ProofSubmitted(proofId, _publicInputs);
        return proofId;
    }
    
    function verifyProof(bytes32 _proofId) external returns (bool) {
        GenomicProof storage proof = proofs[_proofId];
        require(proof.timestamp > 0, "Proof does not exist");
        
        bool isValid = zkVerifier.verify(proof.proof, proof.publicInputs);
        proof.verified = isValid;
        
        emit ProofVerified(_proofId, isValid);
        return isValid;
    }
} 