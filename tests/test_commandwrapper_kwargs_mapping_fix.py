"""
Test CommandWrapper kwargs mapping fix.

This module tests that the fix allows documentation examples to work correctly.
"""

import pytest
import sys
from pathlib import Path

# Add the parent directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from wrapper import CommandWrapper
from models import CommandSpec, OptionSpec, PositionalArgSpec


class TestCommandWrapperKwargsMappingFix:
    """Test cases for CommandWrapper kwargs mapping fix."""
    
    def test_documentation_examples_now_work(self):
        """Test that documentation examples now work with normalized kwargs."""
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
        
        # This is what the documentation shows and now works!
        result = wrapper.run(l=True, a=True, h=True)
        
        # Check that flags were added to command
        assert "-l" in result.command
        assert "-a" in result.command
        assert "-h" in result.command
    
    def test_long_flags_with_dashes_work_as_kwargs(self):
        """Test that long flags with dashes work as normalized kwargs."""
        spec = CommandSpec(
            name="testcmd",
            usage="testcmd [options]",
            options=[
                OptionSpec(flag="--long-option", takes_value=False, description="Long option"),
                OptionSpec(flag="--with-dashes", takes_value=True, description="With dashes"),
                OptionSpec(flag="--verbose", takes_value=False, description="Verbose output")
            ],
            positional_args=[],
            description="Test command",
            examples=[]
        )
        
        wrapper = CommandWrapper("testcmd", spec)
        
        # These now work as normalized kwargs!
        result = wrapper.run(long_option=True, with_dashes="test", verbose=True)
        
        # Check that flags were added to command
        assert "--long-option" in result.command
        assert "--with-dashes" in result.command
        assert "test" in result.command
        assert "--verbose" in result.command
    
    def test_mixed_short_and_long_flags(self):
        """Test mixed short and long flags work together."""
        spec = CommandSpec(
            name="testcmd",
            usage="testcmd [options]",
            options=[
                OptionSpec(flag="-l", takes_value=False, description="Long format"),
                OptionSpec(flag="--all", takes_value=False, description="All files"),
                OptionSpec(flag="-v", takes_value=False, description="Verbose"),
                OptionSpec(flag="--output", takes_value=True, description="Output file")
            ],
            positional_args=[],
            description="Test command",
            examples=[]
        )
        
        wrapper = CommandWrapper("testcmd", spec)
        
        # Mix of short and long flags
        result = wrapper.run(l=True, all=True, v=True, output="file.txt")
        
        # Check that all flags were added to command
        assert "-l" in result.command
        assert "--all" in result.command
        assert "-v" in result.command
        assert "--output" in result.command
        assert "file.txt" in result.command
    
    def test_windows_flags_normalization(self):
        """Test that Windows flags work with normalization."""
        spec = CommandSpec(
            name="testcmd",
            usage="testcmd [options]",
            options=[
                OptionSpec(flag="/?", takes_value=False, description="Windows help"),
                OptionSpec(flag="/help", takes_value=False, description="Windows help alt"),
                OptionSpec(flag="/verbose", takes_value=False, description="Verbose")
            ],
            positional_args=[],
            description="Test command",
            examples=[]
        )
        
        wrapper = CommandWrapper("testcmd", spec)
        
        # Windows flags normalized
        result = wrapper.run(question=True, help=True, verbose=True)
        
        # Check that flags were added to command
        assert "/?" in result.command
        assert "/help" in result.command
        assert "/verbose" in result.command
    
    def test_positional_args_still_work(self):
        """Test that positional arguments still work with normalized kwargs."""
        spec = CommandSpec(
            name="cp",
            usage="cp [options] source dest",
            options=[
                OptionSpec(flag="-r", takes_value=False, description="Recursive"),
                OptionSpec(flag="-v", takes_value=False, description="Verbose")
            ],
            positional_args=[
                PositionalArgSpec(name="source", required=True, variadic=False, description="Source file"),
                PositionalArgSpec(name="dest", required=True, variadic=False, description="Destination file")
            ],
            description="Copy files",
            examples=[]
        )
        
        wrapper = CommandWrapper("cp", spec)
        
        # Positional args + normalized kwargs
        result = wrapper.run("source.txt", "dest.txt", r=True, v=True)
        
        # Check that positional args and flags were added
        assert "source.txt" in result.command
        assert "dest.txt" in result.command
        assert "-r" in result.command
        assert "-v" in result.command
    
    def test_value_flags_work(self):
        """Test that value flags work with normalized kwargs."""
        spec = CommandSpec(
            name="testcmd",
            usage="testcmd [options]",
            options=[
                OptionSpec(flag="--output", takes_value=True, description="Output file"),
                OptionSpec(flag="--format", takes_value=True, description="Format type"),
                OptionSpec(flag="-o", takes_value=True, description="Short output")
            ],
            positional_args=[],
            description="Test command",
            examples=[]
        )
        
        wrapper = CommandWrapper("testcmd", spec)
        
        # Value flags with normalized kwargs
        result = wrapper.run(output="file.txt", format="json", o="output.txt")
        
        # Check that flags and values were added
        assert "--output" in result.command
        assert "file.txt" in result.command
        assert "--format" in result.command
        assert "json" in result.command
        assert "-o" in result.command
        assert "output.txt" in result.command
    
    def test_backward_compatibility_with_string_keys(self):
        """Test that old string key approach still works for backward compatibility."""
        spec = CommandSpec(
            name="testcmd",
            usage="testcmd [options]",
            options=[
                OptionSpec(flag="--all", takes_value=False, description="All files"),
                OptionSpec(flag="-l", takes_value=False, description="Long format")
            ],
            positional_args=[],
            description="Test command",
            examples=[]
        )
        
        wrapper = CommandWrapper("testcmd", spec)
        
        # Old approach with string keys should still work
        result = wrapper.run(**{"--all": True, "-l": True})
        
        # Check that flags were added to command
        assert "--all" in result.command
        assert "-l" in result.command


if __name__ == "__main__":
    pytest.main([__file__])
