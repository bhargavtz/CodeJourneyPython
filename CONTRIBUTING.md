# Contributing to CodeJourneyPython

Thank you for your interest in contributing to CodeJourneyPython! This document provides guidelines and instructions for contributing to the project.

## Project Overview

CodeJourneyPython is a comprehensive Python learning platform with:
- **Beginner Projects**: Simple Python fundamentals (Guess the Number)
- **AI/ML Projects**: Agents, data pipelines, and machine learning workflows
- **Web Projects**: REST APIs and full-stack applications
- **Library Tutorials**: NumPy, Pandas, ML, Data Visualization, Web Frameworks
- **Learning Resources**: Cheatsheets and curated references

## Development Setup

### Prerequisites
- Python 3.9+
- Git
- pip or conda

### Local Environment Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/bhargavtz/CodeJourneyPython.git
   cd CodeJourneyPython
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**:
   ```bash
   # Core development tools
   pip install -r requirements-dev.txt
   
   # For specific feature development
   pip install -r requirements-ml.txt      # For ML projects
   pip install -r requirements-agents.txt  # For AI agents
   pip install -r requirements-web.txt     # For web projects
   ```

4. **Setup pre-commit hooks**:
   ```bash
   pre-commit install
   pre-commit run --all-files  # Run on all files initially
   ```

5. **Verify setup**:
   ```bash
   python -m pytest projects/ -v
   ```

## Code Standards

### Style Guide

We follow **PEP 8** with additional standards:
- **Line length**: 100 characters max (configured in `.flake8` and `pyproject.toml`)
- **Formatter**: Black for automatic formatting
- **Import sorting**: isort for consistent imports
- **Linting**: flake8 for style checks
- **Type checking**: mypy for optional type validation

### Automatic Formatting

Before committing, code is automatically formatted:

```bash
# Manual formatting
black projects/
isort projects/
flake8 projects/

# Or let pre-commit handle it
git add .
git commit  # Pre-commit hooks run automatically
```

### Documentation Standards

Every function and module must have docstrings using **Google/NumPy style**:

```python
"""
Brief description of the module or function.

More detailed explanation if needed.

Attributes:
    attr1: Description of attribute

Example:
    Example usage of the function

Raises:
    ExceptionType: When this exception is raised
"""

def function_name(param1: str, param2: int) -> bool:
    """
    Brief description of what function does.
    
    Longer description with more details about behavior,
    side effects, and important constraints.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param validation fails
        TypeError: When param types are incorrect
        
    Example:
        >>> result = function_name("test", 42)
        >>> print(result)
        True
    """
    pass
```

### Type Hints

Use type hints for all function signatures:

```python
from typing import Optional, List, Dict, Tuple

def process_data(
    items: List[str],
    config: Optional[Dict[str, str]] = None
) -> Tuple[List[str], int]:
    """Process data items and return results."""
    pass
```

## Testing Requirements

### Coverage Targets

- **Minimum coverage**: 80% of new code
- **Target coverage**: 85%+
- **Critical functions**: 100% coverage

### Writing Tests

1. **Test location**: `projects/<project_name>/tests/test_<module>.py`
2. **Test class naming**: `Test<FeatureName>`
3. **Test method naming**: `test_<specific_behavior>`
4. **Use fixtures**: For repeated test setup

Example test file:

```python
import pytest
from projects.example.module import ExampleClass


class TestExampleClass:
    """Test suite for ExampleClass."""
    
    @pytest.fixture
    def instance(self):
        """Create test instance."""
        return ExampleClass(param="test")
    
    def test_basic_functionality(self, instance):
        """Test basic functionality."""
        result = instance.method()
        assert result is not None
    
    def test_error_handling(self, instance):
        """Test error handling."""
        with pytest.raises(ValueError):
            instance.method(invalid_param=True)
```

### Running Tests

```bash
# Run all tests
python -m pytest projects/ -v

# Run specific test file
python -m pytest projects/guess_the_number/tests/test_game.py -v

# Run with coverage report
python -m pytest projects/ --cov=projects --cov-report=html

# Run specific test class
python -m pytest projects/guess_the_number/tests/test_game.py::TestGuessTheNumberGame -v
```

