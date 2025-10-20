"""
File generation and execution tests for UCW.

This module tests generating plugin files and executing them.
"""

import pytest
import subprocess
import sys
import tempfile
import os
from pathlib import Path

# Add the parent directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from __init__ import UniversalCommandWrapper
from generator.file_writer import FileWriter
from models import CommandSpec, OptionSpec


class TestFileGenerationAndExecution:
    """Test cases for file generation and execution."""
    
    def test_generate_plugin_file(self):
        """Test generating a plugin file."""
        ucw = UniversalCommandWrapper()
        
        # Create a mock command spec
        spec = CommandSpec(
            name="testcmd",
            usage="testcmd [options]",
            options=[
                OptionSpec(flag="--verbose", takes_value=False, description="Verbose output"),
                OptionSpec(flag="--output", takes_value=True, description="Output file")
            ],
            positional_args=[],
            description="Test command",
            examples=[]
        )
        
        wrapper = ucw.build_wrapper(spec)
        file_writer = FileWriter()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            temp_file = f.name
        
        try:
            # Generate plugin file
            result_path = file_writer.write_wrapper(spec, wrapper, temp_file)
            assert result_path == temp_file
            assert os.path.exists(temp_file)
            
            # Check file content
            with open(temp_file, 'r', encoding='utf-8') as f:
                content = f.read()
                assert '#!/usr/bin/env python3' in content
                assert 'testcmd Plugin' in content
                assert 'def main():' in content
                assert 'def execute_command' in content
                assert '--verbose' in content
                assert '--output' in content
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_execute_generated_plugin(self):
        """Test executing a generated plugin file."""
        ucw = UniversalCommandWrapper()
        
        # Create a mock command spec
        spec = CommandSpec(
            name="echo",
            usage="echo [options] [text]",
            options=[
                OptionSpec(flag="--verbose", takes_value=False, description="Verbose output")
            ],
            positional_args=[],
            description="Echo command",
            examples=[]
        )
        
        wrapper = ucw.build_wrapper(spec)
        file_writer = FileWriter()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            temp_file = f.name
        
        try:
            # Generate plugin file
            file_writer.write_wrapper(spec, wrapper, temp_file)
            
            # Make file executable
            os.chmod(temp_file, 0o755)
            
            # Execute the plugin
            result = subprocess.run(
                [sys.executable, temp_file, 'execute', '--args', 'hello', 'world'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Should succeed (even if echo fails, plugin should work)
            assert result.returncode == 0
            
            # Should output JSON
            import json
            output = json.loads(result.stdout)
            assert 'status' in output
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_plugin_help_command(self):
        """Test plugin help command."""
        ucw = UniversalCommandWrapper()
        
        # Create a mock command spec
        spec = CommandSpec(
            name="testcmd",
            usage="testcmd [options]",
            options=[
                OptionSpec(flag="--verbose", takes_value=False, description="Verbose output")
            ],
            positional_args=[],
            description="Test command",
            examples=[]
        )
        
        wrapper = ucw.build_wrapper(spec)
        file_writer = FileWriter()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            temp_file = f.name
        
        try:
            # Generate plugin file
            file_writer.write_wrapper(spec, wrapper, temp_file)
            
            # Execute help command
            result = subprocess.run(
                [sys.executable, temp_file, '--help'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Should succeed
            assert result.returncode == 0
            assert 'testcmd Plugin' in result.stdout
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_plugin_execute_command_with_options(self):
        """Test plugin execute command with options."""
        ucw = UniversalCommandWrapper()
        
        # Create a mock command spec
        spec = CommandSpec(
            name="testcmd",
            usage="testcmd [options]",
            options=[
                OptionSpec(flag="--verbose", takes_value=False, description="Verbose output"),
                OptionSpec(flag="--output", takes_value=True, description="Output file")
            ],
            positional_args=[],
            description="Test command",
            examples=[]
        )
        
        wrapper = ucw.build_wrapper(spec)
        file_writer = FileWriter()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            temp_file = f.name
        
        try:
            # Generate plugin file
            file_writer.write_wrapper(spec, wrapper, temp_file)
            
            # Execute with options
            result = subprocess.run(
                [sys.executable, temp_file, 'execute', 
                 '--verbose', '--output', 'test.txt', '--args', 'hello'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Should succeed
            assert result.returncode == 0
            
            # Should output JSON
            import json
            output = json.loads(result.stdout)
            assert 'status' in output
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_update_existing_plugin_file(self):
        """Test updating an existing plugin file."""
        ucw = UniversalCommandWrapper()
        
        # Create first command spec
        spec1 = CommandSpec(
            name="cmd1",
            usage="cmd1 [options]",
            options=[
                OptionSpec(flag="--option1", takes_value=False, description="Option 1")
            ],
            positional_args=[],
            description="Command 1",
            examples=[]
        )
        
        # Create second command spec
        spec2 = CommandSpec(
            name="cmd2",
            usage="cmd2 [options]",
            options=[
                OptionSpec(flag="--option2", takes_value=False, description="Option 2")
            ],
            positional_args=[],
            description="Command 2",
            examples=[]
        )
        
        wrapper1 = ucw.build_wrapper(spec1)
        wrapper2 = ucw.build_wrapper(spec2)
        file_writer = FileWriter()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            temp_file = f.name
        
        try:
            # Generate first plugin file
            file_writer.write_wrapper(spec1, wrapper1, temp_file)
            
            # Check initial content
            with open(temp_file, 'r', encoding='utf-8') as f:
                content1 = f.read()
                assert 'cmd1 Plugin' in content1
                assert '--option1' in content1
            
            # Update with second command
            file_writer.write_wrapper(spec2, wrapper2, temp_file, update=True)
            
            # Check updated content
            with open(temp_file, 'r', encoding='utf-8') as f:
                content2 = f.read()
                assert 'cmd2 Plugin' in content2
                assert '--option2' in content2
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_plugin_file_permissions(self):
        """Test that generated plugin files have correct permissions."""
        ucw = UniversalCommandWrapper()
        
        # Create a mock command spec
        spec = CommandSpec(
            name="testcmd",
            usage="testcmd [options]",
            options=[],
            positional_args=[],
            description="Test command",
            examples=[]
        )
        
        wrapper = ucw.build_wrapper(spec)
        file_writer = FileWriter()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            temp_file = f.name
        
        try:
            # Generate plugin file
            file_writer.write_wrapper(spec, wrapper, temp_file)
            
            # Check file permissions (on Unix systems)
            if os.name != 'nt':
                stat_info = os.stat(temp_file)
                assert stat_info.st_mode & 0o755 == 0o755
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_plugin_file_encoding(self):
        """Test that generated plugin files use UTF-8 encoding."""
        ucw = UniversalCommandWrapper()
        
        # Create a mock command spec with Unicode characters
        spec = CommandSpec(
            name="testcmd",
            usage="testcmd [options]",
            options=[
                OptionSpec(flag="--unicode", takes_value=False, description="Unicode option: 测试")
            ],
            positional_args=[],
            description="Test command with Unicode: 测试",
            examples=[]
        )
        
        wrapper = ucw.build_wrapper(spec)
        file_writer = FileWriter()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            temp_file = f.name
        
        try:
            # Generate plugin file
            file_writer.write_wrapper(spec, wrapper, temp_file)
            
            # Check file content with UTF-8 encoding
            with open(temp_file, 'r', encoding='utf-8') as f:
                content = f.read()
                assert '测试' in content
                assert 'Unicode option: 测试' in content
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


if __name__ == "__main__":
    pytest.main([__file__])
