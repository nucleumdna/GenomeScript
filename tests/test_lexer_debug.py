import pytest
from src.compiler.lexer import Lexer, TokenType, Token

def test_basic_load_command():
    """Test basic LOAD FASTA command"""
    source = 'LOAD FASTA "test.fa" -> genome'
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    expected = [
        Token(TokenType.LOAD, "LOAD", 1, 1),
        Token(TokenType.FASTA, "FASTA", 1, 6),
        Token(TokenType.STRING, "test.fa", 1, 13),
        Token(TokenType.ARROW, "->", 1, 22),
        Token(TokenType.IDENTIFIER, "genome", 1, 25),
        Token(TokenType.EOF, "EOF", 1, 31)
    ]

    print("\nTokens received:")
    for token in tokens:
        print(f"  {token}")
    
    print("\nTokens expected:")
    for token in expected:
        print(f"  {token}")

    assert len(tokens) == len(expected)
    for actual, expected in zip(tokens, expected):
        assert actual.type == expected.type
        assert actual.value == expected.value
        assert actual.line == expected.line
        assert actual.column == expected.column

def test_multiline_script():
    """Test multiline GenomeScript code"""
    source = """
    LOAD FASTA "reference.fa" -> genome
    ANALYZE genome COUNT_GC -> gc_content
    FILTER genome WHERE "length > 1000" -> long_sequences
    """
    
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    print("\nMultiline tokens:")
    for token in tokens:
        print(f"Line {token.line}, Col {token.column}: {token.type} = '{token.value}'")

    # Verify specific tokens
    assert any(t.type == TokenType.LOAD for t in tokens)
    assert any(t.type == TokenType.ANALYZE for t in tokens)
    assert any(t.type == TokenType.FILTER for t in tokens)

def test_error_handling():
    """Test lexer error handling with invalid inputs"""
    invalid_inputs = [
        ('LOAD FASTA "unterminated', "Unterminated string"),
        ('LOAD FASTA @ genome', "Invalid character"),
        ('LOAD FASTA "test.fa" --> genome', "Invalid operator")
    ]

    for source, error_type in invalid_inputs:
        print(f"\nTesting invalid input: {source}")
        try:
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            print("Unexpected success! Tokens:", tokens)
            assert False, f"Expected {error_type} error"
        except SyntaxError as e:
            print(f"Caught expected error: {str(e)}")
            assert True

if __name__ == '__main__':
    print("Running lexer debug tests...")
    test_basic_load_command()
    test_multiline_script()
    test_error_handling()
    print("\nAll debug tests completed.") 