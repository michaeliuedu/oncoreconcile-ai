# GitHub Repository Overview

This document provides a high-level guide to the OncoReconcile AI repository structure and key files.

## Quick Navigation

### 📖 Documentation
- **[README.md](../../README.md)**: Project overview, quickstart, and API reference
- **[Project Summary](project_summary.md)**: Executive summary and key metrics
- **[Demo Workflow](demo_workflow.md)**: End-to-end example (EGFR Exon 19 Deletion)
- **[Architecture Overview](../architecture/architecture_overview.md)**: System design and components
- **[System Workflow](../architecture/system_workflow.md)**: Detailed agent interactions

### 💾 Data
- **`data/reference/v0.1/`**: Reference knowledge base (genes, variants, evidence)
  - `gene_aliases.csv`: HGNC gene mappings
  - `canonical_variants.csv`: Curated variant catalog
  - `variant_synonyms.csv`: Nomenclature mappings
  - `variant_evidence.csv`: Clinical evidence links
- **`data/examples/`**: Example inputs/outputs for testing and demonstration

### 🤖 Source Code (`src/`)
- **`agents/`**: Multi-agent system components
  - `workflow.py`: Main orchestration logic
  - `extraction_agent.py`: Variant parsing
  - `normalization_agent.py`: Canonical mapping
  - `retrieval_agent.py`: KB semantic search
  - `reasoning_agent.py`: LLM integration
  - `confidence_agent.py`: Scoring logic
  - `review_agent.py`: Human review queue

- **`connectors/`**: External data source clients
  - `hgnc_client.py`: Gene database API
  - `clinvar_client.py`: ClinVar API
  - `civic_client.py`: CIViC API

- **`normalization/`**: Canonical representation logic
  - `gene_normalizer.py`: Gene name standardization
  - `variant_normalizer.py`: Variant notation standardization

- **`retrieval/`**: Knowledge base search
  - `semantic_search.py`: Semantic similarity matching

- **`reasoning/`**: LLM integration
  - `llm_reasoner.py`: LLM client and integration
  - `prompts.py`: LLM prompt templates

- **`governance/`**: Human review and audit trail
  - `curation_log.py`: Audit logging
  - `review_queue.py`: Review queue management
  - `kb_update.py`: Versioned KB updates

- **`api/`**: FastAPI backend
  - `main.py`: App initialization
  - `routes.py`: API endpoints
  - `schemas.py`: Request/response models

### 🎨 Frontend
- **`frontend/streamlit_app.py`**: Interactive web UI for variant reconciliation and review

### ✅ Tests
- **`tests/test_gene_normalizer.py`**: Gene normalization tests
- **`tests/test_variant_workflow.py`**: End-to-end workflow tests

### ⚙️ Configuration
- **`.env.example`**: Environment variable template
- **`requirements.txt`**: Python dependencies
- **`docker-compose.yml`**: Container orchestration
- **`Dockerfile`**: Container image definition

---

## Key Concepts

### Agent System
OncoReconcile AI uses a **pipeline of specialized agents** to reconcile variants:

1. **Extraction Agent**: Parses raw variant strings
2. **Normalization Agent**: Maps to canonical representations
3. **Retrieval Agent**: Finds semantically similar variants in KB
4. **Reasoning Agent**: Analyzes clinical context (LLM-augmented)
5. **Confidence Agent**: Scores match quality
6. **Review Agent**: Routes to human experts
7. **(Human Expert)**: Approves/rejects reconciliation
8. **Governance Engine**: Updates versioned KB with audit trail

### Knowledge Base Structure

The KB stores variants in a **normalized, queryable format**:

```
canonical_variant_id: EGFR|exon_19_deletion
├── Gene Info
│   ├── symbol: EGFR
│   ├── hgnc_id: 3236
│   └── entrez_id: 1956
├── Nomenclature
│   ├── hgvs_dna: c.2235_2249del15
│   ├── hgvs_protein: p.E746_A750del
│   ├── transcript: NM_005228.4
│   └── aliases: [EGFR Ex19del, EGFR exon19_del, ...]
├── Clinical Data
│   ├── significance: Sensitizing (TKI-responsive)
│   ├── nccn_tier: 1
│   └── treatment_relevance: [Gefitinib, Erlotinib, ...]
└── Audit Trail
    ├── total_approvals: 157
    ├── total_rejections: 0
    ├── last_approved: 2026-05-17 by Dr. Sarah Chen
    └── version_history: [v0.1, v0.1.1, ...]
```

### Human-in-the-Loop Governance

Every reconciliation is queued for expert human review:
- **Fast Track** (confidence > 0.95): 1-2 min review
- **Standard** (confidence 0.80-0.95): 5-10 min review
- **Escalation** (confidence < 0.80): Expert panel review

