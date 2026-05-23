---

## 17. Explicit Example: Multi-Case ChatGPT Reconciliation Run

### Prompt Used

```
You are an expert in oncology variant normalization. For each input below, map the gene and variant to their canonical forms using current clinical and research standards. If the input is ambiguous, contains typos, or uses legacy names, provide your best mapping, explain your reasoning, and note your confidence. If multiple mappings are possible, list them and explain. If you cannot reconcile, state why.

Inputs:
1. "p53 mutation"
2. "EGFR uncommon exon 20 insertion"
3. "KRAS codon 12 glycine to cysteine"
4. "BRAF V600E-like mutation"
5. "EGFR ex19deltion"
6. "c-erbB-1"
7. "EGFR T790M and L858R double mutation"

For each, return:
- Canonical gene
- Canonical variant(s)
- Confidence (high/medium/low)
- Reasoning
```

### ChatGPT Output (Structured Table)

| Input                                    | Canonical gene | Canonical variant(s)                                                           | Confidence     | Reasoning                                                                                                                                            |
| ---------------------------------------- | -------------- | ------------------------------------------------------------------------------ | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **p53 mutation**                         | **TP53**       | Unspecified TP53 mutation                                                      | **Medium**     | “p53” is a common legacy/protein name associated with **TP53**. But “mutation” is nonspecific, so the exact variant cannot be normalized.            |
| **EGFR uncommon exon 20 insertion**      | **EGFR**       | EGFR exon 20 insertion, exact insertion unspecified                            | **Medium**     | Clearly points to EGFR exon 20 insertion class, but “uncommon” does not define the precise HGVS variant.                                             |
| **KRAS codon 12 glycine to cysteine**    | **KRAS**       | **KRAS p.G12C**                                                                | **High**       | Glycine-to-cysteine substitution at codon 12 maps directly to G12C. KRAS G12C is a known oncogenic variant. ([PMC][1])                               |
| **BRAF V600E-like mutation**             | **BRAF**       | Possible: **BRAF p.V600E**; broader possible group: BRAF V600-class alteration | **Low–Medium** | “V600E-like” is ambiguous. It may mean true V600E, or another V600 alteration such as V600K/D/R with similar signaling behavior. Should be reviewed. |
| **EGFR ex19deltion**                     | **EGFR**       | **EGFR exon 19 deletion**                                                      | **High**       | Likely typo for “ex19 deletion” / “Ex19del.” EGFR exon 19 deletions are common activating EGFR variants in lung cancer. ([PMC][2])                   |
| **c-erbB-1**                             | **EGFR**       | Gene alias only; no variant provided                                           | **High**       | c-erbB-1 / ERBB1 is a legacy name for EGFR. No variant string is present, so only gene normalization is possible.                                    |
| **EGFR T790M and L858R double mutation** | **EGFR**       | **EGFR p.T790M** and **EGFR p.L858R**                                          | **High**       | This contains two specific EGFR protein substitutions. L858R is a common activating EGFR mutation; T790M is a well-known EGFR resistance mutation.   |

### LLM Reasoning Steps & Evidence Logic

For each case, ChatGPT (GPT-4.1) performed:
- **Alias/ontology mapping:** Recognized gene aliases (e.g., p53 → TP53, c-erbB-1 → EGFR) using biomedical conventions.
- **HGVS-style variant interpretation:** Parsed free-text variant descriptions into standard forms (e.g., codon 12 glycine to cysteine → p.G12C).
- **Typo correction:** Detected and corrected likely typos (e.g., ex19deltion → exon 19 deletion).
- **Ambiguity detection:** Flagged vague or ambiguous terms (e.g., V600E-like) and did not force a canonical mapping.
- **Multi-variant parsing:** Split and mapped co-occurring variants (e.g., T790M and L858R).
- **Confidence estimation:** Assigned confidence based on specificity, ambiguity, and standardization certainty.
- **Evidence citation:** Provided literature or database references where relevant (see [PMC][1], [PMC][2]).

#### Model Used
- ChatGPT (GPT-4.1, May 2026)

#### What Was NOT Used
- No live database/API queries (HGNC, ClinVar, etc.)
- No production-grade normalization pipeline
- No vector/semantic retrieval
- No human review

#### Key Takeaway
This output demonstrates LLM-only reasoning, not a hybrid or production pipeline. For real-world use, combine LLM reasoning with deterministic rules, APIs, and human review as described in this guide.

