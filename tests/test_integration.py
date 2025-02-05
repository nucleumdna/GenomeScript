import pytest
from src.compiler.lexer import Lexer
from src.compiler.parser import Parser
from src.vm.optimized_vm import OptimizedGenomeVM
from src.genomics.file_handler import GenomicFileHandler
from src.ai.variant_predictor import VariantPredictor
from src.vm.genome_vm import GenomeVM

@pytest.fixture
def setup_environment(tmp_path):
    """Set up test environment with sample files"""
    # Create sample FASTA
    fasta_content = ">test\nATGCGCTAGC\n"
    fasta_file = tmp_path / "test.fa"
    fasta_file.write_text(fasta_content)
    
    # Create sample VCF
    vcf_content = """##fileformat=VCFv4.2
#CHROM  POS ID  REF ALT QUAL    FILTER  INFO
chr1    100 rs1 A   T   30  PASS    DP=50
"""
    vcf_file = tmp_path / "test.vcf"
    vcf_file.write_text(vcf_content)
    
    return {"fasta": str(fasta_file), "vcf": str(vcf_file)}

def test_full_pipeline(setup_environment):
    """Test complete genomic analysis pipeline"""
    script = f"""
    LOAD FASTA "{setup_environment['fasta']}" -> genome
    LOAD VCF "{setup_environment['vcf']}" -> variants
    
    # Basic analysis
    ANALYZE genome COUNT_GC -> gc_content
    
    # AI prediction
    PREDICT IMPACT variants -> predictions
    
    # Generate proof
    GENERATE PROOF genome "QUERY variant_rs1" -> proof
    VERIFY proof -> is_valid
    """
    
    # Execute pipeline
    lexer = Lexer(script)
    parser = Parser(lexer.tokenize())
    vm = OptimizedGenomeVM()
    
    result = vm.execute(parser.parse())
    
    # Verify results
    assert 'gc_content' in vm.variables
    assert 'predictions' in vm.variables
    assert 'is_valid' in vm.variables

def test_error_scenarios(setup_environment):
    """Test error handling in full pipeline"""
    scripts = [
        # Missing file
        """
        LOAD FASTA "nonexistent.fa" -> genome
        """,
        
        # Invalid analysis
        f"""
        LOAD FASTA "{setup_environment['fasta']}" -> genome
        ANALYZE genome INVALID_OPERATION -> result
        """,
        
        # Invalid proof generation
        f"""
        LOAD FASTA "{setup_environment['fasta']}" -> genome
        GENERATE PROOF genome "INVALID_QUERY" -> proof
        """
    ]
    
    vm = OptimizedGenomeVM()
    
    for script in scripts:
        lexer = Lexer(script)
        parser = Parser(lexer.tokenize())
        ast = parser.parse()
        
        with pytest.raises(Exception):
            vm.execute(ast)

def test_load_bam_file(sample_bam):
    """Test loading BAM file in GenomeScript"""
    script = f"""
    LOAD BAM "{sample_bam}" -> alignments
    """
    
    lexer = Lexer(script)
    parser = Parser(lexer.tokenize())
    vm = GenomeVM()
    
    # Execute
    vm.execute(parser.parse())
    
    # Verify
    assert 'alignments' in vm.variables
    assert len(vm.variables['alignments']) > 0
    assert vm.variables['alignments'][0]['query_name'] == 'read1'

def test_load_multiple_formats(sample_bam, sample_sff):
    """Test loading multiple file formats"""
    script = f"""
    LOAD BAM "{sample_bam}" -> alignments
    LOAD SFF "{sample_sff}" -> flowgrams
    """
    
    lexer = Lexer(script)
    parser = Parser(lexer.tokenize())
    vm = GenomeVM()
    
    # Execute
    vm.execute(parser.parse())
    
    # Verify both loaded correctly
    assert 'alignments' in vm.variables
    assert 'flowgrams' in vm.variables 

@pytest.fixture
def test_script(sample_bam, sample_cram, sample_sff, sample_csfasta):
    """Create a test script using all formats"""
    return f"""
    # Load different file formats
    LOAD BAM "{sample_bam}" -> alignments
    LOAD CRAM "{sample_cram}" -> cram_data
    LOAD SFF "{sample_sff}" -> flowgrams
    LOAD CSFASTA "{sample_csfasta}" -> color_seqs
    
    # Analyze the data
    ANALYZE alignments QUALITY -> alignment_quality
    """

def test_format_integration(test_script):
    """Test integration of all file formats"""
    lexer = Lexer(test_script)
    parser = Parser(lexer.tokenize())
    vm = GenomeVM()
    
    # Execute
    vm.execute(parser.parse())
    
    # Verify all data was loaded
    assert 'alignments' in vm.variables
    assert 'cram_data' in vm.variables
    assert 'flowgrams' in vm.variables
    assert 'color_seqs' in vm.variables
    
    # Verify data content
    assert len(vm.variables['alignments']) > 0
    assert len(vm.variables['flowgrams']) > 0
    assert len(vm.variables['color_seqs']) > 0

def test_load_formats(sample_bam, sample_sff, sample_csfasta):
    """Test loading different file formats"""
    script = f"""
    LOAD BAM "{sample_bam}" -> alignments
    LOAD SFF "{sample_sff}" -> flowgrams
    LOAD CSFASTA "{sample_csfasta}" -> color_seqs
    """
    
    lexer = Lexer(script)
    parser = Parser(lexer.tokenize())
    vm = GenomeVM()
    
    # Execute
    vm.execute(parser.parse())
    
    # Verify data was loaded
    assert 'alignments' in vm.variables
    assert 'flowgrams' in vm.variables
    assert 'color_seqs' in vm.variables
    
    # Verify content
    assert len(vm.variables['alignments']) > 0
    assert len(vm.variables['flowgrams']) > 0
    assert len(vm.variables['color_seqs']) > 0

def test_error_handling():
    """Test error handling for invalid formats"""
    script = """
    LOAD INVALID "test.txt" -> data
    """
    
    lexer = Lexer(script)
    parser = Parser(lexer.tokenize())
    vm = GenomeVM()
    
    with pytest.raises(ValueError) as exc:
        vm.execute(parser.parse())
    assert "Unsupported file format" in str(exc.value) 