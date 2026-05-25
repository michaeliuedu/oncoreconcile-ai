# OncoReconcile AI

## Data Governance Guidance

To ensure transparency, reproducibility, and ethical use of data in this project, all contributors and future data updates must follow these principles:

1. **Provenance and Documentation:**
        - Clearly document the source, method of acquisition, and any synthesis or curation steps for all new data files.
        - Maintain or update the provenance and reproducibility documentation (see `oncoreconcile_starter/PROVENANCE_AND_REPRODUCIBILITY.md`).

2. **Synthetic and Real Data:**
        - Clearly distinguish between synthetic (AI- or human-generated) and real-world data.
        - Do not include any real patient data or protected health information (PHI) unless explicit approval and compliance steps are followed.

3. **Public Data Use:**
        - Only use public, redistributable data sources or those with appropriate licenses for open-source projects.
        - Attribute all external data sources in documentation and code as appropriate.

4. **Reproducibility:**
        - When possible, provide scripts or detailed steps for how new data was generated or processed.
        - Ensure that others can reproduce or extend the dataset using the provided documentation.

5. **Ethics and Compliance:**
        - Follow all applicable data use agreements, licenses, and ethical guidelines.
        - If in doubt, consult with project leads before adding new data.

For more details and examples, see `oncoreconcile_starter/PROVENANCE_AND_REPRODUCIBILITY.md`.

**AI-assisted oncology gene and variant reconciliation platform**

OncoReconcile AI is a DFWIT AI Competition project focused on turning messy oncology gene and variant strings into traceable, reviewable canonical knowledge objects. The project is intentionally human-governed: AI and deterministic logic help reconcile data, but ambiguous or low-confidence mappings must preserve uncertainty and flow into review instead of being forced into a false answer.

## Disclaimer

This is a research and educational prototype. It is not clinical software, does not make clinical claims, does not diagnose disease, and does not recommend treatment.

## Project Goal

Precision oncology data often arrives from different labs, reports, databases, and bioinformatics pipelines with inconsistent names for the same biological concept. Examples include `HER1`, `ERBB1`, and `EGFR`, or `EGFR Ex19del`, `E746_A750del`, and `p.E746_A750del`.

The goal of this repo is to build a small, credible MVP that demonstrates:

- Gene alias reconciliation against curated HGNC-style reference data.
- Variant representation reconciliation for common oncology examples.
- Confidence-aware status assignment: `reconciled`, `needs_review`, and `cannot_reconcile`.
- Human review and audit trail concepts.
- Traceable outputs that preserve original evidence, canonical mappings, confidence, provenance, and review status.

The first demo scope is intentionally narrow: lung adenocarcinoma-oriented examples with genes such as EGFR, KRAS, BRAF, TP53, MET, ALK, and ERBB2/HER2; SNVs and small indels; and curated demo data rather than large raw genomics downloads.

## Current MVP Status

As of May 2026, the repo contains:

- A FastAPI backend scaffold with reconciliation and review endpoints.
- A deterministic CSV-backed gene reconciliation endpoint at `POST /reconcile/gene`.
- A variant reconciliation workflow with extraction, normalization, retrieval, reasoning, confidence scoring, and review queue modules.
- Curated reference data under `data/reference/v0.1/`.
- Starter NSCLC demo data under `oncoreconcile_starter/`.
- A Streamlit demo UI under `frontend/`.
- Architecture, proposal, weekly execution plan, meeting agenda, and GitHub issue planning docs.
- Passing pytest coverage for the current starter workflow.

Some planned production-grade pieces are still placeholders, including semantic embedding retrieval, LLM reasoning integration, persistent database storage, and full frontend/backend review actions.

## System Workflow

```text
Input mutation table or VCF-like data
        |
        v
Gene name reconciliation
        |
        v
Variant extraction
        |
        v
Deterministic normalization
        |
        v
Candidate retrieval
        |
        v
AI-assisted reasoning and confidence scoring
        |
        v
Human review workflow
        |
        v
Governed canonical knowledge object + audit trail
```

## Quick Start

### Install

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run Tests

```bash
python -m pytest -q
```

### Run Backend

```bash
uvicorn src.api.main:app --reload
```

The API will be available at `http://localhost:8000`.

### Run Streamlit Demo

If the backend is running locally:


```bash
export API_URL=http://localhost:8000
streamlit run frontend/streamlit_app.py
```

*This ensures the frontend connects to your local backend. If you see 'Cannot connect to API', check this step.*

If running through Docker Compose, the frontend defaults to the Docker service URL `http://api:8000`.

