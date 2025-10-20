"""
Windows command parser for UCW.

This module handles parsing of Windows command help text (command /? output)
and extracting command specifications.
"""

import re
import subprocess
from typing import List, Optional

from .base import BaseParser
from models import CommandSpec, OptionSpec, PositionalArgSpec


class WindowsParser(BaseParser):
    """Parser for Windows command help text."""
    
    def __init__(self, timeout: int = 10):
        super().__init__(timeout)
    
    def _get_help_command(self, command_name: str) -> List[str]:
        """Get Windows help command."""
        return [command_name, '/?']
    
    def _try_alternative_help(self, command_name: str) -> str:
        """Try alternative help methods for Windows."""
        # Try with /help instead of /?
        try:
            result = subprocess.run(
                [command_name, '/help'],
                capture_output=True,
                text=True,
                shell=True,  # Windows commands need shell=True
                timeout=self.timeout
            )
            # Accept help text if it contains meaningful content, even with non-zero return codes
            if result.stdout.strip() and len(result.stdout.strip()) > 20:
                return result.stdout
        except:
            pass
        
        return f"No help available for {command_name}"
    
    def _parse_help_text(self, command_name: str, help_text: str) -> CommandSpec:
        """Parse Windows help text into CommandSpec."""
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
        """Check if a line contains a Windows option definition."""
        # Windows options typically start with / or -
        # Also handle complex formats like /A[[:]attributes]
        return bool(re.match(r'^\s*[/-][a-zA-Z]', line) or re.match(r'^\s*[/-][a-zA-Z]\[', line))
    
    def _parse_option_line(self, line: str) -> Optional[OptionSpec]:
        """Parse a Windows option line with enhanced patterns for complex formats."""
        # Enhanced patterns to handle complex Windows option formats:
        # /option    Description text
        # /option:value    Description text  
        # /option[[:]attributes]    Description text (complex format)
        # /option[[:]sortorder]    Description text (complex format)
        
        # Try complex pattern first (e.g., /A[[:]attributes])
        # Handle both /A[[:]attributes] and /A    Description formats
        complex_match = re.match(r'^\s*([/-])([a-zA-Z][a-zA-Z0-9]*)\[.*?\]\s+(.+)', line)
        if complex_match:
            prefix, flag_name, description = complex_match.groups()
            flag = f"{prefix}{flag_name}"
            
            # Determine if it takes a value based on content
            takes_value = ':' in line or 'value' in description.lower() or 'specify' in description.lower()
            
            # Infer type hint
            type_hint = self._infer_type_hint(description)
            
            return OptionSpec(
                flag=flag,
                takes_value=takes_value,
                description=description.strip(),
                type_hint=type_hint
            )
        
        # Fall back to simple pattern
        simple_match = re.match(r'^\s*([/-])([a-zA-Z][a-zA-Z0-9]*)(?::([a-zA-Z]+))?\s+(.+)', line)
        if simple_match:
            prefix, flag_name, value_type, description = simple_match.groups()
            flag = f"{prefix}{flag_name}"
            
            # Determine if it takes a value
            takes_value = value_type is not None or ':' in line
            
            # Infer type hint
            type_hint = self._infer_type_hint(description)
            
            return OptionSpec(
                flag=flag,
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
        
        # Look for description in first few lines
        for line in lines[:5]:
            line = line.strip()
            if line and not line.startswith(('Usage:', 'Syntax:', '/', '-')):
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
            
            if in_examples and line and not line.startswith(('Usage:', 'Syntax:', '/', '-')):
                examples.append(line)
            elif in_examples and line.startswith(('Usage:', 'Syntax:', '/', '-')):
                break
        
        return examples
