import pytest
from pathlib import Path
import pysam
from src.genomics.file_handler import GenomicFileHandler, QualityMetrics

@pytest.fixture
def test_data_dir(tmp_path):
    """Create a temporary directory with test data files"""
    data_dir = tmp_path / "genomics"
    data_dir.mkdir()
    return data_dir

@pytest.fixture
def sample_bam(test_data_dir):
    """Create a sample BAM file for testing"""
    bam_path = test_data_dir / "test.bam"
    
    # Create a simple BAM file
    header = {'HD': {'VN': '1.0'},
             'SQ': [{'LN': 1000, 'SN': 'chr1'}]}
    
    with pysam.AlignmentFile(str(bam_path), "wb", header=header) as outf:
        a = pysam.AlignedSegment()
        a.query_name = "read1"
        a.query_sequence = "ATCG"
        a.reference_id = 0
        a.reference_start = 0
        a.mapping_quality = 30
        a.query_qualities = [30, 30, 30, 30]  # Add quality scores
        a.cigar = ((0,4),)
        outf.write(a)
    
    return str(bam_path)

def test_quality_metrics_creation():
    """Test QualityMetrics dataclass"""
    metrics = QualityMetrics(
        phred_scores=[30, 20, 40],
        coverage_depth=15.5,
        gc_content=0.45,
        read_length=100
    )
    assert metrics.phred_scores == [30, 20, 40]
    assert metrics.coverage_depth == 15.5
    assert metrics.gc_content == 0.45
    assert metrics.read_length == 100

def test_file_handler_initialization():
    """Test GenomicFileHandler initialization"""
    handler = GenomicFileHandler()
    assert handler.cached_data == {}
    assert handler.quality_thresholds['phred'] == 20
    assert handler.quality_thresholds['coverage'] == 10

def test_file_handler_caching(sample_bam):
    """Test file caching functionality"""
    handler = GenomicFileHandler()
    
    # First load should cache
    data1 = handler.load_file(sample_bam, "BAM")
    assert sample_bam in handler.cached_data
    
    # Second load should use cache
    data2 = handler.load_file(sample_bam, "BAM")
    assert data1 == data2

def test_unsupported_format():
    """Test handling of unsupported formats"""
    handler = GenomicFileHandler()
    with pytest.raises(ValueError, match="Unsupported file format: XYZ"):
        handler.load_file("test.xyz", "XYZ")
    
    # Test with valid format but invalid file
    with pytest.raises(RuntimeError, match="Error loading BAM file"):
        handler.load_file("nonexistent.bam", "BAM")

def test_quality_filtering_edge_cases(sample_bam):
    """Test quality filtering with edge cases"""
    handler = GenomicFileHandler()
    data = handler.load_file(sample_bam, "BAM")
    
    # Test with very high threshold
    filtered = list(handler.filter_by_quality(data, min_phred=100))
    assert len(filtered) == 0
    
    # Test with very low threshold
    filtered = list(handler.filter_by_quality(data, min_phred=0))
    assert len(filtered) > 0

def test_metrics_edge_cases(test_data_dir):
    """Test quality metrics with edge cases"""
    handler = GenomicFileHandler()
    
    # Test with empty BAM file
    empty_bam = test_data_dir / "empty.bam"
    header = {'HD': {'VN': '1.0'}, 'SQ': [{'LN': 1000, 'SN': 'chr1'}]}
    with pysam.AlignmentFile(str(empty_bam), "wb", header=header) as _:
        pass
    
    data = handler.load_file(str(empty_bam), "BAM")
    metrics = handler.analyze_quality_metrics(data)
    assert metrics.coverage_depth == 0
    assert metrics.gc_content == 0
    assert metrics.read_length == 0 