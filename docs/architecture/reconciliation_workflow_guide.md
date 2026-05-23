# OncoReconcile AI: Gene & Variant Reconciliation Workflow Guide

## Overview
This document provides a comprehensive, step-by-step guide for team members on how to perform gene and variant reconciliation using deterministic rules, public APIs, human review, and AI agents. It includes practical examples, resources, and best practices for each stage of the workflow.

---

## 1. Input Example
- **Input gene:** HER1
- **Input variant:** Ex19del

---

## 2. Deterministic Rules/Mapping

### a. Gene Normalization
- Check `gene_aliases.csv` for the input gene (e.g., HER1 → EGFR).
- If found, map to the canonical gene (EGFR).

### b. Variant Normalization
- Check `variant_synonyms.csv` for the input variant under the canonical gene (e.g., Ex19del under EGFR → EGFR exon 19 deletion).
- If found, map to the canonical variant.

**Result:**
- Canonical gene: EGFR
- Canonical variant: EGFR exon 19 deletion
- **Status:** reconciled (rules/mapping)

---

## 3. If Not Found by Rules/Mapping

### a. Try Normalization Logic
- Apply case normalization, whitespace/punctuation cleanup, typo correction (e.g., TP-53 → TP53).
- If still not found, proceed to public API lookup.

---

## 4. Query Public Databases/APIs

### a. Gene Aliases/Symbols
- **HGNC REST API:**
  - Docs: https://www.genenames.org/help/rest-web-service-help/
  - Fetch by symbol: https://rest.genenames.org/fetch/symbol/EGFR
  - Fetch by alias: https://rest.genenames.org/fetch/alias_symbol/HER1
- **NCBI Entrez Gene:**
  - Docs: https://www.ncbi.nlm.nih.gov/books/NBK25501/
  - Example: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gene&term=HER1[All%20Fields]

### b. Variant Synonyms/Descriptions
- **ClinVar:**
  - Docs: https://www.ncbi.nlm.nih.gov/clinvar/docs/api_http/
  - Example: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term=Ex19del
- **CIViC:**
  - Docs: https://civic.readthedocs.io/en/latest/api.html
  - Example: https://civicdb.org/api/variants?name=V600E
- **COSMIC:**
  - Docs: https://cancer.sanger.ac.uk/cosmic/help/api
  - Example: https://cancer.sanger.ac.uk/cosmic/search?q=EGFR%20exon%2019%20deletion

### c. Example Python (HGNC)
```python
import requests

def query_hgnc_alias(symbol):
    url = f'https://rest.genenames.org/fetch/alias_symbol/{symbol}'
    headers = {'Accept': 'application/json'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data['response']['numFound'] > 0:
            return data['response']['docs'][0]['symbol']  # Canonical symbol
    return None
```

**Result:**
- If found, map and mark as reconciled (external reference).

---

## 5. If Still Not Found—Human Review

### a. Manual Search
- Use authoritative databases:
  - HGNC: https://www.genenames.org/
  - NCBI Gene: https://www.ncbi.nlm.nih.gov/gene/
  - UniProt: https://www.uniprot.org/
  - ClinVar: https://www.ncbi.nlm.nih.gov/clinvar/
  - CIViC: https://civicdb.org/
  - COSMIC: https://cancer.sanger.ac.uk/cosmic
  - OncoKB: https://www.oncokb.org/
- Use literature search:
  - PubMed: https://pubmed.ncbi.nlm.nih.gov/
  - Google Scholar: https://scholar.google.com/

### b. Contextual Interpretation
- Use clinical or report context to infer the most likely mapping.
- Consult with domain experts or tumor boards if needed.

### c. Documentation
- Record the rationale, evidence, and references for the reconciliation decision.

**Result:**
- Human reconciles if possible, documents rationale.
- If not possible, status: cannot_reconcile.

---

## 6. AI Model/Agent Reconciliation

