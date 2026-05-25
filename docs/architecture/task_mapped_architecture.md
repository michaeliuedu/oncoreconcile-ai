# OncoReconcile AI Architecture and Task Map

This document explains the project architecture and maps each active GitHub task to the part of the system it improves. Use it to help team members understand where their work fits in the overall MVP.

## Architecture Overview

```text
User / Demo Operator
        |
        v
Frontend Demo UI
Upload CSV | Results Table | Review Queue | Audit View
        |
        v
FastAPI Backend
API Routes | Request/Response Schemas | Batch Processing
        |
        v
Reconciliation Workflow
Gene Reconciliation -> Variant Extraction -> Variant Normalization
        |
        v
Candidate Retrieval and Reasoning
Reference Lookup | Semantic Retrieval | AI-Assisted Explanation
        |
        v
Confidence and Status Layer
Confidence Score | Reconciled | Needs Review | Cannot Reconcile
        |
        v
Human Governance Layer
Review Queue | Approve/Reject/Request Changes | Audit Log
        |
        v
Reference and Demo Data
Gene Aliases | Variant Synonyms | Canonical Variants | Evidence Hints | Demo CSV
```

## System Layers

| Layer | Purpose | Current Repo Status | Key Files |
| --- | --- | --- | --- |
| Frontend Demo UI | Let users submit examples, view reconciliations, and review uncertain cases. | Prototype exists in Streamlit; upload/results/review workflow needs improvement. | `frontend/streamlit_app.py` |
| FastAPI Backend | Expose reconciliation, review, audit, and health endpoints. | Basic API exists; batch endpoint still needed. | `src/api/routes.py`, `src/api/schemas.py`, `src/api/main.py` |
| Reconciliation Workflow | Orchestrate extraction, normalization, retrieval, reasoning, scoring, and review routing. | Single-row workflow exists. Batch workflow and canonical output schema are next. | `src/agents/workflow.py` |
| Gene Reconciliation | Normalize gene aliases such as HER1, p53, C-MET. | CSV-backed gene reconciliation exists. | `src/agents/normalization_agent.py`, `data/reference/v0.1/gene_aliases.csv` |
| Variant Normalization | Normalize variant synonyms such as Ex19del, V600E, R175H. | CSV-backed variant synonym lookup exists for curated examples. | `src/agents/normalization_agent.py`, `data/reference/v0.1/variant_synonyms.csv` |
| Candidate Retrieval | Retrieve exact/near candidate matches from the reference KB. | Prototype retrieval exists; semantic retrieval is placeholder-level. | `src/agents/retrieval_agent.py`, `src/retrieval/semantic_search.py` |
| Reasoning and Explanation | Generate human-readable interpretation and recommendation text. | Template-based placeholder exists. | `src/agents/reasoning_agent.py`, `src/reasoning/` |
| Confidence and Status | Score reconciliation quality and classify output status. | Confidence scoring exists; explicit statuses still needed. | `src/agents/confidence_agent.py` |
| Human Governance | Queue uncertain cases for review and preserve decisions. | Review queue prototype exists; audit wiring still needed. | `src/agents/review_agent.py`, `src/governance/` |
| Data and Benchmarks | Provide reference data, starter examples, and demo cases. | Reference and starter data exist; curated demo CSV still needed. | `data/reference/v0.1/`, `oncoreconcile_starter/` |
| Testing and Demo QA | Verify correctness and demo readiness. | Tests exist and pass; demo smoke checklist needed. | `tests/`, `docs/project_plan/` |

## Current MVP Flow

Current implemented flow:

```text
Single raw variant input
        |
        v
Extraction Agent
        |
        v
Gene Normalizer
        |
        v
Variant Normalizer
        |
        v
Retrieval Agent
        |
        v
Reasoning Agent
        |
        v
Confidence Agent
        |
        v
Review Agent
```

Target competition demo flow:

```text
Batch CSV input
        |
        v
Canonical reconciliation object per row
        |
        +--> Reconciled
        |
        +--> Needs Review
        |        |
        |        v
        |   Human Review + Audit Log
        |
        +--> Cannot Reconcile
```

## GitHub Issue to Architecture Map

| Issue | Priority | Task | Architecture Layer | Depends On | Blocks |
| --- | --- | --- | --- | --- | --- |
| #1 | P0 | Define canonical reconciliation output schema | Backend schemas, workflow contract, provenance model | Existing single-row workflow | #3, #4, #6, #7 |
| #2 | P0 | Create curated demo CSV dataset | Data and benchmarks | Starter data package | #3, #10, #12 |
| #3 | P0 | Build batch CSV reconciliation endpoint | FastAPI backend, reconciliation workflow | #1, #2 | #7, #12, full demo |
| #4 | P0 | Add explicit reconciliation status logic | Confidence and status layer | #1, existing confidence scoring | #5, #6, #7, #8 |
| #5 | P0 | Improve cannot-reconcile and ambiguity handling | Status, uncertainty, governance | #4 | Trustworthy AI demo story |
| #6 | P1 | Wire review decisions to audit log | Human governance layer | #1, #4 | #8, governance demo |
| #7 | P1 | Build upload and results UI | Frontend Demo UI | #3, #4 | End-to-end visual demo |
| #8 | P1 | Build review queue UI | Frontend Demo UI, governance | #4, #6 | Human review demo |
| #9 | P1 | Add API documentation and local runbook | Docs, backend onboarding | Current endpoint list, #3 when ready | Team onboarding, judge setup |
| #10 | P1 | Create demo case design document | Docs, data, demo narrative | #2, proposal | Pitch narrative |
| #11 | P1 | Prepare pitch deck outline | PM/business/demo | Proposal, MVP scope | Final presentation |
| #12 | P1 | Add demo smoke test checklist | Testing and demo QA | #3, #7 | Final rehearsal |

