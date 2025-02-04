import pytest
from src.compiler.lexer import Lexer, TokenType
from src.compiler.parser import Parser
from src.vm.optimized_vm import OptimizedGenomeVM

def test_basic_genomescript():
    """Test basic GenomeScript functionality"""
    script = """
    LOAD FASTA "test.fa" -> genome
    ANALYZE genome COUNT_GC -> gc_content
    """
    
    lexer = Lexer(script)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    vm = OptimizedGenomeVM()
    result = vm.execute(ast)
    
    assert result is not None

@pytest.fixture
def sample_fasta(tmp_path):
    """Create a sample FASTA file for testing"""
    fasta_content = ">test\nATGCGCTAGC\n"
    fasta_file = tmp_path / "test.fa"
    fasta_file.write_text(fasta_content)
    return str(fasta_file) 