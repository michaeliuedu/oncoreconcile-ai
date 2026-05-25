# OncoReconcile AI

## Human-Governed AI Platform for Oncology Gene & Variant Semantic Reconciliation

---

# 1. Project Overview

## Project Title

**OncoReconcile AI**
AI-Assisted Oncology Gene & Variant Reconciliation Platform

## Vision

OncoReconcile AI is a human-governed AI interoperability platform designed to reconcile heterogeneous oncology gene and variant representations into standards-aligned, evidence-linked, traceable canonical knowledge objects.

The project explores how AI-assisted semantic interoperability workflows can help improve precision oncology data integration while preserving:

* provenance
* explainability
* uncertainty
* auditability
* human oversight
* standards-aware normalization

Rather than building another generic healthcare chatbot, the platform focuses on trustworthy interoperability infrastructure for future precision oncology ecosystems.

---

# 2. Problem Statement

Precision oncology workflows increasingly depend on genomic data originating from:

* molecular diagnostics laboratories
* sequencing vendors
* molecular pathology reports
* VCF pipelines
* EHR systems
* oncology analytics platforms
* translational research environments

However, the same biological concepts are frequently represented in inconsistent ways across systems.

## Example Gene Representations

| Original | Canonical |
| -------- | --------- |
| HER1     | EGFR      |
| ERBB1    | EGFR      |
| p53      | TP53      |
| C-MET    | MET       |

## Example Variant Representations

| Original Variant | Canonical Interpretation |
| ---------------- | ------------------------ |
| EGFR Ex19del     | EGFR exon 19 deletion    |
| E746_A750del     | EGFR exon 19 deletion    |
| c.2235_2249del   | EGFR exon 19 deletion    |
| p.E746_A750del   | EGFR exon 19 deletion    |

These inconsistencies create major downstream challenges for:

* semantic interoperability
* cohort generation
* oncology analytics
* AI-assisted workflows
* translational research
* molecular tumor boards
* biomedical knowledge governance

Today, much of this reconciliation work remains:

* manual
* fragmented
* difficult to audit
* difficult to scale
* highly dependent on expert review

Existing workflows often fail to preserve:

* provenance
* transcript/build context
* evidence references
* uncertainty
* review history
* auditability

As precision oncology and healthcare AI continue expanding, trustworthy semantic interoperability becomes increasingly important.

---

# 3. Proposed Solution

OncoReconcile AI combines:

* deterministic normalization
* biomedical semantic retrieval
* AI-assisted reasoning
* confidence scoring
* human-in-the-loop governance
* provenance-aware audit tracking
* governed canonical knowledge management

to support explainable oncology semantic reconciliation workflows.

The system is designed to:

* normalize heterogeneous oncology representations
* identify semantically equivalent variants
* preserve original source evidence
* generate explainable confidence scores
* support expert review workflows
* maintain governed canonical knowledge objects
* continuously improve through human feedback

The platform emphasizes:

* explainability
* provenance preservation
* standards-aware normalization
* uncertainty handling
* governance workflows
* human oversight

The platform does **NOT** provide:

* diagnosis
* treatment recommendations
* autonomous clinical decision making

---

# 4. Core Design Principles

Key architectural principles include:

* preserve original source evidence
* separate extraction from interpretation
* preserve uncertainty instead of forcing mappings
* support “cannot reconcile” outcomes
* maintain auditability and provenance
* align with emerging interoperability standards
* support human-governed workflows

---

# 5. High-Level Architecture

```text id="y0cnrf"
Data Sources
(HGNC / ClinVar / TCGA / cBioPortal / CSV / VCF / Reports)
        ↓
Extraction Layer
        ↓
Normalization Layer
(HGNC + HGVS)
        ↓
Semantic Retrieval Layer
(keyword + embeddings + vector search)
        ↓
AI-Assisted Reasoning
        ↓
Confidence Scoring
        ↓
Human Review Workflow
        ↓
Governed Canonical Knowledge Base
        ↓
Analytics & Feedback Loop
```

