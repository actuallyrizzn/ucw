"""
CommandWrapper class for UCW.

This module defines the CommandWrapper class that provides callable
wrappers for system commands.
"""

import subprocess
import time
from typing import Dict, Any

from models import CommandSpec, ExecutionResult, OptionSpec


class CommandWrapper:
    """Callable wrapper for a system command."""
    
    def __init__(self, command_name: str, spec: CommandSpec, timeout: int = 30):
        self.command_name = command_name
        self.spec = spec
        self.timeout = timeout
    
    def _normalize_kwargs_key(self, key: str) -> str:
        """Normalize kwargs key to match flag destination names."""
        # Remove leading dashes and slashes
        dest = key.lstrip('-/')
        
        # Handle empty case
        if not dest:
            dest = 'empty'
        
        # Replace remaining dashes with underscores
        dest = dest.replace('-', '_')
        
        # Handle special characters
        if dest == '?':
            dest = 'question'
        elif dest.startswith('?'):
            dest = 'question_' + dest[1:]
        
        # Ensure it's a valid Python identifier
        if not dest.isidentifier():
            # Replace invalid characters with underscores
            import re
            dest = re.sub(r'[^a-zA-Z0-9_]', '_', dest)
            # Ensure it doesn't start with a number
            if dest and dest[0].isdigit():
                dest = '_' + dest
        
        return dest
    
    def _find_option_by_dest(self, dest: str) -> OptionSpec:
        """Find option by normalized destination name."""
        for option in self.spec.options:
            if self._normalize_kwargs_key(option.flag) == dest:
                return option
        return None
    
    def run(self, *args, **kwargs) -> ExecutionResult:
        """
        Execute the command with given arguments.
        
        Args:
            *args: Positional arguments in order
            **kwargs: Named options/flags (normalized keys like 'l', 'all', 'verbose')
            
        Returns:
            ExecutionResult object
        """
        # Build command arguments
        cmd_args = [self.command_name]
        
        # Add options based on kwargs (with normalized key matching)
        for key, value in kwargs.items():
            option = None
            
            # First try to find by normalized key (new approach)
            option = self._find_option_by_dest(key)
            
            # If not found, try exact flag match (backward compatibility)
            if option is None:
                for opt in self.spec.options:
                    if opt.flag == key:
                        option = opt
                        break
            
            if option:
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
                timeout=self.timeout
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
                stderr=f"Command timed out after {self.timeout} seconds",
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
