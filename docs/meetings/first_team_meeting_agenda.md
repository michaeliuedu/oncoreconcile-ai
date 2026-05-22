---

## Troubleshooting: Kill and Restart Backend/Frontend

If you need to restart both the backend (FastAPI) and frontend (Streamlit), use these commands:

**Kill all running processes:**
```bash
pkill -f streamlit && pkill -f uvicorn
```

**Restart backend:**
```bash
uvicorn src.api.main:app --reload
```

**Restart frontend (with correct API_URL):**
```bash
export API_URL=http://localhost:8000
streamlit run frontend/streamlit_app.py
```

*If you see 'Cannot connect to API', always check that both backend and frontend are running and that API_URL is set correctly.*
---

## Proactive Work on Blocked Issues & Backlog

Team members are encouraged to proceed proactively:

- **Blocked issues** can be started as soon as their dependencies are completed—even within the same sprint. If you finish your assigned task early, check if any blocked issue is now unblocked and begin work immediately.
- If a blocked issue is not yet ready, you can:
	- Help review or test ongoing work.
	- Prepare scaffolding, documentation, or test cases for the next blocked issue.
	- Pick up or propose “nice-to-have” (P2) or technical debt issues (e.g., refactoring, improving test coverage, enhancing documentation).
	- Draft user stories, UI mockups, or additional demo scenarios.

### Blocked Issues: When Can They Start?

| Issue | Can Start When... | Early Prep/Backlog Ideas |
|-------|-------------------|-------------------------|
| #3    | #1 & #2 done      | API/test scaffolding    |
| #5    | #4 done           | Uncertainty test cases  |
| #6    | #1 & #4 done      | Audit log design/tests  |
| #7    | #3 done           | UI wireframes           |
| #8    | #4 & #6 done      | UI/UX planning          |
| #10   | #2 done           | Outline/case notes      |
| #12   | #3 & #7 done      | Checklist template      |

As soon as a dependency is finished, the blocked issue can be started—no need to wait for the next sprint. Team members can also work on backlog or support tasks while waiting. This keeps everyone productive and the project moving forward.
# First Team Meeting Agenda

Meeting goal: align the team on the OncoReconcile AI competition vision, current repository status, MVP scope, GitHub issue workflow, and first task pickups.

Recommended duration: 60 minutes




## Quick Links

### Core Project Docs

