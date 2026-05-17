"""KB Update - Versioned knowledge base updates

Manages:
- KB version control
- Variant alias additions
- Evidence linking
- Rollback capability
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from datetime import datetime


@dataclass
class KBVariant:
    """Knowledge base variant entry"""
    canonical_id: str
    gene: str
    hgvs_dna: str
    hgvs_protein: str
    aliases: List[str] = field(default_factory=list)
    clinical_significance: str = ""
    nccn_tier: Optional[int] = None
    evidence_links: List[Dict[str, Any]] = field(default_factory=list)
    approval_history: Dict[str, int] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


class KBUpdate:
    """Manage versioned KB updates"""

    def __init__(self):
        """Initialize KB"""
        self.kb: Dict[str, KBVariant] = {}
        self.version = "0.1"
        self.version_history: List[Dict[str, Any]] = []

    def add_or_update_variant(
        self,
        canonical_id: str,
        gene: str,
        hgvs_dna: str,
        hgvs_protein: str,
        clinical_significance: str = "",
        nccn_tier: Optional[int] = None,
    ) -> KBVariant:
        """Add or update variant in KB"""
        
        if canonical_id in self.kb:
            variant = self.kb[canonical_id]
            variant.updated_at = datetime.utcnow()
        else:
            variant = KBVariant(
                canonical_id=canonical_id,
                gene=gene,
                hgvs_dna=hgvs_dna,
                hgvs_protein=hgvs_protein,
                clinical_significance=clinical_significance,
                nccn_tier=nccn_tier,
            )
            self.kb[canonical_id] = variant
        
        return variant

    def add_alias(self, canonical_id: str, alias: str) -> bool:
        """Add alias to variant"""
        if canonical_id in self.kb:
            variant = self.kb[canonical_id]
            if alias not in variant.aliases:
                variant.aliases.append(alias)
                variant.updated_at = datetime.utcnow()
                return True
        return False

    def add_evidence(self, canonical_id: str, evidence: Dict[str, Any]) -> bool:
        """Add evidence link to variant"""
        if canonical_id in self.kb:
            variant = self.kb[canonical_id]
            variant.evidence_links.append(evidence)
            variant.updated_at = datetime.utcnow()
            return True
        return False

    def increment_version(self, change_description: str) -> str:
        """Increment KB version"""
        parts = self.version.split(".")
        parts[-1] = str(int(parts[-1]) + 1)
        self.version = ".".join(parts)
        
        self.version_history.append({
            "version": self.version,
            "timestamp": datetime.utcnow(),
            "description": change_description,
            "variant_count": len(self.kb),
        })
        
        return self.version

    def get_variant(self, canonical_id: str) -> Optional[KBVariant]:
        """Retrieve variant from KB"""
        return self.kb.get(canonical_id)

    def search_by_alias(self, alias: str) -> List[KBVariant]:
        """Search for variants by alias"""
        return [
            variant for variant in self.kb.values()
            if alias.lower() in [a.lower() for a in variant.aliases]
        ]

    def export_kb(self) -> Dict[str, Any]:
        """Export KB as JSON-serializable dictionary"""
        return {
            "version": self.version,
            "exported_at": datetime.utcnow().isoformat(),
            "variant_count": len(self.kb),
            "variants": {
                canonical_id: {
                    "gene": v.gene,
                    "hgvs_dna": v.hgvs_dna,
                    "hgvs_protein": v.hgvs_protein,
                    "aliases": v.aliases,
                    "clinical_significance": v.clinical_significance,
                    "nccn_tier": v.nccn_tier,
                    "evidence_links": v.evidence_links,
                }
                for canonical_id, v in self.kb.items()
            }
        }
