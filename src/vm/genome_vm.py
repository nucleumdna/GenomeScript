from typing import Dict, Any
import pysam
from Bio import SeqIO
from ..genomics.file_handler import GenomicFileHandler

class GenomeVM:
    def __init__(self):
        self.variables: Dict[str, Any] = {}
        self.loaded_files = {}
        self.file_handler = GenomicFileHandler()

    def execute(self, ast_nodes):
        for node in ast_nodes:
            self._execute_node(node)

    def _execute_node(self, node):
        if isinstance(node, LoadNode):
            self._execute_load(node)
        elif isinstance(node, AnalyzeNode):
            self._execute_analyze(node)

    def _execute_load(self, node: LoadNode):
        data = self.file_handler.load_file(node.file_path, node.file_type)
        if node.quality_filter:
            data = self.file_handler.filter_by_quality(
                data, 
                min_phred=node.quality_filter.get('min_phred', 20)
            )
        self.variables[node.variable_name] = data

    def _execute_analyze(self, node: AnalyzeNode):
        data = self.variables[node.target]
        if node.operation == "QUALITY":
            metrics = self.file_handler.analyze_quality_metrics(data)
            self.variables[node.output] = metrics

    def _load_fasta(self, file_path: str):
        return list(SeqIO.parse(file_path, "fasta"))

    def _load_vcf(self, file_path: str):
        return pysam.VariantFile(file_path)

    def _load_bam(self, file_path: str):
        return pysam.AlignmentFile(file_path, "rb") 