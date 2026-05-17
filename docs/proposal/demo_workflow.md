# Demonstration Workflow: EGFR Exon 19 Deletion Reconciliation

This document walks through a complete end-to-end workflow of the OncoReconcile AI system using a real-world example: reconciling "EGFR Ex19del" from a local lab report.

---

## Scenario

A genomics lab receives a variant report from their next-gen sequencing (NGS) pipeline:

```
Sample ID: PATIENT_001
Gene: EGFR
Variant: Ex19del
Tissue: Lung (NSCLC)
NGS Coverage: 500x
VAF: 45%
```

They want to:
1. **Standardize** this variant notation
2. **Find** all equivalent representations in their knowledge base
3. **Retrieve** clinical evidence and treatment implications
4. **Get human expert confirmation** before updating their records

**Objective**: Map "EGFR Ex19del" → canonical representation with full audit trail.

---

## Workflow Stages

### Stage 1: Extraction (Extraction Agent)

**Input:**
```json
{
  "raw_variant": "EGFR Ex19del",
  "source": "local_lab_ngs_pipeline",
  "timestamp": "2026-05-17T14:32:00Z",
  "tissue": "lung_nsclc",
  "vaf": 0.45,
  "coverage": 500
}
```

**Agent Action:**
The Extraction Agent parses the raw variant string to identify:
- Gene symbol: `EGFR`
- Variant type: `deletion`
- Location: `exon_19`
- Nomenclature style: "shorthand" (not HGVS)

**Output:**
```json
{
  "extracted_components": {
    "gene": "EGFR",
    "variant_type": "deletion",
    "location": "exon_19",
    "nomenclature_style": "shorthand"
  },
  "confidence": 0.95,
  "extraction_notes": "Clear exon-level deletion designation"
}
```

---

### Stage 2: Normalization (Normalization Agent)

**Input:** Extracted components

**Agent Action:**
The Normalization Agent:
1. **Gene Normalization**: Maps "EGFR" → canonical HGNC gene name "EGFR", HGNC ID 3236
2. **Variant Normalization**: 
   - Maps "exon_19" to transcript NM_005228.4
   - Retrieves exon 19 boundaries: c.2235-2249
   - Determines protein impact: p.E746_A750del
   - Generates HGVS nomenclature: c.2235_2249del15
3. **Creates canonical variant ID**: `EGFR|exon_19_deletion`

**Output:**
```json
{
  "canonical_variant_id": "EGFR|exon_19_deletion",
  "canonical_gene": {
    "symbol": "EGFR",
    "hgnc_id": 3236,
    "entrez_gene_id": 1956
  },
  "transcript": "NM_005228.4",
  "genomic_coordinates": {
    "chr": "7",
    "start": 55086714,
    "end": 55086728,
    "build": "GRCh38"
  },
  "hgvs_nomenclature": {
    "dna": "c.2235_2249del15",
    "protein": "p.E746_A750del"
  },
  "normalization_confidence": 0.99,
  "data_sources": ["HGNC", "RefSeq"]
}
```

---

### Stage 3: Retrieval (Retrieval Agent)

**Input:** Canonical variant ID

**Agent Action:**
The Retrieval Agent queries the knowledge base (KB) for:
1. Exact canonical matches
2. Semantic matches (DNA, protein, nomenclature variants)
3. Clinical evidence linked to this variant

**Knowledge Base Query:**
```
SELECT * FROM variants 
WHERE canonical_id = 'EGFR|exon_19_deletion' 
  OR protein_change = 'p.E746_A750del' 
  OR dna_change = 'c.2235_2249del15'
  OR aliases LIKE '%Ex19del%'
```

