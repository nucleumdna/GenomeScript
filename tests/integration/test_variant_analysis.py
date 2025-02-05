import pytest
from src.genomics.file_handler import GenomicFileHandler
from src.ai.variant_analyzer import VariantAnalyzer

@pytest.fixture
def setup_analysis_environment(tmp_path):
    """Set up test environment with sample VCF data"""
    vcf_content = """##fileformat=VCFv4.2
#CHROM  POS ID  REF ALT QUAL    FILTER  INFO    FORMAT  SAMPLE
chr1    1000    rs1 A   T   40  PASS    DP=25   GT  0/1
chr1    2000    rs2 G   C   15  LOW_QUAL    DP=8    GT  0/1
"""
    vcf_file = tmp_path / "test.vcf"
    vcf_file.write_text(vcf_content)
    return str(vcf_file)

def test_end_to_end_variant_analysis(setup_analysis_environment):
    """Test complete variant analysis pipeline"""
    # Initialize components
    file_handler = GenomicFileHandler()
    
    # Load and analyze variants
    variants = [
        {'QUAL': 40.0, 'DP': 25, 'REF': 'A', 'ALT': 'T'},
        {'QUAL': 15.0, 'DP': 8, 'REF': 'G', 'ALT': 'C'}
    ]
    
    # Perform analysis
    filtered_variants = file_handler.analyze_variants(variants)
    
    # Verify results
    assert len(filtered_variants) == 1
    assert filtered_variants[0]['predicted_impact'].score > 0
    assert filtered_variants[0]['predicted_impact'].confidence > 0
    assert len(filtered_variants[0]['predicted_impact'].supporting_evidence) > 0

def test_analysis_with_custom_thresholds(setup_analysis_environment):
    """Test variant analysis with custom configuration"""
    file_handler = GenomicFileHandler()
    analyzer = VariantAnalyzer(model_config={
        'score_threshold': 0.3,
        'confidence_threshold': 0.5
    })
    file_handler.variant_analyzer = analyzer
    
    variants = [
        {'QUAL': 35.0, 'DP': 15, 'REF': 'A', 'ALT': 'T'}
    ]
    
    filtered = file_handler.analyze_variants(variants, quality_threshold=20.0)
    assert len(filtered) == 1
    assert filtered[0]['predicted_impact'].confidence >= 0.5 