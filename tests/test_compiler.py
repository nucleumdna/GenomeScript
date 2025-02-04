import pytest
from src.compiler.lexer import Lexer, TokenType
from src.compiler.parser import Parser, LoadNode
from src.compiler.bytecode import BytecodeGenerator
from src.vm.optimized_vm import OptimizedGenomeVM

def test_lexer():
    source = '''
    LOAD FASTA "sample.fa" -> genome
    ANALYZE genome COUNT_GC
    '''
    
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    assert tokens[0].type == TokenType.LOAD
    assert tokens[1].type == TokenType.FASTA
    assert tokens[2].type == TokenType.STRING
    assert tokens[2].value == "sample.fa"

def test_parser():
    source = 'LOAD FASTA "sample.fa" -> genome'
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    nodes = parser.parse()
    
    assert len(nodes) == 1
    assert isinstance(nodes[0], LoadNode)
    assert nodes[0].file_type == "FASTA"
    assert nodes[0].file_path == "sample.fa" 

def test_quality_filtering():
    source = '''
    LOAD BAM "sample.bam" QUALITY ABOVE 30 -> high_quality_reads
    ANALYZE high_quality_reads COVERAGE -> coverage_stats
    '''
    
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    nodes = parser.parse()
    
    assert len(nodes) == 2
    assert isinstance(nodes[0], LoadNode)
    assert nodes[0].quality_filter['min_phred'] == 30

def test_bytecode_generation():
    source = 'LOAD FASTA "genome.fa" -> ref'
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    nodes = parser.parse()
    
    generator = BytecodeGenerator()
    instructions = generator.generate(nodes)
    
    assert len(instructions) == 2
    assert instructions[0].opcode == OpCode.LOAD_FILE 