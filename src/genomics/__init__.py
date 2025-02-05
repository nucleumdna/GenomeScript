"""
Genomics Module (v1.1.0)
========================

A comprehensive framework for handling and analyzing genomic data files.

Key Features
-----------
* Multi-format support (BAM, CRAM, SFF, CSFASTA)
* Quality metrics analysis
* Efficient file caching
* Extensible parser system

Main Components
--------------
GenomicFileHandler:
    Core class for file operations and quality analysis
    >>> handler = GenomicFileHandler()
    >>> data = handler.load_file("sample.bam", "BAM")
    >>> metrics = handler.analyze_quality_metrics(data)

QualityMetrics:
    Data structure for quality analysis results
    >>> metrics = QualityMetrics(
    ...     phred_scores=[30, 20, 40],
    ...     coverage_depth=15.5,
    ...     gc_content=0.45,
    ...     read_length=100
    ... )

File Format Support
------------------
BAM:
    Binary Alignment/Map format
    >>> data = handler.load_file("sample.bam", "BAM")

CRAM:
    Compressed Reference-oriented Alignment Map
    >>> data = handler.load_file("sample.cram", "CRAM")

SFF:
    Standard Flowgram Format
    >>> data = handler.load_file("sample.sff", "SFF")

CSFASTA:
    Color Space FASTA
    >>> data = handler.load_file("sample.csfasta", "CSFASTA")

Quality Analysis
---------------
* Phred score calculation
* Coverage depth analysis
* GC content measurement
* Read length statistics

For more information, see the README.md in the module directory.
"""

__version__ = "1.1.0"
from .file_handler import GenomicFileHandler, QualityMetrics
from .file_registry import GenomicFileRegistry

__all__ = ['GenomicFileHandler', 'QualityMetrics', 'GenomicFileRegistry', '__version__'] 