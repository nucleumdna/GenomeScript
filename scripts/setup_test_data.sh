#!/bin/bash

# Create test data directory
mkdir -p test_data

# Create sample FASTA file
cat > test_data/sample.fa << EOF
>chr1
ATGCATGCATGC
>chr2
GCATGCATGCAT
EOF

# Create sample VCF file
cat > test_data/variants.vcf << EOF
##fileformat=VCFv4.2
#CHROM  POS ID  REF ALT QUAL    FILTER  INFO
chr1    100 rs1 A   T   30  PASS    DP=50
chr1    200 rs2 G   C   40  PASS    DP=60
EOF 