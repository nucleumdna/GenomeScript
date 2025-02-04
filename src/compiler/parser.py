from dataclasses import dataclass
from typing import List, Optional
from .lexer import Token, TokenType

@dataclass
class ASTNode:
    pass

@dataclass
class LoadNode(ASTNode):
    file_type: str
    file_path: str
    variable_name: str

@dataclass
class AnalyzeNode(ASTNode):
    target: str
    operation: str
    parameters: List[str]

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
        file_type = self._consume(TokenType.IDENTIFIER).value
        file_path = self._consume(TokenType.STRING).value
        self._consume(TokenType.ARROW)
        variable_name = self._consume(TokenType.IDENTIFIER).value
        return LoadNode(file_type, file_path, variable_name)

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