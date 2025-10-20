# UCW Developer Guide

This guide is for developers who want to contribute to UCW, extend its functionality, or understand its internal architecture.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Development Setup](#development-setup)
- [Code Structure](#code-structure)
- [Adding New Features](#adding-new-features)
- [Testing](#testing)
- [Contributing](#contributing)
- [Performance Considerations](#performance-considerations)
- [Debugging](#debugging)
- [Appendices](#appendices)

## Architecture Overview

### High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CLI Interface │    │  Library API    │    │  MCP Integration│
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │ UniversalCommand │
                    │    Wrapper      │
                    └─────────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Parser Layer  │    │ Generator Layer │    │  Wrapper Layer  │
│                 │    │                 │    │                 │
│ • BaseParser    │    │ • WrapperBuilder│    │ • CommandWrapper│
│ • WindowsParser │    │ • FileWriter    │    │ • ExecutionResult│
│ • PosixParser   │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Data Flow

1. **Input**: Command name (e.g., "ls", "cp")
2. **Help Retrieval**: Platform-specific help text fetching
3. **Parsing**: Extract options and positional arguments
4. **Type Inference**: Infer types from descriptions
5. **Wrapper Generation**: Create executable wrapper
6. **Execution**: Run commands with proper argument handling

### Core Components

#### Parser Layer
- **BaseParser**: Abstract base class with common functionality
- **WindowsParser**: Handles Windows command help (`command /?`)
- **PosixParser**: Handles POSIX command help (`command --help`, `man command`)

#### Generator Layer
- **WrapperBuilder**: Creates CommandWrapper objects
- **FileWriter**: Handles CLI file generation and updates

#### Wrapper Layer
- **CommandWrapper**: Executable command wrapper
- **ExecutionResult**: Structured command output

## Development Setup

### Prerequisites

- Python 3.8+
- Git
- Text editor or IDE with Python support
- SMCP (Simple MCP) for plugin integration (optional for standalone use)
- Basic understanding of command-line tools and MCP protocols

### Environment Setup

```bash
# Clone repository
git clone https://github.com/actuallyrizzn/ucw.git
cd ucw

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt

# For SMCP plugin integration (optional)
# cp -r ucw /path/to/smcp/plugins/
```

### Development Tools

```bash
# Install additional development tools
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

## Code Structure

### Directory Layout

```
ucw/
├── __init__.py              # Main exports and UCW class
├── cli.py                   # Command-line interface
├── models.py                # Data models (CommandSpec, OptionSpec, etc.)
├── wrapper.py               # CommandWrapper implementation
├── parser/                  # Parsing layer
│   ├── __init__.py
│   ├── base.py             # Abstract base parser
│   ├── windows.py          # Windows command parser
│   └── posix.py            # POSIX command parser
├── generator/               # Generation layer
│   ├── __init__.py
│   ├── wrapper_builder.py  # Wrapper building logic
│   └── file_writer.py      # File writing utilities
├── tests/                   # Test suite
│   └── test_basic.py       # Basic functionality tests
├── docs/                    # Documentation
│   ├── api-reference.md
│   ├── user-guide.md
│   ├── developer-guide.md
│   ├── plugin-development-guide.md
│   └── project-idea.md
├── requirements.txt         # Development dependencies
├── LICENSE                  # AGPL-3.0 license
├── LICENSE-DOCS            # CC BY-SA 4.0 license
├── README.md               # Main documentation
├── CHANGELOG.md            # Version history
└── CONTRIBUTING.md         # Contribution guidelines
```

### Key Files

#### `__init__.py`
Main module exports and UniversalCommandWrapper class.

#### `models.py`
Core data structures:
- `CommandSpec`: Parsed command specification
- `OptionSpec`: Command option/flag
- `PositionalArgSpec`: Positional argument
- `ExecutionResult`: Command execution result

#### `parser/base.py`
Abstract base parser with common functionality:
- Help text retrieval
- Usage extraction
- Option parsing
- Positional argument parsing
- Type inference

#### `parser/windows.py`
Windows-specific parser:
- Handles `/option` and `/option:value` formats
- Windows-specific help text patterns
- Alternative help methods

#### `parser/posix.py`
POSIX-specific parser:
- Handles `-o`, `--option`, `--option=value` formats
- POSIX help text patterns
- Man page support

#### `wrapper.py`
CommandWrapper implementation:
- Command execution logic
- Argument handling
- Error handling
- Timeout management

## Adding New Features

### Adding New Parser Features

1. **Extend BaseParser**:
   ```python
   class BaseParser(ABC):
       def _extract_custom_info(self, help_text: str) -> List[CustomInfo]:
           """Extract custom information from help text."""
           # Implementation
   ```

2. **Update Platform Parsers**:
   ```python
   class WindowsParser(BaseParser):
       def _extract_custom_info(self, help_text: str) -> List[CustomInfo]:
           """Windows-specific custom info extraction."""
           # Implementation
   ```

3. **Add Tests**:
   ```python
   def test_custom_info_extraction():
       """Test custom info extraction."""
       parser = WindowsParser()
       # Test implementation
   ```

### Adding New Generator Features

1. **Extend WrapperBuilder**:
   ```python
   class WrapperBuilder:
       def generate_custom_wrapper(self, spec: CommandSpec) -> CustomWrapper:
           """Generate custom wrapper type."""
           # Implementation
   ```

2. **Update FileWriter**:
   ```python
   class FileWriter:
       def write_custom_wrapper(self, spec: CommandSpec, output_path: str) -> str:
           """Write custom wrapper to file."""
           # Implementation
   ```

### Adding New Data Models

1. **Define Model**:
   ```python
   @dataclass
   class CustomSpec:
       """Custom specification model."""
       name: str
       value: Optional[str] = None
   ```

2. **Update CommandSpec**:
   ```python
   @dataclass
   class CommandSpec:
       # ... existing fields ...
       custom_info: List[CustomSpec] = None
   ```

3. **Update Parsers**:
   ```python
   def _extract_custom_info(self, help_text: str) -> List[CustomSpec]:
       """Extract custom information."""
       # Implementation
   ```

## Testing

### Test Structure

```
tests/
├── test_basic.py           # Basic functionality tests
├── test_parsers.py         # Parser-specific tests
├── test_generators.py       # Generator tests
├── test_wrappers.py        # Wrapper tests
├── test_cli.py             # CLI tests
└── fixtures/               # Test data
    ├── help_texts/         # Sample help texts
    └── expected_outputs/   # Expected parsing results
```

### Writing Tests

#### Basic Test Structure

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

#### Parser Tests

```python
def test_windows_parser():
    """Test Windows parser functionality."""
    parser = WindowsParser()
    
    # Test option line detection
    assert parser._is_option_line("/v    Verbose output")
    assert not parser._is_option_line("Regular text line")
    
    # Test option parsing
    option = parser._parse_option_line("/v    Verbose output")
    assert option.flag == "/v"
    assert not option.takes_value

def test_posix_parser():
    """Test POSIX parser functionality."""
    parser = PosixParser()
    
    # Test option line detection
    assert parser._is_option_line("-v, --verbose    Verbose output")
    assert parser._is_option_line("--verbose    Verbose output")
    
    # Test option parsing
    option = parser._parse_option_line("-v, --verbose    Verbose output")
    assert option.flag == "-v"
    assert not option.takes_value
```

#### Integration Tests

```python
def test_end_to_end_workflow():
    """Test complete workflow from parsing to execution."""
    ucw = UniversalCommandWrapper()
    
    # Parse command
    spec = ucw.parse_command("ls")
    assert spec.name == "ls"
    
    # Build wrapper
    wrapper = ucw.build_wrapper(spec)
    assert wrapper.command_name == "ls"
    
    # Execute command
    result = wrapper.run(l=True)
    assert result.success
    assert "total" in result.stdout or len(result.stdout) > 0
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
```

## Contributing

### Contribution Process

1. **Fork Repository**: Fork the UCW repository on GitHub
2. **Create Branch**: Create a feature branch for your changes
3. **Make Changes**: Implement your changes with tests
4. **Test Changes**: Run tests to ensure everything works
5. **Submit PR**: Submit a pull request with description

### Code Style

#### Python Style

- Follow PEP 8 guidelines
- Use type hints for all functions
- Write docstrings for all public functions
- Use meaningful variable names

#### Code Formatting

```bash
# Format code with black
black ucw/

# Check style with flake8
flake8 ucw/
```

#### Documentation

- Update README.md for user-facing changes
- Update API documentation for API changes
- Add examples for new features
- Update changelog for releases

### Pull Request Guidelines

#### PR Description

```markdown
## Description
Brief description of changes

## Changes
- List of specific changes
- New features added
- Bugs fixed

## Testing
- Tests added/updated
- Manual testing performed

## Documentation
- Documentation updated
- Examples added
```

#### Review Process

1. **Automated Checks**: CI runs tests and linting
2. **Code Review**: Maintainers review code quality
3. **Testing**: Verify changes work as expected
4. **Documentation**: Ensure documentation is updated
5. **Approval**: Maintainer approves and merges

## Performance Considerations

### Parsing Performance

#### Optimization Strategies

1. **Caching**: Cache parsed command specifications
2. **Lazy Loading**: Parse only when needed
3. **Timeout Management**: Set appropriate timeouts
4. **Memory Management**: Clean up large help texts

#### Performance Monitoring

```python
import time
import cProfile

def profile_parsing():
    """Profile command parsing performance."""
    ucw = UniversalCommandWrapper()
    
    start_time = time.time()
    spec = ucw.parse_command("ls")
    end_time = time.time()
    
    print(f"Parsing time: {end_time - start_time:.3f}s")
    print(f"Options parsed: {len(spec.options)}")
    print(f"Positional args parsed: {len(spec.positional_args)}")

# Use cProfile for detailed profiling
cProfile.run('profile_parsing()')
```

### Execution Performance

#### Optimization Strategies

1. **Subprocess Optimization**: Use appropriate subprocess settings
2. **Timeout Management**: Set reasonable timeouts
3. **Resource Monitoring**: Monitor memory and CPU usage
4. **Batch Operations**: Process multiple commands efficiently

#### Performance Testing

```python
def benchmark_execution():
    """Benchmark command execution performance."""
    ucw = UniversalCommandWrapper()
    spec = ucw.parse_command("ls")
    wrapper = ucw.build_wrapper(spec)
    
    times = []
    for _ in range(10):
        start_time = time.time()
        result = wrapper.run()
        end_time = time.time()
        times.append(end_time - start_time)
    
    avg_time = sum(times) / len(times)
    print(f"Average execution time: {avg_time:.3f}s")
```

## Security Considerations

### UCW Security Model

UCW executes system commands and assumes the runtime environment defines its own boundaries. For containment, deploy SMCP inside a container or restricted user namespace. UCW operates entirely within those boundaries — it neither enforces nor bypasses them.

### Security Philosophy

This approach gives the agent total reach *within that defined sandbox*, while keeping UCW philosophically pure: **maximum capability, user-defined sovereignty**.

- **UCW provides capability** - maximum command access within boundaries
- **Environment provides security** - containers, users, resource limits
- **User defines policy** - what commands are allowed, what resources are available

### Development Security Practices

#### Testing in Containers
```bash
# Test UCW in isolated environment
docker run -it --rm \
  -v $(pwd):/workspace \
  --user 1000:1000 \
  python:3.9-slim \
  bash -c "cd /workspace && python tests/test_basic.py"
```

#### Restricted Development Environment
```bash
# Create development user with limited privileges
sudo useradd -m -s /bin/bash ucw-dev
sudo usermod -aG docker ucw-dev
sudo chown -R ucw-dev:ucw-dev /path/to/ucw/
```

#### Resource Monitoring
```bash
# Monitor resource usage during development
python -m cProfile -o profile.stats cli.py wrap ls
python -c "import pstats; pstats.Stats('profile.stats').sort_stats('cumulative').print_stats(10)"
```

## Debugging

### Debug Tools

#### Logging

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Parse with debug output
ucw = UniversalCommandWrapper()
spec = ucw.parse_command("ls")
```

#### Debug Mode

```python
class UniversalCommandWrapper:
    def __init__(self, platform_name: Optional[str] = None, debug: bool = False):
        self.debug = debug
        # ... rest of initialization
    
    def parse_command(self, command_name: str) -> CommandSpec:
        if self.debug:
            print(f"Debug: Parsing command '{command_name}'")
        # ... parsing logic
```

#### Error Handling

```python
def debug_parsing_error(command_name: str):
    """Debug parsing errors for a command."""
    try:
        ucw = UniversalCommandWrapper()
        spec = ucw.parse_command(command_name)
        print(f"✓ Successfully parsed {command_name}")
    except subprocess.CalledProcessError as e:
        print(f"✗ Command not found: {e}")
    except subprocess.TimeoutExpired:
        print(f"✗ Help command timed out")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
```

### Common Issues

#### Help Text Parsing

```python
def debug_help_text(command_name: str):
    """Debug help text parsing."""
    parser = PosixParser()
    help_text = parser._get_help_text(command_name)
    
    print(f"Help text length: {len(help_text)}")
    print(f"First 500 chars: {help_text[:500]}")
    
    # Test option line detection
    lines = help_text.split('\n')
    option_lines = [line for line in lines if parser._is_option_line(line)]
    print(f"Option lines found: {len(option_lines)}")
```

#### Wrapper Execution

```python
def debug_wrapper_execution(wrapper):
    """Debug wrapper execution."""
    try:
        result = wrapper.run(help=True)
        print(f"✓ Execution successful")
        print(f"Return code: {result.return_code}")
        print(f"Output length: {len(result.stdout)}")
    except Exception as e:
        print(f"✗ Execution failed: {e}")
        import traceback
        traceback.print_exc()
```

This developer guide provides comprehensive information for contributing to UCW. For specific implementation details, refer to the source code and API documentation.

## Appendices

### A. Plugin Development Guide

For detailed information on developing plugins for UCW and MCP integration, see the comprehensive [Plugin Development Guide](planning/plugin-development-guide.md). This guide covers:

- Plugin architecture and directory structure
- Creating your first plugin
- Advanced plugin development techniques
- Testing and deployment strategies
- Integration with MCP servers
- Best practices and troubleshooting

### B. Project Vision and Goals

The original project vision and goals are documented in the [Project Idea](planning/project-idea.md). This document outlines:

- The core concept and motivation behind UCW
- Target use cases and applications
- Design principles and architectural decisions
- Future roadmap and expansion plans
- Community and ecosystem considerations

These documents provide additional context for developers who want to understand the broader vision and contribute to UCW's plugin ecosystem.
