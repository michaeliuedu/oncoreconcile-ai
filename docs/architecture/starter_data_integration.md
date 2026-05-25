# Starter Data Integration

The `oncoreconcile_starter/` directory contains synthetic NSCLC-focused data that was generated as a seed package for developing and evaluating OncoReconcile AI. It is not clinical data and contains no real patient identifiers.

## Purpose

Use the starter data as a development benchmark for:

- Gene alias reconciliation
- Variant synonym reconciliation
- Evidence hint display
- Human review routing
- Extraction from synthetic report text

## File Roles

| Starter file | Intended use |
| --- | --- |
| `oncology_variants_master.csv` | Gold-truth evaluation rows with raw inputs, expected normalized outputs, source provenance, ambiguity flags, and expected actions. |
| `gene_aliases.csv` | Additional HGNC-style aliases to merge into `data/reference/v0.1/gene_aliases.csv`. |
| `variant_synonyms.csv` | Variant synonym benchmark and lookup source for deterministic normalization. |
| `evidence_lookup.json` | Evidence-oriented display hints keyed by canonical gene and variant. |
| `synthetic_reports/` | Synthetic report text for extraction and end-to-end workflow tests. |

## Integration Plan

1. Treat `data/reference/v0.1/` as the runtime source of truth.
2. Merge useful starter gene aliases into `data/reference/v0.1/gene_aliases.csv`.
3. Load `data/reference/v0.1/variant_synonyms.csv` in `VariantNormalizer` before falling back to hardcoded MVP mappings.
4. Use selected rows from `oncoreconcile_starter/oncology_variants_master.csv` as regression tests.
5. Keep ambiguous rows routed to human review rather than forcing overconfident automatic reconciliation.

## Current Scope

The current implementation uses deterministic CSV-backed reconciliation for gene aliases and variant synonyms. It is appropriate for prototype evaluation, not clinical use. Rows with structural variants, copy-number alterations, splice ambiguity, or unspecified fusion partners should preserve review flags and remain human-governed.
