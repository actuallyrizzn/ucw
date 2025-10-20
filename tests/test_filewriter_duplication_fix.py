"""
Test FileWriter duplication fix.

This module tests that the fix prevents file duplication and works correctly.
"""

import pytest
import sys
import tempfile
import os
from pathlib import Path

# Add the parent directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from generator.file_writer import FileWriter
from models import CommandSpec, OptionSpec, PositionalArgSpec


class TestFileWriterDuplicationFix:
    """Test cases for FileWriter duplication fix."""
    
    def test_initial_write_creates_clean_file(self):
        """Test that initial write creates a clean file without UCW markers."""
        writer = FileWriter()
        
        spec = CommandSpec(
            name="testcmd",
            usage="testcmd [options]",
            options=[
                OptionSpec(flag="--verbose", takes_value=False, description="Verbose output")
            ],
            positional_args=[],
            description="Test command",
            examples=[]
        )
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            temp_file = f.name
        
        try:
            # Initial write
            writer.write_wrapper(spec, None, temp_file, update=False)
            
            # Read the file
            with open(temp_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Should not have UCW markers
            assert "# UCW-BEGIN:" not in content
            assert "# UCW-END:" not in content
            
            # Should have the plugin code
            assert "testcmd Plugin" in content
            assert "def main():" in content
            
        finally:
            os.unlink(temp_file)
    
    def test_first_update_replaces_file_without_duplication(self):
        """Test that first update replaces the file without duplicating code."""
        writer = FileWriter()
        
        spec = CommandSpec(
            name="testcmd",
            usage="testcmd [options]",
            options=[
                OptionSpec(flag="--verbose", takes_value=False, description="Verbose output")
            ],
            positional_args=[],
            description="Test command",
            examples=[]
        )
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            temp_file = f.name
        
        try:
            # Initial write
            writer.write_wrapper(spec, None, temp_file, update=False)
            
            # First update
            writer.write_wrapper(spec, None, temp_file, update=True)
            
            # Read the file
            with open(temp_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Should NOT have UCW markers (file was replaced entirely)
            assert "# UCW-BEGIN: testcmd" not in content
            assert "# UCW-END: testcmd" not in content
            
            # Should NOT have duplicated content
            main_count = content.count("def main():")
            # Count unique function definitions, not just string occurrences
            setup_count = content.count("def setup_execute_command")
            execute_count = content.count("def execute_command")
            
            # Should have only one occurrence of each function
            assert main_count == 1, f"Expected 1 'def main():' occurrence, got {main_count}"
            assert setup_count == 1, f"Expected 1 'def setup_execute_command' occurrence, got {setup_count}"
            assert execute_count == 1, f"Expected 1 'def execute_command' occurrence, got {execute_count}"
            
        finally:
            os.unlink(temp_file)
    
    def test_second_update_replaces_content_without_duplication(self):
        """Test that second update replaces content without creating more duplication."""
        writer = FileWriter()
        
        spec = CommandSpec(
            name="testcmd",
            usage="testcmd [options]",
            options=[
                OptionSpec(flag="--verbose", takes_value=False, description="Verbose output")
            ],
            positional_args=[],
            description="Test command",
            examples=[]
        )
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            temp_file = f.name
        
        try:
            # Initial write
            writer.write_wrapper(spec, None, temp_file, update=False)
            
            # First update
            writer.write_wrapper(spec, None, temp_file, update=True)
            
            # Second update
            writer.write_wrapper(spec, None, temp_file, update=True)
            
            # Read the file
            with open(temp_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Should NOT have UCW markers (file was replaced entirely)
            assert "# UCW-BEGIN: testcmd" not in content
            assert "# UCW-END: testcmd" not in content
            
            # Should NOT have duplicated content
            main_count = content.count("def main():")
            # Count unique function definitions, not just string occurrences
            setup_count = content.count("def setup_execute_command")
            execute_count = content.count("def execute_command")
            
            # Should have only one occurrence of each function
            assert main_count == 1, f"Expected 1 'def main():' occurrence, got {main_count}"
            assert setup_count == 1, f"Expected 1 'def setup_execute_command' occurrence, got {setup_count}"
            assert execute_count == 1, f"Expected 1 'def execute_command' occurrence, got {execute_count}"
            
        finally:
            os.unlink(temp_file)
    
    def test_multiple_commands_replace_file_without_duplication(self):
        """Test that multiple commands replace the file without duplication."""
        writer = FileWriter()
        
        spec1 = CommandSpec(
            name="cmd1",
            usage="cmd1 [options]",
            options=[
                OptionSpec(flag="--verbose", takes_value=False, description="Verbose output")
            ],
            positional_args=[],
            description="Command 1",
            examples=[]
        )
        
        spec2 = CommandSpec(
            name="cmd2",
            usage="cmd2 [options]",
            options=[
                OptionSpec(flag="--debug", takes_value=False, description="Debug output")
            ],
            positional_args=[],
            description="Command 2",
            examples=[]
        )
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            temp_file = f.name
        
        try:
            # Initial write with cmd1
            writer.write_wrapper(spec1, None, temp_file, update=False)
            
            # Update with cmd2
            writer.write_wrapper(spec2, None, temp_file, update=True)
            
            # Read the file
            with open(temp_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Should NOT have UCW markers (file was replaced entirely)
            assert "# UCW-BEGIN: cmd2" not in content
            assert "# UCW-END: cmd2" not in content
            
            # Should have cmd2 content (not cmd1)
            assert 'cmd_args = ["cmd2"]' in content
            assert 'if args.debug:' in content
            assert 'cmd_args.append("--debug")' in content
            
            # Should NOT have cmd1 content
            assert 'cmd_args = ["cmd1"]' not in content
            assert 'if args.verbose:' not in content
            
        finally:
            os.unlink(temp_file)
    
    def test_extract_wrapper_code_returns_only_command_functions(self):
        """Test that _extract_wrapper_code returns only command-specific functions."""
        writer = FileWriter()
        
        spec = CommandSpec(
            name="testcmd",
            usage="testcmd [options]",
            options=[
                OptionSpec(flag="--verbose", takes_value=False, description="Verbose output")
            ],
            positional_args=[],
            description="Test command",
            examples=[]
        )
        
        # Generate full plugin code
        plugin_code = writer.wrapper_builder.generate_mcp_plugin_code(spec)
        
        # Extract wrapper code
        wrapper_code = writer._extract_wrapper_code(plugin_code, "testcmd")
        
        # Should contain command-specific functions
        assert "def setup_execute_command" in wrapper_code
        assert "def execute_command" in wrapper_code
        
        # Should NOT contain main function or imports
        assert "def main():" not in wrapper_code
        assert "import argparse" not in wrapper_code
        assert "#!/usr/bin/env python3" not in wrapper_code
    
    def test_update_wrapper_section_handles_fresh_files(self):
        """Test that _update_wrapper_section handles fresh files correctly."""
        writer = FileWriter()
        
        fresh_content = "#!/usr/bin/env python3\nprint('Hello World')"
        command_name = "testcmd"
        new_code = "def test_function():\n    pass"
        
        result = writer._update_wrapper_section(fresh_content, command_name, new_code)
        
        # Should wrap the entire content in UCW markers
        assert "# UCW-BEGIN: testcmd" in result
        assert "# UCW-END: testcmd" in result
        assert fresh_content in result
    
    def test_update_wrapper_section_replaces_existing_sections(self):
        """Test that _update_wrapper_section replaces existing sections correctly."""
        writer = FileWriter()
        
        existing_content = """#!/usr/bin/env python3
# UCW-BEGIN: testcmd
def old_function():
    pass
# UCW-END: testcmd
print('Hello World')"""
        
        command_name = "testcmd"
        new_code = "def new_function():\n    pass"
        
        result = writer._update_wrapper_section(existing_content, command_name, new_code)
        
        # Should replace the old section
        assert "def old_function():" not in result
        assert "def new_function():" in result
        
        # Should keep the rest of the content
        assert "print('Hello World')" in result


if __name__ == "__main__":
    pytest.main([__file__])
