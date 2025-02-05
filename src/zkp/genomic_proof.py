from typing import Dict, List, Any
from dataclasses import dataclass
import json
import subprocess
from pathlib import Path

@dataclass
class GenomicProof:
    proof: Dict
    public_signals: List[str]
    verification_key: Dict

class GenomicZKP:
    """Zero-Knowledge Proof generator for genomic data"""
    
    def __init__(self):
        self.circuit_dir = Path("src/zkp/circuits")
        self.build_dir = Path("build/zkp")
        self.setup_done = False
        self.verification_key = None
        self.proving_key = None
    
    def setup(self, circuit_name: str = "basic_genomic"):
        """Set up the proving system"""
        try:
            # Create build directory if it doesn't exist
            self.build_dir.mkdir(parents=True, exist_ok=True)
            
            # Store circuit name
            self.circuit_name = circuit_name

            # Run setup script
            subprocess.run([
                "./scripts/zkp_setup.sh",
                circuit_name
            ], check=True)
            
            # Load verification key
            with open("verification_key.json") as f:
                self.verification_key = json.load(f)
            
            self.proving_key = "circuit_0000.zkey"
            self.setup_done = True
            
        except Exception as e:
            raise RuntimeError(f"Failed to set up ZK-SNARK system: {str(e)}")
    
    def generate_proof(self, data: Dict[str, Any], public_inputs: Dict[str, Any]) -> Dict:
        """Generate a zero-knowledge proof for genomic data"""
        if not self.setup_done:
            raise RuntimeError("ZK-SNARK system not set up. Call setup() first.")
        
        try:
            input_path = self.build_dir / "input.json"
            witness_path = self.build_dir / "witness.wtns"
            proof_path = self.build_dir / "proof.json"
            public_path = self.build_dir / "public.json"

            # Write input to file
            with open(input_path, 'w') as f:
                json.dump(data, f)
            
            # Generate witness
            subprocess.run([
                "snarkjs", "wtns", "calculate",
                f"{self.circuit_name}.wasm", str(input_path),
                str(witness_path)
            ], check=True)
            
            # Generate proof
            subprocess.run([
                "snarkjs", "groth16", "prove",
                self.proving_key, str(witness_path),
                str(proof_path), str(public_path)
            ], check=True)
            
            # Load proof
            with open(proof_path) as f:
                proof = json.load(f)
            with open(public_path) as f:
                public_signals = json.load(f)
            
            return {
                'proof': proof,
                'public_inputs': public_signals
            }
            
        except Exception as e:
            raise RuntimeError(f"Failed to generate proof: {str(e)}")
    
    def verify_proof(self, proof_data: Dict) -> bool:
        """Verify a genomic zero-knowledge proof"""
        if not self.setup_done:
            raise RuntimeError("ZK-SNARK system not set up. Call setup() first.")
        
        try:
            # Write proof and inputs to files
            with open("proof_to_verify.json", "w") as f:
                json.dump(proof_data['proof'], f)
            with open("public_to_verify.json", "w") as f:
                json.dump(proof_data['public_inputs'], f)
            
            # Verify proof
            result = subprocess.run([
                "snarkjs", "groth16", "verify",
                "verification_key.json",
                "public_to_verify.json",
                "proof_to_verify.json"
            ], capture_output=True, text=True)
            
            return "OK" in result.stdout
            
        except Exception as e:
            raise RuntimeError(f"Failed to verify proof: {str(e)}") 