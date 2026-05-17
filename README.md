# OncoReconcile AI

**Human-Governed AI Agent System for Precision Oncology Semantic Interoperability**

## ⚠️ Disclaimer

**This is a research and educational prototype project for the DFWIT AI Competition.** This software is **NOT clinical software** and does **NOT make clinical claims, provide diagnosis, or recommend treatment**. It is intended solely for demonstrating human-governed AI workflows in semantic reconciliation of oncology variant representations and for research purposes.

---

## 1. Project Overview

OncoReconcile AI is a research-oriented interoperability platform that demonstrates **human-governed AI agent workflows** for reconciling heterogeneous oncology variant representations. The system addresses a critical challenge in precision oncology: variant annotations from different sources (ClinVar, CIViC, local labs) use different nomenclatures and clinical significance assessments, making it difficult for clinicians and researchers to reason across data sources.

### Vision
Enable seamless semantic interoperability of oncology variants through a multi-agent system that:
- **Extracts** raw variant inputs from diverse sources
- **Normalizes** genes and variants to canonical representations
- **Retrieves** semantically similar variants from curated knowledge bases
- **Reasons** about clinical associations using LLM-augmented analysis
- **Scores** confidence using deterministic + ML-based metrics
- **Enforces** human review and approval before knowledge base updates
- **Maintains** versioned, auditable knowledge base history

---

## 2. Problem Statement

### The Interoperability Challenge
Precision oncology relies on accurate, standardized variant annotations. However:

- **Nomenclature Heterogeneity**: The same variant is represented multiple ways:
  - EGFR Exon 19 Deletion: `EGFR Ex19del`, `EGFR exon_19_deletion`, `EGFR c.2235_2249del15`, `EGFR p.E746_A750del`
  
- **Data Silos**: Clinical variants exist in incompatible formats across ClinVar, CIViC, local laboratories, and EHR systems.

- **Trust & Governance**: AI-driven variant reconciliation lacks sufficient human oversight, auditability, and clinical governance.

- **Semantic Gaps**: Simple string matching fails; similar variants need semantic understanding of genomic nomenclature, transcript contexts, and clinical significance.

### Why It Matters
Clinicians and researchers need to:
- Query "find all EGFR exon 19 deletions" and retrieve ALL relevant variants across all nomenclature systems
- Make evidence-based treatment decisions backed by reconciled, trusted data
- Understand HOW variants were normalized and WHOSE decision it was

---

## 3. Proposed Solution

### Architecture: Multi-Agent Semantic Reconciliation
OncoReconcile AI implements a **LangGraph-inspired agent workflow** with human-in-the-loop validation:

```
Raw Variant Input
    ↓
[Extraction Agent] → Extract gene, position, change type
    ↓
[Normalization Agent] → Map to canonical gene names, normalize variant notation
    ↓
[Retrieval Agent] → Fetch semantically similar candidates from KB
    ↓
[Reasoning Agent] → LLM-augmented analysis of clinical associations
    ↓
[Confidence Agent] → Score match quality (deterministic + semantic + LLM)
    ↓
[Review Agent] → Queue for human curation
    ↓
[Human Decision] → Approve/Reject/Request Changes
    ↓
Versioned KB Update → Log audit trail
```

### Key Innovation: Human Governance
- **Every reconciliation** is queued for expert human review
- **Approval workflow** enforces explicit sign-off before KB updates
- **Audit logging** tracks who approved what, when, and with what reasoning
- **Deterministic + AI scoring** reduces cognitive load while preserving human judgment

---

## 4. Example Reconciliation

### Workflow: EGFR Exon 19 Deletion

#### Input (Raw)
```json
{
  "raw_variant": "EGFR Ex19del",
  "source": "local_lab_report",
  "confidence_level": "user_provided",
  "tissue": "lung"
}
```

#### Stage 1: Extraction
```
Gene: "EGFR"
Variant: "Ex19del"
Type: "deletion"
Location: "exon_19"
```

#### Stage 2: Normalization
```
Canonical Gene: "EGFR" (HGNC verified)
Normalized Variant: "EGFR|exon_19_deletion"
Transcript Context: "NM_005228.4"
HGVS Nomenclature: "c.2235_2249del15"
Protein Change: "p.E746_A750del"
```

#### Stage 3: Retrieval (from KB)
```
Candidate Matches:
1. EGFR|exon_19_deletion (canonical, 100% ID match)
2. EGFR p.E746_A750del (protein-level match, 95% semantic sim)
3. EGFR c.2235_2249del15 (DNA-level match, 98% semantic sim)
```

#### Stage 4: Reasoning (LLM Placeholder)
```
Clinical Context:
- EGFR exon 19 deletion is a hallmark sensitizing mutation
- Associated with ~10x higher response rate to EGFR TKI therapy
- Well-characterized in lung adenocarcinoma (NSCLC)
- Recommendation: Strong evidence for tyrosine kinase inhibitor eligibility
```

