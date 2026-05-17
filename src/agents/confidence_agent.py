"""Confidence Agent - Multi-component confidence scoring

Combines:
- Deterministic score (rule-based matching)
- Semantic similarity score (embeddings)
- LLM reasoning score
- Historical approval score (prior decisions)
"""

from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class ConfidenceScore:
    """Result of confidence scoring"""
    composite_score: float
    score_breakdown: Dict[str, float] = field(default_factory=dict)
    confidence_category: str = ""
    queue_recommendation: str = ""


class ConfidenceAgent:
    """Compute multi-component confidence scores"""

    def __init__(self):
        """Initialize scoring agent"""
        self.weights = {
            "deterministic": 0.30,
            "semantic_similarity": 0.25,
            "llm_reasoning": 0.25,
            "historical_approval": 0.20,
        }

    def execute(
        self,
        deterministic_score: float,
        semantic_similarity_score: float,
        llm_confidence_score: float,
        historical_approval_score: float,
    ) -> ConfidenceScore:
        """
        Compute composite confidence score
        
        Args:
            deterministic_score: Rule-based matching score (0-1)
            semantic_similarity_score: Embedding similarity score (0-1)
            llm_confidence_score: LLM reasoning confidence (0-1)
            historical_approval_score: Prior approval rate (0-1)
            
        Returns:
            ConfidenceScore with composite and breakdown
        """
        
        # Compute weighted average
        composite = (
            deterministic_score * self.weights["deterministic"] +
            semantic_similarity_score * self.weights["semantic_similarity"] +
            llm_confidence_score * self.weights["llm_reasoning"] +
            historical_approval_score * self.weights["historical_approval"]
        )
        
        # Clamp to [0, 1]
        composite = max(0.0, min(1.0, composite))
        
        # Determine confidence category
        if composite > 0.95:
            category = "Very High"
        elif composite > 0.80:
            category = "High"
        elif composite > 0.60:
            category = "Moderate"
        elif composite > 0.40:
            category = "Low"
        else:
            category = "Very Low"
        
        # Recommend queue type
        queue_recommendation = self._recommend_queue(
            composite,
            historical_approval_score
        )
        
        return ConfidenceScore(
            composite_score=composite,
            score_breakdown={
                "deterministic": deterministic_score,
                "semantic_similarity": semantic_similarity_score,
                "llm_reasoning": llm_confidence_score,
                "historical_approval": historical_approval_score,
            },
            confidence_category=category,
            queue_recommendation=queue_recommendation,
        )

    @staticmethod
    def _recommend_queue(composite_score: float, historical_score: float) -> str:
        """Recommend review queue based on scores"""
        
        if composite_score > 0.95 and historical_score > 0.95:
            return "fast_track"
        elif composite_score > 0.80:
            return "standard"
        elif composite_score > 0.60:
            return "escalation"
        else:
            return "manual_curation"


def compute_deterministic_score(
    canonical_match: bool,
    nomenclature_consistency: bool,
    gene_validated: bool,
) -> float:
    """
    Compute deterministic score from rule-based matching
    
    Args:
        canonical_match: Perfect canonical ID match
        nomenclature_consistency: HGVS nomenclature is consistent
        gene_validated: Gene found in reference DB
        
    Returns:
        Deterministic score (0-1)
    """
    score = 0.0
    if canonical_match:
        score += 0.6
    if nomenclature_consistency:
        score += 0.3
    if gene_validated:
        score += 0.1
    
    return min(score, 1.0)


def compute_semantic_similarity_score(
    kb_candidates: int,
    best_match_score: float = 0.99,
) -> float:
    """
    Compute semantic similarity score
    
    Args:
        kb_candidates: Number of KB candidates found
        best_match_score: Best embedding similarity score
        
    Returns:
        Semantic similarity score (0-1)
    """
    if kb_candidates == 0:
        return 0.0
    elif kb_candidates == 1:
        return best_match_score
    else:
        # Multiple candidates, use best match with slight discount
        return best_match_score * 0.95


def compute_historical_approval_score(
    total_approvals: int,
    total_rejections: int,
    min_samples: int = 5,
) -> float:
    """
    Compute historical approval rate score
    
    Args:
        total_approvals: Number of prior approvals
        total_rejections: Number of prior rejections
        min_samples: Minimum samples to consider (avoid overfitting)
        
    Returns:
        Historical approval score (0-1)
    """
    total = total_approvals + total_rejections
    
    if total < min_samples:
        # Not enough history - neutral score
        return 0.5
    
    approval_rate = total_approvals / total
    
    # Apply confidence factor based on sample size
    confidence_factor = min(total / (min_samples * 10), 1.0)
    
    return approval_rate * confidence_factor
