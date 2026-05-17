# Contributing to OncoReconcile AI

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. All contributors are expected to:
- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person

## How to Contribute

### 1. Report Issues

If you find a bug or have a feature request:
1. Check existing issues to avoid duplicates
2. Create a clear, descriptive issue with:
   - Expected vs. actual behavior
   - Steps to reproduce (for bugs)
   - Environment details (OS, Python version, etc.)

### 2. Submit Pull Requests

1. **Fork** the repository
2. **Create a feature branch**: `git checkout -b feature/my-feature`
3. **Make changes** with clear, atomic commits
4. **Add tests** for new functionality
5. **Run tests** locally: `pytest tests/`
6. **Submit PR** with description of changes

### 3. Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/oncoreconcile-ai.git
cd oncoreconcile-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dev dependencies
pip install -r requirements.txt
pip install pytest pytest-cov black flake8

# Run tests
pytest tests/

# Run linter
flake8 src/

# Format code
black src/
```

## Code Style

- **Python**: Follow PEP 8
- **Type hints**: All functions should include type hints
- **Docstrings**: Use Google-style docstrings
- **Comments**: Explain "why", not "what"

### Example Function

```python
def reconcile_variant(
    raw_variant: str,
    source: str = "external",
) -> ReconciliationJob:
    """
    Reconcile a raw variant to canonical form.
    
    This function executes the full multi-agent workflow,
    from extraction through confidence scoring and review queue assignment.
    
    Args:
        raw_variant: Raw variant string (e.g., "EGFR Ex19del")
        source: Source of the variant
        
    Returns:
        ReconciliationJob with complete audit trail
        
    Raises:
        ValueError: If raw_variant is empty
    """
    # Implementation here
    pass
```

## Testing Requirements

- **Unit tests**: Test individual functions
- **Integration tests**: Test agent interactions
- **Coverage**: Aim for >80% code coverage

```bash
# Run tests with coverage
pytest tests/ --cov=src --cov-report=html
```

## Documentation

- Update `README.md` for major changes
- Add docstrings to all public functions
- Update architecture docs for design changes
- Include examples for new features

## Commit Messages

Write clear commit messages:

```
Brief summary (50 chars max)

Detailed explanation (wrap at 72 chars):
- Why the change is necessary
- How it addresses the problem
- Any side effects or considerations

Fixes #123
```

## Release Process

1. Update version in `src/__init__.py`
2. Update `CHANGELOG.md` (create if doesn't exist)
3. Update `README.md` with new features
4. Create Git tag: `git tag v0.2.0`
5. Push tag: `git push origin v0.2.0`

## Questions?

- Open a discussion on GitHub
- Email the maintainers
- Join our community Slack/Discord (when established)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to OncoReconcile AI!** 🙏
