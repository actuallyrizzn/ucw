"""
CommandWrapper class for UCW.

This module defines the CommandWrapper class that provides callable
wrappers for system commands.
"""

import subprocess
import time
from typing import Dict, Any

from models import CommandSpec, ExecutionResult


class CommandWrapper:
    """Callable wrapper for a system command."""
    
    def __init__(self, command_name: str, spec: CommandSpec):
        self.command_name = command_name
        self.spec = spec
    
    def run(self, **kwargs) -> ExecutionResult:
        """
        Execute the command with given arguments.
        
        Args:
            **kwargs: Command arguments
            
        Returns:
            ExecutionResult object
        """
        # Build command arguments
        cmd_args = [self.command_name]
        
        # Add options based on kwargs
        for option in self.spec.options:
            if option.flag in kwargs:
                value = kwargs[option.flag]
                if option.is_boolean and value:
                    # Boolean flag - just add the flag
                    cmd_args.append(option.flag)
                elif not option.is_boolean and value is not None:
                    # Value flag - add flag and value
                    cmd_args.extend([option.flag, str(value)])
        
        # Execute command
        start_time = time.time()
        try:
            result = subprocess.run(
                cmd_args,
                capture_output=True,
                text=True,
                timeout=30
            )
            elapsed = time.time() - start_time
            
            return ExecutionResult(
                command=" ".join(cmd_args),
                stdout=result.stdout,
                stderr=result.stderr,
                return_code=result.returncode,
                elapsed=elapsed
            )
        except subprocess.TimeoutExpired:
            elapsed = time.time() - start_time
            return ExecutionResult(
                command=" ".join(cmd_args),
                stdout="",
                stderr="Command timed out after 30 seconds",
                return_code=-1,
                elapsed=elapsed
            )
        except Exception as e:
            elapsed = time.time() - start_time
            return ExecutionResult(
                command=" ".join(cmd_args),
                stdout="",
                stderr=f"Command execution failed: {str(e)}",
                return_code=-1,
                elapsed=elapsed
            )
