# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-01-08

### Added
- Complete project transformation to modern Python package
- Modular src-based architecture with clean separation:
  - `src/audit_packages_tool/models/` - Data structures and enums
  - `src/audit_packages_tool/scanner/` - Package detection logic
  - `src/audit_packages_tool/reporting/` - Output formatting
  - `src/audit_packages_tool/cli.py` - Command-line interface
- Professional pip-installable package (`pip install audit-packages-tool`)
- Console script entry point: `audit-packages` command
- Comprehensive pyproject.toml configuration
- Multi-platform CI/CD pipeline (Linux, Windows, macOS × Python 3.9-3.12)
- Docker containerization with multi-arch support
- Comprehensive test suite with 19 unit tests
- Static analysis with ruff and mypy (strict typing)
- Professional documentation with badges and architecture overview
- Automated releases with semantic versioning
- Support for pip, npm, cargo, brew package managers
- Intelligent executable vs library detection
- JSON export functionality with structured data
- Package search capability by name or description
- Enhanced error handling with user-friendly messages
- Security scanning with Dependabot and automated dependency updates

### Changed
- **BREAKING**: Migrated from `python audit_packages.py` to `audit-packages` command
- Enhanced CLI with professional argument parsing and help system
- Improved package detection algorithms
- Better error handling and type safety throughout

### Removed
- Deprecated `audit_packages.py` script (replaced by modular package)

### Security
- Docker containers run as non-root user
- Hash-pinned dependencies for supply chain security
- Automated security scanning in CI/CD pipeline
- Dependabot for automated dependency updates
