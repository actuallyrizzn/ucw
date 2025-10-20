"""
Error handling integration tests for UCW.

This module tests error handling in various scenarios.
"""

import pytest
import subprocess
import sys
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add the parent directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from __init__ import UniversalCommandWrapper
from parser.base import BaseParser
from models import CommandSpec, OptionSpec


class TestErrorHandling:
    """Test cases for error handling."""
    
    def test_parse_nonexistent_command(self):
        """Test parsing nonexistent command."""
        ucw = UniversalCommandWrapper()
        
        # Should handle nonexistent commands gracefully
        spec = ucw.parse_command("nonexistent_command_12345")
        assert spec.name == "nonexistent_command_12345"
        assert spec.description == ""
        assert len(spec.options) == 0
    
    def test_parse_command_with_timeout(self):
        """Test parsing command that times out."""
        ucw = UniversalCommandWrapper(timeout_help=1)
        
        # Mock a command that times out
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired("testcmd", 1)
            
            spec = ucw.parse_command("testcmd")
            assert spec.name == "testcmd"
            assert spec.description == ""
            assert len(spec.options) == 0
    
    def test_parse_command_with_exception(self):
        """Test parsing command that raises exception."""
        ucw = UniversalCommandWrapper()
        
        # Mock a command that raises exception
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = Exception("Unexpected error")
            
            spec = ucw.parse_command("testcmd")
            assert spec.name == "testcmd"
            assert spec.description == ""
            assert len(spec.options) == 0
    
    def test_execute_command_with_timeout(self):
        """Test executing command that times out."""
        ucw = UniversalCommandWrapper(timeout_exec=1)
        
        # Create a mock command spec
        spec = CommandSpec(
            name="sleep",
            usage="sleep [seconds]",
            options=[],
            positional_args=[],
            description="Sleep command",
            examples=[]
        )
        
        wrapper = ucw.build_wrapper(spec)
        
        # Mock a command that times out
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired("sleep", 1)
            
            result = wrapper.run("5")
            assert result.success is False
            assert "timed out" in result.stderr
            assert result.return_code == -1
    
    def test_execute_command_with_exception(self):
        """Test executing command that raises exception."""
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
        
        # Mock a command that raises exception
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = Exception("Unexpected error")
            
            result = wrapper.run()
            assert result.success is False
            assert "Command execution failed" in result.stderr
            assert result.return_code == -1
    
    def test_invalid_platform(self):
        """Test invalid platform handling."""
        with pytest.raises(ValueError, match="Unknown platform"):
            UniversalCommandWrapper(platform_name="invalid_platform")
    
    def test_unsupported_system_platform(self):
        """Test unsupported system platform."""
        with patch('platform.system', return_value="unsupported"):
            with pytest.raises(ValueError, match="Unsupported platform"):
                UniversalCommandWrapper(platform_name="auto")
    
    def test_file_write_permission_error(self):
        """Test file write permission error."""
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
        file_writer = ucw.file_writer
        
        # Try to write to a directory (should fail)
        with pytest.raises((PermissionError, IsADirectoryError)):
            file_writer.write_wrapper(spec, wrapper, "/")
    
    def test_file_read_permission_error(self):
        """Test file read permission error."""
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
        file_writer = ucw.file_writer
        
        # Create a file with no read permission
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            temp_file = f.name
        
        try:
            # Remove read permission
            os.chmod(temp_file, 0o000)
            
            # Try to update the file (should fail)
            with pytest.raises(PermissionError):
                file_writer.write_wrapper(spec, wrapper, temp_file, update=True)
            
        finally:
            # Restore permissions and clean up
            os.chmod(temp_file, 0o644)
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_cli_invalid_arguments(self):
        """Test CLI with invalid arguments."""
        # Test missing command name
        result = subprocess.run(
            [sys.executable, 'cli.py', 'wrap'],
            capture_output=True,
            text=True,
            timeout=10
        )
        assert result.returncode != 0
        
        # Test invalid subcommand
        result = subprocess.run(
            [sys.executable, 'cli.py', 'invalid'],
            capture_output=True,
            text=True,
            timeout=10
        )
        assert result.returncode != 0
    
    def test_cli_invalid_platform(self):
        """Test CLI with invalid platform."""
        result = subprocess.run(
            [sys.executable, 'cli.py', 'wrap', 'echo', '--platform', 'invalid'],
            capture_output=True,
            text=True,
            timeout=10
        )
        assert result.returncode != 0
    
    def test_cli_invalid_timeout_values(self):
        """Test CLI with invalid timeout values."""
        # Test negative timeout
        result = subprocess.run(
            [sys.executable, 'cli.py', 'wrap', 'echo', '--timeout-help', '-1'],
            capture_output=True,
            text=True,
            timeout=10
        )
        assert result.returncode != 0
        
        # Test zero timeout
        result = subprocess.run(
            [sys.executable, 'cli.py', 'wrap', 'echo', '--timeout-exec', '0'],
            capture_output=True,
            text=True,
            timeout=10
        )
        assert result.returncode != 0
    
    def test_cli_missing_required_files(self):
        """Test CLI when required files are missing."""
        # Test with non-existent output directory
        result = subprocess.run(
            [sys.executable, 'cli.py', 'wrap', 'echo', '--output', '/nonexistent/dir/file.py'],
            capture_output=True,
            text=True,
            timeout=10
        )
        assert result.returncode != 0
    
    def test_wrapper_builder_invalid_spec(self):
        """Test wrapper builder with invalid spec."""
        from generator.wrapper_builder import WrapperBuilder
        
        builder = WrapperBuilder()
        
        # Test with None spec
        with pytest.raises(AttributeError):
            builder.build_wrapper(None)
        
        # Test with invalid spec type
        with pytest.raises(AttributeError):
            builder.build_wrapper("invalid")
    
    def test_command_wrapper_invalid_spec(self):
        """Test command wrapper with invalid spec."""
        from wrapper import CommandWrapper
        
        # Test with None spec
        with pytest.raises(AttributeError):
            CommandWrapper("test", None)
        
        # Test with invalid spec type
        with pytest.raises(AttributeError):
            CommandWrapper("test", "invalid")
    
    def test_parser_invalid_command_name(self):
        """Test parser with invalid command name."""
        ucw = UniversalCommandWrapper()
        
        # Test with None command name
        with pytest.raises(TypeError):
            ucw.parse_command(None)
        
        # Test with empty command name
        spec = ucw.parse_command("")
        assert spec.name == ""
        assert spec.description == ""
        assert len(spec.options) == 0
    
    def test_environment_variable_invalid_values(self):
        """Test environment variables with invalid values."""
        import os
        
        # Set invalid environment variables
        os.environ['UCW_TIMEOUT_HELP'] = 'invalid'
        os.environ['UCW_TIMEOUT_EXEC'] = 'invalid'
        
        try:
            # Should handle invalid values gracefully
            ucw = UniversalCommandWrapper()
            
            # Should fall back to defaults
            assert ucw.timeout_help == 10
            assert ucw.timeout_exec == 30
            
        finally:
            # Clean up environment variables
            if 'UCW_TIMEOUT_HELP' in os.environ:
                del os.environ['UCW_TIMEOUT_HELP']
            if 'UCW_TIMEOUT_EXEC' in os.environ:
                del os.environ['UCW_TIMEOUT_EXEC']
    
    def test_generated_plugin_invalid_json(self):
        """Test generated plugin with invalid JSON input."""
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
        file_writer = ucw.file_writer
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            temp_file = f.name
        
        try:
            # Generate plugin file
            file_writer.write_wrapper(spec, wrapper, temp_file)
            
            # Execute with invalid JSON
            result = subprocess.run(
                [sys.executable, temp_file, 'execute', '--options', 'invalid json'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # Should handle invalid JSON gracefully
            assert result.returncode == 0
            
            # Should output error status
            import json
            output = json.loads(result.stdout)
            assert output['status'] == 'error'
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


if __name__ == "__main__":
    pytest.main([__file__])