---

# 6. End-to-End Workflow

## Step 1 — Upload

Input sources may include:

* CSV mutation tables
* VCF files
* selected molecular reports
* curated oncology examples

## Step 2 — Extraction

Extract:

* genes
* variants
* transcript context
* supporting metadata

## Step 3 — Deterministic Normalization

Perform:

* HGNC gene normalization
* HGVS-style cleanup
* formatting standardization
* ontology alignment

## Step 4 — Semantic Retrieval

Retrieve candidate mappings using:

* rule-based matching
* synonym lookup
* vector similarity
* biomedical embeddings

Potential models:

* SapBERT
* BioBERT
* PubMedBERT

## Step 5 — AI-Assisted Reasoning

Frontier LLMs evaluate:

* semantic equivalence
* ambiguity
* confidence
* mapping rationale

Potential experimentation:

* OpenAI GPT models
* Anthropic Claude
* Google Gemini

## Step 6 — Confidence Scoring

Confidence combines:

* deterministic evidence
* semantic similarity
* ontology support
* reasoning quality
* historical approvals

## Step 7 — Human Review Workflow

Human reviewers may:

* approve
* reject
* edit
* mark unresolved
* inspect evidence
* review provenance

## Step 8 — Governed Canonical Knowledge Base

Approved mappings become governed canonical objects containing:

* canonical representations
* evidence references
* provenance metadata
* confidence history
* review history
* audit trails

## Step 9 — Feedback Loop

Human review decisions continuously improve:

* mapping quality
* retrieval quality
* confidence thresholds
* canonical knowledge base

---

# 7. Core MVP Scope

The MVP intentionally focuses on:

## Supported Data Types

* gene aliases
* SNVs
* small indels
* HGVS-style variants
* small curated VCF-like inputs

## Initial Cancer Focus

* Lung Adenocarcinoma (LUAD)

## Initial Genes

* EGFR
* KRAS
* BRAF
* TP53

## Initial Public Sources

* HGNC
* ClinVar
* TCGA LUAD subsets
* cBioPortal

The MVP prioritizes:

* workflow intelligence
* explainability
* auditability
* governance
* manageable scope
* demo reliability

over large-scale production deployment.

---

# 8. Example Workflow

## Input

| Original Gene | Original Variant |
| ------------- | ---------------- |
| HER1          | Ex19del          |
| ERBB1         | E746_A750del     |
| p53           | R175H            |
| EGF-RX        | UnknownDel19     |

---

## Reconciliation Output

| Canonical Gene | Canonical Variant     | Confidence | Status           |
| -------------- | --------------------- | ---------- | ---------------- |
| EGFR           | EGFR exon 19 deletion | 0.97       | Reconciled       |
| EGFR           | EGFR exon 19 deletion | 0.98       | Reconciled       |
| TP53           | TP53 p.R175H          | 0.95       | Reconciled       |
| -              | -                     | 0.32       | Cannot Reconcile |

---

## Each Output Preserves

* original source strings
* source file/row
* canonical mappings
* transcript/build context
* provenance metadata
* evidence references
* confidence information
* review history
* audit traceability

---

# 9. Human Review Workflow

Human governance is a core architectural principle.

## High Confidence

Mappings above configurable thresholds may be:

* auto-suggested
* optionally sampled for review

## Medium Confidence

Mappings requiring verification enter review queues.

## Low Confidence

Ambiguous mappings may be:

* rejected
* marked unresolved
* escalated for expert review

## Reviewer Interface Displays

* original input
* candidate mapping
* confidence score
* explanation
* provenance
* evidence references
* prior review history

---

# 10. Knowledge Base Vision (“OncoBrain” Layer)

The platform includes a governed oncology semantic knowledge layer storing:

* canonical variants
* synonym relationships
* evidence references
* semantic mappings
* provenance
* review history
* ontology relationships

Future architecture may evolve toward:

* GraphRAG workflows
* semantic entity graphs
* AI memory systems
* ontology-aware retrieval
* FHIR Genomics interoperability

