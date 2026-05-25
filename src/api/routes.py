"""API Routes - FastAPI endpoint implementations"""

from fastapi import APIRouter, HTTPException
from datetime import datetime

from .schemas import (
    GeneReconcileRequest, GeneReconcileResponse,
    ReconcileRequest, ReconcileResponse, ReviewDecision, ReviewDecisionResponse,
    VariantQuery, VariantInfo, AuditLogEntry, HealthResponse
)
from ..agents.workflow import WorkflowOrchestrator
from ..agents.normalization_agent import GeneReconciliationAgent

router = APIRouter()
workflow = WorkflowOrchestrator()
gene_reconciliation_agent = GeneReconciliationAgent()

# Track start time for uptime
_start_time = datetime.utcnow()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    uptime = (datetime.utcnow() - _start_time).total_seconds()
    return HealthResponse(
        status="ok",
        version="0.1.0",
        uptime_seconds=uptime
    )


@router.post("/reconcile", response_model=ReconcileResponse)
async def submit_reconciliation(request: ReconcileRequest):
    """
    Submit a variant for reconciliation
    
    The system will:
    1. Extract variant components
    2. Normalize to canonical form
    3. Search KB for matches
    4. Generate clinical reasoning
    5. Score confidence
    6. Route to expert review queue
    
    Returns immediately with reconciliation_id for polling.
    """
    try:
        # Execute workflow
        job = workflow.execute(
            raw_variant=request.raw_variant,
            source=request.source
        )
        
        # Build response
        response_data = {
            "reconciliation_id": job.reconciliation_id,
            "status": job.status,
            "input_variant": job.raw_variant,
            "canonical_variant": job.normalized.get("canonical_variant_id") if job.normalized else None,
            "confidence_score": job.scored.get("composite_score") if job.scored else None,
            "confidence_category": job.scored.get("confidence_category") if job.scored else None,
            "review_id": job.review_entry.get("review_id") if job.review_entry else None,
            "queue_type": job.review_entry.get("queue_type") if job.review_entry else None,
            "estimated_review_time_minutes": job.review_entry.get("estimated_review_time_minutes") if job.review_entry else None,
        }
        
        return ReconcileResponse(**response_data)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reconcile/gene", response_model=GeneReconcileResponse)
async def reconcile_gene(request: GeneReconcileRequest):
    """
    Reconcile a gene symbol or alias to a canonical HGNC-style gene record.

    This is deterministic and CSV-backed in the MVP, using data/reference/v0.1/gene_aliases.csv
    as the source of truth.
    """
    result = gene_reconciliation_agent.execute(request.gene_name)
    return GeneReconcileResponse(
        input_gene=result.input_gene,
        canonical_gene=result.canonical_gene,
        hgnc_id=result.hgnc_id,
        entrez_gene_id=result.entrez_gene_id,
        confidence=result.confidence,
        match_type=result.match_type,
        aliases=result.aliases,
        description=result.description,
        notes=result.notes,
    )


@router.get("/reconcile/{reconciliation_id}", response_model=ReconcileResponse)
async def get_reconciliation_status(reconciliation_id: str):
    """Get status and details of a reconciliation"""
    
    job = workflow.get_job_status(reconciliation_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Reconciliation {reconciliation_id} not found")
    
    response_data = {
        "reconciliation_id": job.reconciliation_id,
        "status": job.status,
        "input_variant": job.raw_variant,
        "canonical_variant": job.normalized.get("canonical_variant_id") if job.normalized else None,
        "confidence_score": job.scored.get("composite_score") if job.scored else None,
        "confidence_category": job.scored.get("confidence_category") if job.scored else None,
        "review_id": job.review_entry.get("review_id") if job.review_entry else None,
        "queue_type": job.review_entry.get("queue_type") if job.review_entry else None,
        "estimated_review_time_minutes": job.review_entry.get("estimated_review_time_minutes") if job.review_entry else None,
    }
    
    return ReconcileResponse(**response_data)


@router.get("/review-queue")
async def get_review_queue():
    """Get current review queue status"""
    return workflow.review_agent.get_queue_status()


@router.post("/review/{reconciliation_id}/approve", response_model=ReviewDecisionResponse)
async def approve_reconciliation(reconciliation_id: str, decision: ReviewDecision):
    """Approve a reconciliation for KB update"""
    
    job = workflow.get_job_status(reconciliation_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Reconciliation not found")
    
    # Log curation decision
    curation_id = f"cur_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
    
    return ReviewDecisionResponse(
        curation_id=curation_id,
        decision=decision.decision,
        kb_version_before="0.1",
        kb_version_after="0.1.1",
        timestamp=datetime.utcnow()
    )


@router.get("/search")
async def search_variants(query: VariantQuery):
    """Search for variants in KB"""
    # Placeholder
    return {
        "results": [],
        "query": query.dict()
    }


@router.get("/audit-log")
async def get_audit_log():
    """Get curation audit log"""
    # Placeholder
    return {
        "entries": [],
        "total": 0
    }
