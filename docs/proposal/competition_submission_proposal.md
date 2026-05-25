# OncoReconcile AI

## AI-Assisted Oncology Gene & Variant Reconciliation Platform

Project proposal for the DFWIT AI Competition.

## 1. Project Summary

OncoReconcile AI is an AI-assisted interoperability and governance platform for reconciling inconsistent oncology gene and variant representations into traceable, standards-aligned canonical knowledge objects.

Precision oncology workflows depend on genomic data from molecular laboratories, sequencing vendors, pathology reports, bioinformatics pipelines, and public knowledge bases. However, the same gene or variant may appear in many different forms across systems. For example, `HER1`, `ERBB1`, and `EGFR` may refer to the same gene, while `EGFR Ex19del`, `E746_A750del`, `c.2235_2249del`, and `p.E746_A750del` may represent the same biological variant concept.

These inconsistencies create barriers for molecular pathology teams, variant curators, clinical bioinformatics workflows, tumor boards, and downstream AI systems. Today, reconciliation is often manual, difficult to audit, and inconsistent across tools.

OncoReconcile AI aims to demonstrate a trustworthy, human-governed AI workflow that supports gene alias reconciliation, variant normalization, semantic candidate retrieval, confidence scoring, uncertainty handling, and expert review.

This project is a research and educational prototype. It is not clinical software and does not provide diagnosis or treatment recommendations.

## 2. Problem Statement

Precision oncology increasingly depends on accurate interpretation of genomic alterations. However, genomic findings are often represented inconsistently across laboratories, public databases, clinical reports, and analytics platforms.

Examples of inconsistent gene representation:

| Inconsistent Gene Representation | Canonical Gene |
| --- | --- |
| HER1 | EGFR |
| ERBB1 | EGFR |
| p53 | TP53 |
| C-MET | MET |

Examples of inconsistent variant representation:

| Inconsistent Variant Representation | Canonical Variant Concept |
| --- | --- |
| EGFR Ex19del | EGFR exon 19 deletion |
| E746_A750del | EGFR exon 19 deletion |
| c.2235_2249del | EGFR exon 19 deletion |
| p.E746_A750del | EGFR exon 19 deletion |
| R175H | TP53 p.R175H |

These inconsistencies affect molecular pathology laboratories, precision oncology programs, variant curation teams, clinical bioinformatics workflows, translational genomics teams, tumor boards, oncology analytics platforms, and AI-assisted healthcare workflows.

Existing reconciliation workflows often fail to preserve original source strings, provenance, transcript/build context, uncertainty, evidence references, confidence information, human review history, and auditability.

As AI becomes more involved in healthcare and biomedical data workflows, trustworthy semantic interoperability becomes increasingly important.

## 3. Proposed Solution

OncoReconcile AI is designed to reconcile heterogeneous oncology gene and variant representations into governed canonical knowledge objects.

The platform combines:

- gene name reconciliation
- deterministic normalization
- variant synonym matching
- semantic retrieval
- AI-assisted reasoning
- confidence and uncertainty scoring
- human review workflows
- provenance-aware audit tracking

The goal is not to replace expert judgment. Instead, OncoReconcile AI assists human-governed reconciliation workflows by preserving evidence, uncertainty, and traceability.

Key design principles:

- preserve original source evidence
- separate extraction from interpretation
- maintain traceability and auditability
- support `cannot_reconcile` outcomes
- preserve uncertainty instead of forcing mappings
- align with standards-aware canonical modeling
- support human review and governance

## 4. MVP Scope

The competition MVP will focus on a curated, high-quality oncology reconciliation workflow using non-small cell lung cancer and related precision oncology examples.

Core automated MVP scope:

- gene alias reconciliation
- SNV and small-indel variant synonym reconciliation
- curated NSCLC/LUAD demo examples
- EGFR, KRAS, BRAF, and TP53 examples
- structured mutation-table style inputs
- confidence-aware status classification
- human review routing
- traceable canonical outputs

Selected review-oriented examples may include ALK fusion, ROS1 fusion, RET fusion, MET exon 14 skipping, and ERBB2 amplification. These broader alteration types will be used primarily to demonstrate ambiguity handling and human review workflows, not full automated clinical interpretation.

Out of scope for the initial MVP:

- clinical diagnosis
- treatment recommendation automation
- full production HGVS normalization
- large-scale genomic data ingestion
- multi-page PDF parsing
- BAM/FASTQ processing
- complex structural variant interpretation
- enterprise authentication
- clinical deployment

## 5. Core Workflow

```text
Input Mutation Data
        ↓
Gene Name Reconciliation
        ↓
Variant Extraction
        ↓
Normalization Layer
        ↓
Candidate Retrieval
        ↓
AI-Assisted Reasoning
        ↓
Confidence & Uncertainty Scoring
        ↓
Human Review Workflow
        ↓
Governed Canonical Knowledge Object
```

## 6. Example Workflow

Input data:

