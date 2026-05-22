# OncoReconcile AI MVP Overview

## 1. MVP System Diagram


Below is a high-level diagram of the MVP, showing the true status of each feature:

```mermaid
graph TD
    Z[Demo CSV Dataset #2]:::done --> A[User Uploads CSV via UI #7]:::partial
    A --> B[Streamlit Frontend #7 #8]:::partial
    B --> C[API Batch Reconciliation Endpoint #3]:::partial
    C --> D[Agents Normalization Confidence Reasoning #4 #5]:::done
    D --> E[Canonical Output Schema #1]:::done
    D --> F[Status Logic reconciled needs_review cannot_reconcile #4 #5]:::done
    D --> G[Audit Log and Provenance #6]:::next
    D --> H[Review Queue #8]:::next
    E --> I[Download View Results in UI #7]:::partial
    H --> J[Human Review Workflow #8]:::next
    J --> G
    G --> K[Audit Trail Display #6]:::next
    I --> L[Demo Dashboard #10 #12]:::future

    classDef done fill:#b6e7a0,stroke:#333,stroke-width:2px;
    classDef partial fill:#ffe599,stroke:#333,stroke-width:2px;
    classDef next fill:#ffe599,stroke:#333,stroke-width:2px;
    classDef future fill:#f4cccc,stroke:#333,stroke-width:2px;

    class Z,D,E,F done;
    class A,B,C,I partial;
    class G,H,J,K next;
    class L future;
```
## 1a. Issues That Can Be Started Without Blockers


The following issues can be started immediately (no dependencies):

- **#9: Add API documentation and local runbook**
- **#11: Prepare pitch deck outline**

**Note:**
- #1 (Canonical output schema), #2 (Demo CSV dataset), and #4 (Status logic) are now complete and open for team review. See the feature status table above.

Once #1, #2, and #4 were completed, #3 (batch endpoint) became unblocked. See the main meeting agenda for a full dependency table.

- **Green:** Complete or MVP-ready (current week)
- **Yellow:** Partial/in progress (needs work for full MVP)
- **Orange:** Next week
- **Red:** Future/blocked (post-MVP or dependent)

- **Green:** Complete or MVP-ready (current week)
- **Yellow:** In progress or next week
- **Red:** Future/blocked (post-MVP or dependent)


## 2. Feature Status Details

| Feature                                 | Status    | Details | Issue(s) | Blocker(s) | Plug-in Point |
|------------------------------------------|-----------|---------|----------|------------|---------------|
| User Uploads CSV via UI                  | Partial   | Only single variant input via text; CSV upload not yet implemented | #7 | #3 | After #3 merged, connect UI to batch endpoint |
| Streamlit Frontend                       | Ready     | All main UI pages present; single variant input, review queue, audit log | #7, #8 |  |  |
| API: Batch Reconciliation Endpoint       | Partial   | Only single variant per request; batch endpoint not yet implemented | #3 | #1, #2 | After #1, #2 merged, update endpoint/tests |
| Agents: Normalization, Confidence, Reasoning | Ready | Full pipeline for single variant; multi-agent orchestration | #4, #5 |  |  |
| Canonical Output Schema                  | Complete  | Pydantic models in place for all outputs. Feature implemented and MVP-ready. Team review welcome. | #1 |  |  |
| Demo CSV Dataset                         | Complete  | Curated demo CSVs in place. Feature implemented and MVP-ready. Team review welcome. | #2 |  |  |
| Status Logic                             | Complete  | Status set by workflow/confidence agent. Feature implemented and MVP-ready. Team review welcome. | #4, #5 |  |  |
| Download/View Results in UI              | Partial   | Results shown in UI; no explicit download button | #7 | #3 | After #3 merged, connect UI to batch endpoint |
| Audit Log & Provenance                   | Next      | Audit log and provenance tracking planned | #6 | #1, #4 | After #1, #4 merged, update schema |
| Review Queue                             | Next      | Review queue backend and UI planned | #8 | #4, #6 | After #4, #6 merged, connect UI/backend |
| Human Review Workflow                    | Next      | Human review workflow planned | #8 | #4, #6 | After #4, #6 merged, connect UI/backend |
| Audit Trail Display                      | Next      | Audit trail display in UI planned | #6 | #1, #4 | After #1, #4 merged, update schema |
| Demo Dashboard                           | Future    | Dashboard/summary views, test cases | #10, #12 | #2, #3, #7 | After #2, #3, #7 merged, finalize dashboard |

## 3. What’s Next (Next Week)
- Audit log and provenance tracking
- Review queue (backend and UI)
- Human review workflow
- Audit trail display in UI
- More demo/test cases

## 4. What’s After (Future)
- Demo dashboard/summary views
- Advanced review/curation features
- Additional data integrations
- Stretch goals (see proposal)

---

**See also:**
- [Issue-to-File Mapping](../meetings/first_team_meeting_agenda.md#issue-to-file-mapping--where-to-start)
- [Architecture and Task Map](task_mapped_architecture.md)
- [Weekly Execution Plan](../project_plan/weekly_execution_plan.md)

---

*This diagram and summary help the team see what’s built, what’s next, and how new issues fit into the overall MVP.*
