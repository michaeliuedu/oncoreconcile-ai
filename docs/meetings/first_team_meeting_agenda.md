# First Team Meeting Agenda

Meeting goal: align the team on the OncoReconcile AI competition vision, current repository status, MVP scope, GitHub issue workflow, and first task pickups.

Recommended duration: 60 minutes

## Quick Links

### Core Project Docs

- [Competition Submission Proposal](../proposal/competition_submission_proposal.md)
- [Weekly Execution Plan](../project_plan/weekly_execution_plan.md)
- [Architecture and Task Map](../architecture/task_mapped_architecture.md)
- [Architecture Diagrams](../diagrams/architecture_task_map.md)
- [Team Task Board](../project_plan/team_task_board.md)
- [GitHub Issue Backlog](../project_plan/github_issue_backlog.md)
- [Starter Data Integration Notes](../architecture/starter_data_integration.md)

### Google Docs

- [Competition Proposal Google Doc](https://docs.google.com/document/d/18LXDOTTN-USMY87vyVr84RbKx4wY-iaYbksnUknI1Ck)
- [Weekly Execution Plan Google Doc](https://docs.google.com/document/d/1I87vM56YUbo4yRGR3Oh8VajytwmxDaEeYoP-ltOS_pM)
- [Architecture and Task Map Google Doc](https://docs.google.com/document/d/1Ncew1t2lttX8mV2B5njBXqNFL4tie5-Wyizzx5ktPbA)

### GitHub

- [Repository](https://github.com/michaeliuedu/oncoreconcile-ai)
- [Open Issues](https://github.com/michaeliuedu/oncoreconcile-ai/issues)
- [Branch: gene-reconciliation](https://github.com/michaeliuedu/oncoreconcile-ai/tree/gene-reconciliation)

### Initial GitHub Issues

P0 issues:

- [#1: Define canonical reconciliation output schema](https://github.com/michaeliuedu/oncoreconcile-ai/issues/1)
- [#2: Create curated demo CSV dataset](https://github.com/michaeliuedu/oncoreconcile-ai/issues/2)
- [#3: Build batch CSV reconciliation endpoint](https://github.com/michaeliuedu/oncoreconcile-ai/issues/3)
- [#4: Add explicit reconciliation status logic](https://github.com/michaeliuedu/oncoreconcile-ai/issues/4)
- [#5: Improve cannot-reconcile and ambiguity handling](https://github.com/michaeliuedu/oncoreconcile-ai/issues/5)

P1 issues:

- [#6: Wire review decisions to audit log](https://github.com/michaeliuedu/oncoreconcile-ai/issues/6)
- [#7: Build upload and results UI](https://github.com/michaeliuedu/oncoreconcile-ai/issues/7)
- [#8: Build review queue UI](https://github.com/michaeliuedu/oncoreconcile-ai/issues/8)
- [#9: Add API documentation and local runbook](https://github.com/michaeliuedu/oncoreconcile-ai/issues/9)
- [#10: Create demo case design document](https://github.com/michaeliuedu/oncoreconcile-ai/issues/10)
- [#11: Prepare pitch deck outline](https://github.com/michaeliuedu/oncoreconcile-ai/issues/11)
- [#12: Add demo smoke test checklist](https://github.com/michaeliuedu/oncoreconcile-ai/issues/12)

## Agenda

### 1. Welcome and Meeting Goal: 5 minutes

Purpose:

- Welcome team members.
- Explain that this is a competition MVP project.
- Set the tone: practical, demo-focused, human-governed AI.

Opening message:

> OncoReconcile AI is a trustworthy, human-governed AI workflow for reconciling messy oncology gene and variant names into traceable canonical outputs. We are not building clinical decision software. We are building an interoperability and governance demo that preserves uncertainty, provenance, and auditability.

### 2. Problem and Vision: 10 minutes

Use:

- [Competition Proposal Google Doc](https://docs.google.com/document/d/18LXDOTTN-USMY87vyVr84RbKx4wY-iaYbksnUknI1Ck)

Cover:

- Why precision oncology data is messy.
- Gene examples: `HER1 -> EGFR`, `p53 -> TP53`.
- Variant examples: `EGFR Ex19del -> EGFR exon 19 deletion`.
- Why uncertainty matters: `EGF-RX -> cannot_reconcile`.
- Human-governed AI is the differentiator.

### 3. Current Repository Walkthrough: 10 minutes

Use:

- [Repository](https://github.com/michaeliuedu/oncoreconcile-ai)
- [Branch: gene-reconciliation](https://github.com/michaeliuedu/oncoreconcile-ai/tree/gene-reconciliation)
- [Architecture and Task Map](../architecture/task_mapped_architecture.md)
- [Architecture Diagrams](../diagrams/architecture_task_map.md)
- [Architecture and Task Map Google Doc](https://docs.google.com/document/d/1Ncew1t2lttX8mV2B5njBXqNFL4tie5-Wyizzx5ktPbA)

Show:

- FastAPI backend scaffold
- CSV-backed gene reconciliation
- CSV-backed variant synonym lookup
- starter NSCLC dataset
- tests
- Streamlit frontend
- project planning docs
- GitHub issues
- how each GitHub issue maps to the architecture layer it improves

Suggested command for local setup:

```bash
pytest -q
```

### 4. MVP Scope: 10 minutes

Must-have MVP:

- gene alias reconciliation
- variant synonym reconciliation
- batch CSV input
- confidence score
- statuses: `reconciled`, `needs_review`, `cannot_reconcile`
- human review workflow
- audit/provenance display
- demo dashboard

Not first priority:

- clinical diagnosis
- treatment recommendation automation
- large dataset downloads
- BAM/FASTQ files
- multi-page PDF parsing
- full production HGVS normalization
- complex structural variant automation

### 5. GitHub Issues and Task Pickup: 15 minutes

Use:

- [Open Issues](https://github.com/michaeliuedu/oncoreconcile-ai/issues)
- [Team Task Board](../project_plan/team_task_board.md)
- [Weekly Execution Plan](../project_plan/weekly_execution_plan.md)
- [Architecture and Task Map](../architecture/task_mapped_architecture.md)
- [Architecture Diagrams](../diagrams/architecture_task_map.md)

Ask each coding contributor to pick:

- one primary coding task
- one support/review task
- one docs/demo/testing task

Recommended first pickups:

- #1 Canonical output schema
- #2 Demo CSV dataset
- #3 Batch reconciliation endpoint
- #4 Status logic
- #5 Cannot-reconcile handling
- #11 Pitch deck outline

Task claim template:

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

### 6. Working Agreement: 5 minutes

Agree on:

- Use GitHub issues as the source of truth.
- Comment on an issue before starting work.
- Create small branches and small PRs.
- Every code PR should include a test or demo proof.
- Communicate blockers early.
- Do not expand scope without team discussion.

Suggested branch names:

```text
issue-1-canonical-schema
issue-2-demo-csv
issue-3-batch-endpoint
```

### 7. Next Steps and Close: 5 minutes

Before ending, confirm:

- Who is taking which issue?
- What will be done before the next checkpoint?
- When is the next team sync?
- Who will review the first PRs?

Immediate action items:

- Everyone clones the repo.
- Everyone runs tests.
- Everyone comments on their chosen GitHub issue.
- Project lead confirms assignments.
- PM/business lead starts the pitch outline.
- First PRs target P0 issues.

## Desired Meeting Outcomes

By the end of the meeting:

- Everyone understands the project goal.
- Everyone understands MVP scope.
- Everyone knows where docs and issues are.
- At least 5 issues have tentative owners.
- The next checkpoint is scheduled.
- The team agrees to protect scope.

## Closing Message

> Our north star is a narrow, polished demo: upload messy oncology mutation examples, reconcile gene and variant names, show confidence and status, route uncertain cases to review, and preserve an audit trail. If we can do that clearly, we will have a strong competition project.


## Best Practices for Collaboration & Repo Stability

**Branching Strategy:**
- Each feature, bugfix, or task should have its own branch (e.g., `feature/xyz`, `bugfix/abc`).
- Work independently on branches; keep `master`/`main` stable.

**Frequent Commits & Pull Requests:**
- Make small, frequent commits with clear messages.
- Open pull requests (PRs) for review before merging to the main branch.

**Code Review:**
- Review each other’s PRs for code quality, logic, and style.
- Check for potential bugs, test coverage, and documentation.

**Automated Testing:**
- Run tests automatically (CI/CD) on every PR to catch issues early.
- Only merge PRs that pass all tests.

**Continuous Integration:**
- Use CI tools (e.g., GitHub Actions) to build, lint, and test the codebase on every push/PR.
- Ensure the main branch is always deployable.

**Documentation & Communication:**
- Update documentation as features are added or changed.
- Use issues, project boards, and regular meetings to coordinate work and track progress.

**Regular Syncs:**
- Rebase or merge the latest master into feature branches frequently to avoid conflicts.
- Hold short standups or async check-ins to keep everyone aligned.

**Additional Tips for Starting Collaboration:**
- Agree on coding style and formatting (consider using linters/formatters).
- Set up local environments and run all tests before starting work.
- Communicate blockers or questions early—don’t get stuck alone.
- Respect scope: avoid adding features or making large changes without team discussion.
- Celebrate small wins and help each other learn!
