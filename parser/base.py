"""
Base parser class for command help/man page parsing.

This module provides the abstract base class and common functionality
for parsing command help text across different platforms.
"""

import subprocess
import re
from abc import ABC, abstractmethod
from typing import List, Optional

from models import CommandSpec, OptionSpec, PositionalArgSpec


class BaseParser(ABC):
    """Abstract base class for command parsers."""
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout  # Configurable timeout for help commands
    
    def parse_command(self, command_name: str) -> CommandSpec:
        """
        Parse a command's help text into structured specification.
        
        Args:
            command_name: Name of the command to parse
            
        Returns:
            CommandSpec object with parsed information
        """
        if command_name is None:
            raise TypeError("Command name cannot be None")
        if not isinstance(command_name, str):
            raise TypeError("Command name must be a string")
        if not command_name:
            # Return empty spec for empty command name
            return CommandSpec(
                name="",
                usage="",
                options=[],
                positional_args=[],
                description="",
                examples=[]
            )
        
        help_text = self._get_help_text(command_name)
        return self._parse_help_text(command_name, help_text)
    
    def _get_help_text(self, command_name: str) -> str:
        """
        Get help text for a command.
        
        Args:
            command_name: Name of the command
            
        Returns:
            Raw help text
        """
        try:
            cmd = self._get_help_command(command_name)
            # Use shell=True for Windows commands (they need it for proper execution)
            use_shell = self.__class__.__name__ == 'WindowsParser'
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                shell=use_shell,
                timeout=self.timeout
            )
            
            # Accept help text if it contains meaningful content, even with non-zero return codes
            # Many commands (like Windows dir /?) return non-zero codes but provide valid help
            if result.stdout.strip() and len(result.stdout.strip()) > 20:
                return result.stdout
            else:
                # Try alternative help methods
                alt_help = self._try_alternative_help(command_name)
                if alt_help is not None and alt_help != f"No help available for {command_name}":
                    return alt_help
                else:
                    return f"No help available for {command_name}"
                
        except subprocess.TimeoutExpired:
            return f"Help command timed out for {command_name}"
        except Exception as e:
            return f"Failed to get help for {command_name}: {str(e)}"
    
    @abstractmethod
    def _get_help_command(self, command_name: str) -> List[str]:
        """Get the help command for the platform."""
        pass
    
    @abstractmethod
    def _try_alternative_help(self, command_name: str) -> str:
        """Try alternative help methods if primary fails."""
        pass
    
    @abstractmethod
    def _parse_help_text(self, command_name: str, help_text: str) -> CommandSpec:
        """Parse help text into CommandSpec."""
        pass
    
    def _extract_usage(self, help_text: str) -> str:
        """Extract usage line from help text."""
        lines = help_text.split('\n')
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            line_lower = line_stripped.lower()
            # Check if this line is a usage header (like "USAGE" or "Usage:")
            # Match both "usage" (standalone) and "usage:" (with colon)
            is_usage_header = (
                line_lower == 'usage' or
                any(keyword in line_lower for keyword in ['usage:', 'syntax:', 'command:'])
            )
            if is_usage_header:
                # If the line itself contains the usage (like "Usage: command args"), return it
                if ':' in line_stripped:
                    usage_part = line_stripped.split(':', 1)[1].strip()
                    if usage_part:
                        return line_stripped
                # Otherwise, look for the next non-empty line (multi-line format like "USAGE\n  command args")
                for j in range(i + 1, min(i + 5, len(lines))):  # Look ahead up to 5 lines
                    next_line = lines[j].strip()
                    if next_line and not next_line.upper().startswith(('CORE', 'GITHUB', 'ALIAS', 'ADDITIONAL', 'HELP', 'FLAGS', 'OPTIONS', 'EXAMPLES', 'INHERITED')):
                        return next_line
                # If no next line found, return the header line itself
                return line_stripped
        return ""
    
    def _extract_options(self, help_text: str) -> List[OptionSpec]:
        """Extract options from help text."""
        options = []
        lines = help_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if self._is_option_line(line):
                option = self._parse_option_line(line)
                if option:
                    options.append(option)
        
        return options
    
    def _extract_positional_args(self, usage: str) -> List[PositionalArgSpec]:
        """Extract positional arguments from usage line."""
        if not usage:
            return []
        
        # Remove command name and options from usage line
        # Example: "cp [OPTION]... [-T] SOURCE DEST" -> "SOURCE DEST"
        usage_clean = usage.lower()
        
        # Find the command name and remove it
        # Skip "Usage:" prefix if present
        usage_clean = re.sub(r'^usage:\s*', '', usage_clean, flags=re.IGNORECASE)
        
        command_match = re.search(r'^(\w+)', usage_clean)
        if command_match:
            command_name = command_match.group(1)
            usage_clean = usage_clean.replace(command_name, '', 1)
        
        # Remove common option patterns more comprehensively
        option_patterns = [
            r'\[option\]\.\.\.',
            r'\[option\]',
            r'\[flags?\]',  # Match [flags] or [flag]
            r'\[flag\]',
            r'\[-t\]',
            r'\[-h\]',
            r'\[-l\]',
            r'\[-p\]',
            r'\[-o\w*\]',
            r'\[-d\w*\]',
            r'\[-d\s+\w+\]',
            r'\[-h\]',
            r'\[-l\]',
            r'\[-p\]',
            r'\[-olevel\]',
            r'\[-d\s+debugopts\]',
        ]
        
        for pattern in option_patterns:
            usage_clean = re.sub(pattern, '', usage_clean, flags=re.IGNORECASE)
        
        # Clean up extra spaces and empty parts
        usage_clean = re.sub(r'\s+', ' ', usage_clean).strip()
        
        if not usage_clean:
            return []
        
        # Parse positional arguments
        args = []
        parts = usage_clean.split()
        
        for part in parts:
            part = part.strip()
            if not part or part == ':':
                continue
                
            # Determine if argument is required (not in brackets)
            required = not (part.startswith('[') and part.endswith(']'))
            
            # Remove brackets if present
            if part.startswith('[') and part.endswith(']'):
                part = part[1:-1]
            
            # Check if variadic (ends with ...)
            variadic = part.endswith('...')
            if variadic:
                part = part[:-3]
            
            # Skip empty parts
            if not part:
                continue
            
            # Infer type hint
            type_hint = self._infer_positional_type(part)
            
            args.append(PositionalArgSpec(
                name=part.upper(),
                required=required,
                variadic=variadic,
                type_hint=type_hint
            ))
        
        return args
    
    def _infer_positional_type(self, arg_name: str) -> str:
        """Infer type hint for positional argument."""
        arg_lower = arg_name.lower()
        
        if any(word in arg_lower for word in ['file', 'path', 'directory', 'dir', 'source', 'dest', 'target']):
            return 'path'
        elif any(word in arg_lower for word in ['pattern', 'string', 'text', 'name']):
            return 'str'
        elif any(word in arg_lower for word in ['number', 'count', 'size', 'port']):
            return 'int'
        else:
            return 'str'
    
    @abstractmethod
    def _is_option_line(self, line: str) -> bool:
        """Check if a line contains an option definition."""
        pass
    
    @abstractmethod
    def _parse_option_line(self, line: str) -> Optional[OptionSpec]:
        """Parse a single option line."""
        pass
    
    def _infer_type_hint(self, description: str) -> Optional[str]:
        """Infer type hint from option description."""
        if not description:
            return None
            
        description_lower = description.lower()
        
        if any(word in description_lower for word in ['file', 'path', 'directory']):
            return 'path'
        elif any(word in description_lower for word in ['number', 'count', 'size']):
            return 'int'
        elif any(word in description_lower for word in ['verbose', 'quiet', 'debug']):
            return 'bool'
        else:
            return 'str'
