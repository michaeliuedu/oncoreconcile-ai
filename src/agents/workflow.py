"""Workflow Orchestrator - Coordinate multi-agent pipeline

Orchestrates the complete variant reconciliation workflow:
1. Extraction → 2. Normalization → 3. Retrieval → 4. Reasoning → 5. Confidence → 6. Review
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import datetime

from .extraction_agent import ExtractionAgent
from .normalization_agent import NormalizationAgent
from .retrieval_agent import RetrievalAgent
from .reasoning_agent import ReasoningAgent
from .confidence_agent import ConfidenceAgent, compute_deterministic_score, compute_semantic_similarity_score, compute_historical_approval_score
from .review_agent import ReviewAgent


@dataclass
class ReconciliationJob:
    """Complete reconciliation job with full audit trail"""
    reconciliation_id: str
    raw_variant: str
    source: str
    status: str = "pending"
    
    # Agent outputs
    extracted: Optional[Dict[str, Any]] = None
    normalized: Optional[Dict[str, Any]] = None
    retrieved: Optional[Dict[str, Any]] = None
    reasoned: Optional[Dict[str, Any]] = None
    scored: Optional[Dict[str, Any]] = None
    review_entry: Optional[Dict[str, Any]] = None
    
    # Audit trail
    timestamps: Dict[str, datetime] = field(default_factory=dict)
    errors: Dict[str, str] = field(default_factory=dict)


class WorkflowOrchestrator:
    """Orchestrate multi-agent variant reconciliation workflow"""

    def __init__(self):
        """Initialize all agents"""
        self.extraction_agent = ExtractionAgent()
        self.normalization_agent = NormalizationAgent()
        self.retrieval_agent = RetrievalAgent()
        self.reasoning_agent = ReasoningAgent()
        self.confidence_agent = ConfidenceAgent()
        self.review_agent = ReviewAgent()
        self.jobs: Dict[str, ReconciliationJob] = {}

    def execute(self, raw_variant: str, source: str = "external") -> ReconciliationJob:
        """
        Execute full reconciliation workflow
        
        Args:
            raw_variant: Raw variant input string
            source: Source of variant
            
        Returns:
            ReconciliationJob with complete audit trail
        """
        
        # Create job
        job_id = f"rec_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        job = ReconciliationJob(
            reconciliation_id=job_id,
            raw_variant=raw_variant,
            source=source,
        )
        
        try:
            # Stage 1: Extraction
            job.timestamps["extraction_start"] = datetime.utcnow()
            extracted = self.extraction_agent.execute(raw_variant)
            job.extracted = {
                "gene": extracted.gene,
                "variant_type": extracted.variant_type,
                "location": extracted.location,
                "confidence": extracted.confidence,
                "notes": extracted.notes,
            }
            job.timestamps["extraction_end"] = datetime.utcnow()
            
            # Stage 2: Normalization
            job.timestamps["normalization_start"] = datetime.utcnow()
            normalized = self.normalization_agent.execute(
                gene=extracted.gene,
                variant_type=extracted.variant_type,
                location=extracted.location,
            )
            job.normalized = {
                "canonical_variant_id": normalized.canonical_variant_id,
                "canonical_gene": normalized.canonical_gene,
                "hgnc_id": normalized.hgnc_id,
                "transcript": normalized.transcript,
                "hgvs_dna": normalized.hgvs_dna,
                "hgvs_protein": normalized.hgvs_protein,
                "confidence": normalized.confidence,
            }
            job.timestamps["normalization_end"] = datetime.utcnow()
            
            # Stage 3: Retrieval
            job.timestamps["retrieval_start"] = datetime.utcnow()
            retrieved = self.retrieval_agent.execute(normalized.canonical_variant_id)
            job.retrieved = {
                "exact_match_found": retrieved.exact_match_found,
                "total_candidates": len(retrieved.candidates),
                "evidence_links_count": retrieved.evidence_links_count,
                "confidence": retrieved.confidence,
                "candidates": [
                    {
                        "canonical_id": c.canonical_id,
                        "relevance": c.relevance_score,
                        "approval_history": c.approval_history,
                    } for c in retrieved.candidates[:3]
                ]
            }
            job.timestamps["retrieval_end"] = datetime.utcnow()
            
            # Stage 4: Reasoning
            job.timestamps["reasoning_start"] = datetime.utcnow()
            clinical_sig = "Unknown"
            if retrieved.candidates:
                clinical_sig = retrieved.candidates[0].clinical_significance or "Unknown"
            
            reasoned = self.reasoning_agent.execute(
                canonical_variant_id=normalized.canonical_variant_id,
                clinical_significance=clinical_sig,
                candidates_found=len(retrieved.candidates),
                evidence_links_count=retrieved.evidence_links_count,
                approval_history=retrieved.candidates[0].approval_history if retrieved.candidates else None,
            )
            job.reasoned = {
                "clinical_summary": reasoned.clinical_summary,
                "llm_confidence": reasoned.llm_confidence,
                "recommendation": reasoned.recommendation,
                "treatment_relevance": reasoned.treatment_relevance,
            }
            job.timestamps["reasoning_end"] = datetime.utcnow()
            
            # Stage 5: Confidence Scoring
            job.timestamps["confidence_start"] = datetime.utcnow()
            
            deterministic = compute_deterministic_score(
                canonical_match=retrieved.exact_match_found,
                nomenclature_consistency=True,
                gene_validated=normalized.hgnc_id is not None,
            )
            
            semantic = compute_semantic_similarity_score(
                kb_candidates=len(retrieved.candidates),
                best_match_score=retrieved.candidates[0].relevance_score if retrieved.candidates else 0.0,
            )
            
            historical = compute_historical_approval_score(
                total_approvals=retrieved.candidates[0].approval_history.get("approvals", 0) if retrieved.candidates and retrieved.candidates[0].approval_history else 0,
                total_rejections=retrieved.candidates[0].approval_history.get("rejections", 0) if retrieved.candidates and retrieved.candidates[0].approval_history else 0,
            )
            
            scored = self.confidence_agent.execute(
                deterministic_score=deterministic,
                semantic_similarity_score=semantic,
                llm_confidence_score=reasoned.llm_confidence,
                historical_approval_score=historical,
            )
            
            job.scored = {
                "composite_score": scored.composite_score,
                "confidence_category": scored.confidence_category,
                "queue_recommendation": scored.queue_recommendation,
                "breakdown": scored.score_breakdown,
            }
            job.timestamps["confidence_end"] = datetime.utcnow()
            
            # Stage 6: Review Queue Assignment
            job.timestamps["review_start"] = datetime.utcnow()
            review_entry = self.review_agent.execute(
                reconciliation_id=job_id,
                input_variant=raw_variant,
                canonical_variant_id=normalized.canonical_variant_id,
                confidence_score=scored.composite_score,
                confidence_category=scored.confidence_category,
                clinical_summary=reasoned.clinical_summary,
                evidence_count=retrieved.evidence_links_count,
                approval_history=retrieved.candidates[0].approval_history if retrieved.candidates else None,
                reasoning_recommendation=reasoned.recommendation,
            )
            
            job.review_entry = {
                "review_id": review_entry.review_id,
                "queue_type": review_entry.queue_type.value,
                "priority": review_entry.priority.value,
                "assigned_reviewers": review_entry.assigned_reviewers,
                "estimated_review_time_minutes": review_entry.estimated_review_time_minutes,
            }
            job.timestamps["review_end"] = datetime.utcnow()
            
            job.status = "queued_for_review"
            
        except Exception as e:
            job.status = "error"
            job.errors["workflow"] = str(e)
        
        # Store job
        self.jobs[job_id] = job
        return job

    def get_job_status(self, job_id: str) -> Optional[ReconciliationJob]:
        """Get status of reconciliation job"""
        return self.jobs.get(job_id)

    def get_workflow_stats(self) -> Dict[str, Any]:
        """Get workflow execution statistics"""
        
        total_jobs = len(self.jobs)
        completed = len([j for j in self.jobs.values() if j.status in ["queued_for_review", "completed"]])
        errors = len([j for j in self.jobs.values() if j.status == "error"])
        
        return {
            "total_jobs": total_jobs,
            "completed": completed,
            "errors": errors,
            "review_queue_status": self.review_agent.get_queue_status(),
        }
