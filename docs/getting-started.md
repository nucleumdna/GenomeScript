# Getting Started with GenomeScript

## Introduction
GenomeScript is a domain-specific language designed for genomic data analysis. This guide will help you get started with the basic concepts and usage.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/genomescript.git
cd genomescript
```

2. Set up the environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Basic Usage

### Web Interface
1. Start the development servers:
```bash
./scripts/start-dev.sh
```

2. Open http://localhost:3000 in your browser
3. Enter GenomeScript commands in the editor

### Example Commands
```
# Load genomic data
LOAD FASTA "reference.fa" -> genome
LOAD VCF "variants.vcf" -> variants

# Analyze sequences
ANALYZE genome COUNT_GC -> gc_content
FILTER variants WHERE "QUAL >= 30" -> high_quality
```

## Next Steps
- Check out the [API Reference](./api/index.md)
- Try the [Tutorials](./tutorials/index.md)
- Learn about [Security](./security/index.md) 