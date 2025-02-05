import pytest
import numpy as np
from src.ai.variant_analyzer import VariantAnalyzer, VariantImpact

@pytest.fixture
def analyzer():
    """Create a VariantAnalyzer instance for testing."""
    return VariantAnalyzer()

@pytest.fixture
def sample_variant():
    return {
        'QUAL': 40.0,
        'DP': 25,
        'REF': 'A',
        'ALT': 'T',
        'POS': 1000,
        'FILTER': 'PASS'
    }

def test_variant_filtering(analyzer, sample_variant):
    """Test mutation filtering functionality."""
    variants = [sample_variant]
    filtered = analyzer.filter_mutations(variants)
    assert len(filtered) == 1
    assert 'predicted_impact' in filtered[0]

def test_low_quality_filtering(analyzer):
    """Test filtering of low quality variants."""
    low_qual_variant = {
        'QUAL': 10.0,
        'DP': 5,
        'REF': 'A',
        'ALT': 'T'
    }
    filtered = analyzer.filter_mutations([low_qual_variant])
    assert len(filtered) == 0

def test_impact_prediction(analyzer, sample_variant):
    """Test variant impact prediction."""
    impact = analyzer.predict_impact(sample_variant)
    assert isinstance(impact, VariantImpact)
    assert 0 <= impact.score <= 1
    assert 0 <= impact.confidence <= 1
    assert impact.effect_prediction in [
        "HIGH_IMPACT_PATHOGENIC",
        "MODERATE_IMPACT_LIKELY_PATHOGENIC",
        "UNCERTAIN_SIGNIFICANCE",
        "MODERATE_IMPACT_LIKELY_BENIGN",
        "LOW_IMPACT_BENIGN"
    ]
    assert isinstance(impact.supporting_evidence, list)
    assert isinstance(impact.functional_details, dict)

def test_quality_criteria(analyzer):
    """Test quality criteria checking."""
    good_variant = {'QUAL': 40.0, 'DP': 20}
    bad_variant = {'QUAL': 20.0, 'DP': 5}
    
    assert analyzer._meets_quality_criteria(good_variant, 30.0)
    assert not analyzer._meets_quality_criteria(bad_variant, 30.0)

def test_feature_extraction(analyzer, sample_variant):
    """Test feature extraction from variants."""
    features = analyzer._extract_features(sample_variant)
    assert isinstance(features, np.ndarray)
    assert len(features) == 8
    assert all(isinstance(x, (int, float)) for x in features)

def test_impact_score_calculation(analyzer):
    """Test impact score calculation."""
    features = np.array([
        40.0,  # QUAL
        25.0,  # DP
        1.0,   # REF length
        1.0,   # ALT length
        0.4,   # Conservation score
        0.5,   # Variant type score
        0.9,   # Position weight
        0.7    # Sequence complexity
    ])
    score = analyzer._calculate_impact_score(features)
    assert isinstance(score, dict)
    assert 0 <= score['score'] <= 1

def test_confidence_calculation(analyzer):
    """Test confidence score calculation."""
    features = np.array([40.0, 25.0, 1.0, 1.0])
    confidence = analyzer._calculate_confidence(features)
    assert 0 <= confidence <= 1

def test_effect_prediction(analyzer):
    """Test effect prediction logic."""
    # Test direct effect prediction first
    assert analyzer._predict_effect_with_confidence(0.9, 0.1) == "HIGH_IMPACT_PATHOGENIC"
    assert analyzer._predict_effect_with_confidence(0.2, 0.1) == "LOW_IMPACT_BENIGN"
    
    # Now test with feature-based calculation
    high_impact_features = np.array([
        100.0,  # QUAL - max quality
        50.0,   # DP - high depth
        1.0,    # REF length
        3.0,    # ALT length
        0.9,    # Conservation - highly conserved
        0.8,    # Variant type - deletion
        0.9,    # Position weight - PASS
        0.7     # Sequence complexity
    ])
    
    # Calculate and verify the high impact score
    high_impact = analyzer._calculate_impact_score(high_impact_features)
    print(f"High impact score: {high_impact['score']}")  # Debug print
    print(f"Confidence interval: {high_impact['confidence_interval']}")  # Debug print
    
    # The score should be high enough for pathogenic impact
    assert high_impact['score'] > 0.7, f"Score {high_impact['score']} is not high enough"
    
    # Test the effect prediction
    effect = analyzer._predict_effect_with_confidence(
        high_impact['score'],
        high_impact['confidence_interval']
    )
    assert effect == "HIGH_IMPACT_PATHOGENIC", f"Got {effect} instead"
    
    # Test low impact case
    low_impact_features = np.array([
        20.0,   # QUAL - low quality
        10.0,   # DP - low depth
        1.0,    # REF length
        1.0,    # ALT length
        0.3,    # Conservation - low conservation
        0.4,    # Variant type - SNP
        0.3,    # Position weight - LOW_QUAL
        0.2     # Sequence complexity
    ])
    
    low_impact = analyzer._calculate_impact_score(low_impact_features)
    assert analyzer._predict_effect_with_confidence(
        low_impact['score'],
        low_impact['confidence_interval']
    ) == "LOW_IMPACT_BENIGN"

