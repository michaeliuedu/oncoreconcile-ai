# System Architecture Overview

## Vision

OncoReconcile AI provides a **human-governed, multi-agent system** for semantic reconciliation of oncology variants across heterogeneous data sources. The architecture balances:

- **Automation**: Deterministic rule-based processing + semantic AI
- **Human Control**: Mandatory expert review and approval
- **Auditability**: Complete trails from input to decision
- **Modularity**: Pluggable agents and data sources

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI REST API Layer                        │
│  GET /health │ POST /reconcile │ GET /review-queue │ POST /review/approve
└────────────────────────────────────────────────────────────────┬┘
                                                                    │
┌───────────────────────────────────────────────────────────────────┴──────┐
│                    Multi-Agent Workflow Engine                           │
│                         (LangGraph-inspired)                             │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ 1. EXTRACTION AGENT                                              │   │
│  │    Input: Raw variant string                                     │   │
│  │    Output: Parsed gene, variant type, location                  │   │
│  └────────────────────────┬──────────────────────────────────────────┘   │
│                           ↓                                              │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ 2. NORMALIZATION AGENT                                           │   │
│  │    Connectors: HGNC, RefSeq                                      │   │
│  │    Output: Canonical gene/variant, HGVS nomenclature            │   │
│  └────────────────────────┬──────────────────────────────────────────┘   │
│                           ↓                                              │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ 3. RETRIEVAL AGENT                                               │   │
│  │    KB Search: Semantic + exact match                            │   │
│  │    Output: Candidate variants + evidence                        │   │
│  └────────────────────────┬──────────────────────────────────────────┘   │
│                           ↓                                              │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ 4. REASONING AGENT                                               │   │
│  │    LLM: Analyze clinical context, treatment implications        │   │
│  │    Output: Clinical significance summary                        │   │
│  └────────────────────────┬──────────────────────────────────────────┘   │
│                           ↓                                              │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ 5. CONFIDENCE AGENT                                              │   │
│  │    Scoring: Deterministic + Semantic + LLM + Historical         │   │
│  │    Output: Composite confidence (0-1)                           │   │
│  └────────────────────────┬──────────────────────────────────────────┘   │
│                           ↓                                              │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ 6. REVIEW AGENT                                                  │   │
│  │    Route to human expert based on confidence                    │   │
│  │    Output: Queue assignment, review priority                   │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
                              │
                              ↓
        ┌─────────────────────────────────────┐
        │  HUMAN REVIEW QUEUE                  │
        │  (Streamlit Web Interface)           │
        │                                      │
        │  Fast-Track | Standard | Escalation │
        └──────────────┬──────────────────────┘
                       ↓
        ┌──────────────────────────────────────┐
        │  EXPERT DECISION                     │
        │  [✓ APPROVE] [○ REVISE] [✗ REJECT]  │
        └──────────────┬──────────────────────┘
                       ↓
        ┌──────────────────────────────────────┐
        │  GOVERNANCE ENGINE                   │
        │  • Update KB (versioned)             │
        │  • Log approval chain                │
        │  • Archive for audit trail           │
        └──────────────────────────────────────┘
```

---

## Core Components

### 1. API Layer (FastAPI)
**Purpose**: RESTful interface for variant submission and review

**Key Endpoints**:
- `POST /reconcile` – Submit variant for reconciliation
- `GET /reconcile/{id}` – Status and results
- `GET /review-queue` – List pending expert reviews
- `POST /review/{id}/approve` – Expert approval
- `GET /audit-log` – Approval history

**Technologies**: FastAPI, Pydantic, SQLAlchemy ORM

### 2. Multi-Agent Workflow Engine
**Purpose**: Orchestrate the semantic reconciliation pipeline

**Agents**:
- **Extraction**: Parse variant strings (regex + NLP)
- **Normalization**: Map to canonical forms (HGNC, RefSeq)
- **Retrieval**: Semantic KB search (embeddings placeholder)
- **Reasoning**: Clinical context analysis (LLM placeholder)
- **Confidence**: Multi-component scoring
- **Review**: Queue management and expert routing

**Technologies**: LangGraph (structure), async/await, state management

### 3. Data Connectors
**Purpose**: Safe, rate-limited access to external databases

**Connectors**:
- **HGNC Client**: Gene nomenclature validation
- **ClinVar Client**: Clinical variant evidence
- **CIViC Client**: Cancer variant interpretation

**Features**: Error handling, caching, fallback logic

### 4. Knowledge Base (KB)
**Purpose**: Canonical variant repository with version control

**Storage**: 
- Development: DuckDB (file-based, no server needed)
- Production: PostgreSQL

**Contents**:
- Canonical variants (HGVS nomenclature, protein changes)
- Gene aliases and synonyms
- Clinical evidence links
- Approval history and audit trail

### 5. Governance Engine
**Purpose**: Enforce human review, versioning, and audit logging

**Features**:
- **Approval Workflow**: Routes to expert reviewers
- **Versioning**: Track KB changes with full history
- **Audit Trail**: Who approved what, when, why
- **Rollback**: Revert to previous KB versions

### 6. Frontend (Streamlit)
**Purpose**: Interactive UI for variant reconciliation and expert review

**Screens**:
- **Reconciliation Input**: Submit raw variants
- **Review Queue**: Pending expert decisions
- **Review Details**: AI reasoning + recommendation
- **Approval Log**: Historical decisions

---

## Data Flow Diagram

```
Raw Variant Input
(e.g., "EGFR Ex19del")
        ↓
