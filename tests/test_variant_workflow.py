"""Test suite for variant reconciliation workflow"""

import pytest
from src.agents.workflow import WorkflowOrchestrator


class TestWorkflow:
    """Test variant reconciliation workflow"""

    def setup_method(self):
        """Setup test fixtures"""
        self.workflow = WorkflowOrchestrator()

    def test_workflow_egfr_ex19del(self):
        """Test EGFR exon 19 deletion workflow"""
        job = self.workflow.execute(raw_variant="EGFR Ex19del", source="test_lab")
        
        assert job.reconciliation_id.startswith("rec_")
        assert job.status in ["queued_for_review", "error"]
        assert job.extracted is not None
        assert job.extracted["gene"] == "EGFR"
        assert job.extracted["variant_type"] == "deletion"

    def test_workflow_normalization_stage(self):
        """Test normalization stage produces canonical form"""
        job = self.workflow.execute(raw_variant="BRAF V600E")
        
        assert job.normalized is not None
        assert job.normalized["canonical_gene"] == "BRAF"
        assert "V600E" in job.normalized["canonical_variant_id"]

    def test_workflow_confidence_scoring(self):
        """Test confidence scoring"""
        job = self.workflow.execute(raw_variant="KRAS G12C")
        
        assert job.scored is not None
        assert 0 <= job.scored["composite_score"] <= 1
        assert job.scored["confidence_category"] in [
            "Very High", "High", "Moderate", "Low", "Very Low"
        ]

    def test_workflow_review_queue_assignment(self):
        """Test review queue assignment"""
        job = self.workflow.execute(raw_variant="EGFR Ex19del")
        
        assert job.review_entry is not None
        assert "review_id" in job.review_entry
        assert "queue_type" in job.review_entry

    def test_workflow_full_pipeline(self):
        """Test complete workflow pipeline"""
        test_variants = [
            "EGFR Ex19del",
            "BRAF V600E",
            "KRAS G12C",
        ]
        
        for variant in test_variants:
            job = self.workflow.execute(raw_variant=variant)
            
            # Verify all stages completed
            assert job.extracted is not None, f"Extraction failed for {variant}"
            assert job.normalized is not None, f"Normalization failed for {variant}"
            assert job.retrieved is not None, f"Retrieval failed for {variant}"
            assert job.reasoned is not None, f"Reasoning failed for {variant}"
            assert job.scored is not None, f"Scoring failed for {variant}"
            assert job.review_entry is not None, f"Review assignment failed for {variant}"


class TestExtractionAgent:
    """Test extraction agent"""

    def test_egfr_ex19del_extraction(self):
        """Test EGFR exon 19 deletion extraction"""
        from src.agents.extraction_agent import ExtractionAgent
        
        agent = ExtractionAgent()
        result = agent.execute("EGFR Ex19del")
        
        assert result.gene == "EGFR"
        assert result.variant_type == "deletion"
        assert "19" in result.location

    def test_braf_v600e_extraction(self):
        """Test BRAF V600E extraction"""
        from src.agents.extraction_agent import ExtractionAgent
        
        agent = ExtractionAgent()
        result = agent.execute("BRAF V600E")
        
        assert result.gene == "BRAF"
        assert result.variant_type == "substitution"
        assert result.location == "V600E"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