- [MVP Overview & Diagram](../architecture/mvp_overview.md)
- [Competition Submission Proposal](../proposal/competition_submission_proposal.md)
- [Weekly Execution Plan](../project_plan/weekly_execution_plan.md)
- [Sprint 1 Assignments & Dependencies](#sprint-1-week-1-2-task-assignments-and-dependencies)
- [Hands-On Activities](#hands-on-activities-for-the-meeting)
- [Issue-to-File Mapping](#issue-to-file-mapping--where-to-start)
---

## Issue-to-File Mapping & Where to Start

This table helps each team member know where to start for each issue:

| Issue | Where to Start / Key Files |
|-------|----------------------------|
| #1 Canonical output schema | `src/api/schemas.py`, `src/agents/`, `tests/` |
| #2 Demo CSV dataset | `oncoreconcile_starter/oncology_variants_master.csv`, `gene_aliases.csv`, `variant_synonyms.csv` |
| #3 Batch endpoint | `src/api/routes.py`, `src/agents/workflow.py`, `tests/test_variant_workflow.py` |
| #4 Status logic | `src/agents/confidence_agent.py`, `src/agents/normalization_agent.py`, `src/api/schemas.py`, `tests/` |
| #5 Cannot-reconcile logic | `src/agents/reasoning_agent.py`, `src/agents/review_agent.py`, `src/api/schemas.py`, `tests/` |
| #6 Audit log | `src/governance/curation_log.py`, `review_queue.py`, `src/api/routes.py`, `tests/` |
| #7 Upload/results UI | `frontend/streamlit_app.py`, `frontend/README.md` |
| #8 Review queue UI | `frontend/streamlit_app.py`, `src/governance/review_queue.py` |
| #9 API docs/runbook | `README.md`, `src/api/routes.py`, `docs/` |
| #10 Demo case doc | `docs/project_plan/`, `oncoreconcile_starter/oncology_variants_master.csv` |
| #11 Pitch deck | `docs/proposal/` |
| #12 Smoke test checklist | `docs/project_plan/`, `tests/` |

Refer to this table when picking up an issue or starting a new task.
---

## Hands-On Activities for the Meeting

Make your meeting more efficient and engaging by including these hands-on activities:

1. **Live Repo Clone & Setup**
	- Everyone clones the repo and checks out the correct branch.
	- Command: `git clone https://github.com/michaeliuedu/oncoreconcile-ai.git`
	- Command: `git checkout gene-reconciliation`
	- Command: `pip install -r requirements.txt`

2. **Run the Test Suite**
	- Everyone runs `pytest -q` and confirms all tests pass (current: 18 passed).

3. **Start the Backend and Frontend**
	- One person shares their screen to run `uvicorn src.api.main:app --reload` and `streamlit run frontend/streamlit_app.py`.
	- Others follow along on their own machines.

4. **Try a Demo Input**
	- Use the Streamlit UI to submit a sample variant and walk through the workflow.
	- Show the API docs at [http://localhost:8000/docs](http://localhost:8000/docs).

5. **Assign Issues Live**
	- Use the GitHub Issues page to let each member claim a task.
	- Fill out the task claim template together.

6. **Quick Code/Docs Edit**
	- Make a small change (e.g., update a README or add a comment), commit, and push as a group to demonstrate the workflow.

7. **Q&A and Troubleshooting**
	- Allow time for anyone stuck on setup to get help immediately (screen sharing encouraged).

**Tip:**
- Encourage everyone to try these steps on their own machines after the meeting.
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


### 3. Current Repository Walkthrough & Demo Checklist: 10 minutes

Use:

- [Repository](https://github.com/michaeliuedu/oncoreconcile-ai)
- [Branch: gene-reconciliation](https://github.com/michaeliuedu/oncoreconcile-ai/tree/gene-reconciliation)
- [Architecture and Task Map](../architecture/task_mapped_architecture.md)
- [Architecture Diagrams](../diagrams/architecture_task_map.md)
- [Architecture and Task Map Google Doc](https://docs.google.com/document/d/1Ncew1t2lttX8mV2B5njBXqNFL4tie5-Wyizzx5ktPbA)


Show and Demo (step-by-step):

1. **Clone the repository**
	- [GitHub Repo](https://github.com/michaeliuedu/oncoreconcile-ai)
	- Command: `git clone https://github.com/michaeliuedu/oncoreconcile-ai.git`

2. **Check out the main development branch**
	- Command: `git checkout gene-reconciliation`

3. **Install dependencies**
	- Command: `pip install -r requirements.txt`

4. **Run all tests**
	- Command: `pytest -q`

5. **Start the FastAPI backend**
	- Command: `uvicorn src.api.main:app --reload`
	- Docs: [API routes](../src/api/routes.py)
	- Try: [http://localhost:8000/docs](http://localhost:8000/docs)

6. **Run the Streamlit frontend**
	- Command (local):
	  ```bash
	  export API_URL=http://localhost:8000
	  streamlit run frontend/streamlit_app.py
	  ```
	- Try: [http://localhost:8501](http://localhost:8501)
	- *This ensures the frontend connects to your local backend. If you see 'Cannot connect to API', check this step.*

7. **Explore the starter data**
	- Files: `oncoreconcile_starter/`, `data/examples/`, `data/reference/`
	- Docs: [Starter Data Integration Notes](../architecture/starter_data_integration.md)

8. **Review project planning and issues**
	- Docs: [Team Task Board](../project_plan/team_task_board.md), [GitHub Issue Backlog](../project_plan/github_issue_backlog.md)
	- Issues: [Open Issues](https://github.com/michaeliuedu/oncoreconcile-ai/issues)

9. **Map issues to architecture**
	- Docs: [Architecture and Task Map](../architecture/task_mapped_architecture.md)
	- Diagrams: [Architecture Diagrams](../diagrams/architecture_task_map.md)

10. **(Optional) Run with Docker**
	 - Command: `docker-compose up --build`
	 - Docs: [README](../../README.md)

**Tip:**
- Use the above commands live during the meeting to show the system working end-to-end.
- Encourage team members to try these steps on their own machines after the meeting.

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


---

## Sprint 1: Week 1–2 Task Assignments and Dependencies

This section summarizes the actionable work for the first two weeks, based on current features, issues, and dependencies.

### What Can Be Started (Week 1–2)

Assign 1 developer per unblocked P0/P1 issue:

1. **Canonical Output Schema (#1)**
	- Backend/data modeling
	- Unblocks batch endpoint, audit log, and UI

2. **Demo CSV Dataset (#2)**
	- Data curation
	- Unblocks batch endpoint tests, demo doc

3. **Status Logic (#4)**
	- Backend/AI
	- Unblocks review queue, audit, frontend badges

4. **API Docs/Runbook (#9)**
	- Docs/backend
	- Can be started and updated as endpoints are built

5. **Pitch Deck Outline (#11) or Demo Case Doc (#10)**
	- Docs/business/demo
	- #11 can start now; #10 can start as soon as #2 is underway

#### Example Week 1–2 Assignments Table

| Member | Primary Task                | Support/Review         | Docs/Demo/Testing      |
|--------|----------------------------|------------------------|------------------------|
| 1      | #1 Canonical output schema  | #3 Batch endpoint      | #9 API docs/runbook    |
| 2      | #2 Demo CSV dataset         | #1 Schema              | #10 Demo case doc      |
| 3      | #4 Status logic             | #5 Cannot-reconcile    | #11 Pitch deck outline |
| 4      | #9 API docs/runbook         | #4 Status logic        | #12 Smoke test (draft) |
| 5      | #11 Pitch deck outline      | #2 Demo CSV            | #8 Review queue UI (plan)|

**If someone finishes early:**
- Help with #1, #2, or #4, or start on #3 (batch endpoint) as soon as #1 and #2 are done.

### Dependencies Recap

- Start with unblocked issues: #1, #2, #4, #9, #11.
- As soon as #1 and #2 are done, #3 (batch endpoint) can begin.
- As soon as #4 is done, #5 (cannot-reconcile) and #6 (audit log) can begin.
- Docs and pitch can be updated continuously.

This plan ensures all team members have actionable work and that dependencies are cleared for the next sprint.

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