┌───────────────────────────────────────────┐
│ EXTRACTION AGENT                          │
│ ──────────────────────────────────────    │
│ • Parse gene symbol: "EGFR"               │
│ • Parse variant: "Ex19del" (exon deletion)│
│ • Identify nomenclature style             │
└───────────────┬─────────────────────────────┘
                ↓
        Extracted:
        {gene: "EGFR", type: "deletion", loc: "exon_19"}
                ↓
┌───────────────────────────────────────────┐
│ NORMALIZATION AGENT                       │
│ ──────────────────────────────────────    │
│ • Lookup HGNC: "EGFR" → canonical        │
│ • Get transcript: NM_005228.4             │
│ • Compute HGVS: c.2235_2249del15         │
│ • Map to protein: p.E746_A750del         │
│ • Generate canonical ID: EGFR|exon19del  │
└───────────────┬─────────────────────────────┘
                ↓
        Normalized:
        {canonical_id: "EGFR|exon_19_deletion", hgvs_dna: "c.2235_2249del15", ...}
                ↓
┌───────────────────────────────────────────┐
│ RETRIEVAL AGENT                           │
│ ──────────────────────────────────────    │
│ • Query KB: exact match + semantic sim   │
│ • Return candidates + clinical evidence  │
│ • Rank by relevance                      │
└───────────────┬─────────────────────────────┘
                ↓
        Retrieved:
        [{kb_id: "var_egfr_001", approvals: 156, evidence: [...]}, ...]
                ↓
┌───────────────────────────────────────────┐
│ REASONING AGENT                           │
│ ──────────────────────────────────────    │
│ • Input to LLM with context              │
│ • Analyze clinical significance          │
│ • Summarize treatment implications       │
│ • Generate reasoning explanation         │
└───────────────┬─────────────────────────────┘
                ↓
        Reasoned:
        {clinical_context: "...", recommendation: "APPROVE", llm_score: 0.96}
                ↓
┌───────────────────────────────────────────┐
│ CONFIDENCE AGENT                          │
│ ──────────────────────────────────────    │
│ • Deterministic score: 1.0 (perfect match)│
│ • Semantic score: 0.99 (embeddings)      │
│ • LLM score: 0.96 (reasoning)            │
│ • Historical score: 0.98 (156 approvals) │
│ • Composite: (1+0.99+0.96+0.98)/4 = 0.98│
└───────────────┬─────────────────────────────┘
                ↓
        Scored:
        {composite_score: 0.98, category: "Very High Confidence"}
                ↓
┌───────────────────────────────────────────┐
│ REVIEW AGENT                              │
│ ──────────────────────────────────────    │
│ • If score > 0.95: Fast-track queue     │
│ • Assign to expert reviewer              │
│ • Generate summary brief                 │
│ • Set priority                           │
└───────────────┬─────────────────────────────┘
                ↓
        Queued:
        {review_id: "rev_001", queue: "fast_track", assigned_to: ["Dr. Chen"]}
                ↓
┌───────────────────────────────────────────┐
│ EXPERT REVIEW (HUMAN)                     │
│ ──────────────────────────────────────    │
│ • View system reasoning + AI scores      │
│ • Read clinical context                  │
│ • Make approval decision                 │
│ • Add curation notes                     │
└───────────────┬─────────────────────────────┘
                ↓
        Approved/Rejected:
        {decision: "APPROVED", reviewer: "Dr. Chen", notes: "..."}
                ↓
┌───────────────────────────────────────────┐
│ GOVERNANCE ENGINE                         │
│ ──────────────────────────────────────    │
│ • Update KB with new alias               │
│ • Version KB (0.1 → 0.1.1)              │
│ • Log full audit trail                   │
│ • Archive all decisions                  │
└───────────────┬─────────────────────────────┘
                ↓
        Final:
        KB Updated, Audit Log Entry Created, User Notified
