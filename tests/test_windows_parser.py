"""
Test Windows parser functionality.

This module tests the WindowsParser class, specifically focusing on the
_try_alternative_help method that was missing the subprocess import.
"""

import pytest
import subprocess
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add the parent directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from parser.windows import WindowsParser


class TestWindowsParser:
    """Test cases for WindowsParser class."""
    
    def test_init(self):
        """Test WindowsParser initialization."""
        parser = WindowsParser()
        assert parser is not None
        assert hasattr(parser, 'timeout')
    
    def test_get_help_command(self):
        """Test _get_help_command method."""
        parser = WindowsParser()
        command = parser._get_help_command("dir")
        assert command == ["dir", "/?"]
    
    def test_try_alternative_help_success(self):
        """Test _try_alternative_help when /help works."""
        parser = WindowsParser()
        
        # Mock subprocess.run to return successful result
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "Help text for command"
        
        with patch('subprocess.run', return_value=mock_result) as mock_run:
            result = parser._try_alternative_help("testcmd")
            
            # Verify subprocess.run was called correctly
            mock_run.assert_called_once_with(
                ["testcmd", "/help"],
                capture_output=True,
                text=True,
                shell=True,
                timeout=parser.timeout
            )
            
            # Verify result
            assert result == "Help text for command"
    
    def test_try_alternative_help_failure(self):
        """Test _try_alternative_help when /help fails."""
        parser = WindowsParser()
        
        # Mock subprocess.run to raise an exception
        with patch('subprocess.run', side_effect=subprocess.TimeoutExpired("testcmd", 10)):
            result = parser._try_alternative_help("testcmd")
            
            # Should return fallback message
            assert result == "No help available for testcmd"
    
    def test_try_alternative_help_nonzero_returncode(self):
        """Test _try_alternative_help when command returns non-zero exit code."""
        parser = WindowsParser()
        
        # Mock subprocess.run to return non-zero return code
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = "Error message"
        
        with patch('subprocess.run', return_value=mock_result):
            result = parser._try_alternative_help("testcmd")
            
            # Should return fallback message
            assert result == "No help available for testcmd"
    
    def test_try_alternative_help_subprocess_import_available(self):
        """Test that subprocess import is available (regression test for issue #2)."""
        parser = WindowsParser()
        
        # This test verifies that the subprocess import is available
        # and the method can be called without NameError
        try:
            # Mock subprocess.run to avoid actual subprocess calls
            with patch('subprocess.run', side_effect=subprocess.TimeoutExpired("testcmd", 10)):
                result = parser._try_alternative_help("testcmd")
                assert result == "No help available for testcmd"
        except NameError as e:
            pytest.fail(f"NameError occurred - subprocess import missing: {e}")
    
    def test_is_option_line(self):
        """Test _is_option_line method."""
        parser = WindowsParser()
        
        # Test valid option lines
        assert parser._is_option_line("/option    Description")
        assert parser._is_option_line("-option    Description")
        assert parser._is_option_line("  /option    Description")
        
        # Test invalid option lines
        assert not parser._is_option_line("option    Description")
        assert not parser._is_option_line("Usage: command")
        assert not parser._is_option_line("")
    
    def test_parse_option_line(self):
        """Test _parse_option_line method."""
        parser = WindowsParser()
        
        # Test valid option line
        option = parser._parse_option_line("/option    Description text")
        assert option is not None
        assert option.flag == "/option"
        assert option.description == "Description text"
        assert not option.takes_value
        
        # Test option with value
        option = parser._parse_option_line("/option:value    Description text")
        assert option is not None
        assert option.flag == "/option"
        assert option.description == "Description text"
        assert option.takes_value
        
        # Test invalid option line
        option = parser._parse_option_line("Not an option line")
        assert option is None


if __name__ == "__main__":
    pytest.main([__file__])
