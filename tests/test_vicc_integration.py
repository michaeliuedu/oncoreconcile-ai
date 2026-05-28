"""
Minimal tests for VICC Normalizer integration.
"""
from src.services.reconciliation_service import reconcile_with_vicc

def test_original_input():
    out = reconcile_with_vicc("p53", "gene")
    assert out["original_input"] == "p53"

def test_evidence_sources():
    out = reconcile_with_vicc("BRAF V600E", "variant")
    assert out["evidence_sources"]

def test_failed_lookup_human_review():
    out = reconcile_with_vicc("unknown alteration", "variant")
    assert out["requires_human_review"] is True
    assert out["cannot_reconcile"] is True