Example relationship model:

```text id="k0uk8g"
EGFR
   ↓ has_variant
Exon19Deletion
   ↓ supported_by
ClinVar
   ↓ associated_with
LUAD
```

---

# 11. Technical Architecture

## Backend

* Python
* FastAPI
* PostgreSQL
* pgvector
* DuckDB (optional experimentation)

## Frontend

* React
* Tailwind
* lightweight dashboard workflows

## AI / Semantic Retrieval

* SapBERT
* BioBERT
* PubMedBERT
* embeddings + vector retrieval

## AI Reasoning

Potential experimentation with:

* OpenAI GPT
* Anthropic Claude
* Google Gemini

## Orchestration

Potential future experimentation:

* LangGraph
* LangChain
* agent workflows

---

# 12. Recommended Repository Structure

```text id="k3j0yy"
oncoreconcile-ai/
├── frontend/
├── backend/
├── ai-engine/
├── data/
├── docs/
├── presentation/
├── tests/
├── scripts/
├── docker/
└── README.md
```

---

# 13. Target Audience

Primary users may include:

* molecular pathology laboratories
* oncology practices
* precision medicine teams
* translational genomics groups
* healthcare analytics organizations
* pharmaceutical and biotech companies
* clinical informatics teams
* biomedical interoperability teams

---

# 14. Unique Value Proposition (UVP)

Unlike generic LLM systems or traditional rule-based pipelines, OncoReconcile AI emphasizes:

* explainable AI reconciliation
* confidence-aware workflows
* provenance preservation
* standards-aware normalization
* uncertainty handling
* human-governed review
* governed canonical knowledge objects

The project focuses on trustworthy semantic interoperability infrastructure for precision oncology ecosystems.

---

# 15. Standards Alignment

The project is conceptually aligned with:

* HGNC gene normalization
* HGVS variant representation
* GA4GH Genomic Knowledge Standards (GKS)
* VRS-inspired canonical modeling
* FHIR Genomics interoperability

The platform does not attempt to replace these standards systems.

Instead, it explores how AI-assisted interoperability workflows may help operationalize them in real-world oncology environments.

---

# 16. Competition MVP Goals

The MVP aims to demonstrate:

* oncology interoperability challenges
* semantic reconciliation workflows
* explainable AI-assisted matching
* confidence-aware governance
* provenance-aware canonical outputs
* support for unresolved ambiguity
* human review workflows
* governed semantic interoperability

---

# 17. Expected Impact

The project explores how AI-assisted semantic governance workflows may help:

* reduce manual reconciliation effort
* improve oncology interoperability
* improve biomedical data quality
* accelerate cohort generation
* support more trustworthy healthcare AI systems
* enable more explainable biomedical AI pipelines

---

# 18. Important Disclaimer

This project is:

* research-oriented
* educational
* exploratory

It is NOT:

* a clinical diagnostic system
* medical advice software
* autonomous treatment recommendation software

Human oversight and governance are central to the project philosophy.

---

# 19. Team Overview

## Xiang Li (Justin) Zhang

### Team Lead / Biomedical Interoperability Lead

Senior Data Engineer and Bioinformatics Engineer with 15+ years of experience in healthcare, genomics, and AI-enabled data platforms.

Background includes:

* oncology data integration
* healthcare interoperability
* bioinformatics
* cloud-native biomedical data platforms
* AI-assisted healthcare workflows

Experience includes:

* McKesson / Ontada
* Los Alamos National Laboratory
* UT Southwestern Medical Center
* Daiichi Sankyo

Technical expertise includes:

* Python
* SQL
* Databricks
* healthcare interoperability (FHIR/OMOP)
* oncology analytics
* genomic data integration
* biomedical semantic workflows

Role in project:

* technical architecture
* interoperability design
* canonical modeling
* reconciliation workflows
* standards alignment
* AI interoperability strategy

---

## Michael Liu

### Frontend Engineer / Full Stack Contributor