```

---

## Confidence Scoring Model

The system uses a **multi-component confidence score** to route reconciliations to appropriate human reviewers:

### Score Components

1. **Deterministic Score** (weight: 30%)
   - Perfect canonical match: 1.0
   - Partial match with synonyms: 0.8
   - Nomenclature inconsistency: 0.5
   - No match: 0.0

2. **Semantic Similarity Score** (weight: 25%)
   - SapBERT embedding cosine similarity
   - Calculated against top 5 KB candidates
   - Average of best matches

3. **LLM Reasoning Score** (weight: 25%)
   - Confidence from clinical reasoning chain
   - Evidence base assessment
   - Treatment relevance scoring

4. **Historical Approval Score** (weight: 20%)
   - Prior approval rate (approvals / total)
   - Clipped to [0, 1] range
   - Heavily weighted by sample size

### Routing Logic

```
IF composite_score > 0.95 AND historical_approvals > 100 AND rejections == 0:
  → Fast-Track Queue (1 reviewer, 2-5 min)
  
ELSE IF composite_score > 0.80:
  → Standard Queue (1-2 reviewers, 5-15 min)
  
ELSE IF composite_score > 0.60:
  → Escalation Queue (2+ reviewers, 15+ min)
  
ELSE:
  → Hold for manual curation (expert team)
```

---

## Technology Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Language** | Python 3.10+ | Scientific ecosystem, ML libraries |
| **API Framework** | FastAPI | Type safety, async, auto-docs |
| **Agent Orchestration** | LangGraph structure | Modularity, state management |
| **Semantic Understanding** | SapBERT/BioBERT (placeholder) | Biomedical text understanding |
| **LLM Integration** | OpenAI/Claude/Gemini (placeholder) | Reasoning and summarization |
| **Data Storage** | DuckDB / PostgreSQL | SQL-based, versioning support |
| **Frontend** | Streamlit | Rapid prototyping, data viz |
| **Containerization** | Docker / Compose | Reproducibility, deployment |
| **Testing** | pytest | Python standard |

---

## Deployment Architecture

### Development
```
Local Machine
├── Python venv
├── DuckDB (local file)
├── FastAPI (localhost:8000)
└── Streamlit (localhost:8501)
```

### Docker (Single Machine)
```
Docker Host
├── api (FastAPI container)
├── frontend (Streamlit container)
├── db (PostgreSQL container)
└── pgadmin (optional)
```

### Production (Future)
```
Kubernetes Cluster
├── API Pods (horizontal scaling)
├── Frontend Service (Streamlit)
├── PostgreSQL StatefulSet
├── Redis Cache (optional)
├── Monitoring (Prometheus/Grafana)
└── Ingress (SSL/TLS termination)
```

---

## Security Considerations

1. **Input Validation**: All API inputs validated with Pydantic
2. **Rate Limiting**: API rate limits to prevent abuse
3. **Authentication**: JWT tokens for API access (placeholder)
4. **Authorization**: Role-based access control (RBAC)
5. **Audit Logging**: All decisions logged and immutable
6. **Data Privacy**: Environment-based secret management
7. **API Keys**: Secure storage for external service credentials

---

## Scalability Considerations

1. **Stateless API**: Horizontally scalable with load balancer
2. **Async Processing**: Non-blocking I/O for external API calls
3. **Caching**: Redis for KB queries and embeddings
4. **Database Optimization**: Indexed queries for semantic search
5. **Batch Processing**: Queue-based batch reconciliation (future)
6. **CDN**: Static frontend assets (future)

---

## Failure Modes & Mitigation

| Failure | Impact | Mitigation |
|---------|--------|-----------|
| External API down (HGNC, ClinVar) | Normalization fails | Fallback to cached/local data |
| LLM API unavailable | Reasoning score = 0 | Continue with other scores |
| KB database crash | No writes possible | Read-only fallback mode |
| Network timeout | Reconciliation stalls | Async retry with exponential backoff |
| Invalid user input | Processing error | Validate and return clear error |

---

## Future Enhancements

1. **Full LangGraph Integration**: Replace placeholder structure with production framework
2. **Multi-Transcript Support**: Handle alternative transcript contexts
3. **Structural Variants**: Support complex rearrangements (future)
4. **Phenotype Integration**: Link variants to clinical phenotypes
5. **ML Model Training**: Learn from historical approvals/rejections
6. **Institutional Integration**: FHIR, HL7 compatibility
7. **Benchmarking**: Compare against manual curation baselines

---

*Last Updated: May 17, 2026*
