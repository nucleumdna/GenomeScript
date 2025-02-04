from typing import Tuple, List
import pandas as pd
from Bio import SeqIO
from sklearn.model_selection import train_test_split

class GenomicDataPreprocessor:
    def __init__(self, sequence_length: int = 1000):
        self.sequence_length = sequence_length

    def prepare_training_data(self, vcf_path: str, fasta_path: str) -> Tuple[List[str], List[int]]:
        """Prepare training data from VCF and reference genome"""
        # Load reference genome
        reference = self._load_reference(fasta_path)
        
        # Load variants
        variants_df = pd.read_csv(vcf_path, sep='\t')
        
        sequences = []
        labels = []
        
        for _, variant in variants_df.iterrows():
            # Extract sequence context
            pos = variant['POS']
            context = self._get_sequence_context(reference, pos)
            
            # Apply variant
            variant_seq = self._apply_variant(context, variant)
            sequences.append(variant_seq)
            
            # Get label from clinical significance
            label = self._get_label(variant['CLNSIG'])
            labels.append(label)
        
        return sequences, labels

    def _get_sequence_context(self, reference: str, position: int) -> str:
        """Extract sequence context around variant"""
        start = max(0, position - self.sequence_length // 2)
        end = start + self.sequence_length
        return reference[start:end]

    def _apply_variant(self, context: str, variant: pd.Series) -> str:
        """Apply variant to sequence context"""
        ref = variant['REF']
        alt = variant['ALT']
        pos = self.sequence_length // 2
        
        return context[:pos] + alt + context[pos + len(ref):]

    def _get_label(self, clinical_significance: str) -> int:
        """Convert clinical significance to numeric label"""
        significance_map = {
            'Pathogenic': 0,
            'Likely_pathogenic': 1,
            'Uncertain_significance': 2,
            'Likely_benign': 3,
            'Benign': 4
        }
        return significance_map.get(clinical_significance, 2) 