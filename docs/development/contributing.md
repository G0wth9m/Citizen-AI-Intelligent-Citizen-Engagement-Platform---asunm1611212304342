# Contributing to CitizenAI

We welcome contributions to CitizenAI! This guide will help you get started with contributing to the project.

## Getting Started

### Prerequisites

Before contributing, ensure you have:

- Python 3.11 or higher
- Git installed and configured
- A GitHub account
- Basic knowledge of Flask and web development

### Development Setup

1. **Fork the Repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/Citizen-AI.git
   cd Citizen-AI
   ```

2. **Set Up Development Environment**
   ```bash
   # Create virtual environment
   python -m venv .venv
   
   # Activate virtual environment
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. **Configure Environment**
   ```bash
   # Copy example environment file
   cp .env.example .env
   
   # Edit .env with your settings
   # At minimum, set FLASK_DEBUG=True
   ```

4. **Run Tests**
   ```bash
   # Run the test suite
   python -m pytest tests/
   
   # Run with coverage
   python -m pytest --cov=src tests/
   ```

## Development Workflow

### Branch Strategy

We use a simplified Git flow:

- **`main`**: Production-ready code
- **`develop`**: Integration branch for features
- **`feature/*`**: Feature development branches
- **`bugfix/*`**: Bug fix branches
- **`hotfix/*`**: Critical production fixes

### Creating a Feature

```bash
# Create and switch to feature branch
git checkout -b feature/your-feature-name develop

# Make your changes
# ... code, test, commit ...

# Push to your fork
git push origin feature/your-feature-name

# Create pull request on GitHub
```

### Commit Messages

Follow conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

**Examples:**
```bash
feat(chat): add sentiment analysis to chat responses
fix(auth): resolve session timeout issue
docs(api): update authentication documentation
test(concerns): add unit tests for concern validation
```

**Types:**
- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

## Code Standards

### Python Style Guide

We follow PEP 8 with some project-specific conventions:

```python
# Use type hints
def process_message(message: str, user_id: int) -> dict:
    """Process a chat message and return response."""
    return {"response": "Processed"}

# Use docstrings for all functions and classes
class ChatEngine:
    """Handles AI chat interactions."""
    
    def __init__(self, api_key: str) -> None:
        """Initialize chat engine with API key."""
        self.api_key = api_key
```

### Code Formatting

We use Black for code formatting:

```bash
# Format code
black src/ tests/

# Check formatting
black --check src/ tests/
```

### Linting

We use flake8 for linting:

```bash
# Run linter
flake8 src/ tests/

# Configuration in setup.cfg
[flake8]
max-line-length = 88
extend-ignore = E203, W503
```

### Import Organization

Use isort for import organization:

```bash
# Sort imports
isort src/ tests/

# Configuration in setup.cfg
[isort]
profile = black
multi_line_output = 3
```

## Testing Guidelines

### Test Structure

```
tests/
├── unit/           # Unit tests
├── integration/    # Integration tests
├── fixtures/       # Test data and fixtures
└── conftest.py     # Pytest configuration
```

### Writing Tests

```python
import pytest
from src.chat.engine import ChatEngine

class TestChatEngine:
    """Test suite for ChatEngine."""
    
    @pytest.fixture
    def chat_engine(self):
        """Create ChatEngine instance for testing."""
        return ChatEngine(api_key="test-key")
    
    def test_process_message(self, chat_engine):
        """Test message processing."""
        result = chat_engine.process_message("Hello")
        assert result["success"] is True
        assert "response" in result
    
    @pytest.mark.parametrize("message,expected", [
        ("hello", True),
        ("", False),
        (None, False),
    ])
    def test_message_validation(self, chat_engine, message, expected):
        """Test message validation with various inputs."""
        result = chat_engine.validate_message(message)
        assert result == expected
```

### Test Coverage

Maintain high test coverage:

```bash
# Run tests with coverage
pytest --cov=src --cov-report=html tests/

# View coverage report
open htmlcov/index.html
```

**Coverage Requirements:**
- Minimum 80% overall coverage
- 100% coverage for critical paths
- New features must include tests

## Documentation

### Code Documentation

```python
def analyze_sentiment(text: str) -> dict:
    """
    Analyze sentiment of given text.
    
    Args:
        text: The text to analyze for sentiment
        
    Returns:
        Dictionary containing sentiment analysis results:
        {
            "sentiment": "positive" | "negative" | "neutral",
            "confidence": float,  # 0.0 to 1.0
            "scores": {
                "positive": float,
                "negative": float,
                "neutral": float
            }
        }
        
    Raises:
        ValueError: If text is empty or None
        APIError: If sentiment analysis service fails
        
    Example:
        >>> analyze_sentiment("I love this service!")
        {
            "sentiment": "positive",
            "confidence": 0.95,
            "scores": {"positive": 0.95, "negative": 0.02, "neutral": 0.03}
        }
    """
```

