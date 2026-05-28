# LLM Prompt Testing Guide for Gene/Variant Reconciliation

## 1. Ambiguous Example Values & Context

| Ambiguous Value                | Example Lab(s)                  | Example Context Fields                          |
|------------------------------- |---------------------------------|------------------------------------------------|
| EGFR mut+                      | Foundation, Caris, Tempus       | Cancer type: NSCLC; Sample: Tumor; Assay: NGS  |
| KRAS G12X                      | Foundation, Guardant            | Cancer type: Colorectal; Sample: Plasma        |
| BRAF positive                  | Caris, Tempus, NeoGenomics      | Cancer type: Melanoma; Sample: Tumor           |
| ALK rearrangement detected     | Foundation, Guardant            | Cancer type: NSCLC; Sample: Tumor              |
| TP53 abnormality               | Tempus, Caris, NeoGenomics      | Cancer type: Breast; Sample: Tumor             |
| Possible resistance mutation   | Tempus, Guardant                | Cancer type: NSCLC; Prior: EGFR TKI therapy    |
| HER2 low gain                  | Caris, NeoGenomics, Foundation  | Cancer type: Breast; Assay: NGS                |
| MET amplification              | Guardant, Foundation, Caris     | Cancer type: Gastric; Sample: Tumor            |
| EGFR Exl9deI (OCR error)       | Any (OCR from PDF)              | Cancer type: NSCLC; Sample: Tumor              |
| PIK3CA H1047R (panel code: ...) | Foundation, Caris               | Cancer type: Breast; Panel: Custom NGS         |

---

## 2. Recommended LLM Models

- GPT-4 (OpenAI, Azure)
- MedPaLM-2 (Google)
- BioGPT (Microsoft, open-source)
- ClinicalBERT, PubMedBERT (for NER/NLI tasks)

---

## 3. Example Prompt Template

```
You are a clinical genomics assistant. Given the following ambiguous gene/variant finding from a molecular lab report, normalize it to a canonical gene and variant name (HGNC/ClinVar/CIViC standard). Use the provided clinical context to improve accuracy.

Finding: "<ambiguous_value>"
Cancer type: <cancer_type>
Sample type: <sample_type>
Assay: <assay_type>
Prior findings/treatment: <prior_info>
Panel code (if any): <panel_code>

If the finding is an OCR error, correct it first. If the value is too vague, state that human review is needed.
Return:
- The normalized gene and variant
- Evidence (database, accession, or publication)
- Step-by-step explanation of your reasoning
- If uncertain, state that human review is required
```

**Example:**
```
Finding: "EGFR mut+"
Cancer type: NSCLC
Sample type: Tumor
Assay: NGS panel

[LLM should respond:]
Normalized: EGFR activating mutation (e.g., exon 19 deletion or L858R)
Evidence: ClinVar RCV000017576, CIViC Variant 6
Explanation: "EGFR mut+" in NSCLC usually refers to activating mutations such as exon 19 deletion or L858R, which are sensitive to EGFR inhibitors. This is supported by ClinVar and CIViC entries.
```

---

## 4. Additional Context to Provide

- Cancer type (NSCLC, breast, colorectal, etc.)
- Sample type (tumor, plasma, tissue, etc.)
- Assay type (NGS, FISH, PCR, panel name)
- Prior findings or treatments (e.g., prior EGFR mutation, TKI therapy)
- Panel/proprietary codes (if present)
- Any interpretation or summary text from the report

---

## 5. Output Format

Ask the LLM to return:
- Normalized gene name (HGNC)
- Normalized variant (HGVS or common name)
- Evidence (database name, accession, or publication)
- Step-by-step explanation
- Flag if human review is needed

---

## 6. Notes

- Always provide as much context as possible for best results.
- Require the LLM to provide both the normalized result and the evidence/reasoning behind it.
- If the LLM cannot confidently normalize, it should state that human review is required.
- Use real-world ambiguous values from lab reports for testing.

---

This guide ensures your LLM prompt testing is robust, explainable, and evidence-backed for clinical gene/variant reconciliation.
