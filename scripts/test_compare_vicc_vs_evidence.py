"""
Unified comparison script: VICC-based normalization+evidence vs. direct evidence-only.
Prints side-by-side results for each input.
"""
import json
import asyncio
from src.services.reconciliation_service import reconcile_with_vicc
from src.services.evidence_resolution_service import EvidenceResolutionService
from src.connectors.clinvar_client import ClinVarClient
from src.connectors.civic_client import CIVICClient

def pretty(d):
    return json.dumps(d, indent=2, ensure_ascii=False)

examples = [
    ("p53", "gene"),
    ("BRAF V600E", "variant"),
    ("KRAS G12C", "variant"),
    ("EGFR Ex19del", "variant"),
    ("unknown alteration", "variant")
]

async def run_examples():
    print("\n--- VICC vs. Evidence-Only Comparison ---")
    evidence_resolution = EvidenceResolutionService()
    clinvar = ClinVarClient()
    civic = CIVICClient()
    for inp, typ in examples:
        print(f"\n=== {inp} ({typ}) ===")
        # VICC-based
        vicc_result = await reconcile_with_vicc(inp, typ)
        # Evidence-only
        evidence = []
        if typ == "variant":
            queries = [inp, inp.replace(" ", "_"), inp.replace(" ", "").upper()]
            evidence = await evidence_resolution.resolve_variant_evidence(queries)
        elif typ == "gene":
            ev = await clinvar.get_evidence(inp)
            if ev:
                evidence.append(ev)
        # Print side-by-side
        print("[VICC-based normalization + evidence]")
        print(pretty({
            "canonical": vicc_result.get("canonical_representation"),
            "evidence_sources": vicc_result.get("evidence_sources"),
            "confidence": vicc_result.get("confidence"),
            "explainability": vicc_result.get("explainability"),
            "status": vicc_result.get("status")
        }))
        print("[Direct evidence-only]")
        print(pretty({
            "input": inp,
            "evidence_sources": evidence
        }))

if __name__ == "__main__":
    asyncio.run(run_examples())
