# Contributing to Agentic AI Loan Approval System

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Focus on the code, not the person
- Help others learn and grow

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/agentic-loan-approval.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Commit with clear messages: `git commit -m "Add feature: description"`
6. Push to your fork: `git push origin feature/your-feature-name`
7. Create a Pull Request

## Development Setup

```bash
# Clone the repo
git clone https://github.com/yourusername/agentic-loan-approval.git
cd agentic-loan-approval

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/

# Start development servers
python3 fastapi_service.py &
streamlit run streamlit_app.py
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for functions and classes
- Keep lines under 100 characters
- Use meaningful variable names

## Commit Messages

Use clear, descriptive commit messages:
- `feat: Add new agent for X`
- `fix: Resolve issue with Y`
- `docs: Update README`
- `test: Add tests for Z`
- `refactor: Simplify X logic`

## Pull Request Process

1. Update README.md if needed
2. Add tests for new features
3. Ensure all tests pass
4. Request review from maintainers
5. Address feedback promptly

## Adding Features

### New Agent
1. Create agent class in `agents.py`
2. Implement analysis method
3. Add tests
4. Document responsibilities
5. Update README

### API Endpoint
1. Add endpoint in `fastapi_service.py`
2. Define request/response models
3. Add error handling
4. Test with curl or Postman
5. Document in README

### UI Component
1. Add to `streamlit_app.py`
2. Test user interactions
3. Add styling if needed
4. Document features

## Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_agents.py

# Run with coverage
pytest --cov=.
```

## Documentation

- Update README for user-facing changes
- Add docstrings to code
- Include examples for APIs
- Document architecture decisions

## Reporting Issues

Include:
- Clear description
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python version, etc.)

## Questions?

- Open a GitHub issue
- Check existing documentation
- Review closed issues for answers

Thank you for contributing! 🎉
