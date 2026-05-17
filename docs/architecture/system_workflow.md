# Detailed System Workflow

This document describes the interaction between agents and systems in detail.

## State Machine & Agent Interactions

```
STATE: PENDING_SUBMISSION
  ↓
USER: Submit variant via POST /reconcile
  ├─ raw_variant: "EGFR Ex19del"
  ├─ source: "lab_ngs"
  ├─ tissue: "lung"
  └─ metadata: {...}
  ↓
STATE: EXTRACTING
  ↓
EXTRACTION_AGENT.execute()
  ├─ Input: RawVariantInput
  ├─ Parse string using regex + NLP
  ├─ Output: ExtractedVariant {gene, type, location, confidence}
  └─ Update State: extracted_components
  ↓
STATE: NORMALIZING
  ↓
NORMALIZATION_AGENT.execute()
  ├─ Input: ExtractedVariant
  ├─ Call HGNC client: "EGFR" → validate
  ├─ Call RefSeq client: Get transcript context
  ├─ Generate HGVS nomenclature
  ├─ Create canonical_variant_id
  └─ Output: NormalizedVariant
  ↓
STATE: RETRIEVING
  ↓
RETRIEVAL_AGENT.execute()
  ├─ Input: NormalizedVariant
  ├─ Query KB: exact_match(canonical_id)
  ├─ Query KB: semantic_search(embeddings)
  ├─ Rank candidates by relevance
  ├─ Fetch linked clinical evidence
  └─ Output: RetrievedCandidates[]
  ↓
STATE: REASONING
  ↓
REASONING_AGENT.execute()
  ├─ Input: NormalizedVariant, RetrievedCandidates
  ├─ Format prompt with clinical context
  ├─ Call LLM: "Analyze this variant..."
  ├─ Parse LLM response
  └─ Output: ReasoningResult {summary, llm_confidence, recommendation}
  ↓
STATE: SCORING
  ↓
CONFIDENCE_AGENT.execute()
  ├─ Input: All prior outputs
  ├─ Compute deterministic_score
  ├─ Compute semantic_similarity_score
  ├─ Extract llm_score from reasoning
  ├─ Fetch historical_approval_score
  ├─ Compute composite = weighted_average(all_scores)
  └─ Output: ConfidenceScore {score, breakdown, category}
  ↓
STATE: ROUTING
  ↓
REVIEW_AGENT.execute()
  ├─ Input: ConfidenceScore
  ├─ IF score > 0.95 AND historical_approvals > 100:
  │   └─ queue_type = "fast_track", num_reviewers = 1
  ├─ ELSE IF score > 0.80:
  │   └─ queue_type = "standard", num_reviewers = 1-2
  ├─ ELSE:
  │   └─ queue_type = "escalation", num_reviewers = 2+
  ├─ Assign to available experts
  ├─ Generate brief summary
  └─ Output: ReviewQueue entry
  ↓
STATE: QUEUED_FOR_REVIEW
  ↓
HUMAN_REVIEWER.review()
  ├─ View reconciliation details
  ├─ Examine system reasoning
  ├─ Check approval history
  ├─ Make decision: APPROVE | REJECT | REQUEST_CHANGES
  └─ Add curation notes
  ↓
STATE: DECISION_PENDING
  ↓
DECISION: If APPROVE:
  ↓
STATE: APPROVED
  ↓
GOVERNANCE_ENGINE.update_kb()
  ├─ Fetch current KB state
  ├─ Add new alias to canonical variant
  ├─ Increment KB version
  ├─ Create versioned entry
  ├─ Log audit trail:
  │   ├─ reviewer_id: "dr_chen"
  │   ├─ decision: "APPROVED"
  │   ├─ timestamp: "2026-05-17T14:38:45Z"
  │   ├─ curation_notes: "Well-validated variant..."
  │   └─ reasoning_chain: {...}
  ├─ Commit to database
  └─ Return: KBUpdateResult {new_version, update_id}
  ↓
STATE: COMPLETED
  ↓
API.notify_requester()
  ├─ Reconciliation ID: "rec_20260517_001"
  ├─ Status: "APPROVED"
  ├─ Canonical ID: "EGFR|exon_19_deletion"
  └─ KB Version: "0.1.1"
  ↓
USER receives response
  ├─ Via GET /reconcile/rec_20260517_001
  ├─ Or webhook callback (if configured)
  └─ Updates lab system with canonical variant
```

---

## Concurrent Processing & Queuing

