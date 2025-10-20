"""
Unit tests for base parser.

This module tests the BaseParser abstract base class functionality.
"""

import pytest
import subprocess
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add the parent directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from parser.base import BaseParser
from models import CommandSpec, OptionSpec


class ConcreteParser(BaseParser):
    """Concrete implementation of BaseParser for testing."""
    
    def _get_help_command(self, command_name: str):
        """Return help command for testing."""
        return [command_name, "--help"]
    
    def _parse_help_text(self, command_name: str, help_text: str) -> CommandSpec:
        """Parse help text for testing."""
        return CommandSpec(
            name=command_name,
            usage=f"{command_name} [options]",
            options=[
                OptionSpec(flag="--test", takes_value=False, description="Test option")
            ],
            positional_args=[],
            description="Test command",
            examples=[]
        )
    
    def _is_option_line(self, line: str) -> bool:
        """Check if line contains option information."""
        return "--test" in line
    
    def _parse_option_line(self, line: str) -> OptionSpec:
        """Parse option line for testing."""
        if "--test" in line:
            return OptionSpec(flag="--test", takes_value=False, description="Test option")
        return None
    
    def _try_alternative_help(self, command_name: str) -> str:
        """Try alternative help method for testing."""
        return f"Alternative help for {command_name}"


class TestBaseParser:
    """Test cases for BaseParser."""
    
    def test_init(self):
        """Test BaseParser initialization."""
        parser = ConcreteParser(timeout=15)
        assert parser.timeout == 15
        
        # Test default timeout
        parser = ConcreteParser()
        assert parser.timeout == 10
    
    def test_get_help_text_success(self):
        """Test _get_help_text with successful command execution."""
        parser = ConcreteParser()
        
        mock_output = """Test Command Help

Usage: testcmd [options]

Options:
  --test     Test option
  --help     Show this help message
"""
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout=mock_output,
                stderr=""
            )
            
            result = parser._get_help_text("testcmd")
            assert result == mock_output
            mock_run.assert_called_once_with(
                ["testcmd", "--help"],
                capture_output=True,
                text=True,
                shell=False,
                timeout=10
            )
    
    def test_get_help_text_failure(self):
        """Test _get_help_text with failed command execution."""
        parser = ConcreteParser()
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=1,
                stdout="",
                stderr="Command not found"
            )
            
            result = parser._get_help_text("nonexistent")
            # Should try alternative help when main help fails
            assert result == "Alternative help for nonexistent"
    
    def test_get_help_text_timeout(self):
        """Test _get_help_text with timeout."""
        parser = ConcreteParser(timeout=1)
        
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired("testcmd", 1)
            
            result = parser._get_help_text("testcmd")
            # Should return timeout error message
            assert result == "Help command timed out for testcmd"
    
    def test_get_help_text_exception(self):
        """Test _get_help_text with exception."""
        parser = ConcreteParser()
        
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = Exception("Unexpected error")
            
            result = parser._get_help_text("testcmd")
            # Should return exception error message
            assert result == "Failed to get help for testcmd: Unexpected error"
    
    def test_parse_command_success(self):
        """Test parse_command with successful execution."""
        parser = ConcreteParser()
        
        mock_help_text = """Test Command Help

Usage: testcmd [options]

Options:
  --test     Test option
"""
        
        with patch.object(parser, '_get_help_text', return_value=mock_help_text):
            spec = parser.parse_command("testcmd")
            
            assert spec.name == "testcmd"
            assert spec.description == "Test command"
            assert len(spec.options) == 1
            assert spec.options[0].flag == "--test"
    
    def test_parse_command_no_help(self):
        """Test parse_command when no help is available."""
        parser = ConcreteParser()
        
        with patch.object(parser, '_get_help_text', return_value=""):
            spec = parser.parse_command("testcmd")
            
            assert spec.name == "testcmd"
            assert spec.description == "Test command"
            assert len(spec.options) == 1  # Still gets the test option from mock
    
    def test_abstract_methods(self):
        """Test that abstract methods raise NotImplementedError."""
        # Test that we can't instantiate BaseParser directly
        with pytest.raises(TypeError):
            BaseParser()
    
    def test_timeout_configuration(self):
        """Test timeout configuration in subprocess calls."""
        parser = ConcreteParser(timeout=30)
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="test output",
                stderr=""
            )
            
            parser._get_help_text("testcmd")
            
            # Check that timeout was passed correctly
            mock_run.assert_called_once_with(
                ["testcmd", "--help"],
                capture_output=True,
                text=True,
                shell=False,
                timeout=30
            )
    
    def test_subprocess_security(self):
        """Test that subprocess.run is called securely."""
        parser = ConcreteParser()
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="test output",
                stderr=""
            )
            
            parser._get_help_text("testcmd")
            
            # Check that shell=True is not used (security)
            call_args = mock_run.call_args
            assert 'shell' not in call_args.kwargs or call_args.kwargs.get('shell') is False
            
            # Check that command is passed as list, not string
            assert isinstance(call_args.args[0], list)
            assert call_args.args[0] == ["testcmd", "--help"]


if __name__ == "__main__":
    pytest.main([__file__])
