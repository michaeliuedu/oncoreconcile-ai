import httpx
import time
from typing import Any, Dict, Optional
from src.services.evidence.base import EvidenceProvider

HGNC_API_URL = "https://rest.genenames.org/fetch/symbol/{}"
HGNC_REPORT_URL = "https://www.genenames.org/data/gene-symbol-report/#!/hgnc_id/{}"

class HGNCEvidenceProvider(EvidenceProvider):
    async def get_evidence(self, query: str, entity_type: str) -> Optional[Dict[str, Any]]:
        if entity_type != "gene":
            return None
        async with httpx.AsyncClient() as client:
            resp = await client.get(HGNC_API_URL.format(query), headers={"Accept": "application/json"})
            if resp.status_code != 200:
                return None
            data = resp.json()
            docs = data.get("response", {}).get("docs", [])
            if not docs:
                return None
            doc = docs[0]
            hgnc_id = doc.get("hgnc_id")
            symbol = doc.get("symbol")
            url = HGNC_REPORT_URL.format(hgnc_id)
            return {
                "source": "HGNC",
                "url": url,
                "evidence_type": "gene_normalization_reference",
                "hgnc_id": hgnc_id,
                "retrieval_mode": "real_api",
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "confidence_weight": "High" if symbol and symbol.upper() == query.upper() else "Medium"
            }
