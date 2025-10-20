"""
Basic tests for UCW functionality.

This module provides pytest tests to verify UCW is working correctly.
"""

import pytest
import platform
import sys
from pathlib import Path

# Add the parent directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from __init__ import UniversalCommandWrapper


@pytest.mark.skipif(platform.system().lower() != "windows", reason="Windows-specific test")
def test_windows_parser():
    """Test Windows command parsing."""
    ucw = UniversalCommandWrapper(platform_name="windows")
    
    # Test with a simple Windows command
    spec = ucw.parse_command("dir")
    assert spec is not None
    assert spec.name == "dir"
    assert isinstance(spec.usage, str)
    assert isinstance(spec.options, list)
    
    # Test wrapper generation
    wrapper = ucw.build_wrapper(spec)
    assert wrapper is not None
    assert wrapper.command_name == "dir"
    
    # Test execution (just check it doesn't crash)
    result = wrapper.run()
    assert result is not None
    assert hasattr(result, 'return_code')
    assert isinstance(result.return_code, int)


@pytest.mark.skipif(platform.system().lower() == "windows", reason="POSIX-specific test")
def test_posix_parser():
    """Test POSIX command parsing."""
    ucw = UniversalCommandWrapper(platform_name="posix")
    
    # Test with a simple POSIX command
    spec = ucw.parse_command("ls")
    assert spec is not None
    assert spec.name == "ls"
    assert isinstance(spec.usage, str)
    assert isinstance(spec.options, list)
    
    # Test wrapper generation
    wrapper = ucw.build_wrapper(spec)
    assert wrapper is not None
    assert wrapper.command_name == "ls"
    
    # Test execution (just check it doesn't crash)
    result = wrapper.run()
    assert result is not None
    assert hasattr(result, 'return_code')
    assert isinstance(result.return_code, int)


def test_file_generation():
    """Test CLI file generation."""
    ucw = UniversalCommandWrapper()
    
    # Generate a test CLI file
    test_file = "test_cli.py"
    file_path = ucw.write_wrapper("dir", output=test_file)
    
    assert file_path is not None
    assert isinstance(file_path, str)
    
    # Check if file exists and is readable
    assert Path(file_path).exists()
    assert Path(file_path).is_file()
    
    # Clean up
    Path(file_path).unlink()
    assert not Path(file_path).exists()


def test_platform_detection():
    """Test automatic platform detection."""
    ucw = UniversalCommandWrapper()
    
    # Should detect platform automatically
    assert ucw.platform in ["windows", "posix"]
    
    # Should create appropriate parser
    assert ucw.parser is not None


def test_timeout_configuration():
    """Test timeout configuration."""
    ucw = UniversalCommandWrapper(timeout_help=20, timeout_exec=60)
    
    assert ucw.timeout_help == 20
    assert ucw.timeout_exec == 60
    
    # Parser should receive the timeout
    assert ucw.parser.timeout == 20
    
    # Wrapper builder should receive the timeout
    assert ucw.wrapper_builder.timeout_exec == 60


def test_linux_platform_alias():
    """Test that 'linux' is accepted as an alias for 'posix'."""
    ucw = UniversalCommandWrapper(platform_name="linux")
    
    # Should normalize to 'posix'
    assert ucw.platform == "posix"
    
    # Should create PosixParser
    from parser.posix import PosixParser
    assert isinstance(ucw.parser, PosixParser)


if __name__ == "__main__":
    pytest.main([__file__])
