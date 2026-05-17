"""Review Queue - Manage pending expert reviews

Tracks:
- Pending reconciliations awaiting review
- Reviewer assignments
- Review status
- Completion metrics
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime


@dataclass
class ReviewQueueItem:
    """Item in review queue"""
    review_id: str
    reconciliation_id: str
    assigned_reviewers: List[str]
    status: str  # pending, in_progress, completed
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    priority: str = "standard"
    queue_type: str = "standard"


class ReviewQueue:
    """Manage human review queue"""

    def __init__(self):
        """Initialize review queue"""
        self.items: Dict[str, ReviewQueueItem] = {}

    def add_item(
        self,
        review_id: str,
        reconciliation_id: str,
        assigned_reviewers: List[str],
        priority: str = "standard",
        queue_type: str = "standard",
    ) -> ReviewQueueItem:
        """
        Add item to review queue
        
        Args:
            review_id: Unique review ID
            reconciliation_id: Related reconciliation ID
            assigned_reviewers: List of reviewer IDs
            priority: Priority level
            queue_type: Queue type (fast_track, standard, escalation)
            
        Returns:
            ReviewQueueItem
        """
        item = ReviewQueueItem(
            review_id=review_id,
            reconciliation_id=reconciliation_id,
            assigned_reviewers=assigned_reviewers,
            status="pending",
            created_at=datetime.utcnow(),
            priority=priority,
            queue_type=queue_type,
        )
        
        self.items[review_id] = item
        return item

    def start_review(self, review_id: str) -> Optional[ReviewQueueItem]:
        """Mark review as started"""
        if review_id in self.items:
            self.items[review_id].started_at = datetime.utcnow()
            self.items[review_id].status = "in_progress"
            return self.items[review_id]
        return None

    def complete_review(self, review_id: str) -> Optional[ReviewQueueItem]:
        """Mark review as completed"""
        if review_id in self.items:
            self.items[review_id].completed_at = datetime.utcnow()
            self.items[review_id].status = "completed"
            return self.items[review_id]
        return None

    def get_pending_reviews(self, reviewer_id: Optional[str] = None) -> List[ReviewQueueItem]:
        """Get pending reviews, optionally filtered by reviewer"""
        pending = [item for item in self.items.values() if item.status == "pending"]
        
        if reviewer_id:
            pending = [item for item in pending if reviewer_id in item.assigned_reviewers]
        
        # Sort by priority and created_at
        priority_map = {"urgent": 1, "high": 2, "standard": 3, "low": 4}
        pending.sort(
            key=lambda x: (priority_map.get(x.priority, 5), x.created_at)
        )
        
        return pending

    def get_queue_metrics(self) -> Dict[str, Any]:
        """Get queue metrics"""
        
        pending_items = [item for item in self.items.values() if item.status == "pending"]
        completed_items = [item for item in self.items.values() if item.status == "completed"]
        
        review_times = []
        for item in completed_items:
            if item.started_at and item.completed_at:
                duration = (item.completed_at - item.started_at).total_seconds() / 60
                review_times.append(duration)
        
        return {
            "total_pending": len(pending_items),
            "total_completed": len(completed_items),
            "average_review_time_minutes": sum(review_times) / len(review_times) if review_times else 0,
            "pending_by_priority": {
                "urgent": len([i for i in pending_items if i.priority == "urgent"]),
                "high": len([i for i in pending_items if i.priority == "high"]),
                "standard": len([i for i in pending_items if i.priority == "standard"]),
            },
        }
