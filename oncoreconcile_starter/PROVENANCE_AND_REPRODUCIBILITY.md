# Data Provenance, Synthesis, and Reproducibility

This document describes the provenance, synthesis process, and reproducibility considerations for the files in the `oncoreconcile_starter/` data package. This ensures transparency, ethical use, and enables future teams to reproduce or extend the dataset.

---

## Overview

- **No direct downloads:** None of the files are raw exports from a single public database.
- **Curation & synthesis:** All files were curated and synthesized using public biomedical standards, literature, and known mutation patterns.
- **Synthetic data:** All patient records and reports are synthetic, created to mimic real-world patterns without using actual patient data.

---

## File-by-File Provenance Table

| File                         | Derived/Informed From                                        | Public URLs         |
| ---------------------------- | ------------------------------------------------------------ | ------------------- |
| oncology_variants_master.csv | TCGA, GENIE, ClinVar, HGVS, oncology literature patterns     | GDC, GENIE, ClinVar |
| gene_aliases.csv             | HGNC gene alias tables                                       | HGNC                |
| variant_synonyms.csv         | HGVS nomenclature, ClinVar, oncology reporting shorthand     | HGVS, ClinVar       |
| evidence_lookup.json         | ClinVar, CIViC, OncoKB-style evidence                        | ClinVar, CIViC      |
| synthetic_reports/*          | Synthetic only (human-generated realistic templates)         | N/A                 |

---

## Synthesis and Curation Process

### 1. oncology_variants_master.csv
- **Inspired by:** TCGA (GDC), AACR GENIE, ClinVar, HGVS, oncology literature.
- **Process:**
  - Identified common NSCLC mutations and biomarker patterns from public sources.
  - Created synthetic patient records and variant combinations using real-world mutation patterns and nomenclature.
  - Manually curated and normalized rows to benchmark-style format.
  - Added synthetic provenance and evidence fields.

### 2. gene_aliases.csv
- **Inspired by:** HGNC gene alias tables.
- **Process:**
  - Selected a subset of real oncology gene aliases from HGNC downloads.
  - Manually curated to include only relevant aliases for demo/testing.

### 3. variant_synonyms.csv
- **Inspired by:** HGVS nomenclature, ClinVar, oncology shorthand.
- **Process:**
  - Compiled real-world variant representations and synonyms.
  - Created semantic equivalence mappings and oncology shorthand examples for AI testing.

### 4. evidence_lookup.json
- **Inspired by:** ClinVar, CIViC, OncoKB.
- **Process:**
  - Created simplified, synthetic evidence records for demo and explainability.
  - Aggregated evidence fields to mimic real clinical actionability concepts.

### 5. synthetic_reports/
- **Source:** Entirely synthetic.
- **Process:**
  - Generated using realistic wording and mutation combinations based on typical pathology and molecular diagnostics reports.

---

## Reproducibility Notes

- **Manual curation:** The process involved manual review and synthesis, so exact reproduction may require following the steps above and using the same public sources.
- **AI assistance:** Some synthetic data (e.g., reports, variant combinations) may have been generated using language models (e.g., ChatGPT) with prompts based on real-world patterns.
- **No patient data:** All data is synthetic or derived from public, non-identifiable sources.
- **Future extension:** Teams can extend or regenerate the dataset by:
  - Downloading the latest public gene/variant tables from HGNC, ClinVar, GDC, GENIE, etc.
  - Using the same synthesis logic and curation steps described above.
  - Optionally, using AI models to generate new synthetic reports or variant combinations.

---

## References
- [GDC Portal](https://portal.gdc.cancer.gov/)
- [TCGA Overview](https://www.cancer.gov/ccg/research/genome-sequencing/tcga)
- [AACR GENIE](https://www.aacr.org/professionals/research/aacr-project-genie/)
- [GENIE cBioPortal](https://genie.cbioportal.org/)
- [ClinVar](https://www.ncbi.nlm.nih.gov/clinvar/)
- [HGNC Downloads](https://www.genenames.org/download/)
- [HGVS](https://hgvs-nomenclature.org/)
- [CIViC](https://civicdb.org/)
- [OncoKB](https://www.oncokb.org/)

---

For questions or to reproduce the dataset, see the above process and references, or contact the project maintainers.
