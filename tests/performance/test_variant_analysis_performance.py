import pytest
import time
from src.genomics.file_handler import GenomicFileHandler

@pytest.fixture
def large_variant_set():
    """Generate a large set of test variants"""
    return [
        {
            'QUAL': float(qual),
            'DP': int(qual/2),
            'REF': 'A',
            'ALT': 'T',
            'POS': pos,
            'FILTER': 'PASS' if qual >= 30 else 'LOW_QUAL'
        }
        for pos, qual in enumerate(range(20, 60, 2))
    ]

def test_analysis_performance(large_variant_set):
    """Test performance of variant analysis"""
    handler = GenomicFileHandler()
    
    start_time = time.time()
    filtered = handler.analyze_variants(large_variant_set)
    end_time = time.time()
    
    processing_time = end_time - start_time
    
    # Performance assertions
    assert processing_time < 1.0  # Should process in under 1 second
    assert len(filtered) > 0
    assert all('predicted_impact' in v for v in filtered)

def test_parallel_processing_performance(large_variant_set):
    """Test performance with parallel processing"""
    handler = GenomicFileHandler()
    
    # Process in chunks
    chunk_size = 5
    chunks = [large_variant_set[i:i + chunk_size] 
             for i in range(0, len(large_variant_set), chunk_size)]
    
    start_time = time.time()
    results = []
    for chunk in chunks:
        results.extend(handler.analyze_variants(chunk))
    end_time = time.time()
    
    processing_time = end_time - start_time
    assert processing_time < 2.0  # Should process all chunks in under 2 seconds 