**Candidates Retrieved:**
```json
{
  "candidates": [
    {
      "kb_id": "var_egfr_001",
      "canonical_id": "EGFR|exon_19_deletion",
      "aliases": ["EGFR Ex19del", "EGFR exon_19_del", "EGFR L858R exon_19"],
      "protein_change": "p.E746_A750del",
      "clinical_significance": "Sensitizing (TKI-responsive)",
      "approvals": 156,
      "rejections": 0,
      "last_updated": "2026-04-15"
    },
    {
      "kb_id": "var_egfr_002",
      "canonical_id": "EGFR|exon_19_deletion",
      "protein_change": "p.E746_A750del",
      "dna_change": "c.2235_2249del15",
      "source": "ClinVar RCV000045689",
      "clinical_significance": "Pathogenic",
      "associations": ["Lung adenocarcinoma", "EGFR TKI sensitivity"]
    }
  ],
  "evidence_links": [
    {
      "source": "NCCN Guidelines v2.2026",
      "title": "EGFR Exon 19 Deletion: Tier 1 evidence for Gefitinib/Erlotinib/Afatinib",
      "url": "https://nccn.org/professionals/..."
    },
    {
      "source": "CIViC",
      "evidence_id": "eid1234",
      "title": "EGFR exon 19 deletion predicts response to EGFR TKI",
      "assertion": "PREDICTIVE"
    }
  ]
}
```

---

### Stage 4: Reasoning (Reasoning Agent + LLM)

**Input:** Candidate matches + clinical evidence

**Agent Action:**
The Reasoning Agent uses an LLM (with prompt engineering) to:
1. Assess semantic alignment between input and candidates
2. Summarize clinical significance
3. Identify potential treatment implications
4. Flag any conflicts or ambiguities

**LLM Prompt:**
```
You are a genomics expert assistant. Given the following information:

INPUT VARIANT: EGFR Ex19del (exon 19 deletion, lung tissue)
CANONICAL FORM: EGFR|exon_19_deletion (c.2235_2249del15, p.E746_A750del)

KNOWLEDGE BASE MATCHES:
- 156 prior approvals, 0 rejections
- Clinical significance: Sensitizing (TKI-responsive)
- NCCN Guidelines: Tier 1 evidence for EGFR TKI agents

TASK: 
1. Assess clinical validity of this match
2. Identify key treatment implications
3. Rate confidence (0-1 scale)

CONSTRAINTS:
- This is a research tool, not clinical software
- Provide summary, not medical recommendations
```

**LLM Output:**
```json
{
  "reasoning_summary": {
    "semantic_alignment": "Perfect canonical match. EGFR Ex19del is a well-known shorthand for exon 19 deletion.",
    "clinical_context": "EGFR exon 19 deletion is a hallmark activating mutation in lung adenocarcinoma. Associated with high response rates to EGFR kinase inhibitors (Gefitinib, Erlotinib, Afatinib). Tier 1 evidence per NCCN guidelines.",
    "evidence_quality": "Extensive literature support with 156 prior KB approvals, zero rejections. ClinVar classified as 'Pathogenic'. NCCN Tier 1.",
    "treatment_relevance": "Strong predictive value for EGFR TKI response in lung adenocarcinoma (>60% response rate in clinical trials).",
    "risk_factors": "None identified. This is a well-characterized variant."
  },
  "confidence_score": 0.96,
  "recommendation": "HIGH CONFIDENCE. Recommend approval for KB update."
}
```

---

### Stage 5: Confidence Scoring (Confidence Agent)

**Input:** 
- Deterministic matching score
- Semantic similarity (from embeddings, if available)
- LLM reasoning confidence
- Historical approval data

**Agent Action:**
The Confidence Agent computes a composite score:

```
Score Components:
1. Deterministic Score: 1.0
   - Exact canonical match: 1.0
   - Nomenclature consistency: 1.0
   - Gene validation (HGNC): 1.0
   
2. Semantic Similarity Score: 0.99
   - Shorthand to canonical: 0.99 (SapBERT embedding)
   - Protein-level match: 0.98
   - DNA-level match: 0.99
   
3. LLM Reasoning Score: 0.96
   - Clinical context analysis: 0.97
   - Evidence quality: 0.96
   - Treatment relevance: 0.95
   
4. Historical Approval Score: 0.98
   - Prior approvals: 156
   - Prior rejections: 0
   - Approval rate: 100%
   
Composite Score = (1.0 + 0.99 + 0.96 + 0.98) / 4 = 0.9825 ≈ 0.98
```

**Output:**
```json
{
  "composite_confidence_score": 0.98,
  "confidence_category": "Very High",
  "score_breakdown": {
    "deterministic": {"score": 1.0, "weight": 0.30},
    "semantic_similarity": {"score": 0.99, "weight": 0.25},
    "llm_reasoning": {"score": 0.96, "weight": 0.25},
    "historical_approval": {"score": 0.98, "weight": 0.20}
  },
  "recommendation": "AUTO-ROUTE TO FAST TRACK (confidence > 0.95)"
}
```

