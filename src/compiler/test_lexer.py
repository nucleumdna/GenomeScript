from .lexer import Lexer

def test_script(filename: str):
    """Test lexer with a GenomeScript file"""
    print(f"\nTesting script: {filename}")
    print("-" * 50)
    
    with open(filename, 'r') as f:
        source = f.read()
    
    print("Source code:")
    print(source)
    print("\nTokens:")
    
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    for token in tokens:
        if token.type.name != 'EOF':
            print(f"Line {token.line}, Col {token.column}: {token.type.name} = '{token.value}'")

if __name__ == '__main__':
    test_script('test_script.gns') 