def test_evidence_gathering(analyzer, sample_variant):
    """Test supporting evidence gathering."""
    evidence = analyzer._gather_evidence(sample_variant, 0.8)
    assert isinstance(evidence, list)
    assert len(evidence) > 0
    assert all(isinstance(e, str) for e in evidence)

def test_edge_cases(analyzer):
    """Test edge cases and error handling."""
    empty_variant = {}
    impact = analyzer.predict_impact(empty_variant)
    assert impact.score == 0.0
    assert impact.confidence < 0.5
    
    null_values_variant = {'QUAL': None, 'DP': None}
    filtered = analyzer.filter_mutations([null_values_variant])
    assert len(filtered) == 0

@pytest.mark.calculation
def test_impact_score_with_confidence(analyzer):
    """Test impact score calculation with confidence intervals."""
    # Test high impact variant
    high_impact_features = np.array([
        100.0,  # QUAL - max quality
        50.0,   # DP - high depth
        1.0,    # REF length
        3.0,    # ALT length
        0.9,    # Conservation - highly conserved
        0.8,    # Variant type - deletion
        0.9,    # Position weight - PASS
        0.7     # Sequence complexity
    ])
    
    high_impact = analyzer._calculate_impact_score(high_impact_features)
    assert high_impact['score'] > 0.7
    assert 0 <= high_impact['confidence_interval'] <= 0.5
    assert high_impact['lower_bound'] >= 0.0
    assert high_impact['upper_bound'] <= 1.0
    assert len(high_impact['ensemble_predictions']) == 3
    
    # Test low impact variant
    low_impact_features = np.array([
        20.0,   # QUAL - low quality
        10.0,   # DP - low depth
        1.0,    # REF length
        1.0,    # ALT length
        0.3,    # Conservation - low conservation
        0.4,    # Variant type - SNP
        0.3,    # Position weight - LOW_QUAL
        0.2     # Sequence complexity
    ])
    
    low_impact = analyzer._calculate_impact_score(low_impact_features)
    assert low_impact['score'] < 0.3
    assert 0 <= low_impact['confidence_interval'] <= 0.5
    assert low_impact['lower_bound'] >= 0.0
    assert low_impact['upper_bound'] <= 1.0
    
    # Test empty variant
    empty_features = np.zeros(8)
    empty_impact = analyzer._calculate_impact_score(empty_features)
    assert empty_impact['score'] == 0.0
    assert empty_impact['confidence_interval'] == 0.0
    assert empty_impact['lower_bound'] == 0.0
    assert empty_impact['upper_bound'] == 0.0
    assert all(p == 0.0 for p in empty_impact['ensemble_predictions'])
    
    # Test confidence calculation
    confidence = analyzer._calculate_ensemble_confidence(
        high_impact['score'],
        high_impact['confidence_interval'],
        high_impact_features
    )
    assert 0 <= confidence <= 1.0
    assert confidence > 0.5  # High quality should have high confidence

def test_weighted_score_calculation(analyzer):
    """Test weighted score calculation for feature subsets."""
    features = np.array([40.0, 25.0, 1.0, 2.0])
    weights = np.array([0.6, 0.4])
    norm_factors = [100, 50]
    
    score = analyzer._weighted_score(features[:2], weights, norm_factors)
    assert 0 <= score <= 1
    assert isinstance(score, float)

def test_ensemble_confidence_calculation(analyzer):
    """Test ensemble-based confidence calculation."""
    features = np.array([40.0, 25.0, 1.0, 2.0, 0.8, 0.5, 0.9, 0.7])
    score = 0.75
    confidence_interval = 0.1
    
    confidence = analyzer._calculate_ensemble_confidence(score, confidence_interval, features)
    assert 0 <= confidence <= 1
    
    # Test confidence penalty with high uncertainty
    high_uncertainty = analyzer._calculate_ensemble_confidence(score, 0.4, features)
    assert high_uncertainty < confidence  # Higher uncertainty should lower confidence

