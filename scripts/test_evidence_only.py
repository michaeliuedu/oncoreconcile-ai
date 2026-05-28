"""
Test script for direct evidence extraction (no VICC normalization).
Prints pretty JSON outputs for several demo cases.
"""
import json
import asyncio
from src.services.evidence_resolution_service import EvidenceResolutionService
from src.connectors.clinvar_client import ClinVarClient
from src.connectors.civic_client import CIVICClient

def pretty(d):
    print(json.dumps(d, indent=2, ensure_ascii=False))

examples = [
    ("p53", "gene"),
    ("BRAF V600E", "variant"),
    ("KRAS G12C", "variant"),
    ("EGFR Ex19del", "variant"),
    ("unknown alteration", "variant")
]

async def run_examples():
    print("\n--- Evidence-Only Test Script (No VICC) ---")
    evidence_resolution = EvidenceResolutionService()
    clinvar = ClinVarClient()
    civic = CIVICClient()
    for inp, typ in examples:
        print(f"\n=== {inp} ({typ}) ===")
        evidence = []
        if typ == "variant":
            # Try multiple query forms (simple synonym expansion)
            queries = [inp, inp.replace(" ", "_"), inp.replace(" ", "").upper()]
            evidence = await evidence_resolution.resolve_variant_evidence(queries)
        elif typ == "gene":
            # Try ClinVar gene evidence (mock)
            ev = await clinvar.get_evidence(inp)
            if ev:
                evidence.append(ev)
        pretty({
            "input": inp,
            "entity_type": typ,
            "evidence_sources": evidence
        })

if __name__ == "__main__":
    asyncio.run(run_examples())
