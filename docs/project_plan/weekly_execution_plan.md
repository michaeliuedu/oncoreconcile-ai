# OncoReconcile AI Weekly Execution Plan

This execution plan translates the competition proposal into weekly, team-pickup work. It is designed for a project lead, five coding-capable contributors, and one PM/business/marketing contributor.

## Team Operating Model

Each coding contributor should pick a mixed set of tasks each week:

- one primary coding task
- one support or review task
- one documentation, testing, or demo task

The project lead coordinates scope, architecture, code review, final integration, and demo readiness. The PM/business/marketing lead coordinates user framing, pitch narrative, market positioning, deck preparation, and demo storytelling.

## Weekly Ritual

Use this cadence every week:

| Day | Activity |
| --- | --- |
| Monday | Confirm weekly goals, review open GitHub issues, and let members claim tasks. |
| Tuesday-Thursday | Build, test, document, and open small PRs. |
| Midweek | 15-minute checkpoint for blockers and dependency alignment. |
| Friday | Review PRs, merge stable work, update docs and issues. |
| Weekend | Run demo smoke test and record what is ready, risky, or blocked. |

## GitHub Workflow

Use the 12 starter GitHub issues as the initial task board:

- #1: P0 Define canonical reconciliation output schema
- #2: P0 Create curated demo CSV dataset
- #3: P0 Build batch CSV reconciliation endpoint
- #4: P0 Add explicit reconciliation status logic
- #5: P0 Improve cannot-reconcile and ambiguity handling
- #6: P1 Wire review decisions to audit log
- #7: P1 Build upload and results UI
- #8: P1 Build review queue UI
- #9: P1 Add API documentation and local runbook
- #10: P1 Create demo case design document
- #11: P1 Prepare pitch deck outline
- #12: P1 Add demo smoke test checklist

Priority definitions:

| Priority | Meaning |
| --- | --- |
| P0 | Required for the core competition MVP demo. |
| P1 | Important for polish, explainability, and demo confidence. |
| P2 | Nice to have only after the P0/P1 path is stable. |

## Week 1: Alignment, Scope, and Task Setup

### Goals

- Freeze the initial MVP scope.
- Confirm the demo story.
- Ensure every contributor understands the repo and task board.
- Make sure GitHub issues are ready for pickup.

### Recommended Pickup Tasks

| Role/Interest | Suggested Tasks |
| --- | --- |
| Project lead | Confirm MVP scope, assign issue priorities, review branch/PR rules. |
| Backend interest | Review current FastAPI routes and identify endpoint gaps. |
| Data interest | Review starter data and current reference CSVs. |
| AI/retrieval interest | Review confidence scoring and reasoning placeholders. |
| Frontend interest | Review Streamlit app and sketch upload/results flow. |
| Governance/testing interest | Review current tests and audit/review modules. |
| PM/business | Draft problem framing, user personas, and pitch narrative outline. |

### Deliverables

- Confirmed MVP scope.
- Team task board reviewed.
- GitHub issues claimed or ready for claiming.
- Initial demo story documented.

### Exit Criteria

- Everyone knows how to run tests.
- Everyone knows how to claim an issue.
- P0 issues #1-#5 are understood and sequenced.

## Week 2: Canonical Objects and Demo Data

### Goals

- Define the canonical reconciliation output object.
- Create the curated demo CSV.
- Make provenance and status fields explicit.

### Primary Issues

- #1: Define canonical reconciliation output schema
- #2: Create curated demo CSV dataset

### Dependencies

Issue #3 depends on #1 and #2.
Issue #4 depends on confidence/status fields from #1.

### Suggested Task Mix

| Contributor Interest | Primary Task | Support Task | Docs/Demo Task |
| --- | --- | --- | --- |
| Backend | Add schema models for canonical output. | Review API response shapes. | Add example JSON response. |
| Data | Create `data/demo/demo_variants.csv`. | Validate expected gene/variant mappings. | Document demo cases. |
| AI/retrieval | Define explanation fields. | Review confidence inputs. | Draft confidence explanation examples. |
| Frontend | Mock results table using sample JSON. | Review needed fields from backend. | Capture UI requirements. |
| Governance/testing | Add schema tests. | Add unresolved-output tests. | Define review state fields. |
| PM/business | Connect demo examples to user pain. | Review terminology for judges. | Draft slide bullets. |

### Deliverables

- Canonical reconciliation output schema.
- Demo CSV v1.
- Tests for reconciled and unresolved result shapes.
- Example output JSON.

### Exit Criteria

