from typing import Dict, Any, Iterator
import pysam
from Bio import SeqIO
from dataclasses import dataclass

@dataclass
class QualityMetrics:
    phred_scores: List[int]
    coverage_depth: float
    gc_content: float
    read_length: int

class GenomicFileHandler:
    def __init__(self):
        self.cached_data = {}
        self.quality_thresholds = {
            'phred': 20,  # Default Phred score threshold
            'coverage': 10  # Default coverage depth
        }

    def load_file(self, file_path: str, file_type: str) -> Any:
        if file_path in self.cached_data:
            return self.cached_data[file_path]

        try:
            if file_type == "BAM":
                return self._load_bam(file_path)
            elif file_type == "CRAM":
                return self._load_cram(file_path)
            elif file_type == "SAM":
                return self._load_sam(file_path)
            elif file_type == "SFF":
                return self._load_sff(file_path)
            elif file_type == "CSFASTA":
                return self._load_csfasta(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_type}")
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
        if isinstance(data, pysam.AlignmentFile):
            return self._filter_alignment_quality(data, min_phred)
        else:
            return self._filter_seq_quality(data, min_phred)

    def _filter_alignment_quality(self, alignment: pysam.AlignmentFile, min_phred: int) -> Iterator:
        for read in alignment:
            if read.mapping_quality >= min_phred:
                yield read

    def _filter_seq_quality(self, sequences: Iterator, min_phred: int) -> Iterator:
        for seq in sequences:
            if self._calculate_mean_quality(seq) >= min_phred:
                yield seq

    def _calculate_mean_quality(self, seq) -> float:
        if not hasattr(seq, 'letter_annotations'):
            return 0
        qualities = seq.letter_annotations.get('phred_quality', [])
        return sum(qualities) / len(qualities) if qualities else 0

    def analyze_quality_metrics(self, data: Any) -> QualityMetrics:
        """Calculate comprehensive quality metrics"""
        phred_scores = []
        total_bases = 0
        gc_count = 0
        read_lengths = []

        for record in data:
            if isinstance(record, pysam.AlignedSegment):
                phred_scores.extend(record.query_qualities or [])
                seq = record.query_sequence
            else:
                phred_scores.extend(record.letter_annotations.get('phred_quality', []))
                seq = str(record.seq)

            if seq:
                total_bases += len(seq)
                gc_count += seq.count('G') + seq.count('C')
                read_lengths.append(len(seq))

        return QualityMetrics(
            phred_scores=phred_scores,
            coverage_depth=self._calculate_coverage(data),
            gc_content=(gc_count / total_bases if total_bases > 0 else 0),
            read_length=sum(read_lengths) / len(read_lengths) if read_lengths else 0
        )

    def _calculate_coverage(self, data: Any) -> float:
        # Implement coverage calculation based on file type
        pass 