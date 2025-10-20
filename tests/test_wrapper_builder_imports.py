"""
Test WrapperBuilder import functionality.

This module tests that WrapperBuilder can be imported from both locations
and that the duplicate has been properly removed.
"""

import pytest
import sys
from pathlib import Path

# Add the parent directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestWrapperBuilderImports:
    """Test cases for WrapperBuilder import functionality."""
    
    def test_import_from_generator_init(self):
        """Test importing WrapperBuilder from generator/__init__.py."""
        from generator import WrapperBuilder
        assert WrapperBuilder is not None
        assert hasattr(WrapperBuilder, 'build_wrapper')
        assert hasattr(WrapperBuilder, 'generate_mcp_plugin_code')
    
    def test_import_from_wrapper_builder(self):
        """Test importing WrapperBuilder from generator/wrapper_builder.py."""
        from generator.wrapper_builder import WrapperBuilder
        assert WrapperBuilder is not None
        assert hasattr(WrapperBuilder, 'build_wrapper')
        assert hasattr(WrapperBuilder, 'generate_mcp_plugin_code')
    
    def test_both_imports_same_class(self):
        """Test that both import methods return the same class."""
        from generator import WrapperBuilder as WrapperBuilder1
        from generator.wrapper_builder import WrapperBuilder as WrapperBuilder2
        
        assert WrapperBuilder1 is WrapperBuilder2
        assert WrapperBuilder1 == WrapperBuilder2
    
    def test_wrapper_builder_functionality(self):
        """Test that WrapperBuilder works correctly."""
        from generator import WrapperBuilder
        from models import CommandSpec, OptionSpec
        
        # Create a test command spec
        spec = CommandSpec(
            name="testcmd",
            usage="testcmd [options]",
            options=[
                OptionSpec(flag="--help", takes_value=False, description="Show help")
            ],
            description="Test command",
            examples=[]
        )
        
        builder = WrapperBuilder()
        
        # Test build_wrapper method
        wrapper = builder.build_wrapper(spec)
        assert wrapper is not None
        assert wrapper.command_name == "testcmd"
        
        # Test generate_mcp_plugin_code method
        code = builder.generate_mcp_plugin_code(spec)
        assert isinstance(code, str)
        assert "testcmd" in code
        assert "execute" in code
        assert "argparse" in code
    
    def test_no_duplicate_class_definition(self):
        """Test that there's no duplicate class definition."""
        import generator
        import generator.wrapper_builder
        
        # Both modules should have the same WrapperBuilder class
        assert generator.WrapperBuilder is generator.wrapper_builder.WrapperBuilder
        
        # The __init__.py should only re-export, not define
        init_source = Path(__file__).parent.parent / "generator" / "__init__.py"
        init_content = init_source.read_text()
        
        # Should not contain class definition
        assert "class WrapperBuilder:" not in init_content
        # Should contain import statement
        assert "from .wrapper_builder import WrapperBuilder" in init_content


if __name__ == "__main__":
    pytest.main([__file__])
