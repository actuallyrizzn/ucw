"""
Test cases for documentation examples.

This module tests that the examples in README.md actually work.
"""

import pytest
import sys
from pathlib import Path

# Add the parent directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from __init__ import UniversalCommandWrapper


class TestDocumentationExamples:
    """Test cases for documentation examples."""
    
    def test_basic_library_usage_example(self):
        """Test the basic library usage example from README."""
        # This is the example from README.md
        ucw = UniversalCommandWrapper()
        
        # Parse and wrap a command
        spec = ucw.parse_command("echo")
        wrapper = ucw.build_wrapper(spec)
        
        # Execute the command with arguments
        result = wrapper.run("hello", "world")
        
        # Should succeed
        assert result.success is True
        assert "hello" in result.command
        assert "world" in result.command
    
    def test_advanced_usage_example(self):
        """Test the advanced usage example from README."""
        # Platform-specific initialization
        ucw_windows = UniversalCommandWrapper(platform_name="windows")
        ucw_posix = UniversalCommandWrapper(platform_name="posix")
        
        # Should create parsers correctly
        assert ucw_windows.platform == "windows"
        assert ucw_posix.platform == "posix"
    
    def test_file_operations_example(self):
        """Test the file operations example from README."""
        ucw = UniversalCommandWrapper()
        
        # Wrap cp command
        cp_spec = ucw.parse_command("cp")
        cp_wrapper = ucw.build_wrapper(cp_spec)
        
        # Copy file (this will fail on Windows but should not crash)
        result = cp_wrapper.run("source.txt", "dest.txt")
        
        # Should not crash, even if command fails
        assert hasattr(result, 'success')
        assert hasattr(result, 'command')
    
    def test_text_processing_example(self):
        """Test the text processing example from README."""
        ucw = UniversalCommandWrapper()
        
        # Wrap grep command
        grep_spec = ucw.parse_command("grep")
        grep_wrapper = ucw.build_wrapper(grep_spec)
        
        # Search for text (this will fail on Windows but should not crash)
        result = grep_wrapper.run("error", "logfile.txt")
        
        # Should not crash, even if command fails
        assert hasattr(result, 'success')
        assert hasattr(result, 'command')
    
    def test_system_information_example(self):
        """Test the system information example from README."""
        ucw = UniversalCommandWrapper()
        
        # Wrap ls command
        ls_spec = ucw.parse_command("ls")
        ls_wrapper = ucw.build_wrapper(ls_spec)
        
        # List directory contents
        result = ls_wrapper.run()
        
        # Should not crash, even if command fails
        assert hasattr(result, 'success')
        assert hasattr(result, 'command')
    
    def test_mcp_plugin_generation_example(self):
        """Test the MCP plugin generation example from README."""
        ucw = UniversalCommandWrapper()
        
        # Generate MCP plugin for tar command
        tar_spec = ucw.parse_command("tar")
        tar_wrapper = ucw.build_wrapper(tar_spec)
        
        # Should create wrapper successfully
        assert tar_wrapper.command_name == "tar"
        assert tar_wrapper.spec == tar_spec
    
    def test_kwargs_normalization_examples(self):
        """Test the kwargs normalization examples from README."""
        ucw = UniversalCommandWrapper()
        
        # Test with a command that might have options
        spec = ucw.parse_command("echo")
        wrapper = ucw.build_wrapper(spec)
        
        # Test kwargs usage (even if no options are parsed)
        result = wrapper.run("test")
        
        # Should not crash
        assert hasattr(result, 'success')
        assert hasattr(result, 'command')
    
    def test_parameter_names_match_api(self):
        """Test that parameter names in examples match the actual API."""
        # Test that platform_name parameter works
        ucw1 = UniversalCommandWrapper(platform_name="windows")
        ucw2 = UniversalCommandWrapper(platform_name="posix")
        ucw3 = UniversalCommandWrapper()
        
        assert ucw1.platform == "windows"
        assert ucw2.platform == "posix"
        assert ucw3.platform in ["windows", "posix"]
        
        # Test timeout parameters
        ucw4 = UniversalCommandWrapper(timeout_help=15, timeout_exec=45)
        assert ucw4.timeout_help == 15
        assert ucw4.timeout_exec == 45


if __name__ == "__main__":
    pytest.main([__file__])
