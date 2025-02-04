import pytest
from src.compiler.lexer import Lexer
from src.compiler.parser import Parser
from src.vm.optimized_vm import OptimizedGenomeVM

@pytest.fixture
def vm():
    return OptimizedGenomeVM()

def test_basic_execution(vm, sample_fasta):
    """Test basic genomic operations"""
    script = f"""
    LOAD FASTA "{sample_fasta}" -> genome
    ANALYZE genome COUNT_GC -> gc_content
    """
    
    lexer = Lexer(script)
    parser = Parser(lexer.tokenize())
    ast = parser.parse()
    
    result = vm.execute(ast)
    assert 'gc_content' in vm.variables
    assert isinstance(vm.variables['gc_content'], float)

def test_parallel_processing(vm, sample_fasta):
    """Test parallel processing capabilities"""
    script = f"""
    LOAD FASTA "{sample_fasta}" -> genome
    FILTER genome WHERE "length > 1000" -> long_sequences
    """
    
    lexer = Lexer(script)
    parser = Parser(lexer.tokenize())
    ast = parser.parse()
    
    result = vm.execute(ast)
    assert vm.variables['long_sequences'] is not None

def test_ai_operations(vm, sample_fasta):
    """Test AI model operations"""
    script = """
    TRAIN MODEL ON variants WITH reference -> model
    PREDICT IMPACT variants USING model -> predictions
    """
    
    lexer = Lexer(script)
    parser = Parser(lexer.tokenize())
    ast = parser.parse()
    
    result = vm.execute(ast)
    assert 'predictions' in vm.variables

def test_blockchain_operations(vm):
    """Test blockchain integration"""
    script = """
    GENERATE PROOF genome "QUERY variant_rs123" -> proof
    VERIFY proof -> is_valid
    """
    
    lexer = Lexer(script)
    parser = Parser(lexer.tokenize())
    ast = parser.parse()
    
    result = vm.execute(ast)
    assert 'is_valid' in vm.variables
    assert isinstance(vm.variables['is_valid'], bool)

def test_error_handling(vm):
    """Test VM error handling"""
    # Test undefined variable
    script = """
    ANALYZE undefined_genome COUNT_GC -> result
    """
    
    lexer = Lexer(script)
    parser = Parser(lexer.tokenize())
    ast = parser.parse()
    
    with pytest.raises(RuntimeError):
        vm.execute(ast) 