---

### Stage 6: Human Review Queue (Review Agent)

**Input:** High-confidence reconciliation

**Agent Action:**
The Review Agent:
1. Evaluates confidence score and historical precedent
2. Routes to appropriate human reviewer
3. Generates a summary brief

**Assignment Logic:**
```
IF confidence_score > 0.95 AND historical_approvals > 100 AND rejections == 0:
  → Route to "Fast Track" queue (1-2 reviewers)
  → Priority: "standard"
  → Suggested review time: 2-5 minutes
  
ELSE IF confidence_score > 0.80:
  → Route to "Standard" queue
  → Priority: "medium"
  
ELSE:
  → Route to "Escalation" queue
  → Priority: "high"
```

**Review Queue Entry:**
```json
{
  "review_id": "rev_20260517_001",
  "status": "pending_approval",
  "queue": "fast_track",
  "priority": "standard",
  "assigned_reviewer": [
    {"id": "dr_chen", "name": "Dr. Sarah Chen, MD PhD", "specialty": "Clinical Genomics"},
    {"id": "prof_kim", "name": "Prof. James Kim, PhD", "specialty": "Computational Biology"}
  ],
  "input_variant": "EGFR Ex19del",
  "canonical_variant": "EGFR|exon_19_deletion",
  "confidence_score": 0.98,
  "summary": {
    "match_quality": "Perfect canonical match",
    "clinical_significance": "Well-characterized sensitizing mutation",
    "evidence": "156 prior approvals, NCCN Tier 1, strong literature support",
    "recommendation": "Approve for KB update"
  },
  "created_at": "2026-05-17T14:35:00Z",
  "estimated_review_time": "3 minutes"
}
```

**Dr. Chen's Review Interface:**
```
╔════════════════════════════════════════════════════════╗
║          OncoReconcile AI - Review Queue               ║
╠════════════════════════════════════════════════════════╣
║                                                         ║
║  Review ID: rev_20260517_001                           ║
║  Input: EGFR Ex19del (local lab)                       ║
║  Confidence: 98% (Very High)                           ║
║                                                         ║
║  ─────────────────────────────────────────────────    ║
║  SUMMARY:                                               ║
║  ─────────────────────────────────────────────────    ║
║  This reconciliation maps "EGFR Ex19del" to the       ║
║  canonical variant "EGFR|exon_19_deletion"            ║
║  (c.2235_2249del15, p.E746_A750del).                  ║
║                                                         ║
║  CLINICAL CONTEXT:                                      ║
║  - Hallmark sensitizing mutation in lung adenoca.      ║
║  - 156 prior KB approvals (0 rejections)              ║
║  - NCCN Tier 1 evidence                               ║
║  - Strong predictor of EGFR TKI response               ║
║                                                         ║
║  ─────────────────────────────────────────────────    ║
║  REVIEWER ACTION:                                       ║
║  [ ✓ APPROVE ] [ ○ REQUEST CHANGES ] [ ✗ REJECT ]    ║
║                                                         ║
║  Curation Notes (optional):                            ║
║  ┌─────────────────────────────────────────────────┐  ║
║  │ Clinically validated sensitizing mutation.      │  ║
║  │ Aligns with current NCCN guidelines. Strong      │  ║
║  │ evidence base. Ready for clinical integration.  │  ║
║  └─────────────────────────────────────────────────┘  ║
║                                                         ║
║  [ APPROVE ]                                           ║
╚════════════════════════════════════════════════════════╝
```

---

### Stage 7: Approval & KB Update (Governance)

**Dr. Chen's Decision:** ✅ **APPROVED**

**Curation Notes:** 
> "Clinically validated sensitizing mutation. Aligns with current NCCN guidelines (Tier 1 evidence). Strong literature support (156 prior approvals, 0 rejections). Ready for knowledge base integration."

