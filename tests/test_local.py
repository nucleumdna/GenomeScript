import pytest
from pathlib import Path
from src.compiler.lexer import Lexer
from src.compiler.parser import Parser
from src.vm.optimized_vm import OptimizedGenomeVM

def test_local_setup(tmp_path):
    """Test local setup with sample files"""
    # Create test files
    fasta_content = ">test\nATGCGCTAGC\n"
    fasta_file = tmp_path / "test.fa"
    fasta_file.write_text(fasta_content)
    
    # Test basic script
    script = f"""
    LOAD FASTA "{fasta_file}" -> genome
    ANALYZE genome COUNT_GC -> gc_content
    """
    
    # Run through compiler pipeline
    lexer = Lexer(script)
    parser = Parser(lexer.tokenize())
    vm = OptimizedGenomeVM()
    
    # Execute
    result = vm.execute(parser.parse())
    
    # Verify results
    assert 'gc_content' in vm.variables
    assert isinstance(vm.variables['gc_content'], float) 