#### Stage 5: Confidence Scoring
```
Deterministic Score: 1.0 (perfect canonical match)
Semantic Similarity: 0.99 (SapBERT embedding)
LLM Confidence: 0.96 (reasoning chain)
Historical Approval: 0.98 (99 prior approvals, 0 rejections)
─────────────────
Composite Score: 0.98 (Very High Confidence)
```

#### Stage 6: Review & Approval
```
Review Queue Assignment:
- To: Dr. Sarah Chen, MD Genomics (expert)
- Priority: High (common variant)
- Reasoning Summary: "Ex19del perfectly matches EGFR exon 19 deletion (canonical). 
  Strong LLM confidence, 99 historical approvals. Recommend approval."

Dr. Chen's Decision: APPROVED
Curation Notes: "EGFR ex19del is a well-characterized sensitizing mutation. 
Recommendation aligns with NCCN guidelines."
```

#### Stage 7: KB Update (Versioned)
```
Knowledge Base v0.2:
Canonical Variant: EGFR|exon_19_deletion
Aliases: ["EGFR Ex19del", "EGFR exon19_deletion", "EGFR c.2235_2249del15", "EGFR p.E746_A750del"]
Clinical Significance: "Sensitizing (TKI-responsive)"
Last Updated: 2026-05-17
Approved By: Dr. Sarah Chen
Approval Reasoning: "Clinically validated; aligns with NCCN guidelines"
Version History: [v0.1 → v0.2]
```

---

## 5. Technical Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.10+ |
| **Web Framework** | FastAPI |
| **Agentic Orchestration** | LangGraph (placeholder structure) |
| **Semantic Understanding** | SapBERT / BioBERT / PubMedBERT (placeholder) |
| **LLM Reasoning** | OpenAI / Claude / Gemini (placeholder) |
| **Data Store** | DuckDB / PostgreSQL (placeholder) |
| **Frontend** | Streamlit |
| **Containerization** | Docker / Docker Compose |
| **Testing** | pytest |

---

## 6. Repository Structure

```
oncoreconcile-ai/
├── README.md                          # This file
├── LICENSE                            # MIT License
├── .gitignore                         # Git exclusions
├── requirements.txt                   # Python dependencies
├── .env.example                       # Example environment variables
├── docker-compose.yml                 # Container orchestration
│
├── docs/
│   ├── proposal/
│   │   ├── project_summary.md        # Executive summary
│   │   ├── demo_workflow.md          # Detailed workflow demo
│   │   └── github_repository_overview.md
│   ├── architecture/
│   │   ├── architecture_overview.md  # System design
│   │   └── system_workflow.md        # Agent workflow details
│   └── diagrams/
│       └── README.md
│
├── data/
│   ├── reference/
│   │   └── v0.1/
│   │       ├── reference_manifest.yml     # Manifest of reference data
│   │       ├── gene_aliases.csv           # HGNC gene mappings
│   │       ├── canonical_variants.csv     # Curated variant catalog
│   │       ├── variant_synonyms.csv       # Variant nomenclature mappings
│   │       └── variant_evidence.csv       # Clinical evidence links
│   └── examples/
│       ├── sample_inputs.json
│       └── sample_outputs.json
│
├── src/
│   ├── __init__.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── workflow.py               # Main orchestrator
│   │   ├── extraction_agent.py       # Extract variant components
│   │   ├── normalization_agent.py    # Gene/variant normalization
│   │   ├── retrieval_agent.py        # Semantic KB retrieval
│   │   ├── reasoning_agent.py        # LLM-augmented reasoning
│   │   ├── confidence_agent.py       # Confidence scoring
│   │   └── review_agent.py           # Human review queue
│   │
│   ├── connectors/
│   │   ├── __init__.py
│   │   ├── hgnc_client.py            # HGNC gene database API
│   │   ├── clinvar_client.py         # ClinVar API client
│   │   └── civic_client.py           # CIViC API client
│   │
│   ├── normalization/
│   │   ├── __init__.py
│   │   ├── gene_normalizer.py        # Gene name canonicalization
│   │   └── variant_normalizer.py     # Variant notation standardization
│   │
│   ├── retrieval/
│   │   ├── __init__.py
│   │   └── semantic_search.py        # KB semantic search (embeddings placeholder)
│   │
│   ├── reasoning/
│   │   ├── __init__.py
│   │   ├── llm_reasoner.py           # LLM integration placeholder
│   │   └── prompts.py                # LLM prompt templates
│   │
│   ├── governance/
│   │   ├── __init__.py
│   │   ├── curation_log.py           # Audit trail & approval log
│   │   ├── review_queue.py           # Human review queue management
│   │   └── kb_update.py              # Versioned KB update logic
│   │
│   └── api/
│       ├── __init__.py
│       ├── main.py                   # FastAPI app initialization
│       ├── routes.py                 # API endpoints
│       └── schemas.py                # Request/response schemas
│
├── frontend/
│   ├── README.md
│   └── streamlit_app.py              # Interactive UI
│
├── tests/
│   ├── test_gene_normalizer.py
│   └── test_variant_workflow.py
│
└── .env.example                       # Environment template
```

