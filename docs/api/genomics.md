# Genomics API Reference

## GenomicFileHandler

::: src.genomics.file_handler.GenomicFileHandler
    handler: python
    selection:
      members:
        - load_file
        - filter_by_quality
        - analyze_quality_metrics

## VariantPredictor

::: src.ai.variant_predictor.VariantPredictor
    handler: python
    selection:
      members:
        - predict_impact
        - train
        - preprocess_sequence

## GenomicZKP

::: src.zkp.genomic_proof.GenomicZKP
    handler: python
    selection:
      members:
        - generate_proof
        - verify_proof 