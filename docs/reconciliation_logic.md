# OncoReconcile AI: Reconciliation Logic Documentation

## Overview
The reconciliation logic in OncoReconcile AI combines VICC Normalizer API results with public evidence APIs (HGNC, ClinVar, CIViC) to produce canonical, explainable, and auditable gene/variant normalization. The process is designed for robustness, provenance, and human review support.

---

## 1. Input Handling
- Accepts an `original_input` (gene or variant name, possibly ambiguous) and `entity_type` ("gene", "variant", or "disease").
- Preserves the original input for audit trail.

---

## 2. VICC Normalization
- Calls VICC Normalizer API (live or cached) for gene/variant/disease normalization:
  - `normalize_gene()` for genes
  - `normalize_variation()` for variants
  - `normalize_disease()` for diseases
- If VICC returns a canonical normalization, proceeds to evidence lookup.
- If VICC fails, marks as `cannot_reconcile` and requires human review.

---

## 3. Evidence Retrieval (Public APIs)
- **Genes:**
  - Uses HGNC API via `HGNCEvidenceProvider` to retrieve canonical gene evidence.
  - If found, attaches evidence, sets high confidence, and explains normalization.
  - If not found, uses cached/demo mapping and flags for human review.
- **Variants:**
  - Uses ClinVar API via `ClinVarEvidenceProvider` for clinical variant evidence.
  - If not found, attempts multi-source evidence resolution (ClinVar, CIViC) with synonym expansion (e.g., canonical, input, gene+variant, stripped forms).
  - If still not found, uses cached/demo mapping and flags for human review.
- **Fallback:**
  - If no canonical normalization or evidence is found, marks as unresolved and requires human review.

---

## 4. Output Schema
- Returns a dictionary with:
  - `original_input`, `entity_type`, `canonical_gene`, `canonical_variant`, `canonical_representation`
  - `normalization_source`, `normalization_mode` (live, cached, fallback)
  - `confidence`, `evidence_sources`, `explainability`, `requires_human_review`, `cannot_reconcile`, `status`, `audit_trail`
- Includes debug info if enabled.

---

## 5. Explainability & Provenance
- Every step is logged in `audit_trail`.
- `explainability` field summarizes how normalization/evidence was achieved.
- `evidence_sources` includes URLs and provenance for each evidence item.
- If normalization or evidence is incomplete, output flags for human review.

---

## 6. Example Flow (Variant)
1. Input: "EGFR Ex19del", entity_type: "variant"
2. VICC normalization: "EGFR exon 19 deletion"
3. ClinVar evidence lookup: found, attaches ClinVar record
4. Output: canonical representation, evidence, explainability, audit trail

If evidence not found:
- Tries synonym expansion and multi-source (CIViC)
- If still not found, uses cached mapping, lowers confidence, flags for review

---

## 7. Key Files
- `src/services/reconciliation_service.py`: Main orchestration logic
- `src/connectors/vicc_client.py`: VICC API client (live/cached/fallback)
- `src/services/evidence/provider_router.py`: Routes evidence queries
- `src/services/evidence/hgnc_provider.py`: HGNC gene evidence
- `src/services/evidence/clinvar_provider.py`: ClinVar variant evidence
- `src/connectors/civic_client.py`: CIViC evidence (fallback)
- `src/services/evidence_resolution_service.py`: Multi-source evidence fallback

---

## 8. Human Review
- Any case with incomplete normalization or evidence is flagged for human review with clear explainability and audit trail.

---

This documentation summarizes the current reconciliation logic using VICC and public APIs in OncoReconcile AI.
