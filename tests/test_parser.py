import pytest
from src.compiler.lexer import Lexer
from src.compiler.parser import Parser, LoadNode, AnalyzeNode, FilterNode

def test_basic_parsing():
    """Test basic parsing of GenomeScript code"""
    source = """
    LOAD FASTA "reference.fa" -> genome
    ANALYZE genome COUNT_GC -> gc_content
    FILTER variants WHERE "QUAL >= 30" -> high_quality
    """
    
    lexer = Lexer(source)
    parser = Parser(lexer.tokenize())
    ast = parser.parse()
    
    assert len(ast) == 3
    assert isinstance(ast[0], LoadNode)
    assert isinstance(ast[1], AnalyzeNode)
    assert isinstance(ast[2], FilterNode)

def test_ai_model_parsing():
    """Test parsing of AI-related commands"""
    source = """
    TRAIN MODEL ON variants WITH reference -> model
    PREDICT IMPACT variants USING model -> predictions
    """
    
    lexer = Lexer(source)
    parser = Parser(lexer.tokenize())
    ast = parser.parse()
    
    assert len(ast) == 2
    assert ast[0].operation == "TRAIN"
    assert ast[1].operation == "PREDICT"

def test_blockchain_parsing():
    """Test parsing of blockchain operations"""
    source = """
    GENERATE PROOF genome "QUERY variant_rs123" -> proof
    VERIFY proof -> is_valid
    SUBMIT proof TO ETHEREUM
    """
    
    lexer = Lexer(source)
    parser = Parser(lexer.tokenize())
    ast = parser.parse()
    
    assert len(ast) == 3
    assert hasattr(ast[0], 'proof_type')
    assert hasattr(ast[1], 'verification_target')

def test_error_recovery():
    """Test parser error recovery"""
    source = """
    LOAD FASTA "valid.fa" -> genome
    INVALID COMMAND
    ANALYZE genome COUNT_GC -> result
    """
    
    lexer = Lexer(source)
    parser = Parser(lexer.tokenize())
    
    with pytest.raises(SyntaxError):
        parser.parse() 