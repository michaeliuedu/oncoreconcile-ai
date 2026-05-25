"""Test suite for gene normalization"""

import pytest
from src.agents.normalization_agent import GeneNormalizer, GeneReconciliationAgent


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
        assert result["match_type"] == "alias"
        assert result["confidence"] == 0.95

    def test_normalize_braf(self):
        """Test BRAF normalization"""
        result = self.normalizer.normalize_gene("BRAF")
        assert result["canonical"] == "BRAF"
        assert result["match_type"] == "canonical"

    def test_normalize_unknown_gene(self):
        """Test unknown gene handling"""
        result = self.normalizer.normalize_gene("UNKNOWN_GENE")
        assert result["canonical"] == "UNKNOWN_GENE"
        assert result.get("hgnc_id") is None
        assert result["match_type"] == "unmatched"

    def test_case_insensitive(self):
        """Test case-insensitive normalization"""
        result1 = self.normalizer.normalize_gene("egfr")
        result2 = self.normalizer.normalize_gene("EGFR")
        result3 = self.normalizer.normalize_gene("EgFr")
        
        assert result1 == result2 == result3

    def test_reconcile_gene_agent_alias(self):
        """Test first-class gene reconciliation for aliases"""
        agent = GeneReconciliationAgent()
        result = agent.execute("HER2")

        assert result.input_gene == "HER2"
        assert result.canonical_gene == "ERBB2"
        assert result.hgnc_id == 3236
        assert result.entrez_gene_id == 2064
        assert result.match_type == "alias"
        assert "HER2" in result.aliases

    def test_reconcile_gene_agent_unknown(self):
        """Test first-class gene reconciliation for unknown genes"""
        agent = GeneReconciliationAgent()
        result = agent.execute("NOT_A_GENE")

        assert result.canonical_gene == "NOT_A_GENE"
        assert result.match_type == "unmatched"
        assert result.confidence == 0.3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