- Batch endpoint work can begin without guessing output fields.
- Demo data contains reconciled, needs-review, and cannot-reconcile examples.

## Week 3: Batch Reconciliation API

### Goals

- Add a backend endpoint for reconciling multiple rows.
- Connect gene and variant normalization into one row-level output.
- Return stable structured results for the frontend.

### Primary Issues

- #3: Build batch CSV reconciliation endpoint

### Dependencies

Depends on #1 and #2.
Feeds #7 and #12.

### Suggested Task Mix

| Contributor Interest | Primary Task | Support Task | Docs/Demo Task |
| --- | --- | --- | --- |
| Backend | Implement `POST /reconcile/batch`. | Add partial failure handling. | Document request/response. |
| Data | Provide demo rows for endpoint tests. | Validate expected outputs. | Maintain demo CSV notes. |
| AI/retrieval | Attach confidence details to batch output. | Review candidate matching behavior. | Draft explanation snippets. |
| Frontend | Build against mock batch output. | Identify missing fields. | Sketch upload state handling. |
| Governance/testing | Add API integration tests. | Add malformed-row tests. | Draft smoke test step. |
| PM/business | Refine end-to-end demo story. | Review outputs for judge readability. | Draft narration for upload step. |

### Deliverables

- Batch reconciliation endpoint.
- API tests for batch happy path and unresolved input.
- Stable example response for frontend.

### Exit Criteria

- A user can submit multiple rows and receive one result per row.
- Bad rows do not crash the whole batch.

## Week 4: Status, Confidence, and Uncertainty

### Goals

- Implement explicit reconciliation statuses.
- Avoid forced mappings for low-confidence inputs.
- Make confidence/explanation outputs judge-readable.

### Primary Issues

- #4: Add explicit reconciliation status logic
- #5: Improve cannot-reconcile and ambiguity handling

### Dependencies

Depends on #1 and the existing confidence/normalization flow.
Feeds #6, #7, #8, and #12.

### Suggested Task Mix

| Contributor Interest | Primary Task | Support Task | Docs/Demo Task |
| --- | --- | --- | --- |
| Backend | Add status classifier service. | Wire statuses into API output. | Document status meanings. |
| Data | Add unresolved and ambiguous examples. | Validate expected statuses. | Update demo case doc. |
| AI/retrieval | Tune confidence thresholds. | Add uncertainty reasons. | Write explanation examples. |
| Frontend | Add status badges and confidence display. | Test status rendering. | Capture status screenshots. |
| Governance/testing | Add tests for all statuses. | Confirm needs-review routing logic. | Add test checklist items. |
| PM/business | Prepare "trustworthy uncertainty" story. | Review wording for nontechnical audience. | Draft pitch slide. |

### Deliverables

- `reconciled`, `needs_review`, and `cannot_reconcile` logic.
- Tests for each status.
- Human-readable uncertainty reasons.

### Exit Criteria

- `EGF-RX` or similar unknown inputs do not get overconfident mappings.
- At least one row demonstrates each status in the demo.

## Week 5: Review Workflow and Audit Trail

### Goals

- Make human governance visible.
- Connect review decisions to audit records.
- Prepare review queue UI or Streamlit equivalent.

### Primary Issues

- #6: Wire review decisions to audit log
- #8: Build review queue UI

### Dependencies

Depends on #4 and #5.
Feeds final governance demo.

### Suggested Task Mix

| Contributor Interest | Primary Task | Support Task | Docs/Demo Task |
| --- | --- | --- | --- |
| Backend | Add approve/reject/request-changes behavior. | Add audit endpoint. | Document review APIs. |
| Data | Mark demo rows that require review. | Validate review routing. | Add review examples. |
| AI/retrieval | Add reviewer-facing explanation summary. | Review confidence breakdown. | Draft reviewer notes examples. |
| Frontend | Build review queue and detail view. | Add review action controls. | Capture review workflow screenshot. |
| Governance/testing | Add audit tests. | Add review status transition tests. | Write governance checklist. |
| PM/business | Prepare governance narrative. | Review audit wording. | Create governance slide. |

### Deliverables

- Review actions.
- Audit records.
- Review queue UI or demo view.
- Tests for review decisions.

### Exit Criteria

- A needs-review row can be reviewed.
- Review decision is visible in an audit trail.

## Week 6: Frontend Integration and Demo Stabilization

### Goals

- Make the demo usable end to end.
- Polish the upload/results/review flow.
- Add a repeatable smoke test checklist.

### Primary Issues

- #7: Build upload and results UI
- #12: Add demo smoke test checklist

### Dependencies

Depends on #3, #4, and #6 for full workflow.

