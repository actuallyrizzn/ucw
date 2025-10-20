"""
Universal Command Wrapper (UCW) - Main Module

A Python library and CLI utility that analyzes system commands and generates
callable wrappers or MCP plugin files.
"""

import platform
import subprocess
import time
import os
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
    
    def __init__(self, platform_name: Optional[str] = None, 
                 timeout_help: Optional[int] = None,
                 timeout_exec: Optional[int] = None):
        """
        Initialize UCW with platform detection and timeout configuration.
        
        Args:
            platform_name: Platform to use ("windows", "posix", "linux", "auto")
                          Note: "linux" is an alias for "posix"
            timeout_help: Timeout for help commands in seconds (default: 10)
            timeout_exec: Timeout for command execution in seconds (default: 30)
        """
        self.platform = platform_name or self._detect_platform()
        # Normalize platform name - accept "linux" as alias for "posix"
        if self.platform == "linux":
            self.platform = "posix"
        
        # Configure timeouts with environment variable support
        try:
            self.timeout_help = timeout_help or int(os.environ.get('UCW_TIMEOUT_HELP', '10'))
            self.timeout_exec = timeout_exec or int(os.environ.get('UCW_TIMEOUT_EXEC', '30'))
        except ValueError:
            # Use defaults if environment variables are invalid
            self.timeout_help = timeout_help or 10
            self.timeout_exec = timeout_exec or 30
        
        self.parser = self._create_parser()
        self.wrapper_builder = WrapperBuilder(timeout_exec=self.timeout_exec)
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
            return WindowsParser(timeout=self.timeout_help)
        elif self.platform == "posix":
            return PosixParser(timeout=self.timeout_help)
        elif self.platform == "auto":
            # Auto-detect platform
            detected = self._detect_platform()
            if detected == "windows":
                return WindowsParser(timeout=self.timeout_help)
            elif detected == "posix":
                return PosixParser(timeout=self.timeout_help)
            else:
                raise ValueError(f"Unsupported platform: {detected}")
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
