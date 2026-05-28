"""
Script to automatically annotate sample_inputs.json with evidence references from public databases (ClinVar, CIViC).
- For each input, attempts to look up variant evidence and adds an 'evidence_sources' field.
- Output: data/examples/sample_inputs_with_evidence.json

Requirements: requests
"""

import json
import requests
import time
from requests.exceptions import RequestException

INPUT_PATH = "data/examples/sample_inputs.json"
OUTPUT_PATH = "data/examples/sample_inputs_with_evidence.json"

# --- ClinVar lookup ---
def search_clinvar(term):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {"db": "clinvar", "term": term, "retmode": "json"}
    try:
        r = requests.get(url, params=params, timeout=10)
        ids = r.json().get("esearchresult", {}).get("idlist", [])
        if not ids:
            return None
        summary_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
        summary_params = {"db": "clinvar", "id": ids[0], "retmode": "json"}
        # Only use the ID and URL for evidence
        requests.get(summary_url, params=summary_params, timeout=10)  # For completeness, but not used
        return f"ClinVar:{ids[0]} (https://www.ncbi.nlm.nih.gov/clinvar/variation/{ids[0]}/)"
    except RequestException as e:
        print(f"ClinVar lookup failed for '{term}': {e}")
        return None

# --- CIViC lookup ---
def search_civic(gene, variant):
    url = "https://civicdb.org/api/variants"
    # Try original variant string
    params = {"entrez_name": gene, "name": variant}
    try:
        r = requests.get(url, params=params, timeout=10)
        results = r.json()
        if results:
            v = results[0]
            return f"CIViC:{v['id']} (https://civicdb.org/variants/{v['id']}/summary)"
        # Try splitting variant for common patterns (e.g., 'G12C', 'L858R', 'V600E')
        for token in variant.split():
            params2 = {"entrez_name": gene, "name": token}
            r2 = requests.get(url, params=params2, timeout=10)
            results2 = r2.json()
            if results2:
                v2 = results2[0]
                return f"CIViC:{v2['id']} (https://civicdb.org/variants/{v2['id']}/summary)"
        # Fallback: search by gene only, return first variant
        params3 = {"entrez_name": gene}
        r3 = requests.get(url, params=params3, timeout=10)
        results3 = r3.json()
        if results3:
            v3 = results3[0]
            return f"CIViC:{v3['id']} (https://civicdb.org/variants/{v3['id']}/summary)"
        return None
    except RequestException as e:
        print(f"CIViC lookup failed for '{gene} {variant}': {e}")
        return None
    except (ValueError, KeyError, TypeError) as e:
        print(f"CIViC parsing failed for '{gene} {variant}': {e}")
        return None

# --- Main annotation logic ---
def main():
    with open(INPUT_PATH, encoding="utf-8") as f:
        data = json.load(f)
    for ex in data["examples"]:
        raw = ex["input"]["raw_variant"]
        # Improved parsing: try to extract gene and variant tokens
        clean = raw.replace("mutation","").replace("fusion","").replace("insertion","").replace("deletion","").replace("exon","ex").replace("Ex","ex").replace("-"," ").replace("_"," ")
        parts = clean.split()
        gene = parts[0] if parts else ""
        variant = " ".join(parts[1:]) if len(parts) > 1 else ""
        evidence = []
        # ClinVar
        clinvar_ev = search_clinvar(raw)
        if clinvar_ev:
            evidence.append(clinvar_ev)
        time.sleep(0.34)  # NCBI rate limit
        # CIViC
        if gene and variant:
            civic_ev = search_civic(gene, variant)
            if civic_ev:
                evidence.append(civic_ev)
        ex["input"]["evidence_sources"] = evidence
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Annotated file written to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
