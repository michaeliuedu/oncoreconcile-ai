"""Retrieval Agent - Search knowledge base for candidate variants

This agent queries the KB for:
- Exact canonical matches
- Semantic similarity matches
- Clinical evidence links
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class VariantCandidate:
    """A candidate match from KB"""
    kb_id: str
    canonical_id: str
    relevance_score: float
    aliases: List[str] = field(default_factory=list)
    clinical_significance: Optional[str] = None
    evidence_links: List[Dict[str, Any]] = field(default_factory=list)
    approval_history: Optional[Dict[str, int]] = None


@dataclass
class RetrievalResult:
    """Result of retrieval agent processing"""
    candidates: List[VariantCandidate]
    exact_match_found: bool
    total_candidates: int
    evidence_links_count: int
    confidence: float


class RetrievalAgent:
    """Search knowledge base for variant candidates"""

    def __init__(self, kb_data: Optional[Dict] = None):
        """
        Initialize with knowledge base data
        
        Args:
            kb_data: Knowledge base dictionary
        """
        # Placeholder KB for MVP
        self.kb = {
            "EGFR|exon_19_deletion": {
                "kb_id": "var_egfr_001",
                "canonical_id": "EGFR|exon_19_deletion",
                "aliases": [
                    "EGFR Ex19del",
                    "EGFR exon_19_del",
                    "EGFR c.2235_2249del15",
                    "EGFR p.E746_A750del"
                ],
                "clinical_significance": "Sensitizing (TKI-responsive)",
                "approvals": 156,
                "rejections": 0,
                "evidence": [
                    {"source": "NCCN", "title": "EGFR Ex19 TKI sensitivity"},
                    {"source": "ClinVar", "title": "Pathogenic"},
                    {"source": "CIViC", "title": "Predictive for TKI"}
                ]
            },
            "BRAF|V600E": {
                "kb_id": "var_braf_001",
                "canonical_id": "BRAF|V600E",
                "aliases": ["BRAF V600E", "BRAF c.1799T>A"],
                "clinical_significance": "Activating",
                "approvals": 200,
                "rejections": 1,
                "evidence": [
                    {"source": "NCCN", "title": "BRAF inhibitor responsive"}
                ]
            },
            "KRAS|G12C": {
                "kb_id": "var_kras_001",
                "canonical_id": "KRAS|G12C",
                "aliases": ["KRAS G12C", "KRAS c.34G>T"],
                "clinical_significance": "Activating (sotorasib-responsive)",
                "approvals": 89,
                "rejections": 0,
                "evidence": [
                    {"source": "NCCN", "title": "Sotorasib responsive"}
                ]
            },
        }
        if kb_data:
            self.kb.update(kb_data)

    def execute(self, canonical_variant_id: str) -> RetrievalResult:
        """
        Search KB for candidates matching canonical variant ID
        
        Args:
            canonical_variant_id: The canonical ID to search for
            
        Returns:
            RetrievalResult with matching candidates
        """
        candidates = []
        exact_match = False

        # Exact match
        if canonical_variant_id in self.kb:
            entry = self.kb[canonical_variant_id]
            candidate = VariantCandidate(
                kb_id=entry["kb_id"],
                canonical_id=entry["canonical_id"],
                relevance_score=1.0,
                aliases=entry.get("aliases", []),
                clinical_significance=entry.get("clinical_significance"),
                evidence_links=entry.get("evidence", []),
                approval_history={
                    "approvals": entry.get("approvals", 0),
                    "rejections": entry.get("rejections", 0),
                }
            )
            candidates.append(candidate)
            exact_match = True

        # Semantic search (simplified for MVP - just check aliases)
        for kb_id, entry in self.kb.items():
            if entry["canonical_id"] != canonical_variant_id:
                # Check if input matches any alias (partial match)
                score = self._compute_similarity(canonical_variant_id, entry["canonical_id"])
                if score > 0.7 and kb_id not in [c.kb_id for c in candidates]:
                    candidate = VariantCandidate(
                        kb_id=entry["kb_id"],
                        canonical_id=entry["canonical_id"],
                        relevance_score=score,
                        aliases=entry.get("aliases", []),
                        clinical_significance=entry.get("clinical_significance"),
                        evidence_links=entry.get("evidence", []),
                        approval_history={
                            "approvals": entry.get("approvals", 0),
                            "rejections": entry.get("rejections", 0),
                        }
                    )
                    candidates.append(candidate)

        # Sort by relevance
        candidates.sort(key=lambda c: c.relevance_score, reverse=True)

        # Count evidence
        evidence_count = sum(len(c.evidence_links) for c in candidates)

        return RetrievalResult(
            candidates=candidates[:5],  # Return top 5
            exact_match_found=exact_match,
            total_candidates=len(candidates),
            evidence_links_count=evidence_count,
            confidence=1.0 if exact_match else (0.7 if candidates else 0.0)
        )

    @staticmethod
    def _compute_similarity(query: str, target: str) -> float:
        """
        Compute simple string similarity (placeholder for embeddings)
        
        Args:
            query: Query canonical ID
            target: Target canonical ID
            
        Returns:
            Similarity score 0-1
        """
        # Extract gene names
        query_gene = query.split("|")[0] if "|" in query else query
        target_gene = target.split("|")[0] if "|" in target else target
        
        if query_gene == target_gene:
            return 0.8  # Same gene, different variant
        return 0.0
