"""
Test argparse attribute name generation.

This module tests that generated plugin code uses correct argparse attribute names.
"""

import pytest
import sys
from pathlib import Path

# Add the parent directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from generator.wrapper_builder import WrapperBuilder
from models import CommandSpec, OptionSpec


class TestArgparseAttributeNames:
    """Test cases for argparse attribute name generation."""
    
    def test_generate_argument_definitions_with_dest(self):
        """Test that argument definitions use proper dest parameter."""
        builder = WrapperBuilder()
        
        spec = CommandSpec(
            name="testcmd",
            usage="testcmd [options]",
            options=[
                OptionSpec(flag="--all", takes_value=False, description="Show all"),
                OptionSpec(flag="-l", takes_value=False, description="Long format"),
                OptionSpec(flag="--verbose", takes_value=False, description="Verbose output"),
                OptionSpec(flag="--output", takes_value=True, description="Output file"),
                OptionSpec(flag="/?", takes_value=False, description="Windows help")
            ],
            description="Test command",
            examples=[]
        )
        
        definitions = builder._generate_argument_definitions(spec)
        
        # Should use dest parameter to control attribute names
        assert 'dest=' in definitions
        assert 'parser.add_argument("--all", action="store_true", dest="all"' in definitions
        assert 'parser.add_argument("-l", action="store_true", dest="l"' in definitions
        assert 'parser.add_argument("--verbose", action="store_true", dest="verbose"' in definitions
        assert 'parser.add_argument("--output", dest="output"' in definitions
        assert 'parser.add_argument("/?", action="store_true", dest="question"' in definitions
    
    def test_generate_argument_handling_correct_attributes(self):
        """Test that argument handling uses correct attribute names."""
        builder = WrapperBuilder()
        
        spec = CommandSpec(
            name="testcmd",
            usage="testcmd [options]",
            options=[
                OptionSpec(flag="--all", takes_value=False, description="Show all"),
                OptionSpec(flag="-l", takes_value=False, description="Long format"),
                OptionSpec(flag="--output", takes_value=True, description="Output file")
            ],
            description="Test command",
            examples=[]
        )
        
        handling = builder._generate_argument_handling(spec)
        
        # Should use correct attribute names (not __all, _l, etc.)
        assert 'args.all' in handling
        assert 'args.l' in handling
        assert 'args.output' in handling
        
        # Should NOT use incorrect attribute names
        assert 'args.__all' not in handling
        assert 'args._l' not in handling
        assert 'args._output' not in handling
    
    def test_generated_plugin_code_uses_correct_attributes(self):
        """Test that complete generated plugin code uses correct attributes."""
        builder = WrapperBuilder()
        
        spec = CommandSpec(
            name="testcmd",
            usage="testcmd [options]",
            options=[
                OptionSpec(flag="--all", takes_value=False, description="Show all"),
                OptionSpec(flag="-l", takes_value=False, description="Long format"),
                OptionSpec(flag="--output", takes_value=True, description="Output file")
            ],
            description="Test command",
            examples=[]
        )
        
        code = builder.generate_mcp_plugin_code(spec)
        
        # Should use correct attribute names throughout
        assert 'args.all' in code
        assert 'args.l' in code
        assert 'args.output' in code
        
        # Should NOT use incorrect attribute names
        assert 'args.__all' not in code
        assert 'args._l' not in code
        assert 'args._output' not in code
        
        # Should use dest parameter in argument definitions
        assert 'dest="all"' in code
        assert 'dest="l"' in code
        assert 'dest="output"' in code
    
    def test_windows_flag_normalization(self):
        """Test that Windows flags like /? are handled correctly."""
        builder = WrapperBuilder()
        
        spec = CommandSpec(
            name="testcmd",
            usage="testcmd [options]",
            options=[
                OptionSpec(flag="/?", takes_value=False, description="Windows help"),
                OptionSpec(flag="/help", takes_value=False, description="Windows help alt")
            ],
            description="Test command",
            examples=[]
        )
        
        code = builder.generate_mcp_plugin_code(spec)
        
        # Should normalize Windows flags properly
        assert 'dest="question"' in code
        assert 'dest="help"' in code
        assert 'args.question' in code
        assert 'args.help' in code
    
    def test_complex_flag_combinations(self):
        """Test various complex flag combinations."""
        builder = WrapperBuilder()
        
        spec = CommandSpec(
            name="testcmd",
            usage="testcmd [options]",
            options=[
                OptionSpec(flag="--long-option", takes_value=False, description="Long option"),
                OptionSpec(flag="--with-dashes", takes_value=True, description="With dashes"),
                OptionSpec(flag="-a", takes_value=False, description="Short a"),
                OptionSpec(flag="-z", takes_value=True, description="Short z")
            ],
            description="Test command",
            examples=[]
        )
        
        code = builder.generate_mcp_plugin_code(spec)
        
        # Should handle complex flag names correctly
        assert 'dest="long_option"' in code
        assert 'dest="with_dashes"' in code
        assert 'dest="a"' in code
        assert 'dest="z"' in code
        
        assert 'args.long_option' in code
        assert 'args.with_dashes' in code
        assert 'args.a' in code
        assert 'args.z' in code


if __name__ == "__main__":
    pytest.main([__file__])
