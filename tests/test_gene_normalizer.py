"""Test suite for gene normalization"""

import pytest
from src.agents.normalization_agent import GeneNormalizer


class TestGeneNormalizer:
    """Test gene normalization"""

    def setup_method(self):
        """Setup test fixtures"""
        self.normalizer = GeneNormalizer()

    def test_normalize_egfr(self):
        """Test EGFR normalization"""
        result = self.normalizer.normalize_gene("EGFR")
        assert result["canonical"] == "EGFR"
        assert result["hgnc_id"] == 3236
        assert result["entrez_id"] == 1956

    def test_normalize_egfr_alias_her1(self):
        """Test HER1 → EGFR normalization"""
        result = self.normalizer.normalize_gene("HER1")
        assert result["canonical"] == "EGFR"

    def test_normalize_braf(self):
        """Test BRAF normalization"""
        result = self.normalizer.normalize_gene("BRAF")
        assert result["canonical"] == "BRAF"

    def test_normalize_unknown_gene(self):
        """Test unknown gene handling"""
        result = self.normalizer.normalize_gene("UNKNOWN_GENE")
        assert result["canonical"] == "UNKNOWN_GENE"
        assert result.get("hgnc_id") is None

    def test_case_insensitive(self):
        """Test case-insensitive normalization"""
        result1 = self.normalizer.normalize_gene("egfr")
        result2 = self.normalizer.normalize_gene("EGFR")
        result3 = self.normalizer.normalize_gene("EgFr")
        
        assert result1 == result2 == result3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
