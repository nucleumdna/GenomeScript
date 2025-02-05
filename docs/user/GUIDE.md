# Genomics Module User Guide

## Quick Start

```python
from genomics import GenomicFileHandler

# Initialize handler
handler = GenomicFileHandler()

# Load and analyze BAM file
data = handler.load_file("sample.bam", "BAM")
metrics = handler.analyze_quality_metrics(data)

print(f"Coverage depth: {metrics.coverage_depth}x")
print(f"GC content: {metrics.gc_content * 100}%")
```

## File Operations

### Loading Files
```python
# Load different formats
bam_data = handler.load_file("sample.bam", "BAM")
cram_data = handler.load_file("sample.cram", "CRAM")
sff_data = handler.load_file("sample.sff", "SFF")
```

### Quality Filtering
```python
# Filter by quality score
filtered_data = handler.filter_by_quality(data, min_phred=30)

# Process filtered reads
for read in filtered_data:
    process_read(read)
```

### Quality Analysis
```python
metrics = handler.analyze_quality_metrics(data)

# Access metrics
print(f"Average read length: {metrics.read_length}")
print(f"Average coverage: {metrics.coverage_depth}x")
print(f"GC content: {metrics.gc_content * 100}%")
```

## Best Practices

1. Use caching for repeated access:
   ```python
   # First access loads and caches
   data1 = handler.load_file("large.bam", "BAM")
   # Second access uses cache
   data2 = handler.load_file("large.bam", "BAM")
   ```

2. Handle resources properly:
   ```python
   with handler.load_file("sample.bam", "BAM") as data:
       process_data(data)
   ```

3. Error handling:
   ```python
   try:
       data = handler.load_file("sample.bam", "BAM")
   except ValueError as e:
       print(f"Invalid format: {e}")
   except RuntimeError as e:
       print(f"Processing error: {e}")
   ``` 