## Dependency Graph

```text
#1 Canonical Output Schema
  -> #3 Batch Reconciliation Endpoint
  -> #7 Upload and Results UI
  -> #12 Demo Smoke Test Checklist

#2 Demo CSV Dataset
  -> #3 Batch Reconciliation Endpoint
  -> #10 Demo Case Design Document
  -> #12 Demo Smoke Test Checklist

#4 Status Logic
  -> #5 Cannot-Reconcile Handling
  -> #6 Review Decisions and Audit Log
  -> #7 Upload and Results UI
  -> #8 Review Queue UI

#6 Review Decisions and Audit Log
  -> #8 Review Queue UI
  -> Human Governance Demo

#11 Pitch Deck Outline
  -> Week 7 Presentation Package
```

## Task Status Snapshot

Use GitHub issues as the source of truth for live assignment and progress. This table shows the initial architecture status.

| Issue | Status at Project Start | Recommended First Owner Type |
| --- | --- | --- |
| #1 Canonical output schema | Ready to start | Backend/data modeling |
| #2 Demo CSV dataset | Ready to start | Data/domain examples |
| #3 Batch endpoint | Blocked by #1 and #2 | Backend/API |
| #4 Status logic | Ready to start after schema direction is clear | Backend/AI/scoring |
| #5 Cannot-reconcile handling | Blocked by #4 | AI/governance/data |
| #6 Review to audit log | Blocked by #1 and #4 | Governance/backend |
| #7 Upload/results UI | Blocked by #3 and #4 | Frontend |
| #8 Review queue UI | Blocked by #4 and #6 | Frontend/governance |
| #9 API docs/runbook | Can start now, finalize after #3 | Docs/backend |
| #10 Demo case design doc | Can start with #2 | Docs/data/demo |
| #11 Pitch deck outline | Can start now | PM/business |
| #12 Smoke test checklist | Can start draft now, finalize after #3 and #7 | Testing/demo |

## Recommended Workstreams

### Backend/API

Primary issues:

- #1 canonical output schema
- #3 batch reconciliation endpoint
- #6 review/audit endpoint wiring
- #9 API documentation support

### Data/Normalization

Primary issues:

- #2 demo CSV dataset
- #5 unresolved and ambiguous examples
- #10 demo case design support

### AI/Retrieval/Confidence

Primary issues:

- #4 status logic
- #5 cannot-reconcile handling
- #11 pitch explanation support

### Frontend/UI

Primary issues:

- #7 upload/results UI
- #8 review queue UI
- #12 demo smoke checklist support

### Governance/Testing

Primary issues:

- #6 audit log wiring
- #12 smoke test checklist
- tests for #1, #3, #4, #5, and #6

### PM/Business/Demo

Primary issues:

- #10 demo case design document
- #11 pitch deck outline
- #12 rehearsal checklist support

## What Is Already Implemented

The repository already includes:

- FastAPI scaffold
- single-row reconciliation workflow
- CSV-backed gene reconciliation
- CSV-backed variant synonym lookup
- confidence scoring module
- review queue prototype
- governance/audit module skeleton
- starter NSCLC benchmark data
- project proposal
- weekly execution plan
- team task board
- first team meeting agenda
- 18 passing tests

## What Is Not Yet Implemented

The key missing MVP pieces are:

- canonical reconciliation output object
- batch CSV reconciliation endpoint
- explicit status classifier
- cannot-reconcile output behavior
- audit log integration with review decisions
- upload/results UI path
- review queue UI path
- demo smoke test checklist

## Demo Story Mapped to Architecture

| Demo Moment | Architecture Layer | Supporting Issues |
| --- | --- | --- |
| Upload messy mutation rows | Frontend UI, FastAPI batch endpoint | #3, #7 |
| Normalize HER1 to EGFR | Gene reconciliation | Already implemented, #2 for demo data |
| Normalize Ex19del to EGFR exon 19 deletion | Variant normalization | Already implemented for curated synonyms, #2 for demo data |
| Show confidence and explanation | Confidence/reasoning | #1, #4 |
| Show `cannot_reconcile` for EGF-RX | Status/uncertainty | #4, #5 |
| Send uncertain row to review | Governance | #4, #6, #8 |
| Approve/reject and show audit trail | Governance/audit | #6, #8 |
| Explain project value to judges | Docs/pitch | #10, #11, #12 |

## How Team Members Should Use This Map

1. Pick an issue from GitHub.
2. Find the issue in the architecture map.
3. Check what it depends on and what it blocks.
4. Comment on the issue before starting work.
5. Keep changes small and focused on that architecture layer.
6. Add tests or demo proof where possible.
7. Update docs if behavior changes.

## Project North Star

The MVP should clearly demonstrate:

```text
Messy oncology gene/variant input
        ->
traceable canonical reconciliation
        ->
confidence-aware status
        ->
human review for uncertainty
        ->
auditable output
```

If a task does not strengthen that path, it should be considered secondary until the core demo is stable.
