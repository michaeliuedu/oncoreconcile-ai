# GitHub Issue Backlog

The GitHub connector and local `gh` CLI were not authorized to create issues from this environment. Use this backlog to create issues manually or after re-authenticating the GitHub CLI.

To re-authenticate locally:

```bash
gh auth login -h github.com
```

After that, issues can be created from these titles and bodies.

## Issue Creation Helper

The repository includes `scripts/create_github_issues.sh` as a safe helper script.

Default behavior is read-only:

```bash
scripts/create_github_issues.sh
```

This lists current GitHub issues for `michaeliuedu/oncoreconcile-ai`.

To create the remaining P1 issues in a fresh repository or if issues #6-#12 are missing:

```bash
scripts/create_github_issues.sh --create-remaining
```

The script will warn that duplicate issues may be created and requires typing:

```text
CREATE
```

Do not use `--create-remaining` if the P1 issues already exist. As of the initial team setup, issues #1-#12 were created in GitHub.


---

## Issue 1

Title: `P0: Define canonical reconciliation output schema`

Body:

```markdown

> **Governance Reminder:**
> If this issue involves data modeling, provenance, or auditability, follow the data governance guidance in the main README and provenance documentation.

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

## Suggested Interest Fit
Backend/data modeling
```

## Issue 2

Title: `P0: Create curated demo CSV dataset`

Body:

```markdown
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

## Suggested Interest Fit
Data curation/domain examples
```

## Issue 3

Title: `P0: Build batch CSV reconciliation endpoint`

Body:

```markdown
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

## Suggested Interest Fit
FastAPI/backend
```

## Issue 4

Title: `P0: Add explicit reconciliation status logic`

Body:

```markdown

> **Governance Reminder:**
> This issue involves status logic and governance. Ensure all status and review logic is auditable and follows the data governance guidance in the main README and provenance documentation.

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

## Suggested Interest Fit
Rules/scoring
```

## Issue 5

Title: `P0: Improve cannot-reconcile and ambiguity handling`

Body:

```markdown

> **Governance Reminder:**
> This issue involves uncertainty handling and governance. Document all logic for ambiguity and ensure provenance is preserved. Follow the data governance guidance in the main README and provenance documentation.

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

## Suggested Interest Fit
Uncertainty handling
```

## Issue 6

Title: `P1: Wire review decisions to audit log`

Body:

```markdown

> **Governance Reminder:**
> This issue is core to governance and audit. Ensure all review and audit log logic is transparent, reproducible, and follows the data governance guidance in the main README and provenance documentation.

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

## Suggested Interest Fit
Governance/audit
```

## Issue 7

Title: `P1: Build upload and results UI`

Body:

```markdown
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

## Suggested Interest Fit
UI/product
```

## Issue 8

Title: `P1: Build review queue UI`

Body:

```markdown

> **Governance Reminder:**
> This issue involves governance UI. Ensure review queue and detail UI display provenance, auditability, and follow the data governance guidance in the main README and provenance documentation.

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

## Suggested Interest Fit
UI/governance
```

## Issue 9

Title: `P1: Add API documentation and local runbook`

Body:

```markdown
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

## Suggested Interest Fit
Docs/developer experience
```

## Issue 10

Title: `P1: Create demo case design document`

Body:

```markdown
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

## Suggested Interest Fit
Storytelling/data
```

## Issue 11

Title: `P1: Prepare pitch deck outline`

Body:

```markdown
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

## Suggested Interest Fit
Business/product narrative
```

## Issue 12

Title: `P1: Add demo smoke test checklist`

Body:

```markdown
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

## Suggested Interest Fit
QA/reliability
```
