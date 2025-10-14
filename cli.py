#!/usr/bin/env python3
"""
Universal Command Wrapper (UCW) - SMCP Plugin

SMCP-compatible plugin for generating Python wrappers for system commands.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any

from __init__ import UniversalCommandWrapper


def main():
    """Main SMCP plugin entry point."""
    parser = argparse.ArgumentParser(
        description="Universal Command Wrapper (UCW) - SMCP Plugin for generating Python wrappers for system commands"
    )
    
    # Global options
    parser.add_argument("--standalone", "--human", action="store_true",
                       help="Use human-readable output instead of JSON (for standalone usage)")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Add commands
    setup_wrap_command(subparsers)
    setup_parse_command(subparsers)
    setup_execute_command(subparsers)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        # Execute the appropriate command and return JSON result
        if args.command == "wrap":
            result = execute_wrap_command(args)
        elif args.command == "parse":
            result = execute_parse_command(args)
        elif args.command == "execute":
            result = execute_execute_command(args)
        else:
            result = {"status": "error", "error": f"Unknown command: {args.command}"}
        
        # Output result based on mode
        if args.standalone:
            print_human_readable(result)
        else:
            # Output JSON result for SMCP compatibility
            print(json.dumps(result, indent=2))
        
    except Exception as e:
        error_result = {"status": "error", "error": str(e)}
        if args.standalone:
            print(f"Error: {error_result['error']}")
        else:
            print(json.dumps(error_result, indent=2))
        sys.exit(1)


def print_human_readable(result: Dict[str, Any]):
    """Print result in human-readable format for standalone usage."""
    if result.get("status") == "error":
        print(f"Error: {result['error']}")
        return
    
    if result.get("status") != "success":
        print(f"Unknown status: {result.get('status', 'unknown')}")
        return
    
    # Handle wrap command results
    if "message" in result and "spec" in result:
        print(result["message"])
        
        if "output_file" in result:
            print(f"Output file: {result['output_file']}")
            if result.get("update_mode"):
                print("Mode: Updated existing file")
            else:
                print("Mode: Created new file")
            return
        
        # Show command specification
        spec = result["spec"]
        print(f"\nCommand: {spec['name']}")
        print(f"Usage: {spec['usage']}")
        
        if spec.get("description"):
            print(f"Description: {spec['description']}")
        
        # Show positional arguments
        if spec.get("positional_args"):
            print(f"\nPositional arguments:")
            for i, arg in enumerate(spec["positional_args"]):
                req_str = "required" if arg["required"] else "optional"
                var_str = " (variadic)" if arg["variadic"] else ""
                print(f"  {i+1}. {arg['name']} ({req_str}, {arg['type_hint']}){var_str}")
        
        # Show options
        if spec.get("options"):
            print(f"\nAvailable options:")
            for option in spec["options"]:
                value_indicator = " <value>" if option["takes_value"] else ""
                print(f"  {option['flag']}{value_indicator}: {option['description'] or 'No description'}")
    
    # Handle parse command results
    elif "spec" in result:
        spec = result["spec"]
        print(f"Parsed command: {spec['name']}")
        print(f"Usage: {spec['usage']}")
        
        if spec.get("description"):
            print(f"Description: {spec['description']}")
        
        # Show positional arguments
        if spec.get("positional_args"):
            print(f"\nPositional arguments:")
            for i, arg in enumerate(spec["positional_args"]):
                req_str = "required" if arg["required"] else "optional"
                var_str = " (variadic)" if arg["variadic"] else ""
                print(f"  {i+1}. {arg['name']} ({req_str}, {arg['type_hint']}){var_str}")
        
        # Show options
        if spec.get("options"):
            print(f"\nAvailable options:")
            for option in spec["options"]:
                value_indicator = " <value>" if option["takes_value"] else ""
                print(f"  {option['flag']}{value_indicator}: {option['description'] or 'No description'}")
    
    # Handle execute command results
    elif "execution" in result:
        exec_info = result["execution"]
        print(f"Executed command: {result['command']}")
        print(f"Command line: {exec_info['command_line']}")
        print(f"Return code: {exec_info['return_code']}")
        print(f"Success: {exec_info['success']}")
        print(f"Elapsed time: {exec_info['elapsed']:.3f}s")
        
        if exec_info.get("stdout"):
            print(f"\nOutput:")
            print(exec_info["stdout"].rstrip())
        
        if exec_info.get("stderr"):
            print(f"\nErrors:")
            print(exec_info["stderr"].rstrip())
    
    # Handle other success messages
    elif "message" in result:
        print(result["message"])
    
    else:
        print("Command completed successfully")


def setup_wrap_command(subparsers):
    """Setup the wrap command."""
    parser = subparsers.add_parser("wrap", help="Wrap a system command")
    parser.add_argument("command_name", help="Name of the command to wrap")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--update", "-u", action="store_true", 
                       help="Update existing file")
    parser.add_argument("--platform", choices=["windows", "posix", "auto"],
                       default="auto", help="Target platform")


def setup_parse_command(subparsers):
    """Setup the parse command."""
    parser = subparsers.add_parser("parse", help="Parse a command's help text")
    parser.add_argument("command_name", help="Name of the command to parse")
    parser.add_argument("--platform", choices=["windows", "posix", "auto"],
                       default="auto", help="Target platform")


def setup_execute_command(subparsers):
    """Setup the execute command."""
    parser = subparsers.add_parser("execute", help="Execute a wrapped command")
    parser.add_argument("command_name", help="Name of the command to execute")
    parser.add_argument("--args", nargs="*", help="Positional arguments")
    parser.add_argument("--options", help="JSON string of options")
    parser.add_argument("--platform", choices=["windows", "posix", "auto"],
                       default="auto", help="Target platform")


def execute_wrap_command(args) -> Dict[str, Any]:
    """Execute the wrap command."""
    try:
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
            return {
                "status": "success",
                "message": f"Generated wrapper for '{args.command_name}' in {file_path}",
                "command": args.command_name,
                "output_file": file_path,
                "update_mode": args.update
            }
        else:
            # Generate in-memory wrapper
            wrapper = ucw.write_wrapper(args.command_name)
            
            # Prepare result data
            result = {
                "status": "success",
                "message": f"Generated wrapper for '{args.command_name}'",
                "command": args.command_name,
                "spec": {
                    "name": wrapper.spec.name,
                    "usage": wrapper.spec.usage,
                    "description": wrapper.spec.description,
                    "positional_args": [],
                    "options": []
                }
            }
            
            # Add positional arguments
            if wrapper.spec.positional_args:
                result["spec"]["positional_args"] = [
                    {
                        "name": arg.name,
                        "required": arg.required,
                        "variadic": arg.variadic,
                        "type_hint": arg.type_hint
                    }
                    for arg in wrapper.spec.positional_args
                ]
            
            # Add options
            if wrapper.spec.options:
                result["spec"]["options"] = [
                    {
                        "flag": option.flag,
                        "takes_value": option.takes_value,
                        "description": option.description,
                        "type_hint": option.type_hint
                    }
                    for option in wrapper.spec.options
                ]
            
            return result
            
    except Exception as e:
        return {"status": "error", "error": str(e)}


def execute_parse_command(args) -> Dict[str, Any]:
    """Execute the parse command."""
    try:
        # Initialize UCW
        platform_name = args.platform if args.platform != "auto" else None
        ucw = UniversalCommandWrapper(platform_name=platform_name)
        
        # Parse command
        spec = ucw.parse_command(args.command_name)
        
        return {
            "status": "success",
            "command": args.command_name,
            "spec": {
                "name": spec.name,
                "usage": spec.usage,
                "description": spec.description,
                "positional_args": [
                    {
                        "name": arg.name,
                        "required": arg.required,
                        "variadic": arg.variadic,
                        "type_hint": arg.type_hint
                    }
                    for arg in spec.positional_args
                ],
                "options": [
                    {
                        "flag": option.flag,
                        "takes_value": option.takes_value,
                        "description": option.description,
                        "type_hint": option.type_hint
                    }
                    for option in spec.options
                ]
            }
        }
        
    except Exception as e:
        return {"status": "error", "error": str(e)}


def execute_execute_command(args) -> Dict[str, Any]:
    """Execute the execute command."""
    try:
        # Initialize UCW
        platform_name = args.platform if args.platform != "auto" else None
        ucw = UniversalCommandWrapper(platform_name=platform_name)
        
        # Parse command and build wrapper
        spec = ucw.parse_command(args.command_name)
        wrapper = ucw.build_wrapper(spec)
        
        # Parse options if provided
        options = {}
        if args.options:
            try:
                options = json.loads(args.options)
            except json.JSONDecodeError as e:
                return {"status": "error", "error": f"Invalid JSON options: {e}"}
        
        # Execute command
        positional_args = args.args if args.args is not None else []
        result = wrapper.run(*positional_args, **options)
        
        return {
            "status": "success",
            "command": args.command_name,
            "execution": {
                "command_line": result.command,
                "return_code": result.return_code,
                "success": result.success,
                "elapsed": result.elapsed,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        }
        
    except Exception as e:
        return {"status": "error", "error": str(e)}


if __name__ == "__main__":
    main()
