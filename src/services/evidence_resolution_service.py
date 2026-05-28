"""
Evidence orchestration service for OncoReconcile AI.
Attempts multi-source evidence resolution for normalized entities.
"""
from typing import List, Dict, Optional
from src.connectors.clinvar_client import ClinVarClient
from src.connectors.civic_client import CIVICClient

class EvidenceResolutionService:
    def __init__(self):
        self.clinvar = ClinVarClient()
        self.civic = CIVICClient()

    async def resolve_variant_evidence(self, queries: List[str]) -> List[Dict]:
        evidence = []
        # Try ClinVar
        for q in queries:
            clinvar_evidence = await self.clinvar.get_evidence(q)
            if clinvar_evidence:
                evidence.append(clinvar_evidence)
                break
        # Try CIViC if ClinVar not found
        if not evidence:
            for q in queries:
                civic_evidence = self.civic.get_evidence(q)
                if civic_evidence:
                    # CIVICClient.get_evidence returns a list; add all
                    evidence.extend(civic_evidence)
                    break
        return evidence