The system provides:
- **Clear summaries** of AI reasoning
- **Confidence scores** broken down by component
- **Historical precedent** (prior approvals/rejections)
- **Clinical context** from evidence bases

### Audit Trail & Versioning

Every KB update is tracked with:
- **Approval chain**: Who approved what, when
- **Reasoning log**: AI reasoning and confidence scores
- **Version history**: Before/after states
- **Rollback capability**: Revert to previous versions if needed

---

## Typical Usage Flows

### Flow 1: Lab Integration
```
NGS Pipeline Output
    ↓
POST /reconcile
    ↓
OncoReconcile Workflow
    ↓
Review Queue (Expert Assignment)
    ↓
Expert Approval (Web UI)
    ↓
GET /variants/{canonical_id}
    ↓
Lab System (Updated variant record)
```

### Flow 2: Research Query
```
Researcher Query: "Find all EGFR exon 19 deletions"
    ↓
GET /search?gene=EGFR&variant=exon_19_deletion
    ↓
Semantic Search + KB Lookup
    ↓
Reconciled Variants + Evidence
    ↓
Research Database Integration
```

### Flow 3: Expert Curation
```
Review Queue Dashboard
    ↓
Pending Reconciliations (sorted by priority)
    ↓
Expert Reviews & Approves
    ↓
POST /review/approve
    ↓
KB Version Updated
    ↓
Audit Log Entry Created
```

---

## Development Setup

### Quick Start
```bash
# Clone repo
git clone https://github.com/yourusername/oncoreconcile-ai.git
cd oncoreconcile-ai

# Virtual environment
python -m venv venv
source venv/bin/activate

# Dependencies
pip install -r requirements.txt

# Environment config
cp .env.example .env
# Edit .env with your API keys

# Run API
uvicorn src.api.main:app --reload

# In new terminal, run frontend
streamlit run frontend/streamlit_app.py

# Run tests
pytest tests/
```

### Docker Deployment
```bash
docker-compose up -d
```

Access:
- **API**: http://localhost:8000
- **Frontend**: http://localhost:8501
- **pgAdmin**: http://localhost:5050 (optional DB management)

---

## API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | Health check |
| POST | `/reconcile` | Submit variant for reconciliation |
| GET | `/reconcile/{id}` | Get reconciliation status |
| GET | `/variants/{canonical_id}` | Retrieve canonical variant |
| GET | `/review-queue` | List pending reviews |
| POST | `/review/{id}/approve` | Approve reconciliation |
| POST | `/review/{id}/reject` | Reject reconciliation |
| GET | `/search` | Search variants/genes |
| GET | `/audit-log` | View approval history |

See [routes.py](../../src/api/routes.py) for full endpoint documentation.

---

## Data Files Reference

### `gene_aliases.csv`
Maps gene symbols to canonical HGNC names:
```
gene_input,canonical_gene,hgnc_id,entrez_id
EGFR,EGFR,3236,1956
HER2,ERBB2,3236,2064
ErbB2,ERBB2,3236,2064
```

### `canonical_variants.csv`
Curated variant catalog:
```
canonical_id,gene,hgvs_dna,hgvs_protein,variant_type,clinical_significance
EGFR|exon_19_deletion,EGFR,c.2235_2249del15,p.E746_A750del,deletion,Sensitizing
EGFR|L858R,EGFR,c.2573T>G,p.L858R,substitution,Sensitizing
BRAF|V600E,BRAF,c.1799T>A,p.V600E,substitution,Activating
```

### `variant_synonyms.csv`
Nomenclature mappings for flexible searching:
```
canonical_id,synonym,synonym_type
EGFR|exon_19_deletion,EGFR Ex19del,shorthand
EGFR|exon_19_deletion,EGFR exon_19_del,shorthand
EGFR|exon_19_deletion,EGFR c.2235_2249del15,hgvs_dna
```

### `sample_inputs.json` & `sample_outputs.json`
Example reconciliation workflows for testing and demos.

---

## Key Files to Start With

1. **New to the project?** Start with [README.md](../../README.md)
2. **Want to understand the system?** Read [Architecture Overview](../architecture/architecture_overview.md)
3. **See it in action?** Check out [Demo Workflow](demo_workflow.md)
4. **Want to contribute code?** Look at [src/agents/workflow.py](../../src/agents/workflow.py)
5. **Running the API?** See [src/api/main.py](../../src/api/main.py)
6. **Using the frontend?** See [frontend/streamlit_app.py](../../frontend/streamlit_app.py)

---

## Support & Questions

- **Issues**: File GitHub issues for bugs and feature requests
- **Discussions**: Use GitHub Discussions for Q&A
- **Contributing**: See CONTRIBUTING.md for guidelines

---

*Last Updated: May 17, 2026*