### a. When to Use AI
- For ambiguous, free-text, misspelled, legacy, or context-dependent cases not handled by rules, APIs, or human search.

### b. Example AI Prompt
```
You are an expert in oncology variant normalization.
Input gene: c-erbB-1
Input variant: EGFR uncommon exon 20 insertion
Known gene aliases: c-erbB-1, EGFR, HER1
Known variant synonyms for EGFR: Ex19del, E746_A750del, c.2235_2249del, exon 20 insertion
Task: Map the input to a canonical gene and variant. If ambiguous, explain why.
```

### c. AI Model Output
- Maps “c-erbB-1” to “EGFR” using knowledge.
- Suggests “EGFR exon 20 insertion” as the closest canonical variant, with a note on ambiguity.
- Provides confidence score and rationale.

**Result:**
- AI provides a best-effort mapping for human review.

---

## 7. Can AI Reduce Human Work?
- Yes. AI can automate mapping for ambiguous, misspelled, or context-dependent cases, reducing the number of cases requiring full manual review.
- AI can suggest mappings, provide confidence scores, and explanations to help humans make faster decisions.
- AI can surface likely candidates for human approval, speeding up the review process.

---

## 8. Are There Cases Only AI Can Help?
- Yes. Examples include:
  - Complex free-text/narrative variant descriptions (e.g., “KRAS codon 12 glycine to cysteine” → “KRAS G12C”).
  - Legacy or rare synonyms not in any mapping or public database.
  - Multi-variant or context-dependent cases where rules and even human search are slow or infeasible.
  - Cases where AI can synthesize information from multiple sources or infer intent from context.

---

## 9. Example Summary Table
| Step                | Who/What Handles | Example Value                | Outcome                |
|---------------------|------------------|-----------------------------|------------------------|
| Rules/Mapping       | Code             | HER1 → EGFR, Ex19del → ...  | Reconciled             |
| Public API Lookup   | Code             | TP-53 → TP53 (HGNC API)     | Reconciled             |
| Human Review        | Human            | c-erbB-1, ambiguous variant | Manual reconciliation  |
| AI Agent            | AI Model         | Free-text, legacy, complex  | AI-assisted mapping    |

---

## 10. Best Practices
- Always try deterministic rules/mapping first.
- Use public APIs for live lookups if local mapping fails.
- Escalate to human review for ambiguous or novel cases.
- Use AI agents for the hardest cases, especially free-text, legacy, or context-dependent inputs.
- Document all reconciliation decisions and update mapping files as new cases are resolved.

---

## 11. Resources
- HGNC REST API: https://www.genenames.org/help/rest-web-service-help/
- NCBI Entrez Gene: https://www.ncbi.nlm.nih.gov/books/NBK25501/
- ClinVar API: https://www.ncbi.nlm.nih.gov/clinvar/docs/api_http/
- CIViC API: https://civic.readthedocs.io/en/latest/api.html
- COSMIC API: https://cancer.sanger.ac.uk/cosmic/help/api
- PubMed: https://pubmed.ncbi.nlm.nih.gov/
- Google Scholar: https://scholar.google.com/

---

## 12. Example Real-World Cases Where AI Helps
- "p53 mutation" (ambiguous, needs context)
- "EGFR uncommon exon 20 insertion" (not a standard synonym)
- "KRAS codon 12 glycine to cysteine" (free-text description)
- "BRAF V600E-like mutation" (non-standard, context-dependent)
- "EGFR ex19deltion" (typo)
- "c-erbB-1" (legacy name)
- "EGFR T790M and L858R double mutation" (multi-variant)

---

## 13. Team Guidance
- When you encounter an unmapped input, first check if it can be handled by expanding the mapping files or adding a new rule.
- For ambiguous or novel cases, escalate to AI/LLM or human review.
- Document any new rules or mapping logic and update the mapping files as needed.
- Use the resources and workflow in this document for all reconciliation tasks.

---

*This guide should be kept up to date as the project evolves and new reconciliation strategies or resources become available.*
