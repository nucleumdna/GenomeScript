// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract GenomicPoUW is ERC20, Ownable {
    struct Work {
        bytes32 queryId;
        bytes32 dataHash;
        uint256 difficulty;
        uint256 reward;
        bool completed;
    }
    
    mapping(bytes32 => Work) public works;
    mapping(address => uint256) public workerRewards;
    
    uint256 public minDifficulty = 4;
    uint256 public targetBlockTime = 600; // 10 minutes
    
    event WorkGenerated(bytes32 indexed queryId, uint256 difficulty, uint256 reward);
    event WorkCompleted(bytes32 indexed queryId, address indexed worker, uint256 reward);
    
    constructor() ERC20("Genomic Token", "GNOM") {
        _mint(address(this), 1000000 * 10**decimals());
    }
    
    function generateWork(bytes32 dataHash, uint256 difficulty) 
        external 
        onlyOwner 
        returns (bytes32)
    {
        require(difficulty >= minDifficulty, "Difficulty too low");
        
        bytes32 queryId = keccak256(abi.encodePacked(dataHash, block.timestamp));
        uint256 reward = calculateReward(difficulty);
        
        works[queryId] = Work({
            queryId: queryId,
            dataHash: dataHash,
            difficulty: difficulty,
            reward: reward,
            completed: false
        });
        
        emit WorkGenerated(queryId, difficulty, reward);
        return queryId;
    }
    
    function submitWork(
        bytes32 queryId,
        bytes32 resultHash,
        uint256 nonce
    ) external {
        Work storage work = works[queryId];
        require(!work.completed, "Work already completed");
        
        // Verify work meets difficulty requirement
        bytes32 workHash = keccak256(abi.encodePacked(queryId, resultHash, nonce));
        require(
            uint256(workHash) < 2**(256 - work.difficulty),
            "Invalid proof of work"
        );
        
        // Mark work as completed and reward worker
        work.completed = true;
        workerRewards[msg.sender] += work.reward;
        
        // Transfer tokens
        _transfer(address(this), msg.sender, work.reward);
        
        emit WorkCompleted(queryId, msg.sender, work.reward);
    }
    
    function calculateReward(uint256 difficulty) public view returns (uint256) {
        uint256 baseReward = 10 * 10**decimals();
        return baseReward * (2**(difficulty - minDifficulty));
    }
} 