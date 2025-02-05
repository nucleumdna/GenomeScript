import pytest
from src.zkp.genomic_proof import GenomicProof
from src.genomics.file_handler import GenomicFileHandler

@pytest.fixture
def genomic_proof():
    return GenomicProof(
        proof={},
        public_signals=[],
        verification_key={}
    )

@pytest.fixture
def file_handler():
    return GenomicFileHandler() 