import pytest
from src.compiler.lexer import Lexer, TokenType, Token

def test_basic_tokenization():
    """Test basic tokenization of GenomeScript code"""
    source = 'LOAD FASTA "test.fa" -> genome'
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    expected = [
        Token(TokenType.LOAD, "LOAD", 1, 1),
        Token(TokenType.FASTA, "FASTA", 1, 6),
        Token(TokenType.STRING, "test.fa", 1, 12),
        Token(TokenType.ARROW, "->", 1, 21),
        Token(TokenType.IDENTIFIER, "genome", 1, 24),
        Token(TokenType.EOF, "EOF", 1, 30)
    ]
    
    assert len(tokens) == len(expected)
    for actual, expected in zip(tokens, expected):
        assert actual.type == expected.type
        assert actual.value == expected.value

def test_ai_related_tokens():
    """Test tokenization of AI-related commands"""
    source = """
    TRAIN MODEL ON variants WITH reference -> trained_model
    PREDICT IMPACT variants[0] USING trained_model -> prediction
    """
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    assert any(t.type == TokenType.TRAIN for t in tokens)
    assert any(t.type == TokenType.MODEL for t in tokens)
    assert any(t.type == TokenType.PREDICT for t in tokens)
    assert any(t.type == TokenType.IMPACT for t in tokens)

def test_blockchain_tokens():
    """Test tokenization of blockchain-related commands"""
    source = """
    GENERATE PROOF genome "QUERY variant_rs123" -> proof
    VERIFY proof -> is_valid
    SUBMIT proof TO ETHEREUM
    """
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    # Verify blockchain-specific tokens are recognized
    token_types = [t.type for t in tokens]
    assert TokenType.GENERATE in token_types
    assert TokenType.PROOF in token_types
    assert TokenType.VERIFY in token_types
    assert TokenType.SUBMIT in token_types

def test_error_handling():
    """Test lexer error handling"""
    # Test unterminated string
    with pytest.raises(SyntaxError):
        source = 'LOAD FASTA "unterminated'
        lexer = Lexer(source)
        lexer.tokenize()
    
    # Test invalid operator
    with pytest.raises(SyntaxError):
        source = 'LOAD FASTA @ genome'
        lexer = Lexer(source)
        lexer.tokenize() 