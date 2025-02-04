# AI API Reference

## Variant Predictor

::: src.ai.variant_predictor.VariantPredictor
    handler: python
    selection:
      members:
        - predict_impact
        - train
        - preprocess_sequence
        - _create_model
        - _identify_affected_regions

## Data Preprocessor

::: src.ai.data_preprocessor.GenomicDataPreprocessor
    handler: python
    selection:
      members:
        - prepare_training_data
        - _get_sequence_context
        - _apply_variant
        - _get_label

## Model Types

### VariantImpact

::: src.ai.variant_predictor.VariantImpact
    handler: python

### Model Architecture

The default model architecture consists of:

```python
model = keras.Sequential([
    # CNN layers for sequence feature extraction
    keras.layers.Conv1D(64, 3, activation='relu'),
    keras.layers.MaxPooling1D(2),
    keras.layers.Conv1D(128, 3, activation='relu'),
    
    # Attention mechanism
    keras.layers.MultiHeadAttention(num_heads=8, key_dim=64),
    keras.layers.GlobalAveragePooling1D(),
    
    # Dense layers
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dense(4, activation='softmax')
])
```

### Training Configuration

Default training parameters:
- Batch size: 32
- Learning rate: 0.001
- Optimizer: Adam
- Loss function: Categorical crossentropy
- Early stopping patience: 5 