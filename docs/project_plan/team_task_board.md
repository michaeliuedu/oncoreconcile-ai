# Team Task Board

This board is designed for the DFWIT AI Competition team to pick up mixed tasks based on interests while keeping priorities, dependencies, and demo goals clear.

## Working Model

Each coding team member should pick:

- 1 primary coding task
- 1 support/review task
- 1 documentation/demo task

The project lead owns scope control, architecture decisions, code review, final integration, and demo readiness. The PM/business lead owns pitch narrative, user framing, deck coordination, and demo storytelling.

## Priority Levels

| Priority | Meaning |
| --- | --- |
| P0 | Required for competition MVP demo |
| P1 | Important for a polished demo |
| P2 | Nice to have if core workflow is stable |

## Status Values

Use these issue/task statuses:

- Available
- Claimed
- In Progress
- In Review
- Done
- Blocked

## Task Dependencies

```text
Canonical output schema
  -> Batch CSV reconciliation endpoint
  -> Upload/results UI
  -> Demo script and screenshots

Demo CSV and reference examples
  -> Batch endpoint tests
  -> Confidence/status validation
  -> Final demo walkthrough

Status classification
  -> Review queue workflow
  -> Audit trail
  -> Frontend status badges

Review/audit workflow
  -> Human governance demo
  -> Pitch deck governance slide

API docs and runbook
  -> Team onboarding
  -> Judge/reviewer setup
```

## Pickup Tasks

### 1. Define Canonical Reconciliation Output Schema

- Priority: P0
- Workstream: backend, data, governance
- Depends on: current reconciliation workflow
- Blocks: batch endpoint, frontend results table, audit log
- Suggested owner interest: backend/data modeling
- Deliverable: schema/model for one reconciliation result preserving original strings, canonical mappings, confidence, status, evidence/provenance, and review state
- Acceptance criteria:
  - Schema includes original gene and variant
  - Schema includes canonical gene and variant
  - Schema includes confidence score and status
  - Schema includes provenance/source fields
  - Tests cover at least one reconciled and one unresolved result

### 2. Create Demo CSV Dataset

- Priority: P0
- Workstream: data, demo
- Depends on: starter data package
- Blocks: batch endpoint tests, demo walkthrough, validation metrics
- Suggested owner interest: data curation/domain examples
- Deliverable: `data/demo/demo_variants.csv`
- Acceptance criteria:
  - Contains 20-30 curated rows
  - Includes EGFR, KRAS, BRAF, TP53
  - Includes gene alias cases such as HER1, ERBB1, p53, C-MET
  - Includes unresolved cases such as EGF-RX and UnknownDel19
  - Includes expected canonical outputs/statuses for testing

### 3. Build Batch CSV Reconciliation Endpoint

- Priority: P0
- Workstream: backend/API
- Depends on: canonical output schema, demo CSV shape
- Blocks: upload UI, end-to-end demo
- Suggested owner interest: FastAPI/backend
- Deliverable: `POST /reconcile/batch`
- Acceptance criteria:
  - Accepts CSV-style records or JSON rows with original gene and variant
  - Returns one canonical reconciliation object per row
  - Handles partial failures without crashing the whole batch
  - API tests cover happy path and unresolved input

### 4. Add Explicit Reconciliation Status Logic

- Priority: P0
- Workstream: backend, AI/retrieval, governance
- Depends on: confidence scoring and normalization output
- Blocks: review queue routing, frontend badges, cannot-reconcile demo
- Suggested owner interest: rules/scoring
- Deliverable: deterministic status classifier
- Acceptance criteria:
  - Supports `reconciled`, `needs_review`, and `cannot_reconcile`
  - Low-confidence unknown gene/variant maps to `cannot_reconcile`
  - Ambiguous but plausible mappings map to `needs_review`
  - Tests cover all statuses

### 5. Improve Cannot-Reconcile and Ambiguity Handling

- Priority: P0
- Workstream: data, AI/retrieval, governance
- Depends on: status classifier
- Blocks: trustworthy AI demo story
- Suggested owner interest: uncertainty handling
- Deliverable: unresolved/ambiguous examples with explanation reasons
- Acceptance criteria:
  - Inputs like EGF-RX, UnknownDel19, and MET-like do not get forced mappings
  - Output includes a human-readable uncertainty reason
  - Tests prove unresolved examples remain unresolved or review-routed

