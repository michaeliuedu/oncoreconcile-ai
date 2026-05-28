"""
VICC Normalizer API client for OncoReconcile AI.
Supports live and cached/mock modes. Handles errors, timeouts, and wraps results for demo reliability.
"""

import requests
import json
from typing import Optional
from src.connectors.vicc_config import VICC_GENE_URL, VICC_VARIANT_URL, VICC_DISEASE_URL, TIMEOUT, USE_CACHE, DEBUG, CACHE_PATH

# --- Load cache ---
def load_cache():
    try:
        with open(CACHE_PATH, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

CACHE = load_cache()

# --- Client functions ---

def normalize_gene(query: str) -> Optional[dict]:
    if USE_CACHE and query in CACHE.get("gene", {}):
        result = dict(CACHE["gene"][query])
        result["normalization_mode"] = "cached"
        if DEBUG:
            result["debug"] = {"api_called": False, "endpoint": None, "raw_response": result}
        return result
    try:
        r = requests.get(VICC_GENE_URL, params={"q": query}, timeout=TIMEOUT)
        r.raise_for_status()
        data = r.json()
        data["normalization_mode"] = "live"
        if DEBUG:
            data["debug"] = {"api_called": True, "endpoint": VICC_GENE_URL, "raw_response": data}
        return data
    except Exception as e:
        fallback = {"match": False, "normalization_mode": "fallback"}
        if DEBUG:
            fallback["technical_error"] = str(e)
        return fallback


def normalize_variation(query: str) -> Optional[dict]:
    if USE_CACHE and query in CACHE.get("variant", {}):
        result = dict(CACHE["variant"][query])
        result["normalization_mode"] = "cached"
        # Extract canonical_gene if possible
        if "normalized" in result and result["normalized"]:
            result["canonical_gene"] = extract_gene_from_variant(result["normalized"])
        if DEBUG:
            result["debug"] = {"api_called": False, "endpoint": None, "raw_response": result}
        return result
    try:
        r = requests.get(VICC_VARIANT_URL, params={"q": query}, timeout=TIMEOUT)
        r.raise_for_status()
        data = r.json()
        data["normalization_mode"] = "live"
        if "normalized" in data and data["normalized"]:
            data["canonical_gene"] = extract_gene_from_variant(data["normalized"])
        if DEBUG:
            data["debug"] = {"api_called": True, "endpoint": VICC_VARIANT_URL, "raw_response": data}
        return data
    except Exception as e:
        fallback = {"match": False, "normalization_mode": "fallback"}
        if DEBUG:
            fallback["technical_error"] = str(e)
        return fallback


def normalize_disease(query: str) -> Optional[dict]:
    if USE_CACHE and query in CACHE.get("disease", {}):
        result = dict(CACHE["disease"][query])
        result["normalization_mode"] = "cached"
        if DEBUG:
            result["debug"] = {"api_called": False, "endpoint": None, "raw_response": result}
        return result
    try:
        r = requests.get(VICC_DISEASE_URL, params={"q": query}, timeout=TIMEOUT)
        r.raise_for_status()
        data = r.json()
        data["normalization_mode"] = "live"
        if DEBUG:
            data["debug"] = {"api_called": True, "endpoint": VICC_DISEASE_URL, "raw_response": data}
        return data
    except Exception as e:
        fallback = {"match": False, "normalization_mode": "fallback"}
        if DEBUG:
            fallback["technical_error"] = str(e)
        return fallback

# --- Helper: extract canonical_gene from variant string ---
def extract_gene_from_variant(variant_str: str) -> Optional[str]:
    # Simple heuristic: first token before space or p. is gene
    if not variant_str:
        return None
    tokens = variant_str.split()
    if tokens:
        gene = tokens[0]
        # Remove 'p.' or 'c.' if present
        if gene.endswith((':', '.', ',')):
            gene = gene.rstrip(':.',)
        return gene
    return None
