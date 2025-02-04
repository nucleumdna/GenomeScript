from typing import List, Dict, Tuple
import numpy as np
import tensorflow as tf
from tensorflow import keras
from Bio import SeqIO
from dataclasses import dataclass

@dataclass
class VariantImpact:
    severity_score: float
    confidence: float
    affected_regions: List[str]
    clinical_significance: str

class VariantPredictor:
    def __init__(self, model_path: str = None):
        self.sequence_length = 1000  # Context window size
        self.model = self._create_model() if not model_path else self.load_model(model_path)
        
    def _create_model(self) -> keras.Model:
        """Create deep learning model for variant impact prediction"""
        model = keras.Sequential([
            # CNN layers for sequence feature extraction
            keras.layers.Conv1D(64, 3, activation='relu', input_shape=(self.sequence_length, 4)),
            keras.layers.MaxPooling1D(2),
            keras.layers.Conv1D(128, 3, activation='relu'),
            keras.layers.MaxPooling1D(2),
            
            # Attention mechanism for important regions
            keras.layers.MultiHeadAttention(num_heads=8, key_dim=64),
            keras.layers.GlobalAveragePooling1D(),
            
            # Dense layers for prediction
            keras.layers.Dense(256, activation='relu'),
            keras.layers.Dropout(0.5),
            keras.layers.Dense(128, activation='relu'),
            keras.layers.Dense(4, activation='softmax')  # Multi-class prediction
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        return model

    def preprocess_sequence(self, sequence: str) -> np.ndarray:
        """Convert DNA sequence to one-hot encoding"""
        mapping = {'A': [1,0,0,0], 'T': [0,1,0,0], 
                  'G': [0,0,1,0], 'C': [0,0,0,1]}
        encoded = np.array([mapping.get(base, [0,0,0,0]) for base in sequence])
        return encoded

    def train(self, sequences: List[str], labels: List[int], 
             validation_split: float = 0.2):
        """Train the model on genomic data"""
        X = np.array([self.preprocess_sequence(seq) for seq in sequences])
        y = keras.utils.to_categorical(labels)
        
        self.model.fit(
            X, y,
            epochs=50,
            batch_size=32,
            validation_split=validation_split,
            callbacks=[
                keras.callbacks.EarlyStopping(patience=5),
                keras.callbacks.ModelCheckpoint('best_model.h5')
            ]
        )

    def predict_impact(self, variant_sequence: str) -> VariantImpact:
        """Predict the impact of a variant"""
        X = self.preprocess_sequence(variant_sequence)
        X = np.expand_dims(X, axis=0)
        
        predictions = self.model.predict(X)
        severity_score = float(predictions[0][0])
        
        # Get attention weights for interpretability
        attention_weights = self.model.layers[4].get_weights()
        affected_regions = self._identify_affected_regions(attention_weights[0])
        
        return VariantImpact(
            severity_score=severity_score,
            confidence=float(np.max(predictions)),
            affected_regions=affected_regions,
            clinical_significance=self._get_clinical_significance(severity_score)
        )

    def _identify_affected_regions(self, attention_weights: np.ndarray) -> List[str]:
        """Identify genomic regions most affected by the variant"""
        top_k = 3
        top_indices = np.argsort(attention_weights.mean(axis=1))[-top_k:]
        return [f"Region_{i}" for i in top_indices]

    def _get_clinical_significance(self, severity_score: float) -> str:
        """Map severity score to clinical significance"""
        if severity_score > 0.8:
            return "Pathogenic"
        elif severity_score > 0.6:
            return "Likely Pathogenic"
        elif severity_score > 0.4:
            return "Uncertain Significance"
        elif severity_score > 0.2:
            return "Likely Benign"
        else:
            return "Benign" 