### 6. Wire Review Decisions to Audit Log

- Priority: P1
- Workstream: governance/backend
- Depends on: canonical output schema and status logic
- Blocks: human-governed demo
- Suggested owner interest: governance/audit
- Deliverable: approve/reject/request-changes actions that create audit records
- Acceptance criteria:
  - Review endpoint changes review status
  - Audit log records reviewer, decision, timestamp, notes, before/after status
  - Audit endpoint returns recorded entries
  - Tests cover approve and reject paths

### 7. Build Upload and Results UI

- Priority: P1
- Workstream: frontend
- Depends on: batch reconciliation endpoint
- Blocks: end-to-end visual demo
- Suggested owner interest: UI/product
- Deliverable: upload form and reconciliation results table
- Acceptance criteria:
  - User can upload or paste demo rows
  - UI displays original/canonical gene and variant
  - UI displays confidence and status
  - UI visually distinguishes reconciled, needs review, and cannot reconcile

### 8. Build Review Queue UI

- Priority: P1
- Workstream: frontend/governance
- Depends on: status logic, review/audit endpoints
- Blocks: human governance demo
- Suggested owner interest: UI/governance
- Deliverable: review queue and review detail panel
- Acceptance criteria:
  - Needs-review rows appear in queue
  - Reviewer can approve/reject/request changes
  - UI shows original evidence, canonical mapping, confidence, and explanation

### 9. Add API Documentation and Local Runbook

- Priority: P1
- Workstream: docs/backend
- Depends on: current endpoint list
- Blocks: team onboarding and judge setup
- Suggested owner interest: docs/developer experience
- Deliverable: API docs and local run instructions
- Acceptance criteria:
  - Documents health, gene reconcile, variant reconcile, batch reconcile, review, audit endpoints
  - Includes example requests/responses
  - Includes local test command
  - Includes Docker instructions if current Docker path is working

### 10. Create Demo Case Design Document

- Priority: P1
- Workstream: docs/demo/data
- Depends on: demo CSV and project proposal
- Blocks: final pitch narrative
- Suggested owner interest: storytelling/data
- Deliverable: demo case documentation
- Acceptance criteria:
  - Explains gene alias cases
  - Explains variant reconciliation cases
  - Explains cannot-reconcile cases
  - Connects each case to demo value and judging story

### 11. Prepare Pitch Deck Outline

- Priority: P1
- Workstream: PM/business/demo
- Depends on: project proposal and MVP scope
- Blocks: final presentation
- Suggested owner interest: business/product
- Deliverable: slide outline
- Acceptance criteria:
  - Covers problem, users, solution, workflow, demo, governance, roadmap, team
  - Avoids clinical claims
  - Uses screenshots/placeholders where final UI is not ready

### 12. Add Demo Smoke Test Checklist

- Priority: P1
- Workstream: testing/demo
- Depends on: batch endpoint and UI
- Blocks: final demo rehearsal
- Suggested owner interest: QA/reliability
- Deliverable: repeatable smoke test checklist
- Acceptance criteria:
  - Includes backend startup
  - Includes frontend startup
  - Includes one reconciled row
  - Includes one needs-review row
  - Includes one cannot-reconcile row
  - Includes expected visible outputs

## Suggested Weekly Selection

For the next working cycle, prioritize:

1. Define canonical reconciliation output schema
2. Create demo CSV dataset
3. Build batch CSV reconciliation endpoint
4. Add explicit reconciliation status logic
5. Add API documentation and local runbook
6. Prepare pitch deck outline

The frontend review queue and audit workflow can start once statuses and batch output stabilize.

## Task Claim Template

```text
Name:

This week I will own:
- Primary:
- Support/review:
- Docs/demo:

Dependencies:
Expected deliverable:
Expected PR:
```

## GitHub Issue Helper

The 12 initial pickup issues are tracked in GitHub and mirrored in `docs/project_plan/github_issue_backlog.md`.

Use the helper script in read-only mode to list current issues:

```bash
scripts/create_github_issues.sh
```

The script has an explicit `--create-remaining` mode for recreating missing P1 issues in a fresh repository, but it can create duplicates. Only use it intentionally, and only after confirming the issues do not already exist.
