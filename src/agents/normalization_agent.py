"""Normalization Agent - Map variants to canonical representations

This agent normalizes genes and variants to canonical forms using:
- HGNC gene nomenclature
- RefSeq transcripts
- HGVS nomenclature standards
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class NormalizedVariant:
    """Result of normalization agent processing"""
    canonical_variant_id: str
    canonical_gene: str
    hgnc_id: int
    entrez_gene_id: int
    transcript: str
    hgvs_dna: str
    hgvs_protein: str
    genomic_coordinates: Dict[str, Any]
    confidence: float
    notes: Optional[str] = None


class GeneNormalizer:
    """Normalize gene symbols to canonical HGNC names"""

    def __init__(self, gene_aliases_data: Optional[Dict[str, Dict]] = None):
        """
        Initialize with gene alias data
        
        Args:
            gene_aliases_data: Dictionary mapping gene inputs to canonical forms
        """
        # Default mapping for MVP
        self.gene_map = {
            "EGFR": {"canonical": "EGFR", "hgnc_id": 3236, "entrez_id": 1956},
            "EGF": {"canonical": "EGFR", "hgnc_id": 3236, "entrez_id": 1956},
            "BRAF": {"canonical": "BRAF", "hgnc_id": 1097, "entrez_id": 673},
            "ERBB2": {"canonical": "ERBB2", "hgnc_id": 3236, "entrez_id": 2064},
            "HER2": {"canonical": "ERBB2", "hgnc_id": 3236, "entrez_id": 2064},
            "KRAS": {"canonical": "KRAS", "hgnc_id": 6407, "entrez_id": 3845},
            "ALK": {"canonical": "ALK", "hgnc_id": 427, "entrez_id": 238},
            "MET": {"canonical": "MET", "hgnc_id": 6973, "entrez_id": 4233},
        }
        if gene_aliases_data:
            self.gene_map.update(gene_aliases_data)

    def normalize_gene(self, gene_input: str) -> Dict[str, Any]:
        """
        Normalize gene symbol to canonical form
        
        Args:
            gene_input: Input gene symbol
            
        Returns:
            Dictionary with canonical gene info
        """
        gene_upper = gene_input.upper().strip()
        
        if gene_upper in self.gene_map:
            return self.gene_map[gene_upper]
        
        # Fallback: return as-is with warning
        return {
            "canonical": gene_upper,
            "hgnc_id": None,
            "entrez_id": None,
            "confidence": 0.3,
            "note": f"Gene '{gene_input}' not in reference database"
        }


class VariantNormalizer:
    """Normalize variants to canonical HGVS nomenclature"""

    def __init__(self, transcript_data: Optional[Dict] = None):
        """Initialize with transcript reference data"""
        # Default transcripts for MVP
        self.transcripts = {
            "EGFR": {
                "primary": "NM_005228.4",
                "exon_19_start": 2235,
                "exon_19_end": 2249,
            },
            "BRAF": {
                "primary": "NM_004333.4",
            },
            "ERBB2": {
                "primary": "NM_004448.3",
            },
            "KRAS": {
                "primary": "NM_033360.4",
            },
            "ALK": {
                "primary": "NM_004304.4",
            },
            "MET": {
                "primary": "NM_000245.3",
            },
        }
        if transcript_data:
            self.transcripts.update(transcript_data)

    def normalize_variant(
        self,
        gene: str,
        variant_type: str,
        location: str,
    ) -> Dict[str, Any]:
        """
        Normalize variant to canonical HGVS nomenclature
        
        Args:
            gene: Canonical gene name
            variant_type: Type of variant (deletion, substitution, etc.)
            location: Location specification
            
        Returns:
            Dictionary with normalized variant info
        """
        transcript = self.transcripts.get(gene, {}).get("primary", "unknown")
        
        # Map common variants to canonical forms
        if gene == "EGFR" and variant_type == "deletion" and "19" in location:
            return {
                "canonical_id": "EGFR|exon_19_deletion",
                "hgvs_dna": "c.2235_2249del15",
                "hgvs_protein": "p.E746_A750del",
                "transcript": transcript,
                "confidence": 0.99,
            }
        
        if gene == "EGFR" and "L858R" in location:
            return {
                "canonical_id": "EGFR|L858R",
                "hgvs_dna": "c.2573T>G",
                "hgvs_protein": "p.L858R",
                "transcript": transcript,
                "confidence": 0.99,
            }
        
        if gene == "BRAF" and "V600E" in location:
            return {
                "canonical_id": "BRAF|V600E",
                "hgvs_dna": "c.1799T>A",
                "hgvs_protein": "p.V600E",
                "transcript": transcript,
                "confidence": 0.99,
            }
        
        if gene == "KRAS" and "G12C" in location:
            return {
                "canonical_id": "KRAS|G12C",
                "hgvs_dna": "c.34G>T",
                "hgvs_protein": "p.G12C",
                "transcript": transcript,
                "confidence": 0.99,
            }
        
        # Fallback: generic canonical form
        canonical_id = f"{gene}|{location.replace(' ', '_')}"
        return {
            "canonical_id": canonical_id,
            "transcript": transcript,
            "confidence": 0.5,
            "note": "Generic normalization - manual curation recommended"
        }


class NormalizationAgent:
    """Orchestrate gene and variant normalization"""

    def __init__(self):
        """Initialize normalization components"""
        self.gene_normalizer = GeneNormalizer()
        self.variant_normalizer = VariantNormalizer()

    def execute(
        self,
        gene: str,
        variant_type: str,
        location: str,
    ) -> NormalizedVariant:
        """
        Normalize extracted components to canonical forms
        
        Args:
            gene: Input gene symbol
            variant_type: Variant type
            location: Variant location
            
        Returns:
            NormalizedVariant with canonical representation
        """
        # Normalize gene
        gene_info = self.gene_normalizer.normalize_gene(gene)
        canonical_gene = gene_info["canonical"]
        
        # Normalize variant
        variant_info = self.variant_normalizer.normalize_variant(
            canonical_gene, variant_type, location
        )
        
        # Build genomic coordinates (placeholder for MVP)
        genomic_coords = {
            "chr": self._get_chromosome(canonical_gene),
            "build": "GRCh38",
        }
        
        return NormalizedVariant(
            canonical_variant_id=variant_info.get("canonical_id", f"{canonical_gene}|{location}"),
            canonical_gene=canonical_gene,
            hgnc_id=gene_info.get("hgnc_id"),
            entrez_gene_id=gene_info.get("entrez_id"),
            transcript=variant_info.get("transcript", "unknown"),
            hgvs_dna=variant_info.get("hgvs_dna", "unknown"),
            hgvs_protein=variant_info.get("hgvs_protein", "unknown"),
            genomic_coordinates=genomic_coords,
            confidence=min(
                gene_info.get("confidence", 0.8),
                variant_info.get("confidence", 0.5)
            ),
            notes=variant_info.get("note")
        )

    @staticmethod
    def _get_chromosome(gene: str) -> str:
        """Get chromosome for gene"""
        chr_map = {
            "EGFR": "7",
            "BRAF": "7",
            "ERBB2": "17",
            "KRAS": "12",
            "ALK": "2",
            "MET": "7",
        }
        return chr_map.get(gene, "unknown")
