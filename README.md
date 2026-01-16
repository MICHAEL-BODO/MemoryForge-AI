# MemoryForge-AI 🧠⚡

**Next-Generation Hybrid Memory Architecture for AI Assistants**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Alpha](https://img.shields.io/badge/status-alpha-orange.svg)]()

## 🎯 Overview

MemoryForge-AI is an advanced memory enhancement system that transforms Claude AI's capabilities through intelligent, persistent memory architecture. It implements a sophisticated two-tier memory system, autonomous knowledge graph refinement, and natural language memory management.

## ✨ Key Features

### 🏗️ Hybrid Memory Architecture (Phase 1)
- **Tier 1**: Fast in-context memory for active conversations (~8K tokens)
- **Tier 2**: Unlimited persistent disk storage with semantic search
- **Intelligent Archival**: Automatic transitions based on age, importance, and token pressure
- **Semantic Retrieval**: Vector-based search using sentence-transformers

### 📥 Content Ingestion Systems (Phase 3)
- **File Indexing Pipeline**: Real-time monitoring and indexing of local files
- **Multi-Format Support**: PDF, DOCX, XLSX, code files, markdown, and more
- **Google Drive Integration**: Seamless sync and semantic search across Drive
- **Incremental Updates**: Efficient change detection and re-indexing

### 🧩 Knowledge Graph Refinement
- **Autonomous Analysis**: Background agent identifies inconsistencies
- **Duplicate Detection**: Semantic similarity-based merging
- **Relationship Suggestions**: Automatic knowledge graph enhancement
- **Health Monitoring**: Continuous quality metrics and optimization

### 🗣️ Natural Language Memory Interface
- **Conversational API**: "Remember this", "Forget about X", "What do you recall..."
- **Intent Classification**: Intelligent parsing of memory operations
- **Safe Deletions**: Confirmation flows for destructive operations

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- 4GB+ RAM recommended
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/MemoryForge-AI.git
cd MemoryForge-AI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
from phase1_hybrid_memory.vector_store import VectorStore
from phase1_hybrid_memory.memory_models import MemoryEntry

# Initialize vector store
store = VectorStore(persist_directory="./my_memory")

# Create and store a memory
entry = MemoryEntry(content="Important project meeting notes...")
memory_id = store.add_memory(entry)

# Search memories
results = store.search("project meeting", limit=5)
for memory, score in results:
    print(f"[{score:.2f}] {memory.content[:100]}")
```

## 📁 Project Structure

```
MemoryForge-AI/
├── phase1_hybrid_memory/      # Core memory architecture
│   ├── memory_models.py        # Data structures & interfaces
│   ├── embedding_generator.py  # Text-to-vector conversion
│   ├── vector_store.py         # ChromaDB integration
│   └── archival_pipeline.py    # Tier 1 → Tier 2 transitions
├── phase3-content-ingestion/  # File indexing & Drive sync
├── knowledge-graph-refinement/ # Autonomous graph maintenance
├── nl-memory-interface/        # Natural language API
├── docs/                       # Technical documentation
└── tests/                      # Test suite
```

## 📚 Documentation

- **[Technical Specification](docs/TECHNICAL_SPEC.md)** - Architecture deep dive
- **[AI Agent Guide](docs/AI_AGENT_GUIDE.md)** - For Codex/Cline/Roo integration
- **[Development Guide](docs/DEVELOPMENT.md)** - Setup and contribution guidelines
- **[Project Status](STATUS.md)** - Current implementation progress
- **[Changelog](CHANGELOG.md)** - Version history

## 🎯 Roadmap

### Phase 1: Hybrid Memory Architecture ✅ In Progress
- [x] Core data models
- [x] Embedding generation
- [x] Vector storage (ChromaDB)
- [ ] Archival pipeline
- [ ] MCP server integration

### Phase 3: Content Ingestion Systems 🏗️ In Progress
- [ ] File system watcher
- [ ] Multi-format extractors
- [ ] Google Drive sync
- [ ] Semantic search API

### Future Enhancements 💡
- Multi-modal memory (vision + text)
- Predictive context pre-loading
- Federated learning across instances
- Mobile app integration

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- Built for Claude AI by Anthropic
- Powered by sentence-transformers and ChromaDB
- Inspired by the need for persistent, intelligent memory

---

**Status**: Alpha Development | **Version**: 0.1.0 | **Last Updated**: January 2026
