"""
Phase 1: Hybrid Memory Architecture
Core memory tier abstractions and interfaces

This module defines the foundational interfaces for the two-tier memory system:
- Tier 1: Fast in-context memory for active conversations
- Tier 2: Persistent disk-based memory for long-term storage
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum
import uuid


class MemoryTier(Enum):
    """Memory tier classification"""
    TIER_1_ACTIVE = "tier1_active"  # In-context, fast access
    TIER_2_PERSISTENT = "tier2_persistent"  # Disk-based, unlimited
    

class ImportanceLevel(Enum):
    """Importance classification for memory entries"""
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    MINIMAL = 1


@dataclass
class MemoryMetadata:
    """Metadata for memory entries"""
    created_at: datetime = field(default_factory=datetime.now)
    last_accessed: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    importance_score: float = 0.5  # 0.0 to 1.0
    topics: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    source: str = "user_conversation"
    tier: MemoryTier = MemoryTier.TIER_1_ACTIVE
    related_memories: List[str] = field(default_factory=list)  # UUIDs
    

@dataclass
class MemoryEntry:
    """Core memory entry structure"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    content: str = ""
    summary: Optional[str] = None
    embedding: Optional[List[float]] = None
    metadata: MemoryMetadata = field(default_factory=MemoryMetadata)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage"""
        return {
            "id": self.id,
            "content": self.content,
            "summary": self.summary,
            "embedding": self.embedding,
            "metadata": {
                "created_at": self.metadata.created_at.isoformat(),
                "last_accessed": self.metadata.last_accessed.isoformat(),
                "access_count": self.metadata.access_count,
                "importance_score": self.metadata.importance_score,
                "topics": self.metadata.topics,
                "tags": self.metadata.tags,
                "source": self.metadata.source,
                "tier": self.metadata.tier.value,
                "related_memories": self.metadata.related_memories
            }
        }
    

class MemoryInterface(ABC):
    """Abstract interface for memory operations"""
    
    @abstractmethod
    async def store(self, entry: MemoryEntry) -> str:
        """Store a memory entry and return its ID"""
        pass
    
    @abstractmethod
    async def retrieve(self, query: str, limit: int = 10) -> List[MemoryEntry]:
        """Retrieve memories matching the query"""
        pass
    
    @abstractmethod
    async def update(self, memory_id: str, updates: Dict[str, Any]) -> bool:
        """Update a memory entry"""
        pass
    
    @abstractmethod
    async def delete(self, memory_id: str) -> bool:
        """Delete a memory entry"""
        pass
    
    @abstractmethod
    async def get_by_id(self, memory_id: str) -> Optional[MemoryEntry]:
        """Retrieve a specific memory by ID"""
        pass
    
    @abstractmethod
    async def get_health_stats(self) -> Dict[str, Any]:
        """Get memory system health statistics"""
        pass
    
    @abstractmethod
    async def archive(self, memory_id: str) -> bool:
        """Archive a memory (move from Tier 1 to Tier 2)"""
        pass


@dataclass
class ArchivalTrigger:
    """Conditions that trigger memory archival"""
    age_threshold_hours: float = 24.0
    token_pressure_threshold: float = 0.7  # 70% usage
    min_importance_score: float = 0.3
    explicit_user_request: bool = False
    
    def should_archive(self, entry: MemoryEntry, current_token_usage: float) -> bool:
        """Determine if a memory should be archived"""
        # Explicit user request always triggers
        if self.explicit_user_request:
            return True
        
        # Check age
        age_hours = (datetime.now() - entry.metadata.created_at).total_seconds() / 3600
        if age_hours > self.age_threshold_hours:
            return True
        
        # Check token pressure
        if current_token_usage > self.token_pressure_threshold:
            # Archive lower importance items first under pressure
            if entry.metadata.importance_score < self.min_importance_score:
                return True
        
        return False


@dataclass
class MemoryHealth:
    """Memory system health metrics"""
    total_entries_tier1: int = 0
    total_entries_tier2: int = 0
    token_usage: float = 0.0  # 0.0 to 1.0
    token_limit: int = 190000
    avg_importance_tier1: float = 0.0
    avg_importance_tier2: float = 0.0
    oldest_entry_age_hours: float = 0.0
    archival_candidates: int = 0
    fragmentation_score: float = 0.0  # 0.0 to 1.0, higher is worse
    
    def needs_optimization(self) -> bool:
        """Check if memory system needs optimization"""
        return (
            self.token_usage > 0.8 or  # Over 80% token usage
            self.archival_candidates > 10 or  # Many stale entries
            self.fragmentation_score > 0.6  # High fragmentation
        )
