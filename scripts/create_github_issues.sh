#!/usr/bin/env bash
set -euo pipefail

REPO="michaeliuedu/oncoreconcile-ai"
MODE="list"

usage() {
  cat <<'USAGE'
Usage:
  scripts/create_github_issues.sh [--repo owner/name] [--list | --create-remaining]

Default behavior is safe and read-only:
  scripts/create_github_issues.sh

Options:
  --repo owner/name       Target GitHub repository. Default: michaeliuedu/oncoreconcile-ai
  --list                  List current issues. This is the default.
  --create-remaining      Create the remaining P1 task issues (#6-#12). This can create duplicates.

Important:
  The project task issues have already been created. Prefer --list unless you are
  intentionally recreating missing P1 issues in a fresh repository.
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)
      REPO="${2:?Missing repository after --repo}"
      shift 2
      ;;
    --list)
      MODE="list"
      shift
      ;;
    --create-remaining)
      MODE="create-remaining"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1"
      usage
      exit 1
      ;;
  esac
done

if ! command -v gh >/dev/null 2>&1; then
  echo "GitHub CLI not found. Install gh or inspect docs/project_plan/github_issue_backlog.md manually."
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "GitHub CLI is not authenticated. Run: gh auth login -h github.com"
  exit 1
fi

if [[ "$MODE" == "list" ]]; then
  gh issue list --repo "$REPO" --limit 30
  exit 0
fi

echo "WARNING: --create-remaining can create duplicate issues."
echo "Target repository: $REPO"
echo "It will create these P1 issues:"
echo "  - P1: Wire review decisions to audit log"
echo "  - P1: Build upload and results UI"
echo "  - P1: Build review queue UI"
echo "  - P1: Add API documentation and local runbook"
echo "  - P1: Create demo case design document"
echo "  - P1: Prepare pitch deck outline"
echo "  - P1: Add demo smoke test checklist"
printf "Type CREATE to continue: "
read -r confirmation

if [[ "$confirmation" != "CREATE" ]]; then
  echo "Aborted."
  exit 0
fi

create_issue() {
  local title="$1"
  local body="$2"
  gh issue create --repo "$REPO" --title "$title" --body "$body"
}

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
