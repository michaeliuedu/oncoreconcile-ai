"""Test suite for gene reconciliation API endpoints"""

from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


def test_reconcile_gene_alias():
    """Test gene alias reconciliation through the API"""
    response = client.post(
        "/reconcile/gene",
        json={"gene_name": "HER1", "source": "test"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["input_gene"] == "HER1"
    assert data["canonical_gene"] == "EGFR"
    assert data["hgnc_id"] == 3236
    assert data["entrez_gene_id"] == 1956
    assert data["match_type"] == "alias"
    assert data["confidence"] == 0.95
    assert "HER1" in data["aliases"]


def test_reconcile_gene_unknown():
    """Test unknown gene reconciliation through the API"""
    response = client.post(
        "/reconcile/gene",
        json={"gene_name": "UNKNOWN_GENE"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["canonical_gene"] == "UNKNOWN_GENE"
    assert data["match_type"] == "unmatched"
    assert data["confidence"] == 0.3
    assert data["notes"]
