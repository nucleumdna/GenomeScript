from typing import Iterator, Dict
from .base_parser import GenomicFileParser

class CSFASTAParser(GenomicFileParser):
    """Parser for Color Space FASTA format files"""
    
    def parse(self, file_path: str) -> Iterator[Dict]:
        """Parse CSFASTA file and yield color space sequences"""
        if not self.validate(file_path):
            raise ValueError(f"Invalid CSFASTA file: {file_path}")
        
        try:
            current_header = None
            current_sequence = []
            
            with open(file_path, 'r') as csfasta_file:
                for line in csfasta_file:
                    line = line.strip()
                    if not line:
                        continue
                        
                    if line.startswith('>'):
                        if current_header:
                            yield {
                                'header': current_header,
                                'sequence': ''.join(current_sequence)
                            }
                        current_header = line[1:]
                        current_sequence = []
                    else:
                        # Validate color space format (0-3 or .)
                        if not all(c in '0123.' for c in line):
                            raise ValueError(f"Invalid color space character in sequence: {line}")
                        current_sequence.append(line)
                
                if current_header:
                    yield {
                        'header': current_header,
                        'sequence': ''.join(current_sequence)
                    }
                    
        except Exception as e:
            raise ValueError(f"Error parsing CSFASTA file: {str(e)}")
    
    def validate(self, file_path: str) -> bool:
        """Validate CSFASTA file format"""
        try:
            with open(file_path) as f:
                content = f.read().strip()
                if not content:  # Empty file
                    return False
                
                lines = [line.strip() for line in content.split('\n') if line.strip()]
                if not lines:  # Only whitespace
                    return False
                
                if not lines[0].startswith('>'):  # Must start with header
                    return False
                
                # Check alternating header/sequence pattern
                for i, line in enumerate(lines):
                    if i % 2 == 0:  # Header lines
                        if not line.startswith('>'):
                            return False
                    else:  # Sequence lines
                        if not all(c in '0123.' for c in line):
                            return False
                        
                # Must have at least one header and sequence
                if len(lines) < 2:
                    return False
                
                return True
        except Exception:
            return False 