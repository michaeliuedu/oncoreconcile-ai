"""
Test script for VICC Normalizer integration in OncoReconcile AI.
Prints pretty JSON outputs for several demo cases.
"""

import json
import asyncio
from src.services.reconciliation_service import reconcile_with_vicc
from src.connectors.vicc_config import USE_CACHE

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
    print("\n--- VICC Test Script ---")
    print(f"USE_CACHE = {USE_CACHE}")
    for inp, typ in examples:
        print(f"\n=== {inp} ({typ}) ===")
        out = await reconcile_with_vicc(inp, typ)
        print(f"Normalization mode: {out.get('normalization_mode')}")
        pretty(out)

if __name__ == "__main__":
    asyncio.run(run_examples())
