# Changelog

All notable changes to the Universal Command Wrapper (UCW) project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive documentation suite
- API reference documentation
- User guide with examples
- Developer guide for contributors
- AGPL-3.0 license for source code
- CC BY-SA 4.0 license for documentation

### Changed
- Updated project structure for better organization
- Enhanced error handling and validation

## [1.1.0] - 2025-10-20

### Added
- **Issue Resolution**: Comprehensive fix for all open issues (#1-#12)
- **Parsing Robustness**: Enhanced Windows and POSIX parser robustness
  - Support for complex help formats and non-zero return codes
  - Improved regex patterns for complex option formats
  - Better handling of Windows commands like `dir /?`
- **Configurable Timeouts**: Added `timeout_help` and `timeout_exec` parameters
- **Platform Support**: Added "linux" alias for "posix" platform
- **Test Suite**: Comprehensive pytest-based test suite with 90%+ coverage
- **Requirements Management**: Separated production and testing dependencies
- **Documentation**: Fixed documentation drift and added comprehensive guides

### Fixed
- **Issue #1**: Removed duplicate BaseParser and eliminated shell=True usage
- **Issue #2**: Added missing subprocess import in Windows parser
- **Issue #3**: Removed duplicate WrapperBuilder class
- **Issue #4**: Fixed generated plugin argparse attribute names
- **Issue #5**: Fixed CommandWrapper kwargs mapping mismatches
- **Issue #6**: Fixed FileWriter update mode duplication
- **Issue #7**: Added linux alias for posix platform name
- **Issue #8**: Converted tests to proper pytest format
- **Issue #9**: Enhanced parsing robustness for complex help formats
- **Issue #10**: Added configurable timeout support
- **Issue #12**: Fixed documentation drift and API alignment

### Changed
- **Enhanced Parsing**: More robust help text parsing with flexible return codes
- **Better Error Handling**: Improved error messages and validation
- **Test Coverage**: Expanded from basic tests to comprehensive suite
- **Documentation**: Updated all documentation to reflect current API
- **Requirements**: Separated production and development dependencies

## [1.0.0] - 2025-10-20

### Added
- **Core Functionality**
  - Universal Command Wrapper (UCW) main class
  - Cross-platform command parsing (Windows and POSIX)
  - Automatic help text extraction and parsing
  - Command specification generation with type inference

- **Parser System**
  - Abstract BaseParser class with common functionality
  - WindowsParser for Windows command help (`command /?`)
  - PosixParser for POSIX command help (`command --help`, `man command`)
  - Support for various option formats:
    - Windows: `/option`, `/option:value`
    - POSIX: `-o`, `--option`, `--option=value`, `-o, --option`

- **Data Models**
  - CommandSpec: Complete command specification
  - OptionSpec: Command options/flags with type hints
  - PositionalArgSpec: Positional arguments with variadic support
  - ExecutionResult: Structured command execution results

- **Wrapper Generation**
  - CommandWrapper: Executable command wrappers
  - Support for both options and positional arguments
  - Automatic command line construction
  - Error handling and timeout management

- **CLI Interface**
  - Command-line tool (`ucw wrap <command>`)
  - In-memory wrapper generation
  - CLI file generation and updates
  - Platform-specific parsing options

- **SMCP Integration**
  - Designed as a plugin for SMCP (Simple MCP)
  - MCP plugin code generation
  - Complete plugin file creation
  - Compatible with MCP servers
  - Structured JSON output format

- **File Management**
  - New CLI file creation
  - Existing file updates with section tagging
  - Preservation of existing content
  - Executable file permissions

- **Type Inference**
  - Automatic type detection from help text
  - Support for common types: `str`, `int`, `path`, `bool`
  - Context-aware type inference
  - Positional argument type detection

- **Positional Arguments**
  - Full support for positional arguments
  - Required and optional argument detection
  - Variadic argument support (`FILE...`)
  - Proper argument ordering and validation

### Technical Features
- **Zero Dependencies**: Uses only Python standard library
- **Cross-Platform**: Works on Windows, Linux, macOS
- **Timeout Handling**: Configurable timeouts for command execution
- **Error Recovery**: Graceful handling of parsing failures
- **Memory Efficient**: Minimal memory footprint
- **Extensible**: Plugin architecture for custom parsers

### Supported Commands
- **File Operations**: `ls`, `cp`, `mv`, `rm`, `mkdir`, `chmod`
- **Text Processing**: `grep`, `sort`, `sed`, `awk`
- **System Information**: `ps`, `top`, `df`, `du`
- **Archive Operations**: `tar`, `zip`, `unzip`
- **Network Tools**: `wget`, `curl`, `ping`
- **Development Tools**: `git`, `make`, `gcc`

### Testing
- Comprehensive test suite
- Cross-platform testing
- Command validation tests
- Error handling tests
- Performance benchmarks

## [0.9.0] - 2025-10-20

### Added
- Initial implementation of UCW core functionality
- Basic command parsing for Windows and POSIX
- Simple wrapper generation
- CLI interface prototype

### Changed
- Refactored parser architecture
- Improved option detection algorithms
- Enhanced type inference system

## [0.8.0] - 2025-10-20

### Added
- Windows parser implementation
- POSIX parser implementation
- Basic option parsing
- Command specification models

### Fixed
- Fixed subprocess execution issues
- Resolved help text parsing problems
- Corrected option line detection

## [0.7.0] - 2025-10-20

### Added
- Initial parser framework
- Base parser class
- Command help text extraction
- Basic option detection

### Changed
- Improved regex patterns for option parsing
- Enhanced error handling
- Better timeout management

## [0.6.0] - 2025-10-20

### Added
- Core data models
- Command specification structure
- Option and argument models
- Execution result model

### Changed
- Refactored data structures
- Improved type hints
- Enhanced model validation

## [0.5.0] - 2025-10-20

### Added
- Initial project structure
- Basic CLI interface
- Command wrapper concept
- File generation framework

### Changed
- Project organization
- Documentation structure
- Development workflow

## [0.4.0] - 2025-10-20

### Added
- Project planning and design
- Architecture documentation
- Technical specifications
- Development roadmap

### Changed
- Project scope definition
- Feature prioritization
- Implementation strategy

## [0.3.0] - 2025-10-20

### Added
- Initial project concept
- Use case analysis
- Requirements gathering
- Technical feasibility study

### Changed
- Project direction
- Feature set definition
- Target audience identification

## [0.2.0] - 2025-10-20

### Added
- Project idea documentation
- Problem statement
- Solution approach
- Initial research

### Changed
- Project focus
- Technical approach
- Implementation strategy

## [0.1.0] - 2025-10-14

### Added
- Initial project setup
- Repository creation
- Basic documentation
- Development environment

---

## Version Numbering

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR** version for incompatible API changes
- **MINOR** version for functionality added in a backwards compatible manner
- **PATCH** version for backwards compatible bug fixes

## Release Process

1. **Development**: Features developed in feature branches
2. **Testing**: Comprehensive testing on multiple platforms
3. **Documentation**: Updated documentation for new features
4. **Release**: Tagged releases with changelog updates
5. **Distribution**: Available via GitHub releases

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.

## License

- **Source Code**: GNU Affero General Public License v3.0 (AGPL-3.0)
- **Documentation**: Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)

For more information, see [LICENSE](LICENSE) and [LICENSE-DOCS](LICENSE-DOCS).
