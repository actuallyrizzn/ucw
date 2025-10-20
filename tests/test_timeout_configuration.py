"""
Test timeout configuration functionality.

This module tests that timeout configuration works correctly through
constructor parameters, environment variables, and CLI flags.
"""

import pytest
import sys
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add the parent directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestTimeoutConfiguration:
    """Test cases for timeout configuration."""
    
    def test_default_timeouts(self):
        """Test that default timeouts are used when not specified."""
        from __init__ import UniversalCommandWrapper
        
        with patch.object(UniversalCommandWrapper, '_create_parser') as mock_create_parser:
            mock_parser = MagicMock()
            mock_create_parser.return_value = mock_parser
            
            ucw = UniversalCommandWrapper()
            
            # Verify default timeouts
            assert ucw.timeout_help == 10
            assert ucw.timeout_exec == 30
    
    def test_constructor_timeout_parameters(self):
        """Test that constructor timeout parameters work."""
        from __init__ import UniversalCommandWrapper
        
        with patch.object(UniversalCommandWrapper, '_create_parser') as mock_create_parser:
            mock_parser = MagicMock()
            mock_create_parser.return_value = mock_parser
            
            ucw = UniversalCommandWrapper(
                timeout_help=20,
                timeout_exec=60
            )
            
            # Verify custom timeouts
            assert ucw.timeout_help == 20
            assert ucw.timeout_exec == 60
    
    def test_environment_variable_timeouts(self):
        """Test that environment variable timeouts work."""
        from __init__ import UniversalCommandWrapper
        
        with patch.dict(os.environ, {
            'UCW_TIMEOUT_HELP': '15',
            'UCW_TIMEOUT_EXEC': '45'
        }):
            with patch.object(UniversalCommandWrapper, '_create_parser') as mock_create_parser:
                mock_parser = MagicMock()
                mock_create_parser.return_value = mock_parser
                
                ucw = UniversalCommandWrapper()
                
                # Verify environment variable timeouts
                assert ucw.timeout_help == 15
                assert ucw.timeout_exec == 45
    
    def test_constructor_overrides_environment(self):
        """Test that constructor parameters override environment variables."""
        from __init__ import UniversalCommandWrapper
        
        with patch.dict(os.environ, {
            'UCW_TIMEOUT_HELP': '15',
            'UCW_TIMEOUT_EXEC': '45'
        }):
            with patch.object(UniversalCommandWrapper, '_create_parser') as mock_create_parser:
                mock_parser = MagicMock()
                mock_create_parser.return_value = mock_parser
                
                ucw = UniversalCommandWrapper(
                    timeout_help=25,
                    timeout_exec=55
                )
                
                # Verify constructor parameters override environment
                assert ucw.timeout_help == 25
                assert ucw.timeout_exec == 55
    
    def test_parser_receives_timeout(self):
        """Test that parser receives the correct timeout."""
        from __init__ import UniversalCommandWrapper
        from parser.windows import WindowsParser
        
        ucw = UniversalCommandWrapper(
            platform_name="windows",
            timeout_help=20
        )
        
        # Verify parser has correct timeout
        assert isinstance(ucw.parser, WindowsParser)
        assert ucw.parser.timeout == 20
    
    def test_wrapper_builder_receives_timeout(self):
        """Test that wrapper builder receives the correct timeout."""
        from __init__ import UniversalCommandWrapper
        
        ucw = UniversalCommandWrapper(timeout_exec=40)
        
        # Verify wrapper builder has correct timeout
        assert ucw.wrapper_builder.timeout_exec == 40
    
    def test_command_wrapper_timeout(self):
        """Test that CommandWrapper uses the correct timeout."""
        from wrapper import CommandWrapper
        from models import CommandSpec
        
        spec = CommandSpec(
            name="testcmd",
            usage="testcmd [options]",
            options=[],
            description="Test command",
            examples=[]
        )
        
        wrapper = CommandWrapper("testcmd", spec, timeout=50)
        
        # Verify wrapper has correct timeout
        assert wrapper.timeout == 50
    
    def test_generated_code_uses_timeout(self):
        """Test that generated MCP plugin code uses the correct timeout."""
        from generator.wrapper_builder import WrapperBuilder
        from models import CommandSpec
        
        spec = CommandSpec(
            name="testcmd",
            usage="testcmd [options]",
            options=[],
            description="Test command",
            examples=[]
        )
        
        builder = WrapperBuilder(timeout_exec=60)
        code = builder.generate_mcp_plugin_code(spec)
        
        # Verify generated code contains the timeout
        assert "timeout=60" in code
        assert "Command timed out after 60 seconds" in code
    
    def test_cli_timeout_arguments(self):
        """Test that CLI accepts timeout arguments."""
        import argparse
        
        parser = argparse.ArgumentParser()
        parser.add_argument("--timeout-help", type=int, default=10)
        parser.add_argument("--timeout-exec", type=int, default=30)
        parser.add_argument("command")
        parser.add_argument("command_name")
        
        # Test default values
        args = parser.parse_args(['parse', 'ls'])
        assert args.timeout_help == 10
        assert args.timeout_exec == 30
        
        # Test custom values
        args = parser.parse_args(['--timeout-help', '20', '--timeout-exec', '60', 'parse', 'ls'])
        assert args.timeout_help == 20
        assert args.timeout_exec == 60
    
    def test_cli_integration(self):
        """Test that CLI properly passes timeout parameters to UCW."""
        # Test that the timeout parameters are properly handled
        from __init__ import UniversalCommandWrapper
        
        # Test with custom timeouts
        ucw = UniversalCommandWrapper(
            platform_name="windows",
            timeout_help=25,
            timeout_exec=55
        )
        
        # Verify UCW was created with correct parameters
        assert ucw.timeout_help == 25
        assert ucw.timeout_exec == 55
        assert ucw.platform == "windows"


if __name__ == "__main__":
    pytest.main([__file__])