Computer Science student at Carnegie Mellon University.

Focus areas include:

* React
* frontend engineering
* modern web frameworks
* full-stack application development
* workflow visualization

Role in project:

* frontend dashboard development
* reconciliation workflow UI
* review interfaces
* upload workflows
* user experience design

---

## Rin Hayashi

### Full Stack / AI Engineering Contributor

Computer Science student at The University of Texas at Austin.

Focus areas include:

* backend engineering
* bioinformatics workflows
* AI integration
* frontend/backend integration
* biomedical data processing

Role in project:

* backend API development
* AI workflow integration
* genomic data processing
* semantic retrieval workflows
* infrastructure integration

---

## Hao Zhang

### Quantitative Engineering / Backend Contributor

Quantitative developer with strong experience in:

* Python
* Linux
* quantitative and analytical programming workflows

Has been experimenting with LLM-driven development workflows since late 2022.

Focus areas include:

* backend engineering
* automation
* AI-assisted development workflows
* infrastructure and systems engineering
* developer productivity tooling

Role in project:

* backend workflow support
* automation pipelines
* AI-assisted engineering workflows
* infrastructure optimization
* Linux/Python engineering support

---

## Anne Zhang

### Data Analytics / Data Engineering Contributor

Computer Science student at the University of Waterloo.

Completed second year Computer Science studies and currently working as a Data Analyst intern with the York Region government in Toronto.

Focus areas include:

* data analytics
* data processing
* workflow organization
* data validation
* analytical reporting

Role in project:

* dataset preparation
* reconciliation evaluation
* analytics and validation workflows
* benchmark dataset generation
* workflow testing and reporting

---

## Yuka Hayashi

### Product Strategy / Business Contributor

Professional background includes:

* MBA
* accounting
* IT management
* consulting experience in Japan
* marketing experience in the United States

Focus areas include:

* product positioning
* presentation strategy
* commercialization perspectives
* workflow storytelling
* business communications

Role in project:

* product strategy
* competition presentation
* business positioning
* workflow storytelling
* commercialization exploration

---

## Team Strength Summary

The team combines expertise in:

* healthcare interoperability
* oncology data engineering
* bioinformatics
* AI-assisted workflows
* semantic retrieval
* frontend/full-stack engineering
* quantitative development
* data analytics
* workflow governance
* product strategy

The project team includes professionals and students with backgrounds connected to:

* McKesson / Ontada
* Los Alamos National Laboratory
* UT Southwestern Medical Center
* Carnegie Mellon University
* University of Texas at Austin
* University of Waterloo
* York Region Government

This multidisciplinary structure supports both:

* practical MVP implementation
* long-term AI interoperability vision development

---

# 20. Execution Plan

## Week 1 — Planning & Dataset Preparation

* finalize MVP scope
* define canonical object schema
* collect public datasets
* create curated mutation examples
* setup repository and environments

## Week 2 — Normalization & Canonical Modeling

* implement HGNC normalization
* implement HGVS cleanup
* build parsers
* define provenance structure

## Week 3 — Backend APIs & Workflow

* implement FastAPI services
* upload workflows
* reconciliation pipeline
* status classification logic

## Week 4 — AI Semantic Reconciliation

* semantic retrieval
* embeddings
* confidence scoring
* explainable reasoning

## Week 5 — Human Review Dashboard

* React dashboard
* upload interface
* review workflows
* evidence display

## Week 6 — Integration & Validation

* integration testing
* workflow stabilization
* explainability improvements
* ambiguity handling

## Week 7 — Presentation & Demo Preparation

* architecture diagrams
* workflow slides
* demo scripts
* benchmark examples

## Week 8 — Final MVP & Submission

* final integration
* debugging
* documentation
* demo rehearsals
* submission

---

# 21. Vision Statement

OncoReconcile AI explores how human-governed AI workflows may enable more trustworthy semantic interoperability and governed oncology knowledge reconciliation for the future of precision oncology AI ecosystems.
