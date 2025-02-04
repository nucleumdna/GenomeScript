#!/usr/bin/env python3
from src.compiler.lexer import Lexer, TokenType

def debug_lexer():
    print("GenomeScript Lexer Debug Tool")
    print("Enter 'exit' to quit\n")

    while True:
        try:
            source = input("Enter GenomeScript code: ")
            if source.lower() == 'exit':
                break

            lexer = Lexer(source)
            tokens = lexer.tokenize()

            print("\nTokens:")
            for token in tokens:
                if token.type != TokenType.EOF:
                    print(f"Line {token.line}, Col {token.column}: "
                          f"{token.type.name} = '{token.value}'")

        except SyntaxError as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
        print()

if __name__ == '__main__':
    debug_lexer() 