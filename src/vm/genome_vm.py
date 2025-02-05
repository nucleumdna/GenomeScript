from typing import Dict, Any
import pysam
from Bio import SeqIO
from ..genomics.file_handler import GenomicFileHandler
from ..genomics.file_registry import FileFormat, GenomicFileRegistry
from ..compiler.parser import LoadNode, AnalyzeNode

class GenomeVM:
    def __init__(self):
        self.variables: Dict[str, Any] = {}
        self.file_registry = GenomicFileRegistry()
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
        self.execute_load(node)

    def execute_load(self, node):
        """Execute LOAD command"""
        try:
            format_type = FileFormat[node.format.upper()]
            parser = self.file_registry.get_parser(format_type)
            
            # Validate file
            if not parser.validate(node.file_path):
                raise ValueError(f"Invalid {format_type.value} file: {node.file_path}")
            
            # Parse file
            data = list(parser.parse(node.file_path))
            self.variables[node.target] = data
            
        except KeyError:
            raise ValueError(f"Unsupported file format: {node.format}")
        except Exception as e:
            raise RuntimeError(f"Error loading file: {str(e)}")

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