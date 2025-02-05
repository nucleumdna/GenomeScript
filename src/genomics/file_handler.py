from typing import List, Dict, Any, Iterator, Optional
import pysam
from Bio import SeqIO
from dataclasses import dataclass

@dataclass
class QualityMetrics:
    """
    Data structure for genomic quality metrics.
    
    Attributes:
        phred_scores (List[int]): List of Phred quality scores
        coverage_depth (float): Average coverage depth
        gc_content (float): GC content ratio (0-1)
        read_length (int): Average read length in base pairs
    """
    phred_scores: List[int]
    coverage_depth: float
    gc_content: float
    read_length: int

class GenomicFileHandler:
    """
    Core handler for genomic file operations.
    
    Provides functionality for:
    - Loading various genomic file formats
    - Quality filtering
    - Quality metrics calculation
    - File caching
    
    Example:
        >>> handler = GenomicFileHandler()
        >>> data = handler.load_file("sample.bam", "BAM")
        >>> filtered = handler.filter_by_quality(data, min_phred=20)
    """
    def __init__(self):
        self.cached_data = {}
        self.quality_thresholds = {
            'phred': 20,  # Default Phred score threshold
            'coverage': 10  # Default coverage depth
        }

    def load_file(self, file_path: str, file_type: str) -> Any:
        if file_path in self.cached_data:
            return self.cached_data[file_path]

        if file_type not in ["BAM", "CRAM", "SAM", "SFF", "CSFASTA"]:
            raise ValueError(f"Unsupported file format: {file_type}")

        try:
            data = None
            if file_type == "BAM":
                data = self._load_bam(file_path)
            elif file_type == "CRAM":
                data = self._load_cram(file_path)
            elif file_type == "SAM":
                data = self._load_sam(file_path)
            elif file_type == "SFF":
                data = self._load_sff(file_path)
            elif file_type == "CSFASTA":
                data = self._load_csfasta(file_path)
            
            # Store in cache
            self.cached_data[file_path] = data
            return data
        except Exception as e:
            raise RuntimeError(f"Error loading {file_type} file: {str(e)}")

    def _load_bam(self, file_path: str) -> pysam.AlignmentFile:
        return pysam.AlignmentFile(file_path, "rb")

    def _load_cram(self, file_path: str) -> pysam.AlignmentFile:
        return pysam.AlignmentFile(file_path, "rc")

    def _load_sam(self, file_path: str) -> pysam.AlignmentFile:
        return pysam.AlignmentFile(file_path, "r")

    def _load_sff(self, file_path: str) -> Iterator:
        return SeqIO.parse(file_path, "sff")

    def _load_csfasta(self, file_path: str) -> Iterator:
        return SeqIO.parse(file_path, "csfasta")

    def filter_by_quality(self, data: Any, min_phred: int = 20) -> Iterator:
        """Filter reads based on Phred quality scores"""
        try:
            # Reset file pointer if needed
            if hasattr(data, 'reset'):
                data.reset()
            
            for record in data:
                if isinstance(record, pysam.AlignedSegment):
                    # For BAM/SAM files, check query_qualities
                    qualities = record.query_qualities
                    if qualities is not None and len(qualities) > 0:
                        avg_quality = sum(qualities) / len(qualities)
                        if avg_quality >= min_phred:
                            yield record
                else:
                    # For other formats, check letter_annotations
                    qualities = record.letter_annotations.get('phred_quality', [])
                    if qualities and sum(qualities) / len(qualities) >= min_phred:
                        yield record
                    
        except Exception as e:
            raise RuntimeError(f"Error filtering by quality: {str(e)}")

    def analyze_quality_metrics(self, data: Any) -> QualityMetrics:
        """Calculate comprehensive quality metrics"""
        phred_scores = []
        total_bases = 0
        gc_count = 0
        read_lengths = []
        total_positions = 0
        coverage_counts = {}

        try:
            # Reset file pointer if needed
            if hasattr(data, 'reset'):
                data.reset()

            for record in data:
                if isinstance(record, pysam.AlignedSegment):
                    # Handle BAM/SAM records
                    phred_scores.extend(record.query_qualities or [])
                    seq = record.query_sequence
                    
                    # Track coverage
                    if record.reference_start is not None:
                        for pos in range(record.reference_start, record.reference_end or record.reference_start + 1):
                            coverage_counts[pos] = coverage_counts.get(pos, 0) + 1
                else:
                    # Handle other formats (FASTQ, FASTA, etc.)
                    phred_scores.extend(record.letter_annotations.get('phred_quality', []))
                    seq = str(record.seq)

                if seq:
                    total_bases += len(seq)
                    gc_count += seq.count('G') + seq.count('C')
                    read_lengths.append(len(seq))

            # Calculate coverage depth
            avg_coverage = (sum(coverage_counts.values()) / len(coverage_counts)) if coverage_counts else 0.0

            return QualityMetrics(
                phred_scores=phred_scores,
                coverage_depth=avg_coverage,
                gc_content=(gc_count / total_bases if total_bases > 0 else 0.0),
                read_length=int(sum(read_lengths) / len(read_lengths)) if read_lengths else 0
            )
        except Exception as e:
            raise RuntimeError(f"Failed to analyze quality metrics: {str(e)}")

    def _calculate_coverage(self, data: Any) -> float:
        # Implement coverage calculation based on file type
        pass 