"""
CLI integration tests for UCW.

This module tests the command-line interface functionality.
"""

import pytest
import subprocess
import sys
import tempfile
import os
from pathlib import Path

# Add the parent directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from cli import main, setup_wrap_command, setup_parse_command, setup_execute_command
from __init__ import UniversalCommandWrapper


class TestCLIIntegration:
    """Test cases for CLI integration."""
    
    def test_cli_main_without_args(self):
        """Test CLI main function without arguments."""
        # Test that main() handles missing arguments gracefully
        with pytest.raises(SystemExit):
            main()
    
    def test_setup_wrap_command_parser(self):
        """Test that wrap command parser is set up correctly."""
        import argparse
        
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()
        
        setup_wrap_command(subparsers)
        
        # Test parsing wrap command
        args = parser.parse_args(['wrap', 'testcmd'])
        assert args.command_name == 'testcmd'
        assert args.platform == 'auto'
        assert args.timeout_help == 10
        assert args.timeout_exec == 30
        assert args.output is None
        assert args.update is False
    
    def test_setup_wrap_command_with_options(self):
        """Test wrap command with all options."""
        import argparse
        
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()
        
        setup_wrap_command(subparsers)
        
        # Test parsing wrap command with options
        args = parser.parse_args([
            'wrap', 'testcmd',
            '--platform', 'windows',
            '--timeout-help', '15',
            '--timeout-exec', '45',
            '--output', 'test.py',
            '--update'
        ])
        
        assert args.command_name == 'testcmd'
        assert args.platform == 'windows'
        assert args.timeout_help == 15
        assert args.timeout_exec == 45
        assert args.output == 'test.py'
        assert args.update is True
    
    def test_setup_parse_command_parser(self):
        """Test that parse command parser is set up correctly."""
        import argparse
        
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()
        
        setup_parse_command(subparsers)
        
        # Test parsing parse command
        args = parser.parse_args(['parse', 'testcmd'])
        assert args.command_name == 'testcmd'
        assert args.platform == 'auto'
        assert args.timeout_help == 10
    
    def test_setup_execute_command_parser(self):
        """Test that execute command parser is set up correctly."""
        import argparse
        
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()
        
        setup_execute_command(subparsers)
        
        # Test parsing execute command
        args = parser.parse_args(['execute', 'testcmd'])
        assert args.command_name == 'testcmd'
        assert args.platform == 'auto'
        assert args.timeout_help == 10
        assert args.timeout_exec == 30
        assert args.args is None
        assert args.options == '{}'
    
    def test_execute_wrap_command_basic(self):
        """Test basic wrap command execution."""
        from cli import execute_wrap_command
        import argparse
        
        # Create mock args
        args = argparse.Namespace(
            command_name='echo',
            platform='auto',
            timeout_help=10,
            timeout_exec=30,
            output=None,
            update=False
        )
        
        # This should not raise an exception
        result = execute_wrap_command(args)
        assert isinstance(result, dict)
        assert 'status' in result
    
    def test_execute_parse_command_basic(self):
        """Test basic parse command execution."""
        from cli import execute_parse_command
        import argparse
        
        # Create mock args
        args = argparse.Namespace(
            command_name='echo',
            platform='auto',
            timeout_help=10
        )
        
        # This should not raise an exception
        result = execute_parse_command(args)
        assert isinstance(result, dict)
        assert 'status' in result
    
    def test_execute_execute_command_basic(self):
        """Test basic execute command execution."""
        from cli import execute_execute_command
        import argparse
        
        # Create mock args
        args = argparse.Namespace(
            command_name='echo',
            platform='auto',
            timeout_help=10,
            timeout_exec=30,
            args=[],
            options='{}'
        )
        
        # This should not raise an exception
        result = execute_execute_command(args)
        assert isinstance(result, dict)
        assert 'status' in result
    
    def test_cli_help_output(self):
        """Test that CLI shows help output."""
        result = subprocess.run(
            [sys.executable, 'cli.py', '--help'],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert 'Universal Command Wrapper' in result.stdout
        assert 'wrap' in result.stdout
        assert 'parse' in result.stdout
        assert 'execute' in result.stdout
    
    def test_cli_wrap_help(self):
        """Test wrap command help."""
        result = subprocess.run(
            [sys.executable, 'cli.py', 'wrap', '--help'],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert 'wrap' in result.stdout
        assert '--platform' in result.stdout
        assert '--output' in result.stdout
    
    def test_cli_parse_help(self):
        """Test parse command help."""
        result = subprocess.run(
            [sys.executable, 'cli.py', 'parse', '--help'],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert 'parse' in result.stdout
    
    def test_cli_execute_help(self):
        """Test execute command help."""
        result = subprocess.run(
            [sys.executable, 'cli.py', 'execute', '--help'],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert 'execute' in result.stdout
        assert '--args' in result.stdout
        assert '--options' in result.stdout


if __name__ == "__main__":
    pytest.main([__file__])
