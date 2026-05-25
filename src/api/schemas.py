"""API Schemas - Pydantic models for request/response validation"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ReconcileRequest(BaseModel):
    """Variant reconciliation request"""
    raw_variant: str = Field(..., description="Raw variant string (e.g., 'EGFR Ex19del')")
    source: str = Field(default="external", description="Source of variant")
    tissue: Optional[str] = Field(None, description="Tissue type if applicable")
    vaf: Optional[float] = Field(None, description="Variant allele frequency (0-1)")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class ReconcileResponse(BaseModel):
    """Variant reconciliation response"""
    reconciliation_id: str
    status: str
    input_variant: str
    canonical_variant: Optional[str]
    confidence_score: Optional[float]
    confidence_category: Optional[str]
    review_id: Optional[str]
    queue_type: Optional[str]
    estimated_review_time_minutes: Optional[int]


class GeneReconcileRequest(BaseModel):
    """Gene reconciliation request"""
    gene_name: str = Field(..., description="Gene symbol or alias (e.g., 'HER1')")
    source: str = Field(default="external", description="Source of gene name")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class GeneReconcileResponse(BaseModel):
    """Gene reconciliation response"""
    input_gene: str
    canonical_gene: str
    hgnc_id: Optional[int]
    entrez_gene_id: Optional[int]
    confidence: float
    match_type: str
    aliases: List[str]
    description: Optional[str]
    notes: Optional[str]


class ReviewDecision(BaseModel):
    """Expert review decision"""
    reconciliation_id: str
    reviewer_id: str
    decision: str = Field(..., description="APPROVED | REJECTED | REQUEST_CHANGES")
    curation_notes: str = Field(..., description="Reviewer notes")


class ReviewDecisionResponse(BaseModel):
    """Response to review decision"""
    curation_id: str
    decision: str
    kb_version_before: str
    kb_version_after: str
    timestamp: datetime


class VariantQuery(BaseModel):
    """Query for variant retrieval"""
    canonical_id: Optional[str] = Field(None, description="Canonical variant ID")
    gene: Optional[str] = Field(None, description="Gene symbol")
    variant: Optional[str] = Field(None, description="Variant description")


class VariantInfo(BaseModel):
    """Variant information"""
    canonical_id: str
    gene: str
    hgvs_dna: str
    hgvs_protein: str
    clinical_significance: str
    aliases: List[str]
    evidence_count: int


class AuditLogEntry(BaseModel):
    """Audit log entry"""
    curation_id: str
    timestamp: datetime
    reviewer_name: str
    decision: str
    reconciliation_id: str
    curation_notes: str
    confidence_score: float


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    uptime_seconds: Optional[float]
