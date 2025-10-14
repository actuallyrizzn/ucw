# Universal Command Wrapper (UCW) - Technical Specification

## 🧭 **Mission Statement**

The **Universal Command Wrapper (UCW)** is a framework-agnostic library that can **discover**, **analyze**, and **reconstruct** system commands into **structured, callable interfaces**.

It is not a policy engine or security layer — its purpose is simply to *understand* a command's syntax and *reproduce* it programmatically.

## ⚙️ **Functional Scope**

### 1. **Discovery**
* Scan `$PATH` to locate available executable commands.
* Return metadata: `name`, `path`, and basic provenance (system, package, user).
* No filtering or safety classification — all executables are candidates.

### 2. **Help Extraction**
* Retrieve help/man text using platform-specific methods:
  * Windows: `command /?`
  * POSIX: `command --help` or `man command`
* Handle timeouts, missing help, and malformed output gracefully.

### 3. **Parsing & Normalization**
* Parse help/man text into a **CommandSpec** structure:
  * Command name and usage line(s)
  * List of **OptionSpec** entries (flags, arguments, defaults)
  * Descriptive text and examples (if found)
* Infer parameter types (`bool`, `string`, `int`, `path`) from heuristics.

### 4. **Wrapper Construction**
* Generate a callable object that mirrors the CLI:
  * Accepts structured kwargs (`command.run(verbose=True, file="input.txt")`)
  * Builds the correct argument list automatically
  * Executes the command via `subprocess.run`
  * Returns a normalized **ExecutionResult** with `stdout`, `stderr`, `return_code`.

### 5. **Result Normalization**
* Capture execution data in a portable schema:
  ```python
  {
      "command": "ls -la",
      "stdout": "...",
      "stderr": "",
      "return_code": 0,
      "elapsed": 0.132
  }
  ```

## 🔧 **Core Architecture**

### **Module Structure**
```
ucw/
├── __init__.py
├── discovery/
│   ├── windows_discovery.py
│   ├── linux_discovery.py
│   └── base_discovery.py
├── parsing/
│   ├── windows_parser.py
│   ├── linux_parser.py
│   └── base_parser.py
├── generation/
│   ├── wrapper_generator.py
│   └── templates/
└── utils/
    ├── helpers.py
    └── types.py
```

### **Core Interfaces**
```python
class UniversalCommandWrapper:
    def __init__(self, platform: str = "auto"):
        self.platform = platform or self._detect_platform()
    
    def discover_commands(self) -> List[CommandInfo]:
        """Discover available commands on the platform."""
        pass
    
    def parse_command(self, command_name: str) -> CommandSpec:
        """Parse a command's help/man page into structured spec."""
        pass
    
    def build_wrapper(self, spec: CommandSpec) -> CommandWrapper:
        """Build a callable wrapper from a command spec."""
        pass

class CommandWrapper:
    def run(self, **kwargs) -> ExecutionResult:
        """Execute the command with given arguments."""
        pass
```

## 🧩 **Core Data Models**

```python
@dataclass
class CommandSpec:
    name: str
    usage: str
    options: list["OptionSpec"]
    examples: list[str]

@dataclass
class OptionSpec:
    name: str
    aliases: list[str]
    has_value: bool
    value_name: str | None
    type_hint: str | None
    description: str | None

@dataclass
class ExecutionResult:
    command: str
    stdout: str
    stderr: str
    return_code: int
    elapsed: float
```

## 🧠 **API Shape**

```python
from ucw import UniversalCommandWrapper

ucw = UniversalCommandWrapper(platform="windows")
spec = ucw.parse_command("dir")
wrapper = ucw.build_wrapper(spec)

result = wrapper.run(path="C:\\", verbose=True)
print(result.stdout)
```

## 🚫 **Explicitly Out of Scope**

* Command "safety" or privilege analysis
* LLM involvement in parsing
* Plugin registration (SMCP, Letta, or others)
* Concurrency, caching, or sandboxing
* Command chaining or pipelines

## ✅ **Success Criteria**

* Correctly parses ≥75% of tested built-in commands (`ls`, `cat`, `grep`, `date`, `whoami`, `dir`, `findstr`, `ipconfig`, etc.).
* Auto-generates runnable wrappers that produce equivalent CLI results.
* Executes with consistent output schema on Windows and Linux.
* Zero dependency beyond Python stdlib.

## 🎯 **Implementation Phases**

### **Phase 1: Foundation (Weeks 1-2)**
- [ ] Command discovery engine for Windows and Linux
- [ ] Basic help parsing for Windows `/?` and Linux `--help`/`man`
- [ ] Core data models (`CommandSpec`, `OptionSpec`, `ExecutionResult`)
- [ ] Basic wrapper construction and execution

### **Phase 2: Enhancement (Weeks 3-4)**
- [ ] Advanced help parsing with type inference
- [ ] Improved option detection and aliasing
- [ ] Cross-platform testing and validation
- [ ] Error handling and edge case management

### **Phase 3: Optimization (Weeks 5-6)**
- [ ] Performance optimization for discovery and parsing
- [ ] Enhanced type inference heuristics
- [ ] Comprehensive test suite with built-in commands
- [ ] Documentation and examples

### **Phase 4: Polish (Weeks 7-8)**
- [ ] Final testing across Windows and Linux
- [ ] Package distribution and installation
- [ ] Performance benchmarking
- [ ] Community feedback integration

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

This specification defines UCW as a **cross-platform CLI interface synthesizer** — a tool that observes a system's command language and can reconstruct any of its verbs as Python-callable objects.

**Key Success Factors:**
- Focus on core functionality: discover → parse → wrap → execute
- Start with common built-in commands for validation
- Build incrementally with clear phase boundaries
- Maintain zero external dependencies beyond Python stdlib

*This document serves as the complete technical specification for the Universal Command Wrapper (UCW) project.*