## Project Structure

```
CodeJourneyPython/
├── projects/
│   ├── guess_the_number/       # Base Camp - Beginner project
│   │   ├── game.py
│   │   ├── tests/
│   │   └── README.md
│   ├── ai_agent_chatbot/       # River Crossing - AI Agents
│   ├── data_pipeline_etl/      # Mountain Peak - Data Engineering
│   ├── ml_recommendation/      # Skyline Explorer - ML
│   ├── web_api_service/        # Final Frontier - Full Stack
│   └── utils/                  # Shared utilities
├── libraries/
│   ├── Numpy/
│   ├── Pandas/
│   ├── MachineLearning/        # NEW
│   ├── AIAgents/               # NEW
│   └── DataVisualization/      # NEW
├── resources/
│   ├── cheatsheets/
│   └── README.md
└── tests/                      # Integration tests (future)
```

## Adding a New Project

1. **Create project directory**:
   ```bash
   mkdir projects/<project_name>
   cd projects/<project_name>
   touch __init__.py README.md
   mkdir tests
   touch tests/__init__.py
   ```

2. **Create README.md** with:
   - Project description
   - Learning objectives
   - How to run
   - Example usage
   - Key concepts covered

3. **Implement project code** with:
   - Full docstrings
   - Type hints
   - Proper error handling
   - Logging configuration

4. **Write tests**:
   - Create `tests/test_<module>.py`
   - Aim for 80%+ coverage
   - Include edge cases

5. **Update main README.md** to mention new project

Example project structure:
```
projects/example_project/
├── __init__.py
├── main.py            # Main entry point
├── module.py          # Core logic
├── config.py          # Configuration
├── README.md          # Documentation
└── tests/
    ├── __init__.py
    ├── test_main.py
    └── test_module.py
```

## Adding Library Tutorials

1. Create folder in `libraries/<library_name>/`
2. Create comprehensive README.md with:
   - Installation instructions
   - Basic concepts
   - Examples with output
   - Advanced topics
   - Common patterns
   - Resources for further learning

3. Optionally create Jupyter notebook:
   - Executable examples
   - Visualizations
   - Interactive exercises

## Git Workflow

### Branch Naming

```
feature/<feature-name>          # New features
fix/<bug-name>                  # Bug fixes
docs/<documentation-topic>      # Documentation
refactor/<component>            # Code refactoring
```

### Commit Messages

Follow conventional commits:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**: feat, fix, docs, style, refactor, test, chore  
**Scope**: project area affected  
**Subject**: 50 chars max, imperative mood

Example:
```
feat(guess_the_number): add difficulty levels

- Add easy/medium/hard modes with different ranges
- Implement difficulty selection at game start
- Update tests for difficulty modes

Closes #42
```

### Pull Request Process

1. **Create feature branch** from `main`
2. **Make changes** with clear commits
3. **Write/update tests** - must pass with 80%+ coverage
4. **Update documentation** - README, docstrings
5. **Submit PR** with:
   - Clear description of changes
   - Link to related issues
   - Test results and coverage
6. **Address reviews** and resolve discussions
7. **Merge** after approval

### Pre-commit Checklist

Before pushing, verify:

```bash
# Code formatting
black projects/
isort projects/

# Linting
flake8 projects/

# Type checking
mypy projects/

# Tests
pytest projects/ --cov=projects

# Commit message format
# Follows conventional commits
```

## Issues & Feature Requests

### Reporting Issues

Include:
- Python version
- Exact steps to reproduce
- Expected vs actual behavior
- Environment details
- Error messages/tracebacks

### Feature Requests

Include:
- Use case description
- Proposed solution
- Alternative approaches considered
- Estimated difficulty level

## Code Review Process

We review PRs for:
- ✅ Code quality and style
- ✅ Test coverage (80%+)
- ✅ Documentation completeness
- ✅ Performance implications
- ✅ Security concerns
- ✅ Backward compatibility

## Questions?

- Create a GitHub Discussion
- Check existing documentation
- Review similar projects in the repo
- Open an issue with the `question` label

## License

All contributions are licensed under the MIT License. See LICENSE file for details.

---

**Thank you for contributing to CodeJourneyPython!** 🎓
