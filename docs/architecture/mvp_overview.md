# OncoReconcile AI MVP Overview

## 1. MVP System Diagram


Below is a high-level diagram of the MVP, showing the true status of each feature:

```mermaid
graph TD
    A[User Uploads CSV via UI #7]:::partial --> B[Streamlit Frontend #7 #8]:::done
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

    class B,D,E,F done;
    class A,C,I partial;
    class G,H,J,K next;
    class L future;
```

- **Green:** Complete or MVP-ready (current week)
- **Yellow:** Partial/in progress (needs work for full MVP)
- **Orange:** Next week
- **Red:** Future/blocked (post-MVP or dependent)

- **Green:** Complete or MVP-ready (current week)
- **Yellow:** In progress or next week
- **Red:** Future/blocked (post-MVP or dependent)


## 2. Feature Status Details

| Feature                                 | Status    | Details | Issue(s) |
|------------------------------------------|-----------|---------|----------|
| User Uploads CSV via UI                  | Partial   | Only single variant input via text; CSV upload not yet implemented | #7 |
| Streamlit Frontend                       | Ready     | All main UI pages present; single variant input, review queue, audit log | #7, #8 |
| API: Batch Reconciliation Endpoint       | Partial   | Only single variant per request; batch endpoint not yet implemented | #3 |
| Agents: Normalization, Confidence, Reasoning | Ready | Full pipeline for single variant; multi-agent orchestration | #4, #5 |
| Canonical Output Schema                  | Ready     | Pydantic models in place for all outputs | #1 |
| Status Logic                             | Ready     | Status set by workflow/confidence agent | #4, #5 |
| Download/View Results in UI              | Partial   | Results shown in UI; no explicit download button | #7 |
| Audit Log & Provenance                   | Next      | Audit log and provenance tracking planned | #6 |
| Review Queue                             | Next      | Review queue backend and UI planned | #8 |
| Human Review Workflow                    | Next      | Human review workflow planned | #8 |
| Audit Trail Display                      | Next      | Audit trail display in UI planned | #6 |
| Demo Dashboard                           | Future    | Dashboard/summary views, test cases | #10, #12 |

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
