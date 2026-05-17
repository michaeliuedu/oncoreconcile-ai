"""Gene Normalizer - Gene symbol standardization"""


def normalize_gene_symbol(gene_input: str) -> str:
    """Normalize gene symbol to canonical HGNC form"""
    
    # Common aliases
    aliases = {
        "EGF": "EGFR",
        "HER1": "EGFR",
        "ERBB": "EGFR",
        "B-RAF": "BRAF",
        "HER2": "ERBB2",
        "NEU": "ERBB2",
        "K-RAS": "KRAS",
        "HGFR": "MET",
    }
    
    gene_upper = gene_input.upper().strip()
    return aliases.get(gene_upper, gene_upper)
