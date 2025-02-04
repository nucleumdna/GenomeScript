from web3 import Web3
from eth_account import Account
from typing import Dict, Any

class EthereumConnector:
    def __init__(self, node_url: str, contract_address: str):
        self.web3 = Web3(Web3.HTTPProvider(node_url))
        self.contract = self._load_contract(contract_address)
        
    def submit_proof(self, proof: GenomicProof, account: Account) -> str:
        """Submit proof to Ethereum smart contract"""
        tx_data = self.contract.functions.submitProof(
            proof.proof,
            proof.public_inputs
        ).build_transaction({
            'from': account.address,
            'gas': 2000000,
            'gasPrice': self.web3.eth.gas_price,
            'nonce': self.web3.eth.get_transaction_count(account.address)
        })
        
        signed_tx = account.sign_transaction(tx_data)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return tx_hash.hex()

    def verify_on_chain(self, proof_id: str) -> bool:
        """Verify proof on Ethereum blockchain"""
        return self.contract.functions.verifyProof(proof_id).call() 