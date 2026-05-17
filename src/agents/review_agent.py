"""Review Agent - Route reconciliations to human expert queue

This agent:
- Assigns reconciliations to expert reviewers
- Sets priority and queue type based on confidence
- Generates review briefs for human decision-making
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime


class QueueType(str, Enum):
    """Review queue types"""
    FAST_TRACK = "fast_track"
    STANDARD = "standard"
    ESCALATION = "escalation"
    MANUAL_CURATION = "manual_curation"


class Priority(str, Enum):
    """Review priorities"""
    LOW = "low"
    STANDARD = "standard"
    HIGH = "high"
    URGENT = "urgent"


@dataclass
class ReviewQueueEntry:
    """Entry in human review queue"""
    review_id: str
    reconciliation_id: str
    queue_type: QueueType
    priority: Priority
    assigned_reviewers: List[str] = field(default_factory=list)
    confidence_score: float = 0.0
    summary_brief: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    estimated_review_time_minutes: int = 0
    status: str = "pending"


@dataclass
class ReviewBrief:
    """Summary brief for human reviewer"""
    input_variant: str
    canonical_variant: str
    confidence_score: float
    confidence_category: str
    clinical_summary: str
    evidence_count: int
    approval_history: Optional[Dict[str, int]] = None
    reasoning_recommendation: str = ""
    key_decision_points: List[str] = field(default_factory=list)


class ReviewAgent:
    """Manage human review queue and assignments"""

    def __init__(self):
        """Initialize review agent"""
        self.review_queue: List[ReviewQueueEntry] = []
        self.available_reviewers = {
            "dr_chen": {"specialty": "Clinical Genomics", "load": 0, "capacity": 8},
            "dr_kim": {"specialty": "Computational Biology", "load": 0, "capacity": 8},
            "dr_patel": {"specialty": "Molecular Pathology", "load": 0, "capacity": 8},
        }

    def execute(
        self,
        reconciliation_id: str,
        input_variant: str,
        canonical_variant_id: str,
        confidence_score: float,
        confidence_category: str,
        clinical_summary: str,
        evidence_count: int,
        approval_history: Optional[Dict[str, int]] = None,
        reasoning_recommendation: str = "",
    ) -> ReviewQueueEntry:
        """
        Process reconciliation into review queue
        
        Args:
            reconciliation_id: Unique reconciliation ID
            input_variant: Original input variant string
            canonical_variant_id: Canonical variant ID
            confidence_score: Composite confidence score
            confidence_category: Confidence category (Very High, High, etc.)
            clinical_summary: LLM clinical summary
            evidence_count: Number of evidence links
            approval_history: Prior approval/rejection counts
            reasoning_recommendation: LLM recommendation
            
        Returns:
            ReviewQueueEntry assigned to reviewer(s)
        """
        
        # Determine queue and priority
        queue_type, estimated_time = self._determine_queue(
            confidence_score,
            approval_history
        )
        
        priority = self._determine_priority(
            confidence_score,
            evidence_count
        )
        
        # Assign reviewers
        reviewers = self._assign_reviewers(queue_type)
        
        # Generate review brief
        brief = ReviewBrief(
            input_variant=input_variant,
            canonical_variant=canonical_variant_id,
            confidence_score=confidence_score,
            confidence_category=confidence_category,
            clinical_summary=clinical_summary,
            evidence_count=evidence_count,
            approval_history=approval_history,
            reasoning_recommendation=reasoning_recommendation,
            key_decision_points=self._generate_decision_points(
                confidence_score,
                evidence_count,
                approval_history
            ),
        )
        
        # Create queue entry
        review_id = f"rev_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{reconciliation_id[-4:]}"
        entry = ReviewQueueEntry(
            review_id=review_id,
            reconciliation_id=reconciliation_id,
            queue_type=queue_type,
            priority=priority,
            assigned_reviewers=reviewers,
            confidence_score=confidence_score,
            summary_brief=str(brief),
            estimated_review_time_minutes=estimated_time,
        )
        
        # Add to queue
        self.review_queue.append(entry)
        
        # Update reviewer loads
        for reviewer in reviewers:
            if reviewer in self.available_reviewers:
                self.available_reviewers[reviewer]["load"] += 1
        
        return entry

    @staticmethod
    def _determine_queue(
        confidence_score: float,
        approval_history: Optional[Dict[str, int]] = None,
    ) -> tuple[QueueType, int]:
        """
        Determine queue type and estimated review time
        
        Returns:
            (queue_type, estimated_time_minutes)
        """
        
        # High confidence + good history = Fast-track
        if confidence_score > 0.95:
            if approval_history and approval_history.get("rejections", 0) == 0:
                return QueueType.FAST_TRACK, 3
            else:
                return QueueType.STANDARD, 8
        
        # Medium confidence = Standard
        elif confidence_score > 0.80:
            return QueueType.STANDARD, 8
        
        # Lower confidence = Escalation
        elif confidence_score > 0.60:
            return QueueType.ESCALATION, 20
        
        # Very low confidence = Manual curation
        else:
            return QueueType.MANUAL_CURATION, 45

    @staticmethod
    def _determine_priority(confidence_score: float, evidence_count: int) -> Priority:
        """Determine review priority"""
        
        if confidence_score > 0.95 and evidence_count > 2:
            return Priority.STANDARD
        elif confidence_score > 0.80:
            return Priority.STANDARD
        elif confidence_score > 0.60:
            return Priority.HIGH
        else:
            return Priority.URGENT

    def _assign_reviewers(self, queue_type: QueueType) -> List[str]:
        """Assign reviewer(s) based on queue type and load"""
        
        # Sort reviewers by load (ascending)
        sorted_reviewers = sorted(
            self.available_reviewers.items(),
            key=lambda x: x[1]["load"]
        )
        
        if queue_type == QueueType.FAST_TRACK:
            # Single reviewer for fast-track
            reviewer_id = sorted_reviewers[0][0]
            return [reviewer_id] if sorted_reviewers[0][1]["load"] < sorted_reviewers[0][1]["capacity"] else []
        
        elif queue_type == QueueType.STANDARD:
            # Single reviewer for standard
            reviewer_id = sorted_reviewers[0][0]
            return [reviewer_id] if sorted_reviewers[0][1]["load"] < sorted_reviewers[0][1]["capacity"] else []
        
        elif queue_type == QueueType.ESCALATION:
            # Two reviewers for escalation
            reviewers = []
            for reviewer_id, info in sorted_reviewers[:2]:
                if info["load"] < info["capacity"]:
                    reviewers.append(reviewer_id)
            return reviewers
        
        else:  # MANUAL_CURATION
            # All available reviewers
            reviewers = []
            for reviewer_id, info in sorted_reviewers:
                if info["load"] < info["capacity"]:
                    reviewers.append(reviewer_id)
            return reviewers[:3]  # Cap at 3

    @staticmethod
    def _generate_decision_points(
        confidence_score: float,
        evidence_count: int,
        approval_history: Optional[Dict[str, int]] = None,
    ) -> List[str]:
        """Generate key decision points for reviewer"""
        
        points = []
        
        if confidence_score > 0.95:
            points.append("✓ Very high confidence score - well-characterized variant")
        else:
            points.append("⚠ Lower confidence - recommend careful review")
        
        if evidence_count >= 3:
            points.append(f"✓ Strong evidence base ({evidence_count} sources)")
        elif evidence_count > 0:
            points.append(f"⚠ Limited evidence ({evidence_count} source)")
        else:
            points.append("⚠ No external evidence found - novel variant")
        
        if approval_history:
            total = approval_history.get("approvals", 0) + approval_history.get("rejections", 0)
            if total > 100:
                approval_rate = approval_history.get("approvals", 0) / total * 100
                points.append(f"✓ Strong precedent ({approval_history.get('approvals', 0)} approvals, {approval_rate:.0f}%)")
            elif total > 0 and approval_history.get("rejections", 0) > 0:
                points.append("⚠ Some prior rejections - review carefully")
        
        return points if points else ["Review required for approval"]

    def get_queue_status(self) -> Dict[str, Any]:
        """Get current queue status"""
        
        queue_counts = {}
        for queue_type in QueueType:
            queue_counts[queue_type.value] = len([
                e for e in self.review_queue if e.queue_type == queue_type and e.status == "pending"
            ])
        
        reviewer_loads = {}
        for reviewer_id, info in self.available_reviewers.items():
            reviewer_loads[reviewer_id] = {
                "load": info["load"],
                "capacity": info["capacity"],
                "utilization": f"{info['load']}/{info['capacity']}"
            }
        
        return {
            "total_pending": len([e for e in self.review_queue if e.status == "pending"]),
            "queue_counts": queue_counts,
            "reviewer_loads": reviewer_loads,
        }
