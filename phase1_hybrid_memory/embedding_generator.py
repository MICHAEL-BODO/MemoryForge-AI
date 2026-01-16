"""
Embedding Generation System
Handles text-to-vector conversion for semantic search
"""

from sentence_transformers import SentenceTransformer
from typing import List, Union, Optional
import numpy as np
from functools import lru_cache
import hashlib


class EmbeddingGenerator:
    """Generate embeddings for text using sentence-transformers"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize embedding generator
        
        Args:
            model_name: Name of sentence-transformer model
                - all-MiniLM-L6-v2: Fast, good for most use cases (384 dims)
                - all-mpnet-base-v2: Higher quality (768 dims)
                - multi-qa-MiniLM-L6-cos-v1: Optimized for Q&A
        """
        self.model_name = model_name
        self.model = None
        self._embedding_cache = {}
        
    def _ensure_loaded(self):
        """Lazy load the model"""
        if self.model is None:
            print(f"Loading embedding model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            print(f"Model loaded. Embedding dimension: {self.model.get_sentence_embedding_dimension()}")
    
    def generate(self, text: Union[str, List[str]], use_cache: bool = True) -> Union[List[float], List[List[float]]]:
        """
        Generate embeddings for text
        
        Args:
            text: Single string or list of strings
            use_cache: Whether to use caching for repeated text
            
        Returns:
            Embedding vector(s) as list of floats
        """
        self._ensure_loaded()
        
        is_single = isinstance(text, str)
        texts = [text] if is_single else text
        
        # Check cache
        if use_cache:
            cached_results = []
            uncached_texts = []
            uncached_indices = []
            
            for i, t in enumerate(texts):
                cache_key = self._get_cache_key(t)
                if cache_key in self._embedding_cache:
                    cached_results.append((i, self._embedding_cache[cache_key]))
                else:
                    uncached_texts.append(t)
                    uncached_indices.append(i)
            
            # Generate embeddings for uncached texts
            if uncached_texts:
                new_embeddings = self.model.encode(uncached_texts, convert_to_numpy=True)
                
                # Cache new embeddings
                for text, emb in zip(uncached_texts, new_embeddings):
                    cache_key = self._get_cache_key(text)
                    self._embedding_cache[cache_key] = emb.tolist()
                
                # Combine cached and new results
                all_results = {}
                for i, emb in cached_results:
                    all_results[i] = emb
                for i, emb in zip(uncached_indices, new_embeddings):
                    all_results[i] = emb.tolist()
                
                # Sort by original index
                result = [all_results[i] for i in range(len(texts))]
            else:
                # All cached
                result = [emb for _, emb in sorted(cached_results)]
        else:
            # No caching
            embeddings = self.model.encode(texts, convert_to_numpy=True)
            result = [emb.tolist() for emb in embeddings]
        
        return result[0] if is_single else result
    
    def _get_cache_key(self, text: str) -> str:
        """Generate cache key for text"""
        return hashlib.md5(text.encode()).hexdigest()
    
    def batch_generate(self, texts: List[str], batch_size: int = 32) -> List[List[float]]:
        """
        Generate embeddings in batches for efficiency
        
        Args:
            texts: List of texts
            batch_size: Batch size for processing
            
        Returns:
            List of embedding vectors
        """
        self._ensure_loaded()
        
        all_embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            embeddings = self.model.encode(batch, convert_to_numpy=True, show_progress_bar=False)
            all_embeddings.extend([emb.tolist() for emb in embeddings])
        
        return all_embeddings
    
    def similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        Calculate cosine similarity between two embeddings
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Similarity score (0 to 1)
        """
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)
        
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return float(dot_product / (norm1 * norm2))
    
    def clear_cache(self):
        """Clear embedding cache"""
        self._embedding_cache.clear()
    
    def get_dimension(self) -> int:
        """Get embedding dimension"""
        self._ensure_loaded()
        return self.model.get_sentence_embedding_dimension()


# Global singleton instance
_global_generator: Optional[EmbeddingGenerator] = None


def get_embedding_generator(model_name: str = "all-MiniLM-L6-v2") -> EmbeddingGenerator:
    """Get or create global embedding generator"""
    global _global_generator
    if _global_generator is None or _global_generator.model_name != model_name:
        _global_generator = EmbeddingGenerator(model_name)
    return _global_generator
