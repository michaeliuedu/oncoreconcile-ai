#!/usr/bin/env bash
set -euo pipefail

REPO="${1:-michaeliuedu/oncoreconcile-ai}"

if ! command -v gh >/dev/null 2>&1; then
  echo "GitHub CLI not found. Install gh or create issues manually from docs/project_plan/github_issue_backlog.md."
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "GitHub CLI is not authenticated. Run: gh auth login -h github.com"
  exit 1
fi

create_issue() {
  local title="$1"
  local body="$2"
  gh issue create --repo "$REPO" --title "$title" --body "$body"
}

create_issue "P0: Define canonical reconciliation output schema" "$(cat <<'BODY'
## Workstream
Backend, Data, Governance

## Priority
P0 - Required for competition MVP demo

## Depends on
- Current reconciliation workflow

## Blocks
- Batch reconciliation endpoint
- Frontend results table
- Audit log

## Goal
Define a canonical reconciliation result object that preserves original strings, canonical mappings, confidence, status, evidence/provenance, and review state.

## Acceptance Criteria
- Schema includes original gene and variant
- Schema includes canonical gene and variant
- Schema includes confidence score and status
- Schema includes provenance/source fields
- Tests cover at least one reconciled and one unresolved result
BODY
)"

create_issue "P0: Create curated demo CSV dataset" "$(cat <<'BODY'
## Workstream
Data, Demo

## Priority
P0 - Required for competition MVP demo

## Depends on
- Starter data package

## Blocks
- Batch endpoint tests
- Demo walkthrough
- Validation metrics

## Goal
Create `data/demo/demo_variants.csv` with a small, high-quality set of curated oncology reconciliation examples.

## Acceptance Criteria
- Contains 20-30 curated rows
- Includes EGFR, KRAS, BRAF, TP53
- Includes gene alias cases such as HER1, ERBB1, p53, C-MET
- Includes unresolved cases such as EGF-RX and UnknownDel19
- Includes expected canonical outputs/statuses for testing
BODY
)"

create_issue "P0: Build batch CSV reconciliation endpoint" "$(cat <<'BODY'
## Workstream
Backend/API

## Priority
P0 - Required for competition MVP demo

## Depends on
- Canonical output schema
- Demo CSV shape

## Blocks
- Upload UI
- End-to-end demo

## Goal
Implement `POST /reconcile/batch` to reconcile multiple rows in one request.

## Acceptance Criteria
- Accepts CSV-style records or JSON rows with original gene and variant
- Returns one canonical reconciliation object per row
- Handles partial failures without crashing the whole batch
- API tests cover happy path and unresolved input
BODY
)"

create_issue "P0: Add explicit reconciliation status logic" "$(cat <<'BODY'
## Workstream
Backend, AI/Retrieval, Governance

## Priority
P0 - Required for competition MVP demo

## Depends on
- Confidence scoring
- Normalization output

## Blocks
- Review queue routing
- Frontend badges
- Cannot-reconcile demo

## Goal
Add a deterministic status classifier for reconciliation outputs.

## Acceptance Criteria
- Supports `reconciled`, `needs_review`, and `cannot_reconcile`
- Low-confidence unknown gene/variant maps to `cannot_reconcile`
- Ambiguous but plausible mappings map to `needs_review`
- Tests cover all statuses
BODY
)"

create_issue "P0: Improve cannot-reconcile and ambiguity handling" "$(cat <<'BODY'
## Workstream
Data, AI/Retrieval, Governance

## Priority
P0 - Required for trustworthy AI demo story

## Depends on
- Status classifier

## Blocks
- Trustworthy AI demo story

## Goal
Ensure unresolved or ambiguous inputs preserve uncertainty instead of forcing mappings.

## Acceptance Criteria
- Inputs like EGF-RX, UnknownDel19, and MET-like do not get forced mappings
- Output includes a human-readable uncertainty reason
- Tests prove unresolved examples remain unresolved or review-routed
BODY
)"

create_issue "P1: Wire review decisions to audit log" "$(cat <<'BODY'
## Workstream
Governance/Backend

## Priority
P1 - Important for polished demo

## Depends on
- Canonical output schema
- Status logic

## Blocks
- Human-governed demo

## Goal
Make approve/reject/request-changes actions create audit records.

## Acceptance Criteria
- Review endpoint changes review status
- Audit log records reviewer, decision, timestamp, notes, before/after status
- Audit endpoint returns recorded entries
- Tests cover approve and reject paths
BODY
)"

create_issue "P1: Build upload and results UI" "$(cat <<'BODY'
## Workstream
Frontend

## Priority
P1 - Important for polished demo

## Depends on
- Batch reconciliation endpoint

## Blocks
- End-to-end visual demo

## Goal
Build an upload/paste flow and reconciliation results table.

## Acceptance Criteria
- User can upload or paste demo rows
- UI displays original/canonical gene and variant
- UI displays confidence and status
- UI visually distinguishes reconciled, needs review, and cannot reconcile
BODY
)"

create_issue "P1: Build review queue UI" "$(cat <<'BODY'
## Workstream
Frontend/Governance

## Priority
P1 - Important for polished demo

## Depends on
- Status logic
- Review/audit endpoints

## Blocks
- Human governance demo

## Goal
Build review queue and review detail UI.

## Acceptance Criteria
- Needs-review rows appear in queue
- Reviewer can approve/reject/request changes
- UI shows original evidence, canonical mapping, confidence, and explanation
BODY
)"

create_issue "P1: Add API documentation and local runbook" "$(cat <<'BODY'
## Workstream
Docs/Backend

## Priority
P1 - Important for onboarding and judging

## Depends on
- Current endpoint list

## Blocks
- Team onboarding
- Judge/reviewer setup

## Goal
Document API endpoints and local setup.

## Acceptance Criteria
- Documents health, gene reconcile, variant reconcile, batch reconcile, review, audit endpoints
- Includes example requests/responses
- Includes local test command
- Includes Docker instructions if current Docker path is working
BODY
)"

create_issue "P1: Create demo case design document" "$(cat <<'BODY'
## Workstream
Docs/Demo/Data

## Priority
P1 - Important for pitch narrative

## Depends on
- Demo CSV
- Project proposal

## Blocks
- Final pitch narrative

## Goal
Document the demo cases and why each one matters.

## Acceptance Criteria
- Explains gene alias cases
- Explains variant reconciliation cases
- Explains cannot-reconcile cases
- Connects each case to demo value and judging story
BODY
)"

create_issue "P1: Prepare pitch deck outline" "$(cat <<'BODY'
## Workstream
PM/Business/Demo

## Priority
P1 - Important for final presentation

## Depends on
- Project proposal
- MVP scope

## Blocks
- Final presentation

## Goal
Create the first pitch deck outline.

## Acceptance Criteria
- Covers problem, users, solution, workflow, demo, governance, roadmap, team
- Avoids clinical claims
- Uses screenshots/placeholders where final UI is not ready
BODY
)"

create_issue "P1: Add demo smoke test checklist" "$(cat <<'BODY'
## Workstream
Testing/Demo

## Priority
P1 - Important for demo reliability

## Depends on
- Batch endpoint
- UI

## Blocks
- Final demo rehearsal

## Goal
Create a repeatable smoke test checklist for demo readiness.

## Acceptance Criteria
- Includes backend startup
- Includes frontend startup
- Includes one reconciled row
- Includes one needs-review row
- Includes one cannot-reconcile row
- Includes expected visible outputs
BODY
)"
