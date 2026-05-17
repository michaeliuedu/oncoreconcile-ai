# Project Summary

**OncoReconcile AI**: A research-oriented AI interoperability platform demonstrating human-governed agent workflows for semantic reconciliation of oncology variants.

## Executive Summary

### Problem
Precision oncology suffers from semantic interoperability challenges: the same genetic variant is represented differently across ClinVar, CIViC, local laboratories, and EHR systems, making it difficult to query and reason across data sources.

### Solution
OncoReconcile AI implements a **multi-agent system with human-in-the-loop review** that:
1. **Extracts** raw variant inputs
2. **Normalizes** genes and variants to canonical representations
3. **Retrieves** semantically similar variants from a curated knowledge base
4. **Reasons** about clinical associations using LLM-augmented analysis
5. **Scores** confidence using deterministic + semantic similarity + LLM scores
6. **Queues** for human expert review and approval
7. **Updates** a versioned, auditable knowledge base

### Innovation
- **Human Governance**: Every reconciliation requires explicit expert approval before KB updates
- **Auditability**: Complete audit trail of who approved what, when, and why
- **Deterministic + AI Hybrid**: Combines rule-based normalization with semantic AI scoring
- **Versioning**: Knowledge base changes are tracked with full history

### Target Users
- **Genomics Labs**: Integrate variant standardization into clinical workflows
- **Bioinformaticians**: Query reconciled variants across multiple sources
- **Clinicians**: Access trustworthy, standardized variant interpretations
- **Researchers**: Validate AI-assisted reconciliation approaches

## Key Metrics (MVP)

| Metric | Target |
|--------|--------|
| **Genes Supported** | 6 (EGFR, BRAF, ERBB2/HER2, KRAS, ALK, MET) |
| **Variant Types** | Exon deletions, point mutations, fusions |
| **Processing Speed** | < 500ms per reconciliation |
| **Human Review Time** | 1-5 min per variant |
| **Audit Trail Completeness** | 100% of decisions logged |

## Roadmap

### Phase 1: MVP (May 2026)
- Deterministic gene/variant normalization
- Manual reference data curation
- FastAPI backend with core endpoints
- Human review queue UI
- Audit logging

### Phase 2: Semantic Intelligence (June 2026)
- SapBERT semantic similarity integration
- LangGraph agent orchestration
- LLM reasoning pipeline
- Semantic search over KB

### Phase 3: Production (Q3 2026)
- PostgreSQL persistence
- Role-based access control
- API documentation (OpenAPI)
- Institutional integration examples

### Phase 4: Clinical Validation (Q4 2026+)
- External validation on curated cohorts
- Regulatory pathway exploration
- Real-world deployment partnerships

## Team

- **AI Research Lead**: [Name]
- **Genomics Expert**: [Name]
- **Software Engineer**: [Name]
- **Human-in-the-Loop Design**: [Name]

## Disclaimer

⚠️ **This is a research and educational prototype. It does NOT make clinical claims, provide diagnosis, or recommend treatment. It is intended solely for demonstrating human-governed AI workflows and for research purposes.**

---

*For detailed workflow examples, see demo_workflow.md*