### Async Workflow
```
User submits variant
        ↓
API creates ReconciliationJob {id, status, created_at}
        ↓
Job enters async queue
        ↓
API returns immediately: {reconciliation_id, status: "processing"}
        ↓
Workflow processes in background
  • Extraction: ~0.8s
  • Normalization: ~1.2s
  • Retrieval: ~0.5s
  • Reasoning (LLM): ~2.0s (parallel)
  • Confidence: ~0.3s
  • Routing: ~1.0s
  └─ Total: ~6 seconds
        ↓
Review queue updated
        ↓
Expert notified (email/dashboard)
        ↓
Expert reviews (2-10 minutes)
        ↓
KB updated
        ↓
User polls GET /reconcile/{id} → receives final result
```

### Retry Logic
```
External API Call (HGNC, ClinVar, LLM)
        ↓
Success?
  ├─ YES: Continue workflow
  └─ NO: Retry with backoff
        ├─ Attempt 1: Immediate
        ├─ Attempt 2: 1 second delay
        ├─ Attempt 3: 3 seconds delay
        ├─ Attempt 4: 5 seconds delay
        └─ Attempt 5: Fail, use fallback
        
Fallback strategies:
  • HGNC unavailable: Use cached gene list
  • LLM unavailable: Set llm_score = 0.5 (neutral)
  • ClinVar unavailable: Skip evidence retrieval
```

---

## Human Review Queue Management

### Queue Assignment Logic

```python
def assign_reviewer(confidence_score, variant_type, gene):
    """
    Route reconciliation to appropriate reviewer queue.
    """
    
    # High-confidence, well-known variants → Fast-track
    if (confidence_score > 0.95 and 
        is_well_characterized(gene, variant_type)):
        return ReviewQueueType.FAST_TRACK
    
    # Medium confidence → Standard review
    elif confidence_score > 0.80:
        return ReviewQueueType.STANDARD
    
    # Low confidence or novel variants → Escalation
    elif confidence_score > 0.60:
        return ReviewQueueType.ESCALATION
    
    # Very low confidence → Manual curation team
    else:
        return ReviewQueueType.MANUAL_CURATION
```

### Expert Workload Balancing

```
Available Reviewers:
  Dr. Chen (loaded: 5/8) - Oncology Genomics
  Dr. Kim (loaded: 3/8) - Computational Biology
  Dr. Patel (loaded: 6/8) - Molecular Pathology

New Fast-Track Variant (Est. 3 min review):
  → Assign to Dr. Kim (lowest load)

New Standard Variant (Est. 8 min review):
  → Assign to Dr. Chen (medium load, oncology specialist)

New Escalation Variant (Est. 20 min review):
  → Assign to [Dr. Patel, Dr. Chen] (pair review)
```

### Dashboard View (for Reviewers)

```
┌─────────────────────────────────────────────────────────┐
│  OncoReconcile AI - Expert Review Queue                 │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  MY ASSIGNMENTS (Dr. Sarah Chen)                         │
│  ───────────────────────────────────────────────────    │
│                                                           │
│  ┌──────────────────────────────────────────────────┐   │
│  │ Fast-Track (1)          [████░░░░] 1 waiting    │   │
│  │ Standard (3)            [████████] 3 waiting    │   │
│  │ Escalation (1)          [████░░░░] 1 waiting    │   │
│  └──────────────────────────────────────────────────┘   │
│                                                           │
│  RECENT REVIEWS                                          │
│  ───────────────────────────────────────────────────    │
│                                                           │
│  [ ] rec_20260517_001 | EGFR Ex19del | Score: 98%     │
│      ├─ Source: Lab NGS                                 │
│      ├─ Input: "EGFR Ex19del"                           │
│      └─ Canonical: "EGFR|exon_19_deletion"             │
│                                                           │
│      System Recommendation:                              │
│      "Perfect canonical match. 156 prior approvals,     │
│       0 rejections. NCCN Tier 1 evidence. Recommend    │
│       approval for TKI eligibility assessment."         │
│                                                           │
│      [APPROVE] [REQUEST CHANGES] [REJECT]               │
│      ┌──────────────────────────────────────┐           │
│      │ Curation notes (optional):           │           │
│      │ Well-characterized variant. Aligns   │           │
│      │ with NCCN guidelines. Ready for      │           │
│      │ clinical integration.                │           │
│      └──────────────────────────────────────┘           │
│      [SUBMIT]                                            │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

---

## Knowledge Base Update Process

### Versioning Model

```
KB Version Scheme: MAJOR.MINOR[.PATCH]

v0.1 (Initial release)
  └─ 50 canonical variants
  └─ EGFR, BRAF, KRAS core coverage

v0.1.1 (Add alias)
  └─ Add "EGFR Ex19del" as alias for EGFR|exon_19_deletion
  └─ Same canonical variant, improved discoverability

v0.1.2 (Add evidence)
  └─ Link NCCN Guideline 2.2026 to EGFR variants
  └─ Update clinical significance

v0.2 (New variant class)
  └─ Add support for structural variants
  └─ Expand to 100+ genes

