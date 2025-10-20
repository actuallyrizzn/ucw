# UCW Usage Guide

This comprehensive guide covers all aspects of using UCW (Universal Command Wrapper).

## Table of Contents

- [Quick Start](#quick-start)
- [CLI Interface](#cli-interface)
- [Library Interface](#library-interface)
- [Examples](#examples)
- [API Reference](#api-reference)
- [Advanced Usage](#advanced-usage)
- [Troubleshooting](#troubleshooting)

## Quick Start

### Basic CLI Usage

```bash
# Generate wrapper in memory (JSON output)
python cli.py wrap echo

# Generate wrapper and save to file
python cli.py wrap echo --output my_cli.py

# Parse command specification
python cli.py parse echo

# Execute command
python cli.py execute echo --args "hello" "world"
```

### Basic Library Usage

```python
from __init__ import UniversalCommandWrapper

# Initialize UCW
ucw = UniversalCommandWrapper()

# Parse and wrap a command
spec = ucw.parse_command("echo")
wrapper = ucw.build_wrapper(spec)

# Execute the command with arguments
result = wrapper.run("hello", "world")
print(result.stdout)
```

## CLI Interface

### Commands

#### `wrap` - Generate Command Wrapper

```bash
python cli.py wrap <command> [options]
```

**Options:**
- `--output`, `-o`: Output file path for generated wrapper
- `--update`, `-u`: Update existing file instead of creating new one
- `--platform`: Target platform (`windows`, `posix`, `linux`, `auto`)
- `--timeout-help`: Timeout for help commands in seconds (default: 10)
- `--timeout-exec`: Timeout for command execution in seconds (default: 30)

**Examples:**
```bash
# Basic wrapper generation
python cli.py wrap cp

# Generate CLI file
python cli.py wrap tar --output cli.py

# Update existing CLI file
python cli.py wrap find --update cli.py
```

#### `parse` - Parse Command Help

```bash
python cli.py parse <command> [options]
```

**Options:**
- `--platform`: Target platform (`windows`, `posix`, `linux`, `auto`)
- `--timeout-help`: Timeout for help commands in seconds (default: 10)

**Examples:**
```bash
# Parse command help
python cli.py parse grep

# Parse with specific platform
python cli.py parse dir --platform windows
```

#### `execute` - Execute Command

```bash
python cli.py execute <command> [options]
```

**Options:**
- `--args`: Positional arguments
- `--options`: JSON string of options/flags
- `--platform`: Target platform (`windows`, `posix`, `linux`, `auto`)
- `--timeout-help`: Timeout for help commands in seconds (default: 10)
- `--timeout-exec`: Timeout for command execution in seconds (default: 30)

**Examples:**
```bash
# Execute with arguments
python cli.py execute echo --args "hello" "world"

# Execute with options
python cli.py execute ls --options '{"--all": true, "-l": true}'
```

### Output Modes

#### JSON Mode (Default - SMCP Plugin)
```bash
python cli.py wrap echo
# Output: {"status": "success", "command": "echo", ...}
```

#### Human Mode (Standalone Usage)
```bash
python cli.py --standalone wrap echo
python cli.py --human wrap echo
# Output: Human-readable text
```

## Library Interface

### Basic Usage

```python
from __init__ import UniversalCommandWrapper

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
result = wrapper.run("pattern", "file.txt")
```

### Using Options with Kwargs

When commands have parsed options, you can use kwargs to pass them:

```python
# Parse a command with options
spec = ucw.parse_command("tar")
wrapper = ucw.build_wrapper(spec)

# Use kwargs for boolean flags (normalized from flag names)
result = wrapper.run(verbose=True, create=True)

# Use kwargs for value options
result = wrapper.run(file="archive.tar", directory="/path")

# Mix positional args and kwargs
result = wrapper.run("source.txt", "dest.txt", verbose=True)
```

**Note**: Kwargs keys are normalized from flag names:
- `--verbose` becomes `verbose=True`
- `-v` becomes `v=True` 
- `--output-file` becomes `output_file="value"`

### Advanced Usage

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

### Timeout Configuration

```python
# Configure timeouts
ucw = UniversalCommandWrapper(
    timeout_help=15,  # Help command timeout
    timeout_exec=45   # Execution timeout
)

# Environment variables
import os
os.environ['UCW_TIMEOUT_HELP'] = '20'
os.environ['UCW_TIMEOUT_EXEC'] = '60'
ucw = UniversalCommandWrapper()  # Uses env vars
```

## Examples

### Example 1: File Operations

```python
from __init__ import UniversalCommandWrapper

ucw = UniversalCommandWrapper()

# Wrap cp command
cp_spec = ucw.parse_command("cp")
cp_wrapper = ucw.build_wrapper(cp_spec)

# Copy file
result = cp_wrapper.run("source.txt", "dest.txt")
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

# Search for text
result = grep_wrapper.run("error", "logfile.txt")

print(f"Found {len(result.stdout.splitlines())} matches")
```

### Example 3: System Information

```python
# Wrap ls command
ls_spec = ucw.parse_command("ls")
ls_wrapper = ucw.build_wrapper(ls_spec)

# List directory contents
result = ls_wrapper.run()

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

## API Reference

### Core Classes

#### `UniversalCommandWrapper`

Main class for command analysis and wrapper generation.

```python
class UniversalCommandWrapper:
    def __init__(self, platform_name: Optional[str] = None,
                 timeout_help: Optional[int] = None,
                 timeout_exec: Optional[int] = None)
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
    def __init__(self, command_name: str, spec: CommandSpec, timeout: int = 30)
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

## Advanced Usage

### Custom Parsers

```python
from parser.base import BaseParser
from models import CommandSpec, OptionSpec

class CustomParser(BaseParser):
    def _get_help_command(self, command_name: str) -> List[str]:
        return [command_name, "--custom-help"]
    
    def _parse_help_text(self, command_name: str, help_text: str) -> CommandSpec:
        # Custom parsing logic
        return CommandSpec(
            name=command_name,
            usage=f"{command_name} [options]",
            options=[],
            positional_args=[],
            description="Custom parsed command",
            examples=[]
        )
    
    def _is_option_line(self, line: str) -> bool:
        return "--" in line
    
    def _parse_option_line(self, line: str) -> OptionSpec:
        # Custom option parsing
        return None
    
    def _try_alternative_help(self, command_name: str) -> str:
        return f"Alternative help for {command_name}"
```

### Error Handling

```python
from __init__ import UniversalCommandWrapper

ucw = UniversalCommandWrapper()

try:
    spec = ucw.parse_command("nonexistent_command")
    wrapper = ucw.build_wrapper(spec)
    result = wrapper.run()
    
    if not result.success:
        print(f"Command failed: {result.stderr}")
        
except Exception as e:
    print(f"Error: {e}")
```

### Batch Processing

```python
import json
from __init__ import UniversalCommandWrapper

ucw = UniversalCommandWrapper()

# Process multiple commands
commands = ["echo", "ls", "cp", "mv", "grep"]
results = {}

for cmd in commands:
    try:
        spec = ucw.parse_command(cmd)
        wrapper = ucw.build_wrapper(spec)
        result = wrapper.run()
        results[cmd] = {
            "success": result.success,
            "options_count": len(spec.options),
            "args_count": len(spec.positional_args)
        }
    except Exception as e:
        results[cmd] = {"error": str(e)}

print(json.dumps(results, indent=2))
```

## Troubleshooting

### Common Issues

#### Command Not Found
```bash
# Error: Command not found
python cli.py wrap nonexistent_command
```

**Solution**: Use commands that exist on your system.

#### Permission Errors
```bash
# Error: Permission denied
python cli.py wrap sudo
```

**Solution**: UCW runs commands with current user privileges.

#### Platform Detection Issues
```python
# Force specific platform
ucw = UniversalCommandWrapper(platform_name="windows")
ucw = UniversalCommandWrapper(platform_name="posix")
```

#### Timeout Issues
```python
# Increase timeouts
ucw = UniversalCommandWrapper(timeout_help=30, timeout_exec=60)
```

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# UCW will show detailed debug information
ucw = UniversalCommandWrapper()
spec = ucw.parse_command("echo")
```

### Getting Help

- **Issues**: [GitHub Issues](https://github.com/actuallyrizzn/ucw/issues)
- **Discussions**: [GitHub Discussions](https://github.com/actuallyrizzn/ucw/discussions)
- **Documentation**: [GitHub Wiki](https://github.com/actuallyrizzn/ucw/wiki)
