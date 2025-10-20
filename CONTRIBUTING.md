# Contributing to Universal Command Wrapper (UCW)

Thank you for your interest in contributing to UCW! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Contributing Guidelines](#contributing-guidelines)
- [Code Style](#code-style)
- [Testing](#testing)
- [Documentation](#documentation)
- [Release Process](#release-process)
- [Community](#community)

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). By participating, you are expected to uphold this code.

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

Examples of behavior that contributes to creating a positive environment include:

- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Text editor or IDE with Python support
- SMCP (Simple MCP) for plugin integration (optional for standalone development)
- Basic understanding of command-line tools and MCP protocols

### Development Setup

1. **Fork the Repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/ucw.git
   cd ucw
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   # Install development dependencies
   pip install -r requirements.txt
   
   # For SMCP plugin integration (optional)
   # cp -r ucw /path/to/smcp/plugins/
   ```

4. **Verify Installation**
   ```bash
   # Run tests
   python tests/test_basic.py
   
   # Test CLI
   ucw wrap ls
   ```

### Development Tools

```bash
# Install additional tools
pip install black flake8 mypy pytest

# Format code
black ucw/

# Lint code
flake8 ucw/

# Type checking
mypy ucw/

# Run tests
pytest tests/
```

## Development Process

### Branch Strategy

- **main**: Stable, production-ready code
- **develop**: Integration branch for features
- **feature/***: Feature development branches
- **bugfix/***: Bug fix branches
- **hotfix/***: Critical bug fixes

### Workflow

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Write code following our style guidelines
   - Add tests for new functionality
   - Update documentation as needed

3. **Test Changes**
   ```bash
   # Run tests
   python tests/test_basic.py
   
   # Test specific functionality
   python -c "from ucw import UniversalCommandWrapper; ucw = UniversalCommandWrapper(); print('OK')"
   ```

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

5. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   # Create pull request on GitHub
   ```

## Contributing Guidelines

### Types of Contributions

#### Bug Reports

When reporting bugs, please include:

- **Description**: Clear description of the bug
- **Steps to Reproduce**: Detailed steps to reproduce the issue
- **Expected Behavior**: What you expected to happen
- **Actual Behavior**: What actually happened
- **Environment**: OS, Python version, UCW version
- **Additional Context**: Any other relevant information

#### Feature Requests

For feature requests, please provide:

- **Use Case**: Why is this feature needed?
- **Proposed Solution**: How should it work?
- **Alternatives**: Other solutions you've considered
- **Additional Context**: Any other relevant information

#### Code Contributions

- **Small Changes**: Bug fixes, documentation updates, minor improvements
- **Medium Changes**: New features, significant refactoring
- **Large Changes**: Major architectural changes (discuss first)

### Pull Request Guidelines

#### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Changes Made
- List of specific changes
- New features added
- Bugs fixed
- Documentation updated

## Testing
- [ ] Tests added/updated
- [ ] Manual testing performed
- [ ] Cross-platform testing (if applicable)
- [ ] Performance testing (if applicable)

## Documentation
- [ ] README.md updated
- [ ] API documentation updated
- [ ] User guide updated
- [ ] Developer guide updated
- [ ] Changelog updated

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No breaking changes (or breaking changes documented)
```

#### Review Process

1. **Automated Checks**: CI runs tests and linting
2. **Code Review**: Maintainers review code quality and functionality
3. **Testing**: Verify changes work as expected
4. **Documentation**: Ensure documentation is updated
5. **Approval**: Maintainer approves and merges

## Code Style

### Python Style Guide

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with some modifications:

#### Formatting

```python
# Use black for automatic formatting
black ucw/

# Line length: 88 characters (black default)
# Indentation: 4 spaces
# String quotes: Double quotes preferred
```

#### Naming Conventions

```python
# Classes: PascalCase
class UniversalCommandWrapper:
    pass

# Functions and variables: snake_case
def parse_command(command_name: str) -> CommandSpec:
    pass

# Constants: UPPER_SNAKE_CASE
DEFAULT_TIMEOUT = 10

# Private methods: leading underscore
def _extract_options(self, help_text: str) -> List[OptionSpec]:
    pass
```

#### Type Hints

```python
from typing import List, Optional, Union, Dict, Any

def parse_command(self, command_name: str) -> CommandSpec:
    """Parse a command's help text."""
    pass

def run(self, *args, **kwargs) -> ExecutionResult:
    """Execute command with arguments."""
    pass
```

#### Docstrings

```python
def parse_command(self, command_name: str) -> CommandSpec:
    """
    Parse a command's help/man page into structured specification.
    
    Args:
        command_name: Name of the command to parse
        
    Returns:
        CommandSpec object with parsed information
        
    Raises:
        ValueError: If command help cannot be retrieved
        subprocess.TimeoutExpired: If help command times out
    """
    pass
```

### Code Quality Tools

```bash
# Format code
black ucw/

# Lint code
flake8 ucw/

# Type checking
mypy ucw/

# Security check
bandit -r ucw/
```

## Testing

### Test Structure

```
tests/
├── test_basic.py           # Basic functionality tests
├── test_parsers.py         # Parser-specific tests
├── test_generators.py      # Generator tests
├── test_wrappers.py        # Wrapper tests
├── test_cli.py             # CLI tests
├── test_integration.py     # Integration tests
└── fixtures/               # Test data
    ├── help_texts/         # Sample help texts
    └── expected_outputs/   # Expected parsing results
```

### Writing Tests

#### Test Naming

```python
def test_command_parsing():
    """Test basic command parsing."""
    pass

def test_windows_parser_option_detection():
    """Test Windows parser option detection."""
    pass

def test_wrapper_execution_with_positional_args():
    """Test wrapper execution with positional arguments."""
    pass
```

#### Test Categories

1. **Unit Tests**: Test individual functions and methods
2. **Integration Tests**: Test component interactions
3. **End-to-End Tests**: Test complete workflows
4. **Performance Tests**: Test performance characteristics

#### Test Examples

```python
import pytest
from ucw import UniversalCommandWrapper

def test_command_parsing():
    """Test basic command parsing."""
    ucw = UniversalCommandWrapper()
    spec = ucw.parse_command("ls")
    
    assert spec.name == "ls"
    assert len(spec.options) > 0
    assert len(spec.positional_args) >= 0

def test_wrapper_execution():
    """Test wrapper execution."""
    ucw = UniversalCommandWrapper()
    spec = ucw.parse_command("pwd")
    wrapper = ucw.build_wrapper(spec)
    
    result = wrapper.run()
    assert result.success
    assert result.return_code == 0
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_basic.py

# Run with verbose output
pytest -v tests/

# Run with coverage
pytest --cov=ucw tests/

# Run specific test
pytest tests/test_basic.py::test_command_parsing
```

## Documentation

### Documentation Standards

- **README.md**: Project overview and quick start
- **API Documentation**: Complete API reference
- **User Guide**: Comprehensive usage guide
- **Developer Guide**: Contribution and development guide
- **Changelog**: Version history and changes

### Documentation Updates

When contributing, ensure documentation is updated:

1. **New Features**: Update relevant documentation
2. **API Changes**: Update API documentation
3. **User-Facing Changes**: Update user guide
4. **Developer Changes**: Update developer guide
5. **All Changes**: Update changelog

### Writing Documentation

#### Style Guidelines

- Use clear, concise language
- Provide examples for complex concepts
- Include code samples where appropriate
- Use proper markdown formatting
- Link to related sections

#### Documentation Structure

```markdown
# Section Title

Brief description of the section.

## Subsection

Detailed information with examples.

### Code Example

```python
# Example code
from ucw import UniversalCommandWrapper
ucw = UniversalCommandWrapper()
```

### Notes

Additional information or warnings.
```

## Release Process

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible API changes
- **MINOR**: Backwards compatible functionality additions
- **PATCH**: Backwards compatible bug fixes

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] Version number updated
- [ ] Release notes prepared
- [ ] Tag created
- [ ] Release published

### Release Process

1. **Prepare Release**
   ```bash
   # Update version in __init__.py
   # Update CHANGELOG.md
   # Update documentation
   ```

2. **Create Release**
   ```bash
   # Create tag
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   
   # Create GitHub release
   ```

3. **Post-Release**
   - Update documentation
   - Announce release
   - Monitor for issues

## Community

### Getting Help

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and general discussion
- **Documentation**: Comprehensive guides and references
- **Code Comments**: Inline documentation and examples

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General discussion and questions
- **Pull Requests**: Code review and discussion
- **Documentation**: Guides and references

### Recognition

Contributors are recognized in:

- **CONTRIBUTORS.md**: List of contributors
- **Release Notes**: Contributors for each release
- **GitHub**: Contributor statistics and activity

## License

By contributing to UCW, you agree that your contributions will be licensed under:

- **Source Code**: GNU Affero General Public License v3.0 (AGPL-3.0)
- **Documentation**: Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)

## Questions?

If you have questions about contributing, please:

1. Check the documentation first
2. Search existing issues and discussions
3. Create a new issue or discussion
4. Contact maintainers directly

Thank you for contributing to UCW! 🎉