### API Documentation

Use docstrings for API endpoints:

```python
@app.route('/api/v1/chat/message', methods=['POST'])
def send_chat_message():
    """
    Send a chat message and get AI response.
    
    Request Body:
        {
            "message": str,     # Required: The user's message
            "session_id": str,  # Optional: Session identifier
            "context": dict     # Optional: Additional context
        }
    
    Returns:
        {
            "success": bool,
            "data": {
                "response": str,      # AI response
                "confidence": float,  # Response confidence (0-1)
                "intent": str,        # Detected intent
                "session_id": str     # Session identifier
            }
        }
    
    Status Codes:
        200: Success
        400: Invalid request
        401: Authentication required
        429: Rate limit exceeded
        500: Server error
    """
```

## Pull Request Process

### Before Submitting

1. **Ensure tests pass**
   ```bash
   pytest tests/
   ```

2. **Check code quality**
   ```bash
   black --check src/ tests/
   flake8 src/ tests/
   isort --check-only src/ tests/
   ```

3. **Update documentation**
   - Update relevant documentation files
   - Add docstrings to new functions/classes
   - Update CHANGELOG.md if applicable

4. **Test manually**
   - Test your changes in the demo environment
   - Verify UI/UX changes work as expected

### Pull Request Template

```markdown
## Description
Brief description of the changes made.

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that causes existing functionality to change)
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Code is commented, particularly complex areas
- [ ] Documentation updated
- [ ] No new warnings introduced
```

### Review Process

1. **Automated Checks**
   - CI/CD pipeline runs tests
   - Code quality checks
   - Security scanning

2. **Manual Review**
   - Code review by maintainers
   - Functionality verification
   - Documentation review

3. **Approval and Merge**
   - Requires approval from at least one maintainer
   - All checks must pass
   - Squash and merge to maintain clean history

## Development Environment

### Recommended Tools

**IDEs:**
- Visual Studio Code with Python extension
- PyCharm Professional/Community
- Vim/Neovim with Python plugins

**Extensions for VS Code:**
- Python
- Black Formatter
- Flake8
- GitLens
- REST Client

### Environment Configuration

```json title=".vscode/settings.json"
{
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.testing.pytestEnabled": true,
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

### Debug Configuration

```json title=".vscode/launch.json"
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Flask App",
            "type": "python",
            "request": "launch",
            "program": "app_demo.py",
            "env": {
                "FLASK_ENV": "development",
                "FLASK_DEBUG": "1"
            },
            "console": "integratedTerminal"
        }
    ]
}
```

## Issue Reporting

### Bug Reports

Use the bug report template:

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
- OS: [e.g. Windows 10]
- Browser: [e.g. Chrome 96]
- Python version: [e.g. 3.11.0]
- CitizenAI version: [e.g. 1.0.0]

**Additional context**
Any other context about the problem.
```

### Feature Requests

Use the feature request template:

```markdown
**Is your feature request related to a problem?**
A clear description of what the problem is.

**Describe the solution you'd like**
A clear description of what you want to happen.

**Describe alternatives you've considered**
Alternative solutions or features you've considered.

**Additional context**
Any other context or screenshots about the feature request.
```

## Community Guidelines

### Code of Conduct

We follow the [Contributor Covenant](https://www.contributor-covenant.org/):

- **Be respectful**: Treat all community members with respect
- **Be inclusive**: Welcome newcomers and diverse perspectives
- **Be collaborative**: Work together towards common goals
- **Be constructive**: Provide helpful feedback and suggestions

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General discussions and questions
- **Pull Requests**: Code review and collaboration

## Release Process

### Versioning

We use [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

1. Update version numbers
2. Update CHANGELOG.md
3. Run full test suite
4. Create release branch
5. Tag release
6. Deploy to staging
7. Validate staging deployment
8. Deploy to production
9. Create GitHub release

## Getting Help

If you need help with contributing:

1. **Check Documentation**: Review existing documentation
2. **Search Issues**: Look for similar questions or problems
3. **Ask Questions**: Create a GitHub Discussion
4. **Join Community**: Participate in project discussions

## Recognition

Contributors are recognized in:

- **CONTRIBUTORS.md**: List of all contributors
- **Release Notes**: Major contributions highlighted
- **GitHub**: Contributor graphs and statistics

Thank you for contributing to CitizenAI! 🚀
