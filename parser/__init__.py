"""
Base parser class for command help/man page parsing.

This module provides the abstract base class and common functionality
for parsing command help text across different platforms.
"""

import subprocess
import re
from abc import ABC, abstractmethod
from typing import List, Optional

from models import CommandSpec, OptionSpec


class BaseParser(ABC):
    """Abstract base class for command parsers."""
    
    def __init__(self):
        self.timeout = 10  # Default timeout for help commands
    
    def parse_command(self, command_name: str) -> CommandSpec:
        """
        Parse a command's help text into structured specification.
        
        Args:
            command_name: Name of the command to parse
            
        Returns:
            CommandSpec object with parsed information
        """
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
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                shell=True
            )
            
            if result.returncode == 0:
                return result.stdout
            else:
                # Try alternative help methods
                return self._try_alternative_help(command_name)
                
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
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in ['usage:', 'syntax:', 'command:']):
                return line
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
