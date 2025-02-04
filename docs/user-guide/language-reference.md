# Language Reference

## Basic Syntax

GenomeScript uses a simple, readable syntax designed for genomic analysis. Each statement typically follows this pattern:

```genescript
OPERATION [TYPE] "input" [OPTIONS] -> output
```

## Keywords

### Data Loading
- `LOAD`: Load genomic data from a file
- `EXPORT`: Export data to a file
- `ANALYZE`: Perform analysis on data
- `FILTER`: Filter genomic data based on conditions

### AI Operations
- `TRAIN`: Train an AI model
- `PREDICT`: Make predictions using a trained model
- `MODEL`: Specify model operations

### Blockchain Operations
- `GENERATE`: Generate proofs or other data
- `VERIFY`: Verify proofs
- `SUBMIT`: Submit data to blockchain

## Data Types

### File Formats
- `FASTA`: Reference sequences
- `VCF`: Variant data
- `BAM`: Aligned reads
- `SAM`: Sequence alignment
- `CRAM`: Compressed alignment

### Variables
Variables are created using the arrow operator (`->`):
```genescript
LOAD FASTA "reference.fa" -> genome
```

## Examples

### Basic Analysis
```genescript
# Load reference genome
LOAD FASTA "reference.fa" -> genome

# Analyze GC content
ANALYZE genome COUNT_GC -> gc_content

# Export results
EXPORT gc_content TO "results.txt"
```

### AI Analysis
```genescript
# Train model
TRAIN MODEL ON variants WITH reference -> model

# Make predictions
PREDICT IMPACT variants USING model -> predictions
```

### Blockchain Operations
```genescript
# Generate and verify proof
GENERATE PROOF genome "QUERY variant_rs123" -> proof
VERIFY proof -> is_valid
``` 