def test_evidence_gathering_with_confidence(analyzer, sample_variant):
    """Test evidence gathering with confidence intervals."""
    evidence = analyzer._gather_evidence(sample_variant, 0.8, 0.1)
    
    # Check for quality evidence
    assert any("High quality variant" in e for e in evidence)
    assert any("Good sequencing depth" in e for e in evidence)
    
    # Check for confidence-based evidence
    assert any("Strong impact prediction" in e for e in evidence)
    assert any("High confidence prediction" in e for e in evidence)
    
    # Test uncertain prediction
    uncertain_evidence = analyzer._gather_evidence(sample_variant, 0.6, 0.4)
    assert any("interpret with caution" in e for e in uncertain_evidence)

def test_full_variant_analysis(analyzer, sample_variant):
    """Test complete variant analysis pipeline with confidence intervals."""
    impact = analyzer.predict_impact(sample_variant)
    
    assert isinstance(impact, VariantImpact)
    assert 0 <= impact.score <= 1
    assert 0 <= impact.confidence <= 1
    assert impact.effect_prediction in [
        "HIGH_IMPACT_PATHOGENIC",
        "MODERATE_IMPACT_LIKELY_PATHOGENIC",
        "UNCERTAIN_SIGNIFICANCE",
        "MODERATE_IMPACT_LIKELY_BENIGN",
        "LOW_IMPACT_BENIGN"
    ]
    assert len(impact.supporting_evidence) > 0
    
    # Check evidence includes confidence information
    assert any("±" in e for e in impact.supporting_evidence)
    
    # Check functional details
    assert all(k in impact.functional_details for k in [
        'molecular_effect',
        'protein_impact',
        'regulatory_effect',
        'evolutionary_conservation'
    ])

def test_molecular_effect_prediction(analyzer):
    """Test molecular effect prediction."""
    # Test SNP
    assert analyzer._get_molecular_effect('A', 'T') == "SUBSTITUTION"
    
    # Test insertion
    assert analyzer._get_molecular_effect('A', 'AT') == "INSERTION"
    
    # Test deletion
    assert analyzer._get_molecular_effect('AT', 'A') == "DELETION"
    
    # Test complex
    assert analyzer._get_molecular_effect('AT', 'TA') == "COMPLEX"

def test_protein_impact_assessment(analyzer):
    """Test protein impact assessment."""
    # Test frameshift
    frameshift_variant = {
        'FILTER': 'PASS',
        'QUAL': 60.0,
        'REF': 'A',
        'ALT': 'ATG'
    }
    assert analyzer._assess_protein_impact(frameshift_variant) == "FRAMESHIFT"
    
    # Test missense
    missense_variant = {
        'FILTER': 'PASS',
        'QUAL': 60.0,
        'REF': 'A',
        'ALT': 'T'
    }
    assert analyzer._assess_protein_impact(missense_variant) == "MISSENSE"
    
    # Test low quality
    low_qual_variant = {
        'FILTER': 'LOW_QUAL',
        'QUAL': 20.0,
        'REF': 'A',
        'ALT': 'T'
    }
    assert analyzer._assess_protein_impact(low_qual_variant) == "UNKNOWN"

def test_regulatory_effect_prediction(analyzer):
    """Test regulatory effect prediction."""
    # High conservation and position weight
    high_impact_features = np.array([40.0, 25.0, 1.0, 1.0, 0.8, 0.5, 0.9, 0.7])
    assert analyzer._predict_regulatory_effect(high_impact_features) == "REGULATORY_DISRUPTING"
    
    # Moderate impact
    mod_impact_features = np.array([40.0, 25.0, 1.0, 1.0, 0.6, 0.5, 0.5, 0.7])
    assert analyzer._predict_regulatory_effect(mod_impact_features) == "REGULATORY_MODIFYING"
    
    # Low impact
    low_impact_features = np.array([40.0, 25.0, 1.0, 1.0, 0.3, 0.5, 0.3, 0.7])
    assert analyzer._predict_regulatory_effect(low_impact_features) == "REGULATORY_NEUTRAL"

def test_conservation_level_prediction(analyzer):
    """Test conservation level prediction."""
    # Test highly conserved
    high_cons_features = np.array([40.0, 25.0, 1.0, 1.0, 0.9, 0.5, 0.9, 0.7])
    assert analyzer._get_conservation_level(high_cons_features) == "HIGHLY_CONSERVED"
    
    # Test moderately conserved
    mod_cons_features = np.array([40.0, 25.0, 1.0, 1.0, 0.6, 0.5, 0.9, 0.7])
    assert analyzer._get_conservation_level(mod_cons_features) == "MODERATELY_CONSERVED"
    
    # Test low conservation
    low_cons_features = np.array([40.0, 25.0, 1.0, 1.0, 0.3, 0.5, 0.9, 0.7])
    assert analyzer._get_conservation_level(low_cons_features) == "LOW_CONSERVATION"