### Docker

```bash
docker-compose up -d
```

## API Examples

### Health Check

```bash
curl http://localhost:8000/health
```

### Gene Reconciliation

```bash
curl -X POST http://localhost:8000/reconcile/gene \
  -H "Content-Type: application/json" \
  -d '{"gene_name": "HER1", "source": "demo"}'
```

Expected result: `HER1` maps to canonical gene `EGFR` with deterministic alias provenance from `data/reference/v0.1/gene_aliases.csv`.

### Variant Reconciliation

```bash
curl -X POST http://localhost:8000/reconcile \
  -H "Content-Type: application/json" \
  -d '{
    "raw_variant": "EGFR Ex19del",
    "source": "local_lab",
    "tissue": "lung_nsclc"
  }'
```

### Review Queue

```bash
curl http://localhost:8000/review-queue
```

## Repository Structure

```text
oncoreconcile-ai/
├── README.md
├── CONTRIBUTING.md
├── requirements.txt
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
├── data/
│   ├── examples/
│   └── reference/v0.1/
├── docs/
│   ├── architecture/
│   ├── diagrams/
│   ├── meetings/
│   ├── project_plan/
│   └── proposal/
├── frontend/
│   ├── README.md
│   └── streamlit_app.py
├── oncoreconcile_starter/
│   ├── README.md
│   ├── gene_aliases.csv
│   ├── oncology_variants_master.csv
│   ├── variant_synonyms.csv
│   ├── evidence_lookup.json
│   └── synthetic_reports/
├── scripts/
│   └── create_github_issues.sh
├── src/
│   ├── agents/
│   ├── api/
│   ├── connectors/
│   ├── governance/
│   ├── reasoning/
│   └── retrieval/
└── tests/
```

## Project Documentation

- Competition proposal: `docs/proposal/competition_submission_proposal.md`
- Weekly execution plan: `docs/project_plan/weekly_execution_plan.md`
- Team task board: `docs/project_plan/team_task_board.md`
- GitHub issue backlog: `docs/project_plan/github_issue_backlog.md`
- Task-mapped architecture: `docs/architecture/task_mapped_architecture.md`
- Architecture diagrams: `docs/diagrams/architecture_task_map.md`
- First team meeting agenda: `docs/meetings/first_team_meeting_agenda.md`
- Starter data integration notes: `docs/architecture/starter_data_integration.md`

Google Docs copies have also been created for the proposal, weekly plan, and architecture/task map so the team can review and comment outside GitHub.

## Team Workflow

The initial backlog is tracked as GitHub issues #1 through #12 in `michaeliuedu/oncoreconcile-ai`.

Recommended contributor flow:

1. Pick an issue based on interest and dependency readiness.
2. Create a focused branch, for example `issue-3-batch-csv-reconcile`.
3. Keep changes small and tied to the issue.
4. Run `python -m pytest -q` before pushing.
5. Open a pull request and link the issue.

The issue creation helper is intentionally safe by default:

```bash
sh scripts/create_github_issues.sh
```

This lists the planned issues and does not create duplicates. Creation modes require explicit confirmation.

## MVP Priorities

P0 work:

- Canonical reconciliation output schema.
- Curated demo CSV dataset.
- Batch CSV reconciliation endpoint.
- Explicit reconciliation status logic.
- Cannot-reconcile and ambiguity handling.

P1 work:

- Review decisions wired to an audit log.
- Upload and results UI.
- Review queue UI.
- API documentation and local runbook.
- Demo case design document.
- Pitch deck outline.
- Demo smoke test checklist.

## Technical Stack

| Area | Current Direction |
| --- | --- |
| Backend | Python, FastAPI |
| Frontend | Streamlit for MVP demo |
| Data | CSV/JSON reference and demo files |
| Testing | pytest |
| Future semantic retrieval | biomedical embeddings such as SapBERT/BioBERT/PubMedBERT |
| Future persistence | PostgreSQL or DuckDB |
| Future UI | React dashboard if competition scope allows |

## References

- HGNC: https://www.genenames.org/
- ClinVar: https://www.ncbi.nlm.nih.gov/clinvar/
- CIViC: https://civicdb.org/
- GA4GH VRS: https://vrs.ga4gh.org/
- FHIR Genomics: https://hl7.org/fhir/genomics.html
- FastAPI: https://fastapi.tiangolo.com/
- Streamlit: https://streamlit.io/

## License

This project is licensed under the MIT License. See `LICENSE` for details.

## Status

Active development for the DFWIT AI Competition.

Last updated: May 22, 2026
