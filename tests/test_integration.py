import pytest
from src.compiler.lexer import Lexer
from src.compiler.parser import Parser
from src.vm.optimized_vm import OptimizedGenomeVM
from src.genomics.file_handler import GenomicFileHandler
from src.ai.variant_predictor import VariantPredictor

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