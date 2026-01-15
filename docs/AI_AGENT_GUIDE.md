# AI Agent Guide - MemoryForge-AI

**Quick Reference for Codex, Cline, Roo, and other AI coding assistants**

## 🎯 Project Mission

Build a production-grade hybrid memory system for Claude AI with:
1. Two-tier architecture (fast in-context + persistent disk)
2. Semantic search using embeddings
3. Autonomous knowledge graph refinement
4. Natural language memory management

## 🏗️ Architecture Overview

### Core Components

**Phase 1: Hybrid Memory** (`phase1-hybrid-memory/`)
- `memory_models.py` - Data structures (MemoryEntry, MemoryTier, ArchivalTrigger)
- `embedding_generator.py` - Sentence transformers wrapper with caching
- `vector_store.py` - ChromaDB integration for semantic search
- `archival_pipeline.py` - Tier 1→2 transition logic (IN PROGRESS)

**Phase 3: Content Ingestion** (`phase3-content-ingestion/`)
- File watcher using `watchdog` library
- Content extractors for PDF, DOCX, XLSX, code files
- Google Drive API integration
- Semantic indexing pipeline

**Knowledge Graph Refinement** (`knowledge-graph-refinement/`)
- Graph analysis algorithms
- Duplicate detection and merging
- Relationship suggestion engine
- Background scheduler for continuous refinement

**NL Memory Interface** (`nl-memory-interface/`)
- Intent classification (remember/recall/forget/archive)
- Query parsing with entity extraction
- Natural language response generation
- Confirmation flows for destructive ops

## 🔧 Key Design Patterns

### 1. Lazy Loading
Embedding models are loaded only when first needed:
```python
def _ensure_loaded(self):
    if self.model is None:
        self.model = SentenceTransformer(self.model_name)
```

### 2. Caching Strategy
Embeddings are cached by content hash to avoid regeneration:
```python
cache_key = hashlib.md5(text.encode()).hexdigest()
if cache_key in self._embedding_cache:
    return self._embedding_cache[cache_key]
```

### 3. Abstract Interfaces
All memory operations use `MemoryInterface` ABC for flexibility:
```python
class MemoryInterface(ABC):
    @abstractmethod
    async def store(self, entry: MemoryEntry) -> str: pass
```

### 4. Dataclasses for Models
Using Python dataclasses for clean data structures:
```python
@dataclass
class MemoryEntry:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    content: str = ""
    metadata: MemoryMetadata = field(default_factory=MemoryMetadata)
```

## 📝 Coding Conventions

### Style Guide
- **PEP 8** compliant (use `black` for formatting)
- **Type hints** on all function signatures
- **Docstrings** for all classes and public methods (Google style)
- **Async/await** for I/O operations

### Naming Conventions
- Classes: `PascalCase` (e.g., `MemoryEntry`)
- Functions: `snake_case` (e.g., `generate_embedding`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `TOKEN_LIMIT`)
- Private methods: `_leading_underscore` (e.g., `_ensure_loaded`)

### File Organization
```
module_name/
├── __init__.py           # Public API exports
├── models.py             # Data structures
├── core.py               # Main logic
├── utils.py              # Helper functions
└── tests/
    └── test_module.py    # Unit tests
```

## 🔍 Where to Find Things

### Adding New Memory Types
1. Extend `MemoryEntry` in `memory_models.py`
2. Update `to_dict()` serialization
3. Modify `vector_store.py` to handle new fields

### Implementing New Content Extractors
1. Create extractor in `phase3-content-ingestion/extractors/`
2. Implement `extract(file_path: str) -> str` interface
3. Register in `content_extractors.py` dispatcher

### Adding MCP Server Tools
1. Define tool in appropriate MCP server file
2. Use FastMCP decorators: `@mcp.tool()`
3. Add input validation with Pydantic models
4. Update tool documentation

## 🧪 Testing Strategy

### Unit Tests
```python
import pytest
from phase1_hybrid_memory.embedding_generator import EmbeddingGenerator

def test_embedding_generation():
    gen = EmbeddingGenerator()
    embedding = gen.generate("test text")
    assert len(embedding) == 384  # MiniLM dimension
```

### Integration Tests
```python
@pytest.mark.asyncio
async def test_archival_pipeline():
    store = VectorStore(":memory:")
    entry = MemoryEntry(content="test")
    await store.store(entry)
    # Test archival...
```

### Run Tests
```bash
pytest tests/ -v
pytest tests/ --cov=phase1_hybrid_memory  # With coverage
```

## 🚀 Common Development Tasks

### Adding a New Feature
1. Check `TODO.md` for planned work
2. Create feature branch: `git checkout -b feature/your-feature`
3. Implement with tests
4. Update documentation
5. Submit PR with clear description

### Debugging Memory Issues
```python
# Get health statistics
stats = vector_store.get_stats()
print(f"Tier 1: {stats['tier1_count']} entries")
print(f"Tier 2: {stats['tier2_count']} entries")

# Check embedding cache
gen = get_embedding_generator()
print(f"Cache size: {len(gen._embedding_cache)}")
```

### Performance Optimization
- Use batch operations for bulk inserts
- Enable embedding caching for repeated queries
- Monitor ChromaDB collection sizes
- Profile with `cProfile` for bottlenecks

## 📦 Dependencies Explained

### Core ML
- `sentence-transformers` - Text embedding generation
- `torch` - PyTorch backend for transformers
- `transformers` - HuggingFace model library

### Vector Storage
- `chromadb` - Vector database for semantic search
- `faiss-cpu` - Alternative vector index (optional)

### Content Processing
- `PyPDF2` - PDF text extraction
- `python-docx` - Word document parsing
- `openpyxl` - Excel file reading
- `watchdog` - File system event monitoring

### Integration
- `fastmcp` - MCP server framework
- `google-api-python-client` - Google Drive API
- `PyGithub` - GitHub API wrapper

## 🐛 Known Issues & Gotchas

### ChromaDB Persistence
- Always specify `persist_directory` to avoid in-memory DB
- Call `client.persist()` after bulk operations (optional, auto-persists)

### Embedding Model Loading
- First call loads model (~90MB download)
- Use `_ensure_loaded()` pattern to avoid blocking

### Async Operations
- Most MCP tools are async, use `await`
- Don't mix sync/async code without `asyncio.run()`

## 💡 Implementation Tips

### For Archival Pipeline
- Implement importance scoring based on: access frequency, recency, user tags
- Use exponential backoff for archival to avoid thrashing
- Compress content but preserve key facts

### For Content Extractors
- Handle encoding errors gracefully
- Cache extracted content with file hash
- Support incremental updates (only reprocess changed files)

### For Knowledge Graph
- Use NetworkX for graph operations
- Store graph in SQLite alongside ChromaDB
- Implement transactional updates for consistency

## 📞 Getting Help

1. Check `STATUS.md` for current state
2. Review `TECHNICAL_SPEC.md` for architecture details
3. Look at existing implementations as examples
4. Create an issue on GitHub with `[AI Agent]` tag

---

**Remember**: This is a production-quality system. Write clean, tested, documented code! 🚀
