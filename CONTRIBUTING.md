# Contributing to MemoryForge-AI

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 🤝 How to Contribute

### Reporting Issues
- Check existing issues before creating new ones
- Use issue templates when available
- Provide detailed reproduction steps for bugs
- Include system information (OS, Python version)

### Suggesting Features
- Open an issue with `[Feature Request]` tag
- Explain the use case and expected behavior
- Consider implementation complexity

### Submitting Code

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Write clean, tested code** following our style guide
4. **Update documentation** as needed
5. **Commit with clear messages**: `git commit -m "Add: feature description"`
6. **Push to your fork**: `git push origin feature/your-feature-name`
7. **Open a Pull Request** with detailed description

## 📝 Code Style

### Python Style Guide
- Follow **PEP 8**
- Use **type hints** on all function signatures
- Write **docstrings** for classes and public methods (Google style)
- Format with **black**: `black .`
- Lint with **flake8**: `flake8 .`
- Type check with **mypy**: `mypy .`

### Example
```python
from typing import List, Optional

def process_memory(content: str, importance: float = 0.5) -> Optional[str]:
    """
    Process memory content for storage.
    
    Args:
        content: The memory text to process
        importance: Importance score (0.0 to 1.0)
        
    Returns:
        Processed content or None if invalid
    """
    if not content.strip():
        return None
    return content.strip()
```

## 🧪 Testing

### Writing Tests
- Place tests in `tests/` directory
- Name test files `test_*.py`
- Use pytest fixtures for setup
- Aim for >80% code coverage

### Running Tests
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=phase1_hybrid_memory --cov-report=html

# Run specific test
pytest tests/test_embedding_generator.py -v
```

## 📚 Documentation

- Update README.md for user-facing changes
- Update AI_AGENT_GUIDE.md for architectural changes
- Add docstrings to new functions/classes
- Update CHANGELOG.md following Keep a Changelog format

## 🔄 Commit Message Format

```
Type: Brief description (max 50 chars)

Detailed explanation of the change (if needed).
Can span multiple lines.

Fixes #123
```

**Types**:
- `Add:` New feature or functionality
- `Fix:` Bug fix
- `Update:` Modification to existing feature
- `Refactor:` Code restructuring without behavior change
- `Docs:` Documentation only
- `Test:` Adding or updating tests
- `Chore:` Maintenance tasks

## ⚡ Pull Request Guidelines

### Before Submitting
- [ ] Code follows style guide
- [ ] Tests pass locally
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] No merge conflicts

### PR Description Should Include
- Summary of changes
- Motivation and context
- Screenshots (if UI changes)
- Related issues

## 🚫 What NOT to Do

- Don't commit secrets or credentials
- Don't commit large binary files
- Don't break existing tests
- Don't submit PRs without description
- Don't mix unrelated changes in one PR

## 📞 Getting Help

- Check the AI_AGENT_GUIDE.md for implementation details
- Review STATUS.md for current priorities
- Open an issue with `[Question]` tag
- Join discussions in existing issues

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to MemoryForge-AI! 🚀
