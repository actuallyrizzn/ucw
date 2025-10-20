"""
Universal Command Wrapper (UCW) - Main Module

A Python library and CLI utility that analyzes system commands and generates
callable wrappers or MCP plugin files.
"""

import platform
import subprocess
import time
from typing import Optional, Union

from models import CommandSpec, ExecutionResult
from parser.base import BaseParser
from parser.windows import WindowsParser
from parser.posix import PosixParser
from generator.wrapper_builder import WrapperBuilder
from generator.file_writer import FileWriter
from wrapper import CommandWrapper


class UniversalCommandWrapper:
    """Main UCW class for command analysis and wrapper generation."""
    
    def __init__(self, platform_name: Optional[str] = None):
        """
        Initialize UCW with platform detection.
        
        Args:
            platform_name: Platform to use ("windows", "posix", "linux", "auto")
                          Note: "linux" is an alias for "posix"
        """
        self.platform = platform_name or self._detect_platform()
        # Normalize platform name - accept "linux" as alias for "posix"
        if self.platform == "linux":
            self.platform = "posix"
        self.parser = self._create_parser()
        self.wrapper_builder = WrapperBuilder()
        self.file_writer = FileWriter()
    
    def _detect_platform(self) -> str:
        """Detect the current platform."""
        system = platform.system().lower()
        if system == "windows":
            return "windows"
        elif system in ["linux", "darwin"]:
            return "posix"
        else:
            raise ValueError(f"Unsupported platform: {system}")
    
    def _create_parser(self) -> BaseParser:
        """Create the appropriate parser for the platform."""
        if self.platform == "windows":
            return WindowsParser()
        elif self.platform == "posix":
            return PosixParser()
        else:
            raise ValueError(f"Unknown platform: {self.platform}")
    
    def parse_command(self, command_name: str) -> CommandSpec:
        """
        Parse a command's help/man page into structured specification.
        
        Args:
            command_name: Name of the command to parse
            
        Returns:
            CommandSpec object with parsed information
        """
        return self.parser.parse_command(command_name)
    
    def build_wrapper(self, spec: CommandSpec) -> "CommandWrapper":
        """
        Build a callable wrapper from a command specification.
        
        Args:
            spec: CommandSpec object
            
        Returns:
            CommandWrapper object
        """
        return self.wrapper_builder.build_wrapper(spec)
    
    def write_wrapper(self, command_name: str, output: Optional[str] = None, 
                     update: bool = False) -> Union["CommandWrapper", str]:
        """
        Generate wrapper and optionally write to file.
        
        Args:
            command_name: Name of the command to wrap
            output: Output file path (optional)
            update: Whether to update existing file
            
        Returns:
            CommandWrapper object if no output specified, otherwise file path
        """
        spec = self.parse_command(command_name)
        wrapper = self.build_wrapper(spec)
        
        if output:
            file_path = self.file_writer.write_wrapper(spec, wrapper, output, update)
            return file_path
        else:
            return wrapper
