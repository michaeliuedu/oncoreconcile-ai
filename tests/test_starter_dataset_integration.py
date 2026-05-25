"""Regression tests for the synthetic starter data package"""

import csv
from pathlib import Path

from src.agents.normalization_agent import GeneNormalizer, NormalizationAgent, VariantNormalizer


REPO_ROOT = Path(__file__).resolve().parents[1]
STARTER_MASTER = REPO_ROOT / "oncoreconcile_starter" / "oncology_variants_master.csv"
REFERENCE_SYNONYMS = REPO_ROOT / "data" / "reference" / "v0.1" / "variant_synonyms.csv"


def _normalize_lookup_text(value: str) -> str:
    return " ".join(value.upper().replace("::", "-").replace("_", " ").split())


def _load_starter_rows(record_ids: set[str]) -> list[dict[str, str]]:
    with STARTER_MASTER.open(newline="") as csvfile:
        return [
            row for row in csv.DictReader(csvfile)
            if row["record_id"] in record_ids
        ]


def _load_expected_canonical_map() -> dict[tuple[str, str], str]:
    expected = {}
    with REFERENCE_SYNONYMS.open(newline="") as csvfile:
        for row in csv.DictReader(csvfile):
            gene = row["canonical_id"].split("|")[0]
            expected[(gene, _normalize_lookup_text(row["synonym"]))] = row["canonical_id"]
    return expected


def test_reference_synonyms_cover_selected_starter_rows():
    """Selected starter gold rows should reconcile through reference CSV data"""
    rows = _load_starter_rows({
        "OR-0001",  # BRAF p.V600E
        "OR-0008",  # ROS-1 / ROS1 fusion
        "OR-0013",  # ERBB-2 amplification
        "OR-0015",  # RET fusion partner syntax
        "OR-0023",  # MET exon 14 skipping/deletion wording
        "OR-0030",  # P53 alias to TP53
    })
    expected_canonical_map = _load_expected_canonical_map()
    gene_normalizer = GeneNormalizer()
    normalization_agent = NormalizationAgent()

    assert len(rows) == 6

    for row in rows:
        gene_info = gene_normalizer.normalize_gene(row["gene_raw"])
        assert gene_info["canonical"] == row["gene_normalized_expected"]

        expected_key = (
            row["gene_normalized_expected"],
            _normalize_lookup_text(row["variant_normalized_expected"]),
        )
        expected_canonical_id = expected_canonical_map[expected_key]

        normalized = normalization_agent.execute(
            gene=gene_info["canonical"],
            variant_type=row["variant_category"],
            location=row["variant_raw"],
        )

        assert normalized.canonical_variant_id == expected_canonical_id


def test_variant_normalizer_uses_reference_synonym_lookup_before_fallbacks():
    """VariantNormalizer should reconcile starter-style synonyms from CSV"""
    normalizer = VariantNormalizer()

    assert normalizer.normalize_variant("RET", "fusion", "KIF5B::RET")["canonical_id"] == "RET|fusion"
    assert normalizer.normalize_variant("ERBB2", "amplification", "ERBB-2 amplification")["canonical_id"] == "ERBB2|amplification"
    assert normalizer.normalize_variant("TP53", "substitution", "p.Arg175His")["canonical_id"] == "TP53|R175H"
