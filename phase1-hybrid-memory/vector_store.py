"""
Vector Storage System using ChromaDB
Persistent storage for memory embeddings and semantic search
"""

import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import json
from .memory_models import MemoryEntry, MemoryMetadata, MemoryTier
from .embedding_generator import get_embedding_generator


class VectorStore:
    """ChromaDB-based vector storage for memory system"""
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        """
        Initialize vector store
        
        Args:
            persist_directory: Directory for persistent storage
        """
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=str(self.persist_directory),
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Get or create collections for each tier
        self.tier1_collection = self.client.get_or_create_collection(
            name="tier1_active_memory",
            metadata={"description": "In-context active memory"}
        )
        
        self.tier2_collection = self.client.get_or_create_collection(
            name="tier2_persistent_memory",
            metadata={"description": "Long-term persistent memory"}
        )
        
        self.embedding_gen = get_embedding_generator()
    
    def add_memory(self, entry: MemoryEntry) -> str:
        """
        Add a memory entry to the vector store
        
        Args:
            entry: Memory entry to store
            
        Returns:
            Memory ID
        """
        # Generate embedding if not provided
        if entry.embedding is None:
            content_to_embed = entry.summary if entry.summary else entry.content
            entry.embedding = self.embedding_gen.generate(content_to_embed)
        
        # Choose collection based on tier
        collection = (self.tier1_collection if entry.metadata.tier == MemoryTier.TIER_1_ACTIVE 
                     else self.tier2_collection)
        
        # Prepare metadata (ChromaDB requires string/number/bool values)
        metadata = {
            "created_at": entry.metadata.created_at.isoformat(),
            "importance_score": entry.metadata.importance_score,
            "source": entry.metadata.source,
            "tier": entry.metadata.tier.value,
            "topics": json.dumps(entry.metadata.topics),
            "tags": json.dumps(entry.metadata.tags),
            "has_summary": entry.summary is not None
        }
        
        # Add to collection
        collection.add(
            ids=[entry.id],
            embeddings=[entry.embedding],
            documents=[entry.content],
            metadatas=[metadata]
        )
        
        return entry.id
    
    def search(self, query: str, tier: Optional[MemoryTier] = None, 
               limit: int = 10, min_score: float = 0.5) -> List[Tuple[MemoryEntry, float]]:
        """
        Semantic search for memories
        
        Args:
            query: Search query text
            tier: Optional tier filter
            limit: Maximum results to return
            min_score: Minimum similarity score (0 to 1)
            
        Returns:
            List of (MemoryEntry, similarity_score) tuples
        """
        # Generate query embedding
        query_embedding = self.embedding_gen.generate(query)
        
        # Determine which collections to search
        collections = []
        if tier is None:
            collections = [self.tier1_collection, self.tier2_collection]
        elif tier == MemoryTier.TIER_1_ACTIVE:
            collections = [self.tier1_collection]
        else:
            collections = [self.tier2_collection]
        
        # Search all relevant collections
        all_results = []
        for collection in collections:
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=limit,
                include=["documents", "metadatas", "distances", "embeddings"]
            )
            
            if results['ids'][0]:  # Check if we got results
                for i in range(len(results['ids'][0])):
                    # Convert distance to similarity score
                    distance = results['distances'][0][i]
                    similarity = 1.0 / (1.0 + distance)  # Convert distance to 0-1 similarity
                    
                    if similarity >= min_score:
                        # Reconstruct MemoryEntry
                        metadata_dict = results['metadatas'][0][i]
                        entry = MemoryEntry(
                            id=results['ids'][0][i],
                            content=results['documents'][0][i],
                            embedding=results['embeddings'][0][i] if 'embeddings' in results else None,
                            metadata=self._parse_metadata(metadata_dict)
                        )
                        all_results.append((entry, similarity))
        
        # Sort by similarity score
        all_results.sort(key=lambda x: x[1], reverse=True)
        
        # Return top results
        return all_results[:limit]
    
    def update_memory(self, memory_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update a memory entry
        
        Args:
            memory_id: Memory ID to update
            updates: Dictionary of fields to update
            
        Returns:
            Success status
        """
        # Try to find in both collections
        for collection in [self.tier1_collection, self.tier2_collection]:
            try:
                result = collection.get(ids=[memory_id])
                if result['ids']:
                    # Found it - update metadata
                    current_metadata = result['metadatas'][0]
                    current_metadata.update(updates)
                    
                    collection.update(
                        ids=[memory_id],
                        metadatas=[current_metadata]
                    )
                    return True
            except:
                continue
        
        return False
    
    def delete_memory(self, memory_id: str) -> bool:
        """Delete a memory from the store"""
        for collection in [self.tier1_collection, self.tier2_collection]:
            try:
                collection.delete(ids=[memory_id])
                return True
            except:
                continue
        return False
    
    def move_to_tier2(self, memory_id: str) -> bool:
        """
        Archive a memory by moving it from Tier 1 to Tier 2
        
        Args:
            memory_id: Memory ID to archive
            
        Returns:
            Success status
        """
        # Get from Tier 1
        result = self.tier1_collection.get(
            ids=[memory_id],
            include=["documents", "metadatas", "embeddings"]
        )
        
        if not result['ids']:
            return False  # Not found in Tier 1
        
        # Update tier in metadata
        metadata = result['metadatas'][0]
        metadata['tier'] = MemoryTier.TIER_2_PERSISTENT.value
        
        # Add to Tier 2
        self.tier2_collection.add(
            ids=result['ids'],
            embeddings=result['embeddings'],
            documents=result['documents'],
            metadatas=[metadata]
        )
        
        # Delete from Tier 1
        self.tier1_collection.delete(ids=[memory_id])
        
        return True
    
    def get_stats(self) -> Dict[str, Any]:
        """Get storage statistics"""
        tier1_count = self.tier1_collection.count()
        tier2_count = self.tier2_collection.count()
        
        return {
            "tier1_count": tier1_count,
            "tier2_count": tier2_count,
            "total_count": tier1_count + tier2_count,
            "storage_path": str(self.persist_directory)
        }
    
    def _parse_metadata(self, metadata_dict: Dict[str, Any]) -> MemoryMetadata:
        """Parse metadata from ChromaDB format"""
        from datetime import datetime
        
        metadata = MemoryMetadata()
        metadata.created_at = datetime.fromisoformat(metadata_dict.get('created_at', datetime.now().isoformat()))
        metadata.importance_score = metadata_dict.get('importance_score', 0.5)
        metadata.source = metadata_dict.get('source', 'unknown')
        metadata.tier = MemoryTier(metadata_dict.get('tier', MemoryTier.TIER_1_ACTIVE.value))
        
        # Parse JSON fields
        metadata.topics = json.loads(metadata_dict.get('topics', '[]'))
        metadata.tags = json.loads(metadata_dict.get('tags', '[]'))
        
        return metadata
    
    def reset(self):
        """Reset all collections (USE WITH CAUTION)"""
        self.client.delete_collection("tier1_active_memory")
        self.client.delete_collection("tier2_persistent_memory")
        
        self.tier1_collection = self.client.create_collection("tier1_active_memory")
        self.tier2_collection = self.client.create_collection("tier2_persistent_memory")
