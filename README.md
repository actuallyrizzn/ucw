# Universal Command Wrapper (UCW)

[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Documentation License: CC BY-SA 4.0](https://img.shields.io/badge/Documentation%20License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-green.svg)](https://github.com/actuallyrizzn/ucw)

A powerful command wrapper generator that can be used standalone or as an SMCP plugin. UCW automatically analyzes system commands and generates callable wrappers or MCP plugin files, bridging the gap between command-line tools and Python applications through intelligent command parsing and wrapper generation.

## 🚀 Features

- **Cross-platform Support**: Works on Windows (`/?`) and POSIX (`--help`, `man`) systems
- **Zero Dependencies**: Uses only Python standard library
- **Intelligent Parsing**: Automatically extracts options, flags, and positional arguments
- **Type Inference**: Infers parameter types from help text descriptions
- **Dual Output Modes**: 
  - Library mode: Generate callable Python wrappers
  - Builder mode: Generate complete MCP plugin files
- **File Management**: Create new CLI files or update existing ones
- **SMCP Plugin**: Primary use case as SMCP plugin (just copy folder)
- **Standalone Tool**: Can be used independently for development/testing
- **MCP Compatibility**: Generates plugins compatible with MCP servers

## 📋 Table of Contents

- [Installation](#installation)
- [Installation Guide](INSTALL.md) - Detailed installation instructions
- [Usage Guide](docs/usage-guide.md) - Comprehensive usage documentation
- [Quick Start](#quick-start)

## 🛠 Installation

### As SMCP Plugin (Primary Use)

UCW is primarily designed to be used as a plugin for SMCP (Simple MCP):

1. **Clone the repository**:
   ```bash
   git clone https://github.com/actuallyrizzn/ucw.git
   ```

2. **Place in SMCP plugins directory**:
   ```bash
   # Copy to your SMCP plugins directory
   cp -r ucw /path/to/smcp/plugins/
   ```

3. **Make CLI executable**:
   ```bash
   chmod +x /path/to/smcp/plugins/ucw/cli.py
   ```

### Standalone Usage (Development/Testing)

For development, testing, or standalone usage:

```bash
# Clone the repository
git clone https://github.com/actuallyrizzn/ucw.git
cd ucw

# Install production dependencies (zero external dependencies)
pip install -r requirements.txt

# Install testing dependencies (for development/testing)
pip install -r requirements-testing.txt

# Run tests
python -m pytest tests/

# Use CLI directly
python cli.py wrap ls
```

## 🚀 Quick Start

### CLI Usage

#### SMCP Plugin Mode (Default - JSON Output)
```bash
# Generate wrapper in memory (JSON output)
python cli.py wrap ls

# Generate wrapper and save to file (JSON output)
python cli.py wrap ls --output cli.py

# Parse command specification (JSON output)
python cli.py parse ls

# Execute command (JSON output)
python cli.py execute ls --args "/root" --options '{"--all": true}'
```

#### Standalone Mode (Human-Readable Output)
```bash
# Generate wrapper in memory (human-readable output)
python cli.py --standalone wrap ls
python cli.py --human wrap ls  # Alternative flag

# Parse command specification (human-readable output)
python cli.py --standalone parse ls

# Execute command (human-readable output)
python cli.py --standalone execute ls --args "/root" --options '{"--all": true}'

# Generate CLI file (human-readable output)
python cli.py --standalone wrap tar --output cli.py

# Update existing CLI file (human-readable output)
python cli.py --standalone wrap find --update cli.py
```

### Library Usage

```python
from ucw import UniversalCommandWrapper

# Initialize UCW
ucw = UniversalCommandWrapper(platform_name="auto")

# Parse and wrap a command
spec = ucw.parse_command("echo")
wrapper = ucw.build_wrapper(spec)

# Execute the command with arguments
result = wrapper.run("hello", "world")
print(result.stdout)
```

## 📖 Usage

For comprehensive usage documentation, see the [Usage Guide](docs/usage-guide.md).

### Quick Examples

**CLI Usage:**
```bash
# Generate wrapper
python cli.py wrap echo

# Parse command
python cli.py parse ls

# Execute command
python cli.py execute echo --args "hello" "world"
```

**Library Usage:**
```python
from __init__ import UniversalCommandWrapper

ucw = UniversalCommandWrapper()
spec = ucw.parse_command("echo")
wrapper = ucw.build_wrapper(spec)
result = wrapper.run("hello", "world")
print(result.stdout)
```

## 🏗 Architecture

```
ucw/
├── __init__.py              # Main UCW class and exports
├── cli.py                   # Command-line interface
├── models.py                # Core data models
├── wrapper.py               # CommandWrapper implementation
├── parser/                  # Platform-specific parsers
│   ├── __init__.py
│   ├── base.py             # Abstract base parser
│   ├── windows.py          # Windows command parser
│   └── posix.py            # POSIX command parser
├── generator/               # Wrapper and file generation
│   ├── __init__.py
│   ├── wrapper_builder.py  # Wrapper building logic
│   └── file_writer.py      # File writing utilities
├── tests/                   # Test suite
│   └── test_basic.py       # Basic functionality tests
├── docs/                    # Documentation
│   ├── plugin-development-guide.md
│   └── project-idea.md
├── requirements.txt         # Production dependencies (zero external deps)
├── requirements-testing.txt # Testing and development dependencies
└── README.md               # This file
```

### Data Flow

1. **Command Analysis**: UCW fetches help text using platform-specific methods
2. **Parsing**: Help text is parsed to extract options and positional arguments
3. **Type Inference**: Types are inferred from descriptions and argument names
4. **Wrapper Generation**: CommandSpec is converted to executable CommandWrapper
5. **Execution**: Commands are executed with proper argument handling

### Supported Command Formats

#### Windows Commands
- Format: `command /?`
- Options: `/option`, `/option:value`
- Examples: `dir /?`, `copy /?`

#### POSIX Commands
- Format: `command --help` or `man command`
- Options: `-o`, `--option`, `--option=value`
- Examples: `ls --help`, `grep --help`

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone repository
git clone https://github.com/actuallyrizzn/ucw.git
cd ucw

# Install in development mode
pip install -e .

# Install production dependencies (zero external dependencies)
pip install -r requirements.txt

# Install testing dependencies (for development/testing)
pip install -r requirements-testing.txt

# Run tests
python -m pytest tests/
```

### Adding New Features

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

### Code License

This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0) - see the [LICENSE](LICENSE) file for details.

### Documentation License

This documentation is licensed under the Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0) - see the [LICENSE-DOCS](LICENSE-DOCS) file for details.

## 🔒 Security Considerations

UCW executes system commands, so consider security implications:

- **Command validation**: UCW doesn't validate command safety
- **Privilege escalation**: Commands run with current user privileges
- **Input sanitization**: Validate inputs before passing to UCW

### UCW Security Model

UCW assumes the runtime environment defines its own boundaries. For containment, deploy SMCP inside a container or restricted user namespace. UCW operates entirely within those boundaries — it neither enforces nor bypasses them.

**Recommended Security Practices:**

- **Run SMCP in a Docker container** or lightweight VM
- **Mount only the directories** or devices you want the agent to see
- **Use a limited service account** or UID with no sudo privileges
- **Cap CPU/RAM/network** with container or cgroup limits

This approach gives the agent total reach *within that defined sandbox*, while keeping UCW philosophically pure: **maximum capability, user-defined sovereignty**.

## 🙏 Acknowledgments

- Inspired by the need for seamless command-line tool integration
- Built for the Animus, SanctumOS and Letta MCP Server ecosystem
- Thanks to the Python community for excellent standard library tools

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/actuallyrizzn/ucw/issues)
- **Discussions**: [GitHub Discussions](https://github.com/actuallyrizzn/ucw/discussions)
- **Documentation**: [GitHub Wiki](https://github.com/actuallyrizzn/ucw/wiki)

---

**Universal Command Wrapper** - Making command-line tools accessible to Python applications.
