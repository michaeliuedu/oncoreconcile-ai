import httpx
import time
from typing import Any, Dict, Optional
from src.services.evidence.base import EvidenceProvider

CLINVAR_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
CLINVAR_SUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
CLINVAR_BASE_URL = "https://www.ncbi.nlm.nih.gov/clinvar/"

class ClinVarEvidenceProvider(EvidenceProvider):
    async def get_evidence(self, query: str, entity_type: str) -> Optional[Dict[str, Any]]:
        if entity_type != "variant":
            return None
        async with httpx.AsyncClient() as client:
            params = {"db": "clinvar", "term": query, "retmode": "json"}
            search_resp = await client.get(CLINVAR_SEARCH_URL, params=params)
            if search_resp.status_code != 200:
                return None
            search_data = search_resp.json()
            idlist = search_data.get("esearchresult", {}).get("idlist", [])
            if not idlist:
                return None
            clinvar_id = idlist[0]
            summary_params = {"db": "clinvar", "id": clinvar_id, "retmode": "json"}
            summary_resp = await client.get(CLINVAR_SUMMARY_URL, params=summary_params)
            if summary_resp.status_code != 200:
                return None
            summary_data = summary_resp.json()
            docsum = summary_data.get("result", {}).get(clinvar_id, {})
            clinical_significance = docsum.get("clinical_significance", {}).get("description")
            url = f"{CLINVAR_BASE_URL}{clinvar_id}"
            return {
                "source": "ClinVar",
                "url": url,
                "evidence_type": "clinical_variant_reference",
                "clinical_significance": clinical_significance,
                "retrieval_mode": "real_api",
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "confidence_weight": "High" if clinical_significance else "Medium"
            }
