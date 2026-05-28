"""
Reconciliation wrapper for VICC normalization results.
Wraps VICC/cached results in canonical output schema with explainability, provenance, and audit trail.
"""


from src.connectors.vicc_client import normalize_gene, normalize_variation, normalize_disease
from src.connectors.vicc_config import DEBUG
from typing import Optional
import asyncio
from src.services.evidence.provider_router import EvidenceProviderRouter
from src.services.evidence_resolution_service import EvidenceResolutionService
import time

async def reconcile_with_vicc(original_input: str, entity_type: str, source_text: Optional[str] = None) -> dict:
    audit_trail = ["Original input preserved"]
    result = None
    evidence_router = EvidenceProviderRouter()
    evidence_resolution = EvidenceResolutionService()
    evidence = []
    explainability = ""
    confidence = "Low"
    requires_human_review = False
    cannot_reconcile = False
    status = None
    if entity_type == "gene":
        result = normalize_gene(original_input)
        audit_trail.append("VICC gene normalization attempted")
        canonical_gene = result.get("normalized")
        # Evidence retrieval
        gene_evidence = await evidence_router.get_gene_evidence(canonical_gene) if canonical_gene else None
        if result.get("match") and canonical_gene:
            if gene_evidence:
                evidence.append(gene_evidence)
                audit_trail.append("HGNC lookup attempted")
                confidence = gene_evidence.get("confidence_weight", "Medium")
                explainability = "Normalized using HGNC canonical gene mapping."
                status = "normalized_with_evidence"
            else:
                audit_trail.append("HGNC lookup attempted; no evidence found")
                # fallback: try multi-source evidence resolution for gene (future: OMIM, Ensembl, etc.)
                evidence.append({
                    "source": "Cached OncoReconcile Example",
                    "evidence_type": "curated_demo_mapping",
                    "retrieval_mode": "cached",
                    "confidence_weight": "Medium"
                })
                confidence = "Medium"
                requires_human_review = True
                cannot_reconcile = False
                status = "normalized_without_external_evidence"
                explainability = "Input was normalized using cached/demo mapping, but no authoritative external evidence source was found. Human review is recommended."
                audit_trail.append("Cached/demo normalization mapping found")
                audit_trail.append("External evidence lookup did not return authoritative evidence")
                audit_trail.append("Human review recommended")
                audit_trail.append("Cannot_reconcile set to false because canonical normalization was still possible")
        else:
            audit_trail.append("No canonical normalization found")
            audit_trail.append("No evidence source found")
            audit_trail.append("Marked as cannot reconcile")
            explainability = "No reliable normalization or evidence match was found. Human review is required."
            requires_human_review = True
            cannot_reconcile = True
            status = "unresolved"
    elif entity_type == "variant":
        result = normalize_variation(original_input)
        audit_trail.append("VICC variant normalization attempted")
        canonical_variant = result.get("normalized")
        canonical_gene = result.get("canonical_gene")
        # Evidence retrieval
        variant_evidence = await evidence_router.get_variant_evidence(canonical_variant) if canonical_variant else None
        evidence_found = False
        if result.get("match") and canonical_variant:
            if variant_evidence:
                evidence.append(variant_evidence)
                audit_trail.append("ClinVar lookup attempted")
                confidence = variant_evidence.get("confidence_weight", "Medium")
                explainability = "Normalized using ClinVar variant evidence."
                status = "normalized_with_evidence"
                evidence_found = True
            # If no evidence, try multi-source evidence resolution with synonym expansion
            if not evidence_found:
                audit_trail.append("ClinVar lookup attempted; no evidence found")
                # Synonym expansion for variant queries
                variant_queries = list({
                    canonical_variant,
                    original_input,
                    canonical_gene + " " + canonical_variant.split()[-1] if canonical_gene and canonical_variant else None,
                    canonical_variant.replace("p.", "") if canonical_variant and "p." in canonical_variant else None
                })
                variant_queries = [q for q in variant_queries if q]
                fallback_evidence = await evidence_resolution.resolve_variant_evidence(variant_queries)
                if fallback_evidence:
                    evidence.extend(fallback_evidence)
                    audit_trail.append("Multi-source evidence fallback succeeded (ClinVar/CIViC)")
                    confidence = fallback_evidence[0].get("confidence_weight", "Medium")
                    explainability = "Canonical normalization and authoritative external evidence resolution succeeded."
                    status = "normalized_with_evidence"
                    requires_human_review = False
                    cannot_reconcile = False
                else:
                    evidence.append({
                        "source": "Cached OncoReconcile Example",
                        "evidence_type": "curated_demo_mapping",
                        "retrieval_mode": "cached",
                        "confidence_weight": "Medium"
                    })
                    confidence = "Medium"
                    requires_human_review = True
                    cannot_reconcile = False
                    status = "normalized_without_external_evidence"
                    explainability = "Canonical normalization succeeded, but authoritative external evidence resolution was incomplete. Human review is recommended."
                    audit_trail.append("Cached/demo normalization mapping found")
                    audit_trail.append("External evidence lookup incomplete")
                    audit_trail.append("Human review recommended")
                    audit_trail.append("Cannot_reconcile set to false because canonical normalization was still possible")
        else:
            audit_trail.append("No canonical normalization found")
            audit_trail.append("No evidence source found")
            audit_trail.append("Marked as cannot reconcile")
            explainability = "No reliable normalization or evidence match was found. Human review is required."
            requires_human_review = True
            cannot_reconcile = True
            status = "unresolved"
    elif entity_type == "disease":
        result = normalize_disease(original_input)
        audit_trail.append("VICC disease normalization attempted")
        explainability = "Disease normalization attempted. Evidence not yet supported."
    else:
        audit_trail.append("Unknown entity_type; no normalization attempted")
        return {
            "original_input": original_input,
            "source_text": source_text or original_input,
            "entity_type": entity_type,
            "canonical_gene": None,
            "canonical_variant": None,
            "canonical_representation": None,
            "normalization_source": "VICC",
            "normalization_mode": "fallback",
            "confidence": "Low",
            "evidence_sources": [],
            "explainability": "Entity type not supported.",
            "requires_human_review": True,
            "cannot_reconcile": True,
            "audit_trail": audit_trail
        }
    normalization_mode = result.get("normalization_mode", "fallback")
    out = {
        "original_input": original_input,
        "source_text": source_text or original_input,
        "entity_type": entity_type,
        "canonical_gene": result.get("canonical_gene") if entity_type == "variant" else result.get("normalized") if entity_type == "gene" else None,
        "canonical_variant": result.get("normalized") if entity_type == "variant" else None,
        "canonical_representation": result.get("normalized"),
        "normalization_source": "VICC",
        "normalization_mode": normalization_mode,
        "confidence": confidence,
        "evidence_sources": evidence,
        "explainability": explainability,
        "requires_human_review": requires_human_review,
        "cannot_reconcile": cannot_reconcile,
        "status": status,
        "audit_trail": audit_trail
    }
    if DEBUG and result.get("debug"):
        out["debug"] = result["debug"]
    return out
