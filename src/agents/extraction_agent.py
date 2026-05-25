"""Extraction Agent - Parse raw variant strings into components

This agent takes unstructured variant input and extracts structured components:
- Gene symbol
- Variant type (deletion, substitution, insertion, fusion)
- Location (exon, codon, position)
- Nomenclature style (shorthand, HGVS, etc.)
"""

import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class ExtractedVariant:
    """Result of extraction agent processing"""
    gene: str
    variant_type: str
    location: str
    nomenclature_style: str
    confidence: float
    raw_input: str
    notes: Optional[str] = None


class ExtractionAgent:
    """Extract variant components from raw text strings"""

    def __init__(self):
        """Initialize extraction patterns"""
        self.gene_pattern = r"([A-Z0-9]+(?:/[A-Z0-9]+)?)"
        self.deletion_patterns = [
            r"(?:ex|exon)\s*(\d+)\s*(?:del|deletion)",
            r"del(\d+)",
            r"(?:ex|exon)(\d+)del",
        ]
        self.substitution_patterns = [
            r"([A-Z])(\d+)([A-Z])",  # A123B format
            r"c\.(\d+)([A-Z])>([A-Z])",  # HGVS DNA format
        ]
        self.insertion_patterns = [
            r"(?:ex|exon)\s*(\d+)\s*(?:ins|insertion)",
            r"ins",
        ]
        self.fusion_patterns = [
            r"([A-Z0-9]+)-([A-Z0-9]+)\s*(?:fusion|translocation)",
        ]

    def execute(self, raw_variant: str) -> ExtractedVariant:
        """
        Parse raw variant string into components
        
        Args:
            raw_variant: Unstructured variant string (e.g., "EGFR Ex19del")
            
        Returns:
            ExtractedVariant with parsed components
        """
        raw_variant = raw_variant.strip()
        
        # Extract gene (first token or until special character)
        gene_match = re.match(r"^([A-Z0-9]+(?:/[A-Z0-9]+)?)", raw_variant)
        gene = gene_match.group(1) if gene_match else ""
        
        # Determine variant type and location
        remainder = raw_variant[len(gene):].lower()
        
        # Check deletion
        for pattern in self.deletion_patterns:
            match = re.search(pattern, remainder, re.IGNORECASE)
            if match:
                exon = match.group(1) if match.groups() else "unknown"
                return ExtractedVariant(
                    gene=gene,
                    variant_type="deletion",
                    location=f"exon_{exon}",
                    nomenclature_style="shorthand",
                    confidence=0.95,
                    raw_input=raw_variant,
                    notes="Exon-level deletion detected"
                )
        
        # Check substitution
        for pattern in self.substitution_patterns:
            match = re.search(pattern, remainder, re.IGNORECASE)
            if match:
                if len(match.groups()) >= 2:
                    if pattern.startswith("c\\."):
                        location = f"c.{match.group(1)}{match.group(2).upper()}>{match.group(3).upper()}"
                    else:
                        location = f"{match.group(1).upper()}{match.group(2)}{match.group(3).upper()}"

                    return ExtractedVariant(
                        gene=gene,
                        variant_type="substitution",
                        location=location,
                        nomenclature_style="shorthand" if "." not in remainder else "hgvs",
                        confidence=0.90,
                        raw_input=raw_variant,
                        notes="Substitution detected"
                    )
        
        # Check insertion
        for pattern in self.insertion_patterns:
            match = re.search(pattern, remainder, re.IGNORECASE)
            if match:
                return ExtractedVariant(
                    gene=gene,
                    variant_type="insertion",
                    location="exon_20",
                    nomenclature_style="shorthand",
                    confidence=0.85,
                    raw_input=raw_variant,
                    notes="Insertion detected"
                )
        
        # Check fusion
        if "-" in remainder and "fusion" in remainder.lower():
            return ExtractedVariant(
                gene=gene,
                variant_type="fusion",
                location="fusion",
                nomenclature_style="shorthand",
                confidence=0.90,
                raw_input=raw_variant,
                notes="Fusion detected"
            )
        
        # Fallback: Generic variant
        return ExtractedVariant(
            gene=gene,
            variant_type="unknown",
            location="unknown",
            nomenclature_style="unknown",
            confidence=0.5,
            raw_input=raw_variant,
            notes="Could not determine specific variant type"
        )
