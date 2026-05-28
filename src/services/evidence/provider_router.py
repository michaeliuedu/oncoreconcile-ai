from src.services.evidence.hgnc_provider import HGNCEvidenceProvider
from src.services.evidence.clinvar_provider import ClinVarEvidenceProvider
from typing import Optional, Dict, Any

class EvidenceProviderRouter:
    def __init__(self):
        self.hgnc = HGNCEvidenceProvider()
        self.clinvar = ClinVarEvidenceProvider()

    async def get_gene_evidence(self, query: str) -> Optional[Dict[str, Any]]:
        return await self.hgnc.get_evidence(query, "gene")

    async def get_variant_evidence(self, query: str) -> Optional[Dict[str, Any]]:
        return await self.clinvar.get_evidence(query, "variant")

    async def get_evidence(self, query: str, entity_type: str) -> Optional[Dict[str, Any]]:
        if entity_type == "gene":
            return await self.get_gene_evidence(query)
        elif entity_type == "variant":
            return await self.get_variant_evidence(query)
        return None