### Suggested Task Mix

| Contributor Interest | Primary Task | Support Task | Docs/Demo Task |
| --- | --- | --- | --- |
| Backend | Fix API issues found by UI. | Improve errors. | Update runbook notes. |
| Data | Freeze demo CSV. | Validate final demo rows. | Add expected-output table. |
| AI/retrieval | Tune explanations for clarity. | Remove noisy debug details. | Draft explanation guide. |
| Frontend | Polish upload/results UI. | Add filtering by status. | Capture screenshots. |
| Governance/testing | Run smoke tests. | Add missing regression tests. | Maintain checklist. |
| PM/business | Rehearse story against UI. | Identify confusing language. | Draft demo script. |

### Deliverables

- End-to-end demo path.
- Smoke test checklist.
- Frozen demo dataset.
- Screenshots for presentation.

### Exit Criteria

- Demo can run from fresh start.
- Team can show reconciled, needs-review, and cannot-reconcile rows.

## Week 7: Presentation and Demo Package

### Goals

- Prepare the final pitch deck.
- Finalize demo script and screenshots.
- Avoid risky new features.

### Primary Issues

- #9: Add API documentation and local runbook
- #10: Create demo case design document
- #11: Prepare pitch deck outline

### Dependencies

Depends on the stable demo path and frozen demo data.

### Suggested Task Mix

| Contributor Interest | Primary Task | Support Task | Docs/Demo Task |
| --- | --- | --- | --- |
| Backend | Final API cleanup only. | Review runbook. | Add endpoint examples. |
| Data | Validate final demo case document. | Check terminology. | Add data source notes. |
| AI/retrieval | Finalize explanation wording. | Review confidence claims. | Add AI limitation notes. |
| Frontend | Final UI polish only. | Capture screenshots. | Help demo script. |
| Governance/testing | Run full smoke test repeatedly. | Track residual risks. | Add Q&A notes. |
| PM/business | Build deck and narrative. | Coordinate rehearsal. | Prepare submission wording. |

### Deliverables

- API documentation.
- Local runbook.
- Demo case design document.
- Pitch deck outline or draft.
- Demo script.

### Exit Criteria

- Team can rehearse the full story without new engineering work.
- All claims in the deck match what the repo can demonstrate.

## Week 8: Final Integration and Submission

### Goals

- Finalize repository, docs, demo, and presentation.
- Submit competition materials.
- Focus only on bug fixes and clarity.

### Suggested Task Mix

| Contributor Interest | Primary Task | Support Task | Docs/Demo Task |
| --- | --- | --- | --- |
| Project lead | Final branch/PR review and release readiness. | Confirm no scope drift. | Final technical summary. |
| Backend | Fix critical API bugs only. | Verify startup path. | Review run instructions. |
| Data | Verify demo data and expected outputs. | Check source attributions. | Final dataset notes. |
| AI/retrieval | Verify explanations and confidence labels. | Remove unsupported claims. | Add limitations section. |
| Frontend | Final visual polish and demo stability. | Confirm screenshots. | Help video/demo walkthrough. |
| Governance/testing | Run final smoke test. | Record known limitations. | Final QA checklist. |
| PM/business | Final deck, narration, and submission. | Coordinate rehearsals. | Prepare final pitch. |

### Deliverables

- Final working MVP.
- Final GitHub repository.
- Final proposal and technical documentation.
- Pitch deck.
- Demo walkthrough or video if required.
- Submission package.

### Exit Criteria

- Demo runs reliably.
- Proposal, README, and deck tell the same story.
- The team can explain limitations clearly.

## Risk Management

| Risk | Mitigation |
| --- | --- |
| Scope creep into complex variants | Keep fusions/CNVs as review examples, not full automation. |
| Frontend takes too long | Use Streamlit for MVP and React only if time permits. |
| Semantic AI is not ready | Use deterministic synonym retrieval and template explanations for MVP. |
| Data downloads become distracting | Use curated starter data first; public data later. |
| Review/audit persistence is incomplete | Use simple in-memory or file-backed audit for demo if database work is not ready. |
| Demo instability | Freeze features by Week 6 and use smoke tests. |

## Definition of Done for MVP

The competition MVP is done when the team can show:

1. A small table of messy oncology gene/variant inputs.
2. Gene alias reconciliation.
3. Variant synonym reconciliation.
4. Confidence score and explanation.
5. Explicit status: reconciled, needs_review, or cannot_reconcile.
6. Human review action for at least one row.
7. Audit/provenance display for the review action.
8. Clear statement that this is a research prototype, not clinical software.
