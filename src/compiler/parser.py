from dataclasses import dataclass
from typing import List, Optional
from .lexer import Token, TokenType

@dataclass
class ASTNode:
    pass

@dataclass
class LoadNode(ASTNode):
    format: str
    file_path: str
    target: str

@dataclass
class AnalyzeNode(ASTNode):
    target: str
    operation: str
    parameters: List[str]

@dataclass
class FilterNode(ASTNode):
    target: str
    condition: str
    output: str

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> List[ASTNode]:
        nodes = []
        while not self._is_at_end():
            nodes.append(self._parse_statement())
        return nodes

    def _parse_statement(self) -> ASTNode:
        token = self._peek()
        if token.type == TokenType.LOAD:
            return self._parse_load()
        elif token.type == TokenType.ANALYZE:
            return self._parse_analyze()
        else:
            raise SyntaxError(f"Unexpected token {token.type} at line {token.line}")

    def _parse_load(self) -> LoadNode:
        self._advance()  # Consume LOAD
        format_token = self._consume(TokenType.IDENTIFIER)
        file_token = self._consume(TokenType.STRING)
        self._consume(TokenType.ARROW)
        target_token = self._consume(TokenType.IDENTIFIER)
        return LoadNode(
            format=format_token.value,
            file_path=file_token.value.strip('"'),
            target=target_token.value
        )

    def _is_at_end(self) -> bool:
        return self._peek().type == TokenType.EOF

    def _peek(self) -> Token:
        return self.tokens[self.current]

    def _advance(self) -> Token:
        if not self._is_at_end():
            self.current += 1
        return self.tokens[self.current - 1]

    def _consume(self, token_type: TokenType) -> Token:
        if self._peek().type == token_type:
            return self._advance()
        raise SyntaxError(
            f"Expected {token_type.value} but got {self._peek().type.value} at line {self._peek().line}"
        )

    def _parse_analyze(self) -> AnalyzeNode:
        self._advance()  # Consume ANALYZE
        target = self._consume(TokenType.IDENTIFIER).value
        operation = self._consume(TokenType.IDENTIFIER).value
        parameters = []
        
        while not self._is_at_end() and self._peek().type != TokenType.EOF:
            if self._peek().type == TokenType.IDENTIFIER:
                parameters.append(self._advance().value)
            else:
                break
                
        return AnalyzeNode(target, operation, parameters) 