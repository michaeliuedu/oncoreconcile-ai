# Architecture and Task Map Diagrams

These diagrams visualize the OncoReconcile AI MVP architecture and show where each GitHub issue fits.

## MVP System Architecture

```mermaid
flowchart TD
    user["User / Demo Operator"]

    subgraph frontend["Frontend Demo UI"]
        upload["Upload CSV / Paste Rows"]
        results["Results Table"]
        review_ui["Review Queue UI"]
        audit_ui["Audit View"]
    end

    subgraph api["FastAPI Backend"]
        routes["API Routes"]
        schemas["Request / Response Schemas"]
        batch["Batch Processing"]
    end

    subgraph workflow["Reconciliation Workflow"]
        gene["Gene Reconciliation"]
        extract["Variant Extraction"]
        normalize["Variant Normalization"]
        retrieve["Candidate Retrieval"]
        reason["AI-Assisted Explanation"]
        confidence["Confidence Scoring"]
        status["Status Classification"]
    end

    subgraph governance["Human Governance"]
        queue["Review Queue"]
        decision["Approve / Reject / Request Changes"]
        audit["Audit Log"]
    end

    subgraph data["Reference and Demo Data"]
        aliases["Gene Aliases CSV"]
        synonyms["Variant Synonyms CSV"]
        canonical["Canonical Variants CSV"]
        evidence["Evidence Hints"]
        demo["Demo CSV"]
    end

    user --> upload
    upload --> routes
    routes --> schemas
    schemas --> batch
    batch --> gene
    gene --> extract
    extract --> normalize
    normalize --> retrieve
    retrieve --> reason
    reason --> confidence
    confidence --> status
    status --> results
    status --> queue
    queue --> review_ui
    review_ui --> decision
    decision --> audit
    audit --> audit_ui

    aliases --> gene
    synonyms --> normalize
    canonical --> retrieve
    evidence --> reason
    demo --> upload
```

## Issue-to-Architecture Map

```mermaid
flowchart LR
    subgraph data_layer["Data and Reference Layer"]
        i2["#2 Demo CSV Dataset"]
    end

    subgraph backend_layer["Backend and Workflow Layer"]
        i1["#1 Canonical Output Schema"]
        i3["#3 Batch Reconciliation Endpoint"]
        i4["#4 Status Logic"]
        i5["#5 Cannot-Reconcile Handling"]
    end

    subgraph governance_layer["Governance Layer"]
        i6["#6 Review Decisions to Audit Log"]
    end

    subgraph frontend_layer["Frontend Layer"]
        i7["#7 Upload and Results UI"]
        i8["#8 Review Queue UI"]
    end

    subgraph docs_layer["Docs, Demo, and PM Layer"]
        i9["#9 API Docs and Runbook"]
        i10["#10 Demo Case Design"]
        i11["#11 Pitch Deck Outline"]
        i12["#12 Demo Smoke Test Checklist"]
    end

    i1 --> i3
    i2 --> i3
    i1 --> i4
    i4 --> i5
    i4 --> i6
    i3 --> i7
    i4 --> i7
    i6 --> i8
    i4 --> i8
    i3 --> i9
    i2 --> i10
    i3 --> i12
    i7 --> i12
    i10 --> i11
```

## Demo Story Flow

```mermaid
sequenceDiagram
    actor User
    participant UI as Demo UI
    participant API as FastAPI Backend
    participant WF as Reconciliation Workflow
    participant KB as Reference Data
    participant Review as Human Review
    participant Audit as Audit Log

    User->>UI: Upload messy oncology rows
    UI->>API: POST /reconcile/batch
    API->>WF: Process each row
    WF->>KB: Lookup gene aliases and variant synonyms
    KB-->>WF: Candidate canonical mappings
    WF-->>API: Confidence, status, explanation
    API-->>UI: Reconciliation results

    alt High confidence
        UI-->>User: Show reconciled result
    else Ambiguous
        UI-->>Review: Route to review queue
        Review->>Audit: Record approve/reject decision
        Audit-->>UI: Display audit trail
    else Low confidence
        UI-->>User: Show cannot_reconcile
    end
```

## Status Decision Concept

```mermaid
flowchart TD
    input["Raw gene + variant input"]
    gene_match{"Gene reconciled?"}
    variant_match{"Variant reconciled?"}
    confidence{"Confidence high enough?"}
    ambiguity{"Ambiguous or review rule?"}
    reconciled["Status: reconciled"]
    needs_review["Status: needs_review"]
    cannot["Status: cannot_reconcile"]

    input --> gene_match
    gene_match -- "No" --> cannot
    gene_match -- "Yes" --> variant_match
    variant_match -- "No" --> cannot
    variant_match -- "Yes" --> confidence
    confidence -- "Low" --> cannot
    confidence -- "Moderate" --> needs_review
    confidence -- "High" --> ambiguity
    ambiguity -- "Yes" --> needs_review
    ambiguity -- "No" --> reconciled
```

## How to Use These Diagrams

- Use the MVP System Architecture diagram to explain the overall project to new team members and judges.
- Use the Issue-to-Architecture Map to help team members pick tasks and understand dependencies.
- Use the Demo Story Flow to rehearse the final competition walkthrough.
- Use the Status Decision Concept to explain why uncertainty is preserved instead of forcing mappings.
