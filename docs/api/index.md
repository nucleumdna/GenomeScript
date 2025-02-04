# GenomeScript API Reference

## Language Components

### Commands

#### LOAD
Loads genomic data from files.
```
LOAD <format> <filename> -> <variable>
```

#### ANALYZE
Performs analysis on genomic data.
```
ANALYZE <variable> <operation> -> <result>
```

#### FILTER
Filters genomic data based on conditions.
```
FILTER <variable> WHERE <condition> -> <result>
```

### File Formats
- FASTA
- VCF
- BAM

### Operations
- COUNT_GC
- FIND_VARIANTS
- PREDICT_IMPACT

## REST API Endpoints

### POST /analyze
Analyzes GenomeScript code.

Request:
```json
{
  "code": "string"
}
```

Response:
```json
{
  "tokens": [
    {
      "type": "string",
      "value": "string",
      "line": 0,
      "column": 0
    }
  ]
}
``` 