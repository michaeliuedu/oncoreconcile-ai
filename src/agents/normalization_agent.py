
"""
Normalization Agent - Map variants to canonical representations

This agent normalizes genes and variants to canonical forms using:
- HGNC gene nomenclature
- RefSeq transcripts
- HGVS nomenclature standards

====================
Developer Documentation
====================

**Current Logic:**
- Gene normalization uses curated alias mapping (gene_aliases.csv), uppercases, and strips whitespace.
- Variant normalization uses curated synonym mapping (variant_synonyms.csv), uppercases, replaces underscores, trims spaces, and applies some hardcoded rules for common variants (e.g., EGFR exon 19 deletion, L858R, BRAF V600E, KRAS G12C).
- If no match, returns a generic canonical form and a note for manual curation.

**How to Enhance Normalization Logic:**
1. Expand mapping files (gene_aliases.csv, variant_synonyms.csv) with new aliases/synonyms as encountered.
2. Update normalization logic to handle more formatting variations (e.g., punctuation, common typos, alternate spellings).
3. Add more rule-based transformations for common patterns (e.g., regex for "Ex19del" → "exon 19 deletion").
4. Regularly review unmapped or "needs_review" cases and add deterministic rules/mappings if possible.
5. Leverage external databases (HGNC, ClinVar) for additional mappings.

**Team Guidance:**
- When you encounter an unmapped input, first check if it can be handled by expanding the mapping files or adding a new rule.
- For ambiguous or novel cases, escalate to AI/LLM or human review.
- Document any new rules or mapping logic in this file and update the mapping files as needed.
"""

from dataclasses import dataclass
from pathlib import Path
import csv
from typing import Optional, Dict, Any, List


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


@dataclass
class GeneReconciliationResult:
    """Result of reconciling an input gene name to a canonical gene"""
    input_gene: str
    canonical_gene: str
    hgnc_id: Optional[int]
    entrez_gene_id: Optional[int]
    confidence: float
    match_type: str
    aliases: List[str]
    description: Optional[str] = None
    notes: Optional[str] = None


