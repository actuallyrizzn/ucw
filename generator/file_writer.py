"""
File writer for UCW.

This module handles writing generated wrappers to CLI files,
including updating existing files with section tagging.
"""

import os
from typing import Optional

from models import CommandSpec
from .wrapper_builder import WrapperBuilder


class FileWriter:
    """Writer for CLI files."""
    
    def __init__(self):
        self.wrapper_builder = WrapperBuilder()
    
    def write_wrapper(self, spec: CommandSpec, wrapper, output_path: str, 
                     update: bool = False) -> str:
        """
        Write wrapper to file.
        
        Args:
            spec: CommandSpec object
            wrapper: CommandWrapper object
            output_path: Path to output file
            update: Whether to update existing file
            
        Returns:
            Path to written file
        """
        if update and os.path.exists(output_path):
            return self._update_existing_file(spec, wrapper, output_path)
        else:
            return self._write_new_file(spec, wrapper, output_path)
    
    def _write_new_file(self, spec: CommandSpec, wrapper, output_path: str) -> str:
        """Write a new CLI file."""
        plugin_code = self.wrapper_builder.generate_mcp_plugin_code(spec)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(plugin_code)
        
        # Make executable on Unix systems
        if os.name != 'nt':
            os.chmod(output_path, 0o755)
        
        return output_path
    
    def _update_existing_file(self, spec: CommandSpec, wrapper, output_path: str) -> str:
        """Update existing CLI file with new wrapper."""
        # Read existing file
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Generate new wrapper code
        plugin_code = self.wrapper_builder.generate_mcp_plugin_code(spec)
        
        # Extract the command-specific parts
        new_wrapper_code = self._extract_wrapper_code(plugin_code, spec.name)
        
        # Update or add wrapper section
        updated_content = self._update_wrapper_section(content, spec.name, new_wrapper_code)
        
        # Write updated file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        return output_path
    
    def _extract_wrapper_code(self, plugin_code: str, command_name: str) -> str:
        """Extract the wrapper-specific code from plugin code."""
        # For now, return the full plugin code
        # In a more sophisticated implementation, we'd extract just the command-specific parts
        return plugin_code
    
    def _update_wrapper_section(self, content: str, command_name: str, 
                               new_code: str) -> str:
        """Update or add a wrapper section in existing content."""
        begin_tag = f"# UCW-BEGIN: {command_name}"
        end_tag = f"# UCW-END: {command_name}"
        
        # Check if section already exists
        if begin_tag in content and end_tag in content:
            # Replace existing section
            start_idx = content.find(begin_tag)
            end_idx = content.find(end_tag) + len(end_tag)
            
            new_content = (
                content[:start_idx] +
                f"{begin_tag}\n{new_code}\n{end_tag}\n" +
                content[end_idx:]
            )
        else:
            # Add new section at the end
            new_content = content + f"\n\n{begin_tag}\n{new_code}\n{end_tag}\n"
        
        return new_content
