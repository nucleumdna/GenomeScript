from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class ASTNode:
    pass

@dataclass
class LoadNode(ASTNode):
    file_type: str
    file_path: str
    variable_name: str
    quality_filter: Optional[Dict] = None

@dataclass
class AnalyzeNode(ASTNode):
    target: str
    operation: str
    parameters: List[str]
    output: str

@dataclass
class FilterNode(ASTNode):
    target: str
    condition: str
    output: str

@dataclass
class ExportNode(ASTNode):
    source: str
    file_path: str
    format: Optional[str] = None 