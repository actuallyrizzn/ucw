# UCW Installation Guide

This guide explains how to install UCW for different use cases.

## Production Installation (Zero Dependencies)

For production use, UCW requires **zero external dependencies** beyond Python 3.7+:

```bash
# Clone the repository
git clone https://github.com/actuallyrizzn/ucw.git
cd ucw

# No pip install needed! UCW uses only Python standard library
python cli.py wrap ls
```

## Development/Testing Installation

For development, testing, or contributing to UCW:

```bash
# Clone the repository
git clone https://github.com/actuallyrizzn/ucw.git
cd ucw

# Install testing dependencies
pip install -r requirements-testing.txt

# Run tests
python -m pytest tests/

# Run tests with coverage
python -m pytest tests/ --cov=. --cov-report=term-missing
```

## Requirements Files Explained

### `requirements.txt` (Production)
- **Zero external dependencies**
- Contains only comments about future optional features
- UCW works entirely with Python standard library

### `requirements-testing.txt` (Development)
- **Testing framework**: pytest, pytest-cov, pytest-mock, pytest-timeout
- **Code quality**: black, flake8, isort, mypy
- **Coverage**: coverage, tox
- **Development**: pre-commit

## Use Cases

### As SMCP Plugin (Primary Use)
```bash
# Copy to SMCP plugins directory
cp -r ucw /path/to/smcp/plugins/
chmod +x /path/to/smcp/plugins/ucw/cli.py
```

### Standalone Development
```bash
# Install testing dependencies for development
pip install -r requirements-testing.txt

# Use UCW for command wrapping
python cli.py wrap tar --output my_cli.py
```

### Production Deployment
```bash
# No installation needed - just copy the files
cp -r ucw /path/to/production/
```

## Verification

Test that UCW works correctly:

```bash
# Test basic functionality
python cli.py wrap echo

# Test with file output
python cli.py wrap ls --output test_cli.py

# Test parsing
python cli.py parse grep
```

## Troubleshooting

### Import Errors
If you get import errors, ensure you're in the UCW directory:
```bash
cd /path/to/ucw
python cli.py --help
```

### Permission Errors
Make sure the CLI is executable:
```bash
chmod +x cli.py
```

### Python Version
UCW requires Python 3.7 or higher:
```bash
python --version  # Should be 3.7+
```
