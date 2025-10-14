# UCW API Documentation

This document provides comprehensive API reference for the Universal Command Wrapper (UCW) library.

## Table of Contents

- [Core Classes](#core-classes)
- [Data Models](#data-models)
- [Parsers](#parsers)
- [Generators](#generators)
- [CLI Interface](#cli-interface)
- [Error Handling](#error-handling)
- [Type Hints](#type-hints)

## Core Classes

### UniversalCommandWrapper

The main class for command analysis and wrapper generation.

```python
class UniversalCommandWrapper:
    """Main UCW class for command analysis and wrapper generation."""
    
    def __init__(self, platform_name: Optional[str] = None):
        """
        Initialize UCW with platform detection.
        
        Args:
            platform_name: Platform to use ("windows", "posix", "auto")
                          If None, auto-detects based on current system
        """
    
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
    
    def build_wrapper(self, spec: CommandSpec) -> CommandWrapper:
        """
        Build a callable wrapper from a command specification.
        
        Args:
            spec: CommandSpec object
            
        Returns:
            CommandWrapper object
        """
    
    def write_wrapper(self, command_name: str, output: Optional[str] = None, 
                     update: bool = False) -> Union[CommandWrapper, str]:
        """
        Generate wrapper and optionally write to file.
        
        Args:
            command_name: Name of the command to wrap
            output: Output file path (optional)
            update: Whether to update existing file
            
        Returns:
            CommandWrapper object if no output specified, otherwise file path
        """
```

### CommandWrapper

Callable wrapper for executing system commands.

```python
class CommandWrapper:
    """Callable wrapper for a system command."""
    
    def __init__(self, command_name: str, spec: CommandSpec):
        """
        Initialize command wrapper.
        
        Args:
            command_name: Name of the system command
            spec: Parsed command specification
        """
    
    def run(self, *args, **kwargs) -> ExecutionResult:
        """
        Execute the command with given arguments.
        
        Args:
            *args: Positional arguments in order
            **kwargs: Named options/flags
            
        Returns:
            ExecutionResult object with command output and metadata
        """
```

## Data Models

### CommandSpec

Represents a parsed command specification.

```python
@dataclass
class CommandSpec:
    """Represents a parsed command specification."""
    name: str
    usage: str
    options: List[OptionSpec]
    positional_args: List[PositionalArgSpec] = None
    description: str = ""
    examples: List[str] = None
```

**Attributes:**
- `name`: Command name (e.g., "ls", "cp")
- `usage`: Usage line from help text
- `options`: List of available options/flags
- `positional_args`: List of positional arguments
- `description`: Command description
- `examples`: Usage examples (if available)

### OptionSpec

Represents a command option/flag.

```python
@dataclass
class OptionSpec:
    """Represents a command option/flag."""
    flag: str
    takes_value: bool
    description: Optional[str] = None
    type_hint: Optional[str] = None
    required: bool = False
    default: Optional[str] = None
    
    @property
    def is_boolean(self) -> bool:
        """Check if this is a boolean flag (no value)."""
        return not self.takes_value
```

**Attributes:**
- `flag`: Option flag (e.g., "-l", "--long", "/v")
- `takes_value`: Whether the option requires a value
- `description`: Option description from help text
- `type_hint`: Inferred type ("str", "int", "path", "bool")
- `required`: Whether the option is required
- `default`: Default value (if any)

### PositionalArgSpec

Represents a positional argument.

```python
@dataclass
class PositionalArgSpec:
    """Represents a positional argument."""
    name: str
    required: bool
    variadic: bool = False
    description: Optional[str] = None
    type_hint: Optional[str] = None
    
    @property
    def is_optional(self) -> bool:
        """Check if this argument is optional (wrapped in brackets)."""
        return not self.required
```

**Attributes:**
- `name`: Argument name (e.g., "SOURCE", "DEST", "FILE")
- `required`: Whether the argument is required
- `variadic`: Whether it accepts multiple values (e.g., "FILE...")
- `description`: Argument description
- `type_hint`: Inferred type ("str", "int", "path")

### ExecutionResult

Represents the result of command execution.

```python
@dataclass
class ExecutionResult:
    """Represents the result of command execution."""
    command: str
    stdout: str
    stderr: str
    return_code: int
    elapsed: float
    
    @property
    def success(self) -> bool:
        """Check if the command executed successfully."""
        return self.return_code == 0
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
```

**Attributes:**
- `command`: Full command line that was executed
- `stdout`: Standard output from the command
- `stderr`: Standard error from the command
- `return_code`: Exit code from the command
- `elapsed`: Execution time in seconds
- `success`: Boolean indicating successful execution

## Parsers

### BaseParser

Abstract base class for command parsers.

```python
class BaseParser(ABC):
    """Abstract base class for command parsers."""
    
    def __init__(self):
        self.timeout = 10  # Default timeout for help commands
    
    def parse_command(self, command_name: str) -> CommandSpec:
        """Parse a command's help text into structured specification."""
    
    def _get_help_text(self, command_name: str) -> str:
        """Get help text for a command."""
    
    def _extract_usage(self, help_text: str) -> str:
        """Extract usage line from help text."""
    
    def _extract_options(self, help_text: str) -> List[OptionSpec]:
        """Extract options from help text."""
    
    def _extract_positional_args(self, usage: str) -> List[PositionalArgSpec]:
        """Extract positional arguments from usage line."""
    
    def _infer_type_hint(self, description: str) -> Optional[str]:
        """Infer type hint from option description."""
    
    def _infer_positional_type(self, arg_name: str) -> str:
        """Infer type hint for positional argument."""
```

### WindowsParser

Parser for Windows command help text.

```python
class WindowsParser(BaseParser):
    """Parser for Windows command help text."""
    
    def _get_help_command(self, command_name: str) -> List[str]:
        """Get Windows help command."""
        return [command_name, '/?']
    
    def _try_alternative_help(self, command_name: str) -> str:
        """Try alternative help methods for Windows."""
    
    def _is_option_line(self, line: str) -> bool:
        """Check if a line contains a Windows option definition."""
    
    def _parse_option_line(self, line: str) -> Optional[OptionSpec]:
        """Parse a Windows option line."""
```

**Supported Formats:**
- `/option`: Boolean flags
- `/option:value`: Value-taking options
- `/option=value`: Alternative value format

### PosixParser

Parser for POSIX command help text.

```python
class PosixParser(BaseParser):
    """Parser for POSIX command help text."""
    
    def _get_help_command(self, command_name: str) -> List[str]:
        """Get POSIX help command."""
        return [command_name, '--help']
    
    def _try_alternative_help(self, command_name: str) -> str:
        """Try alternative help methods for POSIX."""
    
    def _is_option_line(self, line: str) -> bool:
        """Check if a line contains a POSIX option definition."""
    
    def _parse_option_line(self, line: str) -> Optional[OptionSpec]:
        """Parse a POSIX option line."""
```

**Supported Formats:**
- `-o`: Short options
- `--option`: Long options
- `-o, --option`: Combined short and long
- `--option=ARG`: Value-taking options
- `--option[=ARG]`: Optional value options

## Generators

### WrapperBuilder

Builder for CommandWrapper objects.

```python
class WrapperBuilder:
    """Builder for CommandWrapper objects."""
    
    def build_wrapper(self, spec: CommandSpec) -> CommandWrapper:
        """Build a CommandWrapper from a CommandSpec."""
    
    def generate_mcp_plugin_code(self, spec: CommandSpec) -> str:
        """Generate MCP plugin code following the plugin development guide pattern."""
    
    def _generate_argument_definitions(self, spec: CommandSpec) -> str:
        """Generate argparse argument definitions."""
    
    def _generate_argument_handling(self, spec: CommandSpec) -> str:
        """Generate argument handling code."""
```

### FileWriter

Writer for CLI files.

```python
class FileWriter:
    """Writer for CLI files."""
    
    def __init__(self):
        self.wrapper_builder = WrapperBuilder()
    
    def write_wrapper(self, spec: CommandSpec, wrapper, output_path: str, 
                     update: bool = False) -> str:
        """Write wrapper to file."""
    
    def _write_new_file(self, spec: CommandSpec, wrapper, output_path: str) -> str:
        """Write a new CLI file."""
    
    def _update_existing_file(self, spec: CommandSpec, wrapper, output_path: str) -> str:
        """Update existing CLI file with new wrapper."""
    
    def _extract_wrapper_code(self, plugin_code: str, command_name: str) -> str:
        """Extract the wrapper-specific code from plugin code."""
    
    def _update_wrapper_section(self, content: str, command_name: str, 
                               new_code: str) -> str:
        """Update or add a wrapper section in existing content."""
```

## CLI Interface

### Command Line Arguments

```bash
ucw wrap <command> [options]
```

**Arguments:**
- `command`: Name of the command to wrap

**Options:**
- `--output`, `-o`: Output file path for generated wrapper
- `--update`, `-u`: Update existing file instead of creating new one
- `--platform`: Target platform (`windows`, `posix`, `auto`)

### CLI Functions

```python
def main():
    """Main CLI entry point."""

def setup_wrap_command(subparsers):
    """Setup the wrap command."""

def execute_wrap_command(args):
    """Execute the wrap command."""
```

## Error Handling

### Common Exceptions

```python
class UCWError(Exception):
    """Base exception for UCW errors."""

class CommandNotFoundError(UCWError):
    """Raised when a command is not found."""

class HelpParseError(UCWError):
    """Raised when help text cannot be parsed."""

class WrapperGenerationError(UCWError):
    """Raised when wrapper generation fails."""
```

### Error Handling Examples

```python
from ucw import UniversalCommandWrapper

ucw = UniversalCommandWrapper()

try:
    spec = ucw.parse_command("nonexistent_command")
except subprocess.CalledProcessError:
    print("Command not found")
except subprocess.TimeoutExpired:
    print("Help command timed out")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Type Hints

UCW uses comprehensive type hints for better IDE support and type checking.

### Core Types

```python
from typing import List, Optional, Union, Dict, Any

# Command specifications
CommandSpec = CommandSpec
OptionSpec = OptionSpec
PositionalArgSpec = PositionalArgSpec
ExecutionResult = ExecutionResult

# Wrapper types
CommandWrapper = CommandWrapper
UniversalCommandWrapper = UniversalCommandWrapper

# Parser types
BaseParser = BaseParser
WindowsParser = WindowsParser
PosixParser = PosixParser

# Generator types
WrapperBuilder = WrapperBuilder
FileWriter = FileWriter
```

### Type Checking

To enable type checking with mypy:

```bash
pip install mypy
mypy ucw/
```

## Best Practices

### Command Selection

1. **Test Commands**: Use well-known commands for testing
2. **Platform Awareness**: Consider platform-specific behavior
3. **Error Handling**: Always handle potential command failures

### Wrapper Usage

1. **Argument Validation**: Validate arguments before passing to wrappers
2. **Timeout Handling**: Set appropriate timeouts for long-running commands
3. **Output Processing**: Process command output appropriately

### File Generation

1. **Backup Files**: Backup existing files before updates
2. **Permission Handling**: Ensure proper file permissions
3. **Path Validation**: Validate file paths before writing

## Performance Considerations

### Parsing Performance

- Help text parsing is cached per command
- Timeout is set to 10 seconds by default
- Large help texts may take longer to parse

### Execution Performance

- Commands run with 30-second timeout by default
- Subprocess overhead is minimal
- Consider async execution for multiple commands

### Memory Usage

- CommandSpecs are lightweight
- Help text is not stored after parsing
- Wrappers have minimal memory footprint
