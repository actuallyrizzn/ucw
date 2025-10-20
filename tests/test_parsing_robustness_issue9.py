"""
Test suite for Issue #9: Parsing robustness with real-world commands.
Tests complex help formats that our current parsers miss.
"""

import pytest
import sys
sys.path.append('.')

from parser.windows import WindowsParser
from parser.posix import PosixParser
from models import CommandSpec, OptionSpec


class TestParsingRobustnessIssue9:
    """Test cases demonstrating parsing robustness issues with real commands."""
    
    def test_windows_dir_command_return_code_issue(self):
        """Test that Windows dir command fails due to return code strictness."""
        parser = WindowsParser()
        
        # This should work but currently fails because dir /? returns exit code 1
        spec = parser.parse_command("dir")
        
        print(f"Windows dir command parsing:")
        print(f"  Options found: {len(spec.options)}")
        print(f"  Usage: '{spec.usage}'")
        print(f"  Description: '{spec.description}'")
        
        # This test will FAIL because current parser finds 0 options
        # but dir command has 14+ options when parsed correctly
        assert len(spec.options) >= 10, f"Expected at least 10 options, found {len(spec.options)}"
    
    def test_posix_ffmpeg_command_complex_format(self):
        """Test that ffmpeg command has complex help format that may not parse correctly."""
        parser = PosixParser()
        
        # ffmpeg has complex multi-line synopsis and grouped options
        spec = parser.parse_command("ffmpeg")
        
        print(f"POSIX ffmpeg command parsing:")
        print(f"  Options found: {len(spec.options)}")
        print(f"  Usage: '{spec.usage}'")
        print(f"  Description: '{spec.description}'")
        
        # ffmpeg should have many options
        assert len(spec.options) >= 20, f"Expected at least 20 options, found {len(spec.options)}"
        
        # Check for specific complex options
        option_flags = [opt.flag for opt in spec.options]
        assert "-h" in option_flags, "Missing -h option"
        assert "-v" in option_flags, "Missing -v option"
        assert "-f" in option_flags, "Missing -f option"
    
    def test_posix_ytdlp_command_massive_options(self):
        """Test that yt-dlp command has massive option list that may not parse correctly."""
        parser = PosixParser()
        
        # yt-dlp has 200+ options with complex formats
        spec = parser.parse_command("yt-dlp")
        
        print(f"POSIX yt-dlp command parsing:")
        print(f"  Options found: {len(spec.options)}")
        print(f"  Usage: '{spec.usage}'")
        print(f"  Description: '{spec.description}'")
        
        # yt-dlp should have many options (200+)
        assert len(spec.options) >= 50, f"Expected at least 50 options, found {len(spec.options)}"
        
        # Check for specific complex options
        option_flags = [opt.flag for opt in spec.options]
        assert "--help" in option_flags, "Missing --help option"
        assert "--version" in option_flags, "Missing --version option"
        assert "--format" in option_flags, "Missing --format option"
    
    def test_complex_option_formats_not_handled(self):
        """Test that complex option formats are not being parsed correctly."""
        parser = WindowsParser()
        
        # Test individual complex option lines that current regexes miss
        complex_lines = [
            "  /A[[:]attributes]    Displays files with specified attributes.",
            "  /O[[:]sortorder]    List by files in sorted order.",
            "  /T[[:]timefield]    Controls which time field displayed",
            "  -c[:<stream_spec>] <codec>  select encoder/decoder",
            "  --format-sort SORTORDER    Sort the formats by the fields",
            "  --match-filters FILTER    Generic video filter"
        ]
        
        parsed_options = []
        for line in complex_lines:
            option = parser._parse_option_line(line)
            if option:
                parsed_options.append(option)
        
        print(f"Parsed {len(parsed_options)} out of {len(complex_lines)} complex option lines")
        for opt in parsed_options:
            print(f"  {opt.flag}: {opt.description}")
        
        # This test will FAIL because current parser can't handle complex formats
        assert len(parsed_options) >= 4, f"Expected at least 4 options parsed, found {len(parsed_options)}"
    
    def test_multi_line_usage_not_parsed(self):
        """Test that multi-line usage statements are not being parsed correctly."""
        parser = PosixParser()
        
        # Multi-line usage from ffmpeg
        multi_line_usage = """usage: ffmpeg [options] [[infile options] -i infile]... {[outfile options] outfile}...

Getting help:
    -h      -- print basic options
    -h long -- print more options
    -h full -- print all options (including all format and codec specific options, very long)"""
        
        usage = parser._extract_usage(multi_line_usage)
        
        print(f"Extracted usage: '{usage}'")
        
        # This test will FAIL because current parser doesn't handle multi-line usage
        assert len(usage) > 50, f"Expected substantial usage text, got: '{usage}'"
        assert "ffmpeg" in usage, "Missing ffmpeg in usage"
        assert "options" in usage, "Missing options in usage"
    
    def test_return_code_strictness_issue(self):
        """Test that return code strictness causes parsing failures."""
        parser = WindowsParser()
        
        # Test what happens when we get help text with non-zero return code
        help_text = """Displays a list of files and subdirectories in a directory.

DIR [drive:][path][filename] [/A[[:]attributes]] [/B] [/C] [/D] [/L] [/N]
  [/O[[:]sortorder]] [/P] [/Q] [/R] [/S] [/T[[:]timefield]] [/W] [/X] [/4]

  /A          Displays files with specified attributes.
  /B          Uses bare format (no heading information or summary).
  /C          Display the thousand separator in file sizes."""
        
        spec = parser._parse_help_text("dir", help_text)
        
        print(f"Manual help text parsing:")
        print(f"  Options found: {len(spec.options)}")
        print(f"  Usage: '{spec.usage}'")
        
        # This should work when we manually provide help text
        assert len(spec.options) >= 3, f"Expected at least 3 options, found {len(spec.options)}"
        
        # Check for specific options
        option_flags = [opt.flag for opt in spec.options]
        assert "/A" in option_flags, "Missing /A option"
        assert "/B" in option_flags, "Missing /B option"
        assert "/C" in option_flags, "Missing /C option"


if __name__ == "__main__":
    # Run the tests to see the parsing issues
    test = TestParsingRobustnessIssue9()
    
    print("=== Testing Windows dir command return code issue ===")
    try:
        test.test_windows_dir_command_return_code_issue()
    except AssertionError as e:
        print(f"FAILED: {e}")
    
    print("\n=== Testing POSIX ffmpeg command complex format ===")
    try:
        test.test_posix_ffmpeg_command_complex_format()
    except AssertionError as e:
        print(f"FAILED: {e}")
    
    print("\n=== Testing POSIX yt-dlp command massive options ===")
    try:
        test.test_posix_ytdlp_command_massive_options()
    except AssertionError as e:
        print(f"FAILED: {e}")
    
    print("\n=== Testing complex option formats ===")
    try:
        test.test_complex_option_formats_not_handled()
    except AssertionError as e:
        print(f"FAILED: {e}")
    
    print("\n=== Testing multi-line usage ===")
    try:
        test.test_multi_line_usage_not_parsed()
    except AssertionError as e:
        print(f"FAILED: {e}")
    
    print("\n=== Testing return code strictness ===")
    try:
        test.test_return_code_strictness_issue()
    except AssertionError as e:
        print(f"FAILED: {e}")