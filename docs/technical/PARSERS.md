# Genomic File Parsers

## Overview
The parser system provides a unified interface for handling different genomic file formats.

## Base Parser
All parsers inherit from `GenomicFileParser` which defines the interface:

```python
class GenomicFileParser:
    def validate(self, file_path: str) -> bool:
        """Validate file format"""
        pass

    def parse(self, file_path: str) -> Iterator[Dict]:
        """Parse file and yield records"""
        pass
```

## Supported Formats

### BAM Parser
- Binary format for storing sequence alignments
- Requires: pysam
- Features:
  * Random access
  * Compressed storage
  * Quality score support

### CRAM Parser
- Reference-based compression format
- Requires: pysam, reference genome
- Features:
  * Higher compression than BAM
  * Reference-based storage
  * Quality score preservation

### SFF Parser
- Standard Flowgram Format
- Features:
  * Raw sequencing data
  * Quality metrics
  * Flow information

### CSFASTA Parser
- Color Space FASTA format
- Features:
  * Color space encoding
  * Quality scores
  * Header information

## Adding New Parsers
1. Create new class inheriting from `GenomicFileParser`
2. Implement `validate()` and `parse()` methods
3. Register parser with `GenomicFileRegistry`

Example:
```python
class CustomParser(GenomicFileParser):
    def validate(self, file_path: str) -> bool:
        # Implement validation
        return True

    def parse(self, file_path: str) -> Iterator[Dict]:
        # Implement parsing
        yield {"data": "example"}

registry = GenomicFileRegistry()
registry.register_parser("CUSTOM", CustomParser()) 