class GeneNormalizer:
    """Normalize gene symbols to canonical HGNC names"""

    def __init__(
        self,
        gene_aliases_data: Optional[Dict[str, Dict]] = None,
        gene_aliases_path: Optional[str] = None,
    ):
        """
        Initialize with gene alias data
        
        Args:
            gene_aliases_data: Dictionary mapping gene inputs to canonical forms
            gene_aliases_path: Optional CSV path for gene alias reference data
        """
        self.gene_map: Dict[str, Dict[str, Any]] = {}
        self.aliases_by_canonical: Dict[str, List[str]] = {}
        self._load_aliases_from_csv(gene_aliases_path)

        if gene_aliases_data:
            for gene_input, gene_info in gene_aliases_data.items():
                self._add_gene_alias(gene_input, gene_info)

    @staticmethod
    def _default_gene_aliases_path() -> Path:
        """Return the repository reference data path for gene aliases"""
        return (
            Path(__file__).resolve().parents[2]
            / "data"
            / "reference"
            / "v0.1"
            / "gene_aliases.csv"
        )

    @staticmethod
    def _parse_optional_int(value: Optional[str]) -> Optional[int]:
        """Parse CSV integer values while preserving blanks as None"""
        if value in (None, ""):
            return None
        return int(value)

    def _load_aliases_from_csv(self, gene_aliases_path: Optional[str] = None) -> None:
        """Load gene aliases from the curated reference CSV"""
        path = Path(gene_aliases_path) if gene_aliases_path else self._default_gene_aliases_path()
        if not path.exists():
            return

        with path.open(newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self._add_gene_alias(
                    row["gene_input"],
                    {
                        "canonical": row["canonical_gene"],
                        "hgnc_id": self._parse_optional_int(row.get("hgnc_id")),
                        "entrez_id": self._parse_optional_int(row.get("entrez_id")),
                        "description": row.get("description"),
                    },
                )

    def _add_gene_alias(self, gene_input: str, gene_info: Dict[str, Any]) -> None:
        """Register one input gene spelling as an alias for a canonical gene"""
        alias_key = gene_input.upper().strip()
        canonical = gene_info["canonical"].upper().strip()
        normalized_info = {
            "canonical": canonical,
            "hgnc_id": gene_info.get("hgnc_id"),
            "entrez_id": gene_info.get("entrez_id"),
            "description": gene_info.get("description"),
        }

        self.gene_map[alias_key] = normalized_info
        self.aliases_by_canonical.setdefault(canonical, [])
        if alias_key not in self.aliases_by_canonical[canonical]:
            self.aliases_by_canonical[canonical].append(alias_key)

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
            gene_info = self.gene_map[gene_upper].copy()
            gene_info["confidence"] = 1.0 if gene_upper == gene_info["canonical"] else 0.95
            gene_info["match_type"] = "canonical" if gene_upper == gene_info["canonical"] else "alias"
            gene_info["aliases"] = self.aliases_by_canonical.get(gene_info["canonical"], [])
            return gene_info
        
        # Fallback: return as-is with warning
        return {
            "canonical": gene_upper,
            "hgnc_id": None,
            "entrez_id": None,
            "confidence": 0.3,
            "match_type": "unmatched",
            "aliases": [],
            "note": f"Gene '{gene_input}' not in reference database"
        }


class GeneReconciliationAgent:
    """First-class gene name reconciliation workflow"""

    def __init__(self, gene_normalizer: Optional[GeneNormalizer] = None):
        """Initialize with a CSV-backed gene normalizer"""
        self.gene_normalizer = gene_normalizer or GeneNormalizer()

    def execute(self, gene_input: str) -> GeneReconciliationResult:
        """
        Reconcile a raw gene name or alias to a canonical gene symbol.

        Args:
            gene_input: Gene symbol, alias, or historical name

        Returns:
            GeneReconciliationResult with canonical mapping and audit-friendly details
        """
        gene_info = self.gene_normalizer.normalize_gene(gene_input)
        return GeneReconciliationResult(
            input_gene=gene_input,
            canonical_gene=gene_info["canonical"],
            hgnc_id=gene_info.get("hgnc_id"),
            entrez_gene_id=gene_info.get("entrez_id"),
            confidence=gene_info.get("confidence", 0.3),
            match_type=gene_info.get("match_type", "unmatched"),
            aliases=gene_info.get("aliases", []),
            description=gene_info.get("description"),
            notes=gene_info.get("note"),
        )


class VariantNormalizer:
    """Normalize variants to canonical HGVS nomenclature"""

    def __init__(
        self,
        transcript_data: Optional[Dict] = None,
        variant_synonyms_path: Optional[str] = None,
        canonical_variants_path: Optional[str] = None,
    ):
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
            "ROS1": {
                "primary": "unknown",
            },
            "RET": {
                "primary": "unknown",
            },
            "TP53": {
                "primary": "NM_000546.6",
            },
        }
        if transcript_data:
            self.transcripts.update(transcript_data)

        self.canonical_variants: Dict[str, Dict[str, Any]] = {}
        self.variant_synonym_map: Dict[tuple[str, str], str] = {}
        self._load_canonical_variants(canonical_variants_path)
        self._load_variant_synonyms(variant_synonyms_path)

    @staticmethod
    def _reference_path(filename: str) -> Path:
        """Return a file path under the repository reference data directory"""
        return (
            Path(__file__).resolve().parents[2]
            / "data"
            / "reference"
            / "v0.1"
            / filename
        )

    @staticmethod
    def _normalize_lookup_text(value: str) -> str:
        """Normalize variant text for deterministic synonym lookup"""
        return " ".join(value.upper().replace("::", "-").replace("_", " ").split())

    def _load_canonical_variants(self, canonical_variants_path: Optional[str] = None) -> None:
        """Load canonical variant metadata from the reference CSV"""
        path = Path(canonical_variants_path) if canonical_variants_path else self._reference_path("canonical_variants.csv")
        if not path.exists():
            return

        with path.open(newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.canonical_variants[row["canonical_id"]] = row

    def _load_variant_synonyms(self, variant_synonyms_path: Optional[str] = None) -> None:
        """Load variant synonyms from the reference CSV"""
        path = Path(variant_synonyms_path) if variant_synonyms_path else self._reference_path("variant_synonyms.csv")
        if not path.exists():
            return

        with path.open(newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                gene = row["canonical_id"].split("|")[0]
                synonym_key = self._normalize_lookup_text(row["synonym"])
                canonical_key = self._normalize_lookup_text(row["canonical_id"].replace("|", " "))
                self.variant_synonym_map[(gene, synonym_key)] = row["canonical_id"]
                self.variant_synonym_map[(gene, canonical_key)] = row["canonical_id"]

    def _lookup_variant(self, gene: str, location: str) -> Optional[Dict[str, Any]]:
        """Look up a variant by gene and raw/synonym text"""
        gene = gene.upper().strip()
        lookup_candidates = [
            location,
            f"{gene} {location}",
            location.replace("|", " "),
        ]

        for candidate in lookup_candidates:
            canonical_id = self.variant_synonym_map.get(
                (gene, self._normalize_lookup_text(candidate))
            )
            if canonical_id:
                metadata = self.canonical_variants.get(canonical_id, {})
                return {
                    "canonical_id": canonical_id,
                    "hgvs_dna": metadata.get("hgvs_dna", "unknown"),
                    "hgvs_protein": metadata.get("hgvs_protein", "unknown"),
                    "transcript": metadata.get("transcript", self.transcripts.get(gene, {}).get("primary", "unknown")),
                    "confidence": 0.97,
                    "match_type": "synonym",
                }

        return None

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

        synonym_match = self._lookup_variant(gene, location)
        if synonym_match:
            return synonym_match
        
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
