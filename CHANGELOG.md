# Changelog - MemoryForge-AI

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Complete archival pipeline implementation
- MCP server integration for Phase 1
- File system watcher for Phase 3
- Content extractors for major file types
- Knowledge graph refinement agent
- Natural language memory interface

---

## [0.1.0] - 2026-01-16

### 🎉 Initial Release - Alpha

**Project Inception**: MemoryForge-AI created to enhance Claude AI with persistent, intelligent memory capabilities.

### ✨ Added

#### Phase 1: Hybrid Memory Architecture
- **Core Data Models** (`memory_models.py`)
  - `MemoryEntry` dataclass for storing memory content
  - `MemoryMetadata` with timestamps, importance scores, topics, tags
  - `MemoryTier` enum (Tier 1 active, Tier 2 persistent)
  - `ArchivalTrigger` conditions for automatic archival
  - `MemoryHealth` metrics for system monitoring
  - `MemoryInterface` abstract base class

- **Embedding Generator** (`embedding_generator.py`)
  - Sentence-transformers integration
  - Support for multiple models (MiniLM, MPNet)
  - Intelligent caching system with MD5 hashing
  - Batch processing for efficiency
  - Cosine similarity calculations
  - Lazy model loading (90MB download on first use)
  - Global singleton pattern for memory efficiency

- **Vector Store** (`vector_store.py`)
  - ChromaDB persistent storage integration
  - Dual collection architecture (Tier 1 & Tier 2)
  - Semantic search with similarity thresholds
  - Full CRUD operations
  - Tier migration functionality
  - Storage statistics and health checks
  - Metadata serialization/deserialization

- **Archival Pipeline** (`archival_pipeline.py` - partial)
  - `MemoryCompressor` class structure
  - Foundation for extractive summarization

#### Infrastructure
- **Project Structure**
  - Organized directory layout for all phases
  - Separation of concerns between components
  
- **Dependencies** (`requirements.txt`)
  - Core ML: sentence-transformers, torch, transformers
  - Vector storage: chromadb, faiss-cpu
  - MCP integration: fastmcp, pydantic
  - Content extraction: PyPDF2, python-docx, openpyxl
  - Cloud APIs: google-api-python-client, PyGithub
  - Development: pytest, black, flake8, mypy

- **Documentation**
  - Comprehensive README with quick start guide
  - AI Agent Guide for Codex/Cline/Roo integration
  - Technical specification document
  - Project status tracking
  - Master TODO with detailed task breakdown

#### Development Tools
- Git repository initialization
- Requirements management
- Documentation structure

### 🔄 Changed
- N/A (initial release)

### 🐛 Fixed
- N/A (initial release)

### 🔒 Security
- No security vulnerabilities in initial codebase
- All dependencies from trusted sources

### 📝 Notes

**Key Architectural Decisions**:
1. **Two-Tier Memory**: Separating fast in-context from persistent storage allows optimal performance
2. **ChromaDB**: Chosen for persistent vector storage with excellent Python integration
3. **Sentence-Transformers**: Best balance of quality and speed for embeddings
4. **Async-First**: Designed for async/await to support non-blocking operations
5. **MCP Integration**: Future-proof architecture for Claude integration

**Implementation Highlights**:
- ~800 lines of production-quality Python code
- Type hints throughout for IDE support
- Dataclasses for clean data modeling
- Abstract interfaces for extensibility
- Caching strategies for performance

**What's Working**:
- ✅ Embedding generation with caching
- ✅ Vector storage and retrieval
- ✅ Semantic search across memories
- ✅ Tier-based organization
- ✅ Health monitoring

**What's Next**:
- 🏗️ Complete archival automation
- 🏗️ MCP server tools
- 🏗️ File indexing pipeline
- 🏗️ Google Drive integration

---

## Version History

- **0.1.0** (2026-01-16) - Initial alpha release

---

**Versioning Strategy**:
- **Major** (X.0.0): Breaking API changes
- **Minor** (0.X.0): New features, backwards compatible
- **Patch** (0.0.X): Bug fixes, documentation updates

**Current Focus**: Building out Phase 1 and Phase 3 in parallel, with emphasis on production-ready code quality.
