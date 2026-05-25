# OncoReconcile AI Starter Input Data Package

Focus cancer: Non-Small Cell Lung Cancer (NSCLC).

Files:
- oncology_variants_master.csv: main starter dataset for backend, AI, and frontend.
- gene_aliases.csv: small HGNC-style gene alias mapping.
- variant_synonyms.csv: synonym benchmark for variant reconciliation.
- evidence_lookup.json: evidence-oriented lookup objects for app development.
- synthetic_reports/: synthetic text reports for extraction testing.

Important columns in oncology_variants_master.csv:
- gene_raw, variant_raw: messy input.
- gene_normalized_expected, variant_normalized_expected: gold truth for evaluation.
- source_system, source_text: provenance.
- clinvar_evidence_hint, civic_evidence_hint: evidence hints to display and later replace with live API results.
- ambiguity_flag, expected_action: supports human-in-the-loop review.

Suggested first demo workflow:
1. Load oncology_variants_master.csv.
2. Normalize gene using gene_aliases.csv.
3. Reconcile variant using variant_synonyms.csv and/or embeddings.
4. Attach evidence using evidence_lookup.json.
5. Show source_text + evidence + confidence in UI.


## Data Sources and Provenance

This starter data package and the OncoReconcile AI system use the following data sources:

1. **CIViC (Clinical Interpretation of Variants in Cancer)**  
	- Used for: Cancer variant interpretations, treatment assertions, evidence summaries.  
	- API: https://civicdb.org/api/v2

2. **ClinVar (NCBI)**  
	- Used for: Clinical significance data, variant accession lookups.  
	- API: https://eutils.ncbi.nlm.nih.gov/entrez/eutils

3. **HGNC (HUGO Gene Nomenclature Committee)**  
	- Used for: Gene symbol validation, HGNC ID lookup, alias resolution.  
	- API: https://rest.genenames.org/search

4. **Synthetic/Curated Data**  
	- Files: `oncology_variants_master.csv`, `gene_aliases.csv`, `variant_synonyms.csv`, `evidence_lookup.json`, and `synthetic_reports/`  
	- Purpose: Development, benchmarking, and demo (not clinical or real patient data).  
	- Provenance: Curated by project team, with evidence hints and source columns referencing CIViC and ClinVar.

Note: This package is synthetic/curated for development. It is not clinical advice and contains no real patient identifiers.
