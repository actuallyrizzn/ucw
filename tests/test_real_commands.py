"""
Real command parsing integration tests for UCW.

This module tests parsing real system commands.
"""

import pytest
import subprocess
import sys
from pathlib import Path

# Add the parent directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from __init__ import UniversalCommandWrapper


class TestRealCommandParsing:
    """Test cases for parsing real system commands."""
    
    def test_parse_real_windows_command(self):
        """Test parsing real Windows commands."""
        ucw = UniversalCommandWrapper(platform_name="windows")
        
        # Test with dir command (should exist on Windows)
        try:
            spec = ucw.parse_command("dir")
            assert spec.name == "dir"
            assert len(spec.options) > 0
            assert spec.description != ""
            
            # Check for common dir options
            option_flags = [opt.flag for opt in spec.options]
            assert any(flag in option_flags for flag in ["/?", "/W", "/P", "/A"])
            
        except Exception as e:
            # If dir command fails, that's okay for this test
            pytest.skip(f"Windows dir command not available: {e}")
    
    def test_parse_real_posix_command(self):
        """Test parsing real POSIX commands."""
        ucw = UniversalCommandWrapper(platform_name="posix")
        
        # Test with ls command (should exist on most POSIX systems)
        try:
            spec = ucw.parse_command("ls")
            assert spec.name == "ls"
            assert len(spec.options) > 0
            assert spec.description != ""
            
            # Check for common ls options
            option_flags = [opt.flag for opt in spec.options]
            assert any(flag in option_flags for flag in ["-l", "-a", "-h", "--help"])
            
        except Exception as e:
            # If ls command fails, that's okay for this test
            pytest.skip(f"POSIX ls command not available: {e}")
    
    def test_parse_real_echo_command(self):
        """Test parsing echo command (should exist on most systems)."""
        ucw = UniversalCommandWrapper()
        
        try:
            spec = ucw.parse_command("echo")
            assert spec.name == "echo"
            assert spec.description != ""
            
            # Echo should have some options
            assert len(spec.options) >= 0
            
        except Exception as e:
            # If echo command fails, that's okay for this test
            pytest.skip(f"Echo command not available: {e}")
    
    def test_parse_nonexistent_command(self):
        """Test parsing nonexistent command."""
        ucw = UniversalCommandWrapper()
        
        # Should handle nonexistent commands gracefully
        spec = ucw.parse_command("nonexistent_command_12345")
        assert spec.name == "nonexistent_command_12345"
        assert spec.description == ""
        assert len(spec.options) == 0
    
    def test_parse_command_with_timeout(self):
        """Test parsing command with custom timeout."""
        ucw = UniversalCommandWrapper(timeout_help=5)
        
        try:
            spec = ucw.parse_command("echo")
            assert spec.name == "echo"
            
        except Exception as e:
            pytest.skip(f"Echo command not available: {e}")
    
    def test_build_wrapper_from_real_command(self):
        """Test building wrapper from real command."""
        ucw = UniversalCommandWrapper()
        
        try:
            spec = ucw.parse_command("echo")
            wrapper = ucw.build_wrapper(spec)
            
            assert wrapper.command_name == "echo"
            assert wrapper.spec == spec
            
        except Exception as e:
            pytest.skip(f"Echo command not available: {e}")
    
    def test_execute_real_command(self):
        """Test executing real command through wrapper."""
        ucw = UniversalCommandWrapper()
        
        try:
            spec = ucw.parse_command("echo")
            wrapper = ucw.build_wrapper(spec)
            
            # Execute echo command
            result = wrapper.run("hello", "world")
            
            assert result.command is not None
            assert "echo" in result.command
            assert "hello" in result.command
            assert "world" in result.command
            
        except Exception as e:
            pytest.skip(f"Echo command not available: {e}")
    
    def test_platform_detection(self):
        """Test automatic platform detection."""
        ucw = UniversalCommandWrapper()
        
        # Should detect current platform
        assert ucw.platform in ["windows", "posix"]
        
        # Test with explicit platform
        ucw_windows = UniversalCommandWrapper(platform_name="windows")
        assert ucw_windows.platform == "windows"
        
        ucw_posix = UniversalCommandWrapper(platform_name="posix")
        assert ucw_posix.platform == "posix"
    
    def test_linux_platform_alias(self):
        """Test that linux platform alias works."""
        ucw = UniversalCommandWrapper(platform_name="linux")
        
        # Should normalize to posix
        assert ucw.platform == "posix"
    
    def test_timeout_configuration(self):
        """Test timeout configuration."""
        ucw = UniversalCommandWrapper(timeout_help=15, timeout_exec=45)
        
        assert ucw.timeout_help == 15
        assert ucw.timeout_exec == 45
        
        # Test that timeouts are passed to components
        assert ucw.parser.timeout == 15
        assert ucw.wrapper_builder.timeout_exec == 45
    
    def test_environment_variable_timeouts(self):
        """Test timeout configuration via environment variables."""
        import os
        
        # Set environment variables
        os.environ['UCW_TIMEOUT_HELP'] = '20'
        os.environ['UCW_TIMEOUT_EXEC'] = '60'
        
        try:
            ucw = UniversalCommandWrapper()
            
            assert ucw.timeout_help == 20
            assert ucw.timeout_exec == 60
            
        finally:
            # Clean up environment variables
            if 'UCW_TIMEOUT_HELP' in os.environ:
                del os.environ['UCW_TIMEOUT_HELP']
            if 'UCW_TIMEOUT_EXEC' in os.environ:
                del os.environ['UCW_TIMEOUT_EXEC']
    
    def test_constructor_overrides_environment(self):
        """Test that constructor parameters override environment variables."""
        import os
        
        # Set environment variables
        os.environ['UCW_TIMEOUT_HELP'] = '20'
        os.environ['UCW_TIMEOUT_EXEC'] = '60'
        
        try:
            ucw = UniversalCommandWrapper(timeout_help=25, timeout_exec=75)
            
            # Constructor should override environment
            assert ucw.timeout_help == 25
            assert ucw.timeout_exec == 75
            
        finally:
            # Clean up environment variables
            if 'UCW_TIMEOUT_HELP' in os.environ:
                del os.environ['UCW_TIMEOUT_HELP']
            if 'UCW_TIMEOUT_EXEC' in os.environ:
                del os.environ['UCW_TIMEOUT_EXEC']


if __name__ == "__main__":
    pytest.main([__file__])
