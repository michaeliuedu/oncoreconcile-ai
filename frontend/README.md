# OncoReconcile AI - Streamlit Frontend

This is the interactive web interface for OncoReconcile AI.

## Features

- **Variant Reconciliation**: Submit raw variant strings for reconciliation
- **Review Queue Dashboard**: View pending expert reviews
- **Approval Interface**: Expert reviewers can approve/reject reconciliations
- **Audit Trail Viewer**: Track all historical decisions

## Running the App

```bash
streamlit run frontend/streamlit_app.py
```

Access at: http://localhost:8501

## Screens

### 1. Variant Submission
- Input raw variant (e.g., "EGFR Ex19del")
- Specify tissue and source
- View reconciliation progress
- Get canonical variant result

### 2. Review Queue
- List pending reviews by priority
- Filter by queue type
- View system reasoning
- Route to expert reviewers

### 3. Expert Review
- Review system recommendations
- Examine confidence breakdown
- View approval history
- Make approval decision

### 4. Audit Log
- View historical approvals
- Filter by reviewer or variant
- Export audit trail

---

See main README for API documentation.
