# Universal Command Wrapper (UCW) — Focused Technical Specification

## 🧭 **Mission Statement**

The **Universal Command Wrapper (UCW)** is a Python library and CLI utility that, given a single system command, can **analyze its syntax**, **generate a callable wrapper**, and **optionally write or update a Python CLI file** implementing that wrapper.

It does *not* scan the entire system or classify commands — it focuses exclusively on turning a *specific known CLI command* into a reproducible Python interface.

## ⚙️ **Functional Scope**

### 1. **Input Modes**

* **Command Mode:**
  Supply a CLI command (e.g., `ls`, `grep`, `ipconfig`) → UCW fetches help/man text, parses it, and generates the wrapper.
* **File Mode:**
  Provide a path to an existing `cli.py` file → UCW merges or replaces the specified command definition within it.

```bash
ucw wrap ls --output cli.py
ucw wrap ipconfig --update ./tools/cli.py
```

### 2. **Help Extraction**

* Fetch help/man text using platform-specific strategies:
  * Windows: `command /?`
  * POSIX: `command --help` or `man command`
* Handle:
  * Timeouts (default 10s)
  * Commands with no help text
  * Malformed or paginated output (`less` or `more` interception)

### 3. **Parsing & Schema Generation**

* Extract structured command metadata:
  * Usage syntax line(s)
  * Flags and argument options
  * Examples or descriptive context (if available)
* Build a `CommandSpec` model with inferred parameter types.

### 4. **Wrapper Construction**

* Generate a `CommandWrapper` Python object capable of:
  * Accepting structured kwargs (`wrapper.run(verbose=True, path="/tmp")`)
  * Building the equivalent CLI call
  * Executing it via `subprocess.run`
  * Returning a normalized `ExecutionResult`

### 5. **Output Handling**

Two operation modes:

| Mode                      | Behavior                                                                    |
| ------------------------- | --------------------------------------------------------------------------- |
| **No Output Specified**   | Returns `CommandWrapper` object to memory (library mode).                   |
| **Output File Specified** | Creates or updates a `cli.py` file that includes the wrapper.               |
| **Update Mode**           | Replaces an existing wrapper in a CLI file if the same command name exists. |

File operations should:
* Preserve any unrelated content in the existing file.
* Insert or replace code blocks bounded by tags, e.g.:
```python
  # UCW-BEGIN: ls
  ... auto-generated code ...
  # UCW-END: ls
  ```

### 6. **Execution Normalization**

All wrapper calls return structured execution data:
```python
{
    "command": "ls -la",
    "stdout": "...",
    "stderr": "",
    "return_code": 0,
    "elapsed": 0.124
}
```

## 🧱 **Simplified Architecture**

```
ucw/
├── __init__.py
├── parser/
│   ├── windows.py
│   ├── posix.py
│   └── base.py
├── generator/
│   ├── wrapper_builder.py     # builds callable wrapper object
│   └── file_writer.py         # handles new or updated CLI output
├── models.py
└── cli.py                     # command-line entrypoint
```

## 🧩 **Core Data Models**

```python
@dataclass
class CommandSpec:
    name: str
    usage: str
    options: list["OptionSpec"]

@dataclass
class OptionSpec:
    flag: str
    takes_value: bool
    description: str | None
    type_hint: str | None

@dataclass
class ExecutionResult:
    command: str
    stdout: str
    stderr: str
    return_code: int
    elapsed: float
```

## 🧩 **Core API**

```python
from ucw import UniversalCommandWrapper

ucw = UniversalCommandWrapper(platform="auto")

# Create wrapper in memory
spec = ucw.parse_command("ls")
wrapper = ucw.build_wrapper(spec)
result = wrapper.run(l=True, a=True)

# Generate or update a CLI file
ucw.write_wrapper("ls", output="cli.py", update=True)
```

## 🚫 **Out of Scope**

* System-wide scanning or indexing of commands.
* LLM or semantic inference of arguments.
* Safety, sandboxing, or policy layers.
* Multi-command chaining or pipelines.

## ✅ **Success Criteria**

* Works on both Windows and Linux.
* Correctly parses and wraps ≥80% of tested commands.
* Can generate a new CLI file or update an existing one without corrupting it.
* Maintains zero external dependencies.
* End-to-end runtime for typical command generation: under 5 seconds.

## 🎯 **Implementation Phases**

### **Phase 1: Core Functionality**
* Command parsing and wrapper construction (in-memory)
* Simple file output (new CLI file creation)
* `ucw wrap <command>` CLI entrypoint

### **Phase 2: File Integration**
* Intelligent `--update` mode with section tagging
* Preservation of existing CLI content
* CLI diff and confirmation prompt

### **Phase 3: Type Refinement & Cross-Platform**
* Argument type inference improvements
* Windows `/` vs POSIX `-` handling
* Extended testing matrix

## 🔍 **Key Technical Challenges**

### **Help Parsing Heuristics**
1. **Usage Line Extraction**: Parse `command [options] [args]` patterns
2. **Flag Detection**: Identify `-v`, `--verbose`, `/v` style options
3. **Argument Inference**: Determine if flags take values (`--file=path` vs `--verbose`)
4. **Type Detection**: Infer `bool`, `string`, `int`, `path` from context

### **Cross-Platform Differences**
1. **Windows**: `/` prefix, inconsistent `/?` output formats
2. **Linux**: `-` and `--` prefixes, `man` page groff markup
3. **Command Discovery**: PATH parsing, executable detection
4. **Execution**: `subprocess.run` with platform-specific shell handling

## 🚀 **Ready for Development**

This specification defines UCW as a **single-command wrapper compiler** — a developer tool that can be dropped into any environment to turn arbitrary system commands into working Python interfaces or extend an existing CLI incrementally.

**Key Success Factors:**
- Focus on single-command analysis and wrapper generation
- Dual-mode operation: library (in-memory) and builder (file output)
- Start with common built-in commands for validation
- Build incrementally with clear phase boundaries
- Maintain zero external dependencies beyond Python stdlib

*This document serves as the complete technical specification for the Universal Command Wrapper (UCW) project.*