| Original Gene | Original Variant |
| --- | --- |
| HER1 | Ex19del |
| ERBB1 | E746_A750del |
| p53 | R175H |
| EGF-RX | UnknownDel19 |

Reconciliation output:

| Original Input | Canonical Gene | Canonical Variant | Confidence | Status |
| --- | --- | --- | --- | --- |
| HER1 Ex19del | EGFR | EGFR exon 19 deletion | 0.97 | Needs Review |
| ERBB1 E746_A750del | EGFR | EGFR exon 19 deletion | 0.98 | Reconciled |
| p53 R175H | TP53 | TP53 p.R175H | 0.95 | Reconciled |
| EGF-RX UnknownDel19 | None | No confident mapping | 0.31 | Cannot Reconcile |

Each output preserves original input strings, source row or record, canonical gene mapping, canonical variant mapping, confidence score, reconciliation status, evidence references, provenance metadata, review status, and audit traceability.

## 7. Reconciliation Statuses

The MVP will explicitly support three core statuses:

| Status | Meaning |
| --- | --- |
| `reconciled` | The system found a high-confidence canonical mapping. |
| `needs_review` | The system found a plausible mapping, but uncertainty or ambiguity requires human review. |
| `cannot_reconcile` | The system could not identify a trustworthy mapping and avoids forcing an answer. |

This uncertainty-aware design is a key differentiator. The system is intended to avoid hallucinated or overconfident mappings.

## 8. Human Governance

OncoReconcile AI is designed around human oversight.

The review workflow will allow expert users to inspect original source strings, view canonical candidate mappings, review confidence scores, inspect evidence and provenance, approve a reconciliation, reject a reconciliation, and request changes or additional review.

All review actions are intended to produce audit records containing reviewer identity, decision, timestamp, notes, original mapping, final status, confidence score, and supporting evidence.

## 9. Data Strategy

The project will prioritize small, high-quality demo cases rather than large, difficult-to-control datasets.

Initial data assets include:

- curated gene alias mappings
- curated canonical variant records
- variant synonym mappings
- evidence hint lookups
- synthetic NSCLC reports
- structured demo mutation examples

Planned public references include HGNC gene nomenclature data, ClinVar variant summary data, selected cBioPortal or TCGA LUAD mutation examples, and curated synthetic examples for controlled evaluation.

The current development repository includes a synthetic NSCLC starter benchmark package with gene aliases, variant synonym benchmarks, oncology variant master examples, evidence lookup hints, and synthetic report text examples. The MVP will use these as controlled evaluation and demo assets.

## 10. Technical Approach

The MVP uses a modular architecture:

```text
Frontend Demo UI
        ↓
FastAPI Backend
        ↓
Reconciliation Workflow
        ↓
Gene Normalization
        ↓
Variant Normalization
        ↓
Candidate Retrieval
        ↓
Reasoning & Confidence Scoring
        ↓
Review / Audit Workflow
        ↓
Reference Knowledge Base
```

Current and planned technologies:

| Area | Technology |
| --- | --- |
| Backend | Python, FastAPI |
| Frontend | Streamlit for rapid MVP demo; React optional for later polish |
| Data | CSV reference files, curated demo datasets |
| Testing | pytest |
| Containerization | Docker / Docker Compose |
| Future persistence | PostgreSQL |
| Future retrieval | semantic embeddings / vector search |
| Future AI reasoning | biomedical NLP or LLM-assisted explanations |

The MVP emphasizes reliability, explainability, and demo clarity over broad unsupported feature expansion.

## 11. Standards Alignment

OncoReconcile AI is conceptually aligned with emerging biomedical interoperability standards and practices, including HGNC gene normalization, HGVS-style variant representation, GA4GH Genomic Knowledge Standards concepts, VRS-inspired canonical modeling, FHIR Genomics interoperability concepts, and provenance-aware knowledge object design.

The project does not attempt to replace these standards. Instead, it demonstrates how AI-assisted workflows may help operationalize standards-aware reconciliation in real-world oncology data pipelines.

## 12. Target Users

Primary users:

- molecular pathology laboratories
- precision oncology programs
- variant curation teams
- clinical bioinformatics teams
- translational genomics groups
- molecular tumor boards

Future users:

- oncology analytics platforms
- pharmaceutical research organizations
- genomic testing vendors
- healthcare interoperability teams
- biomedical AI infrastructure platforms

## 13. Unique Value Proposition

OncoReconcile AI focuses on trustworthy semantic reconciliation and governed interoperability workflows rather than opaque fully automated AI outputs.

Key differentiators:

- AI-assisted but human-governed
- confidence-aware reconciliation
- support for unresolved ambiguity
- traceable evidence preservation
- audit-friendly workflow design
- standards-aware canonical modeling
- explainable reconciliation decisions
- original source preservation

Unlike generic LLM-based tools, OncoReconcile AI emphasizes provenance, uncertainty, reviewability, evidence, governance, and transparency.

## 14. Competition MVP Goals

During the competition, the team aims to deliver:

