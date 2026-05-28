import abc
from typing import Any, Dict, Optional

class EvidenceProvider(abc.ABC):
    """Abstract base class for all evidence providers."""
    @abc.abstractmethod
    async def get_evidence(self, query: str, entity_type: str) -> Optional[Dict[str, Any]]:
        """Retrieve evidence for a given query and entity type (gene/variant)."""
        pass
