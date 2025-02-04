from typing import Optional
import hashlib
from web3 import Web3
from ..blockchain.pouw_consensus import PoUWConsensus, GenomicWork, WorkProof
from ..storage.fractal_storage import FractalStorage

class WorkerNode:
    def __init__(self, node_url: str, contract_address: str, private_key: str):
        self.web3 = Web3(Web3.HTTPProvider(node_url))
        self.contract = self._load_contract(contract_address)
        self.account = self.web3.eth.account.from_key(private_key)
        self.consensus = PoUWConsensus()
        self.storage = FractalStorage()
        
    def process_work(self, work: GenomicWork) -> Optional[WorkProof]:
        """Process genomic work and generate proof"""
        start_time = time.time()
        nonce = 0
        
        # Compute result
        result = self.consensus._compute_result(work.sequence_data)
        
        # Find valid nonce
        while True:
            work_hash = hashlib.sha256(
                work.query_id.encode() + 
                result +
                str(nonce).encode()
            ).hexdigest()
            
            if work_hash.startswith('0' * work.difficulty):
                break
                
            nonce += 1
            
        computation_time = time.time() - start_time
        
        return WorkProof(
            work_id=work.query_id,
            result=result,
            computation_time=computation_time,
            nonce=nonce,
            worker_address=self.account.address
        )
        
    def submit_proof(self, work: GenomicWork, proof: WorkProof):
        """Submit work proof to blockchain"""
        tx_data = self.contract.functions.submitWork(
            work.query_id,
            proof.result,
            proof.nonce
        ).build_transaction({
            'from': self.account.address,
            'gas': 2000000,
            'gasPrice': self.web3.eth.gas_price,
            'nonce': self.web3.eth.get_transaction_count(self.account.address)
        })
        
        signed_tx = self.account.sign_transaction(tx_data)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return tx_hash.hex() 