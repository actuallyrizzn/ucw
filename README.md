# Universal Command Wrapper (UCW)

A Python library and CLI utility that analyzes system commands and generates callable wrappers or MCP plugin files.

## Overview

UCW takes a single system command, parses its help/man page, and generates either:
- A callable Python wrapper object (library mode)
- A complete MCP plugin file (builder mode)

## Installation

```bash
# Clone the repository
git clone https://github.com/actuallyrizzn/ucw.git
cd ucw

# Install in development mode
pip install -e .
```

## Usage

### CLI Interface

```bash
# Generate wrapper in memory
ucw wrap ls

# Generate CLI file
ucw wrap ls --output cli.py

# Update existing CLI file
ucw wrap grep --update tools/cli.py
```

### Library Interface

```python
from ucw import UniversalCommandWrapper

# Initialize UCW
ucw = UniversalCommandWrapper(platform="auto")

# Parse and wrap a command
spec = ucw.parse_command("ls")
wrapper = ucw.build_wrapper(spec)

# Execute the command
result = wrapper.run(l=True, a=True)
print(result.stdout)
```

## Features

- **Cross-platform**: Supports Windows (`/?`) and POSIX (`--help`, `man`) commands
- **Zero dependencies**: Uses only Python standard library
- **MCP integration**: Generates plugins compatible with Animus Letta MCP Server
- **File management**: Can create new CLI files or update existing ones
- **Type inference**: Automatically infers parameter types from help text

## Architecture

```
ucw/
├── parser/           # Windows/POSIX help parsing
├── generator/        # Wrapper building + file writing
├── models.py         # Core data models
└── cli.py           # Command-line entrypoint
```

## Development

```bash
# Run tests
python tests/test_basic.py

# Run CLI
python cli.py wrap dir --output test_cli.py
```

## License

MIT License - see LICENSE file for details.