v1.0 (Production release)
  └─ Full clinical validation
  └─ Institutional deployment
```

### Update Audit Trail

```json
{
  "update_id": "upd_20260517_001",
  "timestamp": "2026-05-17T14:38:45Z",
  "kb_version_before": "0.1",
  "kb_version_after": "0.1.1",
  "variant_id": "EGFR|exon_19_deletion",
  "update_type": "ADD_ALIAS",
  "change": {
    "added_alias": "EGFR Ex19del",
    "reason": "Map shorthand notation from lab NGS reports"
  },
  "reviewer": {
    "id": "dr_chen",
    "name": "Dr. Sarah Chen, MD PhD",
    "role": "Clinical Genomics Specialist",
    "institution": "Research Hospital"
  },
  "decision_details": {
    "reconciliation_id": "rec_20260517_001",
    "confidence_score": 0.98,
    "curation_notes": "Clinically validated. NCCN Tier 1 evidence.",
    "approval_time": "2026-05-17T14:38:45Z"
  },
  "metadata": {
    "input_source": "lab_ngs",
    "tissue": "lung_nsclc",
    "reasoning_chain": {...}
  },
  "rollback_capability": true,
  "prior_version_snapshot": {...}
}
```

### Rollback Process (if needed)

```
Admin: git-like rollback
  GET /kb-versions → view history
  POST /kb/rollback?version=0.1 → revert to v0.1
  
Audit trail preserved:
  • Original update recorded
  • Rollback reason documented
  • No data loss
```

---

## Error Handling & Recovery

### Grade 1: User Input Errors (4xx HTTP)
```
User submits: "EGFR Ex19del" with invalid tissue "xyz"
        ↓
Validation error: tissue not in enum
        ↓
Response: 422 Unprocessable Entity
{
  "error": "Validation error",
  "detail": "tissue 'xyz' not in allowed values"
}
```

### Grade 2: External Service Errors (retry logic)
```
HGNC API returns 503 Service Unavailable
        ↓
Retry with exponential backoff (5 attempts)
        ↓
All attempts fail
        ↓
Fallback: Use cached gene database (5% staleness)
        ↓
Continue workflow with note: "gene_source: cached"
        ↓
Mark reconciliation as "degraded_mode" in results
```

### Grade 3: Critical System Errors (5xx HTTP)
```
Database connection pool exhausted
        ↓
Error: 500 Internal Server Error
{
  "error": "Database pool exhausted",
  "request_id": "req_abc123",
  "support_contact": "support@oncoreconcile.ai"
}
        ↓
Admin alerted
        ↓
Automatic recovery: restart pool, retry request
```

---

## Monitoring & Observability

### Key Metrics to Track

```
Latency:
  • Extract agent: p50, p95, p99
  • Normalize agent: p50, p95, p99
  • Retrieve agent: p50, p95, p99
  • LLM reasoner: p50, p95, p99 (includes API latency)
  • End-to-end: p50, p95, p99

Throughput:
  • Reconciliations/sec
  • Approved vs rejected ratio
  • KB updates/day

Quality:
  • Confidence score distribution
  • Approval rate by confidence bucket
  • External API success rate
  • Cache hit rate

Audit:
  • Reviews per reviewer (workload)
  • Review time distribution
  • Rejection rate by variant type
```

### Log Aggregation

```
Each workflow step emits structured logs:

{
  "timestamp": "2026-05-17T14:32:00Z",
  "reconciliation_id": "rec_20260517_001",
  "step": "extraction",
  "status": "success",
  "duration_ms": 800,
  "output": {gene: "EGFR", type: "deletion", ...}
}

{
  "timestamp": "2026-05-17T14:33:00Z",
  "reconciliation_id": "rec_20260517_001",
  "step": "normalization",
  "status": "success",
  "duration_ms": 1200,
  "external_calls": [
    {service: "hgnc", latency_ms: 150, cached: false}
  ],
  "output": {canonical_id: "EGFR|exon_19_deletion", ...}
}
```

---

## Security & Access Control

### API Authentication

```
Endpoint: POST /reconcile
Authorization: Bearer {JWT_TOKEN}

Token payload:
{
  "sub": "lab_facility_001",
  "role": "submitter",
  "iat": 1715958000,
  "exp": 1715961600
}
```

### Role-Based Access Control (RBAC)

```
Role: submitter
  • POST /reconcile
  • GET /reconcile/{id} (own submissions only)
  
Role: reviewer
  • GET /review-queue
  • POST /review/{id}/approve
  • POST /review/{id}/reject
  
Role: admin
  • GET /kb-versions
  • POST /kb/rollback
  • GET /audit-log
  • Manage users/roles
```

---

*Last Updated: May 17, 2026*
