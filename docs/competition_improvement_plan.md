# Competition-Focused Improvement Plan: Segmented Action Items

This document outlines actionable improvements for the competition, segmented by workflow component. Each team segment can use this as a checklist for targeted enhancements.

---

## 1. Extraction & Normalization Segment
- **Expand and Refine Mapping Files**
  - Add more gene and variant synonyms from public databases (HGNC, ClinVar, CIViC).
  - Include common typos, alternate notations, and legacy names.
  - Use regex patterns for more flexible variant normalization.
- **Improve Rule-Based Normalization**
  - Enhance logic to handle more edge cases (whitespace, punctuation, case, misspellings).
  - Add robust matching for multi-variant and ambiguous cases.

## 2. Retrieval Segment
- **Automate Public API Lookups**
  - Integrate live queries to HGNC, ClinVar, or CIViC for unmapped genes/variants.
  - Cache results to speed up repeated lookups.
- **Prepare for Future Graph/AI Integration**
  - Structure data and code to use canonical IDs and modularize retrieval logic.

## 3. Reasoning & Confidence Segment
- **Confidence Scoring and Explainability**
  - Make confidence scoring more transparent (show which rules, mappings, or evidence contributed).
  - Provide clear explanations for each reconciliation decision.

## 4. Review & Human-in-the-Loop Segment
- **Human-in-the-Loop Review**
  - Add a simple review queue for ambiguous or low-confidence cases.
  - Log decisions and rationale for future improvements.

## 5. Documentation & Usability Segment
- **Documentation and Usability**
  - Ensure all workflow steps, rules, and mappings are well documented.
  - Provide clear onboarding and usage instructions for the team and judges.

---

## Summary Table
| Segment                      | Key Improvements                                                                 |
|------------------------------|---------------------------------------------------------------------------------|
| Extraction & Normalization   | Expand mappings, regex, normalization logic                                      |
| Retrieval                    | API lookups, caching, modularization                                            |
| Reasoning & Confidence       | Transparent scoring, explainability                                             |
| Review & Human-in-the-Loop   | Review queue, decision logging                                                  |
| Documentation & Usability    | Clear docs, onboarding, usage instructions                                      |

---

*Use this document as a living checklist. Assign owners for each segment and track progress as you prepare for the competition.*
