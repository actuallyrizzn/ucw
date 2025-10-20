"""
Unit tests for POSIX parser.

This module tests the PosixParser class functionality.
"""

import pytest
import subprocess
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add the parent directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from parser.posix import PosixParser
from models import CommandSpec, OptionSpec


class TestPosixParser:
    """Test cases for PosixParser."""
    
    def test_init(self):
        """Test PosixParser initialization."""
        parser = PosixParser(timeout=15)
        assert parser.timeout == 15
        
        # Test default timeout
        parser = PosixParser()
        assert parser.timeout == 10
    
    def test_get_help_command(self):
        """Test _get_help_command method."""
        parser = PosixParser()
        
        # Test with command name
        cmd = parser._get_help_command("ls")
        assert cmd == ["ls", "--help"]
        
        # Test with different command
        cmd = parser._get_help_command("grep")
        assert cmd == ["grep", "--help"]
    
    def test_try_alternative_help_success(self):
        """Test _try_alternative_help with successful man command."""
        parser = PosixParser()
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="LS(1)                    User Commands                   LS(1)\n\nNAME\n       ls - list directory contents\n\nSYNOPSIS\n       ls [OPTION]... [FILE]...\n\nDESCRIPTION\n       List  information  about  the FILEs (the current directory by default).\n       Sort entries alphabetically if none of -cftuvSUX nor --sort is specified.\n\n       Mandatory arguments to long options are mandatory for short options too.\n\n       -a, --all\n              do not ignore entries starting with .\n\n       -l     use a long listing format\n\n       -h, --human-readable\n              with -l, print sizes in human readable format (e.g., 1K 234M 2G)\n\n       -r, --reverse\n              reverse order while sorting\n\n       -R, --recursive\n              list subdirectories recursively\n\n       -t     sort by modification time, newest first\n\n       -S     sort by file size, largest first\n\n       -X     sort alphabetically by entry extension\n\n       -U     do not sort; list entries in directory order\n\n       -v     natural sort of (version) numbers within text\n\n       -c     with -l: sort by, and show, ctime (time of last modification of\n              file status information)  with -l: show ctime and sort by name;\n              otherwise: sort by ctime, newest first\n\n       -f     do not sort, enable -aU, disable -ls --color\n\n       -u     with -l: sort by, and show, access time  with -l: show access time\n              and sort by name; otherwise: sort by access time\n\n       --sort=WORD\n              sort by WORD instead of name: none (-U), size (-S), time (-t),\n              version (-v), extension (-X)\n\n       --time=WORD\n              with -l, show time as WORD instead of default modification time:\n              atime (-u); access (-u), use (-u), ctime (-c), or status (-c);\n              use specified time as sort key if --sort=time\n\n       --time-style=STYLE\n              with -l, show times using style STYLE: full-iso, long-iso, iso,\n              locale, or +FORMAT; FORMAT is interpreted like in date(1); if\n              FORMAT is FORMAT1<newline>FORMAT2, then FORMAT1 applies to\n              non-recent files and FORMAT2 to recent files; if STYLE is\n              prefixed with 'posix-', STYLE applies only outside the POSIX\n              locale\n\n       --full-time\n              like -l --time-style=full-iso\n\n       --color[=WHEN]\n              colorize the output; WHEN can be 'never', 'auto', or 'always'\n              (the default); more info below\n\n       --indicator-style=WORD\n              append indicator with style WORD to entry names: none (default),\n              slash (-p), file-type (--file-type), classify (-F)\n\n       --quoting-style=WORD\n              use quoting style WORD for entry names: literal, locale,\n              shell, shell-always, shell-escape, shell-escape-always, c, escape\n\n       --show-control-chars\n              show non graphic characters as-is (default is to display as\n              ^char)\n\n       --hide=PATTERN\n              do not list implied entries matching shell PATTERN (overridden\n              by -a or -A)\n\n       -b, --escape\n              print C-style escapes for nongraphic characters\n\n       -d, --directory\n              list directories themselves, not their contents\n\n       -F, --classify\n              append indicator (one of */=>@|) to entries\n\n       --file-type\n              likewise, except do not append '*' (equivalent to --classify)\n\n       --format=WORD\n              across -x, commas -m, horizontal -x, long -l, single-column -1,\n              verbose -l, vertical -C\n\n       --full-time\n              like -l --time-style=full-iso\n\n       -g     like -l, but do not list owner\n\n       --group-directories-first\n              group directories before files;\n\n              can be used with --sort, but sorting is disabled\n\n       -G, --no-group\n              in a long listing, don't print group names\n\n       -H, --dereference-command-line\n              follow symbolic links listed on the command line\n\n       --dereference-command-line-symlink-to-dir\n              follow each command line symbolic link that points to a directory\n\n       --hide=PATTERN\n              do not list implied entries matching shell PATTERN (overridden\n              by -a or -A)\n\n       --indicator-style=WORD\n              append indicator with style WORD to entry names: none (default),\n              slash (-p), file-type (--file-type), classify (-F)\n\n       -i, --inode\n              print the index number of each file\n\n       -I, --ignore=PATTERN\n              do not list implied entries matching shell PATTERN\n\n       -k, --kibibytes\n              default to 1024-byte blocks\n\n       -l     use a long listing format\n\n       -L, --dereference\n              show information about the link itself rather than the file the\n              link points to\n\n       -m     fill width with a comma separated list of entries\n\n       -n, --numeric-uid-gid\n              like -l, but list numeric user and group IDs\n\n       -N, --literal\n              print entry names without quoting\n\n       -o     like -l, but do not list group information\n\n       -p, --indicator-style=slash\n              append / indicator to directories\n\n       -q, --hide-control-chars\n              print ? instead of non graphic characters\n\n       --show-control-chars\n              show non graphic characters as-is (default is to display as\n              ^char)\n\n       -Q, --quote-name\n              enclose entry names in double quotes\n\n       --quoting-style=WORD\n              use quoting style WORD for entry names: literal, locale,\n              shell, shell-always, shell-escape, shell-escape-always, c, escape\n\n       -r, --reverse\n              reverse order while sorting\n\n       -R, --recursive\n              list subdirectories recursively\n\n       -s, --size\n              print the allocated size of each file, in blocks\n\n       -S     sort by file size, largest first\n\n       -t     sort by modification time, newest first\n\n       -T, --tabsize=COLS\n              assume tab stops at each COLS instead of 8\n\n       -u     with -l: sort by, and show, access time  with -l: show access time\n              and sort by name; otherwise: sort by access time\n\n       -U     do not sort; list entries in directory order\n\n       -v     natural sort of (version) numbers within text\n\n       --version\n              output version information and exit\n\n       -w, --width=COLS\n              assume screen width instead of current value\n\n       -x     list entries by lines instead of by columns\n\n       -X     sort alphabetically by entry extension\n\n       -1     list one file per line\n\n       --help display this help and exit\n\n       --version\n              output version information and exit\n\nAUTHOR\n       Written by Richard M. Stallman and David MacKenzie.\n\nREPORTING BUGS\n       GNU coreutils online help: <https://www.gnu.org/software/coreutils/>\n       Report ls translation bugs to <https://translationproject.org/team/>\n\nCOPYRIGHT\n       Copyright © 2020 Free Software Foundation, Inc.  License GPLv3+: GNU\n       GPL version 3 or later <https://gnu.org/licenses/gpl.html>.\n       This is free software: you are free to change and redistribute it.\n       There is NO WARRANTY, to the extent permitted by law.\n\nSEE ALSO\n       The full documentation for ls is maintained as a Texinfo manual.  If\n       the info and ls programs are properly installed at your site, the\n       command\n\n              info ls\n\n       should give you access to the complete manual.\n\nGNU coreutils 8.32                  September 2020                  LS(1)"
            )
            
            result = parser._try_alternative_help("ls")
            assert result is not None
            assert "LS(1)" in result
            assert "ls - list directory contents" in result
    
    def test_try_alternative_help_failure(self):
        """Test _try_alternative_help with failed man command."""
        parser = PosixParser()
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=1,
                stdout="",
                stderr="No manual entry for nonexistent"
            )
            
            result = parser._try_alternative_help("nonexistent")
            assert result is None
    
    def test_try_alternative_help_timeout(self):
        """Test _try_alternative_help with timeout."""
        parser = PosixParser(timeout=1)
        
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired("man", 1)
            
            result = parser._try_alternative_help("ls")
            assert result is None
    
    def test_is_option_line(self):
        """Test _is_option_line method."""
        parser = PosixParser()
        
        # Test valid option lines
        assert parser._is_option_line("       -a, --all")
        assert parser._is_option_line("       -l     use a long listing format")
        assert parser._is_option_line("       --help display this help and exit")
        assert parser._is_option_line("       -h, --human-readable")
        
        # Test invalid lines
        assert not parser._is_option_line("NAME")
        assert not parser._is_option_line("       List  information  about  the FILEs")
        assert not parser._is_option_line("AUTHOR")
        assert not parser._is_option_line("")
    
    def test_parse_option_line(self):
        """Test _parse_option_line method."""
        parser = PosixParser()
        
        # Test simple option
        option = parser._parse_option_line("       -a, --all")
        assert option.flag == "--all"
        assert option.takes_value is False
        assert option.description == ""
        
        # Test option with description
        option = parser._parse_option_line("       -l     use a long listing format")
        assert option.flag == "-l"
        assert option.takes_value is False
        assert option.description == "use a long listing format"
        
        # Test option with value
        option = parser._parse_option_line("       --width=COLS")
        assert option.flag == "--width"
        assert option.takes_value is True
        assert option.description == ""
        
        # Test complex option
        option = parser._parse_option_line("       -h, --human-readable")
        assert option.flag == "--human-readable"
        assert option.takes_value is False
        assert option.description == ""
    
    def test_parse_command_with_mock_help(self):
        """Test parse_command with mocked help text."""
        parser = PosixParser()
        
        mock_help_text = """LS(1)                    User Commands                   LS(1)

NAME
       ls - list directory contents

SYNOPSIS
       ls [OPTION]... [FILE]...

DESCRIPTION
       List  information  about  the FILEs (the current directory by default).

       -a, --all
              do not ignore entries starting with .

       -l     use a long listing format

       -h, --human-readable
              with -l, print sizes in human readable format

       --help display this help and exit
"""
        
        with patch.object(parser, '_get_help_text', return_value=mock_help_text):
            spec = parser.parse_command("ls")
            
            assert spec.name == "ls"
            assert spec.description == "list directory contents"
            assert len(spec.options) >= 3
            
            # Check specific options
            option_flags = [opt.flag for opt in spec.options]
            assert "--all" in option_flags
            assert "-l" in option_flags
            assert "--human-readable" in option_flags
    
    def test_parse_command_with_alternative_help(self):
        """Test parse_command using alternative help (man page)."""
        parser = PosixParser()
        
        mock_man_text = """LS(1)                    User Commands                   LS(1)

NAME
       ls - list directory contents

SYNOPSIS
       ls [OPTION]... [FILE]...

DESCRIPTION
       List  information  about  the FILEs.

       -a, --all
              do not ignore entries starting with .

       -l     use a long listing format
"""
        
        with patch.object(parser, '_get_help_text', return_value=""):
            with patch.object(parser, '_try_alternative_help', return_value=mock_man_text):
                spec = parser.parse_command("ls")
                
                assert spec.name == "ls"
                assert spec.description == "list directory contents"
                assert len(spec.options) >= 2
    
    def test_parse_command_no_help_available(self):
        """Test parse_command when no help is available."""
        parser = PosixParser()
        
        with patch.object(parser, '_get_help_text', return_value=""):
            with patch.object(parser, '_try_alternative_help', return_value=None):
                spec = parser.parse_command("nonexistent")
                
                assert spec.name == "nonexistent"
                assert spec.description == ""
                assert len(spec.options) == 0


if __name__ == "__main__":
    pytest.main([__file__])
