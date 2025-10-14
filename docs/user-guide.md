# UCW User Guide

This comprehensive guide will help you get started with the Universal Command Wrapper (UCW) and master its features.

## Table of Contents

- [Getting Started](#getting-started)
- [Basic Usage](#basic-usage)
- [Advanced Features](#advanced-features)
- [Platform-Specific Usage](#platform-specific-usage)
- [MCP Plugin Development](#mcp-plugin-development)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)
- [Examples Gallery](#examples-gallery)

## Getting Started

### Installation

#### As SMCP Plugin (Primary Use)

```bash
# Clone the repository
git clone https://github.com/actuallyrizzn/ucw.git

# For SMCP integration, place in plugins directory
cp -r ucw /path/to/smcp/plugins/
chmod +x /path/to/smcp/plugins/ucw/cli.py
```

#### Standalone Usage (Development/Testing)

```bash
# Clone the repository
git clone https://github.com/actuallyrizzn/ucw.git
cd ucw

# Install development dependencies (optional)
pip install -r requirements.txt

# Use directly
python cli.py wrap ls
```

### First Steps

1. **Test Installation**:
   ```bash
   ucw wrap ls
   ```

2. **Check Platform Detection**:
   ```python
   from ucw import UniversalCommandWrapper
   ucw = UniversalCommandWrapper()
   print(f"Platform: {ucw.platform}")
   ```

3. **Parse Your First Command**:
   ```python
   spec = ucw.parse_command("pwd")
   print(f"Command: {spec.name}")
   print(f"Options: {len(spec.options)}")
   print(f"Positional args: {len(spec.positional_args)}")
   ```

## Usage Modes

UCW can be used in two ways:

### 1. SMCP Plugin Mode (Primary)
- **Installation**: Copy the `ucw` folder to your SMCP plugins directory
- **Usage**: Access through SMCP's plugin system
- **Benefits**: Integrated with SMCP ecosystem, automatic discovery
- **Use Case**: Production deployments, integrated workflows

### 2. Standalone Mode (Development/Testing)
- **Installation**: Clone repository and use directly
- **Usage**: Run `python cli.py` commands directly
- **Benefits**: Independent operation, easy testing, development
- **Use Case**: Development, testing, standalone automation

## Basic Usage

### CLI Interface

The UCW CLI provides both SMCP-compatible JSON output and human-readable standalone output:

#### SMCP Plugin Mode (Default - JSON Output)
```bash
# Generate wrapper in memory
python cli.py wrap ls

# Parse command specification
python cli.py parse ls

# Execute command with arguments
python cli.py execute ls --args "/root" --options '{"--all": true}'
```

#### Standalone Mode (Human-Readable Output)
```bash
# Use --standalone or --human flag for readable output
python cli.py --standalone wrap ls
python cli.py --human parse ls
python cli.py --standalone execute pwd
```

#### Generate In-Memory Wrapper

```bash
ucw wrap cp
```

**Output:**
```
Generated wrapper for 'cp'
Positional args: <source>, <dest>
Usage: wrapper.run(--archive, --attributes-only, -b)

Positional arguments:
  1. SOURCE (required, path)
  2. DEST (required, path)

Available options:
  --archive: same as -dR --preserve=all
  --attributes-only: don't copy the file data, just the attributes
  -b: like --backup but does not accept an argument
  ...
```

#### Generate CLI File

```bash
ucw wrap tar --output archive_tool.py
```

This creates a complete Python CLI file that can be executed independently.

#### Update Existing File

```bash
ucw wrap find --update existing_cli.py
```

This adds or updates the find command wrapper in an existing CLI file.

### Library Interface

#### Basic Command Wrapping

```python
from ucw import UniversalCommandWrapper

# Initialize UCW
ucw = UniversalCommandWrapper()

# Parse a command
spec = ucw.parse_command("ls")
wrapper = ucw.build_wrapper(spec)

# Execute with options
result = wrapper.run(l=True, a=True, h=True)
print(result.stdout)
```

#### Working with Positional Arguments

```python
# Parse cp command
cp_spec = ucw.parse_command("cp")
cp_wrapper = ucw.build_wrapper(cp_spec)

# Execute with positional arguments
result = cp_wrapper.run("source.txt", "dest.txt", verbose=True)
print(f"Copy successful: {result.success}")
```

#### Mixed Arguments

```python
# Parse grep command
grep_spec = ucw.parse_command("grep")
grep_wrapper = ucw.build_wrapper(grep_spec)

# Execute with both positional and named arguments
result = grep_wrapper.run(
    "error",           # pattern (positional)
    "logfile.txt",     # file (positional)
    i=True,            # ignore case (option)
    n=True,            # line numbers (option)
    r=True             # recursive (option)
)
```

## Advanced Features

### Custom Platform Selection

```python
# Force Windows parsing
ucw_windows = UniversalCommandWrapper(platform_name="windows")

# Force POSIX parsing
ucw_posix = UniversalCommandWrapper(platform_name="posix")

# Auto-detect (default)
ucw_auto = UniversalCommandWrapper(platform_name="auto")
```

### Batch Command Processing

```python
commands = ["ls", "cp", "mv", "grep", "find"]
wrappers = {}

for cmd in commands:
    try:
        spec = ucw.parse_command(cmd)
        wrapper = ucw.build_wrapper(spec)
        wrappers[cmd] = wrapper
        print(f"✓ Wrapped {cmd}")
    except Exception as e:
        print(f"✗ Failed to wrap {cmd}: {e}")
```

### Error Handling

```python
from ucw import UniversalCommandWrapper
import subprocess

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

### Working with Command Specifications

```python
# Parse command
spec = ucw.parse_command("tar")

# Inspect options
print("Options:")
for option in spec.options:
    print(f"  {option.flag}: {option.description}")
    print(f"    Takes value: {option.takes_value}")
    print(f"    Type hint: {option.type_hint}")

# Inspect positional arguments
print("\nPositional arguments:")
for arg in spec.positional_args:
    print(f"  {arg.name}: {arg.type_hint}")
    print(f"    Required: {arg.required}")
    print(f"    Variadic: {arg.variadic}")
```

## Platform-Specific Usage

### Windows Commands

```python
# Windows-specific wrapper
ucw_windows = UniversalCommandWrapper(platform_name="windows")

# Parse Windows commands
dir_spec = ucw_windows.parse_command("dir")
copy_spec = ucw_windows.parse_command("copy")

# Execute Windows commands
dir_wrapper = ucw_windows.build_wrapper(dir_spec)
result = dir_wrapper.run(w=True)  # Wide format
```

### POSIX Commands

```python
# POSIX-specific wrapper
ucw_posix = UniversalCommandWrapper(platform_name="posix")

# Parse POSIX commands
ls_spec = ucw_posix.parse_command("ls")
cp_spec = ucw_posix.parse_command("cp")

# Execute POSIX commands
ls_wrapper = ucw_posix.build_wrapper(ls_spec)
result = ls_wrapper.run(l=True, a=True)
```

### Cross-Platform Compatibility

```python
import platform

# Detect current platform
current_platform = platform.system().lower()

if current_platform == "windows":
    ucw = UniversalCommandWrapper(platform_name="windows")
    commands = ["dir", "copy", "move"]
else:
    ucw = UniversalCommandWrapper(platform_name="posix")
    commands = ["ls", "cp", "mv"]

# Process commands based on platform
for cmd in commands:
    spec = ucw.parse_command(cmd)
    wrapper = ucw.build_wrapper(spec)
    # Use wrapper...
```

## MCP Plugin Development

### Generating MCP Plugins

UCW can generate complete MCP plugin files:

```python
# Generate MCP plugin
spec = ucw.parse_command("tar")
plugin_path = ucw.write_wrapper("tar", output="tar_plugin.py")

print(f"Generated MCP plugin: {plugin_path}")
```

### Plugin Structure

Generated plugins follow this structure:

```python
#!/usr/bin/env python3
"""
tar Plugin

Auto-generated plugin for tar command.
Generated by Universal Command Wrapper (UCW).
"""

import argparse
import json
import subprocess
import sys
import time
from typing import Dict, Any

def main():
    """Main entry point for the plugin CLI."""
    # Plugin implementation...

def setup_execute_command(subparsers):
    """Setup the execute command."""
    # Argument definitions...

def execute_command(args) -> Dict[str, Any]:
    """Execute the tar command."""
    # Command execution logic...
```

### Using Generated Plugins

```bash
# Execute generated plugin
python tar_plugin.py execute --create --file archive.tar file1.txt file2.txt

# Get help
python tar_plugin.py --help
```

### Plugin Integration

```python
# In your MCP server
import subprocess
import json

def call_tar_plugin(arguments):
    """Call the generated tar plugin."""
    cmd = ["python", "tar_plugin.py", "execute"] + arguments
    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout)
```

## Troubleshooting

### Common Issues

#### Command Not Found

```python
try:
    spec = ucw.parse_command("nonexistent_command")
except subprocess.CalledProcessError as e:
    print(f"Command not found: {e}")
    # Handle gracefully
```

#### Help Text Parsing Errors

```python
try:
    spec = ucw.parse_command("problematic_command")
except Exception as e:
    print(f"Parsing failed: {e}")
    # Try alternative approach or manual specification
```

#### Timeout Issues

```python
# For commands with slow help generation
import subprocess

# Increase timeout for specific commands
result = subprocess.run(
    ["slow_command", "--help"],
    capture_output=True,
    text=True,
    timeout=30  # Increase timeout
)
```

#### Permission Errors

```python
import os

# Check file permissions before writing
output_path = "cli.py"
if os.path.exists(output_path):
    if not os.access(output_path, os.W_OK):
        print("No write permission for output file")
        # Handle gracefully
```

### Debug Mode

```python
# Enable debug output
import logging
logging.basicConfig(level=logging.DEBUG)

# Parse with debug information
spec = ucw.parse_command("ls")
print(f"Debug: Parsed {len(spec.options)} options")
print(f"Debug: Parsed {len(spec.positional_args)} positional args")
```

### Validation

```python
def validate_wrapper(wrapper):
    """Validate a generated wrapper."""
    try:
        # Test with help option
        result = wrapper.run(help=True)
        if result.return_code == 0:
            print("✓ Wrapper validation passed")
        else:
            print("✗ Wrapper validation failed")
    except Exception as e:
        print(f"✗ Wrapper validation error: {e}")
```

## Best Practices

### Command Selection

1. **Use Well-Known Commands**: Start with standard system commands
2. **Test Commands First**: Verify commands work before wrapping
3. **Consider Platform Differences**: Account for Windows vs POSIX differences

### Wrapper Usage

1. **Validate Arguments**: Check arguments before passing to wrappers
2. **Handle Errors**: Always handle potential command failures
3. **Use Appropriate Timeouts**: Set timeouts based on expected execution time

### File Management

1. **Backup Files**: Backup existing files before updates
2. **Check Permissions**: Verify write permissions before file operations
3. **Validate Paths**: Ensure file paths are valid and accessible

### Performance

1. **Cache Wrappers**: Reuse wrappers for multiple executions
2. **Batch Operations**: Process multiple commands efficiently
3. **Monitor Resources**: Watch memory and CPU usage for large operations

## Security Considerations

### UCW Security Model

UCW executes system commands and assumes the runtime environment defines its own boundaries. For containment, deploy SMCP inside a container or restricted user namespace. UCW operates entirely within those boundaries — it neither enforces nor bypasses them.

### Security Best Practices

#### Container Deployment
```bash
# Run SMCP in Docker container
docker run -it --rm \
  -v /path/to/allowed/directory:/workspace \
  --user 1000:1000 \
  --memory=512m \
  --cpus=1.0 \
  smcp-container
```

#### Restricted User Account
```bash
# Create limited user account
sudo useradd -r -s /bin/false smcp-user
sudo chown -R smcp-user:smcp-user /path/to/smcp/plugins/
```

#### Resource Limits
```bash
# Set cgroup limits
echo "512M" > /sys/fs/cgroup/memory/smcp/memory.limit_in_bytes
echo "100000" > /sys/fs/cgroup/cpu/smcp/cpu.cfs_quota_us
```

### Security Philosophy

This approach gives the agent total reach *within that defined sandbox*, while keeping UCW philosophically pure: **maximum capability, user-defined sovereignty**.

- **UCW provides capability** - maximum command access within boundaries
- **Environment provides security** - containers, users, resource limits
- **User defines policy** - what commands are allowed, what resources are available

## Examples Gallery

### File Operations

```python
# Copy files with progress
cp_wrapper = ucw.build_wrapper(ucw.parse_command("cp"))
result = cp_wrapper.run("source.txt", "dest.txt", verbose=True, force=True)

# Move files with backup
mv_wrapper = ucw.build_wrapper(ucw.parse_command("mv"))
result = mv_wrapper.run("old.txt", "new.txt", backup=True)

# Remove files safely
rm_wrapper = ucw.build_wrapper(ucw.parse_command("rm"))
result = rm_wrapper.run("file.txt", interactive=True, force=True)
```

### Text Processing

```python
# Search with multiple patterns
grep_wrapper = ucw.build_wrapper(ucw.parse_command("grep"))
result = grep_wrapper.run(
    "error|warning|critical",
    "logfile.txt",
    i=True,  # ignore case
    n=True,  # line numbers
    r=True   # recursive
)

# Sort files
sort_wrapper = ucw.build_wrapper(ucw.parse_command("sort"))
result = sort_wrapper.run("input.txt", output="sorted.txt", reverse=True)
```

### System Information

```python
# List directory contents
ls_wrapper = ucw.build_wrapper(ucw.parse_command("ls"))
result = ls_wrapper.run(
    l=True,    # long format
    a=True,    # all files
    h=True,    # human readable
    t=True     # sort by time
)

# Get system information
uname_wrapper = ucw.build_wrapper(ucw.parse_command("uname"))
result = uname_wrapper.run(a=True)  # all information
```

### Archive Operations

```python
# Create archive
tar_wrapper = ucw.build_wrapper(ucw.parse_command("tar"))
result = tar_wrapper.run(
    create=True,
    file="archive.tar",
    verbose=True,
    "file1.txt", "file2.txt"  # positional args
)

# Extract archive
result = tar_wrapper.run(
    extract=True,
    file="archive.tar",
    verbose=True
)
```

### Network Operations

```python
# Download files
wget_wrapper = ucw.build_wrapper(ucw.parse_command("wget"))
result = wget_wrapper.run(
    "https://example.com/file.txt",
    output_document="downloaded.txt",
    progress="bar"
)

# Test connectivity
ping_wrapper = ucw.build_wrapper(ucw.parse_command("ping"))
result = ping_wrapper.run("google.com", count=4)
```

### Process Management

```python
# Find processes
ps_wrapper = ucw.build_wrapper(ucw.parse_command("ps"))
result = ps_wrapper.run(aux=True)  # all processes

# Kill processes
kill_wrapper = ucw.build_wrapper(ucw.parse_command("kill"))
result = kill_wrapper.run(signal="TERM", "1234")  # PID as positional arg
```

This user guide provides comprehensive coverage of UCW's features and capabilities. For more specific examples or advanced use cases, refer to the API documentation or explore the test suite.