- a working oncology reconciliation workflow
- gene alias normalization
- curated variant synonym reconciliation
- confidence-aware candidate matching
- explicit reconciliation statuses
- human review workflow
- traceable canonical outputs
- an end-to-end demo using curated oncology examples
- documentation and demo materials suitable for judging

The MVP will demonstrate interoperability challenges in oncology genomic data, AI-assisted semantic reconciliation, confidence-aware decision support, provenance-aware governance, explainable reconciliation decisions, and uncertainty preservation.

## 15. Execution Plan

### Week 1: Project Planning & Dataset Preparation

Finalize MVP scope, define reconciliation workflow, assign team responsibilities, prepare curated demo examples, and organize GitHub issues and task board.

Deliverables: architecture draft, initial curated examples, starter dataset integration, team task board, and GitHub issue backlog.

### Week 2: Canonical Modeling & Data Processing

Define the canonical reconciliation object, improve gene and variant normalization, create the demo dataset, and define provenance fields.

Deliverables: canonical output schema, gene reconciliation workflow, variant synonym workflow, curated demo CSV, and schema tests.

### Week 3: Backend APIs & Reconciliation Pipeline

Build core backend APIs, add batch reconciliation, and support structured mutation-table input.

Deliverables: `POST /reconcile/batch`, structured reconciliation results, API tests, and demo-ready backend workflow.

### Week 4: Confidence, Status & Uncertainty Handling

Add reconciliation status classification, refine confidence scoring, support cannot-reconcile examples, and generate explainable outputs.

Deliverables: `reconciled`, `needs_review`, and `cannot_reconcile` logic; uncertainty explanations; confidence thresholds; and tests for all statuses.

### Week 5: Human Review Dashboard & Governance

Build an interactive review workflow, connect review decisions to audit records, and display evidence and provenance.

Deliverables: review queue, approve/reject/request-changes actions, audit log endpoint or display, and governance demo path.

### Week 6: Validation & Stabilization

Validate reconciliation outputs, improve demo reliability, test unresolved ambiguity workflows, and polish UI/UX.

Deliverables: stable MVP workflow, validation checklist, demo smoke tests, refined dataset, and refined explanations.

### Week 7: Presentation & Demo Preparation

Prepare the final presentation, create architecture diagrams, rehearse the demo, and produce screenshots and demo script.

Deliverables: pitch deck, architecture diagram, demo walkthrough, screenshots, and Q&A preparation.

### Week 8: Final Integration & Submission

Finalize the MVP, polish documentation, conduct full demo rehearsal, and submit final materials.

Deliverables: final working MVP, final GitHub repository, technical documentation, presentation deck, and demo script or video if required.

## 16. Team Workflow

The team will use GitHub issues to organize work. Tasks are grouped by priority, dependency, workstream, and acceptance criteria.

Team members can pick mixed tasks based on interests across backend/API, data/normalization, AI/retrieval, frontend/UI, governance/audit, testing/QA, documentation/demo, and business/pitch.

Each team member is encouraged to pick one primary coding task, one support or review task, and one documentation or demo task. The project lead will coordinate scope, architecture, integration, and final demo readiness. The PM/business lead will coordinate pitch narrative, user framing, and presentation materials.

## 17. Current Repository Status

The current repository already includes:

- FastAPI backend scaffold
- agent-style reconciliation workflow
- CSV-backed gene reconciliation
- CSV-backed variant synonym lookup
- confidence scoring module
- review queue prototype
- governance/audit modules
- Streamlit demo frontend
- curated reference data
- synthetic NSCLC starter dataset
- pytest test suite
- team task board
- GitHub issue backlog

Near-term implementation priorities:

- canonical output schema
- batch reconciliation endpoint
- curated demo CSV
- explicit status classification
- cannot-reconcile handling
- review/audit wiring
- upload/results UI
- API documentation and runbook

## 18. Future Vision

Beyond the competition MVP, OncoReconcile AI could expand toward broader variant type support, fusion and structural variant reconciliation, copy-number alteration reconciliation, richer HGVS normalization, FHIR Genomics export, deeper GA4GH/VRS alignment, persistent knowledge-base governance, cohort analytics integration, multi-institution review workflows, and enterprise interoperability APIs.

## 19. Ethical and Safety Framing

OncoReconcile AI is a research and educational prototype. It is not intended for clinical use and does not provide diagnosis, treatment recommendations, or patient-specific medical advice.

The project intentionally emphasizes human oversight, uncertainty preservation, auditability, evidence transparency, non-clinical demo use, and avoidance of unsupported automated claims.

## 20. Conclusion

OncoReconcile AI addresses a practical and important interoperability problem in precision oncology: inconsistent gene and variant representations across systems.

By combining deterministic normalization, semantic reconciliation, confidence scoring, explainable outputs, and human review, the project demonstrates how AI can assist biomedical interoperability workflows without removing expert governance.

The final competition MVP will show how messy oncology genomic inputs can be transformed into traceable, confidence-aware, standards-aligned canonical knowledge objects while preserving uncertainty, evidence, and auditability.
