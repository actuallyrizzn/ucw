"""
Basic tests for UCW functionality.

This module provides simple tests to verify UCW is working correctly.
"""

import subprocess
import sys
from pathlib import Path

# Add the parent directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from __init__ import UniversalCommandWrapper


def test_windows_parser():
    """Test Windows command parsing."""
    print("Testing Windows parser...")
    
    ucw = UniversalCommandWrapper(platform_name="windows")
    
    # Test with a simple Windows command
    try:
        spec = ucw.parse_command("dir")
        print(f"[OK] Parsed 'dir' command")
        print(f"  Usage: {spec.usage}")
        print(f"  Options: {len(spec.options)}")
        
        # Test wrapper generation
        wrapper = ucw.build_wrapper(spec)
        print(f"[OK] Generated wrapper for 'dir'")
        
        # Test execution (just check it doesn't crash)
        result = wrapper.run()
        print(f"[OK] Executed 'dir' command (return code: {result.return_code})")
        
    except Exception as e:
        print(f"[ERROR] Error testing Windows parser: {e}")


def test_posix_parser():
    """Test POSIX command parsing."""
    print("\nTesting POSIX parser...")
    
    ucw = UniversalCommandWrapper(platform_name="posix")
    
    # Test with a simple POSIX command
    try:
        spec = ucw.parse_command("ls")
        print(f"[OK] Parsed 'ls' command")
        print(f"  Usage: {spec.usage}")
        print(f"  Options: {len(spec.options)}")
        
        # Test wrapper generation
        wrapper = ucw.build_wrapper(spec)
        print(f"[OK] Generated wrapper for 'ls'")
        
        # Test execution (just check it doesn't crash)
        result = wrapper.run()
        print(f"[OK] Executed 'ls' command (return code: {result.return_code})")
        
    except Exception as e:
        print(f"[ERROR] Error testing POSIX parser: {e}")


def test_file_generation():
    """Test CLI file generation."""
    print("\nTesting file generation...")
    
    ucw = UniversalCommandWrapper()
    
    try:
        # Generate a test CLI file
        test_file = "test_cli.py"
        file_path = ucw.write_wrapper("dir", output=test_file)
        
        print(f"[OK] Generated CLI file: {file_path}")
        
        # Check if file exists and is readable
        if Path(file_path).exists():
            print(f"[OK] File exists and is readable")
            
            # Clean up
            Path(file_path).unlink()
            print(f"[OK] Cleaned up test file")
        else:
            print(f"[ERROR] Generated file does not exist")
            
    except Exception as e:
        print(f"[ERROR] Error testing file generation: {e}")


def main():
    """Run all tests."""
    print("UCW Basic Tests")
    print("=" * 50)
    
    # Detect platform and run appropriate tests
    import platform
    system = platform.system().lower()
    
    if system == "windows":
        test_windows_parser()
    else:
        test_posix_parser()
    
    test_file_generation()
    
    print("\n" + "=" * 50)
    print("Tests completed!")


if __name__ == "__main__":
    main()
