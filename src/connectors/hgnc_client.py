"""HGNC Client - Gene nomenclature validation

Interfaces with the HUGO Gene Nomenclature Committee API for:
- Gene symbol validation
- HGNC ID lookup
- Alias resolution
"""

from typing import Optional, Dict, Any
import json


class HGNCClient:
    """HGNC gene database API client"""

    def __init__(self):
        """Initialize HGNC client"""
        self.api_url = "https://rest.genenames.org/search"
        # Cache for MVP
        self.cache = self._build_cache()

    def search(self, gene_symbol: str) -> Optional[Dict[str, Any]]:
        """
        Search HGNC for gene information
        
        Args:
            gene_symbol: Gene symbol to search
            
        Returns:
            Gene information dictionary or None
        """
        # For MVP, use cached data
        return self.cache.get(gene_symbol.upper())

    def validate_gene(self, gene_symbol: str) -> bool:
        """Check if gene symbol is valid HGNC"""
        return gene_symbol.upper() in self.cache

    def get_aliases(self, gene_symbol: str) -> list:
        """Get known aliases for gene"""
        info = self.search(gene_symbol)
        return info.get("aliases", []) if info else []

    @staticmethod
    def _build_cache() -> Dict[str, Dict[str, Any]]:
        """Build cached gene data for MVP"""
        return {
            "EGFR": {
                "symbol": "EGFR",
                "hgnc_id": 3236,
                "entrez_id": 1956,
                "aliases": ["EGF", "HER1", "ERBB"],
                "name": "Epidermal Growth Factor Receptor",
                "locus": "7p11.2"
            },
            "BRAF": {
                "symbol": "BRAF",
                "hgnc_id": 1097,
                "entrez_id": 673,
                "aliases": ["B-RAF", "BRAF1"],
                "name": "B-Raf Proto-Oncogene",
                "locus": "7q34"
            },
            "ERBB2": {
                "symbol": "ERBB2",
                "hgnc_id": 3236,
                "entrez_id": 2064,
                "aliases": ["HER2", "NEU"],
                "name": "Receptor Tyrosine-Protein Kinase erbB-2",
                "locus": "17q12"
            },
            "KRAS": {
                "symbol": "KRAS",
                "hgnc_id": 6407,
                "entrez_id": 3845,
                "aliases": ["K-RAS", "KRAS1"],
                "name": "Kirsten Rat Sarcoma Viral Oncogene Homolog",
                "locus": "12p12.1"
            },
            "ALK": {
                "symbol": "ALK",
                "hgnc_id": 427,
                "entrez_id": 238,
                "aliases": ["CD246"],
                "name": "Anaplastic Lymphoma Kinase",
                "locus": "2p23.2"
            },
            "MET": {
                "symbol": "MET",
                "hgnc_id": 6973,
                "entrez_id": 4233,
                "aliases": ["HGFR"],
                "name": "MET Proto-Oncogene",
                "locus": "7q31.2"
            },
        }