---

## 7. Current Team

**OncoReconcile AI** is being developed as part of the **DFWIT AI Competition** by a small multidisciplinary team of researchers and engineers.

### Roles
- **Project Lead / AI Research**: [Your Name]
- **Genomics Domain Expert**: [Collaborator Name]
- **Software Engineering**: [Developer Name]
- **Human-in-the-Loop Design**: [UX/Governance Specialist]

*Team members to be added as project grows.*

---

## 8. Roadmap

### Phase 1: MVP (Current - May 2026)
- [ ] Gene normalization (EGFR, BRAF, ERBB2/HER2, KRAS, ALK, MET)
- [ ] Variant normalization (exon deletions, point mutations, fusions)
- [ ] Deterministic confidence scoring
- [ ] FastAPI backend with /health, /reconcile, /review-queue, /review/approve routes
- [ ] Human review queue UI
- [ ] Curation log & audit trail
- [ ] Docker deployment

### Phase 2: Semantic Intelligence (June 2026)
- [ ] Integrate SapBERT for semantic similarity
- [ ] LangGraph agent orchestration (full framework)
- [ ] LLM reasoning integration (OpenAI/Claude placeholder → real integration)
- [ ] Semantic search over knowledge base
- [ ] Multi-transcript support (transcript-aware normalization)

### Phase 3: Production & Governance (Q3 2026)
- [ ] Database persistence (PostgreSQL)
- [ ] Versioned knowledge base with full audit trail
- [ ] Role-based access control (RBAC)
- [ ] Institutional integration examples
- [ ] FHIR variant representation support
- [ ] API documentation (OpenAPI/Swagger)

### Phase 4: Clinical Validation (Q4 2026+)
- [ ] External validation against curated oncology cohorts
- [ ] Performance benchmarks vs. manual curation
- [ ] Regulatory pathway exploration
- [ ] Institutional partnerships for real-world deployment

---

## Quick Start

### Prerequisites
- Python 3.10+
- Docker & Docker Compose (for containerized deployment)

### Local Development

```bash
# Clone repository
git clone https://github.com/yourusername/oncoreconcile-ai.git
cd oncoreconcile-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your API keys and settings

# Run API server
uvicorn src.api.main:app --reload

# In another terminal, run Streamlit frontend
streamlit run frontend/streamlit_app.py

# Run tests
pytest tests/
```

### Docker Deployment

```bash
docker-compose up -d
```

Access the application at `http://localhost:8000` (API) and `http://localhost:8501` (Frontend).

---

## API Quick Reference

### Health Check
```bash
curl http://localhost:8000/health
```

### Reconcile Variant
```bash
curl -X POST http://localhost:8000/reconcile \
  -H "Content-Type: application/json" \
  -d '{
    "raw_variant": "EGFR Ex19del",
    "source": "local_lab",
    "tissue": "lung"
  }'
```

### View Review Queue
```bash
curl http://localhost:8000/review-queue
```

### Approve Reconciliation
```bash
curl -X POST http://localhost:8000/review/approve \
  -H "Content-Type: application/json" \
  -d '{
    "reconciliation_id": "rec_12345",
    "reviewer_id": "dr_chen",
    "approval_notes": "Well-characterized variant. Aligns with guidelines."
  }'
```

---

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit changes with descriptive messages
4. Push to your fork
5. Submit a pull request

See CONTRIBUTING.md for detailed guidelines.

---

## License

This project is licensed under the **MIT License** – see [LICENSE](LICENSE) file for details.

---

## References & Resources

- **HGNC (HUGO Gene Nomenclature Committee)**: https://www.genenames.org/
- **ClinVar**: https://www.ncbi.nlm.nih.gov/clinvar/
- **CIViC**: https://civicdb.org/
- **NCCN Clinical Practice Guidelines**: https://www.nccn.org/
- **SapBERT**: https://github.com/cambridgeltl/SapBERT
- **LangGraph**: https://github.com/langchain-ai/langgraph
- **FastAPI**: https://fastapi.tiangolo.com/

---

## Citation

If you use OncoReconcile AI in your research, please cite:

```bibtex
@software{oncoreconcile_ai_2026,
  title={OncoReconcile AI: Human-Governed AI Agent System for Precision Oncology Semantic Interoperability},
  author={Your Name},
  year={2026},
  url={https://github.com/yourusername/oncoreconcile-ai}
}
```

---

## Contact

For questions, suggestions, or collaboration inquiries, please open an issue on GitHub or contact the project team.

**Project Status**: 🚀 Active Development

Last Updated: May 17, 2026
