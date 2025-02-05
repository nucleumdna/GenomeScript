from typing import Iterator, Dict
from struct import unpack
from .base_parser import GenomicFileParser

class SFFParser(GenomicFileParser):
    """Parser for Standard Flowgram Format (SFF) files"""
    
    def parse(self, file_path: str) -> Iterator[Dict]:
        """Parse SFF file and yield flowgram records"""
        if not self.validate(file_path):
            raise ValueError(f"Invalid SFF file: {file_path}")
        
        try:
            with open(file_path, 'rb') as sff_file:
                # Parse SFF header
                magic = sff_file.read(4)
                if magic != b'.sff':
                    raise ValueError("Invalid SFF file format")
                
                version = unpack('>I', sff_file.read(4))[0]
                index_offset = unpack('>Q', sff_file.read(8))[0]
                index_length = unpack('>I', sff_file.read(4))[0]
                number_of_reads = unpack('>I', sff_file.read(4))[0]
                
                # Parse each read
                for _ in range(number_of_reads):
                    read_header_length = unpack('>H', sff_file.read(2))[0]
                    name_length = unpack('>H', sff_file.read(2))[0]
                    number_of_bases = unpack('>I', sff_file.read(4))[0]
                    clip_qual_left = unpack('>H', sff_file.read(2))[0]
                    clip_qual_right = unpack('>H', sff_file.read(2))[0]
                    clip_adapter_left = unpack('>H', sff_file.read(2))[0]
                    clip_adapter_right = unpack('>H', sff_file.read(2))[0]
                    
                    name = sff_file.read(name_length).decode('ascii')
                    # Skip to next alignment boundary
                    padding = (read_header_length - (16 + name_length))
                    if padding > 0:
                        sff_file.read(padding)
                    
                    # Read flowgram values
                    flowgram_values = [unpack('>H', sff_file.read(2))[0] for _ in range(number_of_bases)]
                    flow_index_per_base = list(sff_file.read(number_of_bases))
                    bases = sff_file.read(number_of_bases).decode('ascii')
                    quality_scores = list(sff_file.read(number_of_bases))
                    
                    yield {
                        'name': name,
                        'number_of_bases': number_of_bases,
                        'clip_qual_left': clip_qual_left,
                        'clip_qual_right': clip_qual_right,
                        'flowgram_values': flowgram_values,
                        'flow_index_per_base': flow_index_per_base,
                        'bases': bases,
                        'quality_scores': quality_scores
                    }
                    
        except Exception as e:
            raise ValueError(f"Error parsing SFF file: {str(e)}")
    
    def validate(self, file_path: str) -> bool:
        """Validate SFF file format"""
        try:
            with open(file_path, 'rb') as f:
                # Check magic number
                magic = f.read(4)
                if magic != b'.sff':
                    return False
                
                # Check version
                version = f.read(4)
                if not version or len(version) != 4:
                    return False
                
                # Check basic structure
                try:
                    index_offset = unpack('>Q', f.read(8))[0]
                    index_length = unpack('>I', f.read(4))[0]
                    num_reads = unpack('>I', f.read(4))[0]
                    
                    # Additional validation
                    if index_offset < 0 or index_length < 0 or num_reads < 0:
                        return False
                        
                    return True
                except:
                    return False
                
        except Exception:
            return False 