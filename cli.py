#!/usr/bin/env python3
"""
Universal Command Wrapper (UCW) - CLI Entrypoint

Command-line interface for UCW tool.
"""

import argparse
import sys
from pathlib import Path

from __init__ import UniversalCommandWrapper


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Universal Command Wrapper (UCW) - Generate Python wrappers for system commands",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ucw wrap ls                    # Generate wrapper in memory
  ucw wrap ls --output cli.py   # Generate CLI file
  ucw wrap grep --update tools/cli.py  # Update existing CLI file
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Wrap command
    setup_wrap_command(subparsers)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        if args.command == "wrap":
            execute_wrap_command(args)
        else:
            print(f"Unknown command: {args.command}")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def setup_wrap_command(subparsers):
    """Setup the wrap command."""
    parser = subparsers.add_parser("wrap", help="Wrap a system command")
    parser.add_argument("command_name", help="Name of the command to wrap")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--update", "-u", action="store_true", 
                       help="Update existing file")
    parser.add_argument("--platform", choices=["windows", "posix", "auto"],
                       default="auto", help="Target platform")


def execute_wrap_command(args):
    """Execute the wrap command."""
    # Initialize UCW
    platform_name = args.platform if args.platform != "auto" else None
    ucw = UniversalCommandWrapper(platform_name=platform_name)
    
    if args.output:
        # Generate file
        file_path = ucw.write_wrapper(
            args.command_name,
            output=args.output,
            update=args.update
        )
        print(f"Generated wrapper for '{args.command_name}' in {file_path}")
    else:
        # Generate in-memory wrapper
        wrapper = ucw.write_wrapper(args.command_name)
        
        # Test the wrapper
        print(f"Generated wrapper for '{args.command_name}'")
        print(f"Usage: wrapper.run({', '.join([opt.flag for opt in wrapper.spec.options[:3]])})")
        
        # Show available options
        if wrapper.spec.options:
            print("\nAvailable options:")
            for option in wrapper.spec.options:
                print(f"  {option.flag}: {option.description or 'No description'}")


if __name__ == "__main__":
    main()