[1]: https://pmc.ncbi.nlm.nih.gov/articles/PMC7041424/?utm_source=chatgpt.com "KRAS G12C Game of Thrones, which direct KRAS inhibitor ..."
[2]: https://pmc.ncbi.nlm.nih.gov/articles/PMC6764748/?utm_source=chatgpt.com "Diverse EGFR Exon 20 Insertions and Co-Occurring ... - PMC"
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
| "p53 mutation" (ambiguous, needs context)
| "EGFR uncommon exon 20 insertion" (not a standard synonym)
| "KRAS codon 12 glycine to cysteine" (free-text description)
| "BRAF V600E-like mutation" (non-standard, context-dependent)
| "EGFR ex19deltion" (typo)
| "c-erbB-1" (legacy name)
| "EGFR T790M and L858R double mutation" (multi-variant)

### Additional Demo Disease-Specific Examples

**NSCLC (Non-Small Cell Lung Cancer):**
- "EGFR exon 20 insertion, rare type" (ambiguous, not in standard mappings)
- "ALK fusion, EML4-ALK variant 3" (free-text, fusion variant, multiple possible breakpoints)
- "KRAS G12X" (ambiguous, X is a placeholder for any amino acid change)
- "ROS1 rearrangement" (non-specific, could refer to multiple fusion partners)
- "EGFR L858R/T790M" (multi-variant, co-occurring resistance and sensitizing mutations)
- "MET exon 14 skipping" (event, not a simple SNV or indel)

**Colorectal Cancer:**
- "BRAF non-V600E mutation" (ambiguous, needs context to specify)
- "KRAS codon 13 mutation" (free-text, could be G13D, G13C, etc.)
- "NRAS activating mutation" (non-specific, multiple possible codons)
- "APC truncating mutation" (event, not a specific variant)

**Melanoma:**
- "BRAF V600K/R" (ambiguous, could be V600K or V600R)
- "NRAS Q61 mutation" (free-text, could be Q61K, Q61R, Q61L, etc.)
- "KIT exon 11 mutation" (event, not a specific amino acid change)
- "CDKN2A loss" (copy number event, not a sequence variant)

---

## 13. Team Guidance

- When you encounter an unmapped input, first check if it can be handled by expanding the mapping files or adding a new rule.
- For ambiguous or novel cases, escalate to AI/LLM or human review.
- Document any new rules or mapping logic and update the mapping files as needed.
- Use the resources and workflow in this document for all reconciliation tasks.

---

*This guide should be kept up to date as the project evolves and new reconciliation strategies or resources become available.*

### Additional Demo Disease-Specific Examples

**NSCLC (Non-Small Cell Lung Cancer):**
- "EGFR exon 20 insertion, rare type" (ambiguous, not in standard mappings)
- "ALK fusion, EML4-ALK variant 3" (free-text, fusion variant, multiple possible breakpoints)
- "KRAS G12X" (ambiguous, X is a placeholder for any amino acid change)
- "ROS1 rearrangement" (non-specific, could refer to multiple fusion partners)
- "EGFR L858R/T790M" (multi-variant, co-occurring resistance and sensitizing mutations)
- "MET exon 14 skipping" (event, not a simple SNV or indel)

**Colorectal Cancer:**
- "BRAF non-V600E mutation" (ambiguous, needs context to specify)
- "KRAS codon 13 mutation" (free-text, could be G13D, G13C, etc.)
- "NRAS activating mutation" (non-specific, multiple possible codons)
- "APC truncating mutation" (event, not a specific variant)

**Melanoma:**
- "BRAF V600K/R" (ambiguous, could be V600K or V600R)
- "NRAS Q61 mutation" (free-text, could be Q61K, Q61R, Q61L, etc.)
- "KIT exon 11 mutation" (event, not a specific amino acid change)
- "CDKN2A loss" (copy number event, not a sequence variant)

---

## 13. Team Guidance
- When you encounter an unmapped input, first check if it can be handled by expanding the mapping files or adding a new rule.
- For ambiguous or novel cases, escalate to AI/LLM or human review.
- Document any new rules or mapping logic and update the mapping files as needed.
- Use the resources and workflow in this document for all reconciliation tasks.

---

*This guide should be kept up to date as the project evolves and new reconciliation strategies or resources become available.*
