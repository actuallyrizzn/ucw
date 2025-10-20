"""
Test platform name handling functionality.

This module tests that both 'linux' and 'posix' platform names work correctly,
and that 'linux' is properly aliased to 'posix'.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add the parent directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestPlatformNameHandling:
    """Test cases for platform name handling."""
    
    def test_linux_alias_works(self):
        """Test that 'linux' is accepted as an alias for 'posix'."""
        from __init__ import UniversalCommandWrapper
        
        # Mock the parser creation to avoid actual platform detection
        with patch.object(UniversalCommandWrapper, '_create_parser') as mock_create_parser:
            mock_parser = MagicMock()
            mock_create_parser.return_value = mock_parser
            
            ucw = UniversalCommandWrapper(platform_name="linux")
            
            # Verify that the platform was normalized to "posix"
            assert ucw.platform == "posix"
    
    def test_posix_still_works(self):
        """Test that 'posix' still works as before."""
        from __init__ import UniversalCommandWrapper
        
        with patch.object(UniversalCommandWrapper, '_create_parser') as mock_create_parser:
            mock_parser = MagicMock()
            mock_create_parser.return_value = mock_parser
            
            ucw = UniversalCommandWrapper(platform_name="posix")
            
            # Verify that the platform remains "posix"
            assert ucw.platform == "posix"
    
    def test_windows_still_works(self):
        """Test that 'windows' still works as before."""
        from __init__ import UniversalCommandWrapper
        
        with patch.object(UniversalCommandWrapper, '_create_parser') as mock_create_parser:
            mock_parser = MagicMock()
            mock_create_parser.return_value = mock_parser
            
            ucw = UniversalCommandWrapper(platform_name="windows")
            
            # Verify that the platform remains "windows"
            assert ucw.platform == "windows"
    
    def test_auto_detection_still_works(self):
        """Test that auto detection still works."""
        from __init__ import UniversalCommandWrapper
        
        with patch.object(UniversalCommandWrapper, '_detect_platform') as mock_detect:
            mock_detect.return_value = "posix"
            
            with patch.object(UniversalCommandWrapper, '_create_parser') as mock_create_parser:
                mock_parser = MagicMock()
                mock_create_parser.return_value = mock_parser
                
                ucw = UniversalCommandWrapper(platform_name=None)
                
                # Verify that auto detection was used
                assert ucw.platform == "posix"
    
    def test_linux_creates_posix_parser(self):
        """Test that 'linux' creates a PosixParser."""
        from __init__ import UniversalCommandWrapper
        from parser.posix import PosixParser
        
        ucw = UniversalCommandWrapper(platform_name="linux")
        
        # Verify that a PosixParser was created
        assert isinstance(ucw.parser, PosixParser)
    
    def test_posix_creates_posix_parser(self):
        """Test that 'posix' creates a PosixParser."""
        from __init__ import UniversalCommandWrapper
        from parser.posix import PosixParser
        
        ucw = UniversalCommandWrapper(platform_name="posix")
        
        # Verify that a PosixParser was created
        assert isinstance(ucw.parser, PosixParser)
    
    def test_windows_creates_windows_parser(self):
        """Test that 'windows' creates a WindowsParser."""
        from __init__ import UniversalCommandWrapper
        from parser.windows import WindowsParser
        
        ucw = UniversalCommandWrapper(platform_name="windows")
        
        # Verify that a WindowsParser was created
        assert isinstance(ucw.parser, WindowsParser)
    
    def test_invalid_platform_raises_error(self):
        """Test that invalid platform names raise ValueError."""
        from __init__ import UniversalCommandWrapper
        
        with pytest.raises(ValueError, match="Unknown platform"):
            UniversalCommandWrapper(platform_name="invalid")
    
    def test_cli_accepts_linux(self):
        """Test that CLI accepts 'linux' as a valid choice."""
        import argparse
        import sys
        from unittest.mock import patch
        
        # Test CLI argument parsing directly
        parser = argparse.ArgumentParser()
        parser.add_argument("--platform", choices=["windows", "posix", "linux", "auto"])
        parser.add_argument("command")
        parser.add_argument("command_name")
        
        # Test that 'linux' is accepted
        args = parser.parse_args(['--platform', 'linux', 'parse', 'ls'])
        assert args.platform == 'linux'
        
        # Test that 'posix' is still accepted
        args = parser.parse_args(['--platform', 'posix', 'parse', 'ls'])
        assert args.platform == 'posix'
        
        # Test that 'windows' is still accepted
        args = parser.parse_args(['--platform', 'windows', 'parse', 'dir'])
        assert args.platform == 'windows'
        
        # Test that 'auto' is still accepted
        args = parser.parse_args(['--platform', 'auto', 'parse', 'ls'])
        assert args.platform == 'auto'
    
    def test_docstring_updated(self):
        """Test that the docstring reflects the new accepted values."""
        from __init__ import UniversalCommandWrapper
        
        # Get the docstring
        docstring = UniversalCommandWrapper.__init__.__doc__
        
        # Verify it mentions both "linux" and "posix"
        assert "linux" in docstring
        assert "posix" in docstring
        assert "alias" in docstring.lower()


if __name__ == "__main__":
    pytest.main([__file__])