**Update Record:**
```json
{
  "update_id": "upd_20260517_001",
  "timestamp": "2026-05-17T14:38:45Z",
  "decision": "APPROVED",
  "reviewer": {
    "id": "dr_chen",
    "name": "Dr. Sarah Chen, MD PhD",
    "email": "s.chen@institution.org",
    "institution": "Research Hospital"
  },
  "reconciliation_details": {
    "input_variant": "EGFR Ex19del",
    "canonical_variant": "EGFR|exon_19_deletion",
    "confidence_score": 0.98
  },
  "kb_update": {
    "action": "ADD_ALIAS",
    "canonical_id": "EGFR|exon_19_deletion",
    "new_alias": "EGFR Ex19del",
    "kb_version_from": "0.1",
    "kb_version_to": "0.1.1"
  },
  "curation_notes": "Clinically validated sensitizing mutation. Aligns with current NCCN guidelines (Tier 1 evidence). Strong literature support (156 prior approvals, 0 rejections). Ready for knowledge base integration.",
  "audit_trail": {
    "extracted_at": "2026-05-17T14:32:00Z",
    "normalized_at": "2026-05-17T14:33:00Z",
    "retrieved_at": "2026-05-17T14:34:00Z",
    "reasoned_at": "2026-05-17T14:35:00Z",
    "scored_at": "2026-05-17T14:36:00Z",
    "reviewed_at": "2026-05-17T14:38:45Z",
    "approved_at": "2026-05-17T14:38:45Z"
  }
}
```

**Updated Knowledge Base Entry:**
```yaml
variant_id: EGFR|exon_19_deletion
hgnc_gene: EGFR
gene_id: 3236
transcript: NM_005228.4

nomenclature:
  hgvs_dna: c.2235_2249del15
  hgvs_protein: p.E746_A750del
  shorthand: EGFR Ex19del
  
aliases:
  - "EGFR Ex19del"
  - "EGFR exon_19_deletion"
  - "EGFR exon19_del"
  - "EGFR c.2235_2249del15"
  - "EGFR p.E746_A750del"

clinical_significance: Sensitizing (TKI-responsive)
nccn_tier: 1

curation:
  total_approvals: 157
  total_rejections: 0
  last_approved_by: Dr. Sarah Chen, MD PhD
  last_approved_at: 2026-05-17T14:38:45Z
  
version_history:
  v0.1: Initial entry
  v0.1.1: Added "EGFR Ex19del" alias (approved 2026-05-17)

created_at: 2026-05-01
updated_at: 2026-05-17
```

---

## End-to-End Timeline

| Stage | Component | Duration | Timestamp |
|-------|-----------|----------|-----------|
| 1. Extraction | Extraction Agent | 0.8s | 14:32:00 → 14:32:01 |
| 2. Normalization | Normalization Agent | 1.2s | 14:32:01 → 14:33:00 |
| 3. Retrieval | Retrieval Agent | 0.5s | 14:33:00 → 14:34:00 |
| 4. Reasoning | LLM Reasoning | 2.0s | 14:34:00 → 14:35:00 |
| 5. Confidence | Confidence Agent | 0.3s | 14:35:00 → 14:36:00 |
| 6. Review Queue | Review Agent | 1.0s | 14:36:00 → 14:36:01 |
| 7. Human Review | Dr. Chen (Expert) | 2min 45s | 14:36:01 → 14:38:45 |
| 8. KB Update | Governance Engine | 0.2s | 14:38:45 → 14:38:46 |

**Total Wall-Clock Time: 2 minutes 46 seconds (AI: ~6 seconds, Human: 2m 45s)**

---

## Key Learnings from This Example

1. **High Confidence Variants Fast-Track**: With 156 prior approvals and perfect canonical match, this variant received fast-track review (~3 min)

2. **Human Remains in Control**: Despite 98% system confidence, expert human judgment was required before KB update

3. **Auditability**: Complete end-to-end trail from raw input through expert approval to KB versioning

4. **Deterministic Foundation**: Normalization is rule-based (not ML-based), ensuring reproducibility

5. **Semantic Augmentation**: LLM and embeddings enhance but don't replace expert judgment

---

## Variation: Low-Confidence Scenario

If this variant had lower confidence (e.g., 0.65), it would:
1. Route to "Standard" or "Escalation" queue
2. Get assigned to multiple experts
3. Generate more detailed reasoning summaries
4. Potentially request additional evidence or manual curation
5. Create a longer review cycle with potential rejection/revision

This human-governed approach ensures that ambiguous or novel variants get appropriate scrutiny.