def test_detailed_evidence_gathering(analyzer, sample_variant):
    """Test detailed evidence gathering with functional impact."""
    features = analyzer._extract_features(sample_variant)
    impact_data = analyzer._calculate_impact_score(features)
    
    # Use the new _gather_evidence method instead
    evidence = analyzer._gather_evidence(
        sample_variant,
        impact_data['score'],
        impact_data['confidence_interval']
    )
    
    # Check for all required evidence types
    assert any("Impact prediction" in e for e in evidence)
    assert any("Molecular effect" in e for e in evidence)
    assert any("Protein impact" in e for e in evidence)
    assert any("Regulatory effect" in e for e in evidence)
    assert any("Conservation" in e for e in evidence)
    
    # Check for confidence information
    assert any("±" in e for e in evidence)
    
    # Check for quality evidence when applicable
    if sample_variant.get('QUAL', 0) > 30:
        assert any("High quality variant" in e for e in evidence)
    if sample_variant.get('DP', 0) > 20:
        assert any("Good sequencing depth" in e for e in evidence)

def test_comprehensive_variant_analysis(analyzer):
    """Test complete variant analysis with all new features."""
    variant = {
        'QUAL': 60.0,
        'DP': 30,
        'REF': 'A',
        'ALT': 'T',
        'POS': 1000,
        'FILTER': 'PASS'
    }
    
    impact = analyzer.predict_impact(variant)
    
    # Check all components
    assert isinstance(impact.score, float)
    assert isinstance(impact.confidence, float)
    assert impact.effect_prediction in [
        "HIGH_IMPACT_PATHOGENIC",
        "MODERATE_IMPACT_LIKELY_PATHOGENIC",
        "UNCERTAIN_SIGNIFICANCE",
        "MODERATE_IMPACT_LIKELY_BENIGN",
        "LOW_IMPACT_BENIGN"
    ]
    assert isinstance(impact.functional_details, dict)
    assert all(k in impact.functional_details for k in [
        'molecular_effect',
        'protein_impact',
        'regulatory_effect',
        'evolutionary_conservation'
    ])
    assert len(impact.supporting_evidence) > 0

def test_edge_case_functional_impact(analyzer):
    """Test functional impact prediction with edge cases."""
    # Empty variant
    empty_variant = {}
    empty_features = analyzer._extract_features(empty_variant)
    impact = analyzer._predict_functional_impact(empty_variant, empty_features)
    assert all(v in ["UNKNOWN", "COMPLEX", "REGULATORY_NEUTRAL", "LOW_CONSERVATION"] 
              for v in impact.values())
    
    # Invalid values
    invalid_variant = {
        'QUAL': None,
        'DP': 'invalid',
        'REF': None,
        'ALT': None,
        'POS': 'invalid',
        'FILTER': None
    }
    invalid_features = analyzer._extract_features(invalid_variant)
    impact = analyzer._predict_functional_impact(invalid_variant, invalid_features)
    assert all(v in ["UNKNOWN", "COMPLEX", "REGULATORY_NEUTRAL", "LOW_CONSERVATION"] 
              for v in impact.values())

def test_boundary_conservation_scores(analyzer):
    """Test conservation scoring at boundary conditions."""
    # Test exact boundary values
    boundary_variants = [
        {'POS': 0},           # Edge case: position 0
        {'POS': -1},          # Invalid negative position
        {'POS': 2**31 - 1},   # Max int position
        {'POS': None},        # None position
        {}                    # Missing position
    ]
    
    for variant in boundary_variants:
        score = analyzer._get_conservation_score(variant)
        assert 0 <= score <= 1
        assert isinstance(score, float)

def test_complex_variant_types(analyzer):
    """Test variant type scoring with complex cases."""
    complex_cases = [
        ('ACGT', 'TGCA'),    # Complex substitution
        ('A', 'ATCG'),       # Long insertion
        ('ATCG', 'A'),       # Long deletion
        ('', ''),            # Empty strings
        ('N', 'N'),          # Ambiguous bases
        ('ATN', 'ATC'),      # Partial ambiguous
    ]
    
    for ref, alt in complex_cases:
        score = analyzer._get_variant_type_score({'REF': ref, 'ALT': alt})
        assert 0 <= score <= 1
        assert isinstance(score, float) 