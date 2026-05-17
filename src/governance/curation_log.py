"""Curation Log - Audit trail for all reconciliation decisions

Tracks:
- Who approved/rejected what
- When decisions were made
- Complete reasoning chains
- Knowledge base version changes
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class DecisionType(str, Enum):
    """Types of curation decisions"""
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    REQUESTED_CHANGES = "REQUESTED_CHANGES"
    ESCALATED = "ESCALATED"


@dataclass
class CurationRecord:
    """Single curation decision record"""
    curation_id: str
    reconciliation_id: str
    reviewer_id: str
    reviewer_name: str
    decision: DecisionType
    timestamp: datetime
    curation_notes: str
    confidence_score: float
    kb_version_before: str
    kb_version_after: str
    reasoning_chain: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class CurationLog:
    """Audit log for curation decisions"""

    def __init__(self):
        """Initialize curation log"""
        self.records: list[CurationRecord] = []

    def log_decision(
        self,
        curation_id: str,
        reconciliation_id: str,
        reviewer_id: str,
        reviewer_name: str,
        decision: DecisionType,
        curation_notes: str,
        confidence_score: float,
        kb_version_before: str,
        kb_version_after: str,
        reasoning_chain: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> CurationRecord:
        """
        Log a curation decision
        
        Args:
            curation_id: Unique curation record ID
            reconciliation_id: Related reconciliation ID
            reviewer_id: Reviewer identifier
            reviewer_name: Reviewer name
            decision: Approval decision
            curation_notes: Human-written notes
            confidence_score: System confidence score
            kb_version_before: KB version before change
            kb_version_after: KB version after change
            reasoning_chain: Complete reasoning chain
            metadata: Additional metadata
            
        Returns:
            CurationRecord
        """
        record = CurationRecord(
            curation_id=curation_id,
            reconciliation_id=reconciliation_id,
            reviewer_id=reviewer_id,
            reviewer_name=reviewer_name,
            decision=decision,
            timestamp=datetime.utcnow(),
            curation_notes=curation_notes,
            confidence_score=confidence_score,
            kb_version_before=kb_version_before,
            kb_version_after=kb_version_after,
            reasoning_chain=reasoning_chain,
            metadata=metadata or {},
        )
        
        self.records.append(record)
        return record

    def get_decision_history(self, variant_id: str) -> list[CurationRecord]:
        """Get all decisions for a variant"""
        # Placeholder: would query variant_id from metadata
        return [
            r for r in self.records
            if variant_id in str(r.metadata) or variant_id in r.reasoning_chain.get("canonical_id", "")
        ]

    def get_reviewer_stats(self, reviewer_id: str) -> Dict[str, Any]:
        """Get statistics for reviewer"""
        reviewer_records = [r for r in self.records if r.reviewer_id == reviewer_id]
        
        return {
            "total_decisions": len(reviewer_records),
            "approvals": len([r for r in reviewer_records if r.decision == DecisionType.APPROVED]),
            "rejections": len([r for r in reviewer_records if r.decision == DecisionType.REJECTED]),
            "average_confidence": (
                sum(r.confidence_score for r in reviewer_records) / len(reviewer_records)
                if reviewer_records else 0
            ),
        }

    def export_audit_trail(self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> str:
        """Export audit trail as formatted text"""
        
        records = self.records
        if start_date:
            records = [r for r in records if r.timestamp >= start_date]
        if end_date:
            records = [r for r in records if r.timestamp <= end_date]
        
        output = "ONCORECONCILE AI - AUDIT TRAIL EXPORT\n"
        output += f"Generated: {datetime.utcnow().isoformat()}\n"
        output += f"Records: {len(records)}\n"
        output += "=" * 80 + "\n\n"
        
        for record in records:
            output += f"Curation ID: {record.curation_id}\n"
            output += f"Timestamp: {record.timestamp.isoformat()}\n"
            output += f"Reviewer: {record.reviewer_name} ({record.reviewer_id})\n"
            output += f"Decision: {record.decision.value}\n"
            output += f"Confidence: {record.confidence_score:.2f}\n"
            output += f"Notes: {record.curation_notes}\n"
            output += "-" * 80 + "\n\n"
        
        return output
