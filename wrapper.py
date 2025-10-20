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
    
    def run(self, *args, **kwargs) -> ExecutionResult:
        """
        Execute the command with given arguments.
        
        Args:
            *args: Positional arguments in order
            **kwargs: Named options/flags
            
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
        
        # Add positional arguments
        for i, arg in enumerate(self.spec.positional_args):
            if i < len(args):
                # Use provided positional argument
                cmd_args.append(str(args[i]))
            elif arg.required:
                # Required argument not provided - this will likely cause an error
                # but we'll let the command handle it
                pass
        
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
