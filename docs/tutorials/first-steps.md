# First Steps with GenomeScript

## Introduction

This tutorial will guide you through your first GenomeScript program.

### Basic Commands

1. Loading Data:
```
LOAD FASTA "reference.fa" -> genome
```

2. Simple Analysis:
```
ANALYZE genome COUNT_GC -> gc_content
```

3. Filtering Data:
```
FILTER genome WHERE "length > 1000" -> long_sequences
```

### Try It Yourself

1. Open the GenomeScript editor at http://localhost:3000
2. Enter the following code:
```
# My first GenomeScript program
LOAD FASTA "example.fa" -> my_genome
ANALYZE my_genome COUNT_GC -> results
```
3. Click "Analyze" to see the tokenization results 