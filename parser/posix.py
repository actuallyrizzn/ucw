"""
POSIX command parser for UCW.

This module handles parsing of Linux/Unix command help text (--help and man pages)
and extracting command specifications.
"""

import re
import subprocess
from typing import List, Optional

from .base import BaseParser
from models import CommandSpec, OptionSpec


class PosixParser(BaseParser):
    """Parser for POSIX command help text."""
    
    def _get_help_command(self, command_name: str) -> List[str]:
        """Get POSIX help command."""
        return [command_name, '--help']
    
    def _try_alternative_help(self, command_name: str) -> str:
        """Try alternative help methods for POSIX."""
        # Try man page
        try:
            result = subprocess.run(
                ['man', command_name],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            if result.returncode == 0:
                return result.stdout
        except:
            pass
        
        # Try -h instead of --help
        try:
            result = subprocess.run(
                [command_name, '-h'],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            if result.returncode == 0:
                return result.stdout
        except:
            pass
        
        return f"No help available for {command_name}"
    
    def _parse_help_text(self, command_name: str, help_text: str) -> CommandSpec:
        """Parse POSIX help text into CommandSpec."""
        usage = self._extract_usage(help_text)
        options = self._extract_options(help_text)
        description = self._extract_description(help_text)
        examples = self._extract_examples(help_text)
        
        return CommandSpec(
            name=command_name,
            usage=usage,
            options=options,
            description=description,
            examples=examples
        )
    
    def _is_option_line(self, line: str) -> bool:
        """Check if a line contains a POSIX option definition."""
        # POSIX options typically start with - or --
        return bool(re.match(r'^\s*-[a-zA-Z]', line))
    
    def _parse_option_line(self, line: str) -> Optional[OptionSpec]:
        """Parse a POSIX option line."""
        # Pattern: -o, --option    Description text
        # Pattern: -o, --option=ARG    Description text
        # Pattern: --option[=ARG]    Description text
        
        # Handle short and long options
        match = re.match(r'^\s*(-[a-zA-Z](?:,\s*--[a-zA-Z][a-zA-Z0-9-]*)?(?:=\w+)?)\s+(.+)', line)
        if not match:
            return None
        
        flag_part, description = match.groups()
        
        # Extract flags
        flags = [f.strip() for f in flag_part.split(',')]
        primary_flag = flags[0]
        
        # Determine if it takes a value
        takes_value = '=' in flag_part or 'ARG' in description.upper()
        
        # Infer type hint
        type_hint = self._infer_type_hint(description)
        
        return OptionSpec(
            flag=primary_flag,
            takes_value=takes_value,
            description=description.strip(),
            type_hint=type_hint
        )
    
    def _extract_description(self, help_text: str) -> str:
        """Extract command description from help text."""
        lines = help_text.split('\n')
        
        # Look for description in first few lines
        for line in lines[:10]:
            line = line.strip()
            if line and not line.startswith(('Usage:', 'SYNOPSIS:', '-', 'Options:')):
                return line
        
        return ""
    
    def _extract_examples(self, help_text: str) -> List[str]:
        """Extract examples from help text."""
        examples = []
        lines = help_text.split('\n')
        in_examples = False
        
        for line in lines:
            line = line.strip()
            if 'example' in line.lower():
                in_examples = True
                continue
            
            if in_examples and line and not line.startswith(('Usage:', 'SYNOPSIS:', '-', 'Options:')):
                examples.append(line)
            elif in_examples and line.startswith(('Usage:', 'SYNOPSIS:', '-', 'Options:')):
                break
        
        return examples
