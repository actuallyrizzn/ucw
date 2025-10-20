"""
Test BaseParser import functionality and security.

This module tests that BaseParser can be imported from both locations,
that the duplicate has been properly removed, and that shell=True usage
has been eliminated for security.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add the parent directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestBaseParserImports:
    """Test cases for BaseParser import functionality and security."""
    
    def test_import_from_parser_init(self):
        """Test importing BaseParser from parser/__init__.py."""
        from parser import BaseParser
        assert BaseParser is not None
        assert hasattr(BaseParser, 'parse_command')
        assert hasattr(BaseParser, '_get_help_text')
    
    def test_import_from_base(self):
        """Test importing BaseParser from parser/base.py."""
        from parser.base import BaseParser
        assert BaseParser is not None
        assert hasattr(BaseParser, 'parse_command')
        assert hasattr(BaseParser, '_get_help_text')
    
    def test_both_imports_same_class(self):
        """Test that both import methods return the same class."""
        from parser import BaseParser as BaseParser1
        from parser.base import BaseParser as BaseParser2
        
        assert BaseParser1 is BaseParser2
        assert BaseParser1 == BaseParser2
    
    def test_no_duplicate_class_definition(self):
        """Test that there's no duplicate class definition."""
        import parser
        import parser.base
        
        # Both modules should have the same BaseParser class
        assert parser.BaseParser is parser.base.BaseParser
        
        # The __init__.py should only re-export, not define
        init_source = Path(__file__).parent.parent / "parser" / "__init__.py"
        init_content = init_source.read_text()
        
        # Should not contain class definition
        assert "class BaseParser:" not in init_content
        # Should contain import statement
        assert "from .base import BaseParser" in init_content
    
    def test_no_shell_true_usage(self):
        """Test that shell=True usage has been eliminated."""
        # Read the base.py file to check for shell=True
        base_source = Path(__file__).parent.parent / "parser" / "base.py"
        base_content = base_source.read_text()
        
        # Should not contain shell=True
        assert "shell=True" not in base_content
        
        # Should contain subprocess.run calls without shell=True
        assert "subprocess.run(" in base_content
    
    def test_subprocess_security(self):
        """Test that subprocess calls are secure (no shell=True)."""
        from parser.base import BaseParser
        
        # Create a mock parser to test subprocess behavior
        class MockParser(BaseParser):
            def _get_help_command(self, command_name: str):
                return ["test", "command"]
            
            def _try_alternative_help(self, command_name: str):
                return "mock help"
            
            def _parse_help_text(self, command_name: str, help_text: str):
                from models import CommandSpec
                return CommandSpec(
                    name=command_name,
                    usage="test usage",
                    options=[],
                    description="test",
                    examples=[]
                )
            
            def _is_option_line(self, line: str) -> bool:
                return False
            
            def _parse_option_line(self, line: str):
                return None
        
        parser = MockParser()
        
        # Mock subprocess.run to verify it's called without shell=True
        with patch('subprocess.run') as mock_run:
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_result.stdout = "test help"
            mock_run.return_value = mock_result
            
            # This should call subprocess.run without shell=True
            parser._get_help_text("testcmd")
            
            # Verify subprocess.run was called
            mock_run.assert_called_once()
            
            # Get the call arguments
            call_args, call_kwargs = mock_run.call_args
            
            # Verify shell is not True (should be False or not specified)
            assert call_kwargs.get('shell') is not True
    
    def test_baseparser_functionality(self):
        """Test that BaseParser works correctly."""
        from parser.base import BaseParser
        
        # Create a concrete implementation for testing
        class TestParser(BaseParser):
            def _get_help_command(self, command_name: str):
                return ["test", "command"]
            
            def _try_alternative_help(self, command_name: str):
                return "mock help"
            
            def _parse_help_text(self, command_name: str, help_text: str):
                from models import CommandSpec
                return CommandSpec(
                    name=command_name,
                    usage="test usage",
                    options=[],
                    description="test",
                    examples=[]
                )
            
            def _is_option_line(self, line: str) -> bool:
                return False
            
            def _parse_option_line(self, line: str):
                return None
        
        parser = TestParser()
        
        # Test basic functionality
        assert parser.timeout == 10
        assert parser is not None


if __name__ == "__main__":
    pytest.main([__file__])
