"""LLM Prompts - Templates for LLM reasoning

Provides structured prompts for:
- Clinical significance analysis
- Treatment recommendation synthesis
- Evidence summarization
"""


def get_clinical_analysis_prompt(
    canonical_variant_id: str,
    clinical_significance: str,
    evidence_count: int,
    treatment_relevance: str,
) -> str:
    """Generate prompt for clinical analysis"""
    
    return f"""
You are a genomics expert assistant analyzing oncology variants.

VARIANT INFORMATION:
- Canonical ID: {canonical_variant_id}
- Clinical Significance: {clinical_significance}
- Supporting Evidence: {evidence_count} sources
- Treatment Relevance: {treatment_relevance}

TASK:
1. Assess the clinical validity of this variant
2. Summarize key clinical context (1-2 sentences)
3. Identify treatment implications if applicable
4. Rate your confidence in the assessment (0-1 scale)

CONSTRAINTS:
- This is for research purposes, not clinical decision-making
- Provide a summary, not medical recommendations
- Reference evidence strength when available

RESPONSE FORMAT:
Clinical Summary: [1-2 sentences]
Treatment Implications: [if applicable, else "Not applicable"]
Confidence Score: [0.0-1.0]
"""


def get_evidence_summary_prompt(
    variant_id: str,
    evidence_links: list,
) -> str:
    """Generate prompt for evidence summarization"""
    
    evidence_text = "\n".join([f"- {e.get('source', 'Unknown')}: {e.get('title', '')}" for e in evidence_links])
    
    return f"""
Summarize the clinical evidence for this variant.

VARIANT: {variant_id}

EVIDENCE SOURCES:
{evidence_text}

TASK:
Provide a brief summary (2-3 sentences) of the evidence base and clinical importance.
"""


def get_confidence_assessment_prompt(
    variant_id: str,
    deterministic_score: float,
    semantic_score: float,
    evidence_count: int,
) -> str:
    """Generate prompt for confidence assessment"""
    
    return f"""
Assess the confidence in this variant reconciliation.

VARIANT: {variant_id}

SCORING FACTORS:
- Rule-based match score: {deterministic_score:.2f} (0-1)
- Semantic similarity: {semantic_score:.2f} (0-1)
- Evidence strength: {evidence_count} sources found

TASK:
1. Consider all factors above
2. Provide an overall confidence assessment (0-1 scale)
3. Explain key confidence drivers

RESPONSE:
Confidence: [0.0-1.0]
Reasoning: [1-2 sentences]
"""
