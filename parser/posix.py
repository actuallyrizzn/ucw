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
    
    def __init__(self, timeout: int = 10):
        super().__init__(timeout)
    
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
        
        return None
    
    def _parse_help_text(self, command_name: str, help_text: str) -> CommandSpec:
        """Parse POSIX help text into CommandSpec."""
        usage = self._extract_usage(help_text)
        options = self._extract_options(help_text)
        positional_args = self._extract_positional_args(usage)
        description = self._extract_description(help_text)
        examples = self._extract_examples(help_text)
        
        return CommandSpec(
            name=command_name,
            usage=usage,
            options=options,
            positional_args=positional_args,
            description=description,
            examples=examples
        )
    
    def _is_option_line(self, line: str) -> bool:
        """Check if a line contains a POSIX option definition."""
        # POSIX options typically start with - or --
        # Handle both short options (-a) and long options (--all)
        return bool(re.match(r'^\s*-[a-zA-Z]', line) or re.match(r'^\s*--[a-zA-Z]', line))
    
    def _parse_option_line(self, line: str) -> Optional[OptionSpec]:
        """Parse a POSIX option line with enhanced patterns for complex formats."""
        # Enhanced patterns to handle complex POSIX option formats:
        # -o, --option    Description text
        # -o, --option=ARG    Description text
        # --option[=ARG]    Description text
        # --option=SIZE    Description text
        # -c[:<stream_spec>] <codec>    Description text (complex format)
        # --format-sort SORTORDER    Description text (complex format)
        
        # More comprehensive regex to handle various option formats
        patterns = [
            # Complex option with brackets: -c[:<stream_spec>] <codec>    description
            r'^\s*(-[a-zA-Z])(?:\[[^\]]*\])?\s*<(\w+)>\s*(.*)',
            # Long option with equals: --block-size=SIZE    description (most specific first)
            r'^\s*(--[a-zA-Z][a-zA-Z0-9-]*)=(\w+)\s*(.*)',
            # Short and long options: -a, --all    description
            r'^\s*(-[a-zA-Z])(?:,\s*(--[a-zA-Z][a-zA-Z0-9-]*))?\s*(.*)',
            # Long option only: --all    description
            r'^\s*(--[a-zA-Z][a-zA-Z0-9-]*)\s*(.*)',
        ]
        
        for pattern in patterns:
            match = re.match(pattern, line)
            if match:
                groups = match.groups()
                if len(groups) == 3:  # Short and long options or option with value
                    if groups[1] and ('=' in line or '<' in line):  # Option with value like --width=COLS or -c <codec>
                        primary_flag, value, description = groups
                    else:  # Short and long options
                        short_flag, long_flag, description = groups
                        primary_flag = long_flag if long_flag else short_flag
                elif len(groups) == 2:  # Long option only
                    primary_flag, description = groups
                else:
                    continue
                
                # Handle empty description
                if not description:
                    description = ""
                
                # Determine if it takes a value
                takes_value = '=' in line or any(word in description.upper() for word in ['ARG', 'SIZE', 'WORD', 'COLS', 'PATTERN', 'WHEN'])
                
                # Infer type hint
                type_hint = self._infer_type_hint(description)
                
                return OptionSpec(
                    flag=primary_flag,
                    takes_value=takes_value,
                    description=description.strip(),
                    type_hint=type_hint
                )
        
        return None
    
    def _extract_description(self, help_text: str) -> str:
        """Extract command description from help text."""
        # If help text contains error messages, return empty description
        if any(error_msg in help_text for error_msg in [
            "Failed to get help", "Help command timed out", "No help available"
        ]):
            return ""
        
        lines = help_text.split('\n')
        
        # Look for NAME section first (man page format)
        in_name_section = False
        for line in lines:
            line = line.strip()
            if line.startswith('NAME'):
                in_name_section = True
                continue
            elif in_name_section and line and not line.startswith(('SYNOPSIS', 'DESCRIPTION', 'OPTIONS')):
                # Extract description from NAME line like "ls - list directory contents"
                if ' - ' in line:
                    return line.split(' - ', 1)[1].strip()
                elif line and not line.startswith('-'):
                    return line
            elif in_name_section and line.startswith(('SYNOPSIS', 'DESCRIPTION', 'OPTIONS')):
                break
        
        # Fallback: Look for description in first few lines
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
