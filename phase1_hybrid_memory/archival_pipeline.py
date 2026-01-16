"""
Archival Pipeline
Manages the transition of memories from Tier 1 (active) to Tier 2 (persistent)
Includes compression, summarization, and intelligent archival triggers
"""

from typing import List, Optional, Callable
from datetime import datetime
import asyncio
from .memory_models import (
    MemoryEntry, MemoryTier, ArchivalTrigger,
    MemoryHealth
)
from .vector_store import VectorStore
from .embedding_generator import get_embedding_generator


class MemoryCompressor:
    """Compress and summarize memory content for archival"""

    def compress(self, content: str, target_ratio: float = 0.3) -> str:
        """
        Compress content to target ratio

        Args:
            content: Original content
            target_ratio: Target compression ratio (0.3 = 30% of original)

        Returns:
            Compressed content
        """
        sentences = [s.strip() for s in content.split(". ") if s.strip()]
        if not sentences:
            return content

        target_sentences = max(1, int(len(sentences) * target_ratio))

        scored_sentences = []
        for i, sentence in enumerate(sentences):
            score = len(sentence.split())
            score += sentence.count(",") * 2
            score += min(3, sum(1 for c in sentence if c.isdigit()))
            if sentence.endswith("?") or sentence.endswith("!"):
                score += 1
            scored_sentences.append((i, score, sentence))

        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        top_sentences = sorted(scored_sentences[:target_sentences], key=lambda x: x[0])
        compressed = ". ".join(sentence for _, _, sentence in top_sentences)

        if content.endswith(".") and not compressed.endswith("."):
            compressed += "."

        return compressed


class ImportanceScorer:
    """Heuristic importance scoring for archival decisions"""

    def score(self, entry: MemoryEntry) -> float:
        """
        Score memory importance from 0.0 to 1.0

        Args:
            entry: Memory entry to score

        Returns:
            Importance score
        """
        base_score = entry.metadata.importance_score or 0.5
        access_bonus = min(0.2, entry.metadata.access_count / 50.0)

        age_hours = (datetime.now() - entry.metadata.created_at).total_seconds() / 3600
        recency_bonus = 0.1 if age_hours < 24 else 0.0

        topic_bonus = min(0.1, 0.02 * len(entry.metadata.topics))
        tag_bonus = min(0.1, 0.02 * len(entry.metadata.tags))

        score = base_score + access_bonus + recency_bonus + topic_bonus + tag_bonus
        return max(0.0, min(1.0, score))


class ArchivalPipeline:
    """Manage archival workflow for Tier 1 to Tier 2 transition"""

    def __init__(
        self,
        vector_store: VectorStore,
        trigger: Optional[ArchivalTrigger] = None,
        compressor: Optional[MemoryCompressor] = None,
        importance_scorer: Optional[ImportanceScorer] = None
    ):
        self.vector_store = vector_store
        self.trigger = trigger or ArchivalTrigger()
        self.compressor = compressor or MemoryCompressor()
        self.importance_scorer = importance_scorer or ImportanceScorer()
        self.embedding_gen = get_embedding_generator()

    def evaluate_candidates(self, current_token_usage: float) -> List[MemoryEntry]:
        """Determine which Tier 1 entries should be archived"""
        tier1_entries = self.vector_store.list_tier_entries(MemoryTier.TIER_1_ACTIVE)
        candidates = []

        for entry in tier1_entries:
            entry.metadata.importance_score = self.importance_scorer.score(entry)
            if self.trigger.should_archive(entry, current_token_usage):
                candidates.append(entry)

        return candidates

    def archive_candidates(
        self,
        current_token_usage: float,
        target_ratio: float = 0.3
    ) -> List[str]:
        """
        Archive eligible Tier 1 entries

        Args:
            current_token_usage: Current token usage ratio
            target_ratio: Compression ratio for summaries

        Returns:
            List of archived memory IDs
        """
        archived_ids = []
        candidates = self.evaluate_candidates(current_token_usage)

        for entry in candidates:
            if not entry.summary and len(entry.content.split()) > 50:
                entry.summary = self.compressor.compress(entry.content, target_ratio=target_ratio)

            if entry.summary:
                entry.embedding = self.embedding_gen.generate(entry.summary)

            entry.metadata.tier = MemoryTier.TIER_2_PERSISTENT
            self.vector_store.add_memory(entry)
            self.vector_store.delete_memory(entry.id)
            archived_ids.append(entry.id)

        return archived_ids

    def get_health(self, current_token_usage: float) -> MemoryHealth:
        """Build health metrics for memory tiers"""
        tier1_entries = self.vector_store.list_tier_entries(MemoryTier.TIER_1_ACTIVE)
        tier2_entries = self.vector_store.list_tier_entries(MemoryTier.TIER_2_PERSISTENT)

        def avg_importance(entries: List[MemoryEntry]) -> float:
            if not entries:
                return 0.0
            return sum(e.metadata.importance_score for e in entries) / len(entries)

        oldest_age_hours = 0.0
        if tier1_entries:
            oldest = min(e.metadata.created_at for e in tier1_entries)
            oldest_age_hours = (datetime.now() - oldest).total_seconds() / 3600

        archival_candidates = len(self.evaluate_candidates(current_token_usage))

        return MemoryHealth(
            total_entries_tier1=len(tier1_entries),
            total_entries_tier2=len(tier2_entries),
            token_usage=current_token_usage,
            avg_importance_tier1=avg_importance(tier1_entries),
            avg_importance_tier2=avg_importance(tier2_entries),
            oldest_entry_age_hours=oldest_age_hours,
            archival_candidates=archival_candidates,
            fragmentation_score=0.0
        )


class ArchivalScheduler:
    """Background scheduler for periodic archival"""

    def __init__(self, pipeline: ArchivalPipeline, interval_seconds: int = 300):
        self.pipeline = pipeline
        self.interval_seconds = interval_seconds
        self._task: Optional[asyncio.Task] = None
        self._stop_event = asyncio.Event()

    async def _run_loop(self, token_usage_provider: Callable[[], float]):
        while not self._stop_event.is_set():
            token_usage = token_usage_provider()
            self.pipeline.archive_candidates(token_usage)

            try:
                await asyncio.wait_for(self._stop_event.wait(), timeout=self.interval_seconds)
            except asyncio.TimeoutError:
                continue

    def start(self, token_usage_provider: Callable[[], float]) -> None:
        """Start background archival loop"""
        if self._task and not self._task.done():
            return
        self._stop_event.clear()
        self._task = asyncio.create_task(self._run_loop(token_usage_provider))

    async def stop(self) -> None:
        """Stop background archival loop"""
        self._stop_event.set()
        if self._task:
            await self._task
