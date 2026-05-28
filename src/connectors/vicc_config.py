"""
Configuration constants for VICC Normalizer integration.
"""
VICC_GENE_URL = "https://normalize.gene.cancervariants.org/api/normalize"
VICC_VARIANT_URL = "https://normalize.variation.cancervariants.org/api/normalize"
VICC_DISEASE_URL = "https://normalize.disease.cancervariants.org/api/normalize"
TIMEOUT = 5
USE_CACHE = True  # Set to False for live API calls
DEBUG = False     # Set to True to include debug/raw response info
CACHE_PATH = "data/reference/vicc_cached_examples.json"
