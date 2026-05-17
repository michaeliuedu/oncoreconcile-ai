"""Variant Normalizer - Variant notation standardization"""


def normalize_variant_notation(
    gene: str,
    variant_input: str,
) -> Dict[str, str]:
    """
    Normalize variant notation to HGVS standard
    
    Args:
        gene: Canonical gene name
        variant_input: Raw variant notation
        
    Returns:
        Dictionary with HGVS notation
    """
    
    # Placeholder for MVP
    return {
        "hgvs_dna": "TBD",
        "hgvs_protein": "TBD",
    }


from typing import Dict
