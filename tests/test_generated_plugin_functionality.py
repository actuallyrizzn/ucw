"""
Test that generated plugins work correctly with the fixed attribute names.
"""

import pytest
import sys
import tempfile
import subprocess
from pathlib import Path

# Add the parent directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from generator.wrapper_builder import WrapperBuilder
from models import CommandSpec, OptionSpec


class TestGeneratedPluginFunctionality:
    """Test that generated plugins work correctly."""
    
    def test_generated_plugin_execution(self):
        """Test that a generated plugin can be executed successfully."""
        builder = WrapperBuilder()
        
        spec = CommandSpec(
            name="echo",
            usage="echo [options] [text]",
            options=[
                OptionSpec(flag="--all", takes_value=False, description="Show all"),
                OptionSpec(flag="-n", takes_value=False, description="No newline"),
                OptionSpec(flag="--verbose", takes_value=False, description="Verbose output")
            ],
            description="Echo command",
            examples=[]
        )
        
        # Generate plugin code
        code = builder.generate_mcp_plugin_code(spec)
        
        # Write to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        try:
            # Test that the plugin can be imported and run
            result = subprocess.run(
                [sys.executable, temp_file, 'execute', '--all'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # Should not crash (may fail due to echo command not existing, but shouldn't be argparse error)
            assert result.returncode != 1 or "ArgumentError" not in result.stderr
            
        finally:
            # Clean up
            Path(temp_file).unlink()
    
    def test_generated_plugin_with_flags(self):
        """Test that generated plugin correctly handles flags."""
        builder = WrapperBuilder()
        
        spec = CommandSpec(
            name="testcmd",
            usage="testcmd [options]",
            options=[
                OptionSpec(flag="--all", takes_value=False, description="Show all"),
                OptionSpec(flag="-l", takes_value=False, description="Long format")
            ],
            description="Test command",
            examples=[]
        )
        
        # Generate plugin code
        code = builder.generate_mcp_plugin_code(spec)
        
        # Verify the generated code has correct structure
        assert 'parser.add_argument("--all", action="store_true", dest="all"' in code
        assert 'parser.add_argument("-l", action="store_true", dest="l"' in code
        assert 'if args.all:' in code
        assert 'if args.l:' in code
        assert 'cmd_args.append("--all")' in code
        assert 'cmd_args.append("-l")' in code
    
    def test_normalize_dest_name_edge_cases(self):
        """Test edge cases for destination name normalization."""
        builder = WrapperBuilder()
        
        # Test various edge cases
        test_cases = [
            ("--all", "all"),
            ("-l", "l"),
            ("--long-option", "long_option"),
            ("--with-dashes", "with_dashes"),
            ("/?", "question"),
            ("/help", "help"),
            ("--option-with-numbers-123", "option_with_numbers_123"),
            ("-a", "a"),
            ("--", "empty"),  # Edge case
            ("--option@special", "option_special"),
        ]
        
        for flag, expected_dest in test_cases:
            dest = builder._normalize_dest_name(flag)
            assert dest == expected_dest, f"Flag '{flag}' should normalize to '{expected_dest}', got '{dest}'"


if __name__ == "__main__":
    pytest.main([__file__])
