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
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [CLI Interface](#cli-interface)
  - [Library Interface](#library-interface)
- [Examples](#examples)
- [API Reference](#api-reference)
- [Architecture](#architecture)
- [Contributing](#contributing)
- [License](#license)

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

# Install development dependencies (optional)
pip install -r requirements.txt

# Run tests
python tests/test_basic.py

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
python cli.py wrap ls --output my_ls.py

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
```

### Library Usage

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

## 📖 Usage

### CLI Interface

The UCW CLI provides a simple interface for command wrapping:

```bash
ucw wrap <command> [options]
```

#### Options

- `--output`, `-o`: Output file path for generated wrapper
- `--update`, `-u`: Update existing file instead of creating new one
- `--platform`: Target platform (`windows`, `posix`, `auto`)

#### Examples

```bash
# Basic wrapper generation
ucw wrap cp
# Output: Shows positional args and available options

# Generate CLI file
ucw wrap tar --output archive_tool.py

# Update existing file
ucw wrap find --update existing_cli.py
```

### Library Interface

The UCW library provides programmatic access to command wrapping functionality:

#### Basic Usage

```python
from ucw import UniversalCommandWrapper

# Initialize with platform detection
ucw = UniversalCommandWrapper()

# Parse a command
spec = ucw.parse_command("grep")
print(f"Command: {spec.name}")
print(f"Options: {len(spec.options)}")
print(f"Positional args: {len(spec.positional_args)}")

# Build wrapper
wrapper = ucw.build_wrapper(spec)

# Execute with arguments
result = wrapper.run("pattern", "file.txt", i=True)
```

#### Advanced Usage

```python
# Platform-specific initialization
ucw_windows = UniversalCommandWrapper(platform_name="windows")
ucw_posix = UniversalCommandWrapper(platform_name="posix")

# Parse multiple commands
commands = ["cp", "mv", "grep", "find"]
specs = {}
for cmd in commands:
    specs[cmd] = ucw.parse_command(cmd)

# Generate CLI files
for cmd, spec in specs.items():
    wrapper = ucw.build_wrapper(spec)
    file_path = ucw.write_wrapper(cmd, output=f"{cmd}_cli.py")
    print(f"Generated {file_path}")
```

## 💡 Examples

### Example 1: File Operations

```python
from ucw import UniversalCommandWrapper

ucw = UniversalCommandWrapper()

# Wrap cp command
cp_spec = ucw.parse_command("cp")
cp_wrapper = ucw.build_wrapper(cp_spec)

# Copy file with options
result = cp_wrapper.run("source.txt", "dest.txt", verbose=True, force=True)
print(f"Copy result: {result.success}")

# Wrap mv command
mv_spec = ucw.parse_command("mv")
mv_wrapper = ucw.build_wrapper(mv_spec)

# Move file
result = mv_wrapper.run("old_name.txt", "new_name.txt")
```

### Example 2: Text Processing

```python
# Wrap grep command
grep_spec = ucw.parse_command("grep")
grep_wrapper = ucw.build_wrapper(grep_spec)

# Search with multiple options
result = grep_wrapper.run(
    "error", 
    "logfile.txt", 
    i=True,  # ignore case
    n=True,  # line numbers
    r=True   # recursive
)

print(f"Found {len(result.stdout.splitlines())} matches")
```

### Example 3: System Information

```python
# Wrap ls command
ls_spec = ucw.parse_command("ls")
ls_wrapper = ucw.build_wrapper(ls_spec)

# List with detailed information
result = ls_wrapper.run(
    l=True,    # long format
    a=True,    # all files
    h=True     # human readable
)

print("Directory contents:")
print(result.stdout)
```

### Example 4: MCP Plugin Generation

```python
# Generate MCP plugin for tar command
tar_spec = ucw.parse_command("tar")
tar_wrapper = ucw.build_wrapper(tar_spec)

# Create plugin file
plugin_path = ucw.write_wrapper("tar", output="tar_plugin.py")
print(f"Generated MCP plugin: {plugin_path}")

# The generated file can be used as an MCP plugin
```

## 📚 API Reference

### Core Classes

#### `UniversalCommandWrapper`

Main class for command analysis and wrapper generation.

```python
class UniversalCommandWrapper:
    def __init__(self, platform_name: Optional[str] = None)
    def parse_command(self, command_name: str) -> CommandSpec
    def build_wrapper(self, spec: CommandSpec) -> CommandWrapper
    def write_wrapper(self, command_name: str, output: Optional[str] = None, update: bool = False) -> Union[CommandWrapper, str]
```

#### `CommandSpec`

Represents a parsed command specification.

```python
@dataclass
class CommandSpec:
    name: str
    usage: str
    options: List[OptionSpec]
    positional_args: List[PositionalArgSpec]
    description: str
    examples: List[str]
```

#### `OptionSpec`

Represents a command option/flag.

```python
@dataclass
class OptionSpec:
    flag: str
    takes_value: bool
    description: Optional[str]
    type_hint: Optional[str]
    required: bool
    default: Optional[str]
```

#### `PositionalArgSpec`

Represents a positional argument.

```python
@dataclass
class PositionalArgSpec:
    name: str
    required: bool
    variadic: bool
    description: Optional[str]
    type_hint: Optional[str]
```

#### `CommandWrapper`

Callable wrapper for executing commands.

```python
class CommandWrapper:
    def __init__(self, command_name: str, spec: CommandSpec)
    def run(self, *args, **kwargs) -> ExecutionResult
```

#### `ExecutionResult`

Represents the result of command execution.

```python
@dataclass
class ExecutionResult:
    command: str
    stdout: str
    stderr: str
    return_code: int
    elapsed: float
    success: bool
```

### Platform-Specific Parsers

#### `BaseParser`

Abstract base class for command parsers.

#### `WindowsParser`

Parser for Windows command help text (`command /?`).

#### `PosixParser`

Parser for POSIX command help text (`command --help`, `man command`).

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
├── requirements.txt         # Development dependencies
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

# Install development dependencies
pip install -r requirements.txt

# Run tests
python tests/test_basic.py
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

## 🙏 Acknowledgments

- Inspired by the need for seamless command-line tool integration
- Built for the Animus Letta MCP Server ecosystem
- Thanks to the Python community for excellent standard library tools

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/actuallyrizzn/ucw/issues)
- **Discussions**: [GitHub Discussions](https://github.com/actuallyrizzn/ucw/discussions)
- **Documentation**: [GitHub Wiki](https://github.com/actuallyrizzn/ucw/wiki)

---

**Universal Command Wrapper** - Making command-line tools accessible to Python applications.