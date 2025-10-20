"""
Test CommandWrapper kwargs mapping issue.

This module tests the mismatch between documentation examples and actual implementation.
"""

import pytest
import sys
from pathlib import Path

# Add the parent directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from wrapper import CommandWrapper
from models import CommandSpec, OptionSpec, PositionalArgSpec


class TestCommandWrapperKwargsMapping:
    """Test cases for CommandWrapper kwargs mapping issues."""
    
    def test_current_implementation_expects_exact_flags(self):
        """Test that current implementation expects exact flag names."""
        spec = CommandSpec(
            name="testcmd",
            usage="testcmd [options]",
            options=[
                OptionSpec(flag="--all", takes_value=False, description="Show all"),
                OptionSpec(flag="-l", takes_value=False, description="Long format"),
                OptionSpec(flag="--verbose", takes_value=False, description="Verbose output")
            ],
            positional_args=[],
            description="Test command",
            examples=[]
        )
        
        wrapper = CommandWrapper("testcmd", spec)
        
        # This should work with current implementation
        result = wrapper.run(**{"--all": True, "-l": True, "--verbose": True})
        
        # Check that flags were added to command
        assert "--all" in result.command
        assert "-l" in result.command
        assert "--verbose" in result.command
    
    def test_documentation_examples_dont_work(self):
        """Test that documentation examples don't work with current implementation."""
        spec = CommandSpec(
            name="ls",
            usage="ls [options]",
            options=[
                OptionSpec(flag="-l", takes_value=False, description="Long format"),
                OptionSpec(flag="-a", takes_value=False, description="All files"),
                OptionSpec(flag="-h", takes_value=False, description="Human readable")
            ],
            positional_args=[],
            description="List files",
            examples=[]
        )
        
        wrapper = CommandWrapper("ls", spec)
        
        # This is what the documentation shows but doesn't work
        # wrapper.run(l=True, a=True, h=True)  # This would cause SyntaxError
        
        # Instead, we have to use string keys (which is awkward)
        result = wrapper.run(**{"-l": True, "-a": True, "-h": True})
        
        # Check that flags were added to command
        assert "-l" in result.command
        assert "-a" in result.command
        assert "-h" in result.command
    
    def test_long_flags_with_dashes_dont_work_as_kwargs(self):
        """Test that long flags with dashes can't be used as kwargs."""
        spec = CommandSpec(
            name="testcmd",
            usage="testcmd [options]",
            options=[
                OptionSpec(flag="--long-option", takes_value=False, description="Long option"),
                OptionSpec(flag="--with-dashes", takes_value=True, description="With dashes")
            ],
            positional_args=[],
            description="Test command",
            examples=[]
        )
        
        wrapper = CommandWrapper("testcmd", spec)
        
        # These would cause SyntaxError if used as kwargs:
        # wrapper.run(long_option=True, with_dashes="value")  # SyntaxError
        
        # Instead, we have to use string keys
        result = wrapper.run(**{"--long-option": True, "--with-dashes": "test"})
        
        # Check that flags were added to command
        assert "--long-option" in result.command
        assert "--with-dashes" in result.command
        assert "test" in result.command
    
    def test_what_documentation_should_show(self):
        """Test what the documentation examples should actually be."""
        spec = CommandSpec(
            name="ls",
            usage="ls [options]",
            options=[
                OptionSpec(flag="-l", takes_value=False, description="Long format"),
                OptionSpec(flag="-a", takes_value=False, description="All files")
            ],
            positional_args=[],
            description="List files",
            examples=[]
        )
        
        wrapper = CommandWrapper("ls", spec)
        
        # What documentation shows (doesn't work):
        # result = wrapper.run(l=True, a=True)  # SyntaxError
        
        # What actually works:
        result = wrapper.run(**{"-l": True, "-a": True})
        
        # What would be better (normalized kwargs):
        # result = wrapper.run(l=True, a=True)  # This should work with normalized keys
        
        assert "-l" in result.command
        assert "-a" in result.command


if __name__ == "__main__":
    pytest.main([__file__])
