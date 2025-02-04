from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional

class TokenType(Enum):
    # Keywords
    LOAD = auto()
    ANALYZE = auto()
    FILTER = auto()
    EXPORT = auto()
    TRAIN = auto()
    PREDICT = auto()
    MODEL = auto()
    GENERATE = auto()
    VERIFY = auto()
    
    # File types
    FASTA = auto()
    VCF = auto()
    BAM = auto()
    
    # Operators
    ARROW = auto()
    
    # Literals
    STRING = auto()
    NUMBER = auto()
    IDENTIFIER = auto()
    
    # Special
    EOF = auto()

@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.current_char = self.source[0] if source else None

    def error(self, message: str):
        raise SyntaxError(f"Line {self.line}, column {self.column}: {message}")

    def advance(self):
        """Move to next character"""
        self.pos += 1
        self.column += 1
        self.current_char = self.source[self.pos] if self.pos < len(self.source) else None

    def peek(self) -> Optional[str]:
        """Look at next character without advancing"""
        peek_pos = self.pos + 1
        return self.source[peek_pos] if peek_pos < len(self.source) else None

    def skip_whitespace(self):
        """Skip whitespace characters"""
        while self.current_char and self.current_char.isspace():
            if self.current_char == '\n':
                self.line += 1
                self.column = 1
            self.advance()

    def skip_comment(self):
        """Skip single-line comments"""
        while self.current_char and self.current_char != '\n':
            self.advance()
        if self.current_char == '\n':
            self.line += 1
            self.column = 1
            self.advance()

    def _string(self) -> Token:
        """Handle string literals"""
        start_column = self.column
        result = ''
        
        # Skip the opening quote
        self.advance()

        while self.current_char and self.current_char != '"':
            result += self.current_char
            self.advance()

        if not self.current_char:
            self.error("Unterminated string literal")

        # Skip the closing quote
        self.advance()
        return Token(TokenType.STRING, result, self.line, start_column + 1)

    def _identifier(self) -> Token:
        """Handle identifiers and keywords"""
        result = ''
        start_column = self.column

        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()

        # Check for keywords
        token_type = {
            'LOAD': TokenType.LOAD,
            'ANALYZE': TokenType.ANALYZE,
            'FILTER': TokenType.FILTER,
            'EXPORT': TokenType.EXPORT,
            'TRAIN': TokenType.TRAIN,
            'PREDICT': TokenType.PREDICT,
            'MODEL': TokenType.MODEL,
            'GENERATE': TokenType.GENERATE,
            'VERIFY': TokenType.VERIFY,
            'FASTA': TokenType.FASTA,
            'VCF': TokenType.VCF,
            'BAM': TokenType.BAM,
        }.get(result, TokenType.IDENTIFIER)

        return Token(token_type, result, self.line, start_column)

    def tokenize(self) -> List[Token]:
        """Convert source code into tokens"""
        tokens = []

        while self.current_char:
            # Handle comments
            if self.current_char == '#':
                self.skip_comment()
                continue

            # Handle whitespace
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            # Handle strings
            if self.current_char == '"':
                tokens.append(self._string())
                continue

            # Handle arrow operator
            if self.current_char == '-' and self.peek() == '>':
                start_column = self.column
                self.advance()  # Skip '-'
                self.advance()  # Skip '>'
                tokens.append(Token(TokenType.ARROW, "->", self.line, start_column))
                continue

            # Handle identifiers and keywords
            if self.current_char.isalpha():
                tokens.append(self._identifier())
                continue

            self.error(f"Invalid character: {self.current_char}")

        # Add EOF token
        tokens.append(Token(TokenType.EOF, "EOF", self.line, self.column))
        return tokens 