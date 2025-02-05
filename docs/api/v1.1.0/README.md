# Nucleum API Documentation v1.1.0

## Core Components

### GenomicFileHandler

Main class for handling genomic files and performing analysis.

```python
class GenomicFileHandler:
    def __init__(self):
        """Initialize handler with empty cache"""
        
    def load_file(self, file_path: str, file_type: str) -> Any:
        """
        Load genomic file of specified type.
        
        Args:
            file_path (str): Path to genomic file
            file_type (str): One of ["BAM", "CRAM", "SAM", "SFF", "CSFASTA"]
            
        Returns:
            Any: File handler object (type depends on format)
            
        Raises:
            ValueError: If file_type is not supported
            RuntimeError: If file loading fails
        """
        
    def filter_by_quality(self, data: Any, min_phred: int = 20) -> Iterator:
        """
        Filter reads based on quality scores.
        
        Args:
            data: Genomic file data
            min_phred (int): Minimum Phred quality score (default: 20)
            
        Returns:
            Iterator of filtered reads
        """
        
    def analyze_quality_metrics(self, data: Any) -> QualityMetrics:
        """
        Calculate quality metrics for genomic data.
        
        Args:
            data: Genomic file data
            
        Returns:
            QualityMetrics object with calculated metrics
        """
```

### QualityMetrics

Data structure for storing quality analysis results.

```python
@dataclass
class QualityMetrics:
    phred_scores: List[int]    # List of Phred quality scores
    coverage_depth: float      # Average coverage depth
    gc_content: float         # GC content ratio (0-1)
    read_length: int          # Average read length
```

### GenomicFileRegistry

Registry for managing file format parsers.

```python
class GenomicFileRegistry:
    def register_parser(self, format_name: str, parser: GenomicFileParser) -> None:
        """
        Register a new parser for a file format.
        
        Args:
            format_name (str): Name of the format (e.g., "BAM")
            parser (GenomicFileParser): Parser implementation
        """
        
    def get_parser(self, format_name: str) -> GenomicFileParser:
        """
        Get parser for specified format.
        
        Args:
            format_name (str): Name of the format
            
        Returns:
            GenomicFileParser instance
            
        Raises:
            ValueError: If format is not supported
        """
```

## File Parsers

### Base Parser Interface

```python
class GenomicFileParser:
    def validate(self, file_path: str) -> bool:
        """
        Validate file format.
        
        Args:
            file_path (str): Path to file
            
        Returns:
            bool: True if valid, False otherwise
        """
        
    def parse(self, file_path: str) -> Iterator[Dict]:
        """
        Parse file and yield records.
        
        Args:
            file_path (str): Path to file
            
        Returns:
            Iterator of parsed records
            
        Raises:
            ValueError: If file is invalid
        """
```

### Format-Specific Parsers

#### BAMParser
```python
class BAMParser(GenomicFileParser):
    """Parser for Binary Alignment Map (BAM) files"""
    
    def parse(self, file_path: str) -> Iterator[Dict]:
        """
        Yields:
            Dict with keys:
                - query_name (str)
                - sequence (str)
                - mapping_quality (int)
                - reference_start (int)
                - reference_end (int)
        """
```

#### CRAMParser
```python
class CRAMParser(GenomicFileParser):
    """Parser for CRAM files"""
    
    def __init__(self, reference_path: str = None):
        """
        Args:
            reference_path (str): Path to reference genome
        """
```

#### SFFParser
```python
class SFFParser(GenomicFileParser):
    """Parser for Standard Flowgram Format files"""
    
    def parse(self, file_path: str) -> Iterator[Dict]:
        """
        Yields:
            Dict with keys:
                - name (str)
                - number_of_bases (int)
                - flowgram_values (List[int])
                - quality_scores (List[int])
        """
```

#### CSFASTAParser
```python
class CSFASTAParser(GenomicFileParser):
    """Parser for Color Space FASTA files"""
    
    def parse(self, file_path: str) -> Iterator[Dict]:
        """
        Yields:
            Dict with keys:
                - header (str)
                - sequence (str)
        """
```

## Usage Examples

### Basic Usage
```python
from genomics import GenomicFileHandler

handler = GenomicFileHandler()

# Load BAM file
bam_data = handler.load_file("sample.bam", "BAM")

# Get quality metrics
metrics = handler.analyze_quality_metrics(bam_data)
print(f"Coverage: {metrics.coverage_depth}x")
print(f"GC content: {metrics.gc_content * 100}%")

# Filter by quality
filtered = handler.filter_by_quality(bam_data, min_phred=30)
for read in filtered:
    process_read(read)
```

### Custom Parser Registration
```python
from genomics import GenomicFileRegistry, GenomicFileParser

class CustomParser(GenomicFileParser):
    def validate(self, file_path: str) -> bool:
        return True
        
    def parse(self, file_path: str) -> Iterator[Dict]:
        yield {"data": "example"}

registry = GenomicFileRegistry()
registry.register_parser("CUSTOM", CustomParser())
```

## Error Handling

Common exceptions:
- `ValueError`: Invalid format or parameters
- `RuntimeError`: Processing errors
- `FileNotFoundError`: Missing files
- `OSError`: I/O errors

Example:
```python
try:
    data = handler.load_file("sample.bam", "BAM")
except ValueError as e:
    print(f"Invalid format: {e}")
except RuntimeError as e:
    print(f"Processing error: {e}") 