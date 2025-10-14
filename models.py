"""
Core data models for Universal Command Wrapper (UCW).

This module defines the fundamental data structures used throughout UCW
for representing command specifications, options, and execution results.
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class CommandSpec:
    """Represents a parsed command specification."""
    name: str
    usage: str
    options: List["OptionSpec"]
    description: str = ""
    examples: List[str] = None
    
    def __post_init__(self):
        if self.examples is None:
            self.examples = []


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
        return {
            "command": self.command,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "return_code": self.return_code,
            "elapsed": self.elapsed,
            "success": self.success
        }
