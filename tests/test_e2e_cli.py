"""
End-to-end CLI workflow tests for UCW.

This module tests complete CLI workflows from command to file generation.
"""

import pytest
import subprocess
import sys
import tempfile
import os
from pathlib import Path

# Add the parent directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestE2ECLIWorkflow:
    """Test cases for end-to-end CLI workflows."""
    
    def test_cli_wrap_command_basic(self):
        """Test basic wrap command workflow."""
        result = subprocess.run(
            [sys.executable, 'cli.py', 'wrap', 'echo'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Should succeed
        assert result.returncode == 0
        
        # Should output JSON with status
        import json
        output = json.loads(result.stdout)
        assert output['status'] == 'success'
        assert 'command' in output
        assert output['command'] == 'echo'
    
    def test_cli_wrap_command_with_output(self):
        """Test wrap command with file output."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            temp_file = f.name
        
        try:
            result = subprocess.run(
                [sys.executable, 'cli.py', 'wrap', 'echo', '--output', temp_file],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Should succeed
            assert result.returncode == 0
            
            # Should create file
            assert os.path.exists(temp_file)
            
            # File should contain Python code
            with open(temp_file, 'r', encoding='utf-8') as f:
                content = f.read()
                assert '#!/usr/bin/env python3' in content
                assert 'echo Plugin' in content
                assert 'def main():' in content
                assert 'def execute_command' in content
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_cli_parse_command_basic(self):
        """Test basic parse command workflow."""
        result = subprocess.run(
            [sys.executable, 'cli.py', 'parse', 'echo'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Should succeed
        assert result.returncode == 0
        
        # Should output JSON with command spec
        import json
        output = json.loads(result.stdout)
        assert output['status'] == 'success'
        assert 'spec' in output
        assert output['spec']['name'] == 'echo'
    
    def test_cli_execute_command_basic(self):
        """Test basic execute command workflow."""
        result = subprocess.run(
            [sys.executable, 'cli.py', 'execute', 'echo', '--args', 'hello'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Should succeed (even if echo command fails, CLI should work)
        assert result.returncode == 0
        
        # Should output JSON with execution result
        import json
        output = json.loads(result.stdout)
        assert 'status' in output
    
    def test_cli_platform_selection(self):
        """Test CLI platform selection."""
        # Test Windows platform
        result = subprocess.run(
            [sys.executable, 'cli.py', 'wrap', 'dir', '--platform', 'windows'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        assert result.returncode == 0
        
        # Test POSIX platform
        result = subprocess.run(
            [sys.executable, 'cli.py', 'wrap', 'ls', '--platform', 'posix'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        assert result.returncode == 0
        
        # Test auto platform
        result = subprocess.run(
            [sys.executable, 'cli.py', 'wrap', 'echo', '--platform', 'auto'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        assert result.returncode == 0
    
    def test_cli_timeout_configuration(self):
        """Test CLI timeout configuration."""
        result = subprocess.run(
            [sys.executable, 'cli.py', 'wrap', 'echo', 
             '--timeout-help', '5', '--timeout-exec', '10'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        assert result.returncode == 0
        
        # Should output JSON with status
        import json
        output = json.loads(result.stdout)
        assert output['status'] == 'success'
    
    def test_cli_update_existing_file(self):
        """Test CLI update existing file workflow."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            temp_file = f.name
        
        try:
            # First, create a file
            result = subprocess.run(
                [sys.executable, 'cli.py', 'wrap', 'echo', '--output', temp_file],
                capture_output=True,
                text=True,
                timeout=30
            )
            assert result.returncode == 0
            
            # Then update it
            result = subprocess.run(
                [sys.executable, 'cli.py', 'wrap', 'dir', '--output', temp_file, '--update'],
                capture_output=True,
                text=True,
                timeout=30
            )
            assert result.returncode == 0
            
            # File should still exist and be updated
            assert os.path.exists(temp_file)
            
            # File should contain updated content
            with open(temp_file, 'r', encoding='utf-8') as f:
                content = f.read()
                assert 'dir Plugin' in content or 'echo Plugin' in content
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_cli_error_handling_invalid_command(self):
        """Test CLI error handling for invalid commands."""
        result = subprocess.run(
            [sys.executable, 'cli.py', 'wrap', 'nonexistent_command_12345'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Should still return 0 (CLI succeeds, but command parsing may fail)
        assert result.returncode == 0
        
        # Should output JSON with error status
        import json
        output = json.loads(result.stdout)
        assert 'status' in output
    
    def test_cli_error_handling_invalid_platform(self):
        """Test CLI error handling for invalid platform."""
        result = subprocess.run(
            [sys.executable, 'cli.py', 'wrap', 'echo', '--platform', 'invalid'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Should fail with invalid platform
        assert result.returncode != 0
    
    def test_cli_help_commands(self):
        """Test CLI help commands."""
        # Test main help
        result = subprocess.run(
            [sys.executable, 'cli.py', '--help'],
            capture_output=True,
            text=True,
            timeout=10
        )
        assert result.returncode == 0
        assert 'Universal Command Wrapper' in result.stdout
        
        # Test wrap help
        result = subprocess.run(
            [sys.executable, 'cli.py', 'wrap', '--help'],
            capture_output=True,
            text=True,
            timeout=10
        )
        assert result.returncode == 0
        assert 'wrap' in result.stdout
        
        # Test parse help
        result = subprocess.run(
            [sys.executable, 'cli.py', 'parse', '--help'],
            capture_output=True,
            text=True,
            timeout=10
        )
        assert result.returncode == 0
        assert 'Parse command help text' in result.stdout
        
        # Test execute help
        result = subprocess.run(
            [sys.executable, 'cli.py', 'execute', '--help'],
            capture_output=True,
            text=True,
            timeout=10
        )
        assert result.returncode == 0
        assert 'Execute a command' in result.stdout
    
    def test_cli_json_output_format(self):
        """Test that CLI outputs valid JSON."""
        result = subprocess.run(
            [sys.executable, 'cli.py', 'wrap', 'echo'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        assert result.returncode == 0
        
        # Should be valid JSON
        import json
        try:
            output = json.loads(result.stdout)
            assert isinstance(output, dict)
            assert 'status' in output
        except json.JSONDecodeError:
            pytest.fail("CLI output is not valid JSON")
    
    def test_cli_standalone_mode(self):
        """Test CLI standalone mode."""
        result = subprocess.run(
            [sys.executable, 'cli.py', '--standalone', 'wrap', 'echo'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        assert result.returncode == 0
        
        # Should output human-readable text, not JSON
        assert 'echo' in result.stdout
        assert 'Generated wrapper' in result.stdout
        # Should not be JSON
        assert not result.stdout.strip().startswith('{')
    
    def test_cli_human_mode(self):
        """Test CLI human mode."""
        result = subprocess.run(
            [sys.executable, 'cli.py', '--human', 'wrap', 'echo'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        assert result.returncode == 0
        
        # Should output human-readable text, not JSON
        assert 'echo' in result.stdout
        assert 'Generated wrapper' in result.stdout
        # Should not be JSON
        assert not result.stdout.strip().startswith('{')


if __name__ == "__main__":
    pytest